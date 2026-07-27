# Module 5 · Lesson 18: Pointers, and What Strings Really Are

> **Course:** Self-Paced CS50x
> **Module 5:** Memory: see the bytes: pointers, the heap, and files
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 4 - Memory](https://www.youtube.com/watch?v=db0H0U13YsA) · [full transcript](../../transcripts/06-lecture-4-memory.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

A pointer is just a variable that stores a memory address instead of an ordinary value, and once you can hold an address you can finally see the truth that's been hidden since week one: a C string is nothing more than a pointer to its first character, sitting in memory next to its neighbors until a null byte says "stop here."

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *The Pointer Field Trip*, where you declare an integer and a pointer to it, predict what a whole grid of `printf` calls will output *before* you run them, and then walk a string character-by-character two different ways to prove, with your own eyes, that they agree. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Languages and courses change, but "a variable that stores an address" is a concept that predates C itself and outlives it.
>
> - **[*The C Programming Language*](https://en.wikipedia.org/wiki/The_C_Programming_Language) by Brian Kernighan and Dennis Ritchie (2nd edition, 1988).** Chapter 5, "Pointers and Arrays," is the original, timeless account of exactly what this lesson teaches: that an array name and a pointer to its first element are, for almost all purposes, interchangeable. Everything Malan demonstrates in VS Code in this lecture is a live walkthrough of ideas first written down here decades ago.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Byte:** a chunk of 8 bits, the standard-sized unit computers use to measure and address memory. An `int` is usually 4 bytes; a single `char` is exactly 1 byte.
- **Memory address:** a specific numbered location inside the computer's memory, like a house number on a very long street of bytes. Every byte has its own unique address.
- **Pointer:** a variable whose value *is* a memory address: a variable that stores *where* something else lives, rather than storing that something directly.
- **Address-of operator (`&`):** the symbol you put in front of a variable's name to ask the computer, "what memory address is this variable stored at?"
- **Dereference operator (`*`):** the same `*` symbol, used a second, completely different way. Placed in front of a pointer *variable* (not in a declaration), it means "go to the address this pointer stores, and give me, or let me set, the value that lives there."
- **Hexadecimal (`0x...`):** a base-16 way of writing numbers, using digits `0-9` and then `A-F`. Programmers write memory addresses in hex by convention, prefixed with `0x`. You met this in Lesson 17; it comes back constantly today.
- **Null terminator (`\0`):** a single zero byte that marks the end of a string in memory. It's how C knows where a string stops without separately storing its length.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In Lesson 17 you learned that every byte in your computer's memory has a numbered address, written in hexadecimal. That was mostly a spectator sport. You looked at addresses, you didn't do anything with them. Today that changes: you get a variable that can *hold* an address, and once you have that, you can finally answer a question CS50 has been quietly dodging since week one: what is a `string`, really?

This is, by Malan's own account and by the reputation this lecture has across every CS50 cohort, the single hardest concept in the whole course. Take the difficulty seriously, but also take this seriously:

> 🔑 **Read this before anything else today.** "In fact, all these years later, I still remember the day in which I finally understood this topic, which was not the day of the lecture in which I was introduced, but it was in like the back right corner of the Elliott House dining hall. I was sitting down during office hours with my teaching fellow, and he finally helped light bulb go off over my head." (David Malan)
>
> The person who has taught this topic for decades did not get it the first time either. If it doesn't click on your first pass through this lesson, that is the *normal* experience, not a sign you're behind. Reread the diagrams, walk through the capstone slowly, and it will click, just maybe not today.

Once pointers click, entire capabilities open up: Lesson 19 will show you how to grab your own fresh chunk of memory with `malloc` (and why you must give it back with `free`), and Module 6's linked lists are, in Malan's world, nothing more than structs and pointers combined. Pointers are the hinge the rest of the course swings on.

## Learning objectives

By the end of this lesson you will be able to:

1. Declare a pointer to an `int` using the `int *p` syntax and explain, in your own words, what value it actually stores.
2. Use `&` to get a variable's address, and use `*` to dereference a pointer: reading the value it points to, or writing a new one there.
3. State how many bytes a pointer occupies on a modern (64-bit) machine, and explain why that number had to grow over time.
4. Explain that a C string is really a `char *`, the address of its first character, and that CS50's `string` type has, since week one, secretly been a `typedef` for exactly that.
5. Predict, before running any code, what `S`, `&S[i]`, `S + i`, and `*(S + i)` will each print for a given string, and explain why pointer arithmetic and array-bracket syntax always agree.

## Prerequisites

- **Module 5 · Lesson 17: Pixels, hexadecimal, and memory addresses**: you should already be comfortable reading a hexadecimal address like `0x123` and know that memory is just a long numbered row of bytes.
- Comfort declaring variables, using arrays with bracket syntax (`s[0]`), and the idea that a string ends with a null terminator, from earlier modules.
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**): you'll compile and run real C code in the Capstone.

---

## Part 1: Declaring a pointer, a variable that stores an address

Start with the most ordinary line of C you've ever written:

```c
int n = 50;
```

Nothing new. `n` lives somewhere in memory (say, for the sake of a clean diagram, at address `0x123`) and it takes up 4 bytes, because that's how big an `int` is.

```text
address     contents
-------     --------
0x123       50            <- this is n (4 bytes)
```

Now Malan introduces two brand-new symbols (a single `&` and a single `*`) that let you actually see and use that address:

> "One is a single ampersand and one is a single asterisk, and we'll see that the asterisk has a few different uses, but the ampersand has a very simple straightforward one which is to just get the address of a variable in memory." (David Malan)

So `&n` means "the address of `n`": not `n`'s value (`50`), but the house number where `n` lives (something like `0x123`). To print an address instead of a number, C has a format code for it: `%p` (think "pointer"), used the same way you've used `%i` or `%s`.

```c
#include <stdio.h>

int main(void)
{
    int n = 50;
    printf("%p\n", &n);   // prints n's address, something like 0x7ffd3c34ecc
}
```

### Storing that address in a variable

An address is "just" a number, but C wants you to say clearly that a variable holds an *address of an int*, not an int itself. That's the second job of the asterisk, this time used in a **declaration**, not as an operator on its own:

```c
int n = 50;
int *p = &n;   // p stores the address of n
```

> "This is the canonical way to declare a pointer in space, then the star, then without a space, the name of the variable." (David Malan)

Read `int *p` as one idea: "`p` is a pointer to an `int`", a variable that stores the address of some `int`, wherever that `int` happens to live. You will see people write `int* p` or `int * p` too; they all compile identically, but Malan recommends the style above, with the star hugging the variable name.

> ❌ **A trap worth naming immediately.** That `*` looks exactly like the multiplication symbol, and that is not a coincidence anyone chose on purpose:
>
> "It's weird looking syntax. It kind of looks like multiplication, but it isn't. It's just the developers of C decades ago decided to use an asterisk even though it's admittedly non-obvious what it's doing." (David Malan)
>
> Whenever you see `*` right after a type name in a declaration (`int *p`), it means "pointer to," full stop: no arithmetic involved. If you forget the star, the compiler will refuse to compile with an error like `incompatible pointer to integer conversion`, because you'd be trying to stuff an 8-byte address into a 4-byte `int` box.

### How big is a pointer? 8 bytes, always

Here's a detail that surprises almost everyone the first time: it doesn't matter whether a pointer points to an `int`, a `char`, or anything else, the pointer variable *itself* is always the same size on a given machine.

> "It turns out by convention on most systems, a pointer that is a variable that stores an address is actually going to be 8 bytes large. It's going to be 64 bits." (David Malan)

Why 8 bytes (64 bits), and not, say, 4?

> "We use 64 bits or 8 bytes nowadays for pointers because our computers have that much more memory." (David Malan)

With only 32 bits, the biggest address you could count to is about 4 billion, meaning a computer could never have more than about 4 gigabytes of memory, because there'd be no way to number any byte past that point. Modern computers routinely have far more than 4 gigabytes of RAM, so pointers grew to 64 bits so there are enough distinct addresses to go around.

```text
address        contents
-----------    --------
0x123          50            <- n, an int (4 bytes)
...
0x7ffd3c34ecc  0x123         <- p, a pointer (8 bytes): it stores n's address
```

### The mailbox metaphor

If diagrams of bytes and hex addresses feel abstract, Malan's own classroom metaphor may help more:

> "If you think of your computer's memory as hundreds or thousands of little mailboxes, maybe more apartment style where you've just got rows and columns of mailboxes as opposed to individual ones for single family homes, each of those mailboxes can contain the address of some value in memory." (David Malan)

Picture it like this:

```text
   mailbox "p"                     mailbox "n"
  +------------+                  +------------+
  |   0x123    |  --- points to-->|     50     |
  +------------+                  +------------+
   (8 bytes:                       (4 bytes:
    an address)                     an actual int)
```

`p`'s mailbox doesn't contain the number 50. It contains a note that says "go look at address `0x123`." Programmers rarely care what the specific address number actually is, so on a whiteboard (or in this lesson) we usually stop drawing hex numbers altogether and just draw an arrow instead: `p` **points to** `n`.

> 🔑 **The single most important takeaway of this part.** A pointer is a completely ordinary variable: it just so happens that the value it stores is a memory address rather than a "normal" value. `&x` gets you that address; `int *p` gives you somewhere to keep it.

---

## Part 2: Dereferencing, using `*` to go to the address

Declaring `p` and printing it out (as in Part 1) shows you a big, mostly-useless hexadecimal number. The genuinely useful move is to follow that address back to the value sitting there: what Malan calls, using the mailbox-and-arrow picture, "opening the mailbox you're pointing at."

That's the *second* job of the `*` symbol: the dereference operator. Used on a pointer **variable** (not in a declaration), `*p` means "go to the address stored in `p`, and give me what's there."

> "If you simply prefix your variable name with a star, that is the so-called dereference operator, which means go to the address in P." (David Malan)

```c
int n = 50;
int *p = &n;
printf("%i\n", *p);   // prints 50 -- goes to p's address, reads what's there
```

Walk through it line by line, exactly as it happens in memory:

```text
line              what happens                          memory afterward
----              ------------                          -----------------
int n = 50;       n gets 4 bytes, value 50               n=50 @ 0x123
int *p = &n;      p gets 8 bytes, value = n's address     p=0x123 @ (somewhere)
*p                "go to 0x123" -> finds 50               (nothing changes)
```

`*p` and `n` refer to the exact same byte of memory, seen through two different names. That means dereferencing isn't just for reading: you can **write** through a pointer too, and it changes the original variable, because there is no "copy" involved; you went straight to `n`'s own address:

```c
int n = 50;
int *p = &n;
*p = 100;                 // go to the address in p, and store 100 there
printf("%i\n", n);        // prints 100 -- n itself changed, even though
                           // we never wrote the word "n" on this line
```

> 💡 **Nuance worth sitting with.** `p = 100;` (no star) would be a completely different, almost certainly wrong, instruction: it would try to make `p` point at address `100` (a nonsense location), instead of changing the value at the address `p` already points to. The star is what says "go there," not "change what I'm pointing at."

> ✅ **What to do about it:** whenever you're unsure what a line involving `*` and a pointer does, ask yourself first: "is the star in a declaration (means: this variable is a pointer), or is it in front of an already-declared pointer variable being used (means: go to that address)?" Those are the only two jobs that symbol has.

---

## Part 3: Strings revealed, a string is a `char *`

Here is the string program you've written since week one:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string s = get_string("s: ");
    printf("%s\n", s);
}
```

You've always been told `s` is "a string", a sequence of characters. That was, in Malan's words, a "white lie", a simplification to keep week one from also having to teach hexadecimal, addresses, and pointers on day one. Today the lie comes off.

Suppose the human typed `HI!`. In memory, the three characters plus the mandatory null terminator (`\0`) sit back-to-back-to-back, always contiguous, always in that order:

```text
address    value
-------    -----
0x123      'H'    <- s[0]
0x124      'I'    <- s[1]
0x125      '!'    <- s[2]
0x126      '\0'   <- s[3], the null terminator ("stop here")
```

Given that layout, what is `s` itself, the variable, actually storing? Not the letters themselves. Just one thing: the address where the first letter begins.

> "But this is also incorrect conceptually because yes, S is the string, but more technically today S is the address of the first character in the string." (David Malan)

That's it. That's the whole reveal. A string variable is a pointer: an 8-byte box holding the address of character number zero, plus nothing else. It doesn't need to store where the string *ends*, because of the convention you already know:

> "That's why humans decades ago decided to just terminate every string in memory with the backslash zero or null terminator, because if you give me the beginning of the string and the end, I can obviously with a loop find everything else in between." (David Malan)

Drawn as two separate boxes: `s` the 8-byte pointer variable, and the characters it points at, living somewhere else entirely:

```text
s (8 bytes, lives at some other address)      the characters s points at
+------------------+                          +-----+-----+-----+------+
|      0x123       |  ------------------->    | 'H' | 'I' | '!' | '\0' |
+------------------+                          +-----+-----+-----+------+
                                                0x123 0x124 0x125 0x126
