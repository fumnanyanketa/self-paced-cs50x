# Topic maps — CS50x 2026 lectures

Structured skim notes produced per lecture (one Sonnet subagent each, 2026-07-26).
Used to sequence COURSE_OUTLINE.md and to brief lesson-drafting agents. Transcripts
live in `../transcripts/`.

Video IDs: Intro HJP0a6vKvlo · L0 Scratch UuIEbpQms8o · L1 C SlqjA04_dpk ·
L2 Arrays h5Gc1n8ZuU8 · L3 Algorithms 6Svu_ae5ebk · L4 Memory db0H0U13YsA ·
L5 Data Structures PmAI76OGE_E · L6 Python Rl0ludWTLxs · L7 SQL oqRU2So6Z2Y ·
AI -9bo8HlSxwQ · L8 Web yYst7puZXjw · L9 Flask am7POvSZ4GE · L10 The End ApQTgFkf8TU

---

## Lecture 0 — Scratch (transcript: 02-…Scratch.txt)

**Summary:** Malan opens CS50 by building a live AI chatbot in Python, then works bottom-up from binary and ASCII through algorithms and abstraction to introduce Scratch, closing with student-built game demos (Oscar Time, Ivy's Hardest Game).

**Segments:** 1 Course intro & AI framing (early) · 2 Live chatbot build — Python + OpenAI API, system vs user prompt, "pretend you're a cat" (early) · 3 Unary & binary counting, bits, transistors (first-quarter) · 4 ASCII — A=65, 8-volunteer "BOW" demo (first-quarter) · 5 Unicode & emoji (middle) · 6 RGB color (middle) · 7 Images/video/audio as bits (middle) · 8 Linear vs binary search — phone-book demo, n vs log n (middle) · 9 Pseudocode & building blocks — functions, conditionals, loops (middle-late) · 10 Machine code, compilers, abstraction (late-middle) · 11 Scratch interface tour (late-middle) · 12 say/ask/join, arguments/return values/side effects (late) · 13 Loops & custom "meow" block with parameter (late) · 14 Conditionals + Oscar Time and Ivy's Hardest Game walkthroughs (end)

**Splits:** L1 Welcome+chatbot (seg 1–2); L2 Binary representation (3–7); L3 Algorithms & pseudocode (8–10); L4 Scratch programming (11–14).

**Prereqs assumed:** browser, scratch.mit.edu account, no programming.

**Quotes:** "the overarching goal is to teach you how to think, how to take input and produce correct output" (early) · "Functions are verbs or actions that really get some small piece of work done for you." (middle) · "we can stand on the shoulders of others so long as we know how to use and assemble these kinds of building blocks" (late-middle)

**Tools:** VS Code, Python, OpenAI API (GPT-5), CS50.dev, CS50.ai duck, scratch.mit.edu.

---

## Lecture 1 — C (transcript: 03-…C.txt)

**Summary:** Transition from Scratch blocks to writing, compiling, and debugging real C: syntax, the command line, conditionals, loops, functions, and finite-precision bugs (overflow, truncation).

**Segments:** 1 Scratch-to-C mental model, source vs machine code (early) · 2 VS Code / cs50.dev, GUI vs CLI (early) · 3 hello.c — #include, main, printf, `make`, `./hello` (first-quarter) · 4 Escape sequences & compiler errors (first-quarter) · 5 Docs — manual.cs50.io, man pages, libraries vs headers (first-quarter/middle) · 6 get_string, %s placeholders, typed variables (middle) · 7 Linux commands — ls, mkdir, mv, cp, cd, rm (middle) · 8 Conditionals — if/else if/else, == vs =, flowcharts (middle) · 9 Data types — bool char int float double long; get_int etc.; %c %f %i %li (late-middle) · 10 Char comparison & logical operators — agree.c, `||`, `&&` (middle-late) · 11 Loops — while, do while, for, infinite, break/continue, cat.c (late-middle) · 12 Custom functions & scope — void, prototypes (late) · 13 Code quality — correctness/design/style, check50/style50; Mario nested loops, const (late) · 14 Overflow & imprecision — dollar-doubling, Boeing 787 248-day bug, Y2K, 2038 (end)

**Splits:** L1 Getting started with C (1–4); L2 Input, variables, terminal (5–7); L3 Conditionals & loops (8–11); L4 Functions, quality, limits (12–14).

**Prereqs:** Week 0; cs50.dev account.

**Quotes:** "Getting an education from MIT is like trying to drink from a fire hose." (early) · "Any time you don't see any output at a command like this, that's probably a good thing." (first compile) · "Reboot the plane." (Boeing story, late)

**Tools:** cs50.dev VS Code, manual.cs50.io, cs50.h, check50, style50, design50, CS50.ai, make, Linux CLI.

---

## Lecture 2 — Arrays (transcript: 04-…Arrays.txt)

**Summary:** Reading-level analysis and debugging exercises motivate arrays; peels back week-1 "training wheels" to show compilation, memory sizes, arrays and strings under the hood; ends with command-line arguments and Caesar-cipher preview.

**Segments:** 1 Reading-level demo (Seuss → Orwell), week goals (opening) · 2 Grace Hopper moth, "bug"/"debugging" (early) · 3 Syntax-error debugging in buggy.c (first-quarter) · 4 Logical errors, printf as debug tool, off-by-one (first-quarter/middle) · 5 debug50 — breakpoints, step-over/into, call stack (middle) · 6 Rubber-duck debugging, CS50.ai, not over-relying on AI (middle) · 7 Compilation pipeline — Clang vs Make, preprocess/compile/assemble/link, a.out, -lcs50 (middle/late-middle) · 8 Data type sizes; RAM as addressable byte grid (late-middle) · 9 Arrays — scores.c, contiguous memory, magic numbers, const int N (late-middle) · 10 Functions taking arrays, passing length, float casting (late) · 11 Chars vs strings, null terminator \0, hi.c (late) · 12 string.h & ctype.h — strlen, isupper/toupper, uppercase.c (late) · 13 int main(int argc, string argv[]), exit status, greet.c, cowsay (late) · 14 Caesar cipher preview — plaintext/ciphertext/keys, ROT13 (closing)

**Splits:** L1 Finding & fixing bugs (1–6); L2 Source → machine code (7–8); L3 Arrays & strings (9–12); L4 CLI args, exit codes, first cipher (13–14).

**Quotes:** "The compiler has no idea what you are trying to achieve logically. It only knows about the language C itself." · "It's just going to be an array of characters, hence the dots we're trying to connect today." · "So important nowadays with passwords and credit card numbers and personal messages that you might want to send." (closing)

**Tools:** debug50, check50, Clang, make, cs50.h/stdio.h/string.h/ctype.h, cowsay, CS50.ai.

---

## Lecture 3 — Algorithms (transcript: 05-…Algorithms.txt)

**Summary:** Live human demos (counting, locker searches, sorting volunteers) and C code teach linear vs binary search, Big O/Ω/Θ, selection/bubble/merge sort, structs, and recursion.

**Segments:** 1 Algorithms = step-by-step problem solving (opening) · 2 Attendance-counting demo — O(n), O(n/2), O(log n) (early) · 3 Running-time graphs (early) · 4 Arrays & memory, locker metaphor, zero-indexing (first-quarter) · 5 Linear vs binary search — Monopoly-money lockers demo (first-quarter) · 6 Pseudocode for search, if/else pitfalls, base cases (middle) · 7 Big O cheat sheet — worst case (middle) · 8 Omega & Theta (middle) · 9 search.c with ints then strings (strcmp), phonebook.c introducing struct (middle) · 10 Selection sort — 8-volunteer demo, Θ(n²) (middle-late) · 11 Bubble sort — Ω(n) with early exit (late) · 12 Sort visualizations (late) · 13 Recursion — base/recursive cases, Mario iterative vs recursive (late) · 14 Merge sort — O(n log n), music-scored triple visualization (end)

**Splits:** L1 Algorithmic thinking & Big-O (1–3); L2 Searching arrays in C (4–9); L3 Selection & bubble sort (10–12); L4 Recursion & merge sort (13–14).

**Quotes:** "an algorithm is just step by step instructions for solving some problem" (opening) · "a computer can only look at or access one value at a time" (arrays) · "Base cases are generally conditionals that ask a question to which the answer is going to be yes or no right then and there." (recursion)

**Tools:** cs50.h, string.h (strcmp), sorting visualizer, Monopoly props.

---

## Lecture 4 — Memory (transcript: 06-…Memory.txt)

**Summary:** Beyond the CS50 library's training wheels: hexadecimal, pointers, strings-as-char*, stack vs heap, pass-by-reference, and file I/O, building toward the image-filter pset.

**Segments:** 1 Images as pixels/bytes, Post-it cat art (opening) · 2 1-bit smiley bitmap (early) · 3 RGB & hex codes in Photoshop (first-quarter) · 4 Hexadecimal, base 16, 0x prefix (first-quarter) · 5 addresses.c, %p (first-quarter/middle) · 6 Pointers — & and *, 8-byte size, mailbox metaphor (middle) · 7 Dereferencing *p (middle) · 8 string = typedef char*; pointer arithmetic (middle) · 9 Why == fails; strcmp (middle) · 10 Shallow-copy bug; malloc/strcpy/free, leaks, NULL checks (middle) · 11 Valgrind, garbage.c, Binky claymation (middle/late) · 12 Stack vs heap; swap.c bug; pass-by-reference fix (late) · 13 scanf, rewriting get_int/get_string, buffer overflow (late) · 14 File I/O — fopen/fclose/fprintf, phonebook.csv (late) · 15 fread/fwrite, custom cp.c; image-filter teaser (closing)

**Splits:** L1 Numbers, colors, hexadecimal (1–4); L2 Pointers & what strings really are (5–8); L3 Safe strings & memory debugging (9–11); L4 Pass-by-reference & files (12–15).

**Quotes:** "I still remember the day in which I finally understood this topic" (intro to pointers) · "We use 64 bits or 8 bytes nowadays for pointers because our computers have that much more memory." · "If you mallocked it, you must free it."

**Tools:** Valgrind, Photoshop color picker, Binky video (Nick Parlante), stdio/stdlib/string/ctype, cs50.h.

---

## Lecture 5 — Data Structures (transcript: 07-…Data Structures.txt)

**Summary:** Abstract data types (queues, stacks, dictionaries) through concrete C implementations (arrays, linked lists, BSTs, hash tables, tries) via live-coded list.c iterations — the recurring speed-vs-memory trade-off toward O(1) lookup.

**Segments:** 1 Trade-offs framing, last week of C (early) · 2 "Jack and Lou" animation — stacks vs queues (early) · 3 Queues — FIFO, enqueue/dequeue, array struct (early) · 4 Stacks — LIFO, push/pop, Gmail inbox (first-quarter) · 5 Dictionaries ADT — key/value (first-quarter) · 6 list.c: static array → malloc → resize-by-copy → realloc → free, leaks (first-quarter/middle) · 7 Linked lists — struct node, ->, prepending, pointer diagrams (middle) · 8 Traversal with temp pointer (middle) · 9 Running times — prepend O(1), search O(n), sorted insertion cases, unload (middle/late-middle) · 10 Recap: arrays vs linked lists (middle) · 11 BSTs — recursive search, O(log n), can degenerate (late) · 12 Hashing & hash tables — array of linked lists, collisions (late) · 13 Tries — O(1) but memory-hungry (late) · 14 Sweetgreen shelf; speller pset preview (end)

**Splits:** L1 ADTs & resizable arrays (1–6); L2 Linked lists (7–9); L3 Trees, hashing & tries (10–14).

**Quotes:** "a stack, as we've just seen, has a LIFO property to it last in, first out" · "data is value or values you care about. Metadata is data that helps you maintain the data you care about" · "the holy grail of data structures is to achieve something that is big O of 1, like constant time"

**Tools:** malloc/realloc/free, Valgrind, list.c–list9.c distribution code.

---

## Lecture 6 — Python (transcript: 08-…Python.txt)

**Summary:** Python as higher-level interpreted language — nearly every C/Scratch concept translated into concise Python while live-coding spell checkers, image filters, phonebooks, and a QR-code generator.

**Segments:** 1 Why Python, C vs Python trade-offs (early) · 2 hello.py vs hello.c (early) · 3 Speller rewrite — set(), def; 1.87s Python vs 1.32s C (early) · 4 PIL filters — blur.py, edges.py in 4 lines (first-quarter) · 5 Modules & cs50 library; input() (first-quarter) · 6 Named params — end=, sep=; docs.python.org (first-quarter/middle) · 7 Types — bool/float/int/str; int() conversion (middle) · 8 if/elif/else, indentation, CPython (middle) · 9 String methods — ==, in, .lower() etc., intro OOP (middle) · 10 Loops & functions — range(), def, main() + `if __name__ == "__main__"` (middle-late) · 11 Float imprecision persists; overflow solved (late) · 12 try/except, ValueError, .isnumeric() (late) · 13 Lists & dicts — append, len, sum, phonebook.py, for/else (late) · 14 sys.argv, sys.exit, csv module, with open (late) · 15 pip — cowsay, pyttsx3, qrcode finale (closing)

**Splits:** L1 Why Python + first programs (1–4); L2 Variables, types, conditionals, strings (5–9); L3 Loops, functions, exceptions (10–12); L4 Lists, dicts, csv, pip (13–15).

**Quotes:** "And this is what we mean by Python being a higher level language." (early) · "To do something pythonically is to do it the way that most Python programmers would do it." (middle) · "Try to execute these lines of code except if there's an error, then do this other thing instead" (late)

**Tools:** CPython, cs50 Python lib, PIL/Pillow, pip, cowsay, pyttsx3, qrcode, csv, sys, docs.python.org.

---

## Lecture 7 — SQL (transcript: 09-…SQL.txt)

**Summary:** Declarative SQL vs procedural C/Python — same task built in Python (CSV, dicts) then SQL (CRUD, joins, indexes); database design, injection, race conditions with real IMDb data.

**Segments:** 1 Declarative vs procedural (early) · 2 Google Form → Sheets → CSV poll (early) · 3 csv.reader, header-row bug (first-quarter) · 4 DictReader + counting; KeyError; try/except (first-quarter) · 5 CRUD & SQLite — .mode csv, .import, .schema, favorites.db (first-quarter/middle) · 6 SELECT — COUNT, DISTINCT, WHERE, LIKE % (middle) · 7 GROUP BY / ORDER BY / LIMIT (middle) · 8 INSERT, NULL, DELETE, UPDATE, DROP; dangers (middle) · 9 IMDb modeling — normalization, primary/foreign keys, shows.db (mid-late) · 10 Types & constraints; first JOIN shows+ratings (mid-late) · 11 One-to-many & many-to-many — genres, stars, nested subqueries (late-middle) · 12 Indexes & B-trees — .timer, 0.042s→0.001s (late) · 13 Python + SQL — cs50 db.execute (late) · 14 SQL injection — placeholders, Bobby Tables (late) · 15 Race conditions & transactions — dorm milk, Instagram likes, BEGIN/COMMIT/ROLLBACK (end)

**Splits:** L1 From files to Python (1–4); L2 SQL fundamentals (5–8); L3 Relational design & joins (9–11); L4 Speed, integration, security (12–15).

**Quotes:** "SQL is said to be a declarative programming language, which is a different sort of paradigm" (start) · "null… refers explicitly to the absence of data" (middle) · "never trust users' input. Either they're going to do something accidentally or they're going to do something maliciously" (late)

**Tools:** Google Forms/Sheets, sqlite3, csv module, cs50.SQL, IMDb shows.db, XKCD Bobby Tables.

---

## AI lecture (transcript: 10-…Artificial Intelligence.txt)

**Summary:** From the CS50 rubber duck through prompt engineering and Copilot to core ML ideas — decision trees, minimax, reinforcement learning, neural networks, LLMs, hallucinations.

**Segments:** 1 Rubber duck history (early) · 2 AI-vs-real polling game (early) · 3 Duck architecture, system vs user prompt (early-middle) · 4 Week 0 code revisited — client.responses.create() (middle) · 5 Copilot demo: speller dictionary.c (middle) · 6 Copilot demo: mario.c from English (middle) · 7 Everyday invisible AI (middle) · 8 Decision trees — Pong/Breakout (middle) · 9 Tic-tac-toe & minimax (middle-late) · 10 Combinatorial explosion → ML (late) · 11 Reinforcement learning — robot, maze, epsilon explore/exploit (late) · 12 Deep learning, neural nets, embeddings, attention, GPT, hallucinations; Shel Silverstein close (late)

**Splits:** L1 AI tools you already use (1–6); L2 How AI actually solves problems (7–12).

**Quotes:** "prompt engineering really, it's not so much a form of engineering as it is a form of asking good questions" · "this kind of functionality in AI amplifies your capabilities as a programmer sort of overnight" · "hallucinations where the AI just makes something up perhaps because some crazy human on the internet made something up"

**Tools:** CS50.ai, GitHub Copilot, OpenAI Python client, ChatGPT/Claude/Gemini.

---

## Lecture 8 — HTML, CSS, JavaScript (transcript: 11-….txt)

**Summary:** How the internet physically moves data (IP, TCP, DNS, DHCP, HTTP) into building/styling static pages with HTML and CSS, then interactivity with JavaScript's DOM/event model.

**Segments:** 1 CLI → web transition (intro) · 2 ARPANET, routers, TF packet skit (early) · 3 IP & TCP — v4/v6, ports, packetized cat JPEG (early) · 4 DNS hierarchy (early-mid) · 5 DHCP (early-mid) · 6 HTTP & URLs — GET/POST, status codes 200/301/404/418, curl -I, safetyschool.org prank (first-third) · 7 DevTools — Network & Elements tabs (first-third/middle) · 8 HTML fundamentals — doctype, DOM tree, http-server :8080 (middle) · 9 Building blocks — headings, lists, tables, img/alt, video (middle) · 10 Links, forms, validation — phishing, mini Google clone, regex, W3C validator, client-side trust warning (middle-late) · 11 CSS — inline → style tag, semantic tags, selectors, :hover, Bootstrap CDN (late) · 12 JavaScript — addEventListener, querySelector, innerHTML; color buttons, blink, autocomplete, geolocation (final)

**Splits:** L1 How the internet works (1–5); L2 HTTP and the browser (6–7); L3 Building pages with HTML (8–10); L4 Styling and scripting (11–12).

**Quotes:** "TCP guarantees delivery by just doing some bookkeeping on the outside of these envelopes." · "CSS is just going to allow us to slap a whole bunch of key value pairs on our HTML elements." · "Anything with hyphens in CSS is changed to Camelcase in JavaScript."

**Tools:** http-server, curl, Chrome DevTools, validator.w3.org, Bootstrap (jsDelivr CDN).

---

## Lecture 9 — Flask (transcript: 12-…Flask.txt)

**Summary:** Flask — routes, templates/Jinja, forms, GET/POST, databases, sessions/cookies, JSON APIs — by rebuilding Malan's 1997 Frosh IMs registration site, closing with login, shopping cart, and a searchable API.

**Segments:** 1 Static files → routes; query strings (early) · 2 Flask basics — pip install flask, app.py, @app.route (early) · 3 Templates & Jinja — render_template, {{ }} (first-quarter) · 4 request.args + defaults (first-quarter) · 5 Forms with GET, /greet route, duplicated HTML (first-quarter/middle) · 6 Template inheritance — layout.html, {% block %}/{% extends %} (middle) · 7 GET vs POST — request.form, methods=["GET","POST"] (middle) · 8 Frosh IMs case study, select/option (middle) · 9 Server-side validation — SPORTS list, {% for %}, error.html (middle-late) · 10 Persistence — cs50 SQL, db.execute, placeholders (late) · 11 Safe deletes — hidden id, POST-only destructive actions (late) · 12 static/ folder; MVC framing (late) · 13 Cookies & sessions — hand-stamp analogy, Flask-Session, login demo (late/final) · 14 Shopping cart via session["cart"] (final) · 15 Search API — LIKE, jsonify() (final)

**Splits:** L1 Routes & templates (1–4); L2 Forms, layouts, HTTP verbs (5–7); L3 Real app: validation & databases (8–12); L4 Sessions, carts & APIs (13–15).

**Quotes:** "the sort of commodity stuff that like literally every web application on the internet has to do anyway" (early) · "do not trust user input ever" (middle-late) · "post requests are preferred any time there's anything remotely personally identifiable or remotely destructive" (late)

**Tools:** Flask, Jinja2, Flask-Session, cs50.SQL, sqlite3, pip, shows.db.

---

## Lecture 10 — The End (transcript: 13-…The End.txt)

**Summary:** Valedictory lecture — abstraction/precision via two live Pictionary demos, course-arc recap, and practical final-project guidance (local setup, Git, hosting, AI tools), closing with a quiz and cake.

**Segments:** 1 "Delta from week 0", Malan's failed pset1 (early) · 2 Inputs/black-box/outputs recap (early) · 3 Pictionary demo 1 — cube without abstraction fails (early) · 4 Pictionary demo 2 — stick figure with abstraction (early-middle) · 5 Course trajectory recap (middle) · 6 Final project framing — training wheels off, good/better/best, AI as junior colleague (middle) · 7 Hackathon & CS50 Fair (middle) · 8 CS50 Charades (middle) · 9 Local dev — VS Code, Docker, Cursor/Windsurf (late) · 10 Git, Live Share (late) · 11 Hosting & resources — GitHub Pages, Netlify, student discounts, Copilot/ChatGPT/Claude/Gemini, edX (late) · 12 Quiz-show review, 15 questions (late)

**Splits:** L1 Abstraction, precision & the arc (1–5, 8, 12); L2 Shipping your final project (6–7, 9–11).

**Quotes:** "Problem solving is computer science." (early) · "You essentially have a junior colleague next to you who can help solve bugs for you." (middle) · "This is CS50 and... this was CS50, cake is now served." (close)

**Tools:** Docker, Git/GitHub, Live Share, GitHub Pages, Netlify, GitHub Student Developer Pack, edX.
