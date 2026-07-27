# Module 8 · Lesson 28: From Flat Files to Python Dictionaries

> **Course:** Self-Paced CS50x
> **Module 8:** SQL and databases: store data properly and query it declaratively
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 7 - SQL](https://www.youtube.com/watch?v=oqRU2So6Z2Y) · [full transcript](../../transcripts/09-lecture-7-sql.txt)
> **Estimated time:** 45 minutes (read plus exercises)

---

## In one sentence

Before you ever type a line of SQL, you'll feel exactly why it exists: pull a real class poll out of Google Forms as a CSV file, parse it in Python with `csv.reader` and `csv.DictReader`, and watch a simple "how many people said X?" question drag you through a header-row bug, a stateful reader, and a `KeyError`: the exact pain that next lesson's one-line SQL query erases.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *The Favorites Tally*, where you hand-build a small CSV file and write a Python script that counts categories in it safely, two different ways, and prints a sorted popularity report. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Google Forms and VS Code will change; the file format underneath them will not. For the timeless, tool-agnostic version of what you're parsing:
>
> - **[RFC 4180: Common Format and MIME Type for Comma-Separated Values (CSV) Files](https://www.rfc-editor.org/rfc/rfc4180)** (IETF, 2005). This is the closest thing to an official specification of the CSV format Malan downloads from Google Sheets: it defines, precisely and independent of any programming language, why commas separate columns, why newlines separate rows, and how quoting escapes a comma that appears inside a value. Python's `csv` module is one implementation of this spec, so you never have to write that parsing logic yourself.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Procedural programming language:** a language where you tell the computer *how* to solve a problem, step by step: loops, conditionals, variables, in an order you write out yourself. C and Python (mostly) work this way.
- **Declarative programming language:** a language where you tell the computer *what* answer you want, and it figures out the steps for you. SQL, which you'll meet next lesson, works this way.
- **Flat file (database):** a plain text file that stores data in rows, with no fancy structure underneath: "flat" because it's just lines of text, not a real database program. A CSV file is a flat file.
- **CSV (comma-separated values):** a simple way of storing tabular data (rows and columns) as plain text, where a comma marks the boundary between one column's value and the next.
- **Parsing:** the process of reading raw text and pulling structured meaning out of it: for example, turning a line of comma-separated text into a list of separate values.
- **Stateful:** something that remembers information between one use and the next. A stateful CSV reader remembers which row it read last, so the next time you ask it for a row, it gives you the *next* one, not the same one again.
- **`DictReader`:** a tool in Python's `csv` library that hands you each row as a dictionary (keyed by column name) instead of a list (indexed by position).
- **`KeyError`:** the error Python raises when you try to look up a dictionary key that doesn't exist yet.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In **Module 7 · Lesson 27 ("Lists, dictionaries, and the pip ecosystem")** you learned to store data in lists and dictionaries and to read a CSV file in Python. This lesson takes that exact toolkit and stress-tests it with a real, messy, live data set (a poll of an actual lecture hall) until it starts to hurt. That hurt is deliberate. As Malan frames the whole lecture before writing a single line of code:

> "SQL is said to be a declarative programming language, which is a different sort of paradigm whereby when you want to solve some problem you essentially declare what problem you want to solve or you declare what question you have, and it's up to the programming language to figure out using loops and conditionals and all of those lower level building blocks, how to get you the answer." (David Malan)

You cannot appreciate *why* that matters until you've personally written the procedural version and felt its rough edges: the header row sneaking into your output, a reader that silently remembers where it left off, and a `KeyError` on the very first row of data. That is exactly what this lesson puts you through, on purpose. Next lesson, every one of today's headaches disappears into a single `SELECT` statement, and this course's north-star project (a database-backed web app) will lean on SQL, not hand-rolled CSV parsing, for exactly that reason.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the difference between a procedural and a declarative programming language, and say which category C, Python, and SQL each fall into.
2. Describe how a live Google Form becomes a downloadable CSV file, and explain what makes a CSV a "flat file database."
3. Parse a CSV file in Python with `csv.reader`, explain the header-row bug it produces by default, and explain what it means for the reader to be "stateful."
4. Rewrite a `csv.reader` loop to use `csv.DictReader` instead, and explain why indexing a row by column name is more robust than indexing it by position.
5. Tally category counts into a dictionary safely, fixing the resulting `KeyError` two different ways: with an `in` check and with `try`/`except`.

## Prerequisites

- **Module 7 · Lesson 26: Loops, functions, and exceptions**: you'll reuse `try`/`except` here to handle a real error instead of a made-up one.
- **Module 7 · Lesson 27: Lists, dictionaries, and the pip ecosystem**: you should already be comfortable with dictionaries and a first pass at reading a CSV file in Python; this lesson pushes that same toolkit until it strains.
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**).

---

## Part 1: Two kinds of languages (procedural vs. declarative)

Every language you've used so far in this course (Scratch, C, Python) is what's called a **procedural programming language**. You write a *procedure*: a step-by-step recipe of loops, conditionals, and variables that tells the computer exactly how to get from input to output. Malan puts it this way:

> "C very much so and Python to a large extent are very much procedural programming languages whereby you have to write these procedures, functions step by step that tell the computer what to do, including loops and conditionals and all of that." (David Malan)

SQL, which you'll start writing next lesson, is different in kind, not just in syntax. It is a **declarative programming language**:

> "SQL is said to be a declarative programming language, which is a different sort of paradigm whereby when you want to solve some problem you essentially declare what problem you want to solve or you declare what question you have, and it's up to the programming language to figure out using loops and conditionals and all of those lower level building blocks, how to get you the answer." (David Malan)

| | Procedural (C, Python) | Declarative (SQL) |
|---|---|---|
| What you write | The steps: open the file, loop over it, check each row, update a variable | The question: "how many people picked each language?" |
| Who figures out the "how" | You do, line by line | The database engine does, underneath your one statement |
| What this lesson uses | Python: `csv.reader`, `csv.DictReader`, dictionaries, loops | (Preview only, SQL itself starts next lesson) |

You won't write any SQL in this lesson. Instead, you're going to write the *procedural* version of a simple counting problem, by hand, so that the declarative version next lesson lands as a relief instead of an abstraction.

> 🔑 **The single most important takeaway of this part.** Procedural code tells the computer *how*; declarative code tells it *what*. This whole lesson is procedural code getting steadily more annoying, on purpose, so that "what" feels like the obvious upgrade next lesson.

---

## Part 2: From a live poll to a CSV file

To get real data to work with, Malan's class answered a live poll: a Google Form asking "which is your favorite language?" and "which is your favorite problem?" among the ones studied so far. As responses came in, Google Forms displayed live pie charts, but the more interesting question for this lesson is not the answer, it's **how to get at the raw data** underneath that chart.

Google ties its Forms and Sheets products together, so from the form you can click "View in Sheets" to see the underlying spreadsheet, then download it as a plain data file. Malan chose the simplest, most universal option:

> "For Today we're going to download it in a very common format known as CSV for separated values... this is perhaps the most straightforward, easiest way to get raw data out of any kind of tabular data like this to load it into code that we are about to write." (David Malan)

The result, after renaming the long default filename to `favorites.csv`, is what Malan calls a **flat file database**:

> "It's a very lightweight database in the sense that it stores a lot of data, and it's a flat file in the sense that it's literally just a text file." (David Malan)

Opened in a text editor, it looks like this (three columns: a timestamp, the chosen language, and the chosen problem, separated by commas):

```text
timestamp,language,problem
2026/07/26 1:29:57 PM EST,Python,Hello, World
2026/07/26 1:30:04 PM EST,C,Hello, World
2026/07/26 1:30:11 PM EST,Scratch,Mario
```

Every value before the first comma is the timestamp; everything between the 1st and 2nd comma is the language; everything after the 2nd comma is the problem. The rows are "jagged" (some answers are longer than others), but the commas alone are enough to tell code where one column ends and the next begins. CSV isn't the only such convention: **TSV** (tab-separated values) and **PSV** (pipe-separated values) exist too. They all just pick a character unlikely to appear inside the actual data, and use it to separate columns.

> 🔑 **The single most important takeaway of this part.** A CSV file is nothing more than a plain text file where commas mark column boundaries and newlines mark row boundaries: no software required to create one, and no software required to open one, which is exactly why it's the universal "escape hatch" out of Google Sheets, Excel, or Apple Numbers.

---

## Part 3: Parsing the CSV in Python (the header bug and the stateful reader)

Rather than writing a comma-splitting parser from scratch, Python ships with a `csv` library that already knows how to do this. Malan's first version of `favorites.py`:

```python
import csv

with open("favorites.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row[1])
```

`csv.reader` takes an already-opened file and, on each pass of the loop, hands back one row as a **list**: `row[0]` is the first column, `row[1]` the second, and so on, because Python lists are zero-indexed. Running this prints every language selected, from top to bottom, almost. Scrolling to the very first line of output reveals a bug:

> "Yeah, it accidentally includes the header, which is a bug in the sense that I really just wanted to see the languages, but the code is doing what I told it to, which is just print out every row." (David Malan)

The very first "row" the reader hands back is the header row itself: the literal word `language`, not anyone's answer. The fix is to explicitly throw away the first row before the loop starts:

```python
import csv

with open("favorites.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip the header row
    for row in reader:
        favorite = row[1]
        print(favorite)
```

Calling `next(reader)` once, before the loop, consumes the header row and advances the reader past it. That this even works, that asking the reader for "the next row" a second time gives you a *different* row instead of the same one, reveals something about how the reader behaves:

> "This reader is stateful in some sense, and this was actually true of all of the file IO... something was remembering where it was in the file so that you didn't get the same bytes again and again and again. It was more like a cassette tape, an old school cassette tape if you will... and something inside of the computer's memory remembers where it is." (David Malan)

That's what **stateful** means here: the reader silently keeps track of its position in the file between calls, the way a cassette tape (or a video's scrubber bar) remembers where playback left off. `next(reader)` moves that position forward by exactly one row.

