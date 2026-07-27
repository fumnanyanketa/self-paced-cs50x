# COURSE OUTLINE — Self-Paced CS50x

A self-paced companion course built from the **CS50x 2026 lecture transcripts**
(David J. Malan, Harvard). 12 core modules + an optional pre-flight, 43 core
lessons. Each lesson covers ~30–40 minutes of lecture and takes ~45–60 minutes
to work through (read + capstone).

**North-star project:** your own **CS50 final project** — a database-backed web
app you design, build, and host. The C-era capstones build the mental models
it needs; from Python onward, capstones prototype actual components of it.

**Daily ritual:** watch the lecture segment → read the lesson → build the
capstone → log it in PROGRESS.md.

---

## Module 0 — Pre-flight: getting set up (optional)

0. **Pre-flight: your tools, accounts, and first success** — Self-guided
   *Skill gained:* Have a working cs50.dev codespace and a scratch.mit.edu
   account, and run one command in a terminal without fear.

## Module 1 — Computational thinking (Lecture 0 · [Scratch](https://www.youtube.com/watch?v=UuIEbpQms8o)): learn to think in inputs, outputs, and algorithms before any syntax

1. **Welcome to CS50: computers, thinking, and a live AI chatbot**
   *Skill gained:* Explain what programming actually is (input → algorithm → output) and how a system prompt vs a user prompt shapes an AI chatbot.
2. **Bits and binary: how computers represent everything**
   *Skill gained:* Convert small numbers between binary and decimal and explain how bits encode text (ASCII/Unicode), color (RGB), images, video, and sound.
3. **Your first algorithms: search and pseudocode**
   *Skill gained:* Compare linear vs binary search for efficiency and write pseudocode using functions, conditionals, and loops.
4. **Programming in Scratch**
   *Skill gained:* Build a working Scratch program with sprites, variables, loops, conditionals, and custom blocks — a simple interactive game.

## Module 2 — First real programs in C (Lecture 1 · [C](https://www.youtube.com/watch?v=SlqjA04_dpk)): write, compile, run, and fix real code in a terminal

5. **Hello, C: from blocks to code**
   *Skill gained:* Write, compile (`make`), and run a C program, and fix common syntax/header errors by reading compiler messages.
6. **Input, variables, and the command line**
   *Skill gained:* Capture typed user input, format output with placeholders, look up documentation, and navigate files with Linux commands.
7. **Conditionals and loops**
   *Skill gained:* Write programs that branch (if/else) and repeat (while/do-while/for) using the right data types.
8. **Functions, code quality, and the limits of numbers**
   *Skill gained:* Design reusable functions with prototypes and scope, judge code on correctness/design/style, and explain integer overflow and float imprecision.

## Module 3 — Debugging and what the compiler hides (Lecture 2 · [Arrays](https://www.youtube.com/watch?v=h5Gc1n8ZuU8)): debug systematically and see how C really stores data

9. **The art of debugging**
   *Skill gained:* Diagnose syntax and logic errors with printf tracing, the debug50 debugger (breakpoints, step over/into), and rubber-duck reasoning.
10. **From source code to machine code**
    *Skill gained:* Trace the preprocess → compile → assemble → link pipeline and state how C data types are sized in memory.
11. **Arrays and strings under the hood**
    *Skill gained:* Declare, index, and pass arrays to functions, and manipulate strings as null-terminated char arrays with string.h/ctype.h.
12. **Command-line arguments and a first cipher**
    *Skill gained:* Read argc/argv, return meaningful exit statuses, and encrypt/decrypt text with a Caesar shift.

## Module 4 — Algorithms (Lecture 3 · [Algorithms](https://www.youtube.com/watch?v=6Svu_ae5ebk)): measure and choose algorithms, not just write them

13. **Thinking in running time: Big O**
    *Skill gained:* Explain why divide-and-conquer scales better than brute force and read a running-time growth graph.
14. **Searching arrays in C**
    *Skill gained:* Implement linear and binary search (including over strings and structs) and classify them with Big O, Ω, and Θ.
15. **Sorting, the slow way: selection and bubble sort**
    *Skill gained:* Implement selection and bubble sort, explain why both are O(n²), and apply bubble sort's early exit.
16. **Recursion and merge sort**
    *Skill gained:* Write a recursive function with correct base/recursive cases and implement merge sort, explaining why O(n log n) wins.

## Module 5 — Memory (Lecture 4 · [Memory](https://www.youtube.com/watch?v=db0H0U13YsA)): see the bytes — pointers, the heap, and files

17. **Pixels, hexadecimal, and memory addresses**
    *Skill gained:* Read hex notation fluently (colors, addresses) and print a variable's address in C.
18. **Pointers, and what strings really are**
    *Skill gained:* Declare pointers, use & and * correctly, and explain that a C string is a char* to its first character.
19. **malloc, free, and hunting memory bugs**
    *Skill gained:* Deep-copy strings with malloc/strcpy, free correctly, and diagnose leaks and invalid writes with Valgrind.
