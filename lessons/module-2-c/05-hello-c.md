# Module 2 · Lesson 5: Hello, C: From Blocks to Code

> **Course:** Self-Paced CS50x
> **Module 2:** First real programs in C: write, compile, run, and fix real code in a terminal
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 1 - C](https://www.youtube.com/watch?v=SlqjA04_dpk) · [full transcript](../../transcripts/03-lecture-1-c.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

The Scratch program you already understand becomes a real C program today: text you type as **source code**, that a tool called the **compiler** turns into the zeros-and-ones **machine code** your computer actually runs, and in this lesson you'll write it, compile it, run it, break it on purpose, and fix it, all from a terminal.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you write `hello.c`, break it three different ways, and fix each break by reading the compiler's own error messages. Everything before the Capstone teaches the skills you'll use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Tools like VS Code and cs50.dev will change over the years; the language underneath will not.
>
> - **[*The C Programming Language*](https://en.wikipedia.org/wiki/The_C_Programming_Language) by Brian Kernighan and Dennis Ritchie** (Prentice Hall, 1978). Often called "K&R," this is the original, canonical book on C, and the very first "hello, world" program in computing history was written for it. Every `hello.c` since, including the one you'll write today, is a direct descendant of that example.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Source code:** the text you type, in a language like C, that a human can read (with some training). This is what you write.
- **Machine code:** the zeros and ones that a computer's processor actually executes. Humans don't write this directly anymore; computers produce it for us.
- **Compiler:** a program that reads your source code and translates it into machine code, the same way a translator converts English into another language.
- **GUI (graphical user interface):** software you control with a mouse: icons, buttons, windows. "Graphical" because it's visual.
- **CLI (command-line interface) / terminal:** a window where you control software by typing text commands instead of clicking. The terminal is the specific window inside VS Code where you type them.
- **Header file:** a file (its name ends in `.h`) that contains code someone else wrote, which you can use in your own program by asking for it with `#include`.
- **Escape sequence:** a short symbol, starting with a backslash (`\`), that means something special inside a string of text instead of being printed literally: for example `\n` means "move to a new line."
- **Syntax:** the exact spelling, punctuation, and grammar a language requires. Get it slightly wrong and the compiler won't understand what you meant, even if the idea was right.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Last week you built programs by dragging and dropping Scratch puzzle pieces. Today you start typing, and the same ideas (functions, inputs, outputs, variables) will look unfamiliar wearing new syntax. Malan names this feeling directly:

> "even if today feels like a bit of a fire hose such as that pictured here, appreciate that a lot of today's ideas are exactly the same as last week's ideas. It's just that the syntax is going to change." (David J. Malan)

He even points to an MIT hacking tradition where students once rigged a fire hydrant to a drinking fountain under a sign reading:

> "Getting an education from MIT is like trying to drink from a fire hose." (sign quoted by David J. Malan)

That's the honest expectation for today. The payoff is concrete: by the end of this lesson you will have typed, compiled, run, broken, and repaired a real program: the exact loop (write code, build it, run it, read the error, fix it) that every programmer, on every project, repeats forever.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why C looks different from Scratch even though the underlying ideas (functions, input, output) are the same.
2. Distinguish source code from machine code and state what a compiler does between them.
3. Write a minimal C program using `#include`, `main`, and `printf`.
4. Compile a C program with `make` and run it from the terminal with `./`.
5. Use the `\n` and `\"` escape sequences correctly inside a string.
6. Read a compiler error message (file name, line number, description) and fix a missing semicolon or a missing header.

## Prerequisites

- **Module 1 · Lesson 4 (Programming in Scratch).** This lesson maps every C construct straight back onto the Scratch blocks you already used: functions, inputs, outputs.
- **A free cs50.dev account** (sign in with GitHub). If you haven't set this up yet, Module 0's pre-flight lesson walks through it; you'll need it to type along.

---

## Part 1: Same ideas, new syntax (the mental model)

In Scratch, the simplest program made a cat say "Hello world" when you clicked the green flag. Recall from Lesson 4 that this program had three visual layers: a yellowish "when green flag clicked" block that just started things off, a purple block that did the real work, and a white oval inside it holding the actual text.

That same structure exists in C. It's just typed instead of dragged. What you write is called **source code**:

> "So source code is what programmers write. It's what you write." (David J. Malan)

But your computer's processor doesn't understand English-like keywords such as `printf`. It only understands binary: the zeros and ones you met when Scratch first introduced bits. So there has to be a translation step. That translator is a program called a **compiler**:

> "a special piece of software that takes source code as input, produces machine code as output, and that type of program is called a compiler." (David J. Malan)

> 🔑 **The single most important takeaway of this part:** every idea from Scratch (functions, inputs, outputs, variables, loops, conditionals) is still here in C. Only the *syntax* (the spelling and punctuation the computer demands) has changed. Fluency comes from practice, not from the ideas being new.

### Input, output, and the same black box

Just as last week's function black box took arguments in and produced a side effect or a return value out, C functions do the same thing. `printf` (short for "print, formatted") is the C equivalent of Scratch's `say` block: it takes text as input and produces the side effect of that text appearing on the screen.

## Part 2: The environment (GUI, CLI, and cs50.dev)

You'll write today's code inside a browser-based tool called **VS Code** (Visual Studio Code), hosted for you at cs50.dev so nothing needs installing yet. It's a real industry tool ("this is what real programmers, so to speak, are using all of the time nowadays," as Malan puts it) and by the end of the course you're free to install it on your own computer.

VS Code is what's known as a **graphical user interface**:

> "it's an interface for users that's graphical in nature with icons and buttons and the like." (David J. Malan)

But tucked inside that graphical window is a smaller window, the terminal, where you'll type most of your actual commands:

> "that's generally known as a command line interface, or CLI for short." (David J. Malan)

> 💡 **Nuance:** using the terminal can feel like a step backwards from clicking things with a mouse. It isn't. Most programmers end up faster and more precise typing commands than reaching for a trackpad. This lesson is where that habit starts.

Inside VS Code you'll notice three areas that matter today:

| Area | What it's for |
|---|---|
| The tab bar (top) | Your open source-code files, like a normal tabbed editor |
| The editor pane | Where you type the actual C code |
| The terminal (bottom) | The command line where you compile and run your programs |

> ✅ **What to do about it:** whenever you see a `$` prompt in the terminal, that's your cue to type a command. The `$` itself is just convention: it has nothing to do with money.

## Part 3: Writing, compiling, and running hello.c

Let's build the smallest real program you can write in C. In the terminal, typing `code hello.c` creates and opens a new, empty file named `hello.c` (lowercase, no spaces: the convention in this world, unlike a typical Mac or PC desktop). Then you type four lines:

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, world!\n");
}
```

Here's what each piece does:

- **`#include <stdio.h>`**: a request to the compiler: "include the code defined in the standard input/output header file, because I'm about to use one of its functions." Without it, the compiler has no idea what `printf` even means.
- **`int main(void)`**: every C program needs a function called `main`; it's the one that runs automatically when your program starts, the same way Scratch's "when green flag clicked" block kicked things off.
- **`{ ... }`**: the curly braces hug the code that belongs to `main`, the same way an orange or purple Scratch block visually hugged the pieces nested inside it.
- **`printf("Hello, world!\n");`**: print the text between the double quotes to the screen, then finish the line with a semicolon, the C equivalent of ending an English sentence with a period.

Once it's typed, the file exists only as source code: nothing has run yet. Compile it with:

```text
$ make hello
```

You don't retype `hello.c`; `make` is smart enough to look for a file called `hello.c` when you ask it to build a program called `hello`. If this command produces no output at all, that's a good sign:

> "any time you don't see any output at a command like this, that's probably a good thing." (David J. Malan)

Now run the compiled program with a slash in front of its name:

```text
$ ./hello
Hello, world!
```

The `./` means "look in my current folder and run the program found there called `hello`." That three-step rhythm (**write the source code, `make` it, `./` run it**) is a pattern you'll repeat for the rest of the course, no matter what the program is called.

> ❌ **A trap to notice now:** if you edit `hello.c` again, you must run `make hello` again before `./hello` will reflect your changes. The compiler only translates source code into machine code when you ask it to; editing the text alone changes nothing that's already been compiled.

## Part 4: Escape sequences and reading compiler errors

### Escape sequences

Try deleting the `\n` from the end of the string and recompiling. The program still technically prints "Hello, world!", but your terminal's next prompt now appears squashed onto the same line, which looks wrong. That backslash-n was never optional decoration; it's what's called an **escape sequence**:

> "special sequences of symbols like backslash and N in this case that do a little something unusual." (David J. Malan)

Two you'll use constantly:

| Sequence | Meaning |
|---|---|
| `\n` | move to a new line |
| `\"` | print an actual double-quote character inside a string that is itself delimited by double quotes |

`\"` exists because the compiler needs some way to tell "this quote ends my string" apart from "I actually want to print a quote mark." Without the backslash, `printf("She said "hi"\n");` would be ambiguous: which quote is real punctuation and which is a stray character?

> 💡 **Nuance:** you might be tempted to fix a too-long line by literally pressing Enter partway through your code. Resist it: most programming languages, C included, expect one complete thought per line. Escape sequences like `\n` are the sanctioned way to put a new line into your *output* without breaking up your *source code*.

### Reading a compiler error: the missing semicolon

Delete the semicolon after `printf(...)` and run `make hello` again. Instead of silence, you'll get an error message. It looks intimidating, but it's structured and specific:

> "Here is the name of the file in which the problem exists ... Here is the line number in which the problem seems to exist ... it even says expected semicolon after expression. There's a little green carrot symbol pointing me at the mistake." (David J. Malan)

Every compiler error you'll see this term follows that same shape: **file name → line number → plain-English description → a marker pointing at the spot.** The fix here is simply to add the missing semicolon back and recompile.

### Reading a compiler error: the missing header

Now instead delete the `#include <stdio.h>` line entirely (leaving the semicolon back in place) and recompile. You'll get a completely different error, one about an "undeclared" function. That's because `printf` isn't actually part of the core C language: it lives in a **library**, code someone else wrote that you can reuse:

> "a library is code someone else wrote that you can use." (David J. Malan)

The header file `stdio.h` is what tells the compiler "the function `printf` is defined elsewhere; go include its definition before you try to use it." Leave that line out, and the compiler has genuinely never heard of `printf`. Add it back, and the error disappears.

> ❌ **A pitfall you will make at least once:** typing the header's name wrong. Malan calls this out directly:
>
> "It is not studio.h. This is a very common bug online if you find yourself typing studio." (David J. Malan)
>
> It's `stdio.h` (**st**andard **i**nput/**o**utput), not "studio.h."

## Part 3+4 combined: how the pieces fit together

```text
 you type this ──────────► SOURCE CODE (hello.c)
                                  │
                          make hello  (the compiler)
                                  │
                                  ▼
                          MACHINE CODE (hello)
                                  │
                              ./hello
                                  │
                                  ▼
                          Hello, world!  (runs on screen)

 If a step fails, the compiler stops and reports:
   file name → line number → description → pointer to the mistake
```

---

## Key takeaways

1. **Same ideas, new syntax.** Functions, inputs, and outputs from Scratch reappear in C: you're learning new punctuation, not new concepts.
2. **Source code becomes machine code through the compiler.** Nothing runs until you compile it, and nothing reflects your latest edits until you recompile it.
3. **`make hello` then `./hello` is the whole cycle.** Compile, then run: that pattern repeats for every C program you'll ever write.
4. **Escape sequences (`\n`, `\"`) are not optional flourishes.** They're how you put a new line or a literal quote mark inside a string.
5. **Compiler errors are structured, not random.** File, line number, plain-English message, and a pointer at the mistake: read them in that order.

## Common pitfalls

- ❌ Forgetting to recompile (`make hello`) after editing `hello.c`, then wondering why `./hello` doesn't show your change.
- ❌ Typing `studio.h` instead of `stdio.h`: a real, common typo Malan calls out by name.
- ❌ Forgetting the semicolon at the end of a statement: C, unlike Scratch, needs an explicit "I'm done with this thought" marker.
- ❌ Trying to fix a long line of code by literally pressing Enter in the middle of it, instead of using `\n` in the output.
- ❌ Panicking at the length of a compiler error message instead of reading it top to bottom for the file, line, and description.

---

## 🛠️ Capstone Project: Break It, Read It, Fix It

> This is the main hands-on project for the lesson. You'll write a working `hello.c` on cs50.dev, then deliberately sabotage it three different ways so that reading, and trusting, a compiler error message stops feeling scary.

### What you will build

A single `hello.c` file that you compile and run successfully, then break on purpose three separate times, fixing each break by reading what the compiler tells you before you touch the code. Each milestone below stands on its own: if you get stuck on one, reset to your last working `hello.c` and move to the next.

- A working `hello.c` that prints a greeting.
- Three logged "break → read the error → fix" cycles.
- A version that uses both `\n` and `\"` deliberately.

### Why this is the perfect practice

| Lesson idea | Where you use it in the capstone |
|---|---|
| Source code → compiler → machine code | Every `make hello` you run |
| `#include`, `main`, `printf` | Writing `hello.c` from scratch |
| Escape sequences `\n` and `\"` | Milestone 4, adding them deliberately |
| Reading compiler errors (file, line, message) | Milestones 2-3, diagnosing each intentional bug |

### Milestones (build them in order, each one works on its own)

1. **Get a working baseline.** On cs50.dev, run `code hello.c`, type the four lines from Part 3, run `make hello`, then `./hello`. Confirm you see your greeting printed. This is your safe checkpoint: keep a mental (or copy-pasted) note of what correct `hello.c` looks like.
2. **Break it by removing the semicolon.** Delete the `;` after your `printf(...)` line. Run `make hello`. Read the error's file name, line number, and description out loud before you fix anything. Then add the semicolon back and confirm `make hello` and `./hello` work again.
3. **Break it by removing the header.** Starting again from your working baseline, delete the `#include <stdio.h>` line. Run `make hello`. Notice this error looks nothing like the semicolon error: it complains about an unrecognized function, not punctuation. Restore the `#include` line and confirm it compiles again.
4. **Break it a third way: an unclosed string.** Starting again from your working baseline, delete the closing `"` at the end of your greeting (leave the semicolon in place). Run `make hello` and read the new error: it will complain about the string itself, not a missing semicolon or an unknown function. Restore the closing quote and confirm it works.
5. **Add escape sequences on purpose.** Edit your working `hello.c` so it prints two lines: one ending in `\n`, and a second one using `\"` to print an actual quotation mark, for example a line like `She said \"hello\".\n`. Recompile and confirm both escape sequences behave as expected.
6. **Stretch goals.** Before running `make hello`, predict what kind of error you'll get, then test yourself against: misspelling `main` as `Main`, deleting one of the curly braces, or misspelling `printf`. See how close your prediction was.

### How you will know you are done

- ✅ `./hello` prints your greeting correctly after each of the three intentional breaks has been fixed.
- ✅ You can state, from memory and without looking it up, what a "missing semicolon" error looks like versus a "missing header" error.
- ✅ Your `hello.c` uses `\n` at least once and `\"` at least once, on purpose, and you can explain what each does.

> 💡 **Keep yourself honest:** don't fix a break by guessing and retyping the whole line. Read the compiler's file name and line number first, form a hypothesis about the cause, then make the smallest possible edit to test it.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Personalize it (foundational)
Change your working `hello.c` so it prints your own name instead of "world" (for example, `Hello, Ada!`). Recompile with `make hello` and rerun with `./hello` to confirm the change took effect.

### Exercise 2: A second program (intermediate)
Create a brand-new file called `goodbye.c` (remember: `make` will infer the source file from the program name you give it). Write a `main` function that prints two lines: a plain "Goodbye, world!" ending in `\n`, and a second line that uses `\"` to print a sentence containing an actual quotation mark.

### Exercise 3: One file, two bugs (advanced)
In a scratch copy of `hello.c`, introduce two mistakes at once: for example, remove both the semicolon *and* the `#include <stdio.h>` line. Run `make hello` and notice how many errors are reported, and in what order. Fix only one of the two mistakes, recompile, and observe how the error list changes before fixing the second.

---

## Cheat sheet

```text
THE C COMPILE-AND-RUN CYCLE
  1. code hello.c        write/open the source file
  2. (type your code)    #include, main, printf, semicolons
  3. make hello          compile: source code -> machine code
  4. ./hello              run the compiled program

MINIMAL hello.c
  #include <stdio.h>

  int main(void)
  {
      printf("Hello, world!\n");
  }

ESCAPE SEQUENCES
  \n   new line
  \"   a literal double-quote inside a quoted string

READING A COMPILER ERROR
  file name -> line number -> plain-English message -> pointer (^) at the spot

COMMON CAUSE -> SYMPTOM
  missing semicolon        -> "expected semicolon after expression"
  missing #include <stdio.h> -> "undeclared function" (printf unrecognized)
  unclosed "  string         -> error pointing at the string itself
  "studio.h" typo           -> header not found (it's stdio.h)

RULE OF THUMB
  No output after `make hello`?  Good: that means it compiled.
  Any output?  Read it top to bottom before touching your code again.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 4:** you built functions, inputs, outputs, and variables in Scratch by dragging blocks. This lesson re-expressed those exact same ideas as typed C syntax: nothing conceptually new, just new spelling and punctuation to get right.
- **Next, Module 2 · Lesson 6:** "Input, variables, and the command line" builds directly on `hello.c`: you'll capture what a user types with `get_string`, plug it into `printf` with the `%s` placeholder, and start navigating files with Linux commands like `ls` and `cd`.
- **Later, Module 3 · Lesson 10:** "From source code to machine code" pulls back the curtain on `make` itself, tracing the full preprocess → compile → assemble → link pipeline that today's lesson treated as a single black-box step.

---

*Source: "CS50x 2026 - Lecture 1 - C" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