Indexing by position (`row[1]`) has a hidden fragility, though: if someone reorders the CSV's columns (say, by dragging one to a different spot in a spreadsheet app), `row[1]` silently starts meaning something else. That's the motivation for `csv.DictReader`, covered next.

> ✅ **What to do about it:** whenever you use `csv.reader` on a file that has a header row, call `next(reader)` once before your loop to consume that header: otherwise your first "row" of data is actually just the column names.

---

## Part 4: DictReader and counting (from three variables to a dictionary, and the KeyError)

Switching `csv.reader` to `csv.DictReader` changes what each row looks like. Instead of a list indexed by position, each row becomes a **dictionary**, a collection of key-value pairs, keyed by the actual column names from the header row:

```python
import csv

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        favorite = row["language"]
        print(favorite)
```

Notice there's no `next(reader)` call anymore: `DictReader` automatically consumes the header row itself, because it needs those names to build each row's dictionary keys. And now `row["language"]` will keep meaning "the language column" even if someone reorders the file's columns later. That's what makes `DictReader` more **robust** than plain `reader`.

Printing every answer is a start, but the real question is: *how many* people picked each language? Malan's first attempt uses one variable per language:

```python
scratch, c, python = 0, 0, 0

for row in reader:
    favorite = row["language"]
    if favorite == "Scratch":
        scratch += 1
    elif favorite == "C":
        c += 1
    elif favorite == "Python":
        python += 1

print(f"Scratch count: {scratch}")
print(f"C count: {c}")
print(f"Python count: {python}")
```

