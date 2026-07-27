# Module 5 · Lesson 20: Pass-by-Reference and File I/O

> **Course:** Self-Paced CS50x
> **Module 5:** Memory: see the bytes: pointers, the heap, and files
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 4 - Memory](https://www.youtube.com/watch?v=db0H0U13YsA) · [full transcript](../../transcripts/06-lecture-4-memory.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

A C function normally only gets *copies* of the variables you hand it, so it cannot change your originals, unless you hand it their addresses instead (pass by reference), which is also exactly how you read keyboard input safely with `scanf` and how you read and write actual files on disk with `fopen`, `fprintf`, and `fread`/`fwrite`.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a broken swap function, prove it fails, fix it with pointers, and then build a phonebook that actually survives your program quitting, a real file on disk, not something that vanishes the moment the program ends. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Specific functions like `scanf` or `fopen` are C-specific, but the underlying idea, that a function can only modify what it's been given the *address* of, predates every modern language.
>
> - **[*The C Programming Language*](https://en.wikipedia.org/wiki/The_C_Programming_Language) by Brian Kernighan and Dennis Ritchie (1978, 2nd ed. 1988).** Written by C's own creators, this is the original account of "call by value" and of using pointers to let a function reach back and modify a caller's variable. Every later language's story about references, `inout` parameters, or "pass by reference" is a variation on the idea this book first wrote down.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Pass by value:** when you hand a variable to a function, C actually hands over a *copy* of its value. The function can do whatever it wants to that copy. Your original variable back in the caller is untouched.
- **Pass by reference:** handing a function the *address* of a variable instead of a copy of its value, so the function can go to that address and actually change what you have.
- **The stack:** the region of a program's memory used for local variables and function calls. Every time you call a function, it gets a fresh chunk of the stack; that chunk disappears when the function returns.
- **The heap:** the region of memory that `malloc` hands out chunks from, one request at a time, for memory you want to control the lifetime of yourself.
- **`scanf`:** a C function that reads formatted input typed at the keyboard and stores it at an address you give it. It is one of the functions the CS50 library's `get_int` and `get_string` are built on top of.
- **Buffer overflow:** writing more data into a fixed-size chunk of memory (a "buffer," often an array) than that chunk was ever given room for, one of the most common causes of crashes and security bugs in C.
- **File I/O:** "input/output": reading data from, and writing data to, a file that lives on disk, using functions like `fopen`, `fprintf`, and `fclose`, so your data survives after the program that created it quits.
- **Byte:** 8 bits, the smallest unit files and memory are usually addressed in. A file, underneath everything, is just a sequence of bytes.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In **Module 5 · Lesson 19**, you learned to ask the computer for your own memory with `malloc`, to hand it back with `free`, and to use Valgrind to catch the memory bugs that happen when you forget. This lesson takes that same comfort with addresses and turns it into two very concrete new powers: making a function actually change the variables you gave it (instead of quietly doing nothing, which is the default), and making data outlive the program that created it by writing it to an actual file. As Malan puts it, plainly, about why this matters:

> "Previously to today if I asked you to write a function that swaps two values, you could not physically do it in code because you had no way of expressing the solution to this problem." (David Malan)

That is the whole reason this lesson exists: an entire category of useful programs (anything that needs a helper function to modify your data, anything that needs to remember something after it quits) was simply unwritable until now. By the end of this lesson you'll have written a program that persists real data to disk in a `.csv` file, which is not just a toy exercise: it is, in miniature, the same idea behind the database-backed web app you'll design and ship at the end of this course.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why passing a variable to a C function passes a *copy* of its value, and why that means the function cannot modify the caller's original variable.
2. Fix a broken `swap` function by changing it to accept pointers and dereference them, and explain in your own words why that works (pass by reference).
3. Describe the stack and the heap: what each one stores, which direction each one grows, and why letting them collide causes an overflow.
4. Rewrite `get_int`'s behavior using `scanf`, and explain why an uninitialized pointer handed to `scanf` can crash a program, a buffer overflow risk.
5. Open, write to, append to, and safely close a persistent `.csv` file using `fopen`, `fprintf`, and `fclose`, checking the return value for `NULL`.
6. Copy a file byte by byte using `fread` and `fwrite` in binary mode, and explain why that technique generalizes to any file type, including images.

## Prerequisites

- **Module 5 · Lesson 19: malloc, free, and hunting memory bugs**: you should already be comfortable with the `*` and `&` operators, calling `malloc` for heap memory, calling `free` when you're done with it, and reading a Valgrind report. This lesson uses all of that without re-teaching it.
- **Module 2 · Lesson 8: Functions, code quality, and the limits of numbers**: you should be comfortable writing a function with a prototype and understanding that variables declared inside one function are not visible inside another (scope).
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**): you'll compile and run every program in this lesson there.

---

## Part 1: The glass-swap demo, translated into broken code

Before any code, Malan runs a live demo. He hands a volunteer, Olivia, two glasses (one with blue liquid, one with orange) and announces he's poured them into the wrong glasses. Her job: swap them, without mixing the colors. She hesitates, because with only two glasses, there's nowhere to put one color while you move the other. The fix is a third, empty glass, a temporary holding spot:

> "So we're putting one value into the temporary variable, we're putting the other value into the original value." (David Malan)

That is the entire algorithm for swapping two values: copy the first into a temporary spot, copy the second into the first's spot, copy the temporary into the second's spot. Translated directly into C, it looks completely reasonable:

```c
#include <stdio.h>

void swap(int a, int b);

int main(void)
{
    int x = 1;
    int y = 2;

    printf("x is %i, y is %i\n", x, y);
    swap(x, y);
    printf("x is %i, y is %i\n", x, y);
}

void swap(int a, int b)
{
    int temp = a;
    a = b;
    b = temp;
}
```

Run it, and the output is not what you'd expect:

```text
x is 1, y is 2
x is 1, y is 2
```

`x` and `y` are completely unchanged. The swap function ran, and if you'd printed `a` and `b` *inside* `swap`, you'd have seen them successfully swap, but that success never reaches `main`. Why? Because of **scope** (`a` and `b` live inside a different pair of curly braces than `x` and `y` do) combined with a rule that's been true every single time you've called a function so far:

> "Well, in C, all this time, any time you pass in arguments to a function, you are passing in those arguments by value, so to speak. You're literally passing in copies of the variables to the function you are calling." (David Malan)

`a` is a *copy* of `x`. `b` is a *copy* of `y`. Swapping the copies inside `swap` is like Olivia swapping two glasses that only *look* identical to the ones back at the front table: nothing that happens to the copies travels back to the originals.

> 🔑 **The single most important takeaway of this part.** Passing a variable to a function in C passes a copy of its value ("pass by value"): the function can change that copy all it wants, and your original variable, back where you called it from, will never notice.

---

## Part 2: Where variables actually live: the stack and the heap

To see *why* `a` and `b` are separate from `x` and `y`, it helps to know how a running C program actually uses your computer's memory. Malan draws it as one long strip of memory, divided into regions by convention:

```text
 edge of memory (start)
 +---------------------------------------+
 |  Machine code                         |   the compiled 0s and 1s
 |  (the program itself)                 |   of your program
 +---------------------------------------+
 |  Global variables                     |   declared outside every
 |  (declared outside any function)      |   function, so they're
 +---------------------------------------+   reachable from anywhere
 |                                        |
 |             THE HEAP                  |   malloc() hands out chunks
 |               |                       |   from here, one request
 |               v   grows DOWNWARD      |   after another
 |                                        |
 |          . . . . . . . . .            |   <- if heap and stack
 |                                        |      ever meet: overflow
 |               ^   grows UPWARD        |
 |               |                       |
 |             THE STACK                 |   local variables and
 |     (one "frame" per function call)   |   function arguments
 +---------------------------------------+
 edge of memory (end)
```

Malan describes the two regions this way:

> "There's this big chunk of memory below that called the heap. The heap is the chunk of memory that malloc uses to allocate memory for you." (David Malan)

> "The stack is the area of memory that's used any time you create local variables or call functions." (David Malan)

The stack is used automatically, every single time you call a function. You've been using it since week one without knowing its name. Each call gets its own **frame**: a chunk of stack memory holding that function's parameters and local variables. When `main` calls `swap`, the picture looks like this:

```text
STACK (grows upward: each call adds a new frame on top)

 +------------------------------+
 |  swap's frame                |
 |    a = 1   (a copy of x)     |
 |    b = 2   (a copy of y)     |
 |    temp = (local variable)   |
 +------------------------------+
 |  main's frame                |
 |    x = 1                     |
 |    y = 2                     |
 +------------------------------+
```

`swap`'s frame sits on top of `main`'s frame, a completely separate chunk of memory. When `swap` finishes, its frame is popped off the stack (freed up for the next function call); `main`'s frame, with its own `x` and `y`, was never touched. That separateness is *why* pass by value can't reach back into the caller, and it's also why, if a program calls functions too deeply (for instance, unbounded recursion) or asks `malloc` for too much heap, the stack and the heap can grow toward each other until they collide. That's the origin of a term you may have already heard:

> "There's a very popular website called Stack Overflow, and this is the etymology thereof." (David Malan)

A **stack overflow** is what happens when the stack runs out of room (often from a function that calls itself without ever stopping) and grows into memory it shouldn't. A **heap overflow** is the mirror image on the heap's side. Either one, in the real world, crashes your program.

> 🔑 **The single most important takeaway of this part.** Every function call gets its own frame of stack memory that disappears when the function returns; `malloc` hands out separate memory from a different region, the heap. That's the real reason `swap`'s `a` and `b` are physically different memory from `main`'s `x` and `y`.

---

## Part 3: Fixing swap with pointers: pass by reference

Now that pass by value has an actual mechanism behind it (separate stack frames), the fix becomes concrete: instead of giving `swap` copies of the values, give it a "treasure map" to where the real values live.

> "We now have the ability to pass by reference, that is use pointers and addresses more generally to tell the function how to go to an address and do something there, how to go to another address and do something there." (David Malan)

In practice, that means three small changes to the broken program from Part 1: make the parameters pointers (`int *a`, `int *b`), dereference them everywhere you used to use them directly, and pass in *addresses* (`&x`, `&y`) at the call site instead of the values themselves.

```c
#include <stdio.h>

void swap(int *a, int *b);

int main(void)
{
    int x = 1;
    int y = 2;

    printf("x is %i, y is %i\n", x, y);
    swap(&x, &y);
    printf("x is %i, y is %i\n", x, y);
}

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

Run it now, and:

```text
x is 1, y is 2
x is 2, y is 1
```

It works. Pictorially, `a` no longer holds a copy of `1`. It holds the *address* of `x`, so `a` points at `x` the way a foam finger points at something across the room. `*a` (the dereference operator, recapped from Lesson 19: `*` on an existing pointer means "go to the address it holds") means "go to wherever `a` is pointing and use the value that's actually there." So `*a = *b` genuinely means "go to `x`'s address and put what's at `y`'s address there", not a copy-of-a-copy, but the real thing.

> ✅ **What to do about it:** any time you want a function to modify a caller's variable, give the function a pointer to that variable (`&variable` at the call site, `type *parameter` in the function signature), and use `*parameter` inside the function to read or write the real value.

---

## Part 4: scanf, an uninitialized pointer, and buffer overflows

Pass by reference is not just for fixing your own functions: it's *why* a built-in C function called `scanf` ("scan formatted input") needs an address, too. `scanf` is one of the functions the CS50 library's `get_int` is quietly built on top of, and you can rewrite `get_int` yourself with it:

```c
#include <stdio.h>

int main(void)
{
    int n;
    printf("n: ");
    scanf("%i", &n);
    printf("n: %i\n", n);
}
```

Malan explains why the `&` is required here:

> "If scanf exists and it comes with C, its purpose in life is to scan an integer from the keyboard and put it somewhere you want. You can't just give it the variable name because it's going to get a copy of whatever garbage value is in there." (David Malan)

In other words: `scanf` is a function like any other, and functions receive their arguments by value. If you handed it `n` directly, `scanf` would only get a worthless copy of whatever garbage was already sitting in `n`: it needs `n`'s *address* so it can reach back and actually store your keystrokes there, exactly like the fixed `swap` above.

Strings, though, are where this gets genuinely dangerous. Since (from Lesson 19) a `char *` variable *is already an address*, you might reasonably try this, and it will very often seem to work at first:

```c
#include <stdio.h>

int main(void)
{
    char *s;              // BUG: s has never been given any memory
    printf("s: ");
    scanf("%s", s);        // writes wherever s HAPPENS to point, anywhere at all
    printf("s: %s\n", s);
}
```

No `&` is used here (a `char *` is already an address, so adding `&` would ask for the address of an address, a different concept entirely). The real bug is subtler and worse: `s` was declared but never pointed anywhere. It holds a **garbage value**: whatever leftover bits happened to already be in that spot of stack memory. Running Valgrind on this program surfaces the problem immediately: *"use of uninitialized value of size 8."* Every character `scanf` "successfully" stores is being written to a random, unallocated address:

> "You're touching memory that you yourself did not allocate as an array via malloc or some other mechanism." (David Malan)

The program might appear to work on a short input purely by luck (the random address `s` points to happens to be unused at that moment) and then crash unpredictably on a longer one, or corrupt something else in memory silently. This is a **buffer overflow** in its most basic form:

> "A buffer overflow is generally just a chunk of memory like an array that actually just gets overflowed with too many values." (David Malan)

The deeper problem is that you cannot know in advance how many characters a human is about to type (3, 30, or 3 million), so any fixed-size buffer you allocate yourself has to draw a line somewhere, and typing past that line corrupts memory C will not stop you from touching. `get_string` sidesteps this entirely by calling `malloc` again and again as you type, one more byte at a time, growing its buffer to fit, which is real, non-trivial work the CS50 library was quietly doing for you since week one.

| Format code | What you're handing `scanf` | Do you need `&`? |
|---|---|---|
| `%i` into an `int n` | the address of an already-existing `int` | Yes: `&n`, because `n` itself is just a value |
| `%s` into a `char *s` | the address `s` already holds | No: `s` *is* the address, but only if it was already pointed at real, allocated memory |

> ❌ **The trap:** declaring a `char *` and using it with `scanf("%s", ...)` before it has ever been pointed at real memory (via `malloc`, or by making it an array like `char s[5]`). It will compile without complaint and may even run without complaint, right up until the moment it corrupts something you care about.

---

## Part 5: A file that outlives the program: fopen, fprintf, fclose

Every program you've written so far, Malan points out, even last week's in-memory phonebook, loses everything the instant it quits. Its variables lived only on the stack and the heap, both of which are **RAM**: fast, but volatile (wiped the moment power is lost). To make data survive, you need to write it to **persistent storage** (a hard drive or SSD) using a new set of tools called **file I/O**:

> "A file is just a bunch of bytes that are stored on disk." (David Malan)

> "With file I/O though, we have the ability now to start creating, saving, editing, deleting files, much like you would from the File menu of Google Docs, Microsoft Word, or the like." (David Malan)

Let's build a real one: a phonebook that saves to `phonebook.csv`, a **CSV** ("comma-separated values") file, a plain-text way of storing rows and columns where each column is separated by a comma, openable in Excel, Numbers, or Google Sheets.

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    FILE *file = fopen("phonebook.csv", "a");
    if (file == NULL)
    {
        return 1;
    }

    char *name = get_string("Name: ");
    char *number = get_string("Number: ");

    fprintf(file, "%s,%s\n", name, number);

    fclose(file);
}
```

`fopen` opens (creating it, if needed) the file named `"phonebook.csv"`, and hands back a pointer, a `FILE *`, that every other file function needs, so they know which file to act on:

> "This is giving me a pointer to essentially the contents of that file. It's a bit of a white lie, technically giving you a pointer to a chunk of memory that represents that file, but for all intents and purposes it's a pointer to the file for now." (David Malan)

`fprintf` works exactly like `printf`, except its very first argument tells it *which* open file to write to. `fclose` then saves and releases the file: skip it, and your data may never actually make it to disk.

There's one live bug Malan makes and fixes on stage that matters more than it looks: he first opens the file with mode `"w"` (write), runs the program twice, and finds only the *second* entry survives. The first is gone. That's because `"w"` mode means "start writing from byte 0 every time," silently erasing whatever was already there. The fix is mode `"a"` (append): start writing from the *end* of the existing file, keeping everything already saved. Every run after that adds one more line, and the phonebook genuinely accumulates:

| Mode | Meaning | What happens to existing content |
|---|---|---|
| `"r"` | read | file must already exist; nothing is erased |
| `"w"` | write | file is created if missing: **erased and started over from byte 0** if it already exists |
| `"a"` | append | file is created if missing; existing content is **kept**, new writes go to the end |

And just like every pointer you've met since Lesson 19, `fopen` can fail (disk full, permissions wrong, path invalid) and signals that by returning `NULL`, the same sentinel value `malloc` returns on failure. Checking `file == NULL` before you do anything else with it is not optional politeness; it's the difference between a clean error and a crash.

> ✅ **What to do about it:** open files you intend to keep adding to with `"a"`, not `"w"`, and always check the return value of `fopen` against `NULL` before you touch the file it (maybe) gave you.

---

## Part 6: Copying bytes directly: fread, fwrite, and a teaser for image filters

Text files like `phonebook.csv` are one thing; not every file is text. A photo, a song, a program, all of them are, underneath everything, just a sequence of raw bytes. To handle *any* file, C gives you two lower-level functions that read and write bytes directly, rather than formatted text: `fread` and `fwrite`.

Malan builds a tiny, from-scratch version of the `cp` (copy) command every terminal already has, to show exactly how it works:

> "I want to copy this file from source to destination byte by byte, similar in spirit to a buffer like this where you're just grabbing from the internet one byte of the video at a time so as to watch it. In this case, I want to copy it." (David Malan)

```c
#include <stdio.h>

typedef unsigned char byte;

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        return 1;
    }

    FILE *src = fopen(argv[1], "rb");
    FILE *dst = fopen(argv[2], "wb");
    if (src == NULL || dst == NULL)
    {
        return 1;
    }

    byte b;
    while (fread(&b, sizeof(byte), 1, src) != 0)
    {
        fwrite(&b, sizeof(byte), 1, dst);
    }

    fclose(dst);
    fclose(src);
}
```

A few new pieces, each small: `typedef unsigned char byte;` gives the plain-old `char` type a more honest name for this job: a **byte** is 8 bits, and `unsigned` just means "don't interpret these bits as a possibly-negative number; they're raw data." The `"rb"` and `"wb"` modes are the same read/write modes from Part 5 with a `b` added, telling `fopen` this is **binary** data, not text, so nothing gets reinterpreted along the way. The loop itself is the whole idea in two lines: `fread` grabs the next single byte from the source file into `b` and reports back how many bytes it actually got (0 means "end of file, stop"); `fwrite` immediately writes that same byte to the destination. One byte, then the next, then the next, the exact same rhythm as a video player's buffer filling in while you watch.

This is also, finally, the full, honest answer to a question the class asked back in Part 4, why pointers are unavoidable for files:

> "In C without pointers you just can't do file IO unless it's abstracted away for you by some library." (David Malan)

Because `fread` and `fwrite` need to know *where* to put or get each byte, they take an address (`&b`) as their target, pass by reference, the same mechanism from Part 3, doing real work on real files.

And because this technique works byte by byte, on *any* file, it scales directly to something more fun than copying a phonebook: images. A photo is just a grid of pixels, each one a red, green, and blue value, stored back to back as bytes exactly like this. Once you can read and mutate a file's bytes, you can build actual photo filters:

> "You might be able to make it all grayscale by changing the R's, the G's, and the B's to... simpler values that are just black and white and gray tones. You might take that same photo as input and give it more of a sepia tone like an old school photograph instead." (David Malan)

That's this week's problem set, in one sentence: apply grayscale, sepia, reflection, and blur filters to real photographs, all of it built on nothing more than the `fread`/`fwrite` byte-copying loop you just wrote.

> 🎯 **The goal of this part:** notice that `fread`/`fwrite` don't care what the bytes *mean*: they'll copy a `.csv`, a `.bmp`, or any other file with the exact same eight-line loop. That generality is the whole point.

---

## Key takeaways

1. **Pass by value copies; pass by reference points.** A plain `int x` argument gives a function a copy it can't use to change your original; an `int *x` argument (with `&x` at the call site) gives it the real address, so `*x = ...` changes your actual variable.
2. **The stack and the heap are different neighborhoods of memory.** Function calls and local variables live on the stack (one frame per call, freed on return); `malloc`'d memory lives on the heap. Growing either one without bound risks a stack or heap overflow.
3. **`scanf` needs an address for the same reason your own functions do.** `%i` needs `&n`; `%s` into a `char *` doesn't need `&`, but only if that pointer already points at real, allocated memory.
4. **An uninitialized pointer is a loaded gun.** A `char *` that's never been pointed at allocated memory holds a garbage address; writing through it (via `scanf` or otherwise) is a buffer overflow waiting to happen, and it may not crash until much later.
5. **`fopen` returns a pointer you must check.** `NULL` means it failed; `"w"` erases existing content from byte 0, `"a"` appends to the end: pick `"a"` for anything meant to persist across runs.
6. **`fread`/`fwrite` move raw bytes, not text.** Open with `"rb"`/`"wb"`, and the exact same copy loop works on a CSV, an image, or any other file at all.

## Common pitfalls

- ❌ Writing a function that takes plain values when you actually need it to modify the caller's variables: you'll get correct-looking code that silently does nothing to your originals.
- ❌ Forgetting the `&` on a plain variable passed to `scanf` (for example, `scanf("%i", n)` instead of `scanf("%i", &n)`): it compiles, but writes to a garbage address instead of your variable.
- ❌ Declaring `char *s;` and using it with `scanf` or `strcpy` before it has ever been pointed at real, allocated memory: run it through Valgrind before you trust it.
- ❌ Opening a file you want to keep growing with `"w"` instead of `"a"`: every run silently erases what was there before.
- ❌ Skipping the `NULL` check after `fopen` (or `malloc`): the one time it fails silently is the one time your program crashes somewhere confusing, far from the real cause.
- ❌ Forgetting `fclose`: your writes may never actually be saved to disk.

---

## 🛠️ Capstone Project: Swap it, save it, copy it

> This is the main hands-on project for the lesson. You'll build three small, independent programs on cs50.dev, each one proving a single new power: mutating a caller's variables through a pointer, and reading and writing a persistent file. A CSV phonebook may look like a toy, but it's a database in embryo, and Module 8 grows this exact idea into a real Python-backed web app.

### What you will build

Three short C programs, each a self-contained milestone:

1. **`swap.c`**: first the broken pass-by-value version (and proof, from its own output, that it fails), then the pass-by-reference fix.
2. **`phonebook.c`**: appends a name and number you type in to `phonebook.csv` every time you run it, and the file survives across runs.
3. **(Stretch) `cp.c`**: your own byte-for-byte file copier using `fread`/`fwrite`, verified against any real file on your system.

### Why this is the perfect practice

| Lesson idea | Where you use it |
|---|---|
| Pass by value vs. pass by reference (Parts 1 and 3) | Writing, breaking, and fixing `swap.c` |
| The stack and function frames (Part 2) | Explaining out loud why the broken version fails before you fix it |
| `scanf` and pointer safety (Part 4) | Getting a name and number safely with `get_string`, understanding why it's safer than raw `scanf` |
| `fopen`/`fprintf`/`fclose` and `NULL` checks (Part 5) | Building `phonebook.c` |
| `fread`/`fwrite` and binary mode (Part 6) | The stretch-goal `cp.c` |

### Milestones (each one works and proves something on its own)

1. **Build the broken swap.** On cs50.dev, create `swap.c` with the pass-by-value version from Part 1 exactly as shown. Compile with `make swap` and run `./swap`. Confirm the printed output shows `x` and `y` *unchanged*: this is proof of the bug, not a mistake to hide.
2. **Fix it with pointers.** Change `swap`'s prototype and definition to take `int *a, int *b`, dereference them with `*` inside the function body, and pass `&x, &y` at the call site. Recompile and rerun; confirm the second `printf` now shows `x` and `y` genuinely swapped.
3. **Build a persistent phonebook.** Create `phonebook.c` using the code from Part 5: `fopen("phonebook.csv", "a")`, a `NULL` check, `get_string` for a name and a number, `fprintf` to save them as one CSV line, and `fclose`. Run it two or three times with different names and numbers.
4. **Prove it persists.** Open `phonebook.csv` directly (in the cs50.dev file explorer, or `cat phonebook.csv` in the terminal) and confirm every entry from every run is still there, in order: nothing got erased between runs.
5. **(Stretch) Byte-copy any file.** Write `cp.c` from Part 6 using `fread`/`fwrite` in binary mode. Run it on `phonebook.csv` (or any other small file you have) to produce a copy, then open the copy and confirm its contents match the original exactly.
6. **(Stretch) Verify without trusting your eyes.** Compare the original and the copy with the terminal's own `diff original copy` (or `cmp`). No output means the files are byte-for-byte identical: the strongest proof your `fread`/`fwrite` loop is correct.

### How you will know you are done

- ✅ `./swap`'s output visibly changes between the broken version (Milestone 1) and the fixed version (Milestone 2): you have the "before" and "after" to compare.
- ✅ `phonebook.csv` contains every entry from every run of `phonebook.c`, not just the most recent one.
- ✅ Your `fopen` calls in both `phonebook.c` and (if attempted) `cp.c` check for `NULL` before doing anything else with the file.
- ✅ (Stretch) `diff` reports no differences between your original file and `cp.c`'s copy of it.

> 💡 **Keep yourself honest:** actually run the broken `swap.c` and look at its wrong output before you fix it. Skipping straight to the fixed version means you never see the exact failure pass by value causes, and that failure is the whole reason pass by reference exists.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Increment by reference (foundational)
Write a function `void increment(int *n)` that adds one to whatever integer `n` points to. In `main`, declare an `int` set to some starting value, print it, call `increment` on its address, and print it again to confirm it actually changed.

### Exercise 2: A phonebook that loops (intermediate)
Modify `phonebook.c` from the Capstone so that, instead of quitting after one entry, it asks "Add another? (y/n)" in a loop, appending a new name and number to `phonebook.csv` each time you answer `y`, all within a single run of the program.

### Exercise 3: Count the bytes without copying them (advanced)
Write a program that takes one filename as a command-line argument, opens it in binary read mode, and uses `fread` in a loop (like `cp.c`'s) to count how many total bytes the file contains, without writing anything to a second file. Print the final count. Check your answer against the file size your operating system reports.

---

## Cheat sheet

```text
PASS BY VALUE vs PASS BY REFERENCE
  void f(int a)     // gets a COPY of the caller's value: can't change the original
  void f(int *a)    // gets the caller's ADDRESS: *a = ... changes the real thing
  call: f(x)        // pass by value
  call: f(&x)        // pass by reference

STACK vs HEAP
  STACK  - local variables + function call frames, one frame per call, freed on return
  HEAP   - malloc()'d memory, lives until you free() it
  Both share one finite pool of memory; let them collide -> stack/heap overflow

scanf
  scanf("%i", &n);     // n is an int  -> need & to get its address
  scanf("%s", s);      // s is char *  -> already an address, but MUST already
                        //                 point at real, allocated memory first

FILE I/O
  FILE *file = fopen("name.csv", "a");   // "r" read, "w" write (ERASES!), "a" append
  if (file == NULL) { return 1; }         // always check
  fprintf(file, "%s,%s\n", name, number); // like printf, but to a file
  fclose(file);                            // saves it, don't skip this

BYTE COPYING
  typedef unsigned char byte;
  FILE *src = fopen(argv[1], "rb");   // "b" = binary mode
  FILE *dst = fopen(argv[2], "wb");
  byte b;
  while (fread(&b, sizeof(byte), 1, src) != 0)
  {
      fwrite(&b, sizeof(byte), 1, dst);
  }
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 19 (malloc, free, and hunting memory bugs):** gave you the `*`/`&` vocabulary, `malloc`/`free`, and Valgrind. This lesson spends that vocabulary on two new jobs: mutating a caller's variables and reading/writing files.
- **Next, Module 6 · Lesson 21 (Stacks, queues, and resizable arrays):** be careful not to confuse "the stack" (this lesson's region of memory) with "a stack" (a data structure you'll build next lesson): they share a name because the data structure behaves the same way (last in, first out), which is exactly why memory's stack is called that.
- **Later, Module 8 · Lesson 28:** reopens this exact `phonebook.csv` idea, rebuilt in Python, proof that the *concept* of a persistent, row-and-column file survives even when the language and the syntax around pointers disappears.

---

*Source: "CS50x 2026 - Lecture 4 - Memory" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
