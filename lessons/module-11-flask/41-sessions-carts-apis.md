# Module 11 · Lesson 41: Sessions, Carts, and APIs

> **Course:** Self-Paced CS50x
> **Module 11:** Web apps with Flask: everything so far becomes one real application
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 9 - Flask](https://www.youtube.com/watch?v=am7POvSZ4GE) · [full transcript](../../transcripts/12-lecture-9-flask.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

A **session** (a small dictionary Flask keeps for each visitor, tied to a cookie in their browser) is the one idea behind logging someone in, giving them a shopping cart that's theirs alone, and it has nothing to do with the last trick: a search route that hands back plain **JSON** instead of a web page, so any program (not just a browser) can use your data.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you add real accounts and a JSON API to the registration app you built in Lesson 40. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Flask, Flask-Session, and `jsonify()` will all get replaced by other tools someday. The mechanisms underneath them are written down as open standards that outlive any one framework:
>
> - **[RFC 6265: HTTP State Management Mechanism](https://www.rfc-editor.org/rfc/rfc6265)** (IETF, 2011). This is the actual specification for the `Set-Cookie` and `Cookie` headers, the "hand stamp" this lesson describes. Whatever language or framework you use ten years from now, if it remembers a logged-in user, it is doing some version of what this document defines.
> - **[JSON](https://www.json.org/json-en.html)** (Douglas Crockford's spec, formalized as ECMA-404). This is the actual, tool-agnostic definition of the data format `jsonify()` produces: a handful of rules for lists, objects, strings, and numbers that nearly every programming language on Earth can read and write.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Cookie:** a small piece of data a web server asks your browser to store and send back automatically on every later request to that same site. It's how a server recognizes "you" across multiple visits.
- **Session:** a per-visitor storage area, kept on the server, usually a Python dictionary. Flask gives every visitor their own copy and uses a cookie behind the scenes to know which copy belongs to which person.
- **Stateless:** a fancy word for "forgetful." By itself, HTTP treats every request as if it's the very first one it has ever seen: it has no memory of you between requests unless something, like a cookie, adds one.
- **Flask-Session:** a third-party library (separate from Flask itself) that adds real session support to a Flask app and decides where the session data actually lives, by default, as files sitting on the server.
- **Wildcard (in SQL's `LIKE`):** the percent sign `%` inside a `LIKE` pattern means "zero or more of any character here." It turns an exact match into a fuzzy, partial match.
- **API (Application Programming Interface):** a route meant to be called by another program, not read by a human in a browser. Instead of a full web page, it returns raw data.
- **JSON (JavaScript Object Notation):** a plain-text way of writing lists and key-value pairs that almost every programming language can parse. It's the standard format programs use to hand data to other programs.
- **`jsonify()`:** a function that comes with Flask that converts a Python list or dictionary into a proper JSON HTTP response, with the correct headers already attached, ready for any program to read.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

You already know, from Lesson 35, that HTTP is just headers and text flying back and forth, and that by itself, it forgets you the instant a response is sent. That's fine for a static page, but it breaks the moment you want a "you are logged in" message that survives a page reload, or a cart that doesn't empty itself between clicks. Malan calls the fix for this "the juiciest idea for today":

> "That's all a cookie is. It's a key value pair that can be planted on your computer, but it's a wonderfully powerful mechanism for implementing, and this is the juiciest idea for today, I'd argue what are called sessions." (David Malan)

By the end of this lesson, that same small trick (a per-user dictionary tied to a cookie) will carry your login, your shopping cart, and, in the last part, hand your app's data to any other program that asks for it politely, not just a browser showing a page.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain, in plain language, how a cookie lets a stateless HTTP server "remember" a specific visitor across requests.
2. Implement a login/logout flow that stores a username in Flask's `session` and reads it back on later requests.
3. Build a per-user shopping cart using `session["cart"]` as a plain Python list.
4. Write a search route that uses SQL's `LIKE` with `%` wildcards to find partial matches instead of exact ones.
5. Return JSON from a Flask route with `jsonify()` instead of rendering a template, so a program other than a browser can consume the data.

## Prerequisites

- **Module 11 · Lesson 40: A real app: validation and databases**: this lesson assumes you already have a working Flask registration app: routes, forms, GET vs. POST, and rows going in and out of SQLite through CS50's SQL library.
- **Module 10 · Lesson 35: HTTP and the Browser**: cookies ride in the exact same request and response headers you already inspected there.
- **Module 8 · Lesson 29: SQL Fundamentals: CRUD**: you've already met `LIKE` and `%`; today you combine them with a placeholder inside a live route instead of typing them by hand in a terminal.

---

## Part 1: Cookies and sessions (the hand-stamp trick)

Every request you've sent so far has been, on its own, forgetful. Malan names this directly:

> "Sessions are this feature whereby browsers and servers have a persistent connection to each other even though HTTP is what we'll call stateless." (David Malan)

Left alone, a server has no idea that the request hitting `/greet` right now came from the same browser that hit `/` a second ago. So how does a site like Gmail keep you logged in for days? Every time you log in, the server's response quietly includes an instruction to your browser:

> "This is another HTTP header that is usually inside of those virtual envelopes that come back from servers to browsers... it might tell the browser, please set the following cookie." (David Malan)

That instruction is a `Set-Cookie` header, and the cookie itself really is nothing more than a key and a value, often a long, meaningless random string, not your actual username or password:

> "A cookie is just a key value pair." (David Malan)

Malan reaches for a physical-world analogy to make this concrete:

> "If you go to a bar or a club or an amusement park, generally you show your ticket once when you go in and then thereafter you just show your hand if you want to be able to come and go again and again." (David Malan)

The server checks your ticket (your login) exactly once. After that, every time your browser makes another request to that same site, it automatically re-sends the cookie (the equivalent of holding up your stamped hand) inside a `Cookie` header. The server never has to ask who you are again; it just recognizes the stamp.

That stamp is the key to something bigger than "remembering a name." Malan defines it plainly:

> "A session, more concretely, you can think of in Python as a dictionary of key value pairs that you can associate with each and every user." (David Malan)

So a **session** is a dictionary (you can put whatever you want in it, one copy per visitor) and Flask uses the cookie only to figure out *which* copy of that dictionary belongs to the browser making the current request. You never touch the cookie's actual value yourself; you just read and write a normal-looking Python dictionary called `session`, and Flask (with help from a small library called **Flask-Session**) handles the cookie underneath.

Setting this up takes a few lines of boilerplate at the top of `app.py`:

```python
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
```

Malan describes what that configuration is doing:

> "This just says configure this app to use sessions by storing the cookies on the server as files instead of in a database or somewhere else, but this is the default that we use for our examples." (David Malan)

> 🔑 **A session is just a dictionary.** Flask decides, using a cookie your browser sends back automatically, *whose* dictionary you're reading or writing on any given request. You never manage the cookie by hand.

## Part 2: A login/logout demo (usernames only, on purpose)

With `session` available, a login system is almost embarrassingly small. Here is the shape of it, reconstructed from the lecture's example:

```python
@app.route("/")
def index():
    return render_template("index.html", name=session.get("name"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
```

The homepage doesn't need any conditional logic of its own beyond a template check: it just asks the session whether a name is stored, and shows "logged in as ___" or "not logged in" accordingly. Logging in is one line: `session["name"] = request.form.get("name")` stores whatever the visitor typed. Logging out is one line too: `session.clear()` empties the dictionary, which has the effect of erasing everything the server knew about that browser, the equivalent of wiping off the hand stamp.

Notice what's deliberately missing here: a password. Malan is explicit that this is a teaching simplification, not a real login system:

> "I'm again keeping it simple with just user names, no passwords, but as you'll see in Problems at 9, we'll add some passwords to the mix as well." (David Malan)

("Problems at 9" is CS50's own Problem Set 9, Finance: the official next step after this lesson, and exactly where real password handling belongs. More on that in the Capstone below.)

> ❌ **The trap:** never store a real password, or anything else genuinely sensitive, directly inside a cookie or in plain text inside `session`. A session is convenient, not automatically secure. Real logins store a *hashed* password on the server and keep only a meaningless session identifier in the cookie, which is exactly what Problem Set 9 teaches.

> ✅ **What to do about it:** for this lesson and its Capstone, treat "logged in" as nothing more than "a username is sitting in `session`." That's honest about what the demo does, and it's a safe habit for the pedagogical version of login you're about to build.

## Part 3: A shopping cart (one list, one session key)

Once you can stash a username in `session`, storing a shopping cart is the exact same trick applied to a list instead of a string. Malan frames the whole idea this way:

> "A session essentially gives you the ability to implement a shopping cart like this, where the shopping cart, of course, in the real world is specific to each user." (David Malan)

The demo uses a tiny bookstore database (an IMDb-style table of books, each with an `id` and a `title`) and a page that lists every book with an "Add to Cart" button. Each button is a form with a hidden input carrying that book's `id`, submitted by POST to a `/cart` route:

```python
@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = []

    if request.method == "POST":
        id = request.form.get("id")
        if id:
            session["cart"].append(id)
        return redirect("/cart")

    books = db.execute(
        "SELECT * FROM books WHERE id IN (?)", session["cart"]
    )
    return render_template("cart.html", books=books)
```

Two ideas do all the work here. First, `session["cart"]` starts life as an empty list the very first time a visitor shows up, not a database table, not a global variable shared by everyone, just a list that belongs to *this* browser's session. Second, every "Add to Cart" click appends one more book `id` onto that same list, and the `GET` branch turns around and asks the database for every book whose `id` is in that list, so the cart page always reflects exactly what this one visitor has added.

> 🔑 **A cart is nothing more than a list under one session key.** `session["cart"]` behaves like any Python list (append to it, loop over it, look things up by the IDs it contains) except Flask quietly keeps a separate copy for every visitor.

## Part 4: Search as an API (`LIKE`, wildcards, and `jsonify()`)

The last building block starts from something familiar: a search box, like Google's, that queries a table of TV shows. The first version does an exact match:

```python
shows = db.execute("SELECT * FROM shows WHERE title = ?", request.args.get("q"))
```

Typing `The Office` (exact capitalization, exact wording) works. Typing `office` or `the office` returns nothing, because `=` in SQL demands an exact match. This is where `LIKE` and the `%` wildcard you met in Module 8 come back, combined with a placeholder to keep the query safe:

```python
shows = db.execute(
    "SELECT * FROM shows WHERE title LIKE ?", "%" + request.args.get("q") + "%"
)
```

Malan explains exactly what the `%` characters are doing:

> "I want to tolerate zero or more characters to the left via the SQL wildcard and zero or more characters to the right." (David Malan)

Wrapping the visitor's search term in `%` on both sides turns "must match exactly" into "must appear somewhere in this text, in any case", so `office`, `The Office`, and `the office` all now match the same rows. The `?` placeholder still does the job it always does: it lets CS50's SQL library safely insert the visitor's text without ever risking a SQL injection attack, even though the value being inserted now includes those extra `%` characters.

So far, this route still returns a rendered template: a bulleted list of matching titles, meant for a human looking at a browser. But nothing requires that. Malan reframes what a route like this really is:

> "An API is an application programming interface... you can call to get data from someone else's services generally using HTTP, and you can return the data in any number of formats: in text format, in HTML format, or in something called JSON format, which is short for JavaScript object notation." (David Malan)

The same `SELECT ... LIKE ?` query can back two completely different routes: one that renders a template full of `<li>` tags for a human, and one that skips the template entirely and hands back raw data for a program:

```python
from flask import jsonify

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "")
    shows = db.execute(
        "SELECT * FROM shows WHERE title LIKE ?", "%" + q + "%"
    )
    return jsonify(shows)
```

Malan describes what that last function is doing to the rows that came back from the database:

> "I'm using a crazy named function called [j]sonify, which is just another function that comes with Flask itself that has the effect of taking the list of Python dictionaries that came back from my SQL database... [and turning it into something you can] serve it to anyone on the internet, myself included, as a service." (David Malan)

(The lecture transcript renders this word phonetically as "Jasonify": it's Flask's real function, `jsonify()`.) Where `render_template()` hands back a full HTML page meant for a browser to draw on screen, `jsonify()` hands back plain text formatted as JSON (square brackets for a list, curly braces for each row's key-value pairs) with the right HTTP header attached so any program reading the response knows to parse it as JSON, not display it as a page. And this is exactly the same pattern you already saw from the other side, all the way back in Lesson 1:

> "If you now think way back to week 0... where I was writing code that talked to open AI's so-called API to get responses from our server side cat, they were sending us JavaScript object notation like this, and I was just grabbing the data that I actually cared about." (David Malan)

The chatbot in Lesson 1 was the *client* calling someone else's JSON API. Here, you're the one *building* the API: the same shape, from the other side of the conversation.

> 💡 **One query, two audiences.** The SQL query never changes. What changes is only the last line of the route: `render_template(...)` for a human in a browser, `jsonify(...)` for another program. That's the entire difference between a web page and an API.

## Part 5: How the pieces combine

None of these three ideas depend on each other technically, but real apps stack them together constantly: log a user in, remember something about them across multiple requests, and expose a search feature both to people and to other programs.

```text
Browser                                   Flask server
   |  1. POST /login  {name: "david"}        |
   |----------------------------------------->|  session["name"] = "david"
   |  2. Set-Cookie: session=abc123           |
   |<-----------------------------------------|
   |                                          |
   |  3. GET /  Cookie: session=abc123        |
   |----------------------------------------->|  reads session.get("name") -> "david"
   |  4. "logged in as david"                 |
   |<-----------------------------------------|
   |                                          |
   |  5. POST /cart  {id: 2}  Cookie: ...      |
   |----------------------------------------->|  session["cart"].append("2")
   |                                          |
   |  6. GET /api/search?q=office              |
   |----------------------------------------->|  SELECT ... LIKE '%office%'
   |  7. [{"id": 1, "title": "The Office"}]    |  <- jsonify(), not a template
   |<-----------------------------------------|
```

Steps 1-4 are the login demo from Part 2. Step 5 is the cart from Part 3: note it rides on the very same cookie that logging in planted. Steps 6-7 are the API from Part 4, and notice they don't even need a session at all: an API route can be completely public, or you could just as easily check `session.get("name")` inside it too, if you wanted search results limited to what one logged-in user is allowed to see.

---

## Key takeaways

1. **Cookies turn stateless HTTP into something that feels connected.** A `Set-Cookie` header plants a hand stamp; a `Cookie` header presents it again on every later request.
2. **A session is a per-user dictionary, backed by Flask-Session.** You read and write `session[...]` like any Python dict; the cookie is just how Flask knows which visitor's copy to use.
3. **A shopping cart is a list under one session key.** `session["cart"]` starts empty, gets appended to, and is looked up with a single `WHERE id IN (...)` query, nothing more exotic than that.
4. **`LIKE` plus `%` wildcards turn an exact match into a fuzzy search.** Wrapping a search term in `%...%` finds it anywhere in the text, case-insensitively.
5. **`jsonify()` turns a route into an API.** The same SQL query can feed a human-facing HTML page or a machine-facing JSON response: the only difference is the last line of the route.

## Common pitfalls

- ❌ Storing a real password (or anything else sensitive) directly in `session` or a cookie instead of behind a hashed, server-side check: fine for this lesson's pedagogical login, not fine for anything real (that's what Problem Set 9 fixes).
- ❌ Appending to `session["cart"]` without first checking `if "cart" not in session: session["cart"] = []`: the very first visit will crash trying to append to a key that doesn't exist yet.
- ❌ Building a `LIKE` query with an f-string (`f"...LIKE '%{q}%'"`) instead of a placeholder: wrapping in `%` doesn't make string-building safe; you still need `?` to avoid SQL injection.
- ❌ Rendering an HTML template from a route meant to be an API: a third-party program calling `/api/search` doesn't want a full web page back, it wants `jsonify()`'s plain data.

---

## 🛠️ Capstone Project: Give your registration app accounts and an API

> This is the main hands-on project for the lesson. You'll take the database-backed registration app from Lesson 40 and turn it into something that feels like a real product: it knows who you are, it remembers what's yours, and it can talk to other programs, not just browsers.

### What you will build

Starting from your Lesson 40 registration app (name + sport, stored in SQLite), you will add:

- A session-backed login, using a username only (no password), exactly as the lecture does it.
- A logout route that clears the session.
- A per-user "my registrations" view that only shows the rows belonging to whoever is logged in.
- A `/api/search` route that filters registrants with `LIKE` and returns the results as JSON, not HTML.

This is a real piece of your course's north-star project: a database-backed web app with user accounts and an API is exactly what makes a final project feel like a real application instead of a form that dumps into a table.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Sessions (Part 1) | Storing and reading `session["username"]` on every route. |
| Login/logout (Part 2) | Milestones 1 and 2: the login and logout routes themselves. |
| Sessions as per-user state (Part 3) | Milestone 3 and 4: guarding the form and filtering "my registrations" by username. |
| `LIKE` + `jsonify()` (Part 4) | Milestone 5: the `/api/search` route. |

### Milestones (build them in order, each one works on its own)

1. **Add a login route.** `GET /login` shows a form with just a name field, no password. `POST /login` reads `request.form.get("name")`, stores it as `session["username"]`, and redirects to `/`. Done when reloading `/` after logging in shows your name.
2. **Add a logout route.** `GET /logout` calls `session.clear()` and redirects to `/`. Done when `/` goes back to showing "not logged in" afterward.
3. **Guard the registration form.** Before showing or accepting the registration form, check `if "username" not in session` and redirect to `/login` if so. Use `session["username"]` as the registrant's name automatically, instead of asking the visitor to type it again. Done when visiting the registration route while logged out sends you to `/login` first.
4. **Build a "my registrations" view.** Add a route (for example `/my-registrations`) that runs `SELECT * FROM registrants WHERE name = ?` using `session["username"]`, and renders a table of just those rows. Done when two different logged-in usernames each see only their own registrations, never each other's.
5. **Build a JSON search API.** Add `/api/search` that reads `?q=` from `request.args`, runs `SELECT * FROM registrants WHERE name LIKE ? OR sport LIKE ?` with the query wrapped in `%...%`, and returns `jsonify(rows)`, no template. Done when opening `/api/search?q=bas` directly in a browser shows raw JSON (brackets and quotes), not a formatted page.
6. **Stretch goals.** Add a real password field and use `werkzeug.security.generate_password_hash` / `check_password_hash` instead of a bare username: this is precisely what CS50's official **Problem Set 9, Finance,** walks you through next, so treat this milestone as a bridge to that problem set rather than something to fully solve here. Or: make `/api/search` return a friendly JSON error, like `{"error": "missing q"}`, when no query is given.

### How you will know you are done

- ✅ Visiting the registration form while logged out redirects you to `/login` first.
- ✅ Logging in as two different usernames and checking "my registrations" shows two different, non-overlapping tables.
- ✅ `/api/search?q=...` returns a JSON array you can view directly in a browser tab or with `curl`, not an HTML page.
- ✅ You can explain, in one sentence, why this login isn't secure enough for a real product, and name the CS50 problem set (Finance, Problem Set 9) that teaches the fix.

> 💡 **Keep yourself honest:** don't let "no passwords" quietly become your habit outside this lesson. The moment you handle a real password anywhere, hash it. Never store or compare it in plain text.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Welcome back (foundational)
Add a "Welcome back, `<name>`" line and a login/logout link to the homepage of any Flask app you've built, using `session.get("name")` exactly like Malan's `index.html` example in Part 2. Confirm it correctly shows "not logged in" before you log in and your name afterward.

### Exercise 2: A tiny cart (intermediate)
Build (or reuse) a small bookstore-style app with an "Add to Cart" button per item, each submitting a hidden `id` by POST. Store the growing list of IDs in `session["cart"]`, and add a `/cart` page that runs one `SELECT * FROM ... WHERE id IN (...)` query to show everything currently in the cart.

### Exercise 3: One query, two audiences (advanced)
Take any existing `SELECT` query in an app you've built and expose it twice: once as a normal route that renders an HTML template, and once as a `/api/...` route that returns `jsonify()` of the exact same rows. Confirm, by comparing them side by side, that both routes are running the identical query: only the last line differs.

---

## Cheat sheet

```text
COOKIES & SESSIONS
  Set-Cookie: <header the server sends>   plants the "hand stamp"
  Cookie: <header the browser sends>      presents the hand stamp again
  session[...]                            per-user dict, backed by a cookie
  session.clear()                         logs the user out (empties the dict)

LOGIN / LOGOUT (pedagogical: username only, no password)
  session["name"] = request.form.get("name")   # on POST /login
  session.get("name")                          # read it back anywhere
  session.clear()                              # GET /logout
  Real passwords -> hash them (see CS50 Problem Set 9: Finance)

SHOPPING CART
  if "cart" not in session: session["cart"] = []
  session["cart"].append(id)                   # on "Add to Cart"
  SELECT * FROM items WHERE id IN (?)           # to render the cart

SEARCH AS AN API
  WHERE title LIKE ?          with value  "%" + q + "%"     -> fuzzy match
  render_template(...)        -> HTML, for a human in a browser
  jsonify(rows)                -> JSON, for another program to call

GOLDEN RULE
  Same SQL query, different last line: render_template() for people,
  jsonify() for programs. That's the whole difference between a page
  and an API.
```

## How this connects to the rest of the course

- **Earlier, Module 11 · Lesson 40: A real app: validation and databases**: the registration app you validated and connected to SQLite there is exactly what this lesson's Capstone gives accounts and an API.
- **Earlier, Module 10 · Lesson 35: HTTP and the Browser**: cookies ride in the very request and response headers you already learned to inspect there; `Set-Cookie` and `Cookie` are just two more header lines.
- **Earlier, Module 8 · Lesson 29: SQL Fundamentals: CRUD**: you already know `LIKE` and `%`; today's new piece is combining them safely with a placeholder inside a live route, then returning the results as JSON instead of a query result.
- **Earlier, Module 1 · Lesson 1: Welcome to CS50**: an API returning JSON is exactly what the chatbot called; today you built the server side of that same pattern yourself.
- **Next, Module 12 · Lesson 42: Abstraction, precision, and how far you've come**: the course's closing lesson, looking back across everything from Week 0 through the Flask app you can now build, log into, and query from other programs.

---

*Source: "CS50x 2026 - Lecture 9 - Flask" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
