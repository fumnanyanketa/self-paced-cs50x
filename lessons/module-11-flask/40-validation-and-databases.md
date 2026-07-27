# Module 11 · Lesson 40: A Real App: Validation and Databases

> **Course:** Self-Paced CS50x
> **Module 11:** Web apps with Flask: everything so far becomes one real application
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 9 - Flask](https://www.youtube.com/watch?v=am7POvSZ4GE) · [full transcript](../../transcripts/12-lecture-9-flask.txt)
> **Estimated time:** 70 minutes (read plus exercises)

---

## In one sentence

You will rebuild Malan's own 1997 paper-registration site as a live Flask app that never trusts what a visitor types: checking every submission against a real list on the server, storing it permanently in a SQLite database with placeholders instead of raw text, and deleting rows only through a button that a stray link can never trigger.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a mini registration app: a form with a select menu, server-side validation against a Python list, an `INSERT` into SQLite with safe placeholders, a page listing everyone registered, and a POST-only delete button. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** SQL injection is not a Flask quirk or a CS50 invention. It is one of the oldest, best-documented classes of security vulnerability on the web.
>
> - **[OWASP: SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)**, maintained by the Open Web Application Security Project. This is the industry's own reference on why untrusted input concatenated into a query is dangerous, and why parameterized queries (what this lesson calls "placeholders") are the standard fix, the exact defense CS50's SQL library gives you for free.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Server-side validation:** checking that submitted data is actually acceptable using code that runs on your own server, where a visitor cannot see it, change it, or delete it before you check.
- **Select menu:** the HTML drop-down widget (`<select>` with `<option>` tags inside it) that lets a visitor pick from a fixed list instead of typing free text.
- **Global variable:** a variable declared once, outside of any function, so that every function in the file can read it. This lesson uses one to hold the master list of valid sports.
- **`db.execute`:** the one function CS50's Python SQL library gives you to run any SQL statement (`SELECT`, `INSERT`, or `DELETE`) from inside a Flask route.
- **Placeholder:** a `?` you put inside a SQL string in place of a real value, then supply the actual value as a separate argument to `db.execute`. The library escapes it safely so it can never be misread as SQL code.
- **SQL injection:** an attack where someone types SQL syntax (like a stray quote or a `DROP TABLE` statement) into an ordinary form field, hoping an app will paste it directly into a query and let it run.
- **MVC (Model-View-Controller):** a way of organizing a web app into three jobs: the **model** (your persistent data), the **view** (what the user sees, your templates), and the **controller** (the logic deciding what to show, your `app.py`).
- **Static file:** a file (an image, a stylesheet, a script) that Flask serves exactly as-is, with no templating logic applied, from a folder conventionally named `static/`.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 39 got you a form that could `POST` to your own server instead of borrowing Google's. That's a real building block, but a form by itself doesn't *do* anything durable: submit it, and whatever the visitor typed vanishes the moment the response comes back. This lesson is where the pieces from the rest of the course finally combine into one working application, which is exactly how Malan frames the whole week:

> "This week, in particular, the goal is to really synthesize the past 10 weeks of class, drawing upon a lot of the building blocks that are hopefully now, metaphorically in your toolbox and gives you an opportunity now to apply those ideas to new problems." (David Malan)

To make that concrete, Malan rebuilds a website he actually wrote as a Harvard sophomore in 1997 in the language Perl: a registration form for "Frosh IMs," the freshman intramural sports program, that replaced students walking a paper sign-up sheet across Harvard Yard. Rebuilding it live surfaces the exact three problems every real app must solve: can you trust what arrives from the browser (no), where does the data actually live once the server restarts (nowhere, unless you use a database), and how do you let someone remove a row without also letting an email link delete it by accident. This lesson answers all three, and the pattern you build here (a form, a validated `INSERT`, a `SELECT`-driven list, a safe `DELETE`) is the reference architecture for the database-backed web app you'll finish this course with.

## Learning objectives

By the end of this lesson you will be able to:

1. Build an HTML `<select>` menu with `<option>` tags, including a default blank option marked `selected`.
2. Explain why client-side restrictions (like a select menu's fixed choices) can always be bypassed, and write server-side validation that checks submitted data against a Python list instead of trusting the dropdown.
3. Use a Jinja `{% for %}` loop to generate `<option>`, radio button, or checkbox elements dynamically from a single Python list, instead of duplicating HTML by hand.
4. Replace an in-memory Python dictionary with a persistent SQLite database, using `db.execute` to `INSERT` and `SELECT` rows through placeholders that prevent SQL injection.
5. Implement a safe delete: a hidden `id` input, a POST-only `/deregister` route, and an explanation of why a destructive action must never be reachable by `GET`.
6. Serve a static image from a `static/` folder, and explain the Model-View-Controller split between `app.py`, templates, and the database.

## Prerequisites

- **Module 11 · Lesson 39: Forms, layouts, and GET vs POST**: this lesson assumes you can already write a Flask route, extend a `layout.html` with Jinja's `{% block %}`, and submit a form with `method="post"`.
- **Module 8 · Lessons 29-31: SQL fundamentals, relational design, and Python + SQL**: `db.execute`, `INSERT`/`SELECT`, and placeholders were introduced there; this lesson is the first time you use them inside a live web request instead of a script.
- **Module 3 · Lesson 12 and Module 8 · Lesson 31's "never trust input" thread**: the same distrust of user input that motivated escaping and placeholders in SQL comes back here, now aimed at HTML forms too.

---

## Part 1: The Frosh IMs case study (a select menu, built and broken)

Malan sets the stakes with his own history before writing a line of new code:

> "Back when I took CS 50 as a sophomore... it was my sophomore spring maybe or junior fall that I also got involved in the freshman intramural sports program or Frosh IMS for short, and back in the day we would walk from say Matthew's Hall to Wigglesworth freshman year at least, to register for sports by filling out what was called the sheet... and then you would go to the Proctor's dorm room and slide it like under their door or through the mail slot." (David Malan)

He built the original registration site himself, in a language called Perl, and today's rebuild targets that same problem: a name, a sport, and a submit button. The interesting new HTML widget is the **select menu**, the drop-down you get with `<select>` wrapping one or more `<option>` tags:

```html
<select name="sport">
    <option value="" selected>Sport</option>
    <option value="basketball">Basketball</option>
    <option value="soccer">Soccer</option>
    <option value="ultimate frisbee">Ultimate Frisbee</option>
</select>
```

Two details matter here. First, each `<option>` can carry its own `value` attribute, separate from the text the human sees, so the value actually submitted to the server doesn't have to match the visible label exactly. Second, a blank option with `selected` at the top stops the menu from silently defaulting to "Basketball" and registering someone who never touched the dropdown:

> "It's a little presumptuous of me to select basketball by default, and in fact this is kind of inviting user error if they type in their name, don't really think about it, and now register for basketball accidentally." (David Malan)

That blank default plus a `selected` attribute is a small, cheap fix worth remembering any time a form has a meaningful default choice.

> 🔑 **A select menu standardizes what a human can pick, but it does not control what actually arrives at your server.** The dropdown only restricts what's easy to click: anyone with basic developer tools can still submit any value they want, which is exactly what Part 2 confronts.

### The break-in

Once the form worked end to end, Malan opened the browser's developer tools, right-clicked the `<select>`, and added a brand-new option (`volleyball`) that was never in the dropdown to begin with, then submitted it successfully. His conclusion doubles as this lesson's thesis:

> "The short answer is the short, the takeaway here is do not trust user input ever for reasons we've already seen when we discuss SQL ever more so now that we're dealing with the web, because who knows what users are going to do accidentally, foolishly, or even in Kelly's case here maliciously trying to pass data that we did not expect." (David Malan)

If a client-side dropdown were the *only* check, nothing stops that fabricated value from reaching your app. The fix is Part 2's subject: check it again, on the server, where the visitor cannot reach in and edit it.

---

## Part 2: Server-side validation (a global list and a Jinja loop)

### From hardcoded checks to one global list

Malan's first instinct is the most literal one: hardcode every valid sport directly into the check.

```python
sport = request.form.get("sport")
if sport != "basketball" and sport != "soccer" and sport != "ultimate frisbee":
    return render_template("failure.html")
```

It works, but he immediately names the problem with it: the same three sport names now have to be typed twice: once in this `if`, and once again in the HTML `<option>` tags. Add a fourth sport, and you must remember to update both places. His fix is a **global variable**, a list declared once at the top of `app.py` that every route (and, soon, every template) can read:

```python
SPORTS = ["basketball", "soccer", "ultimate frisbee"]
```

All-caps naming here is a Python convention, not a language rule. Python has no real constant, but writing a name in capitals is a signal to yourself and anyone reading the code: "treat this as fixed; don't reassign it." With `SPORTS` defined, the validation check collapses to one clean line:

```python
sport = request.form.get("sport")
if sport not in SPORTS:
    return render_template("failure.html")
```

> ✅ **What to do about it:** whenever the same list of valid values needs to be checked in Python *and* rendered in HTML, put it in exactly one place, a single global list, and have both sides read from it.

### Letting the template read the same list

Because `SPORTS` is now a single source of truth, the template can generate its own `<option>` tags instead of having them typed out by hand. Passing `sports=SPORTS` into `render_template` makes the list available inside Jinja, which supports a `{% for %}` loop with almost the same syntax as Python:

```html
<select name="sport">
    <option value="" selected>Sport</option>
    {% for sport in sports %}
        <option value="{{ sport }}">{{ sport }}</option>
    {% endfor %}
</select>
```

Add a fourth sport to `SPORTS` in `app.py`, and the dropdown grows automatically: no template edit required.

### Radio buttons and checkboxes: the same loop, a different `type`

Select menus aren't the only widget for choosing from a fixed list. A `{% for %}` loop over the same `SPORTS` list can just as easily generate **radio buttons** (mutually exclusive, because every input shares one `name`):

```html
{% for sport in sports %}
    <input type="radio" name="sport" value="{{ sport }}"> {{ sport }}
{% endfor %}
```

Later in the lesson, Malan changes a student's ability to register for more than one sport at once by making exactly one edit (swapping `radio` for `checkbox`), which turns the mutually-exclusive buttons into independently selectable ones. Reading multiple checked values back on the server, though, needs a different method than the one you've used so far: `request.form.get` only ever returns one value, so multiple checkboxes sharing a `name` require `request.form.getlist("sport")` instead, which returns a Python list. Validating that list means looping over every sport the visitor checked and confirming each one individually is in `SPORTS`: one invalid box among several should still fail the whole submission.

### A dedicated error page

A generic "you are not registered" message is technically correct but not helpful. Malan's fix is a dedicated `error.html` template that a route can pass a specific message into:

```python
name = request.form.get("name")
if not name:
    return render_template("error.html", message="missing name")

sport = request.form.get("sport")
if not sport:
    return render_template("error.html", message="missing sport")
if sport not in SPORTS:
    return render_template("error.html", message="invalid sport")
```

```html
{% block body %}
    <h1>Error</h1>
    <p>{{ message }}</p>
{% endblock %}
```

Each `if` checks one specific thing and fails with one specific, human-readable reason ("missing name," "missing sport," "invalid sport") instead of one catch-all failure message for every possible mistake.

> 🔑 **The single most important takeaway of this part.** Never trust that a dropdown, radio button, or checkbox actually restricts what arrives at the server. Keep the list of valid values in exactly one place (a global list), check every submission against it in Python, and give the visitor a specific reason when it fails.

---

## Part 3: Persisting data (from a dictionary to SQLite)

### Why a dictionary in memory isn't enough

Malan's first working version of the registrants list is almost embarrassingly simple: a global Python dictionary.

```python
REGISTRANTS = {}
# later, in the register route:
REGISTRANTS[name] = sport
```

It works (reload the `/registrants` page and everyone who registered is there) right up until the server restarts. Malan demonstrates this live: after tweaking `app.py`, Flask automatically reloads the file, the module-level code reruns, `REGISTRANTS = {}` executes again, and every registrant that existed a moment ago is simply gone.

> "The catch though is if this server ever goes offline, maybe because it needs to be updated or it crashes or it reboots... Flask server is no longer running, which means that global variable called registrants in all caps is gone. It's like free the memory has been freed." (David Malan)

The fix returns to a tool this course already built in Module 8: a real database, whose whole point is that it survives the process that's reading and writing it.

### Wiring up CS50's SQL library

The setup mirrors what Lesson 31 already covered, now inside a Flask app instead of a standalone script:

```python
from cs50 import SQL

db = SQL("sqlite:///froshims.db")
```

The database itself already has a `registrants` table with three columns: `id` (an integer primary key), `name`, and `sport`, both declared `NOT NULL` so the database itself refuses a blank submission as a second line of defense.

### `INSERT` with placeholders, not string-building

With validation already confirming the name and sport are present and the sport is in `SPORTS`, storing the registration is one line:

```python
db.execute("INSERT INTO registrants (name, sport) VALUES (?, ?)", name, sport)
```

Malan is emphatic about why the values are passed as separate arguments after the query string, rather than built into the string itself with an f-string:

> "Here's where you do not want to make yourself vulnerable to SQL injection attacks. No F strings in here, no just plugging students' input in blindly. This is where and why we use these placeholders in both CS 50's library and in many libraries in the real world to specify that I want the library to properly sanitize the user's input and get rid of any scary characters like apostrophes or semicolons or the like." (David Malan)

Each `?` is a **placeholder**. `db.execute` fills them in with the extra arguments you pass, escaping anything that could otherwise be misread as SQL syntax: a stray apostrophe in someone's name can't accidentally close a string early, and a malicious semicolon can't start a second, unintended statement. This is the exact SQL injection concern from Module 8, now facing a wide-open internet form instead of a script you control yourself.

### `SELECT` to read it all back

Reading the registrants back out uses the same `db.execute`, this time with a `SELECT`:

```python
registrants = db.execute("SELECT * FROM registrants")
```

`db.execute` on a `SELECT` returns a **list of dictionaries**: one dictionary per row, each with keys matching the column names. The template loops over that list with the same Jinja `{% for %}` syntax used for the sport dropdown:

```html
<table>
    <thead>
        <tr><th>Name</th><th>Sport</th></tr>
    </thead>
    <tbody>
        {% for registrant in registrants %}
            <tr>
                <td>{{ registrant.name }}</td>
                <td>{{ registrant.sport }}</td>
            </tr>
        {% endfor %}
    </tbody>
</table>
```

The payoff is immediate and durable: register a few people, kill the Flask server with Control-C, restart it, and reload `/registrants`. Everyone is still there, because the data lives in `froshims.db` on disk, not in the process's memory.

> "The database is persistent, which was the whole point of using SQL from week 7 onward." (David Malan)

> 🔑 **The single most important takeaway of this part.** An in-memory dictionary disappears the instant the server process ends. A SQLite database, written to with `db.execute` and placeholders, survives restarts. Placeholders are what keep a hostile name or sport from becoming a SQL command instead of a value.

---

## Part 4: Deleting rows safely (hidden IDs and a POST-only route)

### Why you delete by ID, not by name

Two different students can share a name; only the row's `id`, the primary key from Module 8, uniquely identifies one registration. Malan draws this out by asking what information the browser needs to send back to delete exactly one row, and the answer is the same primary key you've already met:

```text
SELECT * FROM registrants;
 id | name  | sport
----+-------+------------------
  1 | David | basketball
  2 | Kelly | soccer
```

Deleting "Kelly" by name risks catching a second Kelly later; deleting `id = 2` never does.

### A hidden input carries the ID without displaying it

Every row on the registrants page gets its own small form with a hidden field carrying that row's ID, plus a visible delete button:

```html
<form action="/deregister" method="post">
    <input type="hidden" name="id" value="{{ registrant.id }}">
    <input type="submit" value="Deregister">
</form>
```

`type="hidden"` means the field is submitted exactly like any other input, but never rendered on the page for the visitor to see or edit by hand: the ID travels invisibly, tied to whichever row's button was actually clicked.

### The `/deregister` route

On the server, the route pulls that ID out of the POST body and runs a targeted `DELETE`, using a placeholder exactly as before:

```python
@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect("/registrants")
```

### Why this must never be a GET route

Malan makes the strongest safety point of the lesson here, and it is worth reading in full:

> "The catch with using get is that by definition you can visit that resource, that route by just typing in a URL or following a hyperlink. So for instance, if an adversary were to type a URL like slash registrants question mark ID equals... and then send me this URL in an email or send this URL in an email to the proctor who's running the Frosh IMs program. If that Proctor simply clicks naively on this link... Doug gets deregistered just because the proctor followed a link in their email." (David Malan)

He generalizes the rule immediately after:

> "In general post requests are preferred any time there's anything remotely personally identifiable or remotely destructive, like actually changing data on the database like this." (David Malan)

A `GET` request is, by design, anything a browser can trigger just by *visiting* a URL: typing it, following a link, even an image tag pointed at it. A destructive action reachable by `GET` can be triggered by an unsuspecting click, an embedded link in an email, or a phishing page, with no button, no confirmation, and no "are you sure?" in between. Restricting `/deregister` to `methods=["POST"]` means the only way to trigger it is to actually submit a form, which, practically speaking, means clicking a real button on a real page you control.

> ❌ **The trap:** any route that changes or deletes data on the server should never be reachable by a plain `GET`. If clicking a link (or loading a page) alone could trigger it, that link is a loaded gun pointed at your database.

---

## Part 5: Static files and MVC (how it all fits together)

### Serving a static image

Late in the demo, Malan adds an image to the error page and hits a broken-image icon, because the browser looks for `cat.jpeg` relative to the page, not relative to `app.py`. Flask's fix is a naming convention:

> "For organizational sake, any images you want to display on a page or any CSS files or JavaScript files that you want to embed in a page, if they're static assets should actually be in a folder called static, and by static that just means unchanging." (David Malan)

Anything placed in a folder literally named `static/` is served automatically at the URL path `/static/<filename>`: no route needs to be written for it. The one detail to hold onto: `render_template` already knows to look in `templates/` without you ever typing that folder name, but a static asset's path in your HTML must spell out `/static/` explicitly:

```html
<img src="/static/cat.jpeg" alt="grumpy cat">
```

### The MVC paradigm, named

Stepping back from the code, Malan names the pattern the whole app has followed all lesson:

> "The paradigm that we've essentially been implementing is this. If this shape over here represents the human or the user, they keep interacting with what the world generally calls a view... app.ie is technically what the world would call controller logic or business logic... So the views that we're referring to here is like everything in your templates. Those are your views. But there's a third piece of the puzzle... generally called a model... your model is generally your persistent data." (David Malan)

| Piece | What it is in this app | Job |
|---|---|---|
| **Model** | `froshims.db` (the SQLite database) | Stores the data that outlives any single request. |
| **View** | `templates/*.html` (Jinja templates) | Everything the visitor actually sees and submits. |
| **Controller** | `app.py` (Flask routes) | Decides which view to render, validates input, and reads/writes the model. |

Malan is careful to note the lines blur in practice (templates hold loops and conditionals too), but the mindset is what matters: **M**odel-**V**iew-**C**ontroller, or **MVC**, is the standard way the industry talks about organizing exactly this split. Every Flask app you build from here forward, in this course and beyond, uses this same three-part shape.

```text
   visitor's browser
          │
          ▼
     app.py (Controller)
   validate → decide what to render
     │                    │
     ▼                    ▼
templates/*.html      froshims.db
   (View)               (Model)
  what the user      persistent rows,
     sees            survives restarts
```

---

## Key takeaways

1. **A select menu, radio group, or checkbox list only restricts what's easy to click, never what actually arrives.** Anyone can edit the submitted value with developer tools.
2. **"Do not trust user input ever."** Validate every submission on the server, against a single global list (like `SPORTS`), not just once in a dropdown.
3. **Jinja's `{% for %}` loop lets one Python list drive both your validation and your HTML**: add a sport in one place, and the dropdown, the checks, and the template all stay in sync.
4. **An in-memory dictionary dies with the process; a SQLite database, written through `db.execute`, survives a restart.**
5. **Placeholders (`?`) are what keep a user's name or input from being read as SQL code**: never build a query with an f-string using raw user input.
6. **Delete by primary key (`id`), never by a field like `name` that might not be unique**, and pass that ID through a hidden form field.
7. **Any route that deletes or changes data must be POST-only.** A `GET`-triggerable delete can be fired by a stray link, an email, or a phishing page, no button required.
8. **Static assets (images, CSS, JS) live in a `static/` folder and are referenced as `/static/filename`**, while templates need no folder prefix at all.
9. **MVC, Model (database), View (templates), Controller (`app.py`),** is the standard shape of a Flask app, and every lesson in this module has been building toward it.

## Common pitfalls

- ❌ Trusting that because a value came from a `<select>` or a set of radio buttons, it must be one of the options you offered: it must still be checked in Python against your global list.
- ❌ Duplicating the list of valid choices in both `app.py` and the template by hand, instead of passing one global list into `render_template` and looping over it with Jinja.
- ❌ Building a SQL query with an f-string or string concatenation using raw form input: always use a `?` placeholder and pass the value as a separate argument to `db.execute`.
- ❌ Storing registrants (or any data you care about) in a plain Python dictionary or list: it evaporates the moment the server restarts or crashes.
- ❌ Deleting a row by a non-unique field like `name`, or worse, making the delete route reachable by `GET`: both risk deleting the wrong row, or the right row by accident.
- ❌ Forgetting that a static image needs the `/static/` prefix in its `src`, even though templates never need a `/templates/` prefix in `render_template`.

---

## 🛠️ Capstone Project: Build a Mini Registration App

> This is the main hands-on project for the lesson. You will build, on cs50.dev, a small but complete version of Frosh IMs: a form with a select menu, server-side validation against a Python list, a real SQLite `INSERT`, a page that lists everyone via `SELECT`, and a safe, POST-only delete button. This is the reference architecture for the database-backed web app you'll build as this course's capstone.

### What you will build

A Flask app, `app.py`, with a `templates/` folder containing at minimum `layout.html`, `index.html` (the form), `error.html`, and `registrants.html` (the list with delete buttons), plus a `roster.db` SQLite database with one table.

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Select menu with `<option>`/`selected` (Part 1) | The registration form's category dropdown. |
| Global list + server-side validation (Part 2) | Rejecting any submission not in your list, even a hacked one. |
| Jinja `{% for %}` loop (Part 2) | Generating the dropdown's options from that same list. |
| `db.execute`, `INSERT`, placeholders (Part 3) | Storing each registration safely. |
| `SELECT` + `{% for %}` over a list of dicts (Part 3) | The registrants table. |
| Hidden `id` input + POST-only route (Part 4) | The delete button. |
| MVC / static folder (Part 5) | Explaining your own file layout in one sentence. |

### Milestones (build them in order, each one works on its own)

1. **Scaffold the app.** On cs50.dev, create `app.py`, `requirements.txt` (containing `flask` and `cs50`), and a `templates/` folder with `layout.html`. Confirm `flask run` serves a blank page.
2. **Build the form with a select menu.** In `index.html`, add a name text input and a `<select name="category">` with a blank `selected` default option plus at least three real options (e.g., categories of your choosing: book genres, sports, whatever fits your theme). Confirm the form renders and, for now, submits anywhere without erroring.
3. **Add the global list and server-side validation.** In `app.py`, define `CATEGORIES = [...]` as a global list matching your options. Add a `/register` route (`methods=["POST"]`) that checks the name is present and the category is in `CATEGORIES`, returning `error.html` with a specific message for each failure case (missing name, missing category, invalid category). Done when submitting a blank form, and when hand-editing the dropdown in developer tools to submit an invalid value, both correctly fail with the right message.
4. **Loop the dropdown from the same list.** Pass `categories=CATEGORIES` into `render_template` for `index.html`, and replace your hardcoded `<option>` tags with a Jinja `{% for %}` loop over `categories`. Done when adding a fourth item to `CATEGORIES` in `app.py` alone makes it appear in the dropdown with no template edit.
5. **Create the database and insert on success.** Using `sqlite3 roster.db`, create a `registrants` table with `id` (integer primary key), `name` (text, not null), and `category` (text, not null). In `app.py`, connect with `db = SQL("sqlite:///roster.db")` and, on successful validation, run `db.execute("INSERT INTO registrants (name, category) VALUES (?, ?)", name, category)`. Done when you can register someone, then confirm the row exists with `sqlite3 roster.db "SELECT * FROM registrants;"`.
6. **List everyone with SELECT.** Add a `/registrants` route that runs `db.execute("SELECT * FROM registrants")` and renders `registrants.html`, looping over the results in a table. Done when the page shows every row, and still shows them after you restart `flask run`.
7. **Add a safe delete.** In `registrants.html`, give each row its own small `<form method="post" action="/deregister">` with a hidden `id` input carrying that row's ID. Add a `/deregister` route restricted to `methods=["POST"]` that deletes `WHERE id = ?` using a placeholder, then redirects back to `/registrants`. Done when clicking delete removes exactly that row and no other, and visiting `/deregister` directly in the URL bar (a `GET`) correctly fails with "Method Not Allowed."
8. **Stretch goals.** Add a static image (in a `static/` folder) to your error page; switch the category input from a select menu to checkboxes and support registering for multiple categories at once using `request.form.getlist`; or write, in your own words, a one-paragraph explanation of which files in your project are the Model, the View, and the Controller.

### How you will know you are done

- ✅ Submitting the form with a blank name, a blank category, or a hand-edited invalid category each produces a specific, correct error message, never a server crash.
- ✅ A successful registration appears in `/registrants` immediately, and is still there after you stop and restart `flask run`.
- ✅ Clicking "Deregister" removes exactly the row it was clicked on, verified by checking `sqlite3 roster.db "SELECT * FROM registrants;"` before and after.
- ✅ Typing the `/deregister` URL directly into the address bar (a `GET` request) fails with a "Method Not Allowed" error rather than deleting anything.
- ✅ You can point to the exact line in your code where a placeholder (`?`) protects an `INSERT` or `DELETE` from SQL injection.

> 💡 **Keep yourself honest:** before moving on, actually try to break your own form the way Kelly broke Malan's: open developer tools, hand-edit the dropdown to add a fake option, and submit it. If your app doesn't catch it, your validation lives only in the browser, not on the server.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Break your own dropdown (foundational)
Take any form with a `<select>` you've built (in this lesson or the Capstone), open developer tools, and add a fake `<option>` that was never in your list. Submit it. If your app accepts it, add the missing server-side check against your global list; if it already rejects it, write one sentence explaining exactly which line caught it.

### Exercise 2: Radio buttons to checkboxes (intermediate)
Starting from a single-choice form using radio buttons, convert it to checkboxes so a visitor can select more than one option. Update your route to use `request.form.getlist` instead of `request.form.get`, and update your validation to loop over every selected value and reject the whole submission if even one is invalid.

### Exercise 3: Prove the placeholder matters (advanced)
In a throwaway copy of a project with a SQLite database, temporarily rewrite one `INSERT` to build its SQL with an f-string instead of a placeholder (for example, inserting a name directly into the query string). Try submitting a name containing a single quote (like `O'Brien`) and observe what happens. Then revert to the placeholder version and confirm the same input now works correctly: direct, hands-on evidence of what placeholders are actually protecting you from.

---

## Cheat sheet

```text
SELECT MENU (HTML)
  <select name="category">
      <option value="" selected>Category</option>
      <option value="x">X</option>
  </select>

SERVER-SIDE VALIDATION (app.py)
  CATEGORIES = ["a", "b", "c"]        global list, single source of truth
  if value not in CATEGORIES: ...     always re-check on the server

JINJA LOOP (template)
  {% for item in items %}
      <option value="{{ item }}">{{ item }}</option>
  {% endfor %}

RADIO vs CHECKBOX
  radio    -> same name = mutually exclusive -> request.form.get(name)
  checkbox -> same name = multi-select       -> request.form.getlist(name)

SQLITE VIA CS50'S LIBRARY
  from cs50 import SQL
  db = SQL("sqlite:///app.db")
  db.execute("INSERT INTO t (a, b) VALUES (?, ?)", a, b)   -- Create
  db.execute("SELECT * FROM t")                             -- Read (list of dicts)
  db.execute("DELETE FROM t WHERE id = ?", id)               -- Delete

PLACEHOLDERS
  ALWAYS:  db.execute("... WHERE id = ?", id)
  NEVER:   db.execute(f"... WHERE id = {id}")   <- SQL injection risk

SAFE DELETE PATTERN
  <input type="hidden" name="id" value="{{ row.id }}">
  @app.route("/delete", methods=["POST"])   <- POST only, never GET

MVC
  Model      = database (persistent data)
  View       = templates/ (what the user sees)
  Controller = app.py (routes, validation, logic)

STATIC FILES
  static/cat.jpeg  ->  <img src="/static/cat.jpeg">   (explicit /static/ prefix)
  templates/x.html ->  render_template("x.html")      (no /templates/ prefix)

THE ONE RULE THAT MATTERS MOST
  Do not trust user input ever. Validate on the server. Delete only via POST.
```

## How this connects to the rest of the course

- **Earlier, Module 11 · Lesson 39 (Forms, layouts, and GET vs POST):** gave you a form that could `POST` to your own route and a `layout.html` you extend with `{% block %}`; this lesson is the first time that route actually keeps what it receives.
- **Earlier callback, Module 8 · Lessons 29-31:** `db.execute`, `INSERT`/`SELECT`, and placeholders were introduced there against a standalone script; this lesson is where they move inside a live, internet-facing Flask route.
- **Earlier callback, Module 3 · Lesson 12 and Module 8 · Lesson 31:** the "never trust input" instinct you built around command-line arguments and SQL strings is exactly the instinct this lesson applies to HTML forms.
- **Next, Module 11 · Lesson 41 (Sessions, carts, and APIs):** builds on this same app shape to add logins, per-visitor shopping carts, and JSON APIs, all still resting on the validate-then-persist pattern from this lesson.
- **North star:** the form, validation, `INSERT`/`SELECT`, and safe delete you build in this Capstone are the exact reference architecture for the database-backed web app you finish this course with.

---

*Source: "CS50x 2026 - Lecture 9 - Flask" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
