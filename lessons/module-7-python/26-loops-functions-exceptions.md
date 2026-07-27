# Module 7 · Lesson 26: Loops, Functions, and Exceptions

> **Course:** Self-Paced CS50x
> **Module 7:** Python: the same ideas, ten times less code
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 6 - Python](https://www.youtube.com/watch?v=Rl0ludWTLxs) · [full transcript](../../transcripts/08-lecture-6-python.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

This lesson rewrites C's loops and functions in Python's own words (`while`, `for`, and `range()` instead of three-part `for` loops, `def` instead of prototypes, and a `main()` you call yourself instead of one the language calls for you), and then shows you Python's cleaner way to survive bad input: catching an exception with `try`/`except` instead of endlessly checking return values.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you rebuild Module 2's Mario brick pyramid in Python, this time with a `get_height()` function that cannot be broken no matter what the user types. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** `try`/`except` is Python's particular syntax, but the underlying idea (let code signal "something went wrong" as its own distinct event, instead of overloading a function's normal return value to mean both "the answer" and "an error") is much older than Python.
>
> - **[John B. Goodenough, "Exception Handling: Issues and a Proposed Notation"](https://dl.acm.org/doi/10.1145/361227.361230)** (*Communications of the ACM*, 1975). One of the earliest papers to formally argue that a language should let a program raise and catch error conditions separately from its ordinary return values. Python's `try`/`except`, Java's `try`/`catch`, and C++'s exceptions are all descendants of the idea this paper first laid out.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Loop:** an instruction that repeats a block of code again and again, either a fixed number of times or until some condition changes.
- **`range()`:** a built-in Python function that produces a sequence of numbers to loop over, like "0, 1, 2". You almost always see it paired with a `for` loop.
- **Function (`def`):** a named, reusable block of code you write yourself. In Python you create one with the keyword `def`, short for "define."
- **`NameError`:** the error Python raises when your code tries to use a name (a variable or function) that does not exist yet, usually because it is used before it is defined.
- **Entry point:** the part of a program that runs first when the file is executed directly. In Python, the convention is a function called `main()`, protected by the line `if __name__ == "__main__":`.
- **Exception:** a way a program can signal, in the middle of running, that something has gone wrong, separately from whatever value a function would normally return.
- **`ValueError`:** the specific exception Python raises when a value is the right type but the wrong content, such as trying to convert the text `"cat"` into an integer.
- **Integer overflow:** what happens when a whole number grows too large for the fixed number of bits set aside to store it (you met this in Module 2 · Lesson 8), so it silently wraps around to a small or negative number instead of an error.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

You already know what a loop and a function are. You wrote both in Module 2, wrapped in `do while` tricks and function prototypes the compiler demanded. Python keeps the underlying ideas completely intact but strips away nearly all of the ceremony: no prototypes, no curly braces, no manually declared return types, and, as you're about to see, one entire category of C bug that simply cannot happen to you anymore. Malan sums up the whole reason exceptions exist this way: **"an exception in Python is a way of handling error conditions without relying on return values alone."** By the end of this lesson you will have written a single function, `get_height()`, that can survive absolutely any garbage a user throws at it, the same defensive habit every input-handling function in the web app you build at the end of this course will need.

## Learning objectives

By the end of this lesson you will be able to:

1. Write `while` and `for` loops in Python using `range()`, and use the underscore (`_`) convention for a loop variable you are required to name but never actually use.
2. Define your own function with `def`, diagnose a `NameError` caused by calling a function before it is defined, and structure a Python file with a `main()` function that you call yourself, guarded by `if __name__ == "__main__":`.
3. Explain which of C's numeric problems persist in Python (floating-point imprecision) and which are solved natively by the language (integer overflow, and the truncation that came from integer division).
4. Handle invalid input with `try`/`except` and `ValueError`, and contrast this with the return-value-only error checking C forced on you.

## Prerequisites

- **Module 7 · Lesson 25 (Python essentials):** `print()`, `input()`, F-strings, Python's lack of semicolons and curly braces, and the fact that Python infers a variable's type instead of you declaring it.
- **Module 2 · Lesson 7 (Conditionals and loops):** `if`/`else if`/`else`, `while`, `do while`, and `for` loops in C: this lesson translates all of them into Python.
- **Module 2 · Lesson 8 (Functions, code quality, and the limits of numbers):** custom functions, prototypes, scope, and the three numeric failure modes (integer overflow, truncation, floating-point imprecision): this lesson revisits every one of them.

---

## Part 1: Loops, translated (`while`, `for`, `range()`, and the underscore)

A `while` loop in Python looks almost exactly like the C version you already know, just with the type declaration, the semicolons, and the parentheses removed. To make a cat meow three times:

```python
i = 0
while i < 3:
    print("meow")
    i += 1
```

That works, and it is a perfectly reasonable translation of the C version from Lesson 7. But Python's `for` loop is genuinely different from C's, not just shorter. Malan draws the contrast directly: **"in [for] loops and Python, you don't have the parentheses, you don't have the two semicolons, you don't have the initialization and the Boolean expression and the update. You just say a little more English like for each i in the following list or for each value of I in the following list."** Concretely, that first version can be rewritten as:

```python
for i in [0, 1, 2]:
    print("meow")
```

Typing out a list of numbers gets tedious fast, so Python gives you a built-in function for exactly this job. As Malan explains, **"range is not only a data type in Python but more literally a function that you can call to get a range of values from zero on up."** So the idiomatic version is:

```python
for i in range(3):
    print("meow")
```

`range(3)` produces the numbers 0, 1, and 2, one at a time, and it does so lazily, handing them back one at a time instead of building the whole list in memory up front, so `range(3_000_000)` costs you no more memory than `range(3)`.

> 🔑 **`for x in range(n):` is Python's replacement for C's three-part `for (int i = 0; i < n; i++)`: same repetition, far less syntax.**

### The underscore convention

Notice that in the loop above, `i` is never actually used inside the loop body: the loop exists purely to repeat "print meow" three times. Python has a convention for exactly this situation: name the loop variable `_` instead. As Malan puts it, **"an underscore is a valid symbol for a variable name in Python, so it is Pythonic to just use this just to signal to yourself later and to colleagues that, yeah, I'm using a variable because I have to, but it's not one I'm actually going to use elsewhere."**

```python
for _ in range(3):
    print("meow")
```

Nothing about this changes how the code runs: it is purely a signal to any future reader (including you) that the loop's counter is irrelevant this time.

### What happened to `do while`?

Lesson 7 taught you `do while` for the specific case of "run this at least once, then decide whether to run it again", the classic shape of a validation prompt. Python has no `do while` keyword at all. Malan states this plainly: **"Python does not offer a do while loop."** The Pythonic replacement is a deliberate infinite loop, `while True:`, with a `break` inside it the moment the input is acceptable:

```python
while True:
    n = int(input("Height: "))
    if n > 0:
        break
```

This runs the body at least once, exactly like a `do while` would, and keeps looping until the `break` fires. You will use this exact pattern, together with the exception handling from Part 4, to build `get_height()` for this lesson's Capstone.

> 💡 **A subtlety worth knowing:** Python is noticeably looser about scope here than C was. Assigning `n` for the first time *inside* the `while True:` block still lets you use `n` after the loop ends, without declaring it above the loop first the way Lesson 8 required in C. As Malan notes, **"the issue of scope that we encountered in C is not as rigorously enforced"** in Python.

---

## Part 2: Custom functions (`def`, `NameError`, and the `main()` convention)

Defining your own function in Python drops nearly everything C required: no return type, no argument types, and the keyword is simply `def` ("define") instead of writing out a type signature. Here is the simplest possible version, deliberately written the way a beginner first tries it, with `main` calling a function that is defined *below* it:

```python
def main():
    meow()

def meow():
    print("meow")

main()
```

If you instead try to call `meow()` before its `def` appears anywhere in the file at all, Python refuses to run. Malan reads the resulting error aloud: **"The name meow is not defined."** This is a `NameError`, and unlike a C compiler error, it only happens when that specific line actually runs: Python reads and executes top to bottom, and as Malan explains, it will not look ahead to check whether you defined the function somewhere further down: **"meow doesn't exist until line 4. So if you try to use it on line 2 too soon."**

C solved this ordering problem with a *prototype* (Lesson 8) placed above `main`. Python has no equivalent syntax. Instead, the fix is simply to define every function before the point in the file where you first call it. That is exactly why the working version above defines `meow()` before calling it, and it is why the Pythonic convention is to put your own program's logic inside a function named `main`, defined near the top, with every helper function it calls defined above that point in the file. As Malan puts it, **"the Pythonic way to solve this problem, for better or for worse is to actually put your code in a main function."**

### Python will not call `main()` for you

There is a catch that trips up almost everyone the first time: unlike C, Java, or C++, Python attaches no special meaning to a function just because you happened to name it `main`. **"Python has no such special magic."** If you define `main()` but never call it, your program will run and do nothing at all. You have to call `main()` yourself, typically as the very last line of the file, *after* every function it depends on has already been defined.

### The `__name__` guard

Nearly every piece of real-world Python code you will encounter takes this one step further, wrapping the call to `main()` in a conditional:

```python
def main():
    meow(3)

def meow(n):
    for _ in range(n):
        print("meow")

if __name__ == "__main__":
    main()
```

The syntax is admittedly strange the first time you see it, and Malan doesn't pretend otherwise. What it buys you is real: **"This convention of using a conditional before you call main allows you to write more modular code in Python so that some of your files don't actually do anything other than define, define, defined functions that you can then import into other files you write."** In plain terms: this guard means "only run `main()` if someone executed *this* file directly, not if someone else imported it to reuse one of its functions." You will not need that flexibility for most of this course's exercises, but it is standard enough that you should recognize it and use it from here on, exactly as shown above.

Notice, too, that `meow(n)` now takes an argument. Just like in C, you give a Python function an input by naming it inside the parentheses, but with no type to declare:

```python
def meow(n):
    for _ in range(n):
        print("meow")
```

> ✅ **What to do about it:** structure every Python file you write from now on the same way: helper functions first, `def main():` next, and `if __name__ == "__main__": main()` as the very last lines.

---

## Part 3: Numeric issues revisited (one solved, one still with us)

Module 2 · Lesson 8 introduced three numeric failure modes in C, all traced back to one root cause: computers store numbers in a finite number of bits. Python inherits that same finite hardware, but the language hides some of the consequences and not others.

**Truncation is gone by default.** In C, dividing two `int`s with `/` silently discarded everything after the decimal point. In Python, dividing two integers with `/` gives you back a proper decimal answer automatically. Malan explains: **"in Python, even when you're manipulating integers, if you divide one by the other and the result logically should actually be a floating point value, that's what in fact you're going to get back and you don't have to jump through the same hoops that we did before to actually force things to float."** The old truncating behavior still exists if you deliberately ask for it, using `//` instead of `/`:

```python
print(1 / 3)     # 0.3333333333333333 -- true division, the default
print(1 // 3)    # 0 -- old-style integer division, only if you ask for it
```

**Integer overflow is solved natively.** The dollar-doubling bug from Lesson 8, where an `int` silently wrapped around to a negative number, cannot happen in Python: integers simply grow as large as your computer's memory allows. Malan calls this out directly: **"Python wonderfully nowadays just gives you more and more bits as needed if your integers are getting larger and larger, so this is a wonderful feature and ... we've at least addressed one fundamental limitation we ran into in C and this time the language itself provides us a solution."**

```python
x = 2 ** 100
print(x)   # 1267650600228229401496703205376 -- no overflow, no wraparound
```

**Floating-point imprecision is not solved.** This is the one C problem Python cannot make disappear, because the underlying hardware has not changed. Malan is direct about why: **"it's still the case that these computers only have a finite amount of memory. And so even though I'm manipulating clearly floating point values, Python is only allocating, say, 64 bits to those float variables, and so there's only so much precision that's possible."**

```python
z = 1 / 3
print(f"{z:.50f}")
# 0.33333333333333331482961625624739099293947219848633
# still just an approximation -- the extra digits are noise, not more 3s
```

| C problem (Lesson 8) | Still a problem in Python? |
|---|---|
| Truncation (`int / int` drops the decimal) | No: `/` does true division by default; `//` recovers the old behavior on purpose |
| Integer overflow (wraps to negative/zero) | No: Python integers grow as needed, with no fixed ceiling |
| Floating-point imprecision (approximated decimals) | Yes: still finite bits under the hood; unavoidable in any language |

> 🔑 **Python fixed the two numeric bugs that came from *choosing the wrong tool* (using `int` where you needed a decimal, or running out of bits for a whole number), but it cannot fix the one bug that comes from decimal numbers themselves being infinite and computer memory not being.**

---

## Part 4: Exceptions (`try`/`except`, `ValueError`, and a cleaner way to fail)

In C, a function had exactly one channel back to the caller: its return value. If something went wrong, the function had to sacrifice one otherwise-legitimate value (`NULL`, `-1`, `0`) to mean "error," and the caller had to remember to check for it every single time. Malan names the problem directly: **"return values were the only way in C that functions could communicate back to the programmer that something went wrong."** He continues with why that is genuinely limiting: if a function is "supposed to return maybe an integer, whether positive, negative, or zero... it's kind of unfortunate sometimes if you have to steal one of those values and say you can't use this value."

Python offers a different channel entirely: **exceptions**. As Malan defines it, **"an exception in Python is a way of handling error conditions without relying on return values alone."**

### Seeing the problem first

Suppose you ask the user for input and immediately try to convert it to an integer:

```python
n = int(input("What's n? "))
```

Type a real number and this works fine. Type `cat`, and Python crashes with a new kind of error. Malan narrates it live: **"Now I'm getting a value error, which is a different type of error"**. Specifically, Python cannot interpret the text `"cat"` as a whole number at all. This is a `ValueError`: the value's *type* (a string) is fine, but its *content* is not what `int()` needs.

One fix, before reaching for exceptions at all, is to check the string yourself first. Python's strings come with a built-in method for exactly this, alongside the string methods you may already have used, like `.lower()` and `.capitalize()`. As Malan describes it, strings **"come with not just an upper function, a lower function, aka methods, but also ... a method that tells you whether or not the string itself happens to be numeric"** (`.isnumeric()`):

```python
n = input("What's n? ")
if n.isnumeric():
    n = int(n)
    print("That's an integer")
else:
    print("That's not an integer")
```

This works, but it means checking a condition *before* every risky operation, the same defensive-checking burden C put on you, just moved from return values to string methods.

### Catching the error instead

The alternative is to let the risky code run, and tell Python what to do only if it fails. This is exactly what `try`/`except` is for. Malan's own plain-English description of the mechanism is the clearest one available: **"Try to execute these lines of code except if there's an error, then do this other thing instead"**, and, he adds, "therefore you don't have to check any return values."

```python
try:
    n = int(input("What's n? "))
    print("That's an integer")
except ValueError:
    print("Not an integer")
```

Type `cat` here, and the `int(...)` call raises a `ValueError` mid-way through the `try` block. Python immediately abandons the rest of that block (the `print("That's an integer")` line never runs) and jumps straight to the matching `except ValueError:` clause instead.

You do have to name the specific exception you expect, which raises a fair question Malan addresses directly: do you need to anticipate every possible way code can fail? **"In this case, I used a value error. Do I need to define every possible thing that can go wrong? Short answer yes."** There is no catch-all you should reach for reflexively: you name the exceptions you actually expect (`ValueError` for bad conversions, and others you will meet later, like `FileNotFoundError`), and add more `except` clauses as you discover new ways your own code can fail in practice.

> ✅ **What to do about it:** wherever C forced you to check a return value defensively before trusting it, wrap the risky Python code in `try:` and name the specific exception you expect in `except:`. Don't check first and hope; try, and handle failure only if it happens.

---

## Part 5: Putting it together (a function that cannot be broken)

The whole point of combining `def`, the `main()`/`__name__` convention, `while True` with `break`, and `try`/`except` is that they stack into one small, extremely durable pattern: a function that keeps demanding valid input, forever, no matter what garbage arrives, and only ever returns a value you can trust.

```text
def get_height():
    while True:                       <- Part 1: no do-while, so loop forever...
        try:                          <- Part 4: attempt the risky conversion
            height = int(input("Height: "))
            if height > 0:
                return height          <- ...and only escape with a valid answer
        except ValueError:            <- Part 4: garbage input? try again silently
            pass

def main():                            <- Part 2: your program's real entry point
    height = get_height()
    for i in range(height):            <- Part 1: range() drives the pyramid
        print("#" * (i + 1))

if __name__ == "__main__":             <- Part 2: only run if this file is executed directly
    main()
```

Every line of that block is something you already learned in this lesson: `while True` replaces the missing `do while`; `try`/`except ValueError` replaces C's return-value checking; `def` and the `__name__` guard replace prototypes and C's automatic `main`. This exact shape (a small function that validates its own input and never returns garbage) is what you'll build in the Capstone below, and it's the same shape every input-handling function you write from here on should follow.

---

## Key takeaways

1. **`for x in range(n):` replaces C's three-part `for` loop**, and the underscore convention (`for _ in range(n):`) signals a loop variable you're required to name but never use.
2. **Python has no `do while`.** The replacement is a deliberate `while True:` loop with a `break` once the input is acceptable.
3. **`def` defines a function with no type declarations at all**, but Python still executes top to bottom: call a function before its `def` appears anywhere in the file, and you get a `NameError`.
4. **Python never calls `main()` automatically.** You must define it, then call it yourself, conventionally guarded by `if __name__ == "__main__": main()`.
5. **Integer overflow and truncation are solved natively in Python; floating-point imprecision is not**: the first two came from choosing the wrong type, the third comes from finite bits meeting infinite decimals, which no language escapes.
6. **An exception lets a function signal failure separately from its return value.** `try`/`except ValueError` replaces C's return-value-only error checking, and you must name the specific exception(s) you expect to catch.

## Common pitfalls

- ❌ Calling a function before its `def` appears earlier in the file: Python raises `NameError: name '...' is not defined`. Define every function before the point where you first call it.
- ❌ Writing `def main():` and never calling it: Python attaches no special meaning to the name `main`; nothing runs until you call `main()` yourself.
- ❌ Converting user input with `int(input(...))` with no `try`/`except` around it: one non-numeric character raises an uncaught `ValueError` and crashes the whole program.
- ❌ Assuming Python solved *all* of C's numeric problems just because it solved integer overflow: floating-point imprecision is still there, unchanged, because the hardware didn't change.
- ❌ Reaching for a C-style loop with a manually incremented counter when `for _ in range(n):` says exactly the same thing more simply.

---

## 🛠️ Capstone Project: Mario's Pyramid, Rebuilt to Survive Anything

> This is the main hands-on project for the lesson. You'll rebuild Module 2's Mario brick pyramid in Python, but this time, its height comes from a `get_height()` function that cannot be broken by any input a user could possibly type, structured with `main()` and the `__name__` guard. Every route handler you write in the database-backed web app at the end of this course is a `def`, and every one of them validates its input exactly the way `get_height()` will here.

### What you will build

On [cs50.dev](https://cs50.dev), a single program, `mario.py`, that prints a left-aligned pyramid of `#` bricks whose height comes from the user, validated so thoroughly that no input, however malformed, can crash it.

- A `def main():` that drives the program and a separate `def get_height():` that owns all the input validation (Part 2).
- A `while True:` loop inside `get_height()` that keeps asking until it gets a usable answer, replacing the `do while` Python doesn't have (Part 1).
- A `try`/`except ValueError:` inside that loop so that letters, symbols, or an empty line are silently rejected instead of crashing the program (Part 4).
- An `if height > 0:` check so that zero and negative numbers are rejected too, not just non-numeric text.
- A `for` loop using `range()` to print each row of the pyramid (Part 1).
- The `if __name__ == "__main__":` guard around your call to `main()` (Part 2).

### Why this is the perfect practice

| Lesson idea | Where you use it in Mario's Pyramid |
|---|---|
| `def` and function arguments | `get_height()` is its own function, separate from `main()` |
| `NameError` / definition order | `get_height()` must be defined above the point where `main()` calls it |
| `while True:` replacing `do while` | The validation loop inside `get_height()` |
| `try`/`except ValueError` | Catching non-numeric input inside `get_height()` |
| `for` and `range()` | Printing each of the pyramid's rows |
| `main()` / `__name__` guard | The program's overall structure |

### Milestones (build them in order, each one works on its own)

1. **Hardcode the pyramid first.** In a new `mario.py`, write a `for` loop using `range()` that prints a hardcoded pyramid of height 4: row `i` should contain `i + 1` hash marks (`#`, then `##`, then `###`, and so on). Run it with `python mario.py` and confirm the shape before changing anything.
2. **Wrap it in `main()`.** Move that loop inside a `def main():` and call `main()` at the bottom of the file. Confirm the program still prints the same pyramid.
3. **Write `get_height()` on its own, and test it alone.** Above `main()`, write `def get_height():` containing a `while True:` loop that uses `input()` and `int()` to ask `"Height: "`, wrapped in `try`/`except ValueError:` so bad input is silently ignored and the loop asks again. For now, have `main()` just call `get_height()` and `print()` the result, so you can confirm it survives garbage input (letters, blank lines, symbols) before wiring it into the pyramid.
4. **Reject zero and negative heights too.** A `ValueError` only catches non-numeric text: typing `-5` or `0` converts to a valid integer that still shouldn't be allowed. Add an `if height > 0: return height` check inside the loop so only positive numbers escape it.
5. **Wire `get_height()` into the pyramid.** Replace the hardcoded `4` from Milestone 1 with a call to `get_height()`, so the pyramid's size now comes entirely from validated user input.
6. **Add the `__name__` guard.** Replace your direct call to `main()` with `if __name__ == "__main__": main()`.
7. **Stretch goals.** Refactor the row-printing itself into a third function, `def print_row(width):`, mirroring the `print_row` you wrote in C back in Lesson 8's capstone. Or extend the pyramid to the full double-sided version from Module 2's problem set, adding a `get_width()` function alongside `get_height()` that validates the same way.

### How you will know you are done

- ✅ Typing letters, symbols, an empty line, `0`, or a negative number at the height prompt never crashes the program: it always just asks again.
- ✅ Typing any positive whole number prints a correctly-sized pyramid, with row `i` containing `i + 1` bricks.
- ✅ `get_height()` and `main()` are separate functions, with `get_height()` defined above the point where `main()` calls it.
- ✅ The file ends with `if __name__ == "__main__": main()`, not a bare call to `main()`.

> 💡 **Keep yourself honest:** before you call it done, deliberately try to break `get_height()` with the worst input you can think of: an empty line, a sentence, an emoji. A validation function you haven't tried to break is a validation function you haven't actually tested.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Counting with `range()` and the underscore (foundational)
Write a `for` loop using `range()` that prints the numbers 1 through 10, one per line (hint: `range(1, 11)` starts counting from 1 instead of 0). Then, on a separate line below it, write a second loop using the underscore convention that prints your name exactly 5 times, since the loop's counter isn't needed for that one.

### Exercise 2: A reusable validated-input function (intermediate)
Write `def get_positive_int():` that loops forever with `try`/`except ValueError` until the user enters a whole number greater than zero, then returns it, the same shape as `get_height()`, under a different name. Call it from a `def main():`, guarded by `if __name__ == "__main__":`, and print the value it returns.

### Exercise 3: Counting valid and invalid entries (advanced)
Write a program with a function `def count_entries():` that loops forever asking the user to type a number. Before converting anything, check if the user typed the word `"done"` and, if so, `break` out of the loop. Otherwise, use `try`/`except ValueError` to attempt the conversion: keep a running count of successful conversions and a separate count of rejected ones. When the loop ends, return both counts and print them from `main()`.

---

## Cheat sheet

```text
LOOPS
  while cond:            checks BEFORE running (same idea as C)
  for x in range(n):     Python's replacement for C's for (int i = 0; i < n; i++)
  for _ in range(n):     underscore = "I need a variable here, but I never use it"
  while True: ... break  Python's replacement for C's missing do-while

FUNCTIONS
  def name(arg):          no return type, no argument types -- Python infers them
      ...
      return value        omit if the function has nothing to hand back
  Call a function only AFTER its def -- calling it too early raises NameError.

ENTRY POINT CONVENTION
  def main():
      ...
  if __name__ == "__main__":
      main()               <- Python NEVER calls main() for you; you must call it

NUMERIC ISSUES, REVISITED (root cause: finite bits, always -- Lesson 8)
  truncation        -> SOLVED: int / int now gives a real decimal (// for old behavior)
  integer overflow  -> SOLVED: Python ints grow as large as memory allows
  float imprecision -> STILL HAPPENS: 64-bit floats are still finite, in any language

EXCEPTIONS
  try:
      risky_code()
  except ValueError:      name the SPECIFIC exception you expect
      handle_it()
  C: check the return value yourself, every time, or risk a silent bug
  Python: attempt the code; only handle failure if it actually happens
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 7 (Conditionals and loops):** `while` survives almost unchanged; `for` is genuinely rebuilt around `range()`; `do while` disappears entirely, replaced by `while True:` plus `break`.
- **Earlier, Module 2 · Lesson 8 (Functions, code quality, and the limits of numbers):** `def` replaces C's typed function declarations and prototypes; scope is enforced more loosely; two of the three numeric bugs from that lesson (integer overflow, truncation) are solved natively, while floating-point imprecision persists unchanged.
- **Earlier, Module 7 · Lesson 25 (Python essentials):** this lesson assumed you were already comfortable with `print()`, `input()`, F-strings, and Python's lack of semicolons and type declarations.
- **Next, Module 7 · Lesson 27 (Lists, dictionaries, and the pip ecosystem):** the `for` loops and functions from this lesson combine with Python's built-in list and dictionary types, and you'll install your first third-party library with `pip`.
- **Later, Module 11:** every route handler in the database-backed web app you build at the end of this course is a `def`, and every one of them validates its input with `try`/`except` exactly like `get_height()` did here.

---

*Source: "CS50x 2026 - Lecture 6 - Python" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
