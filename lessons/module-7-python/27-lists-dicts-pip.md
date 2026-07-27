# Module 7 · Lesson 27: Lists, Dictionaries, and the pip Ecosystem

> **Course:** Self-Paced CS50x
> **Module 7:** Python: the same ideas, ten times less code
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 6 - Python](https://www.youtube.com/watch?v=Rl0ludWTLxs) · [full transcript](../../transcripts/08-lecture-6-python.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Python's built-in `list` and `dict` types replace the array and the hand-built hash table you coded in C, the `csv` module reads and writes real data files in a few lines instead of hundreds, and a single `pip install` pulls in code that other people already wrote and tested: three upgrades that turn a script into something that behaves like a real, data-driven application.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a phonebook that stores contacts as a list of dictionaries, saves them to a CSV file so they survive a restart, and finishes with your own QR-code generator built from a third-party package you installed yourself. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Python's `csv` module is recent; the file format it reads and writes is not.
>
> - **[RFC 4180: Common Format and MIME Type for Comma-Separated Values (CSV) Files](https://www.rfc-editor.org/rfc/rfc4180)** (Y. Shafranovich, 2005). This short internet standard documents the plain-text convention (one record per line, fields separated by commas, an optional header row) that spreadsheets and databases had already been using informally for decades. Python's `csv` module is just one language's implementation of a format that predates it and will outlive any particular tool you use to read it.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **List:** an ordered, resizable collection of values: Python's upgrade to the fixed-size array you used in C (Module 2 · Lesson 6 and Module 3 · Lesson 11).
- **Dictionary (`dict`):** a collection of key-value pairs. Instead of looking up a value by its numeric position (like `array[0]`), you look it up by a name you choose, called a **key** (like `person["name"]`).
- **Method:** a function that belongs to a value, called with a dot, like `.append()` or `.lower()`. You already met a couple of these in Lesson 26; this lesson adds more.
- **Command-line argument:** an extra word typed after a program's name when you run it, such as the `David` in `python greet.py David`.
- **Context manager (the `with` statement):** a Python construct that automatically cleans up a resource (most commonly, closing a file) for you once you're done with it, even if something goes wrong in between.
- **CSV (comma-separated values):** a plain-text file format for tabular data, one row per line, values separated by commas. Openable in Python, Excel, Google Sheets, or a plain text editor.
- **Module / package:** Python's words for a library. A module is one file of pre-written code; a package is a bundle of modules. Some ship with Python itself; others are third-party and must be installed separately.
- **pip:** the command-line program that downloads and installs third-party Python packages into your own project.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In Module 6 · Lesson 23 you built a hash table by hand in C: you wrote the array of buckets, the hashing function, and the chaining logic yourself, entirely to get fast key-based lookup. Python hands you that same capability for free. As Malan puts it while introducing the dictionary type:

> "The dictionaries are sort of hash tables in particular are sort of the Swiss Army knives of data structures, and that they just let you associate some piece of data with others." (David Malan)

That is the theme of this whole lesson: lists and dictionaries give you, in one line, data structures that took you an entire problem set to build in C; the `csv` module gives you real, persistent storage in a handful of lines instead of the manual `fopen`/`fprintf` bookkeeping from Module 5 · Lesson 20; and `pip` gives you access to code that thousands of other programmers have already written, tested, and published. Put together, a list of dictionaries saved to a CSV file is not just a convenient trick: it is, structurally, a miniature database table. That is exactly the shape Module 8 turns into a real, queryable SQL database, so the phonebook you build today is not a toy: it is a rough draft of the north-star project you'll keep building toward for the rest of this course.

## Learning objectives

By the end of this lesson you will be able to:

1. Grow a Python list with `.append()` and summarize it with `len()` and `sum()`.
2. Look up a value in a dictionary by its string key, and build a **list of dictionaries** to model rows of a table (like a phonebook or a spreadsheet).
3. Use a `for...else` clause so a loop can report "not found" without a separate tracking variable.
4. Read command-line arguments with `sys.argv` and exit a program with a specific status code using `sys.exit()`.
5. Read and write CSV files safely with `with open(...)`, and write rows with both `csv.writer` and `csv.DictWriter`.
6. Install a third-party package with `pip` and import it into your own code, understanding what a `ModuleNotFoundError` is telling you.

## Prerequisites

- **Module 7 · Lesson 26: Loops, functions, and exceptions**: this lesson assumes you're comfortable with `for`/`while` loops, `def`, and `try`/`except`, all of which reappear here.
- **Module 6 · Lesson 23: Trees, hash tables, and tries**: helpful background, since a Python `dict` is essentially the hash table you already designed by hand, minus the work.
- A working cs50.dev codespace (Module 0: Pre-flight).

---

## Part 1: Lists (an array that grows itself)

Recall that a C array had a fixed size you had to decide up front, and no built-in way to ask "how big are you?": you had to carry that number around in a separate variable yourself. Python's **list** removes both restrictions. Malan reintroduces the running-average program from earlier in the course, now with a hardcoded list of three quiz scores:

```python
scores = [72, 73, 33]

average = sum(scores) / len(scores)

print(f"Average: {average}")
```

No loop, no manual addition, no manually tracked count. `sum()` adds every element together and `len()` reports how many there are: both are ordinary Python functions, not something you had to write yourself. Malan is explicit about why this matters:

> "...unlike arrays, you can ask lists how long they are, so you don't have to keep around a variable of how large an array is. You can just add stuff to a list and then ask Python how long is this list, how many elements are in it." (David Malan)

That "add stuff to a list" part is the real upgrade. A list doesn't have to start with values already in it. It can start empty and grow one value at a time, with the user typing each one in:

```python
scores = []

for _ in range(3):
    score = int(input("Score: "))
    scores.append(score)

average = sum(scores) / len(scores)
print(f"Average: {average}")
```

`scores.append(score)` is a **method** call: `.append()` belongs to the list itself, the same way `.lower()` belongs to a string. It adds one value to the end of the list and resizes it automatically: no `malloc`, no `realloc`, no manual bookkeeping of capacity. The underscore in `for _ in range(3)` is a small Python convention worth noting: when a loop variable is required by the syntax but you never actually use its value, it's idiomatic to name it `_` instead of `i`, as a signal to yourself and to anyone reading your code that it's intentionally unused.

> 🔑 **The single most important takeaway of this part.** A Python list is a dynamic array: Python manages its size for you. `.append()` grows it, `len()` reports its size, and `sum()` (for numeric lists) totals it, all without you writing a loop or tracking a counter by hand.

---

## Part 2: Dictionaries, list-of-dicts, and the `for...else` clause

### From a list of names to key-value lookup

Malan builds a phonebook in stages, and each stage teaches something new. The first version is just a list of names, searched with an ordinary loop:

```python
names = ["Kelly", "David", "John Harvard"]

name = input("Search: ")

for n in names:
    if name == n:
        print("Found")
        break
else:
    print("Not found")
```

That trailing `else`, attached to the `for` loop rather than to an `if`, is a Python feature with no equivalent in C. Malan explains what it does:

> "...if you get through this whole loop and you never call `break` ... you've not actually broken out of the loop, so you're going to hit the [else] and in that case you're going to print out not found ... [else] literally handles that scenario in Python." (David Malan)

(The raw transcript renders "else" as "ETS"/"ELTS", a speech-to-text quirk with that word, but the meaning is unambiguous from context: he means the loop's `else` clause.)

In plain terms: a `for...else` loop's `else` block runs only if the loop finishes every iteration **without** hitting `break`. Before Python, you would need a separate boolean variable (`found = False`, then `found = True` inside the loop, then check it afterward) just to remember whether you'd found anything. `for...else` removes that variable entirely.

Python can shrink this even further, because membership testing is itself built in:

```python
if name in names:
    print("Found")
else:
    print("Not found")
```

`in` silently does the same linear search a `for` loop would, and returns `True` or `False`. It works on any list, and (as you're about to see) it works on dictionaries too, just with a different meaning.

### From a list of names to a dictionary of names and numbers

A list only stores one column of data. A **dictionary** stores key-value pairs, exactly the two-column chart (name, number) you'd otherwise need a hash table for:

```python
people = {
    "Kelly": "+16174951000",
    "David": "+16174951000",
    "John Harvard": "+19494682750",
}

name = input("Search: ")

if name in people:
    number = people[name]
    print(f"Found: {number}")
else:
    print("Not found")
```

Here, `name in people` asks a different question than it did for a list: "is this **key** present?" And `people[name]` looks up the value for that key: square brackets, exactly like array indexing in C, except the index is a string instead of a number. Malan calls this out directly:

> "What's amazing about dictionaries, not just in Python but in other languages as well, you can now index into a dictionary just as you can index into an array, but whereas in array you use numeric indices. In dictionaries you use string indices. You can use strings to look up their corresponding value." (David Malan)

### From one dictionary to a list of dictionaries

A single dictionary only models one row. To model many rows (many people, each with a name and a number, the way a spreadsheet or a database table would), you nest dictionaries **inside** a list:

```python
people = [
    {"name": "Kelly", "number": "+16174951000"},
    {"name": "David", "number": "+16174951000"},
    {"name": "John Harvard", "number": "+19494682750"},
]

name = input("Search: ")

for person in people:
    if person["name"] == name:
        print(f"Found: {person['number']}")
        break
else:
    print("Not found")
```

Each `person` is one dictionary as you iterate; `person["name"]` and `person["number"]` read its two fields. This is precisely the shape spreadsheet software and database software use internally: a list of records, each record a set of named fields. Keep that picture in mind: it's exactly the shape your Capstone will build, and exactly the shape Module 8 replaces with a real SQL table.

> ✅ **What to do about it:** reach for a plain dictionary when you have one fixed record of named fields (one contact, one config). Reach for a list of dictionaries the moment you have *many* records that share the same fields (a phonebook, a roster, rows read from a file).

---

## Part 3: The `sys` module and reading/writing CSV files

### Command-line arguments and exit codes, without `main`

Dropping `int main(void)` also dropped `argc`/`argv`, but that functionality didn't disappear, it just moved into a library you now have to import explicitly: `sys`.

```python
from sys import argv

if len(argv) == 2:
    name = argv[1]
    print(f"Hello, {name}")
else:
    print("Hello, world")
```

`argv` is a list of the words typed at the command line, and `argv[0]` is always the script's own name. Malan clarifies exactly what gets counted:

> "...the only things that are being counted are the words after the Python interpreter itself." (David Malan)

So running `python greet.py David` gives you `argv == ["greet.py", "David"]`, and `len(argv) == 2`. You can also exit a program with a specific status code the same way you returned `0` or `1` from `main` in C, except now it's a function call from the `sys` library, `sys.exit()`:

```python
import sys

if len(sys.argv) != 2:
    print("Missing command-line argument")
    sys.exit(1)

print(f"Hello, {sys.argv[1]}")
sys.exit(0)
```

`sys.exit(1)` signals failure, `sys.exit(0)` signals success: the same convention `check50` and other automated tools rely on, just spelled differently than C's `return 1;` inside `main`.

### Writing a CSV file with `csv.writer`

Recall Module 5 · Lesson 20, where you persisted a phonebook to disk in C using `fopen`, `fprintf`, and manual comma-placement. Python's built-in `csv` module removes almost all of that ceremony:

```python
import csv

name = input("Name: ")
number = input("Number: ")

file = open("phonebook.csv", "a")
writer = csv.writer(file)
writer.writerow([name, number])
file.close()
```

`open("phonebook.csv", "a")` opens the file in **append mode**: new runs add rows rather than erasing old ones. `csv.writer(file)` wraps that open file so it knows how to format rows as proper CSV; `writer.writerow([...])` takes a list of values and writes them out, comma-separated, with a newline at the end, so you never have to type a comma yourself. As Malan puts it:

> "Write row is a method, aka function associated with this writer object, and I know that only because I did actually read the documentation for the CSV library." (David Malan)

That habit, reading the actual documentation for a library instead of guessing, is worth adopting for every new module you touch, not just this one.

### Letting Python close the file for you: `with open(...)`

Forgetting to call `file.close()` in C risked a memory or resource leak you'd only catch by running Valgrind. Python's `with` statement removes the risk by closing the file for you automatically, the moment its indented block ends:

```python
with open("phonebook.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow([name, number])
```

Malan draws the comparison to C directly:

> "This just helps us avoid ... stupid mistakes we've made in C because you forget to close a file that you have to open and you don't necessarily notice unless you run Valgrind or something on it." (David Malan)

`with` is Python's **context manager** syntax: "open the following file, run this indented code, then close the file for me, even if something goes wrong in between." You'll see this same pattern reused constantly, well beyond files.

### Writing self-describing rows with `csv.DictWriter`

A bare `csv.writer` assumes you'll always remember that column 0 is the name and column 1 is the number. That's fragile: if the columns ever get reordered, the code silently writes the wrong thing into the wrong place. `csv.DictWriter` fixes this by writing a header row and matching each value to a named field instead of a position:

```python
import csv

name = input("Name: ")
number = input("Number: ")

with open("phonebook.csv", "a") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "number"])
    writer.writerow({"name": name, "number": number})
```

`fieldnames=["name", "number"]` tells the writer what columns exist and in what order to write the header; `writerow({...})` then takes a dictionary, the same shape you already used for a single contact in Part 2, and places each value under its matching column, regardless of the order you list the keys in. (In practice you'd write the header line once, before your program starts appending, so it doesn't get duplicated on every run.)

> 🔑 **The single most important takeaway of this part.** `with open(...)` closes files for you automatically; `csv.writer` writes plain rows by position; `csv.DictWriter` writes self-describing rows by field name, using the exact same dictionary shape you already use to model one record in memory.

```text
list of dicts (in memory)              csv.DictWriter (on disk, phonebook.csv)
[{"name": "Kelly", "number": "..."},        name,number
 {"name": "David", "number": "..."},   -->   Kelly,+16174951000
 {"name": "John",  "number": "..."}]         David,+16174951000
                                              John,+19494682750
```

---

## Part 4: pip and the third-party ecosystem

### Modules, packages, and what pip actually does

Malan draws the vocabulary distinction early in this lecture:

> "Python uses somewhat different vernacular whereby Python has what are called modules and packages, and a package is just a collection of modules ... a module is just a library using Python Speak, so to speak." (David Malan)

Some modules (`sys`, `csv`) ship with Python itself; you still have to `import` them, but nothing needs installing. Others are **third-party**: written and published by someone else, and not present until you fetch them yourself. That's what `pip` is for:

> "You can use a program called PIP to install Python packages into your own code space ... if those libraries are freely available as open source online." (David Malan)

If you try to `import` a package that isn't installed yet, Python raises `ModuleNotFoundError`, exactly the situation Malan demonstrates on purpose with `cowsay` (a library that prints an ASCII-art cow saying whatever text you give it):

```python
import cowsay

cowsay.cow("This is CS50")
```

Running that before installing the package fails with `ModuleNotFoundError: No module named 'cowsay'`. The fix is a single terminal command:

```text
pip install cowsay
```

Once that finishes, the exact same `import cowsay` line above works: no code changes needed, because the library now actually exists in your project.

### Same idea, bigger payoff: text-to-speech and QR codes

Malan runs the same `pip install` pattern twice more, each time with a package that does something a beginner would never build from scratch in a single lecture. First, text-to-speech, on his own computer rather than cs50.dev (cloud codespaces are browser-based, so audio has nowhere to play):

```python
import pyttsx3

engine = pyttsx3.init()
engine.say("This is CS50")
engine.runAndWait()
```

Then, generating an actual scannable QR code image, the finale of the whole lecture:

```python
import qrcode

image = qrcode.make("https://www.youtube.com/watch?v=Rl0ludWTLxs")
image.save("qr.png")
```

`qrcode.make(...)` builds the code from whatever text or URL you give it, and `.save("qr.png")` writes it out as an actual image file you can open and scan with your phone. Neither `pyttsx3` nor `qrcode` comes with Python: both required a `pip install` first, exactly like `cowsay` did. The pattern never changes: `pip install <name>` once, then `import <name>` in your code, forever after.

> ✅ **What to do about it:** whenever you hit `ModuleNotFoundError`, resist the urge to rewrite your code around it. Check the spelling of the package name, run `pip install <name>`, and try the exact same `import` again.

Zoom out, and this lesson's three ideas are one pipeline: a **list of dictionaries** holds your data in memory, `csv.DictWriter` inside a `with` block makes that data survive a restart, and `pip` lets you reach past what you or Python's standard library provide, straight into code the rest of the world has already written. That combination (structured records, a durable file, and borrowed tools) is the entire shape of your Capstone below, and, not coincidentally, the entire shape of the north-star web app this course is building you toward.

---

## Key takeaways

1. **Lists are arrays that manage themselves.** `.append()` grows a list, `len()` reports its size, `sum()` totals it: no manual capacity tracking required.
2. **Dictionaries are hash tables you don't have to build.** Look up a value with a string key (`person["name"]`) instead of a numeric index; check for a key's presence with `in`.
3. **A list of dictionaries models a table.** One dictionary is one record (one row); a list of them is the whole table: the same shape a spreadsheet or a database uses.
4. **`for...else` reports "didn't find it" without an extra variable.** The `else` block runs only if the loop finishes without a `break`.
5. **`sys.argv` and `sys.exit()` replace `argc`/`argv` and `return` from `main`.** `argv[0]` is always the script's own name.
6. **`with open(...)` closes files automatically**, the way you always meant to in C but sometimes forgot.
7. **`csv.writer` writes rows by position; `csv.DictWriter` writes rows by field name**, using a header row so column order can never silently get scrambled.
8. **`pip install <package>` turns a `ModuleNotFoundError` into a working `import`.** The exact same two-step pattern (install once, then import) works for every third-party package, whether it prints a cow or generates a QR code.

## Common pitfalls

- ❌ Assuming `name in some_dict` checks the *values*: it checks the **keys**. Looking for a phone number this way will always come back `False`, even if that number exists as a value somewhere in the dictionary.
- ❌ Opening a CSV file with mode `"w"` instead of `"a"`: `"w"` truncates the file and erases every previous row before writing the new one. Use `"a"` to append.
- ❌ Passing a plain list to `csv.DictWriter.writerow()`, or a dictionary to `csv.writer.writerow()`: each writer expects its own shape, and mixing them raises an error or silently writes garbage columns.
- ❌ Forgetting that `for...else`'s `else` runs when the loop completes *without* `break`: it is easy to misread it as running every time the loop finishes, `break` or not.
- ❌ Mistyping a package name in `pip install` (or forgetting to run it at all) and then debugging your own code for several minutes before rereading the `ModuleNotFoundError` message, which already named the exact missing module.

---

## 🛠️ Capstone Project: Persistent Phonebook + QR Code Finale

> This is the main hands-on project for the lesson. You'll build a phonebook that stores real contacts as a list of dictionaries, prove that it survives being closed and reopened by saving it to a CSV file, and finish by installing a package you've never used before to generate your own scannable QR code. Build it on **cs50.dev**.

### What you will build

Two small Python programs:

1. **`phonebook.py`**: lets you add a contact (name and number) to an in-memory list of dictionaries, look up a contact by name, and saves every contact to `phonebook.csv` with `csv.DictWriter` so the phonebook is still there the next time you run the program.
2. **`qr.py`**: installs and uses the third-party `qrcode` package to generate a QR code image linking to anything you like.

### Why this is the perfect practice

| Lesson idea | Where you use it in this Capstone |
|---|---|
| Lists with `.append()` | Growing your in-memory list of contacts one `add` at a time. |
| Dictionaries + list of dicts | Each contact is a `{"name": ..., "number": ...}` dictionary, stored in a list. |
| `for...else` | Reporting "not found" for a lookup only when the loop finishes without a `break`. |
| `with open(...)` + `csv.DictWriter` | Appending one self-describing row per contact to `phonebook.csv`. |
| Reading a file back with plain string methods | Reloading existing contacts from `phonebook.csv` when the program starts. |
| `pip install` | Installing `qrcode` (and, if you like, `cowsay` or `pyttsx3`) into your codespace. |
| `sys.argv` / `sys.exit()` | Stretch goal: a command-line lookup mode with a proper exit status. |

### Milestones (build them in order, each one works on its own)

1. **In-memory add and lookup.** Write `phonebook.py` with `contacts = []`. Let the user type `add` to append a `{"name": ..., "number": ...}` dictionary to `contacts`, or `search` to look up a name using a `for...else` loop that prints the number if found and `"Not found"` otherwise. Smallest working version: it works correctly for one program run, even though everything disappears when you quit.
2. **Persist every add to CSV.** Inside your `add` flow, open `phonebook.csv` in append mode with `with open("phonebook.csv", "a") as file:` and write each new contact with `csv.DictWriter(file, fieldnames=["name", "number"])`. Write the header row (`name,number`) once, by hand, the first time you create the file. Add two or three contacts and confirm the rows appear correctly in `phonebook.csv`.
3. **Reload contacts on startup.** Before your program does anything else, check whether `phonebook.csv` already exists and, if it does, read it back into `contacts` so your phonebook survives quitting and rerunning the program. Because you haven't learned `csv.reader` yet (Module 8 · Lesson 28 covers that), do it the plain way: read the file's lines, skip the header row, and split each remaining line on the comma yourself. For example:
   ```python
   contacts = []
   try:
       with open("phonebook.csv", "r") as file:
           rows = file.read().splitlines()
       for row in rows[1:]:  # skip the header row
           name, number = row.split(",")
           contacts.append({"name": name, "number": number})
   except FileNotFoundError:
       pass  # no file yet: start with an empty phonebook
   ```
4. **Generate a QR code.** In a separate file, `qr.py`, run `pip install qrcode` in your terminal, then write three lines: `import qrcode`, `image = qrcode.make("...")` with any URL or text you like, and `image.save("qr.png")`. Open `qr.png` and scan it with your phone to confirm it works.
5. **Stretch goal: command-line lookup.** Modify `phonebook.py` so that running `python phonebook.py David` looks up `David` immediately using `sys.argv`, instead of prompting interactively. If the user gives the wrong number of arguments, print a usage message and `sys.exit(1)`.
6. **Stretch goal: give your phonebook a voice.** `pip install cowsay` (or `pyttsx3`, if you're running Python on your own computer rather than cs50.dev) and have your program print (or speak) "Contact added" whenever `add` succeeds.

### How you will know you are done

- ✅ Adding a contact, quitting the program, and rerunning it still shows that contact when you search, proving persistence actually works, not just appending.
- ✅ Searching for a name that doesn't exist prints "Not found" using a `for...else` loop, with no extra tracking variable.
- ✅ `phonebook.csv` opens correctly in a spreadsheet app, with a `name,number` header row followed by one row per contact.
- ✅ `pip install qrcode` completed without errors, and `qr.png` opens as a real, scannable QR code linking to something you chose.
- ✅ You can explain, in one sentence, why a list of dictionaries already looks like a spreadsheet or a database table.

> 💡 **Keep yourself honest:** delete `phonebook.csv` once and rerun your program from a clean slate. If it still works correctly with an empty file, you've actually tested "reload on start", not just "append to a file that already had data in it."

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Grade calculator (foundational)
Write a program that starts with `scores = []`, asks the user for 5 quiz scores one at a time using `input()` and `int()`, appending each one with `.append()`. Then print the total (`sum()`), the count (`len()`), and the average, using an f-string.

### Exercise 2: Contact card lookup (intermediate)
Build a list of dictionaries for at least three friends, each with `"name"` and `"email"` keys. Ask the user for a name and, using a `for...else` loop (not the `in` shortcut), print that person's email if found, or `"Not found"` otherwise.

### Exercise 3: Command-line greeter with exit codes (advanced)
Write `greet.py` using `sys.argv` and `sys.exit()`. If the user runs it with exactly one command-line argument, print `Hello, <name>`. If they run it with any other number of arguments, print a usage message like `Usage: python greet.py NAME` and exit with status `1`. Test both cases from the terminal.

---

## Cheat sheet

```text
LISTS
  scores = []                          start empty
  scores.append(72)                    add to the end
  len(scores)                          how many elements
  sum(scores)                          add every element together (numeric lists)
  value in some_list                    True/False membership test

DICTIONARIES
  person = {"name": "David", "number": "+16174951000"}
  person["name"]                       look up by string key -> "David"
  "name" in person                      True/False: is this KEY present?
  people = [ {...}, {...}, {...} ]      list of dicts = one row per record (a table!)

FOR...ELSE
  for item in some_list:
      if item == target:
          print("found")
          break
  else:
      print("not found")               runs ONLY if the loop finished without break

SYS MODULE
  import sys
  sys.argv                             list of command-line words; argv[0] is the script name
  len(sys.argv)                        how many words were typed (script name included)
  sys.exit(0)                          exit, success
  sys.exit(1)                          exit, error

CSV FILES
  import csv
  with open("phonebook.csv", "a") as file:
      writer = csv.writer(file)
      writer.writerow(["David", "+16174951000"])

  with open("phonebook.csv", "a") as file:
      writer = csv.DictWriter(file, fieldnames=["name", "number"])
      writer.writerow({"name": "David", "number": "+16174951000"})

PIP
  pip install cowsay                   installs a third-party package into THIS project
  import cowsay                        then import and use it like any built-in module
  cowsay.cow("hi")
```

## How this connects to the rest of the course

- **Earlier, Module 7 · Lesson 26:** the `for`/`while` loops and `try`/`except` you learned there are exactly what this lesson's `for...else` and file-handling build on.
- **Earlier, Module 6 · Lesson 23:** you hand-built a hash table in C; this lesson's `dict` is Python doing that same job for you, and Malan says so directly when he calls dictionaries "the Swiss Army knives of data structures."
- **Earlier, Module 5 · Lesson 20:** you hand-wrote a `phonebook.csv` in C with `fopen`/`fprintf`, character by character; this lesson does the same job in a fraction of the code with `csv.DictWriter` and `with open(...)`.
- **Next, Module 8 · Lesson 28:** "From flat files to Python dictionaries" picks up this exact `phonebook.csv` thread and teaches `csv.reader`/`csv.DictReader`: the proper replacement for the brute-force reload you built by hand in the Capstone.
- **Later, Module 8:** SQL fundamentals replace "list of dicts held in memory, backed by a CSV file" with a real, persistent, queryable database: the list of dicts you built today is a database table in miniature.

---

*Source: "CS50x 2026 - Lecture 6 - Python" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