```

### The `typedef` behind the curtain

If `string` is really just "the address of a `char`," what actually *is* `string`? It turns out CS50's library never invented a new kind of data. It just gave an existing type a friendlier name:

> "The type you know as string since week one, all this time has simply been a synonym for char star s." (David Malan)

In code, that "synonym" is written `char *s`: a pointer to a `char`, exactly the same tool from Part 1, just pointing at a character instead of an `int`. CS50's header uses a keyword called `typedef` (short for "type definition") to make `string` mean "`char *`" everywhere in your program, the same trick you used in earlier modules to build your own `person` struct type. Remove `#include <cs50.h>` from a program that uses `string`, and the compiler will complain it has never heard of `string`, because, strictly speaking, C itself has no such keyword. Write `char *s` instead of `string s`, and the exact same program compiles and runs, training wheels fully off.

### Printing `S`, `S + 1`, and `&S[i]`, three ways to say the same address

Because a string is just an address, everything you can do with a pointer, you can do with a string. Malan demonstrates this by printing several different addresses side by side and showing they line up exactly:

```c
char *s = "HI!";
printf("%p\n", s);        // the address s stores
printf("%p\n", &s[0]);    // the address-of operator applied to the first character
```

These two lines print **the exact same address**. `s` already *is* the address of the first character, so asking for `&s[0]` ("the address of character zero") just recomputes the number `s` was storing all along.

