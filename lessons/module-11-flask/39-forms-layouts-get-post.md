# Module 11 · Lesson 39: Forms, Layouts, and GET vs POST

> **Course:** Self-Paced CS50x
> **Module 11:** Web apps with Flask: everything so far becomes one real application
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 9 - Flask](https://www.youtube.com/watch?v=am7POvSZ4GE) · [full transcript](../../transcripts/12-lecture-9-flask.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

A form that submits to its own route tends to duplicate the same HTML boilerplate in every template it touches: Jinja's `{% extends %}` and `{% block %}` let you write that boilerplate once in a `layout.html`, and the HTTP method you put on the form's `method` attribute, `GET` or `POST`, decides whether the user's input becomes a visible, bookmarkable part of the URL or stays tucked inside the request where a passerby can't glance over your shoulder and read it.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you upgrade `hello-flask`, the app from Lesson 38, so its form extends a shared layout, submits first via GET, then via POST, and finally lives in a single route that handles both. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Flask and Jinja will keep changing version numbers, but the pattern of "one shared skeleton, many interchangeable insides" is a general templating idea, documented directly at the source:
>
> - **[Jinja: Template Inheritance](https://jinja.palletsprojects.com/en/stable/templates/#template-inheritance)** (Jinja project documentation). This is the official reference for the exact `{% block %}` / `{% endblock %}` / `{% extends %}` syntax you'll use today, worth bookmarking, since every Flask app you ever write will lean on it.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Route:** a URL path your Flask app recognizes and has code to respond to, like `/` or `/greet`. You "define a route" by writing a Python function and labeling it with `@app.route(...)`.
- **Query string:** the part of a URL after a `?`, made of `key=value` pairs separated by `&`, like `?name=David`. It's how a `GET` request smuggles input into a URL.
- **GET request:** an HTTP method that asks a server for something. Its input, if any, rides along in the query string, which means it's visible in the address bar, saved in browser history, and can be bookmarked or emailed as a link.
- **POST request:** an HTTP method that hands the server data to act on. Its input rides inside the body of the request instead of the URL, so it doesn't show up in the address bar or get saved in browser history.
- **Boilerplate:** the HTML that's identical across pages (`<!DOCTYPE html>`, `<html>`, `<head>`, `<title>`) and would otherwise have to be retyped in every single template.
- **Template inheritance:** a Jinja feature where one "parent" template (conventionally `layout.html`) holds the shared boilerplate, and "child" templates each supply only the one part that changes, using `{% extends %}` and `{% block %}`.
- **`request.args`:** a dictionary-like object Flask fills in with whatever key-value pairs arrived in a `GET` request's query string.
- **`request.form`:** a dictionary-like object Flask fills in with whatever key-value pairs arrived in a `POST` request's body. Same job as `request.args`, different HTTP method, confusingly similar name.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 38 got you to the point where a single route can read one query-string parameter and plug it into a template with `render_template`. That's the smallest possible Flask app. The moment you add a second page (a form here, a results page there), you run into the two problems every real web app runs into on day one: your HTML starts repeating itself, and you have to decide, deliberately, how user input should travel from the browser to your server. Part 1 shows you exactly where that duplication comes from, in Malan's own words, once he has two nearly-identical templates open side by side.

This lesson fixes that with template inheritance, and then tackles the second problem, GET versus POST, with the same form you just built. Both skills are things you will use in literally every route of your CS50 final project, since as you'll see in the Capstone, every user action your app ever receives arrives as one of exactly these two verbs.

## Learning objectives

By the end of this lesson you will be able to:

1. Build an HTML form whose `action` points at a second Flask route, and explain why that pattern duplicates boilerplate HTML across templates.
2. Write a `layout.html` with `{% block body %}{% endblock %}`, and make other templates reuse it with `{% extends "layout.html" %}`.
3. Explain why a `GET` form's data lands in the URL, and why that's a privacy problem for anything sensitive.
4. Switch a form to `method="post"`, read its data with `request.form` instead of `request.args`, and fix the `405 Method Not Allowed` error that follows if you forget to also update the route's `methods`.
5. Merge two routes that show and process the same form into one route using `methods=["GET", "POST"]` and a check on `request.method`.

## Prerequisites

- **Module 11 · Lesson 38: Flask fundamentals: routes and templates**: this lesson assumes you already have a working `hello-flask` app with an `app.py`, a `templates/` folder, an `index.html`, `@app.route`, `render_template`, and a route that reads `request.args`.
- **Module 10 · Lesson 36: Building pages with HTML**: the `<form>` element and its `action`, `method`, and `input` attributes were introduced there in plain HTML, with no server behind it yet.
- **Module 10 · Lesson 35: HTTP and the browser**: GET and POST were first named there as two of HTTP's verbs; today you finally choose between them in your own code.

---

## Part 1: A second route for the form (and the duplication it creates)

Typing a name straight into a URL to test your app (`/?name=David`) works, but "no human actually does that," as Malan says. Real users need an actual form to fill in. The natural first design is two routes: one that shows the form, and a second one that handles what it submits to.

`index.html` shows a form whose `action` points at a new route:

```html
{% extends "layout.html" %}

{% block body %}
    <form action="/greet" method="get">
        <input autocomplete="off" autofocus name="name" placeholder="Name" type="text">
        <button type="submit">Greet</button>
    </form>
{% endblock %}
```

*(Ignore the `{% extends %}` and `{% block %}` lines for a moment: Part 2 explains those. For now, picture this as a normal, self-contained HTML file with a form in its `<body>`.)*

`app.py` gets a matching `/greet` route:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greet")
def greet():
    return render_template("greet.html", name=request.args.get("name", "world"))
```

And `greet.html` renders the actual greeting, using `request.args` exactly as you did in Lesson 38, just now filled in by a real form instead of a hand-typed URL.

This works. But open `index.html` and `greet.html` side by side and a problem jumps out: `<!DOCTYPE html>`, `<html lang="en">`, `<head>`, `<title>` (every line except the one piece of content in the `<body>`) is identical, retyped in full in both files. Malan, looking at his own two templates, doesn't mince words:

> "There's a lot of duplication and technically I didn't copy paste, so I might as well have." (David Malan)

And it only gets worse as the app grows:

> "if I have two forms on my page, I now need 4 routes. If I have 3 forms, I need 6 routes. It seems a little annoying that you use one route just to show the form and another route to process the form." (David Malan)

> 🔑 **The single most important takeaway of this part.** Two templates that are 95% identical boilerplate and 5% actual content are a signal, not a coincidence: it means you're about to want template inheritance, which Part 2 builds.

## Part 2: Template inheritance (one `layout.html`, many children)

Jinja's fix is a **parent template** that holds everything invariant, with one clearly marked hole for whatever changes per page. By convention, this file is called `layout.html`:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>hello</title>
    </head>
    <body>
        {% block body %}{% endblock %}
    </body>
</html>
```

Two new pieces of syntax appear here, both written with curly braces and percent signs (`{% ... %}`) instead of HTML's angle brackets. Jinja deliberately picked a symbol that would never collide with actual HTML tags:

- **`{% block body %}`** opens a named hole. You can call it anything (`foo`, `bar`), but by convention the block that stands in for the whole page body is just called `body`.
- **`{% endblock %}`** closes that hole. An empty block here just means "nothing goes here by default: a child template is expected to fill it in."

As Malan describes it:

> "in layout.html, I can put all of my boilerplate HTML, the stuff that is invariant and doesn't change." (David Malan)

A **child template** then declares which parent it extends, and supplies only the content for that one block. `index.html`, once you strip out everything now living in `layout.html`, shrinks down to just its form:

```html
{% extends "layout.html" %}

{% block body %}
    <form action="/greet" method="get">
        <input autocomplete="off" autofocus name="name" placeholder="Name" type="text">
        <button type="submit">Greet</button>
    </form>
{% endblock %}
```

`greet.html` follows the identical pattern, with a different block body:

```html
{% extends "layout.html" %}

{% block body %}
    Hello, {{ name }}
{% endblock %}
```

Malan sums up the whole mechanism in one line:

> "if I want index.html to use the layout.html blueprint, I can simply say extends layout.html." (David Malan)

Nothing about what the browser receives changes: Flask and Jinja splice the child's `body` block into the parent's `{% block body %}{% endblock %}` slot before sending the page, so "View Page Source" still shows one complete, ordinary HTML document. Only your *source files* got smaller.

```text
layout.html (parent)                index.html (child)
┌─────────────────────┐             ┌───────────────────┐
│ <!DOCTYPE html>      │             │ {% extends         │
│ <html><head>...      │   +         │   "layout.html" %} │   =   one full page,
│ <body>               │             │ {% block body %}   │       sent to the browser
│   [ block body ]  ◄──┼─────────────┤   <form>...        │
│ </body></html>       │             │ {% endblock %}      │
└─────────────────────┘             └───────────────────┘
```

> ✅ **What to do about it:** the moment a second template repeats the same `<!DOCTYPE html>`/`<html>`/`<head>` lines as your first one, move that shared HTML into `layout.html` and have both templates `{% extends %}` it instead of retyping it.

## Part 3: GET vs POST (privacy of the query string, and merging the routes)

With duplication solved, the form from Part 1 still has a `method="get"` on it, meaning its input rides in the query string in full public view. Malan makes the risk concrete:

> "if I have like a nosy sibling and they sit down in my browser, they're gonna see like every URL I visited, including whose name was greeted." (David Malan)

A nosy sibling reading someone's name is low stakes. The same mechanism reading a password, a credit-card number, or a search you'd rather keep private is not. `GET`'s visibility is a feature when you want a page to be linkable or bookmarkable, but a liability the moment the input is sensitive.

The fix is to switch the form's `method` to `post` and change nothing else about the *look* of the form:

```html
<form action="/greet" method="post">
```

That alone isn't enough, though: try it, and Flask responds with `405 Method Not Allowed`, because every `@app.route` defaults to accepting only `GET`. You have to opt the route into `POST` explicitly:

```python
@app.route("/greet", methods=["POST"])
def greet():
    return render_template("greet.html", name=request.form.get("name", "world"))
```

Notice `request.args` became `request.form`. Same job (pull out the value the user typed under the key `"name"`), different HTTP method, and, as Malan admits, a confusing pair of names for it:

> "This is completely unintuitive that request.args is get and request.form is post... because they all come from forms, so it's bad naming, admittedly." (David Malan)

Submit the form again, and the URL bar now shows nothing past `/greet`: no `?name=David` in sight, no trace in browser history. The data still reached the server; it's just no longer written on the outside of the envelope, as earlier lessons put it.

### Merging the two routes into one

Now that both routes exist only to serve one form, Malan notices the same annoyance from Part 1 hasn't actually gone away. You still have two routes doing one job:

> "Is there a way to get kind of the best of both worlds and combine these two routes into one so that everything related to greeting the user all happens in one place?" (David Malan)

The trick: tell one route to accept *both* methods, and branch inside the function on which one actually arrived, using `request.method`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return render_template("greet.html", name=request.form.get("name", "world"))
    return render_template("index.html")
```

The `/greet` route disappears entirely. Everything lives at `/` now. The only other change needed: the form's `action` in `index.html` has to stop pointing at a route that no longer exists.

```html
<form action="/" method="post">
```

*(Leaving `action` off the `<form>` tag entirely works too: a form with no `action` submits back to whatever URL it's already on.)*

```text
        GET /            →  request.method == "GET"   →  render index.html (show the form)
        POST / (name=…)  →  request.method == "POST"  →  render greet.html (show the greeting)
```

One route, one URL, two behaviors: decided entirely by which HTTP verb the browser used to get there.

Finally, it's worth internalizing *why* this choice matters beyond privacy. GET requests can be triggered just by clicking a link or typing a URL: no confirmation, no button press. That makes GET dangerous for anything that changes data on a server (imagine an email link that silently deletes your account the moment it's clicked). POST requires an actual form submission, which is a meaningfully higher bar:

> "post requests are preferred any time there's anything remotely personally identifiable or remotely destructive." (David Malan)

> ✅ **What to do about it:** default every form that submits personal data, or changes anything on the server, to `method="post"`: reach for `GET` only when the result is meant to be a plain, shareable, side-effect-free page.

---

## Key takeaways

1. **Two near-identical templates are a duplication bug, not bad luck.** If most of a template's lines are boilerplate shared with another template, factor them into `layout.html`.
2. **`{% extends %}` and `{% block %}` are Jinja's inheritance syntax.** A parent template (`layout.html`) defines a named hole with `{% block name %}{% endblock %}`; a child template fills it using `{% extends "parent.html" %}` and its own `{% block name %} ... {% endblock %}`.
3. **`GET` puts input in the URL; `POST` puts it in the request body.** Only the first is visible in the address bar, browser history, and bookmarks.
4. **`request.args` reads GET data; `request.form` reads POST data.** The names don't map intuitively to the verbs: you just have to remember it.
5. **A route only accepts `GET` unless you say otherwise.** Add `methods=["POST"]`, or `methods=["GET", "POST"]` to support both, or you'll hit a `405 Method Not Allowed`.
6. **One route can serve and process the same form.** Branch on `request.method` inside the function to decide whether to show the form or handle its submission.

## Common pitfalls

- ❌ Forgetting `{% endblock %}` after `{% block body %}`: Jinja will raise a template error rather than silently guessing where the block ends.
- ❌ Changing a form's `method` to `post` but leaving the route's `methods` at the Flask default (`GET` only): this produces a `405 Method Not Allowed`, not a silent failure, so check the terminal running `flask run` for the real error.
- ❌ Reading `request.args` after switching a form to POST (or vice versa): the data is there, but under the wrong object, so it'll look like the value is simply missing.
- ❌ Merging two routes into one but leaving the form's `action` pointed at the now-deleted route (like `/greet`): update `action` to match wherever the merged route actually lives.
- ❌ Assuming GET is "safe" because the browser visually tucks the URL away: it's still recorded in full in browser history, server logs, and any bookmark or shared link.

---

## 🛠️ Capstone Project: Upgrade hello-flask (One Form, Two Verbs, Zero Duplication)

> This is the main hands-on project for the lesson. Starting from the `hello-flask` app you built in Lesson 38, on cs50.dev, you'll watch the exact same three-act story Malan walked through: factor out duplication with a layout, feel GET's privacy problem for yourself in the URL bar, then fix it and simplify down to one merged route.

### What you will build

An upgraded `hello-flask` with:

- A `layout.html` holding all shared boilerplate, extended by every other template.
- A form that greets the user by name, first working over GET, then over POST.
- A single route on `/` (no separate `/greet`) that uses `methods=["GET", "POST"]` to both show and process that form.

### Why this is the perfect practice

| Lesson idea | Where you use it in `hello-flask` |
|---|---|
| Duplication across templates (Part 1) | Milestone 1: noticing it before you fix it. |
| `{% extends %}` / `{% block %}` (Part 2) | Milestone 1: building `layout.html`. |
| GET and the query string (Part 3) | Milestones 2-3: submitting the form and watching the URL. |
| POST and `request.form` (Part 3) | Milestone 4: switching the method and fixing the resulting error. |
| Merging routes with `methods=["GET", "POST"]` (Part 3) | Milestone 5: collapsing two routes into one. |

### Milestones (build them in order, each one works on its own)

1. **Build `layout.html` and convert your existing templates to extend it.** Move the shared `<!DOCTYPE html>`/`<html>`/`<head>`/`<body>` boilerplate into `layout.html` with `{% block body %}{% endblock %}`. Update every existing template to start with `{% extends "layout.html" %}` and wrap its unique content in `{% block body %} ... {% endblock %}`. Done when your app looks and behaves exactly as it did before, only the files got shorter.
2. **Add a GET form.** In `index.html`, add a `<form>` with `method="get"`, an `action` of `/greet`, and a text `input` named `name`. Done when the form renders and has a working submit button.
3. **Handle the GET submission and read the query string.** Add a `/greet` route (default `GET`) that reads `request.args.get("name", "world")` and renders a `greet.html` (which also extends `layout.html`). Submit the form, then look at the URL bar. Done when you can point to `?name=...` sitting right there in the address bar after clicking submit.
4. **Switch to POST.** Change the form's `method` to `post`, change the `/greet` route to `methods=["POST"]`, and swap `request.args` for `request.form`. Submit again. Done when the URL bar shows no query string at all after submitting, even though the greeting still works.
5. **Merge the two routes into one.** Delete the standalone `/greet` route. Change your `/` route to `methods=["GET", "POST"]`, and inside it, branch on `request.method` to decide whether to render the form or process it. Update the form's `action` to match (or remove `action` entirely). Done when `/greet` no longer exists anywhere in your code, and the single `/` route both shows and handles the form.
6. **Trigger and explain a `405`.** Temporarily set your merged route's `methods` back to just `["GET"]`, submit the form, and read the `405 Method Not Allowed` in your browser. Then restore `["GET", "POST"]`. Done when you can explain in one sentence why that error appeared.
7. **Stretch goals.** Add a second form field (say, a favorite color) and thread it through the same GET-then-POST-then-merge sequence on your own. Or move a shared `<meta name="viewport" ...>` tag into `layout.html` so every page benefits from it at once.

### How you will know you are done

- ✅ `layout.html` holds all shared boilerplate; every other template starts with `{% extends "layout.html" %}` and contains only its own `{% block body %}`.
- ✅ You watched `?name=...` appear in the URL bar with GET, then disappear with POST, on the same form.
- ✅ A single route on `/` with `methods=["GET", "POST"]` handles both showing and processing the form: `/greet` is gone.
- ✅ You can explain, in one sentence, why POST is the safer default for anything private or destructive.

> 💡 **Keep yourself honest:** don't just read the URL bar in a screenshot afterward: actually submit the GET version and the POST version yourself, side by side, so the difference is something you saw happen, not something you're taking on faith.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: A page with no form, still extending layout (foundational)
Create a plain `about.html` with a paragraph of text about your app (no form, nothing dynamic) and make it extend `layout.html` like every other template. Add a route for it. This isolates template inheritance from forms entirely, so you can see it's a general-purpose tool, not something special to forms.

### Exercise 2: A second field, tracked through both verbs (intermediate)
Add a second text input to your form (for example, a favorite color) alongside `name`. Get it working over GET first, confirm you see both `name=...&color=...` in the URL, then switch the whole form to POST and confirm both values still arrive, just no longer visible in the address bar.

### Exercise 3: A second merged route, built from scratch (advanced)
Without copying your `/` route, build an entirely new merged route, say `/subscribe`, that shows a one-field email signup form on GET and prints a confirmation message on POST, using `methods=["GET", "POST"]` and a `request.method` check: the same pattern from Part 3, but written independently to prove you own it.

---

## Cheat sheet

```text
TEMPLATE INHERITANCE (Jinja)
  layout.html (parent):
    {% block body %}{% endblock %}        <- named hole, filled by children

  child.html:
    {% extends "layout.html" %}
    {% block body %}
      ... only the unique content here ...
    {% endblock %}

GET vs POST
  GET   input rides in the URL's query string   ?name=David
        visible in address bar, history, bookmarks, shared links
  POST  input rides in the request body
        not visible in the URL: safer for private/destructive actions

READING THE DATA
  request.args.get("name", "world")   <- GET  (query string)
  request.form.get("name", "world")   <- POST (form body)

ROUTE METHODS
  @app.route("/greet")                        default: GET only
  @app.route("/greet", methods=["POST"])       POST only
  @app.route("/", methods=["GET", "POST"])     both, branch with:
      if request.method == "POST": ...
      else: ...                                (implicitly GET)

COMMON ERROR
  405 Method Not Allowed   -> the route doesn't list the method you just used;
                              add it to methods=[...]

GOLDEN RULE
  Anything remotely personally identifiable or remotely destructive: use POST.
```

## How this connects to the rest of the course

- **Earlier, Module 10 · Lesson 35: HTTP and the browser:** GET and POST were first named there as two of HTTP's verbs, seen only from the outside via status codes and headers. Today you chose between them yourself, inside your own code.
- **Earlier, Module 10 · Lesson 36: Building pages with HTML:** the `<form>` element and its `method`/`action` attributes were built in plain HTML there, with no server behind them. Today that same form finally talks to a real Flask backend.
- **Earlier, Module 11 · Lesson 38: Flask fundamentals: routes and templates:** routes, `render_template`, and `request.args` were introduced there for a single page; this lesson put a second page next to it and had to solve the duplication and privacy problems that appear the moment a real app grows past one route.
- **Next, Module 11 · Lesson 40: A real app: validation and databases:** the merged POST route you built today is exactly where you'll next add server-side validation and persist submissions to a real database.
- **Later, the course capstone:** every user action your final project's database-backed web app ever receives (a login, a purchase, a search, a delete) arrives as one of these two verbs, GET or POST, and today is where you learned to tell them apart and choose deliberately between them.

---

*Source: "CS50x 2026 - Lecture 9 - Flask" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
