# Module 3 · Lesson 10: From Source Code to Machine Code

> **Course:** Self-Paced CS50x
> **Module 3:** Debugging and what the compiler hides: debug systematically and see how C really stores data
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 2 - Arrays](https://www.youtube.com/watch?v=h5Gc1n8ZuU8) · [full transcript](../../transcripts/04-lecture-2-arrays.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Every time you run `make`, your C file secretly passes through four separate translation steps (preprocessing, compiling, assembling, and linking) before it becomes a runnable program, and once it runs, every variable you declare takes up an exact, predictable number of bytes inside one giant addressable grid of memory called RAM.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you manually run each of the four hidden build steps against a real `hello.c` (producing and inspecting the file `make` normally hides at every stage) and then measure, in bytes, exactly how much memory six different C data types actually cost. Everything before the Capstone teaches the ideas you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Clang and cs50.dev will not exist forever in their current form, but the ideas underneath them are decades old and tool-agnostic. For the timeless, tool-agnostic versions:
>
> - **[*The C Programming Language*](https://en.wikipedia.org/wiki/The_C_Programming_Language) by Brian Kernighan and Dennis Ritchie (1978).** Often called "K&R," this is the original, canonical book defining C's basic data types (`int`, `char`, `float`, `double`, and friends) and the mental model of a program as source text that gets translated before it runs. Tools change; the language it defines is still the one you are writing.
> - **[*Compilers: Principles, Techniques, and Tools*](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools) by Alfred Aho, Monica Lam, Ravi Sethi, and Jeffrey Ullman.** Nicknamed "the Dragon Book," this is the classic, durable reference on what a compiler actually does in stages: the timeless version of the preprocess/compile/assemble/link pipeline you'll walk through below.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Compiler:** the program that translates source code (the C you type) into machine code (the zeros and ones a computer's processor can actually run).
- **Header file:** a file such as `stdio.h` or `cs50.h` that tells the compiler "this function exists, and here is its shape," so you can call functions that were written and already translated somewhere else.
- **Preprocessing:** the very first build step, where every `#include` line in your file gets replaced by the actual contents of that header file, before any translation happens.
- **Assembly code:** a low-level, human-readable-ish language of short instructions (like `mov`, `push`, `call`) that maps almost directly onto what one specific kind of CPU understands.
- **Linker / linking:** the last build step, which stitches your own compiled code together with the already-compiled code of any libraries you used (like CS50's) into a single runnable file.
- **Byte:** a group of 8 bits, and the smallest chunk of memory a computer normally lets you address individually.
- **RAM (random access memory):** a computer's working memory while a program runs: picture a huge grid of numbered mailboxes, each one byte in size, that your program can read from and write to.
- **Data type:** a label (like `int`, `float`, or `char`) that tells the compiler what kind of value a variable holds, and (the part this lesson focuses on) exactly how many bytes to set aside for it.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In the last lesson, `debug50` showed you a strange "garbage value" sitting inside a variable before its line of code had even run, and Malan only promised you'd come back to what that really means. This lesson is where that promise starts to pay off: it shows you where memory actually is, and it shows you what `make` has been quietly hiding from you since your very first `make hello`. As Malan puts it, laying his cards on the table:

> "If we really want to get nitpicky, the compiler you've been using is actually called Clang for C language... What make is really doing for us is essentially automating this command." (David Malan)

Once you know that "compiling" is really four separate steps, compiler error messages that mention "linking" or "undefined reference" stop being scary jargon and start being specific, readable clues. And once you know that every variable has an exact size in bytes, sitting at an exact address in a giant grid of memory, ideas like arrays, pointers, and memory bugs, all coming in later modules, stop looking like magic.

## Learning objectives

By the end of this lesson you will be able to:

1. Name, in order, the four hidden stages a build runs (preprocessing, compiling, assembling, linking), and say what each stage produces.
2. Run `clang` directly, without `make`, to produce and inspect the intermediate file created at each of those four stages.
3. Explain what the `-lcs50` flag does, and reproduce and interpret the "undefined reference" linker error you get without it.
4. State how many bytes `bool`, `int`, `long`, `float`, `char`, and `double` each take up in memory, and explain why a `string`'s size is not fixed.
5. Describe RAM as an addressable grid of bytes, and explain in your own words why turning compiled zeros and ones back into readable source code ("decompiling") is hard, even though it's technically possible.

## Prerequisites

- **Module 3 · Lesson 9: The Art of Debugging.** You should be comfortable running `make`, reading a `clang` error message, and recognizing `buggy.c` and `hello.c`, since this lesson reopens those same files to look underneath them.
- **Module 2 · Lessons 5-8.** Basic C syntax: variables, `printf`, `#include`, and functions.
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**).

---

## Part 1: Make Is Not the Compiler

Ever since your first `make hello`, you've been running two commands: `make hello` to build, then `./hello` to run. It turns out `make` itself has been a small, convenient white lie.

> "It was a bit of a white lie for me to let you think... the compiler itself is called Make. Make is a command that literally makes your program. It makes it by compiling it, but make is not technically the compiler." (David Malan)

The real compiler is a separate program called **Clang** (short for "C language"), and it's free, open source, and popular enough that Malan notes you could go read the humans-written code that implements it yourself. `make hello` is really just automating a `clang` command for you. You can run that command directly:

```bash
clang hello.c
```

This works, but it does not produce a file called `hello`. Try `ls` afterward and you'll see a new file named `a.out` instead. That name is not random:

> "The default file name from Clang, the compiler (for historical reasons), it's not going to be hello, as you would hope. It's going to be a.out, for 'assembler output.'" (David Malan)

`./a.out` runs exactly the same program as `./hello` would have. The reason CS50 doesn't make you type `clang` and `a.out` in week one is simply that it's extra, unnecessary friction: `make` (and its `-o hello` naming trick under the hood) removes it.

There's a second wrinkle. If your program uses a CS50 function like `get_string`, plain `clang hello.c` fails with a cryptic message:

```text
Undefined symbols for architecture ...
  "_get_string", referenced from:
Linker command failed with exit code 1
```

This is not a missing `#include`: `#include <cs50.h>` can be right there at the top. The problem is that Clang doesn't automatically know *where on disk* to find CS50's already-compiled code. You have to tell it:

```bash
clang hello.c -lcs50
```

> "This is telling the compiler to link in the CS50 library so that it knows what the zeros and ones are that belong to the get_string function." (David Malan)

`make` has been quietly adding `-lcs50` (and naming your output file for you) this entire time. Once you know that, a "linker" error stops being mysterious: it's Clang telling you, specifically, that it finished translating your code but couldn't find the compiled code for a function you called.

> 🔑 **The single most important takeaway of this part.** `make hello` is not one atomic magic step: it is `clang hello.c -o hello -lcs50` with the typing done for you. Every piece of that longer command maps to something you now know how to reason about.

## Part 2: The Four Hidden Steps Inside "Compiling"

Colloquially, everyone, including Malan, calls the whole process "compiling." But technically, one call to Clang is running four separate, ordered stages:

```text
hello.c                     source code: the C you actually typed
   |
   |  1. PREPROCESSING        (clang -E hello.c -o hello.i)
   v
hello.i                     every #include line replaced by that header file's real contents
   |
   |  2. COMPILING            (clang -S hello.c -o hello.s)
   v
hello.s                     assembly code: mov, call, push... words a specific CPU understands
   |
   |  3. ASSEMBLING           (clang -c hello.c -o hello.o)
   v
hello.o                     object code: your program's own zeros and ones, not runnable alone
   |
   |  4. LINKING              (clang hello.c -o hello -lcs50)
   v
hello / a.out               one executable: your code + cs50's + stdio's, all stitched together
```

> "These four steps are what's been happening ever since the start of last week: pre-processing, compiling, assembling, and linking. But thankfully the world of programmers generally just treats all four of these steps as what we know now as compiling." (David Malan)

**Step 1: Preprocessing.** Every line starting with `#include` gets replaced, literally, by the text of that header file, before anything is translated.

> "The compiler finds on the server's hard drive the file called CS50.h, goes inside, and essentially copies and pastes its contents into my own code." (David Malan)

This is exactly why the compiler suddenly "knows" what `get_string` and `printf` look like: their prototypes were just pasted into the top of your file.

**Step 2: Compiling (to assembly).** The preprocessed C code gets translated into **assembly code**: a much lower-level language full of unfamiliar-looking instructions.

> "These are the assembly instructions. Those are the lowest level instructions that the CPU inside of a computer understands." (David Malan)

You won't be asked to write assembly in this course, but it's worth glancing at once: it's what programmers wrote before languages like C existed, and it's specific to one kind of CPU (Intel, AMD, Apple's own chips, and so on all use slightly different instructions). That's also why a program compiled for a Mac won't run on a PC: the assembly, and the zeros and ones after it, are simply the wrong pattern for that hardware.

**Step 3: Assembling.**

> "What does it mean to assemble a program, which is step three of the compilation process? That means converting assembly code to the actual zeros and ones." (David Malan)

The result is called **object code**: your program's own machine instructions, saved in a file (conventionally named `hello.o`). It is real machine code, but it isn't runnable by itself yet.

**Step 4: Linking.** Your compiled object code has to be combined with the already-compiled object code of every library function you used: CS50's `get_string`, the standard library's `printf`, and so on.

> "The final step then of linking is to combine all of those zeros and ones into one bigger blob of zeros and ones, and that's what's inside your hello program that you can execute." (David Malan)

That is exactly what `-lcs50` controls: it tells the linker where to find CS50's object code so it has something to combine yours with.

> ✅ **What to do about it:** when you see an error mentioning "undefined reference" or "linker command failed," you are not looking at a syntax mistake in your own code: you are looking at a missing `-l` flag (a library the linker doesn't know to include). Check your `#include`s are matched by the right library flag.

## Part 3: Why You Can't Just Reverse the Process

If a compiler turns readable C into zeros and ones, could you run it backward: take someone else's compiled program and reconstruct their original source code? This is called **decompiling**, and it's a real question with real stakes:

> "Couldn't you just kind of reverse this process and reverse engineer someone else's code by decompiling it? ... This is genuinely a threat, and this comes up in matters of law and intellectual property." (David Malan)

In practice, though, it is far harder than it sounds:

> "It's sort of easier said than done to reverse engineer code from these zeros and ones... if you are smart enough and capable enough and have enough free time to do that, it would probably take you less time to just implement Microsoft Word the normal way and just rebuild the software." (David Malan)

And decompiling can never be *perfectly* reversed, even in principle, because some information about your original source is simply thrown away during compiling:

> "You can't figure out from the zeros and ones whether or not it was a while loop or a for loop, because it just results in the same pattern of zeros and ones... it's not going to be obvious from the zeros and ones what the source code originally looked like." (David Malan)

> 💡 **A nuance worth keeping.** Not every language even works this way. As a preview of Module 10, Malan points out that JavaScript is different:
>
> "JavaScript source code is actually sent from web servers to web browsers, and you can look at the source code of any website on the internet... not all languages, it turns out, are even compiled typically. Sometimes the source code is just executed by the underlying computer." (David Malan)
>
> C is compiled ahead of time into zeros and ones before you ever run it. JavaScript, by contrast, typically ships as plain readable source and is executed directly, which is why "view source" on any webpage works, and "view source" on a compiled C program does not.

## Part 4: Every Data Type Has an Exact Size in Memory

Back in Module 2 you used data types like `bool`, `int`, `float`, `char`, and `string` without worrying about their footprint. It turns out each one reserves a specific, predictable number of bytes:

| Data type | Size (bytes) | What it holds |
|---|---|---|
| `bool` | 1 | `true` or `false` |
| `char` | 1 | one ASCII character |
| `int` | 4 | a whole number |
| `long` | 8 | a bigger whole number (twice an `int`'s range) |
| `float` | 4 | a real (decimal-point) number, by default |
| `double` | 8 | a real number, with roughly twice a `float`'s precision |
| `string` | *varies* | depends entirely on how many characters it holds |

A `bool` is a good example of memory being spent for convenience, not necessity:

> "A bool, it turns out, actually takes up one byte, which is kind of stupid because technically a bool, true or false, really only needs one bit. It just turns out that it's more efficient and easier to just use a whole byte." (David Malan)

`int` and `long` scale the same way:

> "An int uses 4 bytes... A long, meanwhile, is twice that: it uses 8 bytes." (David Malan)

And `float`/`double` follow the identical doubling pattern, trading memory for precision:

> "A float is 4 bytes by default, but a double gives you twice as many bits to play with." (David Malan)

A `char`, meanwhile, is the simplest of all: one byte, holding one ASCII character. A `string` is the odd one out on this list:

> "String, I'll put as a question mark, because a string totally depends on its length." (David Malan)

Every other type on this list has one fixed answer no matter what value you put in it: an `int` is always 4 bytes, whether it holds `0` or `2,000,000,000`. A `string`'s size, by contrast, depends entirely on what's inside it. Exactly *why* that is, and what a string actually turns out to be underneath, is the subject of the next lesson.

> 🔑 **The single most important takeaway of this part.** A data type isn't just a label for the compiler: it's a promise about exactly how many bytes to reserve. Everything on this list keeps that promise with a fixed number, except `string`.

## Part 5: How It All Comes Together: Bytes in a Grid Called RAM

Once your program is compiled, linked, and running, every variable it declares has to physically live somewhere. That "somewhere" is RAM (random access memory), and Malan's mental model for it is refreshingly simple:

> "Let's go ahead and draw this really as a grid of memory, a sort of canvas that we... use to store types of data like bools and ints and chars and floats and everything else." (David Malan)

Picture RAM as one enormous strip of numbered, one-byte mailboxes, stretching from byte 0 to however many billions of bytes your machine has:

```text
Byte address:    0     1     2     3     4     5     6     7     8   ...
Contents:      [ 01 ][ 00 ][ 11 ][ 01 ][ ?? ][ ?? ][ ?? ][ ?? ][ ?? ]  ...
                \____________________/
                 a 4-byte int lives here, in 4 addressed bytes side by side
```

Because an `int` is 4 bytes, it doesn't get 4 bytes scattered randomly around the grid, but it gets 4 *consecutive* ones:

> "If you want to store an int, well, that's 4: you might use all 4 of these bytes, necessarily contiguous. You can't just choose random bits all over the place. When you have a 4-byte value like an int, they're all going to be contiguous, back to back to back, in memory." (David Malan)

A `char` uses just 1 of those mailboxes. A `long` or `double` uses 8 in a row. The computer itself has no concept of "up," "down," or "next row": that's purely a drawing convenience for a wide screen. Underneath, it's just one long strip of addressable bytes, and every data type from Part 4 is really just an agreement about how many of those bytes belong to one value.

```text
                Preprocess → Compile → Assemble → Link
                        (Parts 1-2: turns hello.c into a running program)
                                        |
                                        v
                While the program runs, its variables live in RAM:
                a giant addressable grid of bytes (Part 5), where each
                data type (Part 4) reserves a fixed, contiguous number
                of those bytes.
```

---

## Key takeaways

1. **`make` is not the compiler.** `clang` is. `make hello` automates `clang hello.c -o hello -lcs50`: naming your output file and linking the CS50 library for you.
2. **"Compiling" is really four steps.** Preprocessing (copy-paste headers), compiling (C → assembly), assembling (assembly → object code, zeros and ones), and linking (combine your object code with libraries' object code into one executable).
3. **A linker error is not a syntax error.** "Undefined reference" or "linker command failed" means a missing `-l` flag, not a spelling mistake in your code.
4. **Every data type reserves a fixed number of bytes** (`bool` and `char` get 1, `int` and `float` get 4, `long` and `double` get 8), except `string`, whose size depends on its contents.
5. **RAM is one giant addressable grid of bytes**, and a multi-byte value like an `int` always occupies consecutive bytes in that grid, never scattered ones.
6. **Decompiling is technically possible but practically brutal**, and it can never be perfectly reversed: details like whether a loop was written as `for` or `while` are gone forever once compiled.

## Common pitfalls

- ❌ Saying "the compiler" when you mean `make`, or vice versa: `make` is the automation; `clang` is the actual compiler doing the translating.
- ❌ Seeing "undefined reference to `get_string`" and looking for a typo in your own code: check for a missing `-lcs50` (or the matching library flag) instead.
- ❌ Assuming a data type's byte size is a law of the universe: Malan is careful to say "on most modern systems." It's a near-universal convention on today's hardware, not a mathematical guarantee for every computer that has ever existed.
- ❌ Expecting `sizeof` on a `string` variable to tell you how many characters it holds: a `string`'s byte size isn't fixed the way `int` or `char` is, for reasons the next lesson explains.
- ❌ Assuming every language works like C. Some, like JavaScript, ship as plain source and are executed directly, with no separate compiled file to decompile in the first place.

---

## 🛠️ Capstone Project: The Compiler's Assembly Line

> This is the main hands-on project for the lesson. You'll manually run each of the four build stages against a real `hello.c` (producing and inspecting the files `make` normally deletes for you) and then measure, in bytes, exactly what six C data types cost. Knowing precisely how much memory a value costs, and that a "compiled program" is really just your code stitched together with other people's already-compiled code, is exactly the mental model you'll lean on later when your own database-backed final project needs to store and serve real data efficiently.

### What you will build

Two small artifacts on cs50.dev: (1) four intermediate files: `hello.i`, `hello.s`, `hello.o`, and a final executable, produced by hand from one `hello.c`, each inspected before moving to the next; and (2) a `sizeof.c` program that prints the exact byte size of six C data types on your own machine.

### Why this is the perfect practice

| Lesson idea | Where you use it |
|---|---|
| Clang vs. `make` (Part 1) | Milestone 1 |
| Preprocessing, `-E` (Part 2) | Milestone 2 |
| Compiling to assembly, `-S` (Part 2) | Milestone 3 |
| Assembling to object code, `-c` (Part 2) | Milestone 4 |
| Linking, `-lcs50` (Parts 1-2) | Milestone 5 |
| Data type sizes (Part 4) | Milestone 6 |

### Milestones (build them in order, each one works on its own)

1. **Set up `hello.c`.** On cs50.dev, write a small `hello.c` that includes `cs50.h` and `stdio.h`, asks for the user's name with `get_string`, and prints `hello, NAME`. Confirm it works the normal way first: `make hello` then `./hello`.
2. **Preprocess it by hand.** Run `clang -E hello.c -o hello.i`. Open `hello.i`. Scroll past the large wall of text near the top (that's `stdio.h` and `cs50.h`, copy-pasted in) and find your own few lines of code, unchanged, near the bottom.
3. **Compile it to assembly by hand.** Run `clang -S hello.c -o hello.s`. Open `hello.s`. You are not expected to understand most of it: just find the word `main`, and look for `call` instructions that mention `get_string` or `printf`.
4. **Assemble it to object code by hand.** Run `clang -c hello.c -o hello.o`. Try `./hello.o` directly: it will fail, because object code is real zeros and ones but is not yet a complete, linked program. Run `ls -l hello.o` and note its size in bytes.
5. **Link it by hand, and reproduce the missing-library error on purpose.** First run `clang hello.c -o hello_broken` (no `-lcs50`) and copy the exact error text. Then run `clang hello.c -o hello -lcs50` and confirm `./hello` now works correctly.
6. **Measure your data types.** Write `sizeof.c`, including `stdio.h` and `stdbool.h`, that uses `printf` and `sizeof()` to print the byte size of `bool`, `char`, `int`, `long`, `float`, and `double` on your own cs50.dev machine. Compare your output to the table in Part 4.
7. **Stretch goals.** (a) Run `ls -l hello` and compare its size to `hello.o`'s size from Milestone 4: in one sentence, explain why the linked executable is bigger. (b) Declare a `string` variable and try `sizeof` on it: notice it does *not* tell you the number of characters stored, which is a preview of Lesson 11.

### How you will know you are done

- ✅ You have four separate files on disk built from one `hello.c`: `hello.i`, `hello.s`, `hello.o`, and a runnable executable, and can say in one sentence what changed at each step.
- ✅ You've triggered the "undefined reference" / linker error yourself, on purpose, and can explain in your own words what `-lcs50` fixes.
- ✅ `sizeof.c` prints six correct byte counts, and you can explain why `bool` gets a whole byte instead of a single bit.
- ✅ You can explain, without looking it up, why decompiling `hello.o` back into readable C would be far harder than just writing `hello.c` again from scratch.

> 💡 **Keep yourself honest:** don't let `make` or a cleanup command delete `hello.i`, `hello.s`, or `hello.o` before you've actually opened and looked inside each one: the whole point is seeing the in-between states `make` normally hides.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Measure the invisible code (foundational)
Write a one-line program (just `#include <stdio.h>` and an empty `main`). Run `clang -E` on it and save the output. Count how many lines longer the preprocessed file is than your original: that's roughly how many lines of "invisible" code `stdio.h` was hiding from you the whole time.

### Exercise 2: Explain the linker error to a friend (intermediate)
Deliberately compile a program that calls `get_string` with plain `clang program.c` (no `-lcs50`). Copy the exact error text. In two or three sentences, in your own words, explain to a friend what a linker actually does and why this specific error happens.

### Exercise 3: Do the bit math yourself (advanced)
In your `sizeof.c` from the Capstone, print `sizeof(int) * 8` (that should equal the number of bits). Then, using the fact that a 4-byte signed `int` splits its range across positive and negative values, calculate by hand, no looking it up, the largest positive number a 4-byte signed `int` can hold. Compare your answer to the "roughly 2 billion" figure from the lecture.

---

## Cheat sheet

```text
MAKE VS. THE REAL COMPILER
  make hello   =  clang hello.c -o hello -lcs50   (make just automates this)
  a.out         =  Clang's default output name ("assembler output")

THE FOUR HIDDEN STEPS
  1. PREPROCESS   clang -E file.c -o file.i    #include lines -> real header text
  2. COMPILE      clang -S file.c -o file.s    C -> assembly (CPU-specific instructions)
  3. ASSEMBLE     clang -c file.c -o file.o    assembly -> object code (0s and 1s, not runnable alone)
  4. LINK         clang file.c -o file -lXXX   your object code + library object code -> one executable

  "undefined reference" / "linker command failed"  ->  missing -l<library> flag, not a typo

DATA TYPE SIZES
  bool     1 byte    char     1 byte
  int      4 bytes   float    4 bytes
  long     8 bytes   double   8 bytes
  string   varies: depends on its contents (see Lesson 11)

MEMORY MODEL
  RAM = one giant grid of individually addressed bytes (byte 0, byte 1, byte 2, ...)
  A multi-byte value (int, long, double, ...) always occupies CONSECUTIVE bytes.

DECOMPILING
  Technically possible, practically brutal, and never perfectly reversible
  (e.g., a compiled for-loop and while-loop can look identical).
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 9:** `debug50` showed you a "garbage value" sitting in a variable before its line of code ran. This lesson explains where that memory actually is: one giant addressable grid of bytes.
- **Next, Module 3 · Lesson 11 "Arrays and strings under the hood":** now that you know a `char` is exactly 1 byte and memory is addressable, you'll see that a `string` is really just a contiguous array of `char`s, which is exactly why its size "depends on its length."
- **Later, Module 5 · Lesson 17 "Pixels, hexadecimal, and memory addresses":** every byte in the grid you sketched here turns out to have an actual numeric address, which you'll print directly from your own C code.

---

*Source: "CS50x 2026 - Lecture 2 - Arrays" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
