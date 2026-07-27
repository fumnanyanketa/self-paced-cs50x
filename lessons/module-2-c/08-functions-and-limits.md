# Module 2 · Lesson 8: Functions, Code Quality, and the Limits of Numbers

> **Course:** Self-Paced CS50x
> **Module 2:** First real programs in C: write, compile, run, and fix real code in a terminal.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 1 - C](https://www.youtube.com/watch?v=SlqjA04_dpk) · [full transcript](../../transcripts/03-lecture-1-c.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

You will package repeated code into your own reusable C functions (complete with `void`, arguments, return values, and a prototype), learn the three separate lenses CS50 uses to judge whether code is actually *good* (correctness, design, and style), and see why every number a computer stores is secretly finite, which is why calculators glitch, a Boeing 787 once needed rebooting mid-fleet, and your computer's clock is scheduled to break again in 2038.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you refactor a hardcoded, repetitive Mario brick-grid
> program into properly designed functions with prototypes and a constant,
> and then deliberately break a number on purpose and explain why. Everything
> before the Capstone teaches the skills you will use there. If you want to
> see the finish line first, jump to the **"Capstone Project"** section, then
> come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** `float`, `double`, and 32-bit
> integers are C's particular choices, but the underlying problem, a finite
> number of bits can never represent an infinite number of real numbers, is
> universal to every programming language and every piece of hardware that
> has ever existed or ever will.
>
> - **["What Every Computer Scientist Should Know About Floating-Point Arithmetic"](https://dl.acm.org/doi/10.1145/103162.103163)** by David Goldberg (*ACM Computing Surveys*, 1991). The classic, still-cited paper explaining exactly why floating-point math can never be perfectly precise, no matter the language or hardware. You don't need to read it cover to cover today: knowing it exists, and why respected engineers still cite it decades later, is the point.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Function:** a named, reusable block of code that does one job: you "call" it by name instead of retyping its contents every time.
- **Argument:** a value you hand to a function when you call it, so the function can use it to do its job (also called an "input" or, once inside the function, a "parameter").
- **Return value:** a value a function hands back to whoever called it, so that value can be stored, printed, or used elsewhere.
- **Prototype:** a one-line preview of a function, its return type, name, and argument types, placed above `main` so the compiler knows the function exists before it sees the full definition.
- **Scope:** the region of code (marked by a pair of curly braces) where a particular variable actually exists and can be used; outside that region, as far as the compiler is concerned, the variable doesn't exist.
- **Integer overflow:** what happens when a whole number grows too large for the fixed number of bits set aside to store it, so it silently wraps around to a small or negative number instead of an error.
- **Truncation:** the silent loss of everything after the decimal point when you do math using whole-number (`int`) types instead of a decimal type.
- **Floating-point imprecision:** the small, unavoidable rounding error that shows up when a decimal number (like one-third) can't be represented exactly in a finite number of bits.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

By the end of Lesson 7 you could make a program branch and repeat, but you were also, as Malan is quick to call out, starting to *repeat yourself*: copy-pasting the same `printf` three times to make a cat meow, or writing the same guard-clause logic in two different loops. That repetition is exactly the itch this lesson scratches. As Malan puts it, "a lot of programming is about abstracting away your ideas, so you solve a problem once and then reuse it, reuse it, reuse it." This lesson also introduces the vocabulary CS50 (and, frankly, every software team) uses to talk about whether code is actually good, not just working, and it ends with a sobering, very real reminder that "working" still has hard limits, because computers can only count so high before they run out of room.

## Learning objectives

By the end of this lesson you will be able to:

1. Write your own C function with a `void` or typed return value, typed arguments, and a matching prototype, and explain why the prototype is necessary when the function's full definition appears below `main`.
2. Diagnose an "undeclared identifier" or "undeclared function" compiler error as either a scope problem or an ordering problem, and fix it by adding a prototype, moving code, or passing a value in as an argument instead of assuming it's visible everywhere.
3. Judge a piece of code separately on correctness, design, and style, and name which CS50 tool (`check50`, `design50`, or `style50`) checks each one.
4. Explain, starting from the single fact that computers store numbers in a finite number of bits, why integer overflow, truncation, and floating-point imprecision all happen, and recognize each one from its symptoms.

## Prerequisites

- **Module 2 · Lesson 7 (Conditionals and loops):** `if`/`else if`/`else`, `while`, `do while`, and `for` loops, plus the `int`, `float`, `char`, and `bool` types this lesson builds functions around.
- **Module 2 · Lesson 6 (Input, variables, and the CLI):** `get_int`, `get_char`, variables, and `printf` placeholders like `%i` and `%s`.

---

## Part 1: Custom functions and scope

### A function with no input and no output

C doesn't come with a function that makes a cat meow, any more than it comes with one that prints your name. When the built-in toolkit doesn't have what you need, you build it yourself. The simplest possible custom function takes nothing in and gives nothing back: it just has a side effect, like printing to the screen. Malan writes it like this:

```c
void meow(void);

int main(void)
{
    meow();
}

void meow(void)
{
    printf("meow\n");
}
```

Read the two `void`s separately: "for now, know that this is the return value of the function... void means it returns nothing." The second `void`, inside the parentheses, is the argument list: "void means it takes no inputs, and that makes sense because literally meow doesn't return anything, it doesn't take anything, it just meows." Everything else follows the pattern you already know for variables: a function declaration is a type (the return value), a name, and (inside parentheses) zero or more typed arguments.

### Giving a function an argument

A function that always meows exactly three times isn't very reusable. To let the caller decide, you give the function an **argument**: a value passed in when it's called. In C, declaring an argument works exactly like declaring a variable: you write the type, then the name.

```c
void meow(int n);

int main(void)
{
    meow(3);
}

void meow(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("meow\n");
    }
}
```

Malan's rule: "when you invent your own function in C and it takes one or more inputs, AKA arguments, you specify the type and the name of those as well." Inside `meow`, the parameter `n` behaves exactly like any other variable: you can loop over it, print it, or do math with it.

### The ordering problem, and why prototypes exist

If you write `main` first and put `meow`'s full definition below it (a very natural instinct, since `main` is the part of your program you actually care about), the compiler refuses to build it: `call to undeclared function 'meow'`. C compilers read top to bottom and take you completely literally. As Malan explains, "C compilers are fairly simplistic. They won't proactively do you the favor of checking all the way down to the bottom of the file. They're going to take you literally. So if `meow` doesn't exist as of line 9, that's on you."

You could fix this by moving `meow` above `main`, but then every function you write pushes `main`, the part of the file a reader actually wants to see first, further down the page. The real fix is a **prototype**: a copy of just the function's first line (its "signature"), with a semicolon, placed above `main`. Malan describes exactly what it does: "a prototype is just a bit of a hint to the compiler, a promise if you will, that hey, compiler, there will exist a function called `meow`, it takes no input and it returns no output, and it's on the honor system that it will eventually exist later in the file." That's why every code example above lists the prototype first, then `main`, then the full function definition: that's the conventional order in C, and you'll use it for the rest of the course.

> 🔑 **A function has three parts that must all agree with each other: a return type, a name, and a list of argument types.** The prototype states that agreement up front; the full definition (wherever it appears in the file) has to match it exactly.

### Scope: the same variable name doesn't always mean the same variable

Suppose you get lazy and try to let `meow` read a variable named `n` that you already created back in `main`, instead of passing it in as an argument:

```c
int main(void)
{
    int n = get_int("What's n? ");
    meow();          // meow doesn't take n as an argument...
}

void meow(void)
{
    for (int i = 0; i < n; i++)   // ...so this n is undeclared here
    {
        printf("meow\n");
    }
}
```

This fails to compile, and the reason is **scope**: the region of code, marked off by a pair of curly braces, where a given variable actually exists. As Malan puts it, diagnosing exactly this mistake, "even if you create `n` up here and use the name `n`, no other functions can see it, for that same issue of scope." The variable `n` inside `main`'s curly braces is invisible everywhere else, including inside `meow`'s own curly braces, no matter how similar the two functions' code looks.

The fix is the one you already know: pass the value in as an argument. But reusing the exact same name (`n`) for both the outer variable and the inner parameter invites confusion, so Malan renames the parameter to make the code self-documenting: "the solution is exactly what I did the first time: I can pass it into `meow` as input, and I have to tell C to expect that input... but instead of just calling it `n` and using `n` everywhere, this is crazy. Let's just call this `times`." The parameter's name is entirely your choice; it just needs to make sense to whoever reads it next.

```c
void meow(int times);

int main(void)
{
    int n = get_int("What's n? ");
    meow(n);
}

void meow(int times)
{
    for (int i = 0; i < times; i++)
    {
        printf("meow\n");
    }
}
```

### Getting something back: return values

Every function you've written so far either does something (`printf`) or gives something back (`get_int`), and now you can write the second kind yourself. Suppose you want a function whose whole job is to keep asking the user for a number until they give you one that isn't negative:

```c
int get_number(void);

int main(void)
{
    int n = get_number();
    meow(n);
}

int get_number(void)
{
    int n;
    do
    {
        n = get_int("What's n? ");
    }
    while (n < 0);
    return n;
}
```

Two things changed from every function so far. First, the return type in both the prototype and the definition is `int`, not `void`. Malan calls this out as new: "this notion of returning a value... is going to return, not void, which means nothing, but an integer, and that's the whole purpose of this function in life now." Second, the function body ends with a `return` statement, which both hands the value back to whoever called the function and immediately exits the function.

## Part 2: Code quality (correctness, design, and style)

Code that compiles and runs isn't automatically *good* code. Malan names three separate, independent lenses for judging it: "CS50, and really the world in general, tends to focus on these kinds of axes: correctness, design, and style."

- **Correctness** is the most basic: does the code do what it's supposed to? "In the context of a class, it should do exactly what the homework assignment... tells you to do. In the real world, it should do exactly what someone decided the software should do... correctness just means it behaves as it should."
- **Design** is about *how well* it does that, even when it's already correct. Malan points back to earlier examples in the lecture (code that asked three redundant questions when two would do) as "100% correct... but I was wasting the computer's time, I was wasting the human's time." As he puts it, design "is more about... not only saying things that are correct but doing it well: making a good, cogent argument, not just one that happens to be correct."
- **Style** is the most cosmetic of the three, and it's entirely for other humans, not the computer: "that's more of the aesthetics: is everything pretty printed, that is nicely indented, are variables well named and not just called X, Y, Z arbitrarily... style matters really to other humans, not to the computer, but to other humans."

CS50 gives you one tool per axis, and they check genuinely different things. Passing one says nothing about the others:

| Tool | What it checks | In Malan's words |
|---|---|---|
| `check50` | Correctness: does the code produce the right output for a specific problem set (identified by a "slug")? | "You'll get quick feedback on whether or not your code is correct. It doesn't mean it's well implemented or well designed or well stylized, but at least that's the first gauntlet." |
| `design50` | Design: subjective, TA-style feedback on how the code is structured | "Built on top of the CS50 duck... you will get ChatGPT-like advice on how you can improve not the correctness of that code, but the design of that code, the quality thereof." |
| `style50` | Style: formatting, indentation, naming, consistent with CS50's style guide | "It will show you on the left what your code looks like, and on the right what your code really should look like." |

> ✅ **What to do about it:** treat a passing `check50` as step one, not the finish line. Correct-but-ugly and correct-but-wasteful code both pass `check50` and still deserve a `design50` and `style50` pass before you call a problem done.

### The Mario grid: seeing bad design, then fixing it

Malan grounds "design" in a concrete example: printing a 3×3 grid of bricks, the kind Mario jumps into underground, using nested loops. The natural first attempt works, but has two design smells worth naming.

```c
for (int i = 0; i < 3; i++)
{
    for (int j = 0; j < 3; j++)
    {
        printf("#");
    }
    printf("\n");
}
```

**Smell one: unclear names.** `i` and `j` are conventional for loop counters, but only up to a point. Malan's rule of thumb: "it is pretty conventional in code when you want another integer, and it's not `i` because you've used it already, fine, you can use `j`. So using `i` and `j`, maybe `k`, is generally fine. If you're using `l`, `m`, and `o`, at that point you're probably doing something wrong." Renaming them to say what they mean costs nothing and helps every future reader:

```c
const int HEIGHT = 3;

for (int row = 0; row < HEIGHT; row++)
{
    for (int column = 0; column < HEIGHT; column++)
    {
        printf("#");
    }
    printf("\n");
}
```

**Smell two: the magic number, twice.** The original version types `3` in two separate places: the outer loop's condition and the inner loop's condition. It works, but Malan flags exactly why that's fragile: "if I want to make this square bigger and bigger and bigger over time, I'm going to have to change it in two different places, and... eventually that's going to come back and bite you. You're going to do something stupid, or a colleague isn't going to realize you hard-coded 3 in multiple places, just bad design."

The fix is a **constant**: a variable whose value you (and the compiler) promise never to change after it's set. In C, you signal that with the keyword `const`. Malan's own test of it: "if I do something stupid later in my code and I try to set `N` equal to something else, the compiler won't let me do that. It will protect me from myself, so it's just a slightly better design as well." One `const int HEIGHT = 3;` at the top, used in both loops, means the grid's size now lives in exactly one place.

## Part 3: The limits of numbers (overflow, truncation, and imprecision)

Every value in a computer's memory is stored using a fixed, finite number of **bits** (binary digits). An `int` conventionally gets 32 of them. That's not a minor implementation detail: it's the root cause of everything in this final part of the lesson. Malan connects it back to the simplest possible case: "we've seen this problem even on a small scale with our light bulbs... if I have a 3-digit number as represented by 3 physical light bulbs, I can count 0, 1, 2... up to 7. If I want to count to 8, I need a 4th bit. But if you don't have a 4th bit, for all intents and purposes, that number is just 0." Module 5 will show you exactly where those bits physically live inside a computer's memory; for now, just hold onto the consequence: **every number type has a ceiling, and computers hit it silently.**

### Integer overflow: the dollar-doubling meme

Malan reconstructs a familiar meme in C: start with one dollar, and on each round, ask whether to double it and pass it on.

```c
int dollars = 1;
while (true)
{
    char c = get_char("Here's $%i. Double it and give to next person? ", dollars);
    if (c == 'Y')
    {
        dollars *= 2;
    }
    else
    {
        break;
    }
}
```

Say yes enough times, and the dollar amount doesn't just get large: it suddenly goes negative, then drops to zero. That's **integer overflow**: trying to store a value bigger than the variable's bits can hold. As Malan narrates it live, after the number breaks: "the computer only has a finite number of bits allocated to each integer... it's roughly [4] billion... we overflowed the integer in memory. In fact, integer overflow is a term of art." Switching `int` to a 64-bit `long` buys you far more headroom, but as Malan demonstrates by continuing to double the amount, it's still finite, and eventually overflows too.

This is not just a classroom meme. In 2015, the *New York Times* reported a real Boeing 787 bug caused by exactly this: "a Model 787 airplane that has been powered continuously for 248 days can lose all alternating current electrical power due to the generator control unit simultaneously going into fail-safe mode. This condition is caused by a software counter internal to the GCUs that will overflow after 248 days of continuous power." A counter, almost certainly a 32-bit integer counting tenths of a second, ran out of room after 248 days airborne, and the plane's power shut off mid-flight. Asked what the short-term fix was before Boeing shipped a real patch, Malan gives the answer you already know from your own devices: "literally turn it off and back on again, much like you've probably been taught with your phones and computers... **Reboot the plane.**" Rebooting works because it resets every variable, including that overflowing counter, back to its starting value.

Overflow shows up in games, too: a well-known bug in the original *Pac-Man* let you play up to level 255, but "because there was a missing `if` condition that checked what level you were on, you could accidentally garble the screen if you were amazing at Pac-Man, because they too would overflow an integer, and just random characters would end up appearing on the screen." Reaching that level-256 "kill screen" became a badge of honor among top players precisely because it's an overflow bug you can only trigger by being extremely good.

> 🔑 **Integer overflow, truncation, and floating-point imprecision are three symptoms of the exact same root cause: a finite number of bits trying to represent an infinite range of numbers.** Which one you get depends only on what kind of value ran out of room.

### Truncation: when division throws away the remainder

Change the calculator to divide two whole numbers instead:

```c
int x = get_int("What's x? ");
int y = get_int("What's y? ");
printf("%i\n", x / y);
```

Try `1 / 3` and you get `0`, not `0.33`. Try `4 / 3` and you get `1`, not `1.33`. Nothing crashed. The answer is simply wrong, in a very specific way. This is **truncation**: "this other issue in computing when you have finite numbers of bits... whereby even when you're trying to do floating point math, like with a decimal point, if you are using an integer, you're going to throw away everything after the decimal point unless you're explicitly using the right data type." Switching both variables (and the placeholder) from `int`/`%i` to `float`/`%f` fixes it: `1 / 3` correctly becomes `0.333333`.

### Floating-point imprecision: the approximation you can't escape

Fixing truncation doesn't fully fix the deeper problem. Print that same `1.0 / 3.0` with enough digits (`printf("%.50f\n", x / y);`) and instead of an endless run of 3s, you get "all this random stuff happening at the end," garbage digits where you'd expect more 3s. The explanation is the same finite-bits story, one level more subtle: "computers only use finitely many bits to represent floating-point numbers, and if there's an infinite number of those, you can't possibly represent every possible floating-point value. So we're essentially seeing an approximation of one-third, precisely... That then is what we'd call floating-point imprecision." Upgrading from a 32-bit `float` to a 64-bit `double` buys more precision, the same way `long` bought more headroom for integers, but it never eliminates the approximation, only shrinks it.

### Y2K and the Year 2038 problem

Finite bits create the same trap at civilization scale. For decades, computers stored a year using two digits instead of four, "because it was convenient: it was more efficient because you use half as much memory." When 1999 rolled into 2000, any system still storing only two digits risked confusing `00` for 1900, not 2000, the so-called **Y2K problem**, patched worldwide (at enormous effort and expense) just in time.

A near-identical bug is already scheduled. Since the 1970s, most computers have tracked the current date and time as a 32-bit integer counting seconds since January 1, 1970. That counter has the same roughly-2-billion ceiling as any other 32-bit `int`, and "on the date January 19th, 2038, we will overflow a 32-bit counter, and... our computers and phones and other devices may very well think it's December 13, 1901", unless the systems still relying on 32-bit time are upgraded before then. It's the same bug you just triggered on purpose in your own calculator, at a scale that will eventually touch infrastructure you rely on every day.

---

## Key takeaways

1. **A function is a promise with three parts.** Its return type, its name, and its argument types all have to match between the prototype and the full definition.
2. **Prototypes exist so `main` can go first.** C reads top to bottom and won't look ahead; a prototype tells the compiler "trust me, this function exists further down."
3. **Scope is about curly braces, not file position.** A variable declared inside one function (or one loop) is invisible everywhere else, no matter how nearby that other code looks on the page.
4. **Correctness, design, and style are three separate report cards.** Code can be 100% correct and still badly designed or badly styled: CS50 checks each with a different tool (`check50`, `design50`, `style50`).
5. **A magic number typed in two places is a bug waiting to happen; a `const` typed once protects you from yourself.**
6. **Every number in a computer is finite, so it can overflow (too big), truncate (lost decimal), or blur (imprecise decimal): the fix is always "use a bigger or more appropriate type," never "the computer will just know."**

## Common pitfalls

- ❌ Defining a function below `main` with no prototype above it: you'll see `call to undeclared function`. Add the one-line prototype above `main`; don't move the whole function.
- ❌ Assuming a variable declared in `main` is visible inside another function just because both are in the same file: pass it in as an argument instead.
- ❌ Treating a passing `check50` as "the code is good." It only means the code is *correct* for that specific problem: run `design50` and `style50` too.
- ❌ Hardcoding the same size or limit in two or more places instead of one `const`: the moment you need to change it, one copy will get missed.
- ❌ Assuming `int` division gives you a decimal answer, or that `float` math is perfectly exact: the first truncates, the second is only ever an approximation.

---

## 🛠️ Capstone Project: Refactor Mario, Then Break a Number on Purpose

> This is the main hands-on project for the lesson. You'll take the exact
> kind of repetitive, hardcoded code the lecture starts with and turn it
> into properly designed C (functions, a prototype, a constant) and then,
> on purpose, make it fail in one of the three numeric ways you just learned
> to recognize.

### What you will build

On [cs50.dev](https://cs50.dev), a single program, `mario.c`, that starts life exactly like the lecture's version (two nested `for` loops hardcoding a 3×3 grid of `#` bricks) and evolves, milestone by milestone, into a small but genuinely well-designed program: a `void print_row(int width)` function with its own prototype, a `const int` controlling the grid's size, and a custom function that returns a validated height from the user. Below that grid code, you'll add a second, clearly separated block where you deliberately trigger integer overflow, truncation, or floating-point imprecision, with a comment explaining exactly why it happens.

### Why this is the perfect practice

| Lesson idea | Where you use it in the project |
|---|---|
| Custom function + prototype (Part 1) | `print_row` is pulled out of `main` and declared above it. |
| Scope (Part 1) | The row's width is passed in as an argument, not read from a variable defined elsewhere. |
| Return value (Part 1) | `get_height` loops until the input is valid, then `return`s it to `main`. |
| Constants (Part 2) | One `const int HEIGHT` replaces the number 3 typed twice. |
| `design50` / `style50` (Part 2) | A feedback pass on the finished `mario.c`. |
| Overflow / truncation / imprecision (Part 3) | A second, deliberate block of code that breaks a number on purpose, with an explanatory comment. |

### Milestones (build them in order, each one works on its own)

1. **Rebuild the grid, hardcoded.** In a new `mario.c`, write two nested `for` loops that print a 3×3 grid of `#` characters, exactly like the lecture's first version. Compile with `make mario` and confirm it runs before changing anything.
2. **Pull the row into its own function.** Write `void print_row(int width)` that prints one row of `width` `#` characters followed by a newline. Add its prototype above `main`, delete the inner loop from `main`, and call `print_row` from inside the outer loop instead.
3. **Replace both 3s with one constant.** Declare `const int HEIGHT = 3;` above `main` and use `HEIGHT` everywhere the size 3 currently appears. Confirm that editing that single line resizes the whole grid.
4. **Add a function that returns a value.** Write `int get_height(void)` that loops with `get_int` until the user enters a non-negative number, then `return`s it. Call it from `main` and use the result in place of (or alongside) `HEIGHT`.
5. **Break a number on purpose.** Below your grid code, clearly separated with a comment banner, reproduce one bug from Part 3: your choice of integer overflow (repeatedly double an `int` until it goes negative), truncation (divide two `int`s and print the result as if it were a decimal), or floating-point imprecision (print `1.0 / 3.0` to 20+ digits). Write a `//` comment, in your own words, explaining why it happens.
6. **Get outside feedback.** `mario.c` is a custom exercise, not an official CS50 problem set, so there's no `check50` slug to run against it: you verify correctness yourself, by eye. Instead, run `design50` and `style50` on the finished file and apply at least one suggestion from each.
7. **Stretch goals.** Extend `print_row` (or add a sibling function) into a full ascending pyramid, with a second nested loop printing leading spaces before each row's bricks. Or trigger two different number bugs side by side and compare their symptoms in your comments.

> 💡 **One line ahead:** the database-backed web app you'll build by the end of this course will be full of functions that look exactly like `print_row`: a name, typed arguments, and often a return value. The habit you're practicing on bricks today is the same habit a web app's route-handling functions use later.

### How you will know you are done

- ✅ `mario.c` compiles with `make mario` and prints its grid using a function you wrote, not copy-pasted `printf` calls.
- ✅ Your program has a prototype above `main` for every function defined below it, and a `const` controlling the grid's size.
- ✅ Changing the grid's size requires editing exactly one line.
- ✅ A second, clearly separated block of code deliberately overflows, truncates, or loses precision, with a comment explaining why in your own words.
- ✅ You've run `design50` and `style50` on the file and read their feedback, even if you don't apply all of it.

> 💡 **Keep yourself honest:** before you add the deliberate bug in Milestone
> 5, run the grid code once more and confirm it's still correct: you want
> to be certain the failure you demonstrate next is the one you intended,
> not a leftover mistake from refactoring.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: A function with an argument (foundational)
Write `void print_line(int length)` that prints `length` dash characters followed by a newline, with its prototype above `main`. Call it three times from `main` with three different lengths (for example, 5, 10, and 20) and confirm each line is the right size.

### Exercise 2: A function with a return value, and an overflow (intermediate)
Write `int square(int n)` that returns `n * n`, with a matching prototype. Use it in `main` to print the squares of 1 through 5. Then call `square(50000)` and print the result. It will not be 2,500,000,000: in a comment, explain why, using what you learned about a 32-bit `int`'s roughly 2-billion ceiling.

### Exercise 3: Truncation vs. a proper decimal (advanced)
Given a `score` of 7 and a `total` of 9, compute and print a percentage two different ways: once using only `int` math (`score * 100 / total`), and once by casting at least one value to `float` or `double` before dividing. Print both results and, in a comment, explain in your own words why they differ.

---

## Cheat sheet

```text
FUNCTION SHAPE
  return_type name(type argument);              <- prototype (above main)
  return_type name(type argument)                <- full definition (anywhere else)
  {
      ...
      return value;   // omit if return_type is void
  }

SCOPE RULE
  A variable declared between { and } only exists between that { and }.
  Need it somewhere else?  Pass it in as an argument, or return it out.

CODE QUALITY  (three separate report cards)
  correctness  -> does it work?           checked by check50  (needs a problem's slug)
  design       -> is it well built?       checked by design50 (subjective, TA-style)
  style        -> is it well formatted?   checked by style50  (formatting, naming)

CONST
  const int HEIGHT = 3;   // one source of truth; compiler blocks any later change

WHY NUMBERS BREAK  (root cause: finite bits, always)
  integer overflow          -> value too big for its type -> wraps to negative / 0
  truncation                -> int / int throws away the decimal part
  floating-point imprecision -> decimal value can't be stored exactly -> tiny error

REAL-WORLD OVERFLOW
  Boeing 787: 32-bit counter overflows after 248 days powered on  -> "reboot the plane"
  Pac-Man:    level counter overflows past 255                    -> kill screen at 256
  Y2K:        2-digit year overflows going from 99 to 00           -> 2000 read as 1900
  Year 2038:  32-bit seconds-since-1970 counter overflows          -> Jan 19, 2038
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 7 (Conditionals and loops):** the loops and conditionals you learned there are exactly what you now package inside your own functions: this lesson doesn't add new control flow, it adds a way to name and reuse the control flow you already have.
- **Next, Module 3 · Lesson 9 ("The art of debugging"):** every bug category you triggered on purpose here (scope errors, undeclared functions, overflow, truncation, imprecision) is exactly the kind of bug you'll learn to hunt down deliberately, instead of stumbling into by accident.
- **Later, Module 5 (Memory):** this lesson explained *that* every number type has a finite ceiling; Module 5 explains *where*, physically, in a computer's memory those bits actually live, and why that placement is what makes overflow and imprecision inevitable rather than a bug CS50 could simply have avoided.

---

*Source: "CS50x 2026 - Lecture 1 - C" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
