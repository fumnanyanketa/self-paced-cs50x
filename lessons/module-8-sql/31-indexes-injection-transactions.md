# Module 8 · Lesson 31: Indexes, Injection, and Race Conditions

> **Course:** Self-Paced CS50x
> **Module 8:** SQL and databases: store data properly and query it declaratively
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 7 - SQL](https://www.youtube.com/watch?v=oqRU2So6Z2Y) · [full transcript](../../transcripts/09-lecture-7-sql.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

A database only feels instant if you help it: build an index so it can search like `O(log n)` binary search instead of checking every row, call SQL from Python with the cs50 library's `db.execute()` so you get the best of both languages, always hand user input to that function as a `?` placeholder instead of pasting it into the query string yourself (or an attacker can rewrite your query for you), and wrap any multi-step update in a transaction so two things happening "at the same time" can never corrupt your data.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where, on cs50.dev, you time a real query before and after
> building an index, write a small Python script that queries a database
> safely with a placeholder, work out on paper exactly how an unsafe query
> could be hijacked (without ever running it against anything live), and wrap
> a two-step update in a transaction so it can't be corrupted by bad timing.
> Everything before the Capstone teaches the skills you will use there. If you
> want to see the finish line first, jump to the **"Capstone Project"**
> section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** SQLite, the cs50 library, and IMDb's dataset are specific to this lecture, but the three underlying ideas are each much older and tool-agnostic:
>
> - **[B-tree](https://en.wikipedia.org/wiki/B-tree)** (Rudolf Bayer and Edward M. McCreight, 1972). The original tree structure behind almost every database index in use today, including the one SQLite builds when you run `CREATE INDEX`: the reason a lookup can jump straight to an answer instead of scanning every row.
> - **[OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)**. The industry-standard, continually updated reference for defending against exactly the attack this lesson walks through with the login-form example: parameterized queries (what this lesson calls placeholders) are its first and strongest recommendation.
> - **[ACID (Atomicity, Consistency, Isolation, Durability)](https://en.wikipedia.org/wiki/ACID)**. The classic set of guarantees a database transaction is supposed to provide: the formal version of the "all or nothing" promise behind `BEGIN TRANSACTION` / `COMMIT` / `ROLLBACK` in this lesson's last part.

## A few plain-language basics first

This lesson uses some everyday-sounding terms in a specific way. Here they are in plain words:

- **Index:** extra bookkeeping a database builds for one column so it can find matching rows quickly, instead of checking every row one by one. It costs some storage space and a little extra time on every insert or update, in exchange for much faster searches.
- **B-tree:** the tree-shaped structure SQLite (and most databases) actually uses to implement an index. Its rows are organized so the database can discard most of the table with each comparison, the same way binary search discards half of a sorted array at every step.
- **Placeholder (`?`):** a stand-in symbol you put inside a SQL query string wherever a value should go, instead of pasting that value into the string yourself. You hand the real value to your SQL library as a separate argument, and the library inserts it safely.
- **SQL injection:** an attack where someone's input is crafted so that, once it's pasted into your SQL query, it changes what the query actually does, for example, turning a login check into "let anyone in."
- **Race condition:** a bug that happens when two things read and then write the same piece of shared data at almost the same time, and the final result depends on the unpredictable order in which they happened to run.
- **Lock:** a database's way of saying "don't touch this row until I'm done with it," so a second query can't read or change a value while a first query is still in the middle of updating it.
- **Transaction:** one or more SQL statements grouped so the database treats them as a single, indivisible step: either all of them take effect, or, if something goes wrong, none of them do.
- **cs50 library (Python):** CS50's own teaching library. Its `SQL` class wraps a database connection and gives you one method, `execute()`, which runs a query and hands back the results as a list of dictionaries, one dictionary per row.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 30 gave you the design skill (normalized tables, primary and foreign keys, JOINs, subqueries) to model real-world data and ask it real questions. But three practical problems show up the moment that database leaves your laptop and meets real traffic: it gets slow at scale, it gets attacked by real users typing real things into real forms, and it gets corrupted when two requests touch the same row at once. This lesson is those three problems and their fixes, in the order Malan hits them once `shows.db` and real users enter the picture.

The very first of the three is a direct callback: back in **Module 4 · Lesson 14** you learned that binary search beats linear search by discarding half of what's left at every step. Malan draws that same line explicitly once someone asks how SQL searches actually work:

> "In the most naive implementation, SQL is essentially just doing linear search from the top of the table all the way to the bottom. However, we as the programmers are going to have the ability to optimize those queries so that the database can actually do something closer to binary search." (David Malan)

An index is that optimization, Lesson 14's idea, grown into a database. And the injection section revives a thread from even earlier, **Module 3 · Lesson 12**'s closing line about ciphers and command-line input: never trust input, validate it before you use it. Here, Malan states the database version of that rule directly:

> "The more important lesson is never trust users' input. Either they're going to do something accidentally or they're going to do something maliciously, and you do not want that to happen." (David Malan)

This lesson is also, concretely, why the north-star database-backed web app you're building toward will hold up under real users: every query it ever runs, all the way through **Module 11 · Lesson 40**'s capstone, goes through `db.execute()` with a placeholder, because of what you're about to see happen when one doesn't.

## Learning objectives

By the end of this lesson you will be able to:

1. Measure how long a SQL query takes with `.timer`, speed it up with `CREATE INDEX`, and explain the speedup in terms of B-trees and logarithmic search.
2. Call a SQL query from Python using the cs50 library's `SQL` class and `db.execute()`, and read each result row back as a dictionary.
3. Explain, using a concrete worked example, how an f-string-built SQL query lets user input change the query's meaning, a SQL injection attack, and why a `?` placeholder prevents it.
4. Rewrite an f-string-built query to use a placeholder instead, without changing its behavior for ordinary, well-behaved input.
5. Explain what a race condition is using the dorm-fridge milk example, and identify why the same failure can happen to something like an Instagram like count.
6. Wrap a multi-step database update in `BEGIN TRANSACTION` / `COMMIT` (and `ROLLBACK`) so it either fully happens or not at all.

## Prerequisites

- **Module 8 · Lesson 30: Relational design and JOINs**: you should be comfortable with primary keys, foreign keys, and querying `shows.db` with `JOIN`s and nested subqueries.
- **Module 8 · Lesson 29: SQL fundamentals: CRUD**: comfort with `SELECT`, `WHERE`, and the interactive `sqlite3` prompt.
- **Module 7 (Python)**: enough Python to read a `for` loop, a dictionary lookup like `row["language"]`, and a function call with arguments.
- Helpful context, not required to re-read: **Module 4 · Lesson 14** (binary search and `O(log n)`) and **Module 3 · Lesson 12** (never trust input), both are called back to directly below.
- A cs50.dev codespace with `sqlite3` installed, and the `favorites.db` and `shows.db` files from Lessons 29-30 (or recreate them with `.mode csv` / `.import`, as in Lesson 29).

---

## Part 1: Indexes and B-trees (making search fast on purpose)

### Timing a query with `.timer`

Every SQL keyword you've used so far describes *what* you want, never *how* the database should find it. By default, SQLite finds it the dumbest possible way: checking every row from the top, exactly like linear search. You can watch this cost in real time with a SQLite-specific command, `.timer`, which prints how long each subsequent command actually takes:

```sql
.timer on
SELECT * FROM shows WHERE title = 'The Office';
```

Against the 250,000-plus-row `shows` table from Lesson 30, Malan runs this and reports:

> "That query took, let's say in real terms 0.042 seconds. That's crazy fast." (David Malan)

0.042 seconds is imperceptible to one person clicking search once. But Malan immediately reframes why it's still worth shaving down:

> "It makes for happier customers and users because you're getting them the answer faster... it saves you money because presumably if you've spent $1000 for a server and that server has a certain amount of RAM, a certain speed CPU... it can only do so many searches per unit of time... so you can handle not 1000 users at once but 2000 users or 5000 users all with the same hardware." (David Malan)

### `CREATE INDEX`: telling the database what to optimize for

A relational database, unlike a spreadsheet, lets you plan ahead for the searches you know you'll run often. The command is `CREATE INDEX`, and it names three things: the index (whatever name you like), the table, and the column(s) to optimize:

```sql
CREATE INDEX title_index ON shows(title);
```

Running it takes a moment up front: SQLite has to build that structure once, and after that it has to keep the index updated on every insert, update, or delete to that column. In exchange, rerunning the *exact same* query as before:

```sql
SELECT * FROM shows WHERE title = 'The Office';
```

comes back in 0.001 seconds instead of 0.042. Malan does the arithmetic out loud:

> "Orders of magnitude faster, so I can handle 42 times as many users on the same database, so to speak, than I could have previously just by building this index." (David Malan)

### What an index actually is: a B-tree

An index isn't magic. It's a specific, well-known data structure:

> "An index in a database is very often created using what's called a B-tree. This is not a binary tree. ... The tree is its own distinct structure that's very similar in spirit in that it's fairly shallow because most of the nodes have children, but it doesn't necessarily have two children. It might have more children, and in fact, the more children the nodes have, the sort of higher up you can pull all of the leaf nodes and the shorter you can make the height of the tree." (David Malan)

The payoff is the same shape as Lesson 14's binary search, just generalized to nodes with more than two children each:

> "When I am now searching for titles like The Office, the database doesn't have to do the default behavior, which is start at the top and use linear search all the way to the bottom. If it has proactively built up an index in memory... it now has a tree-like structure storing those titles that allows it to find in some logarithmic time... the same data much more quickly, and that's how we went from 0.042 to 0.001 second instead." (David Malan)

An index trades a little extra storage and slightly slower writes for a query that scales like `O(log n)` instead of `O(n)`, precisely the trade that made binary search worth having a sorted array for in Lesson 14, now applied to a database table instead of an in-memory array.

> 🔑 **The single most important takeaway of this part.** `CREATE INDEX` builds a B-tree on a column so the database can search it in roughly logarithmic time instead of checking every row, the exact same `O(log n)` win as binary search, now working for you automatically on every future query against that column.

## Part 2: Calling SQL from Python (the cs50 library's `db.execute()`)

### The problem with doing it all in Python

Back in Lesson 29's `favorites.py`, sorting the language counts required real work: `sorted(counts)` sorts by key, `sorted(counts, key=counts.get)` sorts by value but ascending, and getting descending order takes a third named argument, `reverse=True`. Malan lands on the same frustration that motivated switching to SQL in the first place:

> "This is just very annoying to have to use that amount of code to actually answer relatively simple questions, and this is why we did transition for much of today to a declarative language like SQL that just let me select what I care about in that data." (David Malan)

Meanwhile, the equivalent SQL is one line:

```sql
SELECT language, COUNT(*) AS n FROM favorites GROUP BY language ORDER BY n DESC;
```

The natural next question: why choose? A real application usually needs both: Python's `input()`, loops, and web-framework glue, *and* SQL's declarative power over stored data.

### Bridging the two languages

The cs50 library for Python ships a small SQL module for exactly this. You open a connection once, then call one method every time you need data:

```python
from cs50 import SQL

db = SQL("sqlite:///favorites.db")

rows = db.execute("SELECT language, COUNT(*) AS n FROM favorites GROUP BY language ORDER BY n DESC")

for row in rows:
    print(row["language"], row["n"])
```

`"sqlite:///favorites.db"` is a URI (a structured way of naming a resource) telling the library which SQLite database file to open, the same `favorites.db` you were opening manually with `sqlite3 favorites.db` all lesson.

`db.execute()` is, in Malan's words, the one function that matters here:

> "The only function that's useful in the CS 50 library for SQL is this execute function, which allows me to write literally a line of SQL." (David Malan)

And the shape of what comes back matters just as much as the call itself:

> "It returns by design a list of rows. Each of those rows is a dictionary of key value pairs." (David Malan)

That's why `row["language"]` and `row["n"]` work inside the loop: each `row` is a dictionary, indexed by the column name (or alias, like `n` for `COUNT(*)`) you chose in the `SELECT`. Run this version and you get the exact same three numbers Lesson 29's twenty-line dictionary-and-loop version produced, sorted, correctly, in one query.

> ✅ **What to do about it:** reach for SQL to do the sorting, filtering, and counting it's built for (`GROUP BY`, `ORDER BY`, `WHERE`), and reach for Python for everything around it: taking input, looping over results, building a web page. Let each language do what it's good at.

## Part 3: SQL injection (never trust user input)

### Where this goes wrong: an f-string query

Suppose your Python program asks a user for their favorite problem, then looks up how many people share that answer. The tempting first draft uses an f-string to build the query directly:

```python
favorite = input("Favorite problem: ")
rows = db.execute(f"SELECT COUNT(*) AS n FROM favorites WHERE problem = '{favorite}'")
print(rows[0]["n"])
```

This works fine for ordinary input like `Hello, world`. Malan asks the room what happens with an answer like `hello, it's me`, a string that itself contains a single quote:

> "If I inputted the other problem we played with, hello, it's me, where it was IT apostrophe S, that if interpolated right here is clearly going to confuse the single quotes such that who knows what's going to come back." (David Malan)

The apostrophe in the user's own text closes the quote early, and whatever text follows it is now interpreted as SQL syntax, not as data. In the best case, that just breaks the query with a confusing error. In the worst case, Malan explains, a deliberately crafted answer can do far more:

> "What if the user types something crazy like the word delete or drop or update or any of those destructive commands that we saw earlier and somehow tricks your code into executing maybe the select, but then eventually an additional query like a delete... This is the biggest threat to taking user input and trusting it in the context of databases, and it's called... a SQL injection attack." (David Malan)

### The `--` comment character

One tool that makes injection especially dangerous is SQL's comment syntax:

> "It turns out that [`--`] in SQL is the comment character. So it's like hash in Python or slash slash [in] C. This in SQL means ignore everything to the right." (David Malan)
>
> *(The transcript's speech-to-text has a gap right where Malan says the symbol aloud; `--` is filled in from context: it's the only SQL comment marker discussed anywhere in the lecture, and the sentence structure needs a subject there.)*

Anything after `--` on that line is simply discarded by the database, including, as you're about to see, the rest of a query the programmer wrote on purpose.

### The GitHub login example (a hypothetical, not a real vulnerability)

To make the danger concrete, Malan poses a hypothetical using a login form everyone recognizes:

> "Here for instance is like the login screen to GitHub.com... suppose for the sake of discussion GitHub is using SQL Lite, which they're not using because it's not meant for massive, large data sets like this, but suppose they are." (David Malan)

This is explicitly a teaching hypothetical, not a claim that GitHub or any real site is built this way. Imagine the server-side code, written with an f-string instead of a placeholder, looks like this:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
rows = db.execute(query)
```

A well-behaved user typing a normal email and password produces exactly the query the programmer intended. Now imagine the *username* field receives this instead:

```text
malan@harvard.edu' --
```

Substituted into the f-string, the resulting query text becomes:

```sql
SELECT * FROM users WHERE username = 'malan@harvard.edu' --' AND password = 'anything'
```

The single quote right after the real email closes the string early (exactly the apostrophe problem from `hello, it's me`), and `--` then comments out everything after it, including the entire password check:

> "This would seem to finish the thought prematurely, and then it says [`--`], and so that just means ignore everything else. So what GitHub ends up doing accidentally in this case is selecting star from users where username is malan@harvard.edu irrespective of what his password actually is." (David Malan)

No password was ever needed. The attacker's input didn't just supply a value: it rewrote the query's logic.

### The famous version of this bug: Bobby Tables

This exact category of bug is famous enough in software culture to have its own name, from a well-known [xkcd](https://xkcd.com/) comic by Randall Munroe: a parent named their child something like `Robert'); DROP TABLE Students;--`, quietly wiping out a school's database the first time it was inserted into a query without a placeholder. Malan closes the lecture on that same joke, and the transcript also mentions a real-world echo of it, someone who registered a license plate reading literally `NULL`, which confused automated toll-booth systems that read plates straight into a database query without sanitizing them first. Both examples exist purely to make the *defensive* lesson land: any system that pastes untrusted text into a query is exposed, whether the text comes from a login form, a search box, or a camera reading a license plate.

### The fix: placeholders, not string-building

The fix is not "write cleverer escaping code yourself." Malan is direct about this:

> "The solution then is to use a library, almost always use a library. This is not a wheel you should reinvent yourself." (David Malan)

Concretely, that means replacing the f-string with a `?` placeholder, and handing the real value to `db.execute()` as a separate argument:

```python
favorite = input("Favorite problem: ")
rows = db.execute("SELECT COUNT(*) AS n FROM favorites WHERE problem = ?", favorite)
print(rows[0]["n"])
```

The `?` is not CS50-specific: it's a common convention across SQL libraries in many languages. Here's what changes underneath:

> "If you instead use a library like CS50's, and you don't just use F strings... you use question marks. What will happen is this: when the user goes and types in [something with] a single quote, that's fine. Let them put weird scary characters like single quotes in their input. The library will take charge of escaping user input, so anything dangerous in their input will be changed from one single quote to two." (David Malan)

With the placeholder version, typing `malan@harvard.edu' --` as a username no longer breaks anything out of the string: the library treats the entire value, apostrophe and all, as *data*, never as SQL syntax. The query still runs; it just correctly finds no matching username, because no username actually contains a literal apostrophe and two dashes.

> ✅ **What to do about it:** never build a SQL query by pasting a variable directly into the string (with an f-string, `.format()`, or `+` concatenation). Always write a `?` in the query text and pass the real value as a separate argument to `db.execute()`.

## Part 4: Race conditions and transactions (when timing itself is the bug)

### The dorm-fridge milk problem

Even a perfectly written, injection-safe query can still corrupt data if it collides with another query at just the wrong moment. Malan introduces this with a simple story: you and a roommate share a dorm fridge. You check it, see no milk, and walk to a store to buy some. Meanwhile, before you're back, your roommate checks the same fridge, also sees no milk, and walks to a different store. You both come home with milk: now you have too much.

> "Why did we find ourselves in a situation where we ended up with too much milk? ... We inspected the state of a variable that was in the process of being updated by someone else." (David Malan)

That's a **race condition** end to end: two processes (you and your roommate) both read a piece of shared state (the fridge is empty), both decide independently what to do based on that stale read, and both act, and because neither knew what the other was doing, the combined result is wrong. Malan's proposed fix is exactly the database's fix, just physical:

> "Maybe dramatically lock the refrigerator somehow, and in fact that's a term of art in databases: to actually use a database lock, so that if you are in the process of updating the value in the database, lock it so that no one else can inspect the value of that database and potentially make a poor decision." (David Malan)

### The same bug at scale: Instagram likes

The milk story is contrived on purpose; the real version happens constantly on any popular website. Malan's example is a single Instagram post receiving hundreds of thousands of near-simultaneous likes, served by many web servers all talking to the same underlying data. The naive Python-plus-SQL logic to increment a like count takes two steps:

```python
rows = db.execute("SELECT likes FROM posts WHERE id = ?", id)
likes = rows[0]["likes"]
db.execute("UPDATE posts SET likes = ? WHERE id = ?", likes + 1, id)
```

Note that both queries already use `?` placeholders: this code is safe from injection. It is not, however, safe from timing. Malan walks through exactly how it breaks:

> "Maybe there's 100 likes at this point in the story. And then just by chance, another server... it too gets the same answer, there's currently 100 likes. Meanwhile, the first server... updates the number of likes from 100 to 101. But because the other server was essentially running the same code in parallel, it's going to make the same mathematical decision and update the number of likes from 100 to [101]. But at this point in the story, the number of likes should obviously be [102], so we've lost data." (David Malan)
>
> *(Bracketed numbers correct two evident speech-to-text typos in the raw transcript, "1001" and "10. 2", where the recording clearly means 101 and 102.)*

Both servers read `100` before either one wrote anything back. Both, correctly, computed `100 + 1 = 101`. The post ends up recording 101 likes when it should record 102: a like silently vanished, not because either query was wrong on its own, but because they overlapped in time.

### Transactions: making multi-step updates atomic

The database-level fix is a **transaction**, a way of telling the database "treat everything between these two points as one indivisible step":

> "You would use commands in SQL like begin transaction, and then execute the lines of code that you want, and then when you're ready to commit it, that is save it, you use a commit command. But if something goes wrong or you get interrupted, you can actually roll back the whole thing." (David Malan)

In SQL, that looks like:

```sql
BEGIN TRANSACTION;

SELECT likes FROM posts WHERE id = 123456;
UPDATE posts SET likes = 101 WHERE id = 123456;

COMMIT;
```

While a transaction is open, the database locks the row(s) involved so that a second, concurrent transaction touching the same row has to wait its turn instead of reading a value that's mid-update. If anything goes wrong partway through (an error, a lost connection), `ROLLBACK` undoes everything since `BEGIN TRANSACTION`, so the database is never left half-updated:

```sql
BEGIN TRANSACTION;

UPDATE posts SET likes = 101 WHERE id = 123456;
-- something goes wrong here

ROLLBACK;  -- posts.likes is back to 100, as if nothing happened
```

Malan's summary of what this buys you:

> "You can ensure that those... two database queries inside will either both be executed or not at all. They will not be interrupted, and that's the fundamental solution to this problem, analogous to putting a lock on the fridge, or by leaving a note, or calling your roommate, preventing them from making the same decision themselves." (David Malan)

> 🔑 **The single most important takeaway of this part.** A race condition happens when two processes read shared data, decide what to do, and write back, all without knowing about each other. A transaction (`BEGIN TRANSACTION` ... `COMMIT`, with `ROLLBACK` as the escape hatch) is how you tell the database "lock this, do all these steps as one unit, and let no one else in until I'm done."

## Part 5: How the four ideas fit together

Every idea in this lesson answers a different question about the same underlying worry: *what happens to my database once real, unpredictable users start hitting it?*

```text
QUESTION                          TOOL                     WHY IT WORKS
"Is this query fast enough        .timer, CREATE INDEX     Builds a B-tree so search is
 at real scale?"                                            O(log n), not O(n) (Lesson 14's
                                                             binary search, generalized)

"Can I use SQL's power without    cs50's SQL class,        One line of declarative SQL
 giving up Python's glue?"        db.execute()              instead of loops + dictionaries

"Can a user's own typed input     ? placeholders,           The library treats the value as
 rewrite my query?"               never f-strings           data, never as SQL syntax

"Can two requests at once         BEGIN TRANSACTION /       Locks the row(s) so no one reads
 corrupt shared data?"            COMMIT / ROLLBACK          a value mid-update
```

A production-grade query in your eventual capstone project combines all four: it runs against an indexed column, it's called from Python through `db.execute()`, every user-supplied value arrives as a `?` placeholder, and any multi-step update is wrapped in a transaction. None of the four is optional once real users are involved: they solve four genuinely different failure modes, and a database that only handles three of them will still break in production.

---

## Key takeaways

1. **An index trades storage and write time for read speed.** `CREATE INDEX name ON table(column)` builds a B-tree so lookups on that column run in roughly `O(log n)` time instead of `O(n)`, the same win as binary search over linear search.
2. **`.timer on` turns "it feels fast" into a number.** Measure before you optimize, and measure again after, so you know the index actually helped.
3. **`db.execute()` returns a list of dictionaries.** Each row is indexed by column name (or `AS` alias), which is why `row["language"]` works after a `SELECT language, ...`.
4. **Never build a query by pasting a value into the string.** An f-string, `.format()`, or string concatenation with a raw value lets that value change the query's meaning: that's what a SQL injection attack exploits.
5. **A `?` placeholder is the fix, not a nicety.** Pass the query as a template with `?` in it and the real values as separate arguments; the library escapes them so they can only ever be data.
6. **A race condition needs no attacker at all**: it's two ordinary, correct-looking operations overlapping in time and silently losing data, like the dorm-fridge milk or an Instagram like count.
7. **A transaction makes multiple statements atomic.** `BEGIN TRANSACTION` ... `COMMIT` guarantees all-or-nothing execution; `ROLLBACK` undoes an in-progress transaction cleanly if something goes wrong.

## Common pitfalls

- ❌ **Adding an index to every column "just in case."** Each index costs extra space and slows down every future insert/update/delete on that column: index the columns you actually search or join on often, not all of them.
- ❌ **Building a SQL query with an f-string because it "works in testing."** It works right up until a user's input contains a quote, a `--`, or a semicolon: test with exactly that kind of input before trusting any query.
- ❌ **Assuming placeholders are only about avoiding typos with quotes.** They're a security boundary: the library escapes the value so it can never be interpreted as SQL syntax, no matter what it contains.
- ❌ **Believing "my code ran fine once" means it's race-condition-free.** Race conditions are timing-dependent: code can pass every manual test and still fail the moment two requests genuinely overlap in production.
- ❌ **Wrapping a transaction around only one query.** Transactions matter when a *sequence* of statements (read-then-write, like the like-count example) needs to happen as one unit. A single, standalone statement rarely needs one.

---

## 🛠️ Capstone Project: Optimize and Defend Your Database

> This is the main hands-on project for the lesson. On cs50.dev, you'll measure a real speedup from an index, call SQL from Python the safe way, work out an injection attack entirely on paper (never against a live target), and make a multi-step update atomic with a transaction. Together these four moves are exactly what your eventual north-star web app needs from every query it runs.

### What you will build

Using the `shows.db` and `favorites.db` files from Lessons 29-30 on your cs50.dev codespace:

- A timed, then indexed, query against `shows.db`, with both timings recorded.
- A small Python script, `lookup.py`, that safely queries `favorites.db` using cs50's `SQL` class and a `?` placeholder.
- A plain-text file, `injection_notes.txt`, that reconstructs (on paper only) an unsafe f-string query, a malicious input for it, and the safe placeholder rewrite.
- A short transaction demo that wraps a two-step "increment a count" update in `BEGIN TRANSACTION` / `COMMIT`, plus one deliberate `ROLLBACK`.

### Why this is the perfect practice

| Lesson idea | Where you use it in the capstone |
|---|---|
| `.timer` and `CREATE INDEX` (Part 1) | Milestones 1-2: measure, then eliminate, a real linear-search cost on `shows.db`. |
| cs50's `db.execute()` (Part 2) | Milestone 3: `lookup.py` queries `favorites.db` from Python. |
| Placeholders vs. f-strings (Part 3) | Milestones 3-4: the script uses `?` for real; the notes file shows on paper why the f-string version wouldn't have been safe. |
| Transactions (Part 4) | Milestone 5: a two-step update made atomic with `BEGIN TRANSACTION` / `COMMIT` / `ROLLBACK`. |

### Milestones (build them in order, each one works on its own)

1. **Time the baseline query.** On cs50.dev, open `sqlite3 shows.db`, run `.timer on`, then run `SELECT * FROM shows WHERE title = 'The Office';` a couple of times. Write down the reported time.
2. **Index it, then re-time it.** Run `CREATE INDEX title_index ON shows(title);`, then rerun the *exact same* `SELECT` from Milestone 1. Write down the new time and compute the speedup as a ratio (yours may not be exactly 42x: record whatever you actually observe, and note whether it's a bigger or smaller jump than Malan's).
3. **Write `lookup.py`.** Using `from cs50 import SQL`, open `favorites.db`, use Python's `input()` to ask for a language, and run `SELECT COUNT(*) AS n FROM favorites WHERE language = ?` with that input passed as the placeholder's value. Print the count. Confirm it works for ordinary input like `Python` or `C`.
4. **Write `injection_notes.txt`, on paper only, never run this against anything.** By hand, write out: (a) the *unsafe* version of Milestone 3's query built with an f-string instead of a placeholder; (b) one example input containing a single quote and `--` that would change what that unsafe query does; (c) the exact resulting SQL text after substitution, with the part `--` comments out marked; (d) one sentence explaining why the placeholder version from Milestone 3 is immune to that same input. Do not point any of this at a real website, form, or database you don't own: the point is understanding the mechanism, not attacking anything.
5. **Make a two-step update atomic.** In `favorites.db` (or a small scratch table you create), pick any integer column you can safely increment (or add one, e.g. `views INTEGER DEFAULT 0`). Wrap a `SELECT` of the current value followed by an `UPDATE` that adds one inside `BEGIN TRANSACTION` / `COMMIT`. Then run a second attempt where you deliberately stop before `COMMIT` and issue `ROLLBACK` instead: confirm with a fresh `SELECT` that the value reverted to what it was before that transaction.
6. **Stretch goals.** (a) Run `EXPLAIN QUERY PLAN` before and after Milestone 2's index to see SQLite describe the change from a full table scan to an index search, in its own words. (b) Add a second index on a different column and time a query that benefits from it. (c) Rewrite `lookup.py` so every one of its queries (not just the lookup) runs inside a single transaction.

### How you will know you are done

- ✅ You have two recorded timings for the identical query (one before, one after `CREATE INDEX`) and the "after" number is meaningfully smaller.
- ✅ `lookup.py` runs correctly for at least two different inputs, using a `?` placeholder, never an f-string, for the user-supplied value.
- ✅ `injection_notes.txt` contains all four parts from Milestone 4, and the malicious input you chose really would change the unsafe query's behavior if it were (hypothetically) run.
- ✅ Your transaction demo shows both outcomes: one `COMMIT` that keeps the change, and one `ROLLBACK` that discards it, confirmed by a `SELECT` afterward.

> 💡 **Keep yourself honest:** if Milestone 4's malicious input doesn't actually break the sentence structure of the unsafe query when you trace through it by hand, character by character, you haven't found a real injection: go back to the `--`-comment example in Part 3 and match its shape exactly.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Predict the speedup (foundational)
Without running anything, look at the `stars` table from Lesson 30 (many rows, no index on `person_id`). Would `CREATE INDEX person_index ON stars(person_id);` help the query `SELECT show_id FROM stars WHERE person_id = ?` run faster? Explain your answer in one or two sentences using the words "B-tree" and "linear search."

### Exercise 2: Spot the injection (intermediate)
Here is a query built with an f-string: `f"SELECT * FROM shows WHERE title = '{title}'"`. Write down a value for `title` that would make this query return every row in the table, and trace through, character by character, why it works. Then rewrite the query safely with a placeholder.

### Exercise 3: Design a transaction (advanced)
Sketch (in plain English or pseudocode, no need to run it) the two SQL statements you'd need to transfer "5 points" from one row's `score` column to another row's `score` column in a single table. Explain, in a sentence, what could go wrong if two such transfers overlapped without a transaction, and how `BEGIN TRANSACTION` / `COMMIT` prevents it.

---

## Cheat sheet

```text
INDEXES
  .timer on                                   -- print how long each command takes
  CREATE INDEX name ON table(column);          -- build a B-tree index on that column
  Full table scan: O(n).  Indexed lookup: O(log n) -- same win as binary search.

PYTHON + SQL (cs50 library)
  from cs50 import SQL
  db = SQL("sqlite:///file.db")
  rows = db.execute("SELECT ... WHERE col = ?", value)   -- rows: list of dicts
  rows[0]["column_name"]                                  -- read a value back

SQL INJECTION -- NEVER DO THIS
  f"SELECT * FROM users WHERE username = '{username}'"    -- unsafe: value can
                                                            -- rewrite the query
  --  is SQL's comment character: everything after it on the line is ignored

SQL INJECTION -- DO THIS INSTEAD
  db.execute("SELECT * FROM users WHERE username = ?", username)
  -- the library escapes the value; it can only ever be data, never SQL syntax

RACE CONDITIONS AND TRANSACTIONS
  Race condition: two reads-then-writes of shared data overlap in time,
                  and the last write silently loses the other one's update.
  BEGIN TRANSACTION;
    SELECT ...;      -- read
    UPDATE ...;       -- write, based on what you just read
  COMMIT;             -- both happen, atomically -- or, on error:
  ROLLBACK;           -- neither happens; back to before BEGIN TRANSACTION
```

## How this connects to the rest of the course

- **Earlier, Module 8 · Lesson 30:** "Relational design and JOINs" gave you `shows.db`'s schema and the queries this lesson times and secures: you can't optimize or defend a query you don't already know how to write.
- **Earlier still, Module 4 · Lesson 14 and Module 3 · Lesson 12:** an index is Lesson 14's binary search, grown into a database (`O(log n)` instead of `O(n)`); the injection section is Lesson 12's "never trust input" thread, now applied to SQL specifically.
- **Next, Module 9 · Lesson 32:** "Using AI well: prompts and copilots" is a self-contained detour (no SQL required) before Module 10 returns to building with the web.
- **Later, Module 11 · Lesson 40:** the capstone project's own database layer calls `db.execute()` with a `?` placeholder for every single query it runs, with no exceptions: this lesson is why.

---

*Source: "CS50x 2026 - Lecture 7 - SQL" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
