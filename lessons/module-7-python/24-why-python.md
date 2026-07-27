# Module 7 · Lesson 24: Why Python? Your First Scripts

> **Course:** Self-Paced CS50x
> **Module 7:** Python: the same ideas, ten times less code
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 6 - Python](https://www.youtube.com/watch?v=Rl0ludWTLxs) · [full transcript](../../transcripts/08-lecture-6-python.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Python trades away almost every piece of ceremony C makes you write (headers, a `main` function, semicolons, declared types) for a language you run directly and that already ships with power tools like sets and image filters, and today you'll prove both halves of that bargain yourself: faster to write, a little slower to run.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *Same Problem, Ten Times Less Code*, where you write `hello.py`, re-solve a tiny C program you already wrote in Python and count the lines side by side, and apply an image filter to a picture in about four lines. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Today's exact benchmark numbers (1.87 seconds, 1.32 seconds) and today's exact library (PIL) will age. The design philosophy that explains why Python code looks the way it does will not.
>
> - **[PEP 20: The Zen of Python](https://peps.python.org/pep-0020/) by Tim Peters (2004).** This short, official design document lists the principles the Python language itself was built around: "Simple is better than complex," "Readability counts," "There should be one, and preferably only one, obvious way to do it." Every piece of "missing ceremony" you see in this lesson (no headers, no semicolons, `print` instead of `printf`) is that philosophy made literal in the syntax.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Higher-level language:** a programming language that hides more of the computer's low-level bookkeeping (compiling, declared data types, memory addresses) so you can write less code to get the same job done, usually at some small cost in how fast the finished program runs.
- **Interpreter:** a program that reads your source code and carries it out directly, one line at a time, instead of translating the whole file into machine code ahead of time the way a compiler does. Python is itself an interpreter: a program, just like `clang` is a program.
- **Script:** a lightweight program, typically read and run top to bottom, left to right, without the ceremony (headers, a `main` function) that a compiled language like C requires.
- **`def`:** the Python keyword that begins a function definition, short for "define." It replaces C's "return type, then name, then parameter types" with just a name and parameter names.
- **`set`:** a built-in Python data type that stores a collection of values with no duplicates and no guaranteed order, so you can ask "is this value in here?" without writing your own hash table.
- **Library (module):** code someone else already wrote that you can reuse. Python calls one library file a "module"; a collection of modules bundled together is a "package."
- **PIL (Python Imaging Library):** a library, distributed today under the name "Pillow," for opening, transforming, and saving image files in a handful of lines instead of looping over pixels yourself.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

You've just spent several lessons learning C the hard way: headers, compilation, declared types, and, in Module 6, a hash table you built yourself, bucket by bucket. That was deliberate. As Malan tells the class on day one of this transition:

> "…among the goals for this week and this week's problem set and really the rest of the course is to get you more comfortable feeling uncomfortable in front of your keyboard, because we're not going to give you and tell you everything you need to know for a language like Python." (David Malan)

Today that discomfort starts paying interest. The same ideas you already understand (a function, a collection of unique values, a transformation applied to an image) get expressed in a fraction of the code, because Python is what this lesson calls a **higher-level language**. This is not a detour from the course's spine, either: Flask, the web framework you'll use to build this course's final database-backed project in Module 11, is itself written in Python. Every script you write from here forward is direct rehearsal for that capstone.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what makes a language "higher-level" than C, and state the concrete trade-off Malan measured when he benchmarked the two (faster to develop, a little slower to run).
2. Write, save, and run a Python script (`hello.py`) on cs50.dev with no header, no `main` function, and not a single semicolon.
3. Translate a small piece of C logic into Python using `def` (no declared types, no declared return type) and `set()` (no hand-built hash table), and explain in your own words why the Python version ends up shorter.
4. Apply an image filter (blur or edge detection) to any image using the PIL library in about four lines of Python.

## Prerequisites

- **Module 2 · Lesson 5: Hello, C**: you should already be able to write, compile with `make`, and run a small C program on cs50.dev.
- **Module 6 · Lesson 23: Trees, hash tables, and tries**: the `set()` you'll use in this lesson is the payoff of the hash table you hand-built there. You don't need to remember every implementation detail, just what a hash table is *for*: fast membership checks.
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**).

---

## Part 1: Why Python? Trading syntax for speed of development

C was never meant to be the whole story. After weeks of headers, curly braces, and manual memory management, Malan opens this lecture by naming exactly what's about to change:

> "Today, very excitingly, all of that is truly going to go away and be distilled into a single line of code when you indeed want to have the computer say something like Hello world." (David Malan)

Why did it take decades for languages like Python to show up, instead of everyone just starting there? Malan's answer is a story about hardware and human judgment, not magic:

> "So humans over the decades learned from earlier designs, earlier programming languages, what worked well, what did not. Computers got faster. Computers had more memory, and so you were able to start spending more of those resources in order to have the computer do more for you. And so you don't need to be as pedantic syntactically anymore." (David Malan)

That is the definition of a **higher-level language** in one sentence: it spends some of the computer's now-abundant speed and memory on *your* time instead, so you type less and the interpreter figures out more. Malan names this directly:

> "And this is what we mean by Python being a higher level language." (David Malan)

This does not mean Python is simply "better" than C. It means Python and C are tools built for different priorities, and, as you'll measure yourself later in this lesson, that convenience is not free. It costs a small amount of runtime speed. Malan is also candid that CS50 will not spoon-feed you every rule of this new language the way it did with C:

> "…among the goals for this week and this week's problem set and really the rest of the course is to get you more comfortable feeling uncomfortable in front of your keyboard, because we're not going to give you and tell you everything you need to know for a language like Python." (David Malan)

In practice, that means when this lesson (or a later one) doesn't cover some Python behavior you're curious about, the correct move is to look it up (in the official documentation at `docs.python.org`, or by asking an AI assistant a narrow, specific question), exactly the research habit **Module 2 · Lesson 6** already had you practicing with C's man pages.

> 🔑 **The single most important takeaway of this part.** "Higher-level" means the language spends the computer's abundant speed and memory on saving *you* typing and syntax, not that it automatically runs faster. Expect to write less code and look more things up.

---

## Part 2: `hello.py` vs. `hello.c` (the boilerplate disappears)

Recall the C version of the first program you ever compiled:

```c
#include <stdio.h>

int main(void)
{
    printf("hello, world\n");
}
```

Here is the entire Python equivalent, `hello.py`:

```python
print("hello, world")
```

One line. No `#include`, no `int main(void)`, no curly braces, no semicolon, and yet it does exactly the same thing. Laid side by side, here is everything that changed:

| In `hello.c` | In `hello.py` |
|---|---|
| `#include <stdio.h>` header needed | No headers at all |
| Must wrap code in `int main(void) { ... }` | No entry-point function needed: the file itself is the program |
| `printf` (the `f` means "formatted") | `print`: plainer, more human-friendly |
| Must type `\n` yourself for a new line | A new line is added for you automatically |
| Every statement ends in `;` | No semicolons |
| Compile first (`make hello`, which runs `clang` under the hood), then run `./hello` | Run directly: `python hello.py`, no separate compile step |

That last row matters enough to say plainly: Python is not only a language, it is also a program. Just as `clang` is the C compiler you've been invoking (via `make`) for weeks, `python` is the program that reads your `.py` file and runs it immediately: an **interpreter**, reading and executing your code top to bottom rather than translating the whole file into machine code first. There is nothing to build in advance; you write `hello.py` and immediately run `python hello.py`.

Malan calls this style of file, more generally, a **script**: a lightweight program that mostly just reads top to bottom, left to right, without the scaffolding a compiled language expects.

> ✅ **What to do about it:** on cs50.dev, forget `make` for Python files entirely. Save your file, then run it with `python filename.py` directly from the terminal.

---

## Part 3: The speed demo (rewriting the Problem Set 5 spell checker)

To show what a higher-level language buys you on a real problem, not just `hello, world`, Malan opens the actual staff solution to Problem Set 5, the spell checker you built in C by hand-rolling a **hash table** (the data structure **Module 6 · Lesson 23** walked you through, bucket by bucket, with its own hash function). Then, live, he reimplements the whole thing in Python.

He starts with one line that replaces the entire hash table:

> "The first thing I'm gonna do is declare a global variable, we'll call it words, and set that equal to the return value of a Python function called set, which essentially gives me a set object wherein I can store a whole bunch of words without duplicates." (David Malan)

That single call to Python's built-in **`set`**, a collection that automatically rejects duplicates and can be searched for membership, *is* the hash table. No buckets, no linked lists, no hash function to write. Next, defining the function that checks a word against the dictionary, Malan points out what's missing compared to C:

> "…we don't have to specify the type of the variable being passed in (word, in this case) and we also don't have to specify a return type for the function." (David Malan)

Put together, here is an illustrative reconstruction of `dictionary.py`, following the transcript step by step:

```python
words = set()

def check(word):
    return word.lower() in words

def load(dictionary):
    with open(dictionary) as file:
        words.update(file.read().split())
    return True

def size():
    return len(words)

def unload():
    return True
```

A few things worth noticing, all of which are new relative to C:

- `def` (short for "define") starts a function: no return type, no parameter types.
- `check` returns the result of `word.lower() in words` directly: a single Boolean expression asking "is this word a member of the set?" Python's `in` operator does the searching for you.
- `load` opens the dictionary file, reads its entire contents, splits it into individual words, and adds them all to the set with `.update()`: no manual character-by-character parsing.
- `unload` simply returns `True`, because Python manages its own memory. There is nothing for you to free.

Once it worked, Malan's own summary of the result was blunt:

> "And that's it in like 19 lines of code in Python, most of which are blank lines." (David Malan)

### The benchmark: develop faster, run a little slower

Writing the Python version took, in Malan's words, "a minute or two." But writing code quickly is only half the story: the other half is how fast the finished program runs. Malan ran both versions on the same large dictionary and text file:

> "…at the very end of this output I should see not only how many words were found, but the total time involved, which appears to be 1.87 seconds. Not bad, seeing as it only took me like what, a minute or two to write the actual code." (David Malan)

Then he ran the staff's C solution, the one built on a hand-written hash table, on the exact same input:

> "…total time spent in the CPU, not necessarily printing everything to the screen, which might take longer, is only 1.32 seconds versus the 1.87 seconds in Python. Now, while only half a second, that's a decent percentage of the total amount of time spent running this spell checker in each of the windows." (David Malan)

| | Python (`speller.py`) | C (`speller`) |
|---|---|---|
| Data structure used | built-in `set()` | hand-built hash table (Lesson 23) |
| Approximate time to *write* | a minute or two | a full problem set |
| Time to *run* on the large dictionary | **1.87 seconds** | **1.32 seconds** |

Why is the Python version slower, even though it's doing "the same" work? Because C is compiled (translated once, in advance, into machine code) while Python is generally interpreted:

> "So there's a bit of overhead when using Python, but I will say that the Python community has been working on this problem for some time, and so in general it's not necessarily going to be as significant a trade-off, because there's certain tricks we can do." (David Malan)

> 💡 **A nuance worth knowing:** the interpreter you're using (CPython) doesn't strictly re-read your source code line by line forever: under the hood it secretly compiles your code into an intermediate form called **bytecode** first, which is faster to re-run than plain text would be. It's still not the same as C's machine code, but it's why the gap isn't larger than half a second on a problem this size.

> 🔑 **The single most important takeaway of this part.** Python traded roughly 40% more runtime (1.87s vs. 1.32s) for a spell checker that took a couple of minutes to write instead of an entire problem set. That trade, "develop faster, run a little slower," is the central bargain of choosing a higher-level language, and it is frequently a bargain worth taking.

---

## Part 4: Four lines, one filter (PIL blur and edges)

For a second demonstration, Malan turns to Problem Set 4's image filters: instead of hand-writing pixel-by-pixel blur and edge-detection loops in C, he reaches for a library.

**PIL**, the Python Imaging Library (distributed today as the `pillow` package and already available in your cs50.dev codespace), gives you two objects worth knowing: `Image`, for opening and saving pictures, and `ImageFilter`, for a menu of ready-made transformations. Here is `blur.py`, reconstructed from the transcript:

```python
from PIL import Image, ImageFilter

before = Image.open("bridge.bmp")
after = before.filter(ImageFilter.BoxBlur(10))
after.save("out.bmp")
```

Four lines total: import the two features you need, open the image, apply a filter, save the result. Malan's own reaction:

> "So in just 4 lines of code, I claim I've implemented the blur function now in Python of what we did previously in C." (David Malan)

Now watch how little has to change to get an entirely different effect. Here is `edges.py`, identical except for one line:

```python
from PIL import Image, ImageFilter

before = Image.open("bridge.bmp")
after = before.filter(ImageFilter.FIND_EDGES)
after.save("out.bmp")
```

Swap `ImageFilter.BoxBlur(10)` for `ImageFilter.FIND_EDGES`, and:

> "…thanks to Python and just 4 lines of code, we now have all of our edges detected." (David Malan)

> 💡 **A nuance worth knowing:** neither `blur.py` nor `edges.py` invented anything new about how blurring or edge detection actually works: the math is exactly what you implemented by hand, pixel by pixel, in C. What changed is that someone else already wrote and published that math as a **library**, and Python makes it trivial to import and reuse. Knowing when to reach for an existing library instead of writing a loop yourself is itself a skill.

---

## Part 5: How the ideas combine

Every example in this lesson is really the same trade-off wearing a different costume:

```text
                    LESS CODE, MORE BUILT IN                       RUNTIME COST
  C:       #include, int main, declared types, semicolons,     ->  fast     (1.32s)
           hand-built hash tables, pixel-by-pixel loops
  Python:  print(), def, set(), PIL filters: the language        ->  a bit slower (1.87s)
           and its libraries do the low-level work for you

  Rule of thumb: prototype and build in Python for speed of development;
  reach for C only when the extra fraction of a second, byte, or bit
  of control genuinely matters.
```

`hello.py` removed C's ceremony (Part 2). `dictionary.py` removed the need to hand-build a data structure (Part 3). `blur.py` and `edges.py` removed the need to hand-write the transformation itself (Part 4). Stack all three and you get the module's tagline made literal: the same ideas, in roughly ten times less code, at the cost of a little speed.

---

## Key takeaways

1. **"Higher-level" means less code, not automatically faster code.** Python spends the computer's abundant speed and memory on saving you typing; you pay a small runtime cost for that convenience.
2. **`hello.py` has none of `hello.c`'s ceremony.** No headers, no `main`, no semicolons, and a new line is added for you automatically. Run it directly with `python hello.py`: there is no compile step.
3. **Python is itself a program (an interpreter).** It reads and executes your source code directly, rather than translating the whole file into machine code ahead of time the way `clang` does.
4. **`set()` and `def` turned a hand-built hash table into about 19 mostly-blank lines.** Same idea as Lesson 23's hash table, dramatically less code to get there.
5. **The measured trade-off was real and small: 1.87s vs. 1.32s.** A library like PIL can turn an entire image-processing routine into about four lines, blur and edge detection alike.

## Common pitfalls

- ❌ Assuming "higher-level" means "faster." Malan's own benchmark showed the opposite: the Python spell checker ran *slower* than the C one (1.87s vs. 1.32s), even though it was far quicker to write.
- ❌ Reaching for `make` out of habit. Python files don't get compiled that way: just run `python filename.py`.
- ❌ Manually typing `\n` at the end of a `print()` string. Python's `print` already adds a new line for you; typing your own usually just gives you a blank line you didn't want.
- ❌ Treating `set()` like an array or list. A set has no positions to index into: you can only ask whether something is a member of it (`in`), not ask for "the third item."
- ❌ Writing your own pixel-processing loop before checking whether a library like PIL already has the filter you need: reinventing what someone already published is rarely the fastest path.

---

## 🛠️ Capstone Project: Same Problem, Ten Times Less Code

> This is the main hands-on project for the lesson. You'll write your very first Python script, then prove the module's tagline to yourself by re-solving a tiny program you already wrote in C and literally counting the lines, and finally apply an image filter using a real third-party library, all on cs50.dev.

### What you will build

Three small, independent scripts on cs50.dev:

1. `hello.py`: your first Python program.
2. A Python rewrite of a tiny C program you already have from Module 2, with a side-by-side line count.
3. `blur.py`: a PIL-based blur filter applied to any image you choose.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| No headers, no `main`, no semicolons (Part 2) | Milestone 1: `hello.py` |
| `def` with no declared types (Part 3) | Milestone 2: your rewritten C program |
| The develop-faster / run-slower trade-off (Parts 1 & 3) | Milestone 2: the line-count comparison |
| A library doing the work for you in ~4 lines (Part 4) | Milestone 3: `blur.py` |

### Milestones (build them in order, each one works on its own)

1. **Write and run `hello.py`.** On cs50.dev, create `hello.py` containing a single line: `print("hello, world")`. Run it with `python hello.py`: no `make`, no compiling. Then edit it to print your own name instead, on its own line, still with no semicolon.
2. **Re-solve one tiny C program in Python, and count the lines.** Open the simplest arithmetic program you wrote back in Module 2, for example, a program that stores two whole numbers and prints their sum (no user input needed; hardcode the two numbers). Count its lines, including `#include`s, `int main(void)`, braces, declared types, and semicolons. Now write the Python equivalent (something like `x = 1`, `y = 2`, `print(x + y)`) using only what Part 2 taught you (no headers, no `main`, no declared types, no semicolons). Count those lines too, and write both totals down side by side.
3. **Blur an image.** Create `blur.py` on cs50.dev. Use `from PIL import Image, ImageFilter`, open any image already in your codespace (or drag in a small JPG or PNG, since Pillow handles more than just BMP), apply `ImageFilter.BoxBlur(10)`, and save the result to a new file. Open both the original and the blurred file to confirm the effect.
4. **Edge-detect the same image (stretch).** Duplicate `blur.py` as `edges.py` and change only the filter line to `ImageFilter.FIND_EDGES`. Confirm you changed exactly one line to get an entirely different effect.
5. **Time it yourself (stretch).** In your cs50.dev terminal, run `time python hello.py` (or your Milestone 2 script) and compare the "real" time reported to what you remember (or re-measure with `time ./yourprogram`) from the C version. You won't see exactly 1.87s vs. 1.32s (the programs are tiny), but you'll see the same *kind* of comparison Malan made.

### How you will know you are done

- ✅ `python hello.py` prints your name with no compile step and no semicolon anywhere in the file.
- ✅ You can state, out loud, the exact line counts of your Module 2 C program and your Milestone 2 Python rewrite, and roughly how many times shorter the Python version is.
- ✅ Opening the file `blur.py` produced actually looks visibly blurred compared to the original.
- ✅ You can explain, in your own words, why the Python version of any of these programs might run a little slower than the C version, even though it was faster to write.

> 💡 **Keep yourself honest:** don't skip the line-counting in Milestone 2 by eyeballing it: actually count both files. The "ten times less code" idea in this module's title is a claim worth verifying on your own code, not just taking on faith.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Two prints, no semicolons (foundational)
Write a new script, `greeting.py`, with two separate `print()` calls: one that prints a greeting, one that prints a fact about yourself. Run it with `python greeting.py`. Then open your Module 2 `hello.c` and count how many lines it takes to print those same two pieces of text in C (including headers, `main`, and two `printf` calls). Write both totals down.

### Exercise 2: Membership check with `set` (intermediate)
Write `membership.py`. Create `words = set()`, then add a handful of words to it in one call using `words.update("cat dog bird fish".split())` (the same `.split()` trick `load()` used in Part 3). Define a function `check(word)` exactly like the one in `dictionary.py`, returning `word.lower() in words`. Print the result of calling `check("cat")` and `check("shark")` directly: no need for a conditional statement, just print the Boolean value each call returns.

### Exercise 3: Two filters, one script (advanced)
Write `filters.py` that opens one image, applies `ImageFilter.CONTOUR` and saves it as `contour.png`, then re-opens the *original* image (not the contoured one) and applies `ImageFilter.FIND_EDGES`, saving that as `edges.png`. Confirm you now have three files, the original plus two differently filtered copies, from a script that is still well under ten lines.

---

## Cheat sheet

```text
HELLO WORLD
  hello.c:  #include, int main(void), printf("hello, world\n");, semicolons, make + ./hello
  hello.py: print("hello, world")                                            python hello.py
  -> no headers, no main, no semicolons, new line is automatic, no compile step

WHY "HIGHER-LEVEL"
  Computers got faster + gained more memory -> language spends that on YOUR time, not just runtime.
  Higher-level = less code to write. NOT automatically faster to run.

THE BENCHMARK (Problem Set 5 spell checker, same dictionary + text file)
  Python (set(), def, ~19 mostly-blank lines):  1.87 seconds to run, ~1-2 minutes to write
  C (hand-built hash table):                     1.32 seconds to run, a full problem set to write
  -> develop faster, run a little slower

KEY SYNTAX SEEN TODAY
  def name(params):        define a function - no return type, no parameter types
  set()                    a collection with no duplicates; check membership with `in`
  words.update(iterable)   add many values to a set at once
  with open(path) as file: open a file; closes automatically
  from PIL import Image, ImageFilter
  Image.open(path) / img.filter(ImageFilter.X) / img.save(path)

FOUR-LINE IMAGE FILTER
  from PIL import Image, ImageFilter
  before = Image.open("bridge.bmp")
  after  = before.filter(ImageFilter.BoxBlur(10))   # or ImageFilter.FIND_EDGES
  after.save("out.bmp")

RUN IT
  python filename.py     (no make, no clang, no separate compile step)
```

## How this connects to the rest of the course

- **Earlier, Module 6 · Lesson 23 (Trees, hash tables, and tries):** you hand-built a hash table, bucket by bucket, to solve Problem Set 5 in C. Today's `set()` and `dict` are that same idea, built into the language: you get the structure for free.
- **Next, Module 7 · Lesson 25 (Python essentials):** this lesson deliberately stayed narrow: just `print`, `def`, `set`, and one library. Lesson 25 fills in the rest of the syntax you'll need constantly: variables without declared types, conditionals, loops, lists, and dictionaries, translated directly from the C you already know.
- **Later, Module 11:** the final database-backed web app you design and ship at the end of this course runs on Flask, a Python library, exactly like the PIL library you used today, just built for web pages instead of images. Every script you write in Module 7 is direct rehearsal for that project.

---

*Source: "CS50x 2026 - Lecture 6 - Python" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
