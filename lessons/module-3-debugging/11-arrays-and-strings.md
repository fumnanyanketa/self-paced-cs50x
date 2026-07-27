# Module 3 · Lesson 11: Arrays and Strings Under the Hood

> **Course:** Self-Paced CS50x
> **Module 3:** Debugging and what the compiler hides: debug systematically and see how C really stores data
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 2 - Arrays](https://www.youtube.com/watch?v=h5Gc1n8ZuU8) · [full transcript](../../transcripts/04-lecture-2-arrays.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

An array lets you replace a pile of copy-pasted variables with one variable and a number in square brackets, because C actually stores it as one unbroken block of memory, and once you see that a string is nothing more than an array of characters ending in a hidden terminator byte, functions like `strlen`, `islower`, and `toupper` stop looking like magic tricks and start looking like ordinary loops over memory you could have written yourself.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *The Word Inspector*, where you read a word from the user, print its length, print every character alongside its numeric code and its position in the array, and then uppercase it two different ways. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Languages and libraries come and go, but the idea taught here, that a string is just a contiguous run of bytes with a sentinel marking its end, is as old as C itself. For the timeless, tool-agnostic version:
>
> - **[*The C Programming Language*](https://en.wikipedia.org/wiki/The_C_Programming_Language_(book)) by Brian Kernighan and Dennis Ritchie (1978).** Written by the creators of C, this is the original account of arrays as contiguous memory and of the null-terminated string convention that `printf`, `strlen`, and every function in this lesson still rely on today, decades later.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Array:** one variable that holds several values of the same type, back to back, that you reach by position instead of by separate names.
- **Contiguous memory:** memory laid out with no gaps: element 1 sits immediately after element 0, element 2 immediately after that, and so on, like houses in a row with no empty lots.
- **Index:** the position of a value inside an array, written in square brackets. Indexes in C always start at 0, so the first element is at index `0`, not `1`.
- **Magic number:** a literal value (like `3`) typed directly into your code in more than one place, with no name explaining what it means or tying the copies together. If it needs to change, you have to remember every place it appears.
- **Constant:** a variable whose value is set once and can never change afterward. In C you mark one with `const` before the type.
- **Truncation:** what happens when you divide two whole numbers (`int`s) in C: the decimal part of the answer is simply thrown away, not rounded.
- **ASCII:** the standard table that assigns every letter, digit, and punctuation mark a whole number from 0 to 255, so that a computer (which only stores numbers) can also store text.
- **Null terminator:** a single hidden byte, written `\0` and worth exactly the number 0, that C automatically places right after the last real character of a string, so functions know where the string ends.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In the last lesson you deliberately broke and fixed small programs to learn how to *find* mistakes. This lesson is about something a little different: a design mistake that isn't a bug at all: code that compiles, runs, and gives the right answer, but is built in a way that falls apart the moment your problem gets bigger. Three separate `int` variables for three problem-set scores works fine. Thirty separate variables for thirty problem-set scores is absurd. Malan puts the underlying question plainly while looking at his own three-variable version of that exact program:

> "Think about the extreme. If you don't have 3 scores, but 30 or 300, is this really going to be the best way to do it?" (David Malan)

The fix, arrays, also happens to unlock the single biggest reveal of the whole lecture: that a string, which you've been treating as a black box since week one, is just an array in disguise. Once you can see that, whole categories of programs (reading levels, ciphers, and later the very web app you'll build in this course) become loops over bytes instead of mysteries.

## Learning objectives

By the end of this lesson you will be able to:

1. Declare a fixed-size C array, initialize its elements, and read or write any element using square-bracket indexing.
2. Explain why C stores arrays as contiguous memory, and rewrite a hard-coded array size as a named `const int` to remove a magic number.
3. Write a function that accepts an array and its length as two separate parameters, and correctly cast an `int` to a `float` to avoid truncating an average.
4. Explain why a C string is really an array of `char` terminated by `\0`, and predict what happens when you deliberately read one array position past the end of a string.
5. Use `strlen`, `islower`, and `toupper` from `string.h` and `ctype.h` to inspect and transform a string, and explain why recomputing `strlen` inside a loop's condition on every pass is wasteful.

## Prerequisites

- **Module 3 · Lesson 10: From source code to machine code**: this lesson assumes you're comfortable with `int`, `float`, and `printf` format codes, and with the idea that a variable simply occupies some number of bytes in memory.
- **Module 2 · Lesson 7: Conditionals and loops**: you'll write `for` loops and `while` loops throughout this lesson.
- **Module 2 · Lesson 8: Functions and limits**: you'll write your own function (`average`) with a prototype, and you already met integer truncation briefly there.

---

## Part 1: From three variables to one array

Malan starts with the most ordinary program imaginable: three problem-set scores, three separate `int` variables, and their average.

```c
#include <stdio.h>

int main(void)
{
    int score1 = 72;
    int score2 = 73;
    int score3 = 33;

    printf("Average: %i\n", (score1 + score2 + score3) / 3);
}
```

(He picked those particular numbers, 72, 73, and 33, on purpose, as an old friend from an earlier lesson. Hold onto them; they'll reappear later in this lesson in a different disguise.)

This works. But it does not scale, and Malan names the flaw directly:

> "Think about the extreme. If you don't have 3 scores, but 30 or 300, is this really going to be the best way to do it?" (David Malan)

The fix is the **array**: one variable that reserves a whole run of memory for several values of the same type, which you reach by position instead of by a separate name for each one.

> "An array is a chunk of contiguous memory back to back to back, whereby if you want to store 3 things, you ask the computer for a chunk of memory for 3 things. If you want 30, you ask for one chunk of size 30." (David Malan)

**Contiguous** just means "with no gaps": element 0 sits directly next to element 1, which sits directly next to element 2, like houses in a row with no empty lots between them. This is exactly what the debugger's "Variables" pane in the last lesson was quietly hinting at: every value you store, no matter its type, is just bytes sitting somewhere in memory. Malan is explicit that "somewhere" has no real shape at all:

> "The computer has no notion of up, down, left, right... it's just a piece of hardware that's got lots of bytes available that can be addressed from the first byte all the way down to the last byte." (David Malan)

Any grid or row you see drawn on a whiteboard (or in this lesson) is a human convenience for talking about memory: the hardware itself is just one long sequence of addressable bytes.

### The syntax

Declaring an array names its element type, gives it a name, and states its size in square brackets:

```c
int scores[3];
```

This reserves room for exactly three `int`s, all contiguous, all reachable through the one name `scores`. You fill in (or read) individual elements with an **index**: the position of a value inside the array, written in square brackets, always counting from 0:

```c
scores[0] = 72;
scores[1] = 73;
scores[2] = 33;
```

Rewriting the averaging program with an array:

```c
#include <stdio.h>

int main(void)
{
    int scores[3];
    scores[0] = 72;
    scores[1] = 73;
    scores[2] = 33;

    printf("Average: %i\n", (scores[0] + scores[1] + scores[2]) / 3);
}
```

Same answer, but now it's one variable instead of three, and if you needed a fourth score, you'd change one number (the size) instead of inventing a fourth variable name.

> 🔑 **The single most important takeaway of this part.** An array is not a new kind of data: it's a promise from the compiler that several values of the same type sit back to back in memory, so you can reach any of them with a name and a position instead of a separate variable for each one.

### Killing the magic number

Even the array version above still has a problem. The number `3` is typed twice: once as the array's size and once as the loop bound when you later fill it in a loop. Malan calls this out by name:

> "It's got a magic number, as people say." (David Malan)

A **magic number** is a literal value typed into your code in more than one place with nothing tying the copies together: if you ever need to change it, you're relying on your own memory (and honor system) to update every copy correctly. The fix is a named, unchangeable value:

> "...we should declare it as constant... it should not be changeable by you, by a colleague, a collaborator, or the like." (David Malan)

By convention, a **constant**, a value set once that can never change afterward, is written in `ALL_CAPS` so any reader immediately recognizes it as special:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    const int N = 3;
    int scores[N];

    for (int i = 0; i < N; i++)
    {
        scores[i] = get_int("Score: ");
    }

    printf("Average: %i\n", (scores[0] + scores[1] + scores[2]) / N);
}
```

Now the size lives in exactly one place, `N`, and both the array declaration and the loop bound refer to it. Change one number, and the whole program follows.

---

## Part 2: Passing arrays to functions, writing average()

The averaging math is still stuffed directly into `main`, and it still doesn't scale: you'd want the exact same averaging logic for a class of 3 students or 300. The next step is to package it into its own function, `average()`, that takes the array of scores as input.

Passing an array to a function needs one new piece of syntax. Because, unlike more modern languages, C cannot ask an array its own size, you must pass the length in separately, as a second argument:

> "If you've come into CS50 with programming before, you can usually just ask an array, AKA a vector, what its length is in Java and in Python and the like. You can't do that in C." (David Malan)

> "When you create your own function that takes an array as input, you have to take as input the length of the array." (David Malan)

```c
float average(int numbers[], int length);

int main(void)
{
    const int N = 3;
    int scores[N];

    for (int i = 0; i < N; i++)
    {
        scores[i] = get_int("Score: ");
    }

    printf("Average: %f\n", average(scores, N));
}

float average(int numbers[], int length)
{
    int sum = 0;
    for (int i = 0; i < length; i++)
    {
        sum += numbers[i];
    }
    return sum / (float) length;
}
```

Notice the parameter `int numbers[]`: empty square brackets. You don't repeat the size in the function's own signature; the function trusts whatever `length` you hand it alongside the array.

### The truncation trap, again

The very first version of `average()` you'd naturally write divides `sum / length`, where both are `int`s. That reintroduces a bug you first met at the end of Module 2: **truncation**, where dividing two whole numbers in C throws away everything after the decimal point rather than rounding. For scores 72, 73, and 33, the true average is 59.33, and an all-`int` division reports a flat, wrong `59`.

The fix is to make sure at least one value in the division is a `float` before the division happens:

> "It turns out so long as you involve like one float in your math, the whole thing is going to get promoted, so to speak, to floating point values instead of integers." (David Malan)

You have a few equally valid ways to do this (change `sum`'s type to `float`, divide by a literal `3.0` instead of `3`), but the most explicit and reusable one is an explicit **cast**: writing the target type in parentheses immediately before the value you want converted.

```c
return sum / (float) length;
```

`(float) length` doesn't change what's stored in `length`: it just tells the compiler "for this one calculation, treat this value as a float." Because one side of the division is now a `float`, C promotes the whole expression to floating point, and `average()` correctly returns `59.333333` instead of `59`.

> ✅ **What to do about it:** any time you divide to get an average, a percentage, or a rate, cast at least one operand to `float` (or `double`) *before* the division runs: casting the final result afterward is too late; the truncation already happened.

---

## Part 3: Chars, strings, and the null terminator

So far every array has held numbers. Now Malan turns the same square-bracket syntax on something you've been using since week one without looking underneath: the string.

### A char is a number in a costume

Start with three individual `char` variables: a **char** holds exactly one character, written in single quotes (not double quotes, which are reserved for strings):

```c
#include <stdio.h>

int main(void)
{
    char c1 = 'H';
    char c2 = 'I';
    char c3 = '!';

    printf("%c%c%c\n", c1, c2, c3);
}
```

This prints `HI!`, unsurprisingly. Malan draws the char/string line explicitly:

> "chars are single quotes, strings are double quotes" (David Malan)

But here's the trick: swap the `%c` format codes for `%i` (integer), with no other change to the variables themselves:

```c
printf("%i %i %i\n", c1, c2, c3);
```

This prints `72 73 33`, the exact same numbers as the averaging program from Part 1. That's not a coincidence Malan invented for this lesson alone; it demonstrates a real fact about how the computer stores characters:

> "there's nothing stopping me from telling the compiler, don't print these as chars, print them as integers." (David Malan)

Every character your computer can display is secretly a whole number under **ASCII**, the standard table assigning every letter, digit, and punctuation mark a number from 0 to 255. `'H'` is 72. `'I'` is 73. `'!'` is 33. A `char` variable and an `int` variable holding 72 are, in memory, the identical pattern of bits: `char` just tells `printf` which way to *display* it.

### A string is an array of chars

Now write the same three characters as a string instead:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string s = "HI!";
    printf("%s\n", s);
}
```

Because a `string` is just our training-wheels name for this idea, you can index into it exactly like the `scores` array from Part 1:

```c
printf("%c%c%c\n", s[0], s[1], s[2]);
```

Same output, `HI!`, because underneath, `s[0]` really is `'H'`, `s[1]` really is `'I'`, `s[2]` really is `'!'`. This is the connection the whole lecture has been building toward:

> "It's just going to be an array of characters, hence the dots we're trying to connect today." (David Malan)

**Strings are arrays for today's purposes.** A `char` is a one-byte number; a string is simply several of those bytes sitting contiguously, one after another, exactly the way `scores[0]`, `scores[1]`, and `scores[2]` sat contiguously.

### The hidden byte at the end

If a string is only as long as the characters you typed, how does `printf`'s `%s` know *where to stop*, especially once there's other data sitting in memory right after it? Malan answers this by deliberately poking one array position past the end of a 3-character string:

> "let's look 1 location past the end of this array." (David Malan)

Reading `s[3]` (one past `'H'`, `'I'`, `'!'` at indexes 0, 1, 2) with `%i` reveals a `0`:

```c
printf("%i\n", s[3]);   // prints 0
```

That zero is not an accident, and it is not garbage. C automatically appends one extra invisible byte, worth the number 0, to the end of every string literal, written as the escape sequence `\0` and called the **null terminator**:

> "The null character is just a byte of zero bits, and it represents the end of a string." (David Malan)

So the string `"HI!"`, three visible characters, actually occupies **four** bytes in memory: `'H'`, `'I'`, `'!'`, `\0`. Every function that walks a string (`printf`'s `%s`, `strlen`, the loop you're about to write yourself) works the same simple way: read one character at a time and stop the instant you hit that `\0`. That's also why two strings sitting next to each other in memory never bleed into one another when you print them: each one's own `\0` acts as a stop sign before the next string begins.

```text
Memory (each box is one byte):

  s[0]   s[1]   s[2]   s[3]
 +------+------+------+------+
 | 'H'  | 'I'  | '!'  | '\0' |
 |  72  |  73  |  33  |   0  |
 +------+------+------+------+
```

> 🔑 **The single most important takeaway of this part.** A C string is not a special built-in type: it is an array of `char` with one extra hidden byte, `\0`, glued onto the end automatically, so that any function reading it knows exactly where to stop.

---

## Part 4: string.h and ctype.h, stop reinventing the wheel

### Measuring a string yourself, then not

Knowing that a string ends at `\0`, you could count its length by hand with a `while` loop that walks forward until it hits that terminator:

```c
int n = 0;
while (name[n] != '\0')
{
    n++;
}
```

This genuinely works. But someone solved this exact problem decades ago and packaged the solution into a library function so nobody has to rewrite that loop ever again:

> "Someone else literally decades ago wrote the code that essentially looks quite like this but packaged it up in a function that you and I can use so we don't have to jump through these stupid hoops just to count the length of a string." (David Malan)

That function is `strlen` ("string length"), declared in the header file `string.h`:

```c
#include <string.h>

int n = strlen(name);
```

One line replaces the whole hand-rolled loop.

### Don't call strlen from inside a loop's condition

Here's a subtle trap. A perfectly reasonable-looking loop that prints a string one character at a time might check the length like this:

```c
for (int i = 0; i < strlen(s); i++)
{
    printf("%c", s[i]);
}
```

It produces correct output, but it's wasteful, and Malan is blunt about exactly why:

> "...you are literally using strlen again and again and again and like a crazy person you're asking the computer what's the length of S, what's the length of S? What's the length of S? It's not going to change." (David Malan)

Recall how a `for` loop actually runs: the condition (`i < strlen(s)`) is re-checked on *every single pass*. If `s` has 20 characters, that means calling `strlen`, which itself walks the whole string looking for `\0`, 20 separate times, recomputing an answer that never changes. The fix is to compute the length exactly once, store it, and reuse the stored value:

```c
for (int i = 0, n = strlen(s); i < n; i++)
{
    printf("%c", s[i]);
}
```

C lets you declare more than one variable before a `for` loop's first semicolon, as long as they share the same type, which is exactly what `i` and `n` do here (both `int`).

> ✅ **What to do about it:** if a loop's condition calls a function whose answer can't change between iterations (like `strlen` on a string you aren't modifying), compute it once before or at the start of the loop and reuse a variable: don't recompute it on every pass.

### Uppercasing: the hard way, then the easy way

Last piece: transforming a string, not just reading it. Say you want to force every character of user input to uppercase. Recall from Part 3 that lowercase and uppercase letters are just nearby ASCII numbers: Malan points out the exact distance between them:

> "lowercase a for instance, is 97, and they are all contiguous thereafter." (David Malan)

Uppercase `'A'` is 65. The gap between every matching lowercase and uppercase letter is a constant 32. So you *could* uppercase a character by hand: check whether it falls in the lowercase range, and if so, subtract 32:

```c
if (s[i] >= 'a' && s[i] <= 'z')
{
    printf("%c", s[i] - 32);
}
else
{
    printf("%c", s[i]);
}
```

This works, but just like `strlen`, someone already solved "is this character lowercase?" and "convert this character to uppercase" as reusable library functions, this time in `ctype.h`:

> "someone else years ago wrote the conditional code that checks if it's between little a and little Z." (David Malan)

`ctype.h` gives you `islower(c)` (true if `c` is a lowercase letter) and `toupper(c)` (returns the uppercase version of `c`, or passes any non-lowercase character through completely unchanged, no `if` needed at all):

```c
#include <ctype.h>

printf("%c", toupper(s[i]));
```

That one call replaces the entire `if`/`else` block above. (`ctype.h` also provides the mirror-image functions `isupper(c)` and `tolower(c)`, for exactly the opposite checks and conversions.)

Putting it together as `uppercase.c`:

```c
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string s = get_string("Before: ");
    printf("After:  ");

    for (int i = 0, n = strlen(s); i < n; i++)
    {
        printf("%c", toupper(s[i]));
    }
    printf("\n");
}
```

---

## Key takeaways

1. **An array is contiguous memory, addressed by index.** `int scores[3]` reserves three `int`-sized slots back to back; `scores[0]`, `scores[1]`, `scores[2]` reach them by position, starting at 0.
2. **Name your sizes.** A hard-coded number repeated in more than one place is a magic number; a `const int N` used everywhere that number belongs removes the bug of forgetting to update one copy.
3. **Functions can't ask an array its own length in C.** Always pass the length as a separate parameter alongside the array itself.
4. **Casting before dividing avoids truncation.** `sum / (float) length` promotes the whole division to floating point; casting after the division is too late.
5. **A string is an array of `char` plus one hidden `\0`.** That null terminator, worth the number 0, is what every string-reading function uses to know where to stop.
6. **Chars and their ASCII numbers are the same bits.** `'H'` and `72` are stored identically; `%c` and `%i` just choose how to display them.
7. **Don't reinvent, and don't recompute.** `strlen`, `islower`, and `toupper` already solve problems you could hand-roll; and once you've called `strlen` on an unchanging string, store the answer instead of calling it again on every loop iteration.

## Common pitfalls

- ❌ Hard-coding an array's size as a bare number in two or more places (the declaration and a loop bound) instead of one shared `const int`.
- ❌ Writing a function that takes an array but forgetting to also take its length as a separate parameter: C cannot recover it for you.
- ❌ Dividing two `int`s and expecting a decimal answer: cast one operand to `float` (or `double`) *before* the division, not after.
- ❌ Calling `strlen(s)` directly inside a `for` loop's condition, recomputing an unchanging answer on every single pass.
- ❌ Assuming a string ends wherever you stopped typing: it ends at the hidden `\0` the compiler appended, which is one byte *past* your last visible character.

---

## 🛠️ Capstone Project: The Word Inspector

> This is the main hands-on project for the lesson. You'll build a small program that reads one word and shows you, byte by byte, everything this lesson just taught about how C actually stores it, proving to yourself that a string really is an array, not just taking Malan's word for it.

### What you will build

A program, `inspector.c`, built on cs50.dev, that reads a single word from the user and reports on it in increasing detail: its length, every character's ASCII code and position, and two independently-computed uppercase versions of it that must agree with each other.

- Reading input and measuring it → `get_string` and `strlen`.
- Walking the array → a `for` loop indexing into the string with `[i]`.
- Chars as numbers → printing each character next to its ASCII code with `%c` and `%i`.
- Manual vs. library uppercasing → the hand-written `if`/subtract-32 version, then `toupper`.

### Why this is the perfect practice

| Lesson idea | Where you use it in The Word Inspector |
|---|---|
| Arrays and indexing (Part 1) | Every character of the word is reached with `word[i]`. |
| Passing length separately, casting (Part 2) | You'll reuse the pattern of computing a value once (the length) and reusing it, exactly like `average()`'s length parameter. |
| Strings as char arrays, the null terminator (Part 3) | You print each character's ASCII code, proving the string is really numbers underneath. |
| `string.h` / `ctype.h` (Part 4) | `strlen` measures the word once (not on every loop pass); `islower`/subtraction and then `toupper` uppercase it two ways. |

### Milestones (build them in order, each one works on its own)

1. **Read it and measure it.** Write a program that asks `get_string("Word: ")`, computes its length once with `strlen`, and prints `Length: <n>`. Confirm it reports the right length for a few different words, including a one-letter word and an empty string (just pressing enter).
2. **Show every character and its ASCII code.** Loop from `i = 0` to the stored length, and for each position print the character, its ASCII number, and its index, one per line: for example `s[2] = 'l' (108)`. This is where you prove to yourself a string is an array: you're indexing it exactly like `scores[i]` from Part 1.
3. **Uppercase it by hand.** Add a second loop that builds and prints an uppercased version using the manual check-and-subtract-32 technique from Part 4 (no `ctype.h` yet). Confirm it correctly leaves non-letters (spaces, punctuation, digits) untouched.
4. **Uppercase it again with `toupper`.** Add `#include <ctype.h>` and a third loop that uses `toupper` instead of your manual math. Print both uppercased results side by side and confirm they are character-for-character identical.
5. **Stretch goals.** Also print a lowercased version using `tolower`; count and print how many characters in the word were already uppercase before you touched them (using `isupper`); or handle multi-word input by printing the ASCII code of the space character too, and explain why it doesn't get uppercased.

### How you will know you are done

- ✅ `make inspector` compiles with no errors or warnings.
- ✅ For the input `Hi!`, your program reports length `3`, and lists `s[0] = 'H' (72)`, `s[1] = 'i' (105)`, `s[2] = '!' (33)`.
- ✅ Your manual uppercase loop and your `toupper`-based loop produce identical output for the same input.
- ✅ You can explain, out loud, why `strlen` is called exactly once in your program rather than inside a loop condition.

> 💡 **Keep yourself honest:** before you add `ctype.h`, actually run your manual, subtract-32 version on a string with a space or a digit in it. If your manual `if` check is wrong, you'll uppercase things that should never change: exactly the kind of logical bug `islower`'s already-tested library code protects you from.

This same byte-by-byte discipline (never trusting that a string "just works," always knowing how it's laid out and where it ends) is precisely what you'll rely on later when your database-backed capstone web app has to validate, trim, or compare a username or password field.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Kill the magic number (foundational)
Write a program that declares `int scores[5]` with a hard-coded `5` in the declaration and a separate hard-coded `5` in a `for` loop that fills it using `get_int`. Refactor it to use one `const int N = 5` in both places instead, then confirm the program still behaves identically. Change `N` to `7` and confirm both the declaration and the loop update automatically.

### Exercise 2: A sum() function (intermediate)
Write a function `int sum(int numbers[], int length)` that adds up every element of an array of integers and returns the total (no casting needed here, since an integer sum has no truncation risk). Write a prototype for it above `main`, call it on an array of at least 4 numbers you fill with `get_int`, and print the result.

### Exercise 3: Write your own strlen (advanced)
Without using `string.h`, write your own function `int my_strlen(string s)` that walks the string with a `while` loop looking for `'\0'`, exactly like the hand-rolled version in Part 4. Call both your `my_strlen` and the real `strlen` on the same `get_string` input and print both results side by side to confirm they always agree.

---

## Cheat sheet

```text
DECLARE AN ARRAY
  int scores[3];                declares room for 3 ints, uninitialized
  int scores[3] = {72, 73, 33}; declares AND fills it in one line (size optional here)
  scores[0] = 72;                assign one element (indexes start at 0)

PASS AN ARRAY TO A FUNCTION
  float average(int numbers[], int length);   <- always pass length separately, C can't ask
  average(scores, N);                          <- call site: array name, then its length

AVOID TRUNCATION
  sum / length            <- int / int  = truncates (wrong)
  sum / (float) length    <- cast BEFORE dividing = correct

CHAR <-> ASCII NUMBER (same bits, different %format)
  'H' = 72   'I' = 73   '!' = 33   'a' = 97   'A' = 65   (gap of 32)  '\0' = 0

STRING = ARRAY OF CHAR + HIDDEN \0
  "HI!"  ->  s[0]='H' s[1]='I' s[2]='!' s[3]='\0'   (4 bytes total, not 3)

string.h / ctype.h  (don't reinvent, don't recompute)
  strlen(s)      length of s, walks to '\0'   -> compute ONCE, reuse; don't call in loop condition
  islower(c)     true if c is a-z
  isupper(c)     true if c is A-Z
  toupper(c)     uppercase version of c (unchanged if not a lowercase letter)
  tolower(c)     lowercase version of c (unchanged if not an uppercase letter)

  for (int i = 0, n = strlen(s); i < n; i++)   <- the idiomatic, efficient pattern
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 10:** "From source code to machine code" established that every variable is just bytes sitting somewhere in memory: this lesson used that same idea to explain why arrays must be contiguous and why a string needs an explicit end marker.
- **Next, Module 3 · Lesson 12: Command-line arguments and a first cipher**: you'll meet `argv`, which is literally an array of strings, and write your first Caesar cipher by looping over a string's characters exactly the way you did in this lesson's `uppercase.c` and Word Inspector.
- **Later, Module 5 · Lesson 18** reveals what `string` was secretly hiding this whole time: a string is literally a `char *`, a pointer to the first character of exactly the kind of array you built by hand in this lesson.

---

*Source: "CS50x 2026 - Lecture 2 - Arrays" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
