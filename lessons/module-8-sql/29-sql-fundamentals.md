# Module 8 · Lesson 29: SQL Fundamentals: CRUD

> **Course:** Self-Paced CS50x
> **Module 8:** SQL and databases: store data properly and query it declaratively
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 7 - SQL](https://www.youtube.com/watch?v=oqRU2So6Z2Y) · [full transcript](../../transcripts/09-lecture-7-sql.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

Instead of writing loops and dictionaries to parse a CSV file by hand, SQL lets you load that same data into a real database once and then get any answer you want (a count, a filter, a ranking, or a change) just by declaring the question, not the steps to answer it.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you rebuild last lesson's `favorites.csv` as a real SQLite database and interrogate it with SQL: answering five real questions, then practicing every write operation (insert, update, delete) safely. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** SQLite, MySQL, and Postgres will keep changing, but the idea underneath them is much older:
>
> - **[E. F. Codd, "A Relational Model of Data for Large Shared Data Banks"](https://dl.acm.org/doi/10.1145/362384.362685)** (*Communications of the ACM*, 1970). This paper introduced the relational model itself: representing data as tables of rows and columns with no built-in traversal order, and querying it by describing *what* you want rather than *how* to fetch it. Every SQL database you touch in this lesson (SQLite on your laptop, or IMDb's servers in Lesson 30) is an engineering descendant of the model Codd proposed years before the personal computer existed.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Database:** a piece of software, running somewhere on a computer, whose whole job is to store a lot of data and let you get at it reliably, as opposed to a plain text file that you have to parse yourself.
- **Table:** the database version of a spreadsheet tab: data arranged in **rows** (one record, like one form response) and **columns** (one field of that record, like "language").
- **Query:** a single instruction you send to a database asking it to read or change data. In SQL, a query is a sentence like "select the rows where the language is C."
- **CRUD:** an acronym for the four things you can do to data in a database: **C**reate, **R**ead, **U**pdate, **D**elete. Almost everything in SQL is one of these four.
- **Schema:** the design of a database: which tables exist, which columns each one has, and what type of data each column holds.
- **NULL:** SQL's way of saying "there is deliberately no value here." Not zero, not an empty string: the conscious absence of data.
- **Declarative language:** a language where you state *what* answer you want and let the software figure out *how* to compute it, as opposed to a **procedural language** (like C or Python) where you write out every loop and step yourself.
- **Wildcard:** a symbol that stands in for "anything." SQL actually uses two different ones for two different jobs. Watch for this, it trips everyone up at first.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In the last lesson you wrote a Python program that opened `favorites.csv`, looped over it row by row, and built up a dictionary just to answer one question: which language is most popular? It worked, but Malan calls out exactly why it doesn't feel right:

> "Writing this amount of code is kind of annoying just to ask a relatively simple question like what's the most popular language in this file." (David Malan)

That annoyance is the whole motivation for today. SQL is a genuinely different kind of language, **declarative** instead of **procedural**, and it comes with only four fundamental operations, CRUD, that cover essentially everything you'll ever need to do to stored data. Once your data lives in a real database, the twenty-line loop-and-dictionary program from last lesson collapses into a single line you can type at a prompt. This is also the first tool in this course that scales: the database-backed web app you'll design as this course's final project will store its data exactly this way, in tables you query with the commands you're about to learn.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the CRUD acronym and why a relational database replaces the flat-file-plus-dictionary pattern from the last lesson.
2. Load a CSV file into a brand-new SQLite database using `sqlite3`, `.mode csv`, and `.import`, then inspect its structure with `.schema`.
3. Write `SELECT` queries that choose specific columns, filter rows with `WHERE`, correctly escape a quote inside a string, and pattern-match text with `LIKE` and `%`.
4. Summarize data with `COUNT` and `DISTINCT`, and shape results with `GROUP BY`, `ORDER BY`, column aliases (`AS`), and `LIMIT`.
5. Modify a database's contents with `INSERT`, `UPDATE`, and `DELETE`, and explain why forgetting the `WHERE` clause on the last two is one of the most dangerous mistakes you can make.
6. Distinguish `DELETE` (removes rows) from `DROP TABLE` (removes the whole table), and `NULL` (deliberate absence of data) from an empty string or a zero.

## Prerequisites

- **Module 7 · Lesson 28: From flat files to Python dictionaries**: this lesson picks up with the exact `favorites.csv` file from that lesson, and directly replaces the loop-and-dictionary code you wrote to analyze it.
- Comfortable at a command line (`cd`, `ls`) from earlier modules, and a working cs50.dev codespace (Module 0: Pre-flight), where `sqlite3` is already installed for you.

---

## Part 1: CRUD, and why a "flat file" wasn't enough

Last lesson's `favorites.csv` was what Malan calls a **flat file database**:

> "A very lightweight database in the sense that it stores a lot of data, and it's a flat file in the sense that it's literally just a text file." (David Malan)

It works, but every question about it ("how many people picked Python?") meant writing a loop, a dictionary, and careful bookkeeping in Python yourself. C and Python are **procedural** languages: you tell the computer every step (open the file, loop over each row, check a condition, increment a counter). SQL is different in kind. It is a **declarative** language:

> "Select data means to read data from the database, and in this sense it's going to be a declarative language because I'm just going to declare what data I want to select from the database." (David Malan)

You state the question; the database decides how to loop, filter, and fetch. And however complicated your question gets, it always boils down to one of four operations. The acronym the whole industry uses is **CRUD**:

> "That is to say, when using a relational database, you can create data, read data, update the data, or delete data, and that's pretty comprehensive as to what's possible." (David Malan)

| Letter | Operation | SQL keyword |
|---|---|---|
| C | Create | `INSERT` |
| R | Read | `SELECT` |
| U | Update | `UPDATE` |
| D | Delete | `DELETE` (rows) or `DROP` (a whole table) |

Note the one naming oddity: the "R" in CRUD is called *read*, but the SQL keyword for it is `SELECT`, not "read." That's just vocabulary to memorize once.

The data itself moves into a **relational database**:

> "A relational database is simply data in which you define relations among your data." (David Malan)

For now, one table is enough to see the whole pattern; relationships *across* multiple tables (and why they matter) are Lesson 30's topic.

> 🔑 **The single most important takeaway of this part.** Every SQL statement you will ever write is one of four things: Create, Read, Update, or Delete, and SQL lets you *declare* the answer you want instead of writing the loop that computes it.

---

## Part 2: Setting up SQLite (from CSV to `favorites.db`)

CS50 uses **SQLite**, a lightweight, file-based version of SQL (the same engine used inside countless mobile and web apps) run from the command line as `sqlite3`. Bigger products (MySQL, Postgres, Oracle, SQL Server) add scale and features, but the core language you're about to learn is the same one they all speak.

To turn `favorites.csv` into a real database, you run three commands at a terminal:

```bash
sqlite3 favorites.db
```

This opens (or creates, if it doesn't exist) a database file called `favorites.db`. You're now inside SQLite's own interactive prompt. From here:

```sql
.mode csv
.import favorites.csv favorites
```

`.mode csv` tells SQLite "the next thing I import will be comma-separated." `.import favorites.csv favorites` reads that file and creates a table (named `favorites`, matching the file) with one column per CSV column.

> 💡 **A naming rule worth noticing immediately.** Any command that starts with a dot (`.mode`, `.import`, `.schema`, `.quit`) is specific to SQLite itself. Anything *without* a leading dot (`SELECT`, `INSERT`, `WHERE`) is standard SQL that works the same way on MySQL, Postgres, or any other SQL database in the world.

To see what `.import` actually built, run `.schema`:

```sql
.schema
```
```text
CREATE TABLE IF NOT EXISTS "favorites"(
  "timestamp" TEXT,
  "language" TEXT,
  "problem" TEXT
);
```

Three columns (`timestamp`, `language`, `problem`) all typed as plain text, because `.import` doesn't know any better than what it read from a CSV. (Lesson 30 shows how to declare more precise types and constraints yourself when creating a table by hand.)

One more thing worth knowing: if you try to open `favorites.db` in a text editor, it won't display as readable text: SQLite stores it as binary, not as commas and characters. That's normal, and it's part of why a real database can be faster and more capable than a CSV file at scale.

> ✅ **What to do about it:** whenever you're handed a CSV and a SQL prompt, your first three commands are almost always `sqlite3 <name>.db`, `.mode csv`, then `.import <file>.csv <table-name>`, followed immediately by `.schema` to confirm what you actually got.

---

## Part 3: `SELECT` basics (reading data your way)

With `favorites` loaded, you can start asking questions. The simplest is "show me everything":

```sql
SELECT * FROM favorites;
```

The `*` here is a **wildcard** meaning "all columns." If you only care about specific columns, name them instead:

```sql
SELECT language FROM favorites;
SELECT language, problem FROM favorites;
```

SQLite also ships with built-in functions, much like a spreadsheet's formulas. Two of the most useful:

```sql
SELECT COUNT(*) FROM favorites;                 -- 272 rows submitted
SELECT DISTINCT language FROM favorites;          -- unique languages seen
SELECT COUNT(DISTINCT language) FROM favorites;   -- how many distinct languages: 3
```

`COUNT(*)` counts rows; `DISTINCT` collapses duplicates so you see each unique value once. Combine them (`COUNT(DISTINCT ...)`) to count how many *unique* values exist.

To filter rows instead of just picking columns, add `WHERE`, logically similar to an `if` condition, but written inside the query itself:

```sql
SELECT COUNT(*) FROM favorites WHERE language = 'C';                         -- 58
SELECT COUNT(*) FROM favorites WHERE language = 'C' AND problem = 'hello world';  -- 5
```

Notice the single quotes around text values, and `AND` to combine conditions. You can stack as many as you need.

Now suppose the text itself contains an apostrophe, like the problem name "hello, it's me." A bare single quote there would confuse SQLite about where the string ends. The fix is to double it:

> "In SQLite what you instead do is doubly single quote it. So putting two single quotes is the convention for escaping a single quote." (David Malan)

```sql
SELECT COUNT(*) FROM favorites WHERE language = 'C' AND problem = 'hello, it''s me';
```

Finally, `LIKE` lets you match a *pattern* instead of an exact string, using `%` as its own wildcard:

> "In SQL you say percent sign to represent zero or more characters." (David Malan)

```sql
SELECT COUNT(*) FROM favorites WHERE language = 'C' AND problem LIKE 'hello%';
```

This matches "hello world," "hello, it's me," or anything else starting with "hello", in one query instead of an `OR`-ed list of exact strings.

> ❌ **The trap:** `*` and `%` are both called "wildcards," but they are not interchangeable. `*` only ever means "every column" and only appears right after `SELECT`. `%` only ever means "zero or more characters" and only appears inside a `LIKE` pattern string.

---

## Part 4: Shaping results (`GROUP BY`, `ORDER BY`, aliases, and `LIMIT`)

Counting one language at a time with repeated `WHERE` queries doesn't scale. `GROUP BY` answers "how many of each?" in a single line, clustering rows that share a value, then applying an aggregate function (like `COUNT`) to each cluster:

```sql
SELECT language, COUNT(*) FROM favorites GROUP BY language;
```

| language | COUNT(*) |
|---|---|
| C | 58 |
| Python | 190 |
| Scratch | 24 |

That's the same answer the loop-and-dictionary Python program worked twenty lines to produce, in one statement. To control the order the rows come back in, add `ORDER BY`:

```sql
SELECT language, COUNT(*) FROM favorites GROUP BY language ORDER BY COUNT(*) DESC;
```

Repeating `COUNT(*)` is a mouthful, so SQL supports **aliases**, a temporary name for a column, using `AS`:

```sql
SELECT language, COUNT(*) AS n FROM favorites GROUP BY language ORDER BY n DESC;
```

And if you only want the top result (or top few), `LIMIT` caps how many rows come back:

```sql
SELECT language, COUNT(*) AS n FROM favorites GROUP BY language ORDER BY n DESC LIMIT 1;
```
```text
Python | 190
```

One row, the answer to "what's the single most popular language?": Python, with 190 votes out of 272 responses. `LIMIT 3` instead of `LIMIT 1` would give you a top-3 ranking the same way.

> 🔑 **The single most important takeaway of this part.** Every `SELECT` returns a *temporary* table that exists only in the moment you ask for it: nothing is saved to disk just by reading it. `GROUP BY` clusters, `ORDER BY` sorts, `AS` renames, and `LIMIT` trims. Stack all four and you can turn raw rows into a ranked, readable answer in one line.

---

## Part 5: The rest of CRUD (`INSERT`, `NULL`, `DELETE`, `UPDATE`, `DROP`)

So far this lesson has only *read* data. The other three letters of CRUD change it.

**Create a row with `INSERT`:**

```sql
INSERT INTO favorites (language, problem) VALUES ('SQL', '50ville');
```

You name the table, the columns you're supplying values for (you can skip columns you don't have data for), then the matching values. Selecting the table afterward shows the new row, but the `timestamp` column, which you didn't supply, isn't blank. It's `NULL`:

> "There's our old friend null, which is not a null pointer, it's the same word, literally NULL, and it refers explicitly to the absence of data." (David Malan)

> "Null signifies the conscious omission of data. It's not just a missing value, it's consciously not there." (David Malan)

That distinction matters: `NULL` is not zero, and it is not an empty string `''`. It means *this cell deliberately has nothing in it*, and SQL gives you a special way to test for it: `IS NULL` (not `= NULL`, which never matches anything).

**Delete rows with `DELETE`**, always scoped by `WHERE`:

```sql
DELETE FROM favorites WHERE timestamp IS NULL;
```

This removes only the row(s) matching the condition. Now watch what happens without a `WHERE`:

> "Be very, very, very careful with delete statements." (David Malan)

```sql
DELETE FROM favorites;   -- DANGER: no WHERE means every row, gone
```

> "These are very destructive commands and just like in the real world if you don't have backups or versions of these same tables, the data can indeed be lost." (David Malan)

**Update rows with `UPDATE`**, which has exactly the same danger:

```sql
UPDATE favorites SET language = 'SQL', problem = '50ville' WHERE language = 'C';
```

Leave off the `WHERE` and every row in the table gets overwritten with the same values:

> "There is no going back to the previous version of the table unless I quit out of this and I import the whole CSV again." (David Malan)

**Drop a whole table with `DROP TABLE`**, which removes the table's structure entirely, not just its rows:

```sql
DROP TABLE favorites;
```

> "That's an even worse command to run unless you know and intend what you're doing." (David Malan)

> ❌ **The trap:** `DELETE FROM table;` and `UPDATE table SET ...;` are syntactically *valid* SQL with no `WHERE` at all: SQLite will not stop you. The only thing standing between "change one row" and "change every row in the table" is whether you remembered to type `WHERE`.

> ✅ **What to do about it:** before running any `UPDATE` or `DELETE`, run the exact same `WHERE` clause as a `SELECT` first, read back the rows it would touch, and only then swap `SELECT *` for `UPDATE`/`DELETE`.

---

## Part 6: How the pieces combine

Put together, this lesson's whole workflow looks like this:

```text
favorites.csv (flat file, from Lesson 28)
        │
        │  sqlite3 favorites.db
        │  .mode csv
        │  .import favorites.csv favorites
        ▼
favorites.db  →  table "favorites" (timestamp, language, problem)
        │
        │  SELECT ... WHERE ... GROUP BY ... ORDER BY ... AS ... LIMIT ...   -> Read
        │  INSERT INTO favorites (...) VALUES (...)                          -> Create
        │  UPDATE favorites SET ... WHERE ...                                -> Update
        │  DELETE FROM favorites WHERE ...                                   -> Delete
        ▼
   an answer (from SELECT), or a changed table (from the other three),
   never both, and never without a WHERE you already checked
```

Everything from here through the rest of the course, joining multiple tables (next lesson), and eventually a whole web app, is built on exactly this same small set of verbs.

---

## Key takeaways

1. **CRUD is the whole language.** Every SQL statement is one of four things: Create (`INSERT`), Read (`SELECT`), Update (`UPDATE`), or Delete (`DELETE`/`DROP`).
2. **SQL is declarative, not procedural.** You declare the question (`SELECT ... WHERE ...`); the database decides how to loop, filter, and fetch. No loop of your own required.
3. **`.mode csv` + `.import` turn a spreadsheet into a queryable table in two commands.** Dot-commands are SQLite-specific; everything without a leading dot is portable SQL.
4. **`COUNT`, `DISTINCT`, `WHERE`, and `LIKE '%...'` answer precise questions without a single loop**, and doubling a quote (`''`) is how you escape an apostrophe inside a string.
5. **`GROUP BY` + `ORDER BY` + `AS` + `LIMIT` turn raw rows into a ranked answer**, exactly what a spreadsheet's pie chart is doing behind the scenes.
6. **`NULL` means "consciously absent," never zero or blank**, and `DELETE`/`UPDATE` without `WHERE` are, in Malan's words, "very destructive" with no undo.

## Common pitfalls

- ❌ Forgetting the `WHERE` clause on `DELETE` or `UPDATE`: it will silently match every row, and there is no undo short of re-importing the original CSV.
- ❌ Confusing `*` (the column wildcard in `SELECT *`) with `%` (the pattern wildcard in `LIKE`): they look similar but do unrelated jobs.
- ❌ Writing a raw apostrophe inside a string literal (`'hello, it's me'`) instead of escaping it (`'hello, it''s me'`): SQLite reads the first quote as ending the string early.
- ❌ Testing for missing data with `WHERE column = NULL`: this never matches anything; the correct form is `WHERE column IS NULL`.
- ❌ Running `UPDATE`/`DELETE` straight away instead of first running the identical `WHERE` as a `SELECT` to confirm exactly which rows it will touch.

---

## 🛠️ Capstone Project: Query and Change Your Own Database

> This is the main hands-on project for the lesson. You will rebuild the exact `favorites.csv` from Lesson 28 as a real SQLite database, answer five genuine questions about it in SQL, and then practice every write operation (insert, update, delete) the safe way, always with `WHERE`. `favorites.db` is small, but it's the same relational pattern, a table queried and modified with SQL, that will sit underneath the database-backed web app you build as this course's final project.

### What you will build

A `favorites.db` SQLite database on cs50.dev, imported from your own `favorites.csv`, plus a running log of the SQL queries you used to answer five questions and to insert, update, and delete one row of your own.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| `sqlite3`, `.mode csv`, `.import`, `.schema` (Part 2) | Rebuilding `favorites.db` from `favorites.csv` and confirming its structure. |
| `COUNT`, `DISTINCT`, `WHERE`, `LIKE` (Part 3) | Answering questions 1-3. |
| `GROUP BY`, `ORDER BY`, `AS`, `LIMIT` (Part 4) | Answering questions 4-5. |
| `INSERT`, `UPDATE`, `DELETE`, always with `WHERE` (Part 5) | The CRUD-practice milestone. |

### Milestones (build them in order, each one works on its own)

1. **Rebuild the database.** On cs50.dev, put your `favorites.csv` from Lesson 28 in a folder, then run `sqlite3 favorites.db`, `.mode csv`, `.import favorites.csv favorites`, and confirm the result with `.schema`. Done when `.schema` shows one table with your three columns.
2. **Answer with `COUNT`.** Write one query answering: "How many total responses are in the file?" Done when it returns a single number.
3. **Answer with `DISTINCT`.** Write one query answering: "Which languages actually appear, and how many distinct ones are there?" Done when you have both the list and the count.
4. **Answer with `LIKE`.** Write one query answering: "How many favorite problems start with a specific word or phrase of your choosing (e.g., 'hello')?" Done when you can explain, in one sentence, what `%` did in your pattern.
5. **Answer with a `GROUP BY` ranking.** Write one query answering: "Which language is most popular, ranked from most to least chosen?" using `GROUP BY`, an alias (`AS n`), and `ORDER BY n DESC`. Done when the most popular language is on top.
6. **Answer with `LIMIT`.** Extend the previous query with `LIMIT 3` to answer: "What are the top 3 most popular languages?" Done when exactly three rows come back.
7. **Practice full CRUD, safely.** `INSERT` one new row for yourself (any language and problem you like); confirm it with a `SELECT ... WHERE` that matches only your row; `UPDATE` just that row (change the problem, say) using the same targeted `WHERE`; confirm again; then `DELETE` just that row with `WHERE`, and confirm with a final `SELECT` that it's gone and nothing else changed. Done when all four confirmations show exactly what you expect: no more, no less.
8. **Stretch goal: feel the danger, safely.** On a throwaway *copy* of `favorites.db` (never your working copy), run a `DELETE FROM favorites;` or `UPDATE favorites SET ...;` with no `WHERE` at all, then `SELECT * FROM favorites;` to see the damage for yourself. Restore your real database afterward by re-running `.mode csv` and `.import` from the original CSV.

### How you will know you are done

- ✅ `.schema` shows a `favorites` table with the same columns as your original CSV.
- ✅ You have five saved queries, one per question, each returning the correct single answer (not just "some rows").
- ✅ You inserted, updated, and deleted exactly one row of your own, each time with a `WHERE` that targeted only that row, and can show the confirming `SELECT` after each step.
- ✅ You can explain out loud why `DELETE FROM favorites;` with no `WHERE` is different in kind, not just degree, from `DELETE FROM favorites WHERE ...;`.

> 💡 **Keep yourself honest:** before every `UPDATE` or `DELETE` in this Capstone, run the identical `WHERE` as a `SELECT` first and actually read the row(s) back. Only run the destructive version once you've confirmed, with your own eyes, that it targets exactly the row you mean.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: One column, one filter (foundational)
Write a single `SELECT` that lists only the `problem` column, for every row where `language` equals 'Python'. Then change it to use `LIKE` instead of `=`, matching any language containing the letter "y" (hint: `'%y%'`), and see how the results change.

### Exercise 2: Rank from the bottom (intermediate)
Write a `GROUP BY` query that counts rows per `problem` instead of per `language`, orders the results ascending (least popular first) with an alias, and uses `LIMIT 1` to surface the single least-popular problem in the file.

### Exercise 3: Full CRUD on a scratch copy (advanced)
On a throwaway copy of your database, run three separate `INSERT` statements to add three new rows. Then write one `UPDATE` whose `WHERE` clause uses `LIKE` to match all three at once (for example, by a shared problem name) and changes their `language` in a single statement. Finally, `DELETE` only two of the three, using a `WHERE` with `AND` precise enough to leave the third untouched, confirming with a `SELECT` after each step.

---

## Cheat sheet

```text
SETUP (once per CSV)
  sqlite3 <name>.db          open or create a database file
  .mode csv                  tell SQLite the next import is comma-separated
  .import <file>.csv <table>  load the CSV into a new table
  .schema [table]             show table structure (columns, types)
  .quit                       leave the SQLite prompt

READ (SELECT)
  SELECT * FROM t;                        every column, every row
  SELECT col1, col2 FROM t;               only these columns
  SELECT COUNT(*) FROM t;                 how many rows
  SELECT DISTINCT col FROM t;             unique values only
  SELECT COUNT(DISTINCT col) FROM t;      how many unique values
  ... WHERE col = 'value';                filter rows (string equality)
  ... WHERE col = 'it''s';                escape a quote by doubling it
  ... WHERE col LIKE 'hello%';            % = zero or more characters
  ... GROUP BY col;                       cluster rows by shared value
  ... GROUP BY col ORDER BY n DESC;       sort a grouped result
  ... AS n                                alias a column (temp rename)
  ... LIMIT k;                            cap the number of rows returned

WRITE (CRUD's other three letters)
  INSERT INTO t (col1, col2) VALUES (v1, v2);   Create: missing cols become NULL
  UPDATE t SET col = v WHERE ...;               Update: DANGEROUS with no WHERE
  DELETE FROM t WHERE ...;                       Delete (rows): DANGEROUS with no WHERE
  DROP TABLE t;                                  Delete (whole table, no undo)

NULL
  IS NULL / IS NOT NULL      the only correct way to test for NULL (never = NULL)
  NULL means "deliberately absent," never 0 or ''

GOLDEN RULE
  Before UPDATE or DELETE: run the same WHERE as a SELECT first. Read it back. Then act.
```

## How this connects to the rest of the course

- **Earlier, Module 7 · Lesson 28:** the loop-and-dictionary CSV parsing you wrote there is exactly the pain this lesson's `SELECT`, `GROUP BY`, and `COUNT` replace. You rebuild the same `favorites.csv` here as `favorites.db`.
- **Next, Module 8 · Lesson 30: Relational design and JOINs:** one table only gets you so far. The next lesson introduces primary keys, foreign keys, and `JOIN` so you can split data across multiple tables (like IMDb's shows, people, and ratings) without redundancy, and still ask one question across all of them.
- **Later, capstone:** the database-backed web app you design at the end of this course stores its data in tables exactly like `favorites`, read and changed with the same four CRUD verbs you practiced here.

---

*Source: "CS50x 2026 - Lecture 7 - SQL" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
