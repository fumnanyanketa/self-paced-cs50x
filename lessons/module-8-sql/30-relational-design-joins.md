# Module 8 · Lesson 30: Relational Design and JOINs

> **Course:** Self-Paced CS50x
> **Module 8:** SQL and databases: store data properly and query it declaratively
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 7 - SQL](https://www.youtube.com/watch?v=oqRU2So6Z2Y) · [full transcript](../../transcripts/09-lecture-7-sql.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

Real-world data almost never fits neatly in one table without wasting space or inviting typos, so this lesson teaches you to split it into several small, normalized tables linked by primary and foreign keys, and then pull the pieces back together on demand with JOINs and nested subqueries: the exact design skill behind every multi-table question a real app ever has to answer.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you design and build a tiny library database (books, authors, and borrowers, including a many-to-many relationship) and answer real questions about it with joins and a subquery. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** SQLite and IMDb's particular schema are specific to this lecture, but the idea of splitting data into independent, linked tables instead of one big flat file is more than fifty years old.
>
> - **[A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)** (E. F. Codd, *Communications of the ACM*, 1970). The original paper proposing that data be stored as separate "relations" (tables) connected by shared values rather than one giant, repetitive file: precisely the redesign this lesson walks through with the Office/Steve Carell spreadsheet.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Schema:** the design of a database: which tables exist, what columns each one has, and what type of data each column holds. Running the `.schema` command in SQLite prints this design back to you.
- **Primary key:** the column in a table whose value is unique for every row and identifies that row, the way a Harvard ID number identifies one specific student and no one else.
- **Foreign key:** a column that stores another table's primary key value, so a row here can point at a specific row over there. The same integer is called "primary" in its home table and "foreign" everywhere else it shows up.
- **Normalization:** reorganizing data into several smaller tables, each about one kind of thing, so that no piece of information (a name, a title) ever has to be typed out (and possibly misspelled) more than once.
- **Junction table:** a small table whose only job is to link two other tables together, one row per pairing, so that either table can relate to many rows of the other.
- **JOIN:** a SQL command that combines rows from two or more tables into one temporary result, matching them up by a shared column: usually a primary key on one side and a foreign key on the other.
- **Subquery (nested query):** a `SELECT` statement written inside another `SELECT` statement, so the inner query's answer becomes an ingredient the outer query searches for.
- **One-to-many / many-to-many:** descriptions of how many rows on one side of a relationship can connect to how many rows on the other. One show has many genres: one-to-many. One person can star in many shows, and one show can have many stars: many-to-many.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

**Module 8 · Lesson 29** gave you CRUD on a single table: `favorites`, with one row per survey response. That's plenty for a spreadsheet you downloaded once. But the moment your data describes a *world* (TV shows, the people in them, how good they are, what genres they belong to), one table stops working. You either repeat information until it becomes unmanageable, or you split it up and need a new tool to put it back together. That tool is what this lesson teaches. As Malan puts it while looking at his first attempt to model TV shows in a spreadsheet:

> "What I have done here is normalize the data by eliminating all redundancies except for maximally some redundant integers." (David Malan)

That one sentence is the whole lesson in miniature: stop repeating text, and accept a *few* repeated integers instead, because integers are cheap to store and fast to compare. Everything else in this lesson is the machinery for living with that trade: primary keys, foreign keys, data types, constraints, JOINs, and subqueries. It is also, quite literally, the design skill behind this course's **north-star project**: the database-backed web app you'll build near the end. Designing that app's schema *is* this lesson, just with your own tables instead of IMDb's.

## Learning objectives

By the end of this lesson you will be able to:

1. Redesign a repetitive, spreadsheet-style dataset into normalized tables that eliminate copy-pasted redundancy.
2. Identify a primary key and a foreign key in a `CREATE TABLE` statement, and explain why the very same value is "primary" in one table and "foreign" in another.
3. Read a table's schema with `.schema` and choose an appropriate SQLite data type (`INTEGER`, `NUMERIC`, `REAL`, `TEXT`, `BLOB`) and constraint (`NOT NULL`, `UNIQUE`) for a new column.
4. Write a `JOIN` that combines two tables to answer a question neither table can answer alone.
5. Write a nested (subquery-based) `SELECT` that looks something up before it looks up the thing you actually want.
6. Tell apart one-to-one, one-to-many, and many-to-many relationships, and model a many-to-many relationship correctly with a junction table.

## Prerequisites

- **Module 8 · Lesson 29: SQL fundamentals: CRUD**: you should already be comfortable running `SELECT`, `INSERT`, `UPDATE`, and `DELETE` with `WHERE`, `LIKE`, `GROUP BY`, `ORDER BY`, and `LIMIT` at the `sqlite3` interactive prompt.
- A cs50.dev codespace (or any machine with `sqlite3` installed), from earlier modules.

---

## Part 1: From a leaky spreadsheet to normalized tables

Before touching a database at all, Malan models the same real-world problem three different ways in a spreadsheet: who starred in which TV show. Watching the design fail twice, on purpose, is what makes the third version click.

### Attempt 1: one column per star

The first instinct is a wide table: one row per show, one column per star:

```text
title      | star1        | star2        | star3          | star4         | star5
-----------|--------------|--------------|----------------|---------------|------------
The Office | Steve Carell | Rainn Wilson | John Krasinski | Jenna Fischer | B.J. Novak
Cheers     | Ted Danson   | Shelley Long |                |               |
```

This immediately runs into trouble. A show with two stars leaves three columns blank (a sparse, "ragged" table); a show with a bigger ensemble cast needs a sixth, seventh, even tenth `starN` column that most other rows won't use. There is no fixed number of columns that fits every show.

### Attempt 2: one row per star, title repeated

The next instinct is to flip rows and columns: one row per *(show, star)* pair, with the title repeated for every star in that show:

```text
title      | star
-----------|----------------
The Office | Steve Carell
The Office | Rainn Wilson
The Office | John Krasinski
The Office | Jenna Fischer
The Office | B.J. Novak
Cheers     | Ted Danson
Cheers     | Shelley Long
```

This solves the ragged-columns problem, but introduces a new one: the string `"The Office"` is now typed out five separate times. Type it as `"The Ofice"` once by accident, and you've silently split one show into two, with no way for the database to notice.

### Attempt 3: three linked sheets, and integers instead of text

The design that actually works splits the data into three separate sheets, each about exactly one kind of thing, and gives each "thing" a unique integer ID instead of repeating its name:

```text
shows sheet                 people sheet                  stars sheet (cross-reference)
+---------+------------+    +-----+----------------+      +---------+-----------+
| show_id | title      |    | id  | name           |      | show_id | person_id |
+---------+------------+    +-----+----------------+      +---------+-----------+
| 386676  | The Office |    | 1   | Steve Carell   |      | 386676  | 1         |
+---------+------------+    | 2   | Rainn Wilson   |      | 386676  | 2         |
                             | 3   | John Krasinski |      | 386676  | 3         |
                             +-----+----------------+      +---------+-----------+
```

The `stars` sheet is the least readable of the three to a human (it's just numbers) but it is the design that scales. Malan explains why he switched from names to integer IDs:

> "Integers, at least we know from our days in C, are going to be a finite length. It's going to be 32 bits, maybe 64 bits, but it's always going to be the same number of bits... These IDs for the title of the show and these IDs for the persons are not going to vary in length because they're all just integers." (David Malan)

A name like `"John Krasinski"` can be any length, which makes it slower to store predictably and to compare. An integer ID is always the same size, which is exactly what lets a database search and cross-reference it efficiently, the same reason arrays and binary search worked well on fixed-size data earlier in this course.

### From a spreadsheet to `shows.db`

Scale this exact idea up to real IMDb data, and you get `shows.db`: a SQLite database with **six** linked tables instead of three sheets (`shows`, `people`, `stars`, `writers`, `ratings`, and `genres`), each holding hundreds of thousands of rows:

```text
                     +-----------------+
                     |   people        |
                     | id (PK)         |
                     | name            |
                     | birth_year      |
                     +--------+--------+
                              ^
                              | person_id (FK)
                     +--------+--------+          +------------------+
                     |   stars/writers |          |   ratings        |
                     | show_id (FK) ---+--------->|  show_id (FK,    |
                     | person_id (FK)  |          |     UNIQUE)      |
                     +--------+--------+          |  rating          |
                              |                    |  votes           |
                              v                    +------------------+
                     +-----------------+
                     |   shows         |          +------------------+
                     | id (PK)         |<---------|   genres         |
                     | title           |          |  show_id (FK)    |
                     | year            |          |  genre           |
                     | episodes        |          +------------------+
                     +-----------------+
```

> 🔑 **The single most important takeaway of this part.** Normalize by giving every real-world "thing" (a show, a person) its own table with a unique ID, then use that ID everywhere else instead of retyping the name. A few repeated integers are a fair price for eliminating repeated, error-prone text.

## Part 2: Meeting `shows.db` (data types, constraints, and your first JOIN)

### Reading a schema with `.schema`

`shows.db` already exists as a file Malan prepared in advance. Opening it and running the SQLite-specific command `.schema shows` prints back the exact statement that built the `shows` table, the same idea as `.schema` from Lesson 29, just on a richer table:

```sql
CREATE TABLE shows (
    id INTEGER,
    title TEXT NOT NULL,
    year NUMERIC,
    episodes INTEGER,
    PRIMARY KEY(id)
);
```

Four columns, four different jobs. `id` is the table's **primary key**: the column SQLite guarantees can be used to look up exactly one row. Malan defines primary and foreign keys together, since neither makes sense without the other:

> "A primary key is the unique identifier for a table. It is the column of values that uniquely identify every row... When that same ID appears in another table for cross referencing purposes, you refer to it instead as a foreign key because that same key is over there in another table, thus foreign." (David Malan)

So `shows.id` is a primary key *in the `shows` table*. The exact same integer, sitting in the `ratings`, `genres`, or `stars` table under a name like `show_id`, is a **foreign key** there: a pointer back to one specific row in `shows`. Same value, different job, depending on which table it's sitting in.

### The five SQLite data types

Notice `shows.title` is declared `TEXT` and `shows.year` is declared `NUMERIC`. SQLite supports exactly five data types, far fewer than C's menagerie of `int`, `float`, `double`, `char`, and friends:

```text
INTEGER   whole numbers                     a show's id, a rating's vote count
NUMERIC   a catch-all for things like        the year a show debuted (IMDb's data
          dates and other real-world          for this isn't a pure int or float)
          numeric-ish data
REAL      floating-point numbers             a show's average rating, e.g. 8.4
TEXT      strings                            a title, a person's name, a genre
BLOB      "binary large object" -- raw       rare; storing an actual file (an
          zeros and ones                     image, etc.) inside the database
```

Malan is blunt about how short this list is:

> "That's it for SQLite. There are only these 5 types... you have blobs, which is a great name which stands for binary large objects." (David Malan)

Other databases (MySQL, PostgreSQL, Oracle) support more types, but SQLite's five cover almost everything a beginner needs.

### `NOT NULL` and `UNIQUE`: constraints as built-in defenses

A **constraint** is a rule the database enforces on a column for you, so bad data never gets in, no exceptions, no matter which program is doing the inserting. `shows.title` is marked `NOT NULL`:

> "You can specifically say when creating a table that this column cannot be null. And if I try to insert data into that table with a null value... the insertion will fail." (David Malan)

This is a genuine step up from a spreadsheet, where a blank cell can mean "no data" or "forgot to type it" or "not applicable," and nothing stops you from leaving it blank. In SQL, `NULL` is not the same as an empty string `""`: it explicitly and consciously means "no data here," and `NOT NULL` refuses to let a column ever hold that absence.

The `ratings` table adds a second constraint, `UNIQUE`, on its foreign key:

```sql
CREATE TABLE ratings (
    show_id INTEGER NOT NULL UNIQUE,
    rating REAL,
    votes INTEGER,
    FOREIGN KEY(show_id) REFERENCES shows(id)
);
```

`UNIQUE` says no value may appear twice in that column, which is exactly what enforces a **one-to-one relationship**: every show gets at most one row in `ratings`, never two.

### Your first JOIN: shows + ratings

Before JOIN, the only way to connect `shows` and `ratings` was a nested query: get the good show IDs first, then look up shows matching them:

```sql
SELECT title FROM shows
WHERE id IN (SELECT show_id FROM ratings WHERE rating >= 6.0 LIMIT 10);
```

That answers "which shows are highly rated," but not "what is each show's actual rating": the rating itself lives in a different table and never comes back. A `JOIN` solves this by lining the two tables up on their shared column and returning both sides at once:

```sql
SELECT title, rating FROM shows
JOIN ratings ON shows.id = ratings.show_id
WHERE rating >= 6.0
LIMIT 10;
```

Now every row of the result has both a `title` (from `shows`) and a `rating` (from `ratings`), matched up correctly because `shows.id` (primary key) was lined up with `ratings.show_id` (foreign key).

> ✅ **What to do about it:** give every table a primary key, mark any column that must always have a value `NOT NULL`, and mark a foreign key `UNIQUE` whenever the relationship it represents really is one-to-one, as `ratings.show_id` is here.

## Part 3: One-to-many and many-to-many (genres, stars, and Steve Carell)

Not every relationship is one-to-one. A show can belong to several genres, and a person can star in several shows while a show has several stars. SQL handles both with the same JOIN and subquery tools, just with a little more care.

### One-to-many: a show and its genres

The `genres` table has no `UNIQUE` constraint on `show_id`, because one show is allowed to appear many times, once per genre:

```sql
CREATE TABLE genres (
    show_id INTEGER NOT NULL,
    genre TEXT NOT NULL,
    FOREIGN KEY(show_id) REFERENCES shows(id)
);
```

To find every genre for the 1970 show *Cat Weasel* (id `63881`), Malan shows two equivalent approaches. First, a nested subquery: look up the show's ID inside the parentheses, then use that ID in the outer query:

```sql
SELECT genre FROM genres
WHERE show_id = (SELECT id FROM shows WHERE title = 'Cat Weasel');
```

Second, a JOIN that lines up the two tables directly:

```sql
SELECT title, genre FROM shows
JOIN genres ON shows.id = genres.show_id
WHERE shows.id = 63881;
```

The JOIN version returns *Cat Weasel* three times over, once per genre row, because a joined result must have the same number of columns in every row, so the show's title gets duplicated to keep each genre paired with it. That repetition exists only in this temporary answer, never in the stored data itself.

### Many-to-many: the `stars` table

Genres are one-to-many, but people and shows are a different, third kind of relationship entirely. Malan introduces it while unveiling the `stars` table:

> "We have a third and final type of relationship. A many to many relationship. Why? Because it's certainly the case that one person can be in multiple shows, and it's certainly the case that some shows have multiple people, hence many to many." (David Malan)

`stars` is a **junction table**: just two foreign-key columns, `show_id` and `person_id`, and nothing else:

```sql
CREATE TABLE stars (
    show_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    FOREIGN KEY(show_id) REFERENCES shows(id),
    FOREIGN KEY(person_id) REFERENCES people(id)
);
```

Neither `shows` nor `people` mentions the other directly; `stars` is the only table that knows who was in what.

### Three baby steps: who starred in The Office (2005)?

Rather than write one giant query, Malan builds the answer as a chain of nested subqueries, one small question at a time, and recommends this approach for exactly that reason:

> "I think it's quite often easier to just do multiple nested queries because you sort of work your way from the inside out taking sort of baby steps to the problem." (David Malan)

Step 1: find the show's own ID (there are several "Office" shows; year narrows it to one):

```sql
SELECT id FROM shows WHERE title = 'The Office' AND year = 2005;
-- 386676
```

Step 2: plug that into `stars` to get every person ID linked to that show:

```sql
SELECT person_id FROM stars
WHERE show_id = (SELECT id FROM shows WHERE title = 'The Office' AND year = 2005);
```

Step 3: plug *that* into `people` to get actual names instead of IDs:

```sql
SELECT name FROM people
WHERE id IN (
    SELECT person_id FROM stars
    WHERE show_id = (SELECT id FROM shows WHERE title = 'The Office' AND year = 2005)
);
```

The same chain runs just as well in reverse. To find every show Steve Carell has starred in, look up his `id` first, then his shows:

```sql
SELECT title FROM shows
WHERE id IN (
    SELECT show_id FROM stars
    WHERE person_id = (SELECT id FROM people WHERE name = 'Steve Carell')
);
```

### The same answer with JOINs (explicit and implicit)

The nested version above can be rewritten as one JOIN spanning all three tables:

```sql
SELECT title FROM shows
JOIN stars ON shows.id = stars.show_id
JOIN people ON stars.person_id = people.id
WHERE name = 'Steve Carell';
```

There's also an older, more implicit style: list all three tables after `FROM`, separated by commas, and let the `WHERE` clause do the work of lining them up:

> "This is just a third way to express the exact same idea by doing implicit joins... by selecting data clearly from all three tables as per this comma separated list of table names but telling the database with your predicate, the where clause, how you want to line all of those tables up." (David Malan)

```sql
SELECT title FROM shows, stars, people
WHERE shows.id = stars.show_id
AND people.id = stars.person_id
AND name = 'Steve Carell';
```

All three versions (nested subqueries, explicit `JOIN`, implicit comma-join) return exactly the same rows. Nested subqueries tend to be the easiest to reason about while you're learning, because you build the answer from the inside out, one small question at a time. (Malan also notes that in a lot of real production code, a library called an **ORM**, short for object-relational mapper, writes these joins for you once it understands your schema, useful to know exists, but out of scope for this course.)

## Part 4: How the pieces fit together

Zoom back out to the whole `shows.db` diagram from Part 1. Every technique in this lesson is really one repeated move: give each real "thing" its own table and a primary key, connect tables with a foreign key column, and choose nested subqueries or a JOIN depending on how many tables you need to cross at once.

```text
RELATIONSHIP TYPE     EXAMPLE                  HOW YOU ENFORCE / QUERY IT
one-to-one              shows <-> ratings        FK marked UNIQUE; JOIN or subquery
one-to-many              shows <-> genres         plain FK (no UNIQUE); JOIN or subquery
many-to-many             shows <-> people          junction table (stars) with two FKs;
                                                   JOIN across 3 tables, or nested subqueries
```

This is also, directly, the shape of the Capstone you're about to build: a tiny library where books relate to authors (many-to-many, needing a junction table) and to borrowers (through loan records). Design that schema well up front, and every question you'll ever want to ask it (who wrote this, who has that book out right now) becomes a JOIN or a subquery instead of a mess of repeated text.

---

## Key takeaways

1. **Normalize by splitting, not by repeating.** Give each real-world "thing" its own table with a unique primary key, and reference that key elsewhere instead of retyping names or titles.
2. **Primary and foreign key are the same value, different roles.** A column is a primary key in the table it uniquely identifies, and a foreign key anywhere else it's used to cross-reference that table.
3. **SQLite has five data types, not fifty.** `INTEGER`, `NUMERIC`, `REAL`, `TEXT`, `BLOB`: choose based on what the value actually is, not habit from another language.
4. **Constraints are defenses, not suggestions.** `NOT NULL` blocks missing required data at insert time; `UNIQUE` on a foreign key is what actually makes a relationship one-to-one.
5. **JOIN lines two (or more) tables up by a shared key.** A one-to-many JOIN duplicates the "one" side's row per match on the "many" side. That's expected, not a bug.
6. **Many-to-many needs a third table.** A junction table like `stars` (just two foreign keys) is the only correct way to represent "many of these relate to many of those."
7. **Nested subqueries and JOINs are interchangeable.** They can answer the exact same question; subqueries are usually easier to reason about first, working from the inside out.

## Common pitfalls

- ❌ **Repeating a name or title across rows "because it's easier for now."** That's exactly the Attempt-2 spreadsheet problem: one typo silently creates a duplicate entity the database can't detect.
- ❌ **Forgetting `UNIQUE` on a foreign key that's supposed to be one-to-one.** Without it, nothing stops a second row from sneaking in and silently turning a one-to-one relationship into one-to-many.
- ❌ **Trying to cram a many-to-many relationship into one of the two "real" tables.** A `books` table with an `author_id` column only works if every book has exactly one author: the moment a book has two authors, you need a junction table.
- ❌ **Being surprised by duplicate rows after a JOIN.** If you join a "one" table to a "many" table, the "one" side's data repeats once per match. That's correct behavior, not a bug in your query.
- ❌ **Assuming SQLite's five types are the only path.** Choose `NUMERIC` for a genuinely ambiguous real-world value (like a year), not just `TEXT` because it's easiest to insert first and think about later.

---

## 🛠️ Capstone Project: A Tiny Library Database

> This is the main hands-on project for the lesson. You'll design a small relational schema from scratch (books, authors, and borrowers) with a real many-to-many relationship in it, then prove the design works by answering questions that require exactly the tools this lesson taught: joins and a nested subquery. Designing a schema like this well is precisely the skill your eventual final project depends on.

### What you will build

A SQLite database, `library.db`, built on cs50.dev, containing:

- An **`authors`** table and a **`books`** table (one-to-many isn't quite right here: books can have multiple authors, and authors can write multiple books).
- A **`book_authors`** junction table linking them: the many-to-many relationship, modeled the way `stars` links `shows` and `people`.
- A **`borrowers`** table and a **`loans`** table recording who has (or had) which book checked out.
- A handful of seeded rows, and three answered questions: two that require a `JOIN`, one that requires a nested subquery.

### Why this is the perfect practice

| Lesson idea | Where you use it in the library |
|---|---|
| Normalization (Part 1) | Separate `authors`, `books`, and `borrowers` tables instead of one wide, repetitive sheet. |
| Primary/foreign keys, constraints (Part 2) | Every table gets an `id` primary key; `NOT NULL` on required columns. |
| Many-to-many via a junction table (Part 3) | `book_authors` links `books` and `authors`, just like `stars` links `shows` and `people`. |
| JOIN across tables (Parts 2-3) | Listing a book's author(s), and listing who currently has which book. |
| Nested subquery (Part 3) | Finding every book by a given author, mirroring the Steve Carell pattern. |

### Milestones (build them in order, each one works on its own)

1. **Create the tables.** On cs50.dev, run `sqlite3 library.db` and write `CREATE TABLE` statements for `authors` (`id`, `name NOT NULL`, `birth_year`), `books` (`id`, `title NOT NULL`, `year`), `book_authors` (`book_id`, `author_id`, both `NOT NULL`, both foreign keys, the junction table), `borrowers` (`id`, `name NOT NULL`, `email UNIQUE`), and `loans` (`id`, `book_id`, `borrower_id`, `checked_out_on`, `returned_on`, with `book_id`/`borrower_id` as foreign keys). Run `.schema` and confirm all five tables and their constraints exist.
2. **Seed a few rows.** `INSERT` at least 3 authors, 4 books, and 3 borrowers. Insert `book_authors` rows so that **at least one book has two authors**: this is what proves the relationship is genuinely many-to-many, not accidentally one-to-many. Insert a few `loans` rows, leaving `returned_on` as `NULL` for books currently checked out.
3. **Answer with a JOIN, question 1: "List every book together with the name(s) of everyone who wrote it."** Requires joining `books`, `book_authors`, and `authors`. Confirm the co-authored book from Milestone 2 shows up once per author.
4. **Answer with a JOIN, question 2: "List every book currently checked out, together with the borrower's name."** Requires joining `loans`, `books`, and `borrowers`, filtered `WHERE returned_on IS NULL`.
5. **Answer with a nested subquery, question 3: "List the titles of every book written by a specific author."** Build it in baby steps like the Steve Carell example: first get the author's `id`, then the matching `book_id`s from `book_authors`, then the titles from `books`, all as one nested query, not a JOIN.
6. **Stretch goals.** (a) Add a `CHECK` or extra constraint of your choosing (for example, requiring `year` to be a plausible number). (b) Rewrite question 3 as an explicit `JOIN` instead of a nested subquery, and confirm both return identical rows. (c) Using `GROUP BY` and `COUNT` from Lesson 29, find which borrower currently has the most books checked out.

### How you will know you are done

- ✅ `.schema` shows five tables, each with a primary key, and foreign keys correctly declared on `book_authors` and `loans`.
- ✅ At least one book in `book_authors` has two (or more) author rows: proof the many-to-many relationship is real, not just modeled as one-to-many by accident.
- ✅ Both JOIN questions return correct, matched-up results (book + author name; book + current borrower name).
- ✅ The nested-subquery question returns the correct book titles for a chosen author, built as parenthetical steps rather than a JOIN.

> 💡 **Keep yourself honest:** after writing the nested-subquery version of question 3, also write it as a JOIN and confirm the two return exactly the same rows. If they don't match, one of your foreign keys is pointing at the wrong column.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Spot the relationship (foundational)
Without writing any SQL, sketch (as a `text` diagram like Part 1's) a two-table design for "students" and "clubs." Decide: is a student-to-club relationship one-to-one, one-to-many, or many-to-many? Explain your reasoning in a sentence, and note whether you'd need a junction table.

### Exercise 2: Same answer, two ways (intermediate)
Using your library database (or `shows.db`), pick one question and answer it twice: once with a `JOIN`, once with an equivalent nested subquery. Run both and confirm they return the identical set of rows.

### Exercise 3: A second many-to-many (advanced)
Add a `tags` table (e.g., "mystery," "young-adult," "reference") and a `book_tags` junction table to your library database, modeled on `book_authors`. Write the query "list every tag for a specific book" three ways: a nested subquery, an explicit `JOIN`, and an implicit comma-separated join, and confirm all three return the same rows.

---

## Cheat sheet

```text
NORMALIZE A SPREADSHEET
  One table per "thing" (shows, people) + unique integer IDs, not repeated text.
  Cross-reference tables (stars, book_authors) hold only foreign keys.

KEYS
  Primary key   = uniquely identifies a row in ITS OWN table.
  Foreign key   = a primary key value stored in ANOTHER table, for cross-referencing.

DATA TYPES (SQLite has exactly 5)
  INTEGER  NUMERIC  REAL  TEXT  BLOB

CONSTRAINTS
  NOT NULL   -- this column may never be empty
  UNIQUE     -- no value may repeat in this column (this is what makes a
                foreign key relationship 1-to-1)

RELATIONSHIPS
  1-to-1        FK marked UNIQUE                  (shows <-> ratings)
  1-to-many     plain FK, no UNIQUE               (shows <-> genres)
  many-to-many  junction table, 2 FKs, no PK-per- (shows <-> people via stars)
                entity meaning of its own

JOIN
  SELECT ... FROM a JOIN b ON a.id = b.a_id WHERE ...;

NESTED SUBQUERY (build from the inside out)
  SELECT ... FROM x WHERE col = (SELECT ... FROM y WHERE ...);
  SELECT ... FROM x WHERE col IN (SELECT ... FROM y WHERE ...);

IMPLICIT JOIN (older style, same result as JOIN)
  SELECT ... FROM a, b WHERE a.id = b.a_id AND ...;
```

## How this connects to the rest of the course

- **Earlier, Module 8 · Lesson 29:** "SQL fundamentals: CRUD" gave you `SELECT`/`INSERT`/`UPDATE`/`DELETE` with `WHERE`, `LIKE`, `GROUP BY`, `ORDER BY`, and `LIMIT` on one table. This lesson is what happens the moment your data needs more than one.
- **Next, Module 8 · Lesson 31:** "Indexes, injection, and race conditions" picks up right where the JOINs here can get slow at real-world scale. You'll learn to speed them up with an index, and how to call these exact queries safely from Python.
- **Later, the north-star project:** designing your own final project's schema (users, posts, orders, whatever your app needs) is exactly this lesson's skill, just with your own tables instead of IMDb's.

---

*Source: "CS50x 2026 - Lecture 7 - SQL" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
