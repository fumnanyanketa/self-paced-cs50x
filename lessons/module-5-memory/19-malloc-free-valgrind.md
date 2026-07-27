# Module 5 · Lesson 19: malloc, free, and Hunting Memory Bugs

> **Course:** Self-Paced CS50x
> **Module 5:** Memory: see the bytes, pointers, the heap, and files
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 4 - Memory](https://www.youtube.com/watch?v=db0H0U13YsA) · [full transcript](../../transcripts/06-lecture-4-memory.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

A string is really just an address, so comparing two strings with `==` compares their addresses instead of their characters, copying a string with a plain assignment gives you two names for the very same characters instead of two independent copies, and Valgrind is the tool that reads your program's memory habits back to you, line by line, so you can catch both mistakes, plus leaks and invalid touches, before they ship.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *The Deep-Copy Fix*, where you deliberately break string copying, watch it happen, fix it with `malloc`, `strcpy`, and `free`, and then use Valgrind to *prove* the fix is clean. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Memory-debugging tools will keep changing, but the discipline they enforce (every allocation needs a matching release, and you may only touch memory you were actually given) is permanent. For the timeless, tool-agnostic reference:
>
> - **[Valgrind Quick Start Guide](https://valgrind.org/docs/manual/quick-start.html)** (Valgrind Developers). The official documentation for the exact tool you use in this lesson's capstone. Bookmark it: you'll reach for Valgrind, or a descendant of it, in any language that hands you manual control over memory.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **`malloc`:** short for "memory allocate." A function that asks the computer for a specific number of fresh bytes and hands you back the address of the first one.
- **`free`:** the function you call to give memory back to the computer once you got it from `malloc` and no longer need it.
- **Memory leak:** memory your program asked for with `malloc` but never gave back with `free`. The computer keeps thinking it's in use, even though your program can no longer reach it.
- **`NULL`:** a special address (`0x0`, pronounced "null") that means "nothing lives here." Functions like `malloc` and `get_string` return it when they cannot give you what you asked for, so you must check for it before using whatever they returned.
- **Garbage value:** whatever bits already happen to be sitting in a chunk of memory before you put your own value there. It looks like a real number, but it means nothing, and it is not safe to rely on it.
- **Valgrind:** a separate program (not part of CS50) that runs your compiled code and watches every memory operation it performs, then reports which bytes were never freed and which memory accesses were invalid.
- **Heap:** the region of a running program's memory that `malloc` hands bytes out from. It is separate from where your ordinary local variables live, and it grows every time you allocate more.
- **Shallow copy:** copying a variable that holds an address, so both variables end up pointing at the exact same underlying data, instead of each getting its own independent copy (a "deep copy").

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

The last lesson revealed that a C string is really just a `char *`: the address of its first character, with a null terminator marking where it ends. That one fact has consequences you haven't hit yet: if a string is really an address, then comparing two strings, copying them, and losing track of memory you asked for all behave differently than they would for a plain number like an `int`. Malan is blunt about the discipline this requires:

> "So the rule of thumb quite simply is if you mallocked it, you must free it." (David Malan)

Get this lesson's three ideas right (compare with `strcmp`, copy with `malloc` and `strcpy`, and verify with Valgrind) and you have exactly the safety habits that Module 6's linked lists depend on, and that any long-running program needs, including the database-backed web app you'll design and ship as this course's final project.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why `==` compares addresses, not characters, when applied to two strings, and use `strcmp` to compare their actual contents instead.
2. Reproduce the shallow-copy bug, where two string "copies" secretly point at the same memory and mutating one appears to mutate both.
3. Write a correct deep copy of a string using `malloc`, `strcpy`, and a matching `free`.
4. Check the return value of `malloc` (and other functions) for `NULL` before touching the memory it points to.
5. Run Valgrind on a compiled program and use its output to find memory leaks and invalid reads or writes.
6. Explain what a garbage value is, and why dereferencing an uninitialized pointer is dangerous.

## Prerequisites

- **Module 5 · Lesson 18: Pointers, and what strings really are**: you should already be comfortable with `&` (address-of), `*` (dereference), and the fact that a C string is a `char *` pointing at its first character, terminated by `\0`.
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**): you'll compile and run real C code in the Capstone.

---

## Part 1: Comparing strings, why `==` lies to you

In week one, comparing two numbers was simple: `if (i == j)` checks whether the two *values* are equal, and it just works, because an `int` variable's own bytes hold the number itself.

```c
int i = 50;
int j = 50;

if (i == j)
{
    printf("same\n");   // this prints
}
```

Strings look like they should work the same way, but a string variable doesn't hold characters, it holds an *address*. `get_string` gives every call its own fresh chunk of memory, even if two people type the exact same word, so two strings that look identical almost always live at two different addresses:

```c
string s = get_string("s: ");
string t = get_string("t: ");

if (s == t)
{
    printf("same\n");
}
else
{
    printf("different\n");   // this prints, even if you typed "hi" both times
}
```

| What you compare | What `==` actually checks | Works as expected? |
|---|---|---|
| `int i = 50; int j = 50;` then `i == j` | The two integer *values*, stored directly in each variable | Yes |
| `string s = get_string(...); string t = get_string(...);` then `s == t` | The two *addresses* stored in `s` and `t`, not the characters they point to | No: fails even on identical input |

Malan puts the failure plainly:

> "If you literally compare S equals equal T, that's like saying does 0x123 equal equal 0x456, and that's obviously not true because those are literally two different addresses." (David Malan)

The fix is a function whose entire job is to walk both strings character by character until it finds a difference or reaches both null terminators: `strcmp` (string compare), from `string.h`. It returns `0` when the strings are identical, not `1`, which trips people up the first time:

```c
#include <string.h>

if (strcmp(s, t) == 0)
{
    printf("same\n");
}
else
{
    printf("different\n");
}
```

> 🔑 **The single most important takeaway of this part.** `==` on two strings compares *where* they live in memory, not *what* they say. Always compare string contents with `strcmp(s, t) == 0`, never with `s == t`.

---

## Part 2: Copying strings, the shallow-copy trap, and the fix

Copying an `int` is trivial: `int j = i;` gives `j` its own independent 4 bytes with the same value. It is tempting to assume copying a string works the same way:

```c
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

int main(void)
{
    string s = get_string("s: ");
    string t = s;                 // looks like a copy...
    t[0] = toupper(t[0]);         // capitalize the copy only, right?

    printf("s: %s\n", s);
    printf("t: %s\n", t);
}
```

Type `hi`, and both lines print `Hi`. The original changed too, even though the only line that touched anything was `t[0] = toupper(t[0]);`. Why? Because `t = s` doesn't copy the characters: it copies the *address*. Both variables now point at the one and only chunk of memory that holds `h`, `i`, `!`, `\0`.

> "S and T [are] both pointing to the same chunk of memory ... when that lowercase h becomes a capital H, it's as though both S and T have changed." (David Malan)

```text
Shallow copy (the bug):                   Deep copy (the fix):

  s ----> [ h | i | ! | \0 ]                s ----> [ h | i | ! | \0 ]   (untouched)
  t ---/  (same address as s)               t ----> [ h | i | ! | \0 ]   (its own memory)

  t[0] = 'H' also changes what s sees       t[0] = 'H' changes only t's own copy
```

To get a real, independent copy (a **deep copy**), you have to ask the computer for a brand-new chunk of memory yourself, then physically copy the bytes into it:

1. **Allocate room.** `malloc(strlen(s) + 1)`: `strlen(s)` gives the number of visible characters, and the `+ 1` reserves one more byte for the null terminator you'd otherwise silently drop.
2. **Check it worked.** `malloc` returns `NULL` if the computer has no memory left to give you. Touching that memory anyway is exactly the kind of mistake this lesson's third part shows going wrong.
3. **Copy the bytes.** Either a hand-written loop, or the library function built for this: `strcpy(destination, source)`.
4. **Free it when you're done.** Whatever you `malloc`, you must eventually `free` (see below).

```c
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    string s = get_string("s: ");
    if (s == NULL)
    {
        return 1;
    }

    string t = malloc(strlen(s) + 1);    // +1 for the null terminator
    if (t == NULL)
    {
        return 1;
    }
    strcpy(t, s);                        // now t has its own copy of s's bytes

    t[0] = toupper(t[0]);

    printf("s: %s\n", s);                // unchanged
    printf("t: %s\n", t);                // capitalized

    free(t);                             // t was mallocked, so it must be freed
    return 0;
}
```

Two details are easy to miss, and both matter:

> ✅ **What to do about it:** every successful `malloc` needs exactly one matching `free`, once you're truly done with that memory. If you never call `free`, the bytes stay reserved for the whole life of the program: that's a **memory leak**. Malan describes exactly what that looks like from the outside:
>
> "Your computer might get slower and slower and slower and slower, essentially because it's running out of memory, not physically, but the computer thinks it's using all of its memory even if it's not actively in use." (David Malan)

The one exception: `get_string` manages its own memory and frees it automatically once it's no longer needed, so `s` in the code above does **not** need a `free` call, only `t`, because `t` came from a `malloc` call you made yourself.

The second detail is the `NULL` checks. `malloc` can fail (no memory left to give you), and `get_string` can fail too (for instance, if there truly isn't room for what the user typed). Either way, you get back the special address `NULL`, and using it as if it pointed to real memory causes exactly the kind of crash this lesson's next part demonstrates on purpose:

> "What I should always have been doing since week one, but we consciously don't because it adds just too much overhead, is check if S equals equals null, then we should abort the program altogether." (David Malan)

---

## Part 3: Debugging memory errors, Valgrind, garbage values, and Binky

Some memory mistakes crash your program immediately. Others (like a leak, or writing one slot past the end of an array) don't crash anything most of the time, so eyeballing the code isn't reliable. That's the gap **Valgrind** fills: it's a separate program, not part of CS50, that runs your compiled code and watches every allocation, read, and write it makes.

> "Valgrind ... is a nice complement to something like debug50 and printf and the duck for actually chasing down specifically in this case memory related errors." (David Malan)

Consider a small, deliberately buggy program:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *x = malloc(3 * sizeof(int));   // room for 3 ints: valid indices 0, 1, 2
    x[1] = 72;
    x[2] = 73;
    x[3] = 33;                          // bug: index 3 doesn't exist
}                                       // bug: x is never freed
```

It compiles cleanly and, most of the time, runs without visibly crashing: the kind of "latent, harder to detect bug" Valgrind exists for. Running `valgrind ./memory` produces dense output, but two phrases carry almost all the useful information:

| Valgrind says | Plain-language translation | Where to look |
|---|---|---|
| `Invalid write of size 4` | You wrote 4 bytes (an `int`) somewhere you were never given permission to write | The line number Valgrind names, usually an off-by-one array index |
| `definitely lost NN bytes in 1 blocks` | You `malloc`'d `NN` bytes and the program ended without ever `free`ing them (a leak) | The line number of the original `malloc` call, listed further down in the same block |
| `in use at exit: 0 bytes` ... `0 errors` | Everything you allocated, you freed; nothing was touched out of bounds | Nowhere: this is what "clean" looks like |

The fix here is the same pattern from Part 2: use valid indices, check for `NULL`, and free what you allocated.

```c
int *x = malloc(3 * sizeof(int));
if (x == NULL)
{
    return 1;
}
x[0] = 72;
x[1] = 73;
x[2] = 33;
free(x);
```

**Garbage values.** Memory the computer gives you is never blank: it's whatever bits were left over from something else that used those bytes before. A program that prints an array without ever putting anything into it makes this visible directly:

```c
int scores[5];
for (int i = 0; i < 5; i++)
{
    printf("%i\n", scores[i]);   // prints leftover bits, not real scores
}
```

> "You have no idea what values are going to be in X and Y unless you yourself put those values there." (David Malan)

A garbage *number* is merely useless. A garbage **pointer** is dangerous, because dereferencing it means following an address you never chose to somewhere in memory you don't control. This is exactly the scenario in a claymation short, "Pointer Fun with Binky," that Malan's lecture screens at this point: two pointers, `x` and `y`, are declared, but only `x` is ever pointed at real allocated memory (its **pointee**, in the video's term for "the thing a pointer points at"). Binky, the character, tries to dereference the uninitialized `y` anyway:

> "Initially, pointers don't point to anything. The things they point to are called pointees, and setting them up's a separate step." (from the Binky video (Nick Parlante, Stanford CS Education Library), screened during the lecture)

> "I don't think dereferencing Y is a good idea because ... setting up the pointee is a separate step, and I don't think we ever did it." (from the Binky video, screened during the lecture)

Malan draws the moral directly:

> "The key detail was that bad things happened to Binky when we did this line of code, dereferencing an invalid pointer that had no true value assigned. It was just some garbage value." (David Malan)

```text
pointer x  ---->  [ pointee: 42 ]     (after malloc + *x = 42;  -- a real pointee)
pointer y  ---->  ????                (declared, never malloc'd or assigned -- garbage address)

*y = 13;   -->  undefined behavior: y points somewhere random, possibly invalid, memory
```

The video's fix (and the same fix as every `NULL` check in this lesson) is to never dereference a pointer until you know, concretely, what it points to: either by `malloc`-ing its own pointee, or by pointing it at something that already has one.

---

## Key takeaways

1. **A string is an address, so `==` compares addresses.** Two strings with identical characters at different addresses will always fail `==`; use `strcmp(s, t) == 0` to compare their actual contents.
2. **Assigning a pointer copies the address, not the data (a shallow copy).** `string t = s;` gives you a second name for the very same characters; change one, and the other appears to change too.
3. **A deep copy needs its own memory.** `malloc(strlen(s) + 1)` reserves room (including the null terminator); `strcpy(t, s)`, or your own character-by-character loop, actually duplicates the bytes.
4. **Every successful `malloc` needs a matching `free`, or you leak.** As Malan puts it: "If you mallocked it, you must free it." The one exception is `get_string`'s own memory, which the CS50 library frees for you automatically.
5. **Check for `NULL` before you use what a function gave you.** `malloc` and `get_string` both return `NULL` on failure; touching that memory anyway is how Binky's uninitialized pointer went wrong.
6. **Valgrind reads your program's memory habits back to you.** Its output is dense, but two phrases matter most: "invalid write/read" (you touched memory you don't own) and "definitely lost" (you never freed something you allocated).

## Common pitfalls

- ❌ Comparing strings with `if (s == t)`: that compares two addresses, not the words inside them. Use `strcmp(s, t) == 0` instead.
- ❌ Writing `string t = s;` and expecting an independent copy: you only get a second pointer to the same characters. Deep-copy with `malloc` + `strcpy` instead.
- ❌ Allocating `strlen(s)` bytes instead of `strlen(s) + 1`: you'll silently drop room for the null terminator and corrupt whatever memory happens to sit right after your string.
- ❌ Calling `malloc` without ever calling a matching `free`: a memory leak that Valgrind reports as bytes "definitely lost," and that would slowly degrade a long-running program such as a server.
- ❌ Dereferencing a pointer before it has ever been pointed at real memory: like Binky's `y`, this touches a garbage address and can crash your program.
- ❌ Calling `free` on memory that `get_string` gave you: CS50's library already frees that memory for you; only `free` what you yourself `malloc`'d.

---

## 🛠️ Capstone Project: The Deep-Copy Fix

> This is the main hands-on project for the lesson. You will deliberately break string copying, watch the bug happen with your own eyes, fix it properly with `malloc`/`strcpy`/`free`, and then use Valgrind, not your own eyeballs, to prove the fix is clean.

### What you will build

Two small C programs on cs50.dev, each a milestone building on the last, plus a series of Valgrind runs you read and interpret yourself:

- `copy_bad.c`: reproduces the shallow-copy bug on purpose.
- `copy_good.c`: the `malloc` + `strcpy` + `free` fix, first leaked on purpose, then corrected.

### Why this is the perfect practice

| Lesson idea | Where you use it in The Deep-Copy Fix |
|---|---|
| `==` compares addresses, not characters (Part 1) | Printing both strings' addresses with `%p` shows you directly why a shallow copy shares one address. |
| Shallow vs. deep copy (Part 2) | `copy_bad.c` is the shallow-copy bug; `copy_good.c` is the fix. |
| `malloc` / `free` / `NULL` checks (Part 2) | Every allocation in `copy_good.c` is checked and freed (or, on purpose, briefly isn't). |
| Reading Valgrind output (Part 3) | You diagnose your own leak from Valgrind's own words, the same way Malan diagnosed `memory.c`. |

This same discipline (allocate only what you need, check that it succeeded, free it when you're done) is exactly what keeps a long-running server, such as the database-backed web app you'll ship at the end of this course, from grinding slower and slower under its own memory leaks.

### Milestones (build them in order, each one works on its own)

1. **Reproduce the bug on purpose.** Write `copy_bad.c`: `get_string` into `s`, then `string t = s;`, then capitalize `t[0]` with `toupper`. Print both `s` and `t`. Run it and confirm both strings changed: see the bug with your own eyes before you fix it.
2. **Fix it with malloc + strcpy.** Write `copy_good.c`: after `get_string`, allocate `strlen(s) + 1` bytes with `malloc`, check the result for `NULL`, `strcpy` the source into it, then capitalize only the copy. Print both strings again and confirm only the copy changed.
3. **Leak on purpose.** In a copy of `copy_good.c`, delete (or comment out) the `free(t);` line, recompile, and run `valgrind ./copy_good`. Find the line reporting bytes "definitely lost," and check that the byte count matches `strlen(s) + 1`.
4. **Free it and confirm zero leaks.** Restore the `free(t);` line, recompile, and re-run `valgrind ./copy_good`. Confirm Valgrind's "in use at exit" reads 0 bytes and its summary reads 0 errors.
5. **Stretch goal.** Deliberately allocate one byte too few (`malloc(strlen(s))` instead of `+ 1`), rerun Valgrind, and explain in your own words why the missing room for the null terminator produced the error you now see.

### How you will know you are done

- ✅ You watched `copy_bad.c` corrupt both strings, and can explain why in terms of addresses, not "magic."
- ✅ `copy_good.c` capitalizes only the copy; the original string is untouched, confirmed by printing both.
- ✅ You have seen Valgrind report a real leak, then seen the very same program report zero leaks after adding `free` back.
- ✅ You can read a Valgrind "definitely lost" line and say, out loud, which `malloc` call it's blaming.

> 💡 **Keep yourself honest:** don't add `free` just because this lesson told you to: run Valgrind before and after so the tool confirms the fix, rather than taking it on faith.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: `==` vs. `strcmp` (foundational)
Write a program that `get_string`s two words from the user and prints `"same"` or `"different"` using plain `==`. Run it and type the exact same word twice: notice it (incorrectly) prints `"different"`. Now fix it using `strcmp`, and confirm identical input correctly prints `"same"`.

### Exercise 2: Write your own deep-copy function (intermediate)
Write a function `char *duplicate(string s)` that returns a brand-new, independently allocated copy of `s`: check for `NULL`, allocate `strlen(s) + 1` bytes, copy every character including the null terminator, and return the new pointer. Call it from `main`, capitalize the copy, and print both the original and the copy to prove they're independent. Remember to `free` whatever `duplicate` returns once you're done with it.

### Exercise 3: Hunt an off-by-one with Valgrind (advanced)
Write a program that calls `malloc(5 * sizeof(int))` for an array of 5 integers, then writes into indices `1` through `5` instead of `0` through `4` (one index too high). Compile it, run it under Valgrind, and use the "invalid write" line it reports to find and fix the bug. Free the memory and confirm Valgrind reports zero errors.

---

## Cheat sheet

```text
COMPARE STRINGS
  s == t              compares ADDRESSES -- almost always wrong for strings
  strcmp(s, t) == 0    compares CHARACTERS -- use this instead

COPY STRINGS
  string t = s;                       SHALLOW copy -- t is just another name for s's address
  string t = malloc(strlen(s) + 1);   DEEP copy -- give t its own memory...
  strcpy(t, s);                       ...then actually copy the bytes into it

MEMORY RULES
  if (t == NULL) return 1;    check every malloc (and get_string) before using the result
  free(t);                    every successful malloc needs exactly one matching free
  (get_string's own memory frees itself -- don't call free on it yourself)

VALGRIND
  valgrind ./program
  "invalid write/read of size N"          touched memory you don't own -- usually an off-by-one
  "definitely lost NN bytes in 1 blocks"   a malloc with no matching free -- a leak
  "in use at exit: 0 bytes" ... "0 errors"  clean -- everything allocated was freed and valid

GARBAGE VALUES
  An uninitialized variable or pointer holds leftover bits, not zero.
  Dereferencing an uninitialized POINTER (not just reading a garbage number) can crash your program.
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 18: Pointers, and what strings really are:** gave you `&`, `*`, and the fact that a C string is a `char *` pointing at its first character: this lesson's entire shallow-copy bug only makes sense once you know a string variable holds an address, not the characters themselves.
- **Next, Module 5 · Lesson 20: Pass-by-reference and file I/O:** applies the same "give the function an address, not a copy" idea to swap two variables' values, and opens the door to reading and writing files with `FILE *`.
- **Later, Module 6:** the linked list in `list.c` allocates a new node with `malloc` and frees it on every insert and delete: the discipline you built in this lesson's capstone (check for `NULL`, free what you allocate, confirm it with Valgrind) is exactly its safety training.

---

*Source: "CS50x 2026 - Lecture 4 - Memory" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