This works (the class's real poll came back roughly 190 Python, 58 C, 24 Scratch), but Malan is quick to point out why it's a bad design:

> "If we were to add a bunch more languages, a 4th 1, a 5th 1, a 6th 1, a 10th 1, a 20th 1, like having that many variables, it's just certainly going to look unwieldy... it shouldn't rub you the right way." (David Malan)

The fix is the dictionary you already know from Lesson 27: one variable, `counts`, whose keys are the languages and whose values are the running totals.

```python
counts = {}

for row in reader:
    favorite = row["language"]
    counts[favorite] += 1
```

This looks reasonable, but it crashes on the very first row, with a `KeyError`. Why?

> "If this is like the very first time through the file, there is no key Python. There is no key C or scratch because no one has put them there and yet recall that plus equal means you're going to that location in the dictionary and just blindly incrementing it." (David Malan)

`counts[favorite] += 1` means "go to `counts[favorite]`, read whatever number is there, add 1, and store it back," but the very first time a language shows up, there is nothing there yet to read. Malan shows two ways to fix it. The first checks whether the key exists before touching it:

```python
counts = {}

for row in reader:
    favorite = row["language"]
    if favorite in counts:
        counts[favorite] += 1
    else:
        counts[favorite] = 1
```

A slightly different way to say the same thing: always guarantee the key exists first, then increment it unconditionally:

```python
counts = {}

for row in reader:
    favorite = row["language"]
    if favorite not in counts:
        counts[favorite] = 0
    counts[favorite] += 1
```

The second fix leans on exception handling instead of checking in advance, the same `try`/`except` pattern from Lesson 26:

> "Whenever you have these kinds of trace backs that refer to certain exceptions... you can also change your code to just try to do something and then try to catch the exception instead... Try to do that please, except if there is a key error, in which case, you know what, go ahead and just initialize that value to one instead." (David Malan)

```python
counts = {}

for row in reader:
    favorite = row["language"]
    try:
        counts[favorite] += 1
    except KeyError:
        counts[favorite] = 1
```

All three versions produce the same counts. Finally, printing the tally is just a loop over the dictionary's keys:

```python
for favorite in counts:
    print(favorite, counts[favorite])
```

By this point, Malan has written roughly 20 lines of Python just to answer "what's the most popular language?", and he says so out loud, as a deliberate cliffhanger:

> "Writing this amount of code is kind of annoying just to ask a relatively simple question like what's the most popular language in this file... it's starting to feel like with almost 20 lines of code like maybe. There's a better way." (David Malan)

That "better way" is SQL, and it starts next lesson.

> 🔑 **The single most important takeaway of this part.** A `KeyError` on a dictionary almost always means "I assumed this key already existed." Guard against it either by checking first (`if key in dict`) or by attempting the operation and catching the failure (`try`/`except KeyError`): both are equally "Pythonic," and you'll see both patterns in real code.

---

## Key takeaways

1. **Procedural vs. declarative.** C and Python make you spell out *how* to solve a problem, step by step; SQL (starting next lesson) lets you declare *what* answer you want and leaves the "how" to the database.
2. **CSV is a flat file database.** It's plain text, comma-separated, with no software required to create or read it, which is exactly why it's the universal export format from Google Sheets, Excel, and Apple Numbers.
3. **`csv.reader` is stateful and header-blind.** It remembers where it is in the file between calls, but it will hand you the header row as if it were data unless you call `next(reader)` first.
4. **`csv.DictReader` is more robust.** It keys each row by column name instead of position, so reordering the file's columns doesn't silently break your code, and it consumes the header row automatically.
5. **A `KeyError` on `dict[key] += 1` means the key isn't there yet.** Fix it with an `if key in dict` check or a `try`/`except KeyError` block: both are legitimate, and both show up constantly in real Python code.

## Common pitfalls

- ❌ Using `csv.reader` on a file with a header row and forgetting `next(reader)`: your first "row" of data will actually be the column names.
- ❌ Calling `next(reader)` *again* after switching to `csv.DictReader`: `DictReader` already consumes the header row itself, so an extra `next()` call will silently skip the first real row of data.
- ❌ Indexing a `csv.reader` row by position (`row[1]`) and assuming that position will always mean the same column: it won't, if the source file's columns ever get reordered.
- ❌ Writing `counts[favorite] += 1` on a fresh dictionary without a guard: this raises `KeyError` the first time any given key appears.
- ❌ Reaching for a pile of separate variables (`scratch`, `c`, `python`, ...) instead of one dictionary the moment you have more than a couple of categories to count.

---

## 🛠️ Capstone Project: The Favorites Tally

> This is the main hands-on project for the lesson. You'll hand-build a tiny CSV file, then write a Python script that parses it with `DictReader` and tallies category counts safely, both ways, before printing a sorted popularity report. This is the same file-parsing muscle you'd reach for before your future Flask project ever touches a real database.

### What you will build

A `favorites.csv` file you write by hand on cs50.dev, and a `tally.py` script that reads it with `csv.DictReader`, counts how many rows fall into each category, and prints the categories from most to least popular. Its pieces:

- A small hand-made CSV file with a header row and at least 10 data rows.
- A `DictReader`-based loop that prints each row's category, proving the parsing works.
- A `counts` dictionary built with the `in`-check pattern.
- The same counting logic rebuilt with `try`/`except KeyError` instead, to prove both patterns give identical results.
- A sorted popularity report, most popular category first.

### Why this is the perfect practice

| Lesson idea | Where you use it in The Favorites Tally |
|---|---|
| CSV as a flat file (Part 2) | Milestone 1: you hand-write the exact kind of file Google Sheets would have exported. |
| `csv.reader`/header handling (Part 3) | Milestone 2: using `DictReader` instead, you see firsthand why no `next()` call is needed. |
| Dictionary counting + `KeyError` fix #1 (Part 4) | Milestone 3: the `in`-check pattern. |
| Dictionary counting + `KeyError` fix #2 (Part 4) | Milestone 4: the `try`/`except` pattern. |
| "20 lines of code... maybe there's a better way" (Part 4) | Milestone 5: sorting a dictionary by value is exactly the kind of question that feels tedious here and effortless in SQL next lesson. |

### Milestones (build them in order, each one works on its own)

1. **Hand-build `favorites.csv`.** On cs50.dev, create `favorites.csv` with a header row `name,category` and at least 10 data rows of your own choosing (movie genres, ice cream flavors, anything with repeating categories works). Make sure at least three different categories appear, and that at least one category appears more than once.
2. **Parse it and print each category.** Write `tally.py`. Open the file, create a `csv.DictReader` over it, and loop over the rows printing `row["category"]` for each one. Confirm you see every row's category and nothing extra (no header row leaking through).
3. **Count safely with an `in` check.** Add a `counts = {}` dictionary. Inside the loop, use `if category in counts: ... else: ...` to increment the count for each category without ever raising a `KeyError`. Print the dictionary at the end and confirm the numbers match the rows in your file.
4. **Count safely with `try`/`except` instead.** Duplicate the script (or comment out the `in`-check version) and rebuild the exact same counting logic using `try: counts[category] += 1 except KeyError: counts[category] = 1`. Run both versions and confirm they produce identical counts.
5. **Print a sorted popularity report.** Using whichever counting version you prefer, print the categories from most popular to least, using `sorted(counts, key=counts.get, reverse=True)` to control the order, with an f-string like `f"{category}: {count}"` for each line.
6. **Stretch goals.** Add a row to your CSV with a category you haven't seen before and confirm your script still works without changes. Then try deliberately reordering the CSV's columns (`category,name` instead of `name,category`) and confirm your `DictReader`-based script still works unchanged, because it looks up columns by name, not position.

### How you will know you are done

- ✅ `favorites.csv` has a header row, at least 10 data rows, and at least one repeated category.
- ✅ Both counting versions (`in`-check and `try`/`except`) run without error and print identical counts for every category.
- ✅ Your final printed report is sorted from the most popular category to the least popular.
- ✅ You can explain, out loud, in one sentence, why `csv.DictReader` didn't need a `next(reader)` call the way plain `csv.reader` did.

> 💡 **Keep yourself honest:** don't peek at the code snippets above before you've tried writing your own `in`-check version from just the description in Milestone 3: the value of this capstone is in hitting the `KeyError` yourself first, the same way Malan's class did.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Reproduce the header bug on purpose (foundational)
Write a three-line CSV file with a header row and two data rows. Parse it with plain `csv.reader` (no `next(reader)` call) and print `row[0]` for every row. Confirm the very first thing printed is the header text itself, not real data, then add `next(reader)` and confirm the header disappears from the output.

### Exercise 2: Trigger and fix a real KeyError (intermediate)
Write a five-line loop that builds a `counts` dictionary from a short hand-typed list of words (no CSV needed, a Python list of strings is fine) using `counts[word] += 1` with no guard. Run it, read the actual `KeyError` traceback Python prints, and note which word and which line triggered it. Then fix it using the `if word in counts` pattern from Part 4.

### Exercise 3: Position vs. name (advanced)
Take the `favorites.csv` file from the Capstone and duplicate it with its two columns swapped (`category,name` instead of `name,category`). Run a `csv.reader`-based script that indexes by position (`row[0]` assuming it's the name) against both files and observe it silently produce wrong answers on the swapped file. Then run a `csv.DictReader`-based script that indexes by column name (`row["name"]`) against both files and confirm it gives correct answers on both, unchanged.

---

## Cheat sheet

```text
PARADIGMS
  Procedural (C, Python)   -> you write the steps: loops, conditionals, variables
  Declarative (SQL, next!) -> you write the question; the engine finds the steps

CSV = flat file database: plain text, comma-separated columns, newline-separated rows

CSV.READER (list-based, position-indexed)
  import csv
  with open("file.csv", "r") as file:
      reader = csv.reader(file)
      next(reader)          # REQUIRED: skip the header row, or it prints as data
      for row in reader:
          row[0], row[1], ...   # position-indexed -> fragile if columns get reordered

CSV.DICTREADER (dict-based, name-indexed)
  with open("file.csv", "r") as file:
      reader = csv.DictReader(file)   # header row consumed automatically -- no next()
      for row in reader:
          row["column_name"]          # name-indexed -> robust to reordering

COUNTING SAFELY (avoid KeyError on dict[key] += 1)
  Option A (check first):     if key in counts: counts[key] += 1
                               else: counts[key] = 1
  Option B (try/except):      try: counts[key] += 1
                               except KeyError: counts[key] = 1

SORT A DICTIONARY BY VALUE, DESCENDING
  sorted(counts, key=counts.get, reverse=True)

STATEFUL = remembers its position between calls (like a cassette tape / video scrubber)
```

## How this connects to the rest of the course

- **Earlier, Module 7 · Lesson 27:** "Lists, dictionaries, and the pip ecosystem" gave you the dictionaries and first CSV-reading skills this lesson deliberately stress-tests until they hurt.
- **Next, Module 8 · Lesson 29:** "SQL fundamentals: CRUD" turns every headache from this lesson (skipping the header, guessing column order, guarding against `KeyError`) into a single declarative line: `SELECT language, COUNT(*) FROM favorites GROUP BY language;`.
- **Later, Module 8 · Lessons 30-31:** relational design, joins, indexes, and calling SQL safely from Python all build on this same `favorites` data set, and on the parsing instincts you built here.

---

*Source: "CS50x 2026 - Lecture 7 - SQL" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
