# Module 11 · Lesson 38: Flask Fundamentals: Routes and Templates

> **Course:** Self-Paced CS50x
> **Module 11:** Web apps with Flask: everything so far becomes one real application
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 9 - Flask](https://www.youtube.com/watch?v=am7POvSZ4GE) · [full transcript](../../transcripts/12-lecture-9-flask.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

Instead of a URL pointing at a literal file the way it did with plain HTML, a Flask **route** is a URL wired to a Python function you write yourself, and by the end of this lesson that function will read a name straight out of the URL and hand it to a Jinja **template**, which is the smallest possible skeleton of every dynamic website you use every day.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build **hello-flask**: a tiny Flask app with a route that greets whoever's name shows up in the URL, defaulting politely when nobody gives one, plus a second route that proves the pattern scales past a single page. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Flask itself is barely a decade and a half old, and some future framework will eventually replace it. But the contract it's quietly built on top of (a standard, tool-agnostic way for a web server to hand a Python program a request and get a response back) is written down and version-controlled like any other spec:
>
> - **[PEP 3333: Python Web Server Gateway Interface (WSGI) v1.0.1](https://peps.python.org/pep-3333/)** (Python Software Foundation, 2010). This is the actual specification that lets any Python web framework, Flask included, accept an incoming URL and request as plain, standardized input and hand back a response as plain, standardized output. Whatever framework you use ten years from now, if it's written in Python, it is almost certainly still speaking WSGI underneath, for exactly the reason this lesson opens with: a URL has stopped being a file path and started being generic input to your program.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Route:** the specific path portion of a URL (like `/` or `/greet`) that your program associates with one particular block of code, so that different URLs can trigger different behavior instead of all pointing at files.
- **Query string:** the part of a URL after a `?`, made of one or more `key=value` pairs joined by `&`: a way of sending small pieces of input to a program through the URL itself, like `?name=David`.
- **Framework (here, a micro-framework):** a library of code someone else already wrote, plus a set of conventions you're expected to follow, that handles the repetitive "commodity" work of building an application so you only have to write the logic specific to your own problem.
- **Decorator:** special Python syntax, written with an `@` symbol directly above a function definition, that changes how that function behaves. Flask uses one, `@app.route(...)`, to attach a URL to the function written just beneath it.
- **Template:** an HTML file that isn't quite finished: it has placeholders inside double curly braces, `{{ }}`, that get filled in with real values right before the page is sent to the browser.
- **Jinja:** the templating library bundled with Flask that knows how to read a template file and substitute real values into its `{{ }}` placeholders.
- **`request.args`:** a dictionary-like object, provided by Flask, holding every key/value pair that arrived in the current URL's query string.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Every module up to this point has been building one piece of a puzzle: C's logic, Python's simplicity, SQL's storage, HTML's structure, CSS and JavaScript's polish. This lesson is where those pieces stop being separate exercises and start being one program. As Malan puts it at the very start of the lecture this lesson is drawn from:

> "We come full circle and bring back a server side component whereby we'll again write some Python, we'll again write some SQL code and use it to make our full fledged own web applications." (David Malan)

Concretely, that means two things change today. First, the URL itself changes meaning: in Lesson 36 you served literal files with `http-server`, and a URL like `/about.html` meant exactly one thing: go find that file. Starting today, a URL is an instruction to run a Python function, and Flask hands that function whatever came after the `?` as input. Second, your HTML stops being static: it becomes a **template**, filled in fresh on every request. This is the first lesson where you write `def` and get back a real web page, the same `def` you first wrote in Module 7 · Lesson 26, now answering the exact GET requests you inspected with `curl` and DevTools back in Lesson 35.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain how a Flask route generalizes a URL from "a literal file path" into "generic input to a program," including how a query string carries `key=value` pairs after a `?`.
2. Install Flask with `pip` and a `requirements.txt` file, and scaffold a minimal `app.py` using `Flask(__name__)` and the `@app.route` decorator.
3. Return a response from a route as plain text, and then as a full HTML string, and explain the difference by viewing the page's source.
4. Move hard-coded HTML out of `app.py` and into a `templates/index.html` file, rendering it with `render_template()`.
5. Read a query parameter safely with `request.args`, and replace an `if`/`else` fallback with the one-line `request.args.get("name", "world")`.

## Prerequisites

- **Module 10 · Lesson 35 (HTTP and the browser):** you already know what a GET request and a query string are, and how to read status codes like 400 and 404. This lesson is where your own code starts answering those requests instead of just observing them.
- **Module 7 · Lesson 26 (Loops, functions, and exceptions):** you already know how to write a Python function with `def`. Every Flask route is, underneath the decorator, exactly one of those.
- **Module 10 · Lesson 36 (Building pages with HTML):** you already know how to write a valid HTML document by hand. Templates in this lesson are that same HTML, just missing a few values.
- Comfort with a cs50.dev terminal and `pip`, from earlier modules.

---

## Part 1: From file paths to routes

Recall from Lesson 36 that `http-server` served up whatever was literally sitting in your folder: visit `/about.html` and it handed back the bytes of the file called `about.html`. That was the entire model: a URL was a path on disk, full stop. Malan names the shift that's about to happen to that model:

> "So today we're going to generalize that at least in terms of nomenclature and start talking more about routes, because essentially in web programming we are going to exercise a lot more control over what is in the URL." (David Malan)

A **route** is a URL your program has decided to answer with code, not a file it happens to find. And routes come with a companion idea you've already half-seen if you've ever searched Google: the **query string**. Anything after a `?` in a URL is `key=value` input, with multiple pairs joined by `&`:

```text
STATIC FILE ERA (Lesson 36's http-server)
  https://example.com/about.html   →  looks for the literal file about.html on disk

ROUTE ERA (Flask, starting today)
  https://example.com/greet?name=David   →  runs the Python function tied to the route "/greet"
                                             "name=David" arrives as input, not a filename
```

This is exactly what was happening every time you searched Google in earlier lessons:

> "Question mark cats just meant that the query parameter, the input from the web form, is going to contain in this particular example the word cats." (David Malan)

Building the machinery that turns a raw URL into usable input (splitting it at the `?`, splitting again at each `&`, pulling apart every `key=value`) is exactly the kind of code nobody wants to write from scratch. That is precisely the gap a **framework** fills:

> "The sort of commodity stuff that like literally every web application on the internet has to do anyway" (David Malan)

so, in his words, "we don't have to retrace those steps ourselves." That framework, for this course, is Flask, the subject of the rest of this lesson.

> 🔑 **The single most important takeaway of this part.** A URL is no longer a path to a file. Starting today, it's generic input: a route your own code answers, plus an optional query string of `key=value` pairs your code gets to read.

## Part 2: Flask itself (pip, requirements.txt, and app.py)

Flask is what the transcript calls a **micro-framework**:

> "Flask is a framework as the world would say, or more specifically, a micro framework, which just means it's a library of code that other people wrote to make it easier for us to implement web applications." (David Malan)

Getting it involves the same `pip` command you met installing other Python packages:

```text
$ pip install flask
```

By convention, real projects don't rely on you remembering that command: they list every library the project needs, one per line, in a file called `requirements.txt`, so anyone (a teammate, or a fresh cs50.dev codespace) can reinstall everything with one command:

```text
requirements.txt
─────────────────
flask
```

```text
$ pip install -r requirements.txt
```

With Flask installed, the minimal possible application needs exactly one file, `app.py`, containing this much code:

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world"
```

Line by line: `from flask import Flask` gives you access to the `Flask` function itself. `app = Flask(__name__)` turns this file into a Flask application, using Python's own `__name__` variable, the same special variable behind the `if __name__ == "__main__":` guard from Module 7 · Lesson 26, just used here for a different purpose: telling Flask which file it's running from.

Then comes the new syntax:

> "What's generally called a Python decorator ... a type of function that essentially affects the behavior of the function right after it." (David Malan)

`@app.route("/")` is that decorator. It tells Flask: whenever a visitor requests the route `/`, call the function defined immediately below (here, `index()`) and send back whatever it returns. You can name the function anything; `index` is just the convention for "the site's default page."

Run it with `flask run`, and (unlike `http-server`'s default of port 8080) Flask listens on **port 5000** by default. Visit the page and view its source, and you'll see something worth noticing: it's a single line of plain text, `Hello, world`, with no HTML at all. The browser is politely filling in the blanks of a minimal page for you; the server sent nothing but that one string. Return an actual HTML string instead, and the difference shows up immediately in view-source:

```python
@app.route("/")
def index():
    return "<!DOCTYPE html><html lang='en'><head><title>hello</title></head><body>hello, world</body></html>"
```

Now the browser really did receive full HTML, but hard-coding an entire page as one long string inside `app.py` is exactly the kind of tangled, unfactored code Lesson 37 already taught you to avoid with CSS and JavaScript. Part 3 fixes it.

> ✅ **What to do about it:** the moment you catch yourself writing HTML as a Python string, stop: that HTML belongs in its own file, which is exactly what a template is for.

## Part 3: Templates and Jinja (factoring the HTML back out)

Flask ships with a second useful function, `render_template()`, whose entire job is to read an HTML file from disk and send it back as the response, but that file has to live in one very specific place:

> "It turns out per flask's documentation, if you want to create your own HTML files, you simply have to add a directory that by convention is called templates, and that's it." (David Malan)

So, alongside `app.py` and `requirements.txt`, you need a folder literally named `templates` (all lowercase), containing your HTML:

```text
hello-flask/
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>hello</title>
    </head>
    <body>
        hello, world
    </body>
</html>
```

Notice `render_template("index.html")` names only the file, never the `templates/` folder itself. Flask already knows to look there.

At the moment, this HTML file is no different from the ones you wrote by hand in Lesson 36: it's just static text, quietly relocated. What makes it a genuine **template** is the ability to leave a gap for a real value to be dropped in later:

> "It's kind of the blueprint for the web page I want the user to see, but it's going to be dynamically generated using indeed this blueprint by plugging in the value." (David Malan)

That gap is written with a pair of double curly braces:

```html
hello, {{ placeholder }}
```

> "By using these pairs of curly braces, I'm telling Flask that I want to interpolate, so to speak, that variable. I want to substitute in its value." (David Malan)

To fill it in, pass a named argument to `render_template()` matching the name inside the braces:

```python
@app.route("/")
def index():
    return render_template("index.html", placeholder="David")
```

**Interpolate**, here, just means "substitute a real value into a placeholder." This is Jinja, the templating library bundled with Flask, doing the substitution, the same basic idea as an f-string in Python, just written for an HTML file instead of a line of code.

> 🔑 **The single most important takeaway of this part.** A template is HTML with `{{ }}` gaps in it. `render_template()` fills those gaps with whatever named values you hand it, and it always looks inside a folder called exactly `templates`.

## Part 4: Reading the URL (request.args and defaults)

Hard-coding `"David"` into `render_template()` isn't useful: the whole point is to greet whoever actually visits. That value should come from the query string, and Flask hands it to you through a special object:

> "You have access to a special global variable ... where args just means the arguments or the parameters that were passed in to this HTTP request." (David Malan)

`request.args` behaves like a dictionary: the key is the parameter's name from the URL, the value is whatever the visitor typed after the `=`. The first, most literal way to use it is a conditional, checking whether the key is even there before reading it:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    if "name" in request.args:
        name = request.args["name"]
    else:
        name = "world"
    return render_template("index.html", placeholder=name)
```

That `else` branch is not optional decoration. Skip it (read `request.args["name"]` directly with no check) and visiting the bare route with no query string at all breaks the app outright:

> "This is sort of bad, bad request. It's an HTTP 400 ... 400 just means the user did something wrong by not passing in the parameter that was expected." (David Malan)

That's the exact status code from Lesson 35, now caused by your own code instead of observed from someone else's server. The `if`/`else` above is what prevents it.

Because "check if a query parameter exists, and fall back to a default if it doesn't" is something practically every route ever written needs to do, Flask folds all four of those lines into one:

> "It turns out this is so common to just ask a question as to whether the parameter is there and then do something with it or not that flask comes with some logic to do this." (David Malan)

```python
@app.route("/")
def index():
    name = request.args.get("name", "world")
    return render_template("index.html", name=name)
```

`request.args.get("name", "world")` means exactly what it says: get the query parameter called `name`; if it isn't there, use `"world"` instead. One line replaces four, and it can never raise the error the naive version could. Note also the small renaming from `placeholder` to `name` in both the template and the function call: `name=name` looks odd at first, but it's a real Flask convention worth adopting: the left-hand `name` is the placeholder inside the template, the right-hand `name` is the Python variable holding the value, and giving them the same word keeps a file with many placeholders readable.

> 💡 **A nuance worth catching now.** An *absent* key and a *present-but-empty* key are not the same thing. Visit `/?name=David` and you get "David." Visit `/` with no query string at all, and the default `"world"` kicks in. But visit `/?name=` (the key is there, just with nothing after the `=`) and `.get()`'s default never fires at all, because the key genuinely exists. You'll see "hello, " with nothing after it, not "hello, world."

> ✅ **What to do about it:** always give `request.args.get()` a sensible default as its second argument, and remember that a default only protects you against a *missing* key, not an empty one.

## Part 5: How the pieces combine

Put together, a single request now flows through your route, your query string, and your template in one pass:

```text
 browser:  GET /?name=David
              │
              ▼
 app.py:  @app.route("/")
          def index():
              name = request.args.get("name", "world")   →  "David"
              return render_template("index.html", name=name)
              │
              ▼
 templates/index.html:   hello, {{ name }}
              │
              ▼
 response sent to browser:   hello, David
```

Nothing here is hidden or magic: it's a `def` (Lesson 26), answering a GET request with a query string (Lesson 35), returning HTML (Lesson 36), just generated fresh, on the server, on every single request, instead of sitting on disk unchanged.

---

## Key takeaways

1. **A route replaces a file path with a function.** `@app.route("/greet")` tells Flask to run the `def` right beneath it whenever that URL is visited: the URL is input, not a location on disk.
2. **A query string is `key=value` pairs after a `?`,** joined by `&` when there's more than one, and Flask parses all of it for you so you never touch raw text after the `?` yourself.
3. **`Flask(__name__)`, `@app.route`, and `flask run` on port 5000 are the whole minimal skeleton**: everything else in this lesson builds on those three pieces.
4. **`render_template()` always looks in a folder named exactly `templates`,** and a template is just HTML with `{{ }}` gaps that Jinja fills in with values you pass by name.
5. **`request.args.get("name", "world")` is the safe, one-line way to read a query parameter,** replacing a four-line `if`/`else` and eliminating the HTTP 400 a missing, unchecked parameter would otherwise cause.

## Common pitfalls

- ❌ Naming the templates folder anything other than exactly `templates` (or capitalizing it): `render_template()` won't find your HTML, and Flask's terminal output will say so with a template-not-found error.
- ❌ Forgetting the double curly braces around a placeholder in the template: Jinja won't interpolate it, and the visitor will see the literal word `name` printed on the page instead of a real value.
- ❌ Reading `request.args["name"]` directly with no `if "name" in request.args` check and no default: a visitor who leaves off the query string entirely gets a real HTTP 400, not your page.
- ❌ Assuming `?name=` (present but empty) behaves like a missing key: it doesn't; `.get()`'s default only fires when the key is truly absent, not when it's blank.
- ❌ Forgetting to `pip install -r requirements.txt` (or list `flask` in it at all) before handing a project to someone else, or to a fresh cs50.dev codespace: the very first `import` line will fail.

---

## 🛠️ Capstone Project: Build hello-flask

> This is the main hands-on project for the lesson. On cs50.dev, you'll build **hello-flask**, the smallest possible dynamic website: a route that reads a name out of the URL and greets whoever it is with a real Jinja template, plus a second route proving the same pattern holds up past one page. This is, quite literally, the first running skeleton of the database-backed web app you'll ship at the end of this course.

### What you will build

A two-route Flask app in a folder called `hello-flask/`:

- `requirements.txt` listing `flask`, and `app.py` creating the app with `Flask(__name__)`.
- `templates/index.html`, rendered by the `/` route, greeting `?name=...` with a default of `"world"`.
- `templates/about.html`, rendered by a second route, `/about`, written in the same template style.

### Why this is the perfect practice

| Lesson idea | Where you use it in hello-flask |
|---|---|
| Routes as generic input, not file paths (Part 1) | Every `@app.route` you write. |
| `pip`, `requirements.txt`, `Flask(__name__)` (Part 2) | Milestone 1, the scaffold. |
| `render_template()` and the mandatory `templates/` folder (Part 3) | Milestone 3, factoring your HTML out of `app.py`. |
| `{{ }}` interpolation (Part 3) | Milestones 4 and 6, the greeting and the about line. |
| `request.args.get("name", "world")` (Part 4) | Milestone 5, and the `/about` route in Milestone 6. |

### Milestones (build them in order, each one works on its own)

1. **Scaffold hello-flask and say hello in plain text.** On cs50.dev, create a `hello-flask` folder with `requirements.txt` (containing `flask`) and `app.py` (with `Flask(__name__)` and one route, `/`, returning the plain string `"Hello, world!"`). Run `pip install -r requirements.txt`, then `flask run`. Done when you see the greeting in your browser on port 5000, and view-source shows nothing but that plain text.
2. **Return real HTML: no template yet.** Change the same route to return a full hard-coded HTML string (doctype, `<html>`, `<head>`, `<body>`). Done when view-source shows real tags instead of plain text.
3. **Factor the HTML into a template.** Create a `templates/` folder (exact spelling and case), move your HTML into `templates/index.html`, and replace the returned string in `app.py` with `render_template("index.html")`. Done when the page looks identical to Milestone 2, but `app.py` no longer contains any HTML.
4. **Greet the URL's name, the naive way.** Add a `{{ placeholder }}` gap to `templates/index.html`. In `app.py`, import `request`, use an `if "name" in request.args: ... else: ...` block to set `name`, and pass it to `render_template()`. Confirm `/?name=<your name>` shows your name and the bare `/` shows `"world"`. Then, on purpose, delete the `else` branch, visit the bare route, and read the real HTTP 400 your own code just produced, then put the `else` back.
5. **Simplify to one line.** Replace the whole `if`/`else` with `name = request.args.get("name", "world")`, and rename `placeholder` to `name` in both the template and the `render_template()` call. Done when the behavior is identical to Milestone 4 but the logic is one line.
6. **Add a second route: `/about`.** Create `templates/about.html` in the same style (doctype, head, title, a body with its own `{{ name }}` gap: something like `"This app was built by {{ name }}."`). Add `@app.route("/about")` in `app.py`, using the same `request.args.get("name", "world")` pattern. Done when `/` and `/about` each render their own template, independently, both with and without `?name=`.
7. **Stretch goals.** Add a third route with its own template; or accept a second query parameter (say `?language=`) alongside `name`, with its own default, and interpolate both into one sentence.

### How you will know you are done

- ✅ `flask run` serves `hello-flask` on port 5000 from cs50.dev.
- ✅ Visiting `/` with no query string shows a default greeting; visiting `/?name=YourName` shows your actual name, and view-source proves the greeting came from the server, not the browser.
- ✅ `/about` renders its own template, in the same style, entirely independent of `/`.
- ✅ You can point to the single line `request.args.get("name", "world")` and explain, out loud, what each of its two arguments does.

> 💡 **Keep yourself honest:** don't skip Milestone 4's "break it on purpose" step. Seeing your own code produce a real HTTP 400 is worth more than reading about it: it's the same status code from Lesson 35, except this time you caused it, and you fixed it.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Predict the query string (foundational)
Without running any code, write down what `name` would equal, using `request.args.get("name", "world")`, for each of these URLs: `/`, `/?name=Kelly`, `/?name=`, and `/?sport=basketball`. Then actually build a one-route app to check your answers, and pay special attention to the third one.

### Exercise 2: A second query parameter (intermediate)
Extend `hello-flask`'s `/` route to also read `?language=`, defaulting to `"English"` if absent, and interpolate both `name` and `language` into a single sentence in `templates/index.html`, such as "Hello, {{ name }}! Enjoying CS50 in {{ language }}?"

### Exercise 3: Diagnose a broken template on purpose (advanced)
Rename your `templates` folder to something else (like `template`, singular), or delete one `}` from a `{{ }}` placeholder, and run `flask run` again. Read the actual error Flask prints in your terminal, and write one sentence explaining what it means and how you'd recognize this bug in the future without a walkthrough telling you what to look for.

---

## Cheat sheet

```text
MINIMAL FLASK APP (app.py)
  from flask import Flask, render_template, request
  app = Flask(__name__)

  @app.route("/")
  def index():
      name = request.args.get("name", "world")
      return render_template("index.html", name=name)

REQUIREMENTS.TXT
  flask

RUN IT
  pip install -r requirements.txt
  flask run                      -- serves on port 5000 by default (not 8080)

ROUTES
  @app.route("/path")            -- decorator: wires a URL to the def below it
  def some_name(): ...           -- runs whenever that URL is visited

QUERY STRINGS
  /greet?name=David              -- one key=value pair
  /greet?name=David&sport=chess  -- two, joined by &

TEMPLATES
  templates/                     -- folder name is mandatory, exact, lowercase
  render_template("file.html", key=value)   -- never include "templates/" in the filename
  {{ key }}                      -- Jinja interpolation inside the HTML file

REQUEST.ARGS
  request.args["name"]           -- raises trouble (HTTP 400) if "name" is missing
  request.args.get("name", "world")   -- safe: "world" only if the key is truly absent
                                       -- ?name= (empty) still counts as present!

GOLDEN RULE
  A URL is input to your program now, not a path to a file. Everything from here
  forward is about what your own code decides to do with that input.
```

## How this connects to the rest of the course

- **Earlier, Module 10 · Lesson 37 (CSS and JavaScript):** that lesson's whole argument was to factor styling and behavior out of hard-coded HTML; this lesson applies the exact same discipline to the HTML itself, factoring it out of `app.py` and into `templates/`.
- **Earlier callback, Module 10 · Lesson 35 (HTTP and the browser):** the raw GET requests, query strings, and status codes you inspected with `curl` and DevTools are exactly what `@app.route` now answers: today, your own code sits on the other end of that conversation for the first time.
- **Earlier callback, Module 7 · Lesson 26 (Loops, functions, and exceptions):** every route in this lesson is, underneath the `@app.route` decorator, an ordinary Python `def`, the same tool you used to build `get_height()` back in Module 7.
- **Next, Module 11 · Lesson 39 (Forms, layouts, and GET vs POST):** you'll submit an actual HTML form to a route like this one, stop copy-pasting boilerplate HTML between templates with layout inheritance, and choose deliberately between GET and POST.
- **Later, Module 11 · Lessons 40-41:** this same route-and-template pattern grows server-side validation, a real SQLite database, login sessions, and a JSON API, all built on exactly the skeleton you wrote today.
- **North star:** `hello-flask` is not a throwaway exercise: it is the first running version of the database-backed web app you will finish building as this course's final capstone.

---

*Source: "CS50x 2026 - Lecture 9 - Flask" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