The same idea extends down the string. `s`, `s + 1`, `s + 2` are the addresses of the 1st, 2nd, and 3rd characters, and Malan shows you can even hand those addresses straight to `%s` and get a valid (if slightly odd) printed string starting from each point:

```text
printf("%s\n", s);         ->  HI!    (starts reading at s[0], stops at '\0')
printf("%s\n", s + 1);     ->  I!     (starts reading at s[1], stops at the same '\0')
printf("%s\n", s + 2);     ->  !      (starts reading at s[2], stops at the same '\0')
```

Each call still finds the same null terminator: it just starts counting from a different byte, which is exactly what Malan calls **pointer arithmetic**:

> "There is a concept known as pointer arithmetic, which means given an address you can add to it, subtract to it." (David Malan)

### Pointer arithmetic vs. array syntax, two spellings, one answer

This brings you to the last piece: `s[i]` (the array-bracket notation you've used since Module 3) and `*(s + i)` (pointer arithmetic plus a dereference) are two different ways of writing the *identical instruction*. `s[i]` means "go `i` steps past where `s` points, and give me the byte there", which is exactly what `*(s + i)` spells out longhand.

| Bracket syntax | Pointer-arithmetic equivalent | Meaning |
|---|---|---|
| `s[0]` | `*(s + 0)`, i.e. `*s` | the 1st character |
| `s[1]` | `*(s + 1)` | the 2nd character |
| `s[i]` | `*(s + i)` | the (i+1)-th character |
| `&s[0]` | `s` | the address of the 1st character |
| `&s[i]` | `s + i` | the address of the (i+1)-th character |

The bracket version exists purely for human convenience:

> 🔑 **The single most important takeaway of this part.** `s[i]` and `*(s + i)` always produce the same value, because the compiler quietly rewrites the first into the second for you. Array syntax is what programmers call *syntactic sugar*, a nicer-looking spelling of the exact same underlying operation. Nobody's forcing you to write `*(s + i)`; it's worth being able to read it, because it's the truth the bracket notation is hiding.

---

## Key takeaways

1. **A pointer is a variable that stores an address, nothing more exotic.** `int *p` declares one; `&n` gets you the address to put in it.
2. **`*` has two unrelated jobs, and context tells them apart.** In a declaration (`int *p`), it means "this is a pointer." On an existing pointer variable (`*p`), it means "go to that address": to read the value there, or to write a new one.
3. **Pointers are 8 bytes (64 bits) on modern machines**, regardless of what type they point to, because computers now have far more than the ~4 billion bytes a 32-bit address could reach.
4. **A C string is a `char *`**, the address of its first character, nothing else. `string` (from `cs50.h`) is just a friendlier `typedef` name for exactly that type.
5. **`s[i]` and `*(s + i)` are the same instruction in two spellings.** Bracket notation is syntactic sugar the compiler translates into pointer arithmetic behind the scenes.

## Common pitfalls

- ❌ Forgetting the `*` in a pointer declaration (`int p = &n;` instead of `int *p = &n;`): the compiler will reject it with an "incompatible pointer to integer conversion" error, because you tried to squeeze an 8-byte address into a 4-byte `int`.
- ❌ Confusing the two meanings of `*`: writing `*p` when you meant to declare a new pointer, or forgetting the `*` when you meant to dereference one and go to that address.
- ❌ Writing `p = 100;` when you meant `*p = 100;`: the first repoints `p` at a bogus address; the second changes the value `p` already points to.
- ❌ Assuming `&` belongs before every variable you pass around. You need `&n` to get the address of an `int`, but a string variable `s` is *already* an address: writing `&s` gives you the address of the pointer itself (a different, more advanced idea, "a pointer to a pointer," not needed here).
- ❌ Expecting this to click on the first read. It is famously the hardest lesson in the course: reread the diagrams and lean on the capstone before judging yourself against a single pass.

---

## 🛠️ Capstone Project: The Pointer Field Trip

> This is the main hands-on project for the lesson. You will declare a plain `int` and a pointer to it, predict what a whole page of `printf` calls will output *before you ever run the program*, and then prove, character by character, that array syntax and pointer arithmetic agree on a string. Every row you'll eventually pull out of a database table at the end of this course is, underneath, just bytes sitting at an address: this is the field trip where you finally see that terrain up close.

### What you will build

A single file, `pointer_trip.c`, on cs50.dev, in two parts:

1. **Part A, an int and a pointer to it.** Declare an `int` and a pointer to it, then print every meaningful combination of value, address, and dereference, after writing down your prediction for each line first.
2. **Part B, a string, two ways.** Walk a string character-by-character using `s[i]`, and again using `*(s + i)`, printing both side by side to prove, for every index, that they match.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Pointer Field Trip |
|---|---|
| Declaring a pointer (`int *p = &n;`) | Part A, milestone 2. |
| `&` to get an address, `%p` to print one | Part A, milestones 2-3. |
| `*p` to read and write through a pointer | Part A, milestone 3. |
| Pointers are 8 bytes regardless of type | Part A, milestone 4 (stretch). |
| String is `char *`; `s[i]` vs. `*(s + i)` | Part B, milestones 5-6. |

### Milestones (build them in order, each one works on its own)

1. **Set up.** On cs50.dev, create `pointer_trip.c` with `#include <stdio.h>` at the top and an empty `int main(void)`.
2. **Predict before you print.** Inside `main`, declare `int n = 50;` then `int *p = &n;`. Before writing a single `printf`, write down (in a comment, or on paper) what you expect each of the following to print: `n`, `&n`, `p`, `*p`. Note which format code each needs: `%i` for a value, `%p` for an address.
3. **Reveal and compare.** Now add the four `printf` calls from your prediction list, compile with `make pointer_trip`, and run it. Confirm `&n` and `p` print the *same* address, and `n` and `*p` print the *same* value. Then add one more line, `*p = 100;`, followed by `printf("%i\n", n);`, predict what it prints *before* running, then confirm.
4. **Measure a pointer (stretch).** Add `printf("%zu\n", sizeof(p));` (the `z u` format code prints an unsigned size). Confirm it prints `8`. Then declare a second pointer to a different type, such as `char *c;`, and confirm `sizeof(c)` is also `8`, even though a `char` and an `int` are different sizes.
5. **Walk a string two ways.** In the same file (or a new one, `string_walk.c`), declare `char *s = "computer";`. Write a `for` loop from `i = 0` up to (and including) `strlen(s)` that prints, on each pass, both `s[i]` and `*(s + i)` as characters (`%c`) side by side. Confirm every single row matches, including the final row at the null terminator.
6. **Prove the address equivalence (stretch).** Add one line printing `%p` for both `s` and `&s[0]`. Confirm they are identical: this is the concrete proof that a string variable *is* the address of its first character.

### How you will know you are done

- ✅ You wrote your predictions for `n`, `&n`, `p`, `*p` *before* compiling, and can say whether each one matched.
- ✅ `&n` and `p` print identical addresses; `n` and `*p` print identical values.
- ✅ After `*p = 100;`, printing `n` shows `100`, proving you changed `n` by going through `p`, not by touching `n` directly.
- ✅ `sizeof(p)` and `sizeof(c)` (or any other pointer type) both print `8`.
- ✅ Your character-by-character walk shows `s[i]` and `*(s + i)` matching for every index from `0` through the null terminator.

> 💡 **Keep yourself honest:** don't peek at the output before writing your prediction down. The entire point of this capstone is catching the moment your mental model and the computer's actual behavior either agree or don't: that gap is exactly where the learning happens.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: `sizeof` roulette (foundational)
Declare a few different pointer variables (`int *a;`, `char *b;`, and if you're comfortable, `double *c;`) and print `sizeof` each one with `%zu`. Confirm they're all `8`, no matter what they point to. Then print `sizeof(int)`, `sizeof(char)`, and `sizeof(double)` themselves, and notice those numbers *do* differ. Write one sentence explaining, in your own words, why the pointer sizes don't change but the pointed-to sizes do.

### Exercise 2: String detective (intermediate)
Given `char *s = "hello";`, predict, then print, `s`, `s + 1`, and `s + 2` using `%s` for each. In one sentence per line, explain why each one prints what it does, and why all three, despite starting from different characters, still know exactly when to stop.

### Exercise 3: Write through a pointer, from a function (advanced)
Write a small function `void bump(int *p)` that adds `1` to whatever `p` points to (`*p = *p + 1;`). In `main`, declare an `int` set to any starting value, print it, call `bump` by passing its *address* (`bump(&n);`), then print it again. Confirm the value changed, even though you never reassigned `n` directly in `main`. This is your first hint at why functions ever need pointers at all, a thread this course picks back up soon.

---

## Cheat sheet

```text
DECLARING A POINTER
  int *p;          p can store the address of an int (not yet pointing anywhere valid)
  int *p = &n;      p now stores n's actual address

THE TWO JOBS OF *
  int *p            (in a declaration) -> "p is a pointer to an int"
  *p                 (on an existing pointer) -> "go to the address in p"
  *p                 on the right of =  -> READ the value there
  *p = 100;          on the left of =   -> WRITE a new value there

THE ONE JOB OF &
  &n                "the address of n"

POINTER SIZE
  sizeof(any pointer) == 8 bytes (64 bits) on a modern machine, ALWAYS,
  no matter what type it points to.

STRING = CHAR *
  string s            (cs50.h)  is just a friendlier name for...
  char *s              ...the address of s's first character.
  s                    the address of the first character
  &s[0]                same address as s
  s + i                the address of the (i+1)-th character
  &s[i]                same address as s + i
  s[i]                 the (i+1)-th character itself
  *(s + i)             same character as s[i]  <- array syntax is sugar for this

FORMAT CODES USED TODAY
  %i    an int value          %p    a memory address
  %s    a string (until \0)   %c    a single character
  %zu   an unsigned size (from sizeof)
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 17:** "Pixels, hexadecimal, and memory addresses" taught you to read a hex address like `0x123`: today you finally got a variable that can *hold* one.
- **Next, Module 5 · Lesson 19:** "malloc, free, and hunting memory bugs": once you can store and follow addresses, the natural next question is "can I ask the computer for a brand-new chunk of memory of my own?" That's `malloc`, and it comes with new ways to get it wrong (and new tools, like Valgrind, to catch them).
- **Later, Module 6:** linked lists, and every other pointer-based structure you'll build, are, in Malan's own framing, nothing but structs and pointers wired together. Everything you practiced here is the entire prerequisite for that leap.

---

*Source: "CS50x 2026 - Lecture 4 - Memory" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