20. **Pass-by-reference and file I/O**
    *Skill gained:* Mutate a caller's variables via pointers and read/write persistent files with fopen/fprintf/fread/fwrite.

## Module 6 — Data structures (Lecture 5 · [Data Structures](https://www.youtube.com/watch?v=PmAI76OGE_E)): trade speed for memory deliberately

21. **Stacks, queues, and resizable arrays**
    *Skill gained:* Implement array-backed stacks/queues and grow an array with malloc/realloc without leaking.
22. **Linked lists**
    *Skill gained:* Build, traverse, and insert into a linked list with self-referential structs, stating the Big O of each operation.
23. **Trees, hash tables, and tries**
    *Skill gained:* Write a recursive BST lookup and choose between BST, hash table, and trie by time-vs-memory trade-off.

## Module 7 — Python (Lecture 6 · [Python](https://www.youtube.com/watch?v=Rl0ludWTLxs)): same ideas, 10× less code

24. **Why Python? Your first scripts**
    *Skill gained:* Write and run Python scripts and articulate the develop-fast/run-slower trade-off vs C.
25. **Python essentials: variables, conditionals, strings**
    *Skill gained:* Use input(), typed-but-undeclared variables, if/elif/else, and string methods pythonically.
26. **Loops, functions, and exceptions**
    *Skill gained:* Write loops with range(), structure programs with def/main(), and handle errors with try/except.
27. **Lists, dictionaries, and the pip ecosystem**
    *Skill gained:* Store and query data in lists/dicts, read/write CSV files, and install/use third-party packages.

## Module 8 — SQL and databases (Lecture 7 · [SQL](https://www.youtube.com/watch?v=oqRU2So6Z2Y)): store data properly and query it declaratively

28. **From flat files to Python dictionaries**
    *Skill gained:* Parse CSVs with csv.reader/DictReader and tally categories safely.
29. **SQL fundamentals: CRUD**
    *Skill gained:* Load data into SQLite and write SELECT/INSERT/UPDATE/DELETE with WHERE, LIKE, GROUP BY, ORDER BY, LIMIT.
30. **Relational design and JOINs**
    *Skill gained:* Design normalized tables with primary/foreign keys and answer multi-table questions with joins and subqueries.
31. **Indexes, injection, and race conditions**
    *Skill gained:* Speed queries with indexes, call SQL from Python with safe placeholders, and explain transactions.

## Module 9 — Artificial intelligence (AI lecture · [watch](https://www.youtube.com/watch?v=-9bo8HlSxwQ)): use AI well, and know how it works underneath

32. **Using AI well: prompts and copilots**
    *Skill gained:* Write effective system/user prompts and use an AI assistant to scaffold code responsibly.
33. **How machines learn**
    *Skill gained:* Trace decision trees, minimax, reinforcement learning, and neural nets/LLMs — including why hallucinations happen.

## Module 10 — The web (Lecture 8 · [HTML, CSS, JavaScript](https://www.youtube.com/watch?v=yYst7puZXjw)): from packets to pages people can use

34. **How the internet works**
    *Skill gained:* Explain how a packet travels — IP, TCP, DNS, DHCP — and what each protocol contributes.
35. **HTTP and the browser**
    *Skill gained:* Inspect real requests/responses with curl and DevTools and interpret status codes.
36. **Building pages with HTML**
    *Skill gained:* Write a valid multi-element page (headings, lists, tables, media, links, forms) and validate it.
37. **CSS and JavaScript**
    *Skill gained:* Style pages with selectors and Bootstrap, and add interactivity with DOM events.

## Module 11 — Web apps with Flask (Lecture 9 · [Flask](https://www.youtube.com/watch?v=am7POvSZ4GE)): everything so far becomes one real application

38. **Flask fundamentals: routes and templates**
    *Skill gained:* Serve a page from a Flask route that reads URL parameters and renders a Jinja template.
39. **Forms, layouts, and GET vs POST**
    *Skill gained:* Post forms to Flask routes, eliminate duplication with layout inheritance, and choose the right HTTP verb.
40. **A real app: validation and databases**
    *Skill gained:* Validate submissions server-side, persist them in SQLite with safe placeholders, and serve static assets (MVC).
41. **Sessions, carts, and APIs**
    *Skill gained:* Implement login/logout and per-user state with sessions, and expose a JSON API endpoint.

## Module 12 — The finish line (Lecture 10 · [The End](https://www.youtube.com/watch?v=ApQTgFkf8TU)): ship something of your own

42. **Abstraction, precision, and how far you've come**
    *Skill gained:* Explain why abstraction + precision is the whole game, and trace how each course language raised the abstraction level.
43. **Shipping your final project**
    *Skill gained:* Set up a local dev environment (VS Code, Git, Docker), pick hosting, and scope a good/better/best final project plan.

---

*Sources: CS50x 2026 lecture playlist (13 videos). Raw transcripts in
`transcripts/`; per-lecture topic maps in `notes/topic-maps.md`. Official
problem sets and the real course live at cs50.harvard.edu/x — this companion
is for learning the lectures deeply, not a replacement for doing the psets.*
