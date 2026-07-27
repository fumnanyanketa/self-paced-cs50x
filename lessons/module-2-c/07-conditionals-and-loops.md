# Module 2 · Lesson 7: Conditionals and Loops

> **Course:** Self-Paced CS50x
> **Module 2:** First real programs in C: write, compile, run, and fix real code in a terminal
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 1 - C](https://www.youtube.com/watch?v=SlqjA04_dpk) · [full transcript](../../transcripts/03-lecture-1-c.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

You can make a C program branch between different actions with `if`/`else if`/`else`, and repeat an action with `while`, `do while`, or `for`, as long as you store each value in a variable of the right data type.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a small guessing game that validates input, branches on the player's guess, and loops until they win. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Tools and languages change, but the shape of every program does not.
>
> - **[Böhm-Jacopini theorem](https://dl.acm.org/doi/10.1145/355592.365646)** ("Flow Diagrams, Turing Machines and Languages with Only Two Formation Rules," *Communications of the ACM*, 1966). This proof showed that *any* algorithm, no matter how complicated, can be built from just three ingredients: doing things in **sequence**, **selecting** between paths (what `if`/`else` does), and **repeating** a block (what loops do). Every program you will ever write, in any language, is some combination of those three. This lesson teaches you the second and third ingredients in C.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Conditional (branch):** an instruction that tells the computer "do this if some question is true, otherwise do that." It is a fork in the road.
- **Boolean expression:** a question whose only possible answers are true or false, like "is `x` less than `y`?"
- **Comparison operator:** a symbol like `<`, `>`, or `==` that compares two values and produces a true/false answer.
- **Logical operator:** a symbol like `||` (or) or `&&` (and) that combines two boolean expressions into one.
- **Data type:** the kind of value a variable holds: a whole number, a character, a true/false value, and so on. C makes you state the type up front.
- **Format specifier:** a placeholder like `%i` or `%c` inside a `printf` string that tells C what type of value to substitute in, and how to display it.
- **Loop:** an instruction that repeats a block of code again and again, either a fixed number of times or until some condition changes.
- **Scope:** the region of a program (marked by curly braces `{ }`) in which a variable exists and can be used. Outside that region, the variable is gone.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 6 got you capturing input and printing it back out, but every program so far has done exactly one thing, once, in a straight line. Real programs need to make decisions and repeat work: reject bad input, retry until the user cooperates, keep asking a game player to guess again. Malan frames the whole idea simply: **"conditionals were sort of the proverbial fork in the road, enabling you to do this or this or some other thing based on the answer to a question, a so-called boolean expression."** By the end of this lesson you can write that fork, and the loops that surround it, correctly and efficiently: the exact two skills every input-validating, decision-making program (including the web app you'll eventually build) depends on.

## Learning objectives

By the end of this lesson you will be able to:

1. Write an `if`/`else if`/`else` chain in C using the right comparison operators, ordering the branches so the computer never asks a question it doesn't need to.
2. Explain the difference between `=` (assignment) and `==` (equality), and avoid the classic bug of confusing them.
3. Declare variables with the right C data type (`bool`, `char`, `int`, `float`, `double`, `long`), read them with the matching CS50 `get_` function, and print them with the matching format specifier.
4. Compare single characters with single quotes and combine boolean expressions with `||` and `&&` to accept more than one valid answer.
5. Write `while`, `do while`, and `for` loops; deliberately write and stop an infinite loop; and use `break` and `continue` to control a loop from the inside.

## Prerequisites

- **Lesson 6 (Input, variables, and the command line):** you should already be comfortable typing commands in the cs50.dev terminal, compiling with `make`, and using `get_string` plus `%s` to capture and print text.
- No prior programming language experience is assumed.

---

## Part 1: Conditionals: the fork in the road

In Scratch, a conditional was an orange puzzle piece you snapped a boolean expression into. In C, the same idea has no puzzle piece, just the keyword `if`, parentheses, and curly braces:

```c
if (x < y)
{
    printf("x is less than y\n");
}
```

Malan describes the whole family of constructs this way: **"conditionals were sort of the proverbial fork in the road, enabling you to do this or this or some other thing based on the answer to a question, a so-called boolean expression."** The parentheses after `if` are *not* a function call: `if` is a built-in feature of C, and whatever boolean expression you put inside must evaluate to true or false.

To handle more than two outcomes, chain `else if` and finish with a plain `else`:

```c
if (x < y)
{
    printf("x is less than y\n");
}
else if (x > y)
{
    printf("x is greater than y\n");
}
else
{
    printf("x is equal to y\n");
}
```

> 🔑 **An `if` asks a yes/no question and runs one block of code depending on the answer; chain `else if` for more questions, and end with `else` as the catch-all.**

### One equals sign or two?

The first time you write a condition, it is tempting to write `if (x = y)`. That's a bug, and a famous one. A single `=` is the **assignment operator**: it copies the value on the right into the variable on the left, exactly like it does in `answer = get_string(...)`. Malan explains where the double-equals convention came from: **"The solution in C as well as in many other languages is literally this they use 2. So this is the equality operator, whereas a single one is the assignment operator."** So `==` asks "are these equal?" while `=` says "make this equal." Scratch avoided the confusion entirely by using a single `=` for both, since it didn't want to confuse beginners. C, like most text-based languages, needs the two symbols kept distinct.

Here is the full comparison operator table:

| Operator | Meaning |
|---|---|
| `<` | less than |
| `>` | greater than |
| `<=` | less than or equal to |
| `>=` | greater than or equal to |
| `==` | equal to (a comparison, never an assignment) |
| `!=` | not equal to ("bang equals") |

### Ordering branches so you don't waste time

Malan's first working version of a number-comparison program asked three separate questions (is `x < y`, is `x > y`, is `x == y`) even though, once you know the first two answers, the third is a foregone conclusion. He calls this out directly: **"Even if X ends up being less than Y from the get-go, you're still wasting everyone's time by saying, well, is X greater than Y? You already might know that it's not."** The fix is to chain the checks with `else if` instead of writing three independent `if` statements, so that once one branch matches, C skips the rest automatically:

```c
if (x < y)
{
    printf("x is less than y\n");
}
else if (x > y)
{
    printf("x is greater than y\n");
}
else
{
    printf("x is equal to y\n");
}
```

Three independent `if` statements are each checked no matter what happened before, even after the true answer is already known. An `if`/`else if`/`else` chain is mutually exclusive by design: as soon as one branch matches, C skips straight past the rest.

> ✅ **What to do about it:** when your branches are mutually exclusive (only one can ever be true), chain them with `else if`/`else` rather than writing separate `if` statements: it is both more correct-feeling and faster.

---

## Part 2: Data types and the CS50 `get_` functions

C forces you to say up front what *kind* of value a variable will hold, unlike Scratch, where a variable could hold anything. Here are the types you'll use constantly:

| Type | Holds | CS50 input function | `printf` placeholder |
|---|---|---|---|
| `bool` | true or false | *(no `get_bool`, rarely useful to prompt for)* | -- |
| `char` | a single character | `get_char` | `%c` |
| `int` | a whole number (about ±2 billion) | `get_int` | `%i` |
| `float` | a number with a decimal point (32 bits) | `get_float` | `%f` |
| `double` | a number with a decimal point, more precisely (64 bits) | -- | `%f` |
| `long` | a whole number with a bigger range (64 bits) | -- | `%li` |

On why `float` needs so many bits and still isn't perfect, Malan explains: **"A float is otherwise known as a floating point value, which is just a number that has a decimal point in it, a real number if you will, but a float generally uses nowadays 32 bits total to represent those numbers."** A `double` simply doubles that budget to 64 bits for more precision: the same underlying idea, just roomier. (Lesson 8 digs into what happens when even that room runs out: integer overflow and floating-point rounding. For now, just know the type names and when to reach for the bigger one.)

Every `get_` function works the same way you already know from `get_string`: it prompts the user, waits, and hands back a value of the matching type, which you store with `=` into a variable you've declared with that type:

```c
int x = get_int("What's x? ");
```

Format specifiers are the other half of the puzzle: they tell `printf` how to display a value you hand it. As Malan puts it: **"if you want to print out something like a char [...] you're actually going to use percent C. If you want to print out a floating point value, you're going to use percent F, an integer percent I, and a long integer that is a long, you're going to use LI instead."** Get the specifier wrong (say, `%i` for a `float`) and `printf` will print garbage: the type of the placeholder must match the type of the variable.

> 🔑 **Every variable has exactly one type; that type decides which `get_` function fills it and which `%` placeholder prints it.**

---

## Part 3: Comparing characters and combining conditions

A `char` holds exactly one character: not a word, not a sentence, just one letter, digit, or symbol. To get one from the user and check it, CS50's `agree.c` pattern looks like this:

```c
char c = get_char("Do you agree? ");

if (c == 'y')
{
    printf("Agreed.\n");
}
else if (c == 'n')
{
    printf("Not agreed.\n");
}
```

Notice the single quotes around `'y'` and `'n'`. That's not optional styling: it's how C tells a lone character apart from a string. Malan draws the line clearly: **"When you want to compare a single character, you use chars and you use single quotes. When you want to use strings of text like multiple characters, multiple words, multiple sentences or paragraphs, you use strings."** Double quotes (`"y"`) would make a string of one character, which is a different type than `char` and would not compare correctly with `==`.

The `agree.c` example above has a real gap, though: typing an uppercase `Y` doesn't match `'y'`, so a perfectly reasonable answer gets treated as disagreement. You could add a second, nearly-identical `else if` for `'Y'`, but that repeats yourself: the same message twice, so a future wording change means editing it in two places. The better fix is a **logical operator**, which combines two boolean expressions into one:

```c
if (c == 'y' || c == 'Y')
{
    printf("Agreed.\n");
}
```

On what that symbol means, Malan says: **"the two vertical bars, which is probably not a character you type that often [...] just means logical or."** `||` asks "is at least one of these true?", so this line reads "the character equals lowercase y, or the character equals uppercase Y." The other logical operator, `&&` ("and"), requires *both* sides to be true, which would be the wrong choice here, since a single character obviously cannot simultaneously equal `'y'` and `'Y'` at the same time.

> ✅ **What to do about it:** when more than one input should count as a match, reach for `||` instead of copy-pasting a near-identical branch for each accepted value.

---

## Part 4: Loops: while, do while, for, and controlling them from the inside

A loop repeats a block of code. Malan's plain definition: **"a loop is just something that does something again and again and again."** Scratch's "repeat" block doesn't exist by that name in C. The closest match is a `while` loop, built from a boolean expression that stays true until it doesn't:

```c
int i = 3;
while (i > 0)
{
    printf("meow\n");
    i--;
}
```

This counts *down* from 3 to 1, printing `meow` each time, and stops the instant `i > 0` becomes false. You can just as easily count *up*, which is the more conventional style in C, start at 0, and loop while the counter is *less than* the value you care about:

```c
int i = 0;
while (i < 3)
{
    printf("meow\n");
    i++;
}
```

Because "loop a known number of times" is so common, C offers a `for` loop that packs the setup, the condition, and the increment into a single line:

```c
for (int i = 0; i < 3; i++)
{
    printf("meow\n");
}
```

Read it left to right: initialize `i` to 0, check `i < 3` before every pass, and run `i++` automatically after every pass. It behaves identically to the `while` version above, just fewer lines to write.

### Infinite loops, and how to stop one

Sometimes you want something to repeat forever, until you say otherwise. There's no dedicated "forever" keyword, so the convention is `while (true)`:

```c
while (true)
{
    printf("meow\n");
}
```

Malan ran exactly this in class and let it run through a break, printing `meow` nonstop, until VS Code itself warned about runaway CPU use. The escape hatch is a keyboard shortcut, not a code fix: **"Control C would have been our friend."** `Ctrl+C` interrupts whatever is currently running in the terminal: good to know before you accidentally write your own infinite loop.

### Validating input with `break` and `continue`

An infinite loop becomes genuinely useful once you can exit it on your own terms. Suppose you want to keep asking for a number until the user gives you a non-negative one:

```c
int n;
while (true)
{
    n = get_int("What's n? ");
    if (n < 0)
    {
        continue;
    }
    else
    {
        break;
    }
}
```

`continue` and `break` are two different ways of interrupting a loop from inside: **"So continue essentially brings you to the top, brake [break] brings you to the bottom if you will."** `continue` jumps back up to re-check the loop's condition (try again); `break` jumps out past the loop's closing curly brace entirely (stop looping). Since asking to loop again is already the default behavior, the `continue` here is optional: the same logic reads more cleanly as just `if (n >= 0) { break; }`.

Notice `int n;` is declared *above* the loop, with no value yet, rather than inside it. That's deliberate, and it's the first time this lesson touches **scope**: a variable declared inside a pair of curly braces only exists inside that same pair of braces. Malan hits this directly while debugging exactly this mistake: **"This is a problem of what's known as scope [...] and only exists inside of the scope of the while loop in which it was declared."** Declare `n` inside the loop's braces, and it vanishes the moment the loop's block ends, so if you need the value afterward, declare it one level up first.

### `do while`: check the condition at the bottom, not the top

A `while (true)` loop with a manual `break` works, but C offers a construct built for exactly this "do it, then decide whether to repeat" shape: `do while`.

```c
int n;
do
{
    n = get_int("What's n? ");
}
while (n < 0);
```

The difference from a plain `while` loop is simply *when* the condition is checked: at the bottom instead of the top, meaning the body always runs at least once before anything is questioned. Malan illustrates the distinction with a cartoon pairing: **"the difference between do while loop, like the roadrunner, is stopping because he's checking the condition while not on edge, he'll run, but if he is on the edge, he's not going to proceed further. But of course the coyote here, he's going to do running no matter what and then only too late does he check."** A `do while` loop is the coyote: it runs first and checks after. A plain `while` loop is the roadrunner: it checks first and only runs if the check passes. Use `do while` whenever you know you want to do something at least once: asking the user a question is the classic case.

> 🔑 **`while` checks before it runs; `do while` runs once before it checks: pick `do while` whenever the first attempt should happen unconditionally.**

---

## Part 5: Putting branches and loops together

The whole point of this lesson is that conditionals and loops are not separate tools. They combine. A validation loop is a loop wrapped around a conditional; a game loop is a loop wrapped around several conditionals in a row. In text form:

```text
do
{
    guess = get_int("Guess: ");     <- loop body (repeats)

    if (guess < secret)             <- conditional (branches)
    {
        printf("Too low!\n");
    }
    else if (guess > secret)
    {
        printf("Too high!\n");
    }
    else
    {
        printf("Correct!\n");
    }
}
while (guess != secret);            <- loop's exit condition
```

The `do while` guarantees the player gets at least one guess before anything is checked; the `if`/`else if`/`else` chain inside decides what to tell them; and the loop's own condition (checked at the bottom) decides whether to ask again. This exact shape is what you'll build in the Capstone below.

---

## Key takeaways

1. **`if`/`else if`/`else` is a fork in the road.** Chain mutually-exclusive branches with `else if` so C never checks a question whose answer is already implied.
2. **`=` assigns, `==` compares.** Confusing them is one of the most common early C bugs: `if (x = y)` silently assigns instead of asking a question.
3. **Every variable has a type, and the type decides everything downstream.** Pick the right `get_` function to read it and the right `%` placeholder to print it: `bool`, `char`/`get_char`/`%c`, `int`/`get_int`/`%i`, `float`/`get_float`/`%f`, `double`/`%f`, `long`/`%li`.
4. **Single characters use single quotes; strings use double quotes.** `c == 'y'` compares a char; `c == "y"` does not mean what you think it means.
5. **`||` accepts either side; `&&` requires both.** Use `||` to accept more than one valid answer for the same input.
6. **`while` checks first, `do while` checks last, `for` packs a counting loop onto one line.** `break` exits a loop immediately; `continue` jumps back to re-check the condition.
7. **A variable only exists inside the curly braces it was declared in (its scope).** Declare it one level higher if you need it to outlive a loop.

## Common pitfalls

- ❌ Writing `if (x = 5)` when you meant `if (x == 5)`: this assigns 5 to `x` (and is usually treated as true), it does not compare anything.
- ❌ Writing three independent `if` statements for mutually exclusive cases instead of chaining them with `else if`: every one gets checked even after the answer is already known.
- ❌ Comparing a `char` against a string, like `c == "y"` instead of `c == 'y'`: double quotes and single quotes are different types in C.
- ❌ Reaching for `&&` when you mean `||` (or vice versa): ask yourself whether *both* conditions must hold, or whether *either* one is enough.
- ❌ Writing `while (true)` without a `break` anywhere inside it: you now have a real infinite loop; remember `Ctrl+C` if you get stuck.
- ❌ Declaring a variable inside a loop's curly braces and then trying to use it after the loop ends: it's out of scope. Declare it above the loop instead.

---

## 🛠️ Capstone Project: Guess My Number

> This is the main hands-on project for the lesson. You'll build a small, complete C program on cs50.dev that validates input with a loop, branches on the player's guess, and loops the whole game until they win: proving you can combine every idea from this lesson into one working thing. Validation loops and branching logic like this run every form your app will ever process, right up through the database-backed web app you build at the end of this course.

### What you will build

A command-line guessing game, `guess.c`, where the computer picks a secret number and the player guesses until they get it right, with the program telling them "too high" or "too low" after each guess.

- A `do while` loop that rejects out-of-range input (Part 4).
- An `if`/`else if`/`else` chain, ordered efficiently, that compares the guess to the secret number (Part 1).
- A loop that repeats the guess-and-check cycle until the player wins, using `break` to stop (Part 4).
- A `char`-based "play again?" prompt using `||` to accept `'y'` or `'Y'` (Part 3).

### Why this is the perfect practice

| Lesson idea | Where you use it in Guess My Number |
|---|---|
| `if`/`else if`/`else`, ordered efficiently | Comparing the guess to the secret number |
| `==` vs `=` | Checking `guess == secret` to end the loop |
| Data types & `get_int`/`get_char` | Reading the guess (`int`) and the replay answer (`char`) |
| `||` / `&&` | Accepting `'y'` or `'Y'` for "play again?" |
| `do while` | Forcing at least one valid guess before checking it |
| `while` / `for` + `break` | Repeating guesses until correct, and counting attempts |
| Scope | Declaring the attempt counter above the loop so you can print it after |

### Milestones (build them in order, each one works on its own)

1. **Validate a range with `do while`.** In a new `guess.c`, hardcode `int secret = 42;`. Write a `do while` loop that uses `get_int` to ask "Guess a number between 1 and 100: " and rejects (loops again on) anything outside 1-100.
2. **Branch on the guess.** Inside the loop, add an `if`/`else if`/`else` chain that prints `"Too low!\n"`, `"Too high!\n"`, or `"Correct!\n"` by comparing the guess to `secret`. Order the checks so the correct case needs no extra question.
3. **Loop until correct, and count attempts.** Wrap the guessing in a `while` (or `for`) loop with a counter (`int tries = 0;`, declared *above* the loop). Increment it each pass, `break` out the moment the guess is correct, and print the number of tries it took.
4. **Ask "play again?" with `get_char` and `||`.** After a win, use `get_char` to ask `"Play again? (y/n) "`. If the answer is `'y'` or `'Y'`, loop the whole game again from the top (wrap steps 1-3 in an outer `while (true)` that `break`s on `'n'`/`'N'`); otherwise, print a goodbye message and end.
5. **Stretch goals.** Add a difficulty menu at the start (`'e'`/`'m'`/`'h'` via `get_char` and an `if`/`else if` chain) that changes the guessing range to 1-10, 1-100, or 1-1000. Or track and print the player's total wins across replays using a counter declared outside the outer loop.

### How you will know you are done

- ✅ Entering a number outside 1-100 (or letters, which `get_int` itself rejects) re-prompts you instead of crashing or misbehaving.
- ✅ The program correctly tells you "too low" or "too high" and eventually "correct" no matter which number you guess.
- ✅ Typing `y`, `Y`, `n`, or `N` at the "play again?" prompt all behave correctly; nothing else does.
- ✅ `make guess` compiles with no errors or warnings, and you can play multiple full rounds without restarting the program.

> 💡 **Keep yourself honest:** if you find yourself writing the same `if`/`else if` block twice for uppercase and lowercase versions of an answer, that's your cue to reach for `||` instead.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Two-number comparator (foundational)
Write a program that uses `get_float` twice to read two numbers and prints which one is smaller, using `%f` and an efficiently-ordered `if`/`else if`/`else` chain (don't ask a third question once the first two have ruled it out).

### Exercise 2: Temperature classifier (intermediate)
Write a program that uses `get_int` to read a Fahrenheit temperature and prints `"Freezing"`, `"Cold"`, `"Mild"`, or `"Hot"` using an `if`/`else if`/`else` chain. Pick your own cutoffs, but order the checks so the most likely case is cheap to reach.

### Exercise 3: Star grid with an early stop (advanced)
Using only nested `for` loops (no functions yet, that's next lesson), print an `n`-by-`n` grid of `*` characters, where `n` is read with `get_int`. Then add a `break` so that if a special row index (say, row 2) is reached, the grid stops printing early: practice tracing exactly which loop your `break` exits.

---

## Cheat sheet

```text
CONDITIONALS
  if (bool_expr)      { ... }               one branch
  if (...) else       { ... }               two branches
  if (...) else if (...) else { ... }       chain: order for efficiency
  ==  equals (compare)     =  assigns (never compare with this!)
  <  >  <=  >=  ==  !=      comparison operators
  ||  "or" (either true)    &&  "and" (both must be true)

DATA TYPES              get_ FUNCTION      printf PLACEHOLDER
  bool                     --                  --
  char                     get_char            %c
  int                      get_int             %i
  float                    get_float           %f
  double                   --                  %f
  long                     --                  %li
  char literals use single quotes: 'y'   strings use double quotes: "y"

LOOPS
  while (cond)     { ... }             checks BEFORE running
  do { ... } while (cond);             checks AFTER running (runs >= once)
  for (init; cond; update) { ... }     counting loop, one line of setup
  while (true) { ... }                 infinite -- needs a break inside
  break     -> exit the loop now
  continue  -> skip to the next check of the condition
  Ctrl+C    -> kill a runaway program from the terminal
  Scope: a variable declared inside { } only exists inside those { }
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 6:** you learned to capture input with `get_string`, store it in a variable, and print it with `%s` and `printf` placeholders. This lesson reused that exact pattern for `get_int`, `get_char`, and `get_float`, and added the decision-making and repetition that turn a one-shot script into an interactive program.
- **Next, Module 2 · Lesson 8 "Functions, code quality, and the limits of numbers":** you'll notice the guessing loop's body has repeated bits: that's exactly what functions exist to eliminate. Lesson 8 also finally explains what happens when the `int` and `float` types you used here get pushed past their limits (overflow and imprecision).
- **Later, Module 4:** the `while` and `for` loops you wrote today become the object of study themselves: you'll learn to measure how many times a loop like this runs as its input grows (Big O), turning "does it work" into "how well does it scale."

---

*Source: "CS50x 2026 - Lecture 1 - C" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
