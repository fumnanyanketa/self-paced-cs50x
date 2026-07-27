# Module 7 · Lesson 25: Python Essentials: Variables, Conditionals, Strings

> **Course:** Self-Paced CS50x
> **Module 7:** Python: the same ideas, ten times less code.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 6 - Python](https://www.youtube.com/watch?v=Rl0ludWTLxs) · [full transcript](../../transcripts/08-lecture-6-python.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Python replaces C's headers, semicolons, curly braces, and declared types with modules you `import`, a single `input()` function, variables whose type Python figures out on its own, colon-and-indentation conditionals, and strings that come with built-in actions like `.lower()` and `.capitalize()`: the exact same ideas you already learned in C, just typed in a fraction of the code.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you rebuild Module 2's greeter and agree programs entirely
> in Python. Everything before the Capstone teaches the skills you will use
> there. If you want to see the finish line first, jump to the **"Capstone
> Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Python's syntax will keep
> evolving, but the philosophy behind it was written down once and hasn't
> changed since.
>
> - **[PEP 20: The Zen of Python](https://peps.python.org/pep-0020/)** (Tim
>   Peters, 2004). Nineteen short lines ("Readability counts," "Explicit is
>   better than implicit," "There should be one, and preferably only one,
>   obvious way to do it") that explain why Python looks the way it does,
>   and why Malan keeps calling certain choices "pythonic" throughout this
>   lesson. Type `import this` into any Python interpreter and it prints the
>   whole thing.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Module:** a file of pre-written Python code you can reuse, Python's version of a C library.
- **Package:** a bundle of modules grouped together, the way a folder groups files.
- **Named parameter:** an argument you pass to a function by writing its name (like `end=""`) instead of relying on where it falls in the list of arguments.
- **F-string:** a specially marked string (written with an `f` right before the opening quote) where anything inside curly braces `{}` gets swapped out for a variable's actual value.
- **Object:** a value sitting in memory that carries both data and built-in actions it knows how to perform on itself.
- **Method:** a function that belongs to an object, called with a dot, like `name.lower()`.
- **Type conversion:** turning a value of one data type into another, like turning the text `"3"` into the number `3` with `int("3")`.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Module 2 spent two whole lessons on variables, data types, and conditionals in C, and you earned every line of that ceremony: declared types, curly braces, semicolons, `strcmp` loops just to compare two strings. Malan opens this lecture by naming exactly why that ceremony is about to disappear: **"humans over the decades learned from earlier designs, earlier programming languages, what worked well, what did not... so you don't need to be as pedantic syntactically anymore."** This lesson is not new material so much as it is the same four ideas from Module 2 (Lessons 6 and 7) rewritten with the ceremony stripped away. If a sentence here reminds you of C, that's the point: you're meant to feel the rhyme.

## Learning objectives

By the end of this lesson you will be able to:

1. Import a function from a module with `from cs50 import get_string`, explain why it is a "training wheel," and replace it with Python's own built-in `input()`.
2. Use named parameters like `end=` and `sep=` in `print()`, and look up any Python function's signature at docs.python.org.
3. Declare a variable with no type keyword, name Python's four core data types (`bool`, `float`, `int`, `str`), and convert typed-in text to a number with `int()`.
4. Write an `if`/`elif`/`else` chain that relies on Python's mandatory indentation instead of curly braces.
5. Compare strings with `==` and `in`, and normalize user input with string methods like `.lower()`, `.capitalize()`, and `.upper()`.

## Prerequisites

- **Module 2 · Lessons 6-7 (Input, Variables, and the Command Line; Conditionals and Loops):** you should already be comfortable with `get_string`, `get_int`, declared C types (`bool`, `char`, `int`, `float`), and `if`/`else if`/`else` chains. This lesson assumes that vocabulary and shows you its Python mirror.
- **Lesson 24 (Why Python? Your first scripts):** you should already have run a `.py` file with `python` on cs50.dev and seen `print("hello, world")` work with no `#include`, no `main`, and no semicolon.

---

## Part 1: Modules, packages, and taking off the CS50 training wheels

In C, `#include <cs50.h>` gave you `get_string` by pointing the compiler at a header file. Python has its own vocabulary for the same idea. As Malan puts it: **"anytime you hear someone discussing a module or a package in Python, they're just talking about using a library."** A **module** is a single file of reusable code, Python's word for what C called a library. A **package** is just a collection of modules bundled together, the way a folder holds several files. Some modules ship built into the language; others, like the CS50 library, you install yourself.

To smooth the move from C, CS50 built a Python version of its own library, with familiar names like `get_string`, `get_int`, and `get_float`. The syntax for reaching it is different from a header include:

```python
from cs50 import get_string

answer = get_string("What's your name? ")
print(f"hello, {answer}")
```

`from cs50 import get_string` tells Python exactly one thing you want out of the `cs50` module, rather than pulling in the whole library. But Malan is upfront that this (like `get_int`, `get_char`, and the rest of the CS50 library) is scaffolding, not a real Python feature: **"these two though are meant to be training wheels that you can take off and should take off, you know, even within a week or so."**

Python already has a built-in function that does the same job with no import at all: `input()`. It prompts, waits, and hands back whatever the user typed: exactly like `get_string`, minus the CS50 dependency. As Malan concludes once he swaps it in: **"input is generally going to be the way you go about getting input now from the user."**

```python
answer = input("What's your name? ")
print(f"hello, {answer}")
```

Notice the `f` right before the opening quote in `print(f"hello, {answer}")`: that marks it as an **f-string**, where `{answer}` gets replaced with the actual value stored in `answer` when the line runs. Leave off the `f` and Python prints the literal text `{answer}`, curly braces and all, a bug Malan deliberately triggers in class to show what the `f` is doing.

> 🔑 **`import` is Python's `#include`, but narrower and named per-function, and CS50's own library is a training wheel meant to come off within the first week or two of using Python.**

## Part 2: Named parameters and reading the docs

Every argument you passed to `printf` in C was a **positional parameter**. Order was everything: the format string first, then the values, in that exact sequence. Python supports that too, but it adds a second option. In Malan's words: **"Python additionally supports what are called named parameters whereby you don't have to rely only on the order in which you're enumerating the arguments to a function."** Instead of remembering a position, you write the parameter's actual name when you call it.

`print()` is the clearest example. By default, `print()` ends every call with a newline and separates multiple arguments with a single space: you've been getting both for free. Override either one by naming it:

```python
print("$", end="")        # no newline: the next print() continues on this line
print("$", end="\n")      # back to the default behavior, explicitly
print("cat", "dog", sep=", ")   # -> cat, dog
```

How would you know `print` even has parameters called `end` and `sep`, or what their defaults are, without being told in lecture? You read the documentation. Malan names the exact place to look: **"if you want to learn more about Python and the functions it offers and the arguments it takes, you go to the official documentation, docs.python.org."** Unlike C's scattered, decades-old man pages, Python's own community maintains one official reference. Scroll to the entry for `print` and you'll see its **signature**, the same concept as a C function prototype. Malan describes reading one: **"this is representative of a Python prototype, if you will, also called a signature, that just tells you the name of a function and then how many and what type of arguments it takes."** That signature is also where you'd learn the default value for `end` is `"\n"` and for `sep` is `" "`, the two defaults you've been relying on without knowing their names.

> ✅ **What to do about it:** whenever a function takes more arguments than you want to memorise the order of, check docs.python.org for its signature and pass the ones you need by name.

## Part 3: Variables and data types (no declarations, no pointers)

Recall from C: `int counter = 0;` (type, name, value, semicolon). Python drops two of those four pieces:

```python
counter = 0
```

No type keyword, no semicolon. That doesn't mean types vanished: Python is simply inferring the type from the value you gave it. The types themselves are a trimmed-down version of what you already know from Module 2. In Malan's rundown: **"we still have bools, we still have floats, we still have ints, and we do have strings, but they're literally called strs."** `char` does not survive the move: **"there is no way to get a single character per se, but you can get a string that has a single character... char is not a data type in Python."** Every place C made you choose between `char` and `string`, Python just gives you `str`.

One thing disappears entirely, and Malan calls it out directly, having spent two full weeks of Module 5 on it: **"there are no pointers in Python."** Whatever memory management you did by hand with `malloc` and `free`, Python now does for you.

The catch shows up the moment you try to do arithmetic on `input()`'s return value. Recall `calculator.c` from Module 2, rewritten first the naive way:

```python
x = input("What's x? ")
y = input("What's y? ")
print(x + y)     # typing 1 and 2 prints "12", not 3
```

`input()` always returns a `str`, so `+` here concatenates two pieces of text instead of adding two numbers. Fixing it means converting, not casting. Malan draws that distinction precisely: **"we're not casting, but converting, and converting just implies that there's a little more work that has to be done."** In C you told the compiler what a value already was; in Python you call a function that builds a new value of the type you want. As Malan puts it: **"the data type itself is a function that takes an argument which is the str, or string, that you want to convert."**

```python
x = int(input("What's x? "))
y = int(input("What's y? "))
print(x + y)     # 3
```

Nesting the call this way (passing `input()`'s output straight into `int()`) is exactly the kind of thing Malan flags with the term this lesson's first-principles companion is built around: **"To do something pythonically is to do it the way that most Python programmers would do it."**

> ✅ **What to do about it:** if a program is supposed to do math on something the user typed, wrap `input()` in `int()` or `float()` before you touch it with `+`, `-`, `*`, or `/`.

## Part 4: Conditionals and mandatory indentation

Module 2 Lesson 7 called `if`/`else if`/`else` "the proverbial fork in the road." The fork itself doesn't change in Python: only its punctuation does. Here is `compare.c`'s logic, rewritten:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
else:
    print("x is equal to y")
```

Three changes from C: no parentheses around the condition, no curly braces around the block, and `else if` shrinks to one word, `elif`. In their place, Python asks for a colon at the end of each `if`/`elif`/`else` line, and it *requires* the lines underneath to be indented. This isn't a style suggestion the way it was with `style50` in C: it's the actual syntax. Malan is blunt about how strict this is: **"Python requires that you indent your code properly."** He goes further: **"You can't be lazy and leave it all left aligned and sort of fix it up later."** Skip the indentation and Python refuses to run the program at all, the same way a missing semicolon once stopped `clang`, except now it's whitespace doing the enforcing.

The comparison operators themselves (`<`, `>`, `<=`, `>=`, `==`, `!=`) are identical to the C table you already learned. What has changed is only the punctuation wrapped around them.

> 🔑 **Python has no curly braces. A colon plus consistent indentation is the entire syntax for "this code belongs to that condition."**

> 💡 **A curiosity worth knowing:** a student in lecture asked what language Python itself is written in. Malan's answer: **"The interpreter we are using within VS Code is itself written in C, AKA CPython."** The tool translating your Python, line by line, into something the machine can run is, underneath, a C program, the same language you spent five weeks learning.

## Part 5: Strings are objects (comparison and methods)

Module 2's hardest string lesson was that `s == t` in C compares two addresses, not two words: you needed `strcmp`, a loop, and knowledge of the null terminator just to ask "are these the same word?" Python erases that entire problem. Rewriting `compare.c`'s string-comparing sibling:

```python
s = input("s: ")
t = input("t: ")

if s == t:
    print("same")
else:
    print("different")
```

`==` here just works, character by character, with no loop of your own. Malan's verdict: **"Python has solved that seemingly annoying problem of not taking us literally, like, don't compare the pointer against the pointer. Compare what a reasonable programmer probably really cares about, the values of those strings."**

Now recall `agree.c`: get a `char`, compare it against `'y'` and `'Y'` with `||`. In Python there's no `char` (just a `str`, however long), so the comparison becomes a plain string check, and Python's `in` keyword lets you check membership in a whole list of acceptable answers at once instead of chaining comparisons:

```python
s = input("Do you agree? ")
s = s.lower()

if s in ["y", "yes"]:
    print("Agreed")
else:
    print("Not agreed")
```

`s.lower()` is doing something new: it's not a standalone function you pass `s` into (the way C's `tolower` worked), it's an action `s` performs *on itself*, called with a dot. Malan names what's really going on here: **"methods are simply functions that are inside of objects and in this case the object in question itself is a string."** A **string** in Python isn't just text sitting in memory the way a C string was. It's an **object**: a value that carries both its data and a set of built-in **methods** for acting on that data. `s.lower()` normalizes capitalization so `"YES"`, `"Yes"`, and `"yes"` all match the same check; without it, `"YES" in ["y", "yes"]` would fail.

Two more of those built-in methods, straight from the transcript's own examples. First, `copy.c`'s Python equivalent, capitalizing just the first letter:

```python
s = input("s: ")
t = s.capitalize()

print(f"s: {s}")
print(f"t: {t}")
```

Malan explains `.capitalize()` by pointing at its documentation entry: **"S.capitalize... whose purpose in life, if we read Python's documentation for string methods, will be to uppercase the first letter of the word that the user has presumably just typed in."** And second, `uppercase.c`'s equivalent, capitalizing the whole word, no loop required:

```python
before = input("before: ")
after = before.upper()

print(f"after:  {after}")
```

Where the C version looped character by character calling `toupper` on each one, Python's `.upper()` acts on the entire string in one call. Malan's summary of why that's possible: **"these strings are objects and those objects have methods. Those methods will actually operate on the entire string at once, unlike the more pedantic work we had to do character by character in C."** (Lesson 26 picks this exact thread back up when it shows you how a `for` loop *can* still walk a string one character at a time. You just rarely need to anymore.)

> ✅ **What to do about it:** before you write a loop or a chain of `or`s to handle a string, check whether a method already named for the job exists: `.lower()`, `.upper()`, and `.capitalize()` are the ones you'll reach for constantly.

---

Put the five parts together and you get the whole shape of this lesson, the same pipeline as Module 2, with every piece of ceremony trimmed away:

```text
MODULES        from cs50 import get_string   ->   input()
                                                    (Part 1: training wheels off)

PARAMETERS     printf("%s", x)               ->   print(x, end="")
                                                    (Part 2: named, not just positional)

VARIABLES      int x = get_int(...);         ->   x = int(input(...))
                                                    (Part 3: no declared type, converted not cast)

CONDITIONALS   if (x < y) { ... }            ->   if x < y:
                                                       ...
                                                    (Part 4: colon + indentation, not braces)

STRINGS        strcmp(s, t) == 0             ->   s == t
               c == 'y' || c == 'Y'          ->   s.lower() in ["y"]
                                                    (Part 5: value comparison + methods, no char)
```

---

## Key takeaways

1. **Modules and packages are Python's word for libraries.** `from cs50 import get_string` pulls in one function; the CS50 library itself is a training wheel meant to come off in favor of `input()`.
2. **Named parameters let you skip memorizing argument order.** `print(end="", sep=", ")` overrides defaults by name; docs.python.org is where you look up any function's signature to find those names.
3. **Variables have no declared type, but the underlying types didn't disappear.** `bool`, `float`, `int`, and `str` still exist; there is no `char` (a single character is just a `str` of length one) and no pointers.
4. **`int()` and `float()` convert a string to a number; they don't cast it.** `input()` always returns a `str`, so math on user input needs an explicit conversion first: skip it and `+` concatenates instead of adding.
5. **Indentation is mandatory syntax, not a style choice.** A colon ends each `if`/`elif`/`else` line; the indented block underneath is how Python knows what belongs to that branch.
6. **Strings are objects, and `==` compares their values, not their addresses.** No more `strcmp`, and methods like `.lower()`, `.capitalize()`, and `.upper()` act on a whole string at once via dot notation.

## Common pitfalls

- ❌ Doing math directly on `input()`'s return value: `input("x: ") + input("y: ")` concatenates two strings; wrap each call in `int()` or `float()` first.
- ❌ Leaving a conditional's body un-indented, or mixing tabs and spaces: Python treats this as a syntax error, not a style nit.
- ❌ Writing `else if` out of C habit, Python's keyword is one word: `elif`.
- ❌ Comparing user input to one fixed capitalization, like `if s == "Y":`, and missing `"y"`, `"yes"`, or `"YES"`: normalize first with `.lower()` or `.upper()`.
- ❌ Assuming `char` still exists as its own type: a single character in Python is simply a `str` with one letter in it.

---

## 🛠️ Capstone Project: Greeter and Agree, Reborn in Python

> This is the main hands-on project for the lesson. You'll rebuild two
> programs you already wrote once in C, proving to yourself, line by
> vanished line, exactly how much of that C ceremony Python was doing for
> you all along.

### What you will build

Two small Python programs, run on cs50.dev: a `greet.py` that captures and echoes back a name, and an `agree.py` that normalizes and branches on a yes/no answer, the direct Python siblings of Module 2's `greeter.c` and `agree.c`. Alongside the code, you'll keep a running tally of every line of C boilerplate that had no Python equivalent.

- `greet.py`: `input()`, an f-string, and a named parameter used on purpose.
- `agree.py`: `input()`, `.lower()`, `in`, and an `if`/`else` branch.
- A short boilerplate audit: the count of vanished `#include`s, `main`, curly braces, semicolons, and declared types.

### Why this is the perfect practice

| Lesson idea | Where you use it in the project |
|---|---|
| Modules & training wheels (Part 1) | `greet.py` uses `input()` instead of `from cs50 import get_string` |
| Named parameters (Part 2) | Using `end=` or `sep=` at least once to control `print()`'s formatting |
| Variables & conversion (Part 3) | A bonus numeric prompt in `greet.py`, converted with `int()` |
| Conditionals & indentation (Part 4) | `agree.py`'s `if`/`elif`/`else` chain, correctly indented |
| String methods (Part 5) | `.lower()` and `in` in `agree.py` to accept multiple spellings of "yes" |

### Milestones (build them in order, each one works on its own)

1. **Rebuild the greeter.** Create `greet.py`. Use `input()` to ask "What's your name? ", store it in a variable, and print `f"hello, {name}"`. Confirm it behaves exactly like Module 2's `greeter.c`, with none of its `#include`s, `main`, or semicolons.
2. **Add a named parameter on purpose.** Change one `print()` call in `greet.py` to use `end=""` or `sep=", "` somewhere reasonable (for example, printing the greeting without a trailing newline, then adding a second `print()` with just `"!"`). Confirm the output still reads correctly.
3. **Rebuild agree, the naive way first.** Create `agree.py`. Ask "Do you agree? " with `input()`, and branch with `if s == "y" or s == "Y":` / `else:`, printing `Agreed` or `Not agreed`. Confirm both branches work.
4. **Normalize and expand with `.lower()` and `in`.** Replace the `or` chain with `s = s.lower()` followed by `if s in ["y", "yes"]:`. Test with `y`, `Y`, `yes`, and `YES`: all four should now print `Agreed`.
5. **Add one numeric prompt.** In `greet.py`, add a second question (a lucky number) captured with `int(input(...))`, and print it doubled using an f-string. This is the same `int()`-around-`input()` pattern from Part 3, just reused.
6. **Audit the vanished boilerplate.** Open Module 2's `greeter.c` and `agree.c` side by side with your two new files. Write a comment at the top of each Python file listing every line from the C version that has no Python counterpart: headers, `int main(void)`, curly braces, semicolons, declared types, and (for `agree.c`) the `char`/single-quote comparisons.
7. **Stretch goals.** Add a third branch to `agree.py` with `elif` for an answer like `"maybe"`. Or use `.capitalize()` on the name in `greet.py` before printing it, so `"david"` greets back as `"David"`.

### How you will know you are done

- ✅ `python greet.py` prints a personalized greeting and a doubled lucky number, using `input()` and `int()` only, no `cs50` import anywhere.
- ✅ `python agree.py` prints `Agreed` for `y`, `Y`, `yes`, and `YES`, and `Not agreed` for anything else.
- ✅ Your boilerplate-audit comment names at least five specific lines or symbols from the C versions (headers, `main`, braces, semicolons, declared types, `strcmp`/single quotes) that Python needed none of.

> 💡 **Keep yourself honest:** this exact pattern (take raw text from a user,
> normalize it with `.lower()`, and branch on it) is precisely what you'll
> do to sanitize a web form's input in the database-backed app you build at
> the end of this course. Get comfortable with it now.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Three-way number comparator (foundational)
Write a Python program that asks for two numbers with `input()`, converts each with `int()`, and prints whether the first is less than, greater than, or equal to the second, the direct Python translation of Module 2's `compare.c`, using `if`/`elif`/`else` and proper indentation.

### Exercise 2: Capitalize vs. uppercase (intermediate)
Write a program that asks for a word once, then prints both `word.capitalize()` and `word.upper()` on separate lines using f-strings, so you can see side by side exactly how the two methods differ on the same input.

### Exercise 3: A three-way agree, tightened (advanced)
Extend `agree.py` to accept a third answer, "maybe," using `elif` and its own `in` list (so `"maybe"`, `"not sure"`, and `"unsure"` all count). Then, using only named parameters (no string concatenation), make the final line of output print all three possible responses (Agreed, Not agreed, Unsure) on one line separated by commas, by calling `print()` three times with a `sep=` or `end=` combination of your choosing.

---

## Cheat sheet

```text
MODULES & PACKAGES
  from cs50 import get_string     import one function (training wheel)
  answer = input("Name? ")        the real Python way, no import needed

NAMED PARAMETERS (print)
  print(x, end="")                 suppress the trailing newline
  print(x, y, sep=", ")            change what separates multiple arguments
  docs.python.org                  official reference for any function's signature

VARIABLES & TYPES            no declared type; Python infers it
  bool   float   int   str         the four core types (no char, no pointers)
  int(input(...))                  convert typed text to a number (not a cast)

CONDITIONALS
  if x < y:
      ...
  elif x > y:                      one word, not "else if"
      ...
  else:
      ...
  colon + indentation = Python's curly braces; indentation is mandatory

STRINGS AS OBJECTS
  s == t                           compares VALUES (no strcmp needed)
  s in ["y", "yes"]                membership check across a whole list
  s.lower()   s.upper()   s.capitalize()    methods, called with a dot
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lessons 6-7 (Input, Variables, and the Command Line; Conditionals and Loops):** you learned `get_string`/`get_int`, declared C types, and `if`/`else if`/`else` chains with `||`. This lesson is the Python mirror of both lessons at once: same ideas, a fraction of the syntax.
- **Earlier, Lesson 24 (Why Python? Your first scripts):** got you running your first `.py` file. This lesson is where that first script grows into real variables, branching logic, and string handling.
- **Next, Lesson 26 (Loops, functions, and exceptions):** picks up exactly where Part 5 left off: Python's `for` and `while` loops, `def` for your own functions, and `try`/`except` for handling errors without checking return values.
- **Later, the north-star project:** the `.lower()`-and-branch pattern from `agree.py` is the same technique you'll use to validate and normalize every form field in the database-backed web app you build at the end of this course.

---

*Source: "CS50x 2026 - Lecture 6 - Python" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
