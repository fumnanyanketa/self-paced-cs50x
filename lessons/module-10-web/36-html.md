# Module 10 · Lesson 36: Building Pages with HTML

> **Course:** Self-Paced CS50x
> **Module 10:** The web: from packets to pages people can use
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 8 - HTML, CSS, JavaScript](https://www.youtube.com/watch?v=yYst7puZXjw) · [full transcript](../../transcripts/11-lecture-8-html-css-javascript.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

You are about to write real HTML files by hand (headings, paragraphs, lists, tables, images, video, links, and a form), serve them from your own machine, and check your work with a validator, which is the exact skill that will let you build (and eventually generate) every page your future web apps show people.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a personal home page from scratch (headings, a list, a table, an image with alt text, a link, and a working search form), then run it through the official W3C validator until it passes clean. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Browsers, editors, and even HTML's own version number will keep changing; the rules for what a tag means will not, because they are written down in one place everyone agrees to follow.
>
> - **[The HTML Living Standard](https://html.spec.whatwg.org/)**, maintained by WHATWG. This is the actual specification that defines what every tag and attribute in this lesson means: whatever your browser does with a `<table>` or an `<input>`, this document is the rulebook it is implementing.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **HTML (HyperText Markup Language):** the language web pages are written in. It is not a programming language (there are no loops, no conditionals, no variables). It just describes what's on a page and lets the browser decide how to draw it.
- **Tag:** a bit of text in angle brackets, like `<p>`, that marks where something starts or ends. Most tags come in pairs: an opening tag like `<p>` and a closing tag like `</p>`.
- **Element:** a start tag, an end tag, and everything in between: the whole unit. "The paragraph element" means the opening `<p>`, the text inside it, and the closing `</p>` together.
- **Attribute:** an extra bit of information added inside a tag's opening bracket, written as `name="value"`, like `lang="en"` inside `<html lang="en">`. It modifies how that one element behaves.
- **DOM (Document Object Model):** the tree-shaped structure the browser builds in memory the moment it reads your HTML file. Every element becomes a node in that tree.
- **Port:** a number that tells a computer which program on it should handle an incoming connection. A web server usually listens on port 80 (or 443 for the secure version); this lesson's practice server uses port 8080 instead, since 80 and 443 are already taken on cs50.dev.
- **Hyperlink:** clickable text (or an image) that sends the browser to another URL when clicked. Built with the anchor tag, `<a>`.
- **Query string:** the part of a URL after a `?`, made of `key=value` pairs joined by `&`, that sends input to a server as plain text inside the URL itself, for example, `?q=cats`.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 35 opened the envelope that travels between browser and server and read the headers on the outside: the verb, the status code, the content type. This lesson is about what's actually *inside* the envelope: the file itself, and how you write one. As Malan frames the whole topic before touching a single tag:

> "We're about to dive into is an actual language, not a programming language, a markup language called HTML, hypertext markup language, whose purpose in life is just to tell browsers what to display on the screen." (David Malan)

It also closes a loop from much earlier in the course. Lesson 23 introduced trees as a data structure you build by hand out of nodes and pointers. Today, the browser builds one *for* you, out of your HTML, every time a page loads: the very tree that Lesson 37 will teach you to reprogram live with JavaScript. And there's a direct line from here to the end of the course: every page your Module 11 Flask application renders is, underneath whatever Python generates it, exactly the HTML you are about to learn to write by hand.

## Learning objectives

By the end of this lesson you will be able to:

1. Write a valid, minimal HTML5 document from scratch (doctype, `<html>`, `<head>`, `<body>`), and serve it from your own machine with `http-server`.
2. Explain the DOM as a tree, and describe how the browser builds that tree from your HTML file, node by node.
3. Use paragraphs, headings (`h1`-`h6`), lists (`ul`/`ol`/`li`), tables, images (with required `alt` text), and video (with `controls`) correctly in a page.
4. Build a working hyperlink with the anchor tag, and explain how the same feature that makes links convenient also makes phishing possible.
5. Build a form that submits via `GET` as a query string, and add basic client-side validation with `pattern` or `type="email"`.
6. Validate an HTML page with the W3C validator, and explain why passing client-side validation is never enough on its own.

## Prerequisites

- **Module 10 · Lesson 35: HTTP and the browser**: you already know what travels inside an HTTP request and response (verbs, status codes, headers); this lesson is about the file that comes back in the body of that response.
- **Module 6 · Lesson 23: Trees, hash tables, and tries**: you've already built a tree by hand out of nodes and pointers; today you'll see the browser build one automatically, called the DOM.
- A cs50.dev (GitHub Codespaces) account and basic comfort with its terminal, from earlier modules.

---

## Part 1: HTML fundamentals (tags, attributes, and the DOM)

### The only two terms of art

HTML has almost none of the complexity of a real programming language. There's no arithmetic, no `if`, no loops. Malan is explicit that it comes down to two ideas:

> "Let's take a look at perhaps the simplest of webpage and specifically glean from them what tags are and what attributes are really the only two terms of art that are going to be germane for this particular language." (David Malan)

A **tag** is the bracketed marker (`<p>`, `</p>`); an **element** is the tag pair plus its contents; an **attribute** is an extra `key="value"` pair added inside an opening tag to modify that one element: the same key-value idea you've already seen in dictionaries and hash tables, just with a different spelling.

### hello.html, start to finish

Every HTML5 file begins with the same one-line boilerplate, which you memorize or copy-paste rather than reason about:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>hello title</title>
    </head>
    <body>
        hello body
    </body>
</html>
```

`<!DOCTYPE html>` tells the browser "this file is HTML5." Then comes the **root element**, `<html>` (every page has exactly one), with a `lang="en"` attribute:

> "Here for instance is syntax that essentially is going to tell the browser when my browser reads this file top to bottom left, right, hey browser, here comes the HTML of my page, and the language in which the contents of this page are written are in English." (David Malan)

Inside `<html>` there are exactly two children: `<head>`, which holds page metadata like `<title>` (the text shown in the browser tab), and `<body>`, which holds everything the visitor actually sees: what Malan calls "the 95% of the screen, the so-called viewport." Indentation and line breaks here are purely for humans; as you'll see in Part 2, the browser mostly ignores whitespace.

### Serving it: http-server and port 8080

Saving a `.html` file only lets *you* see it, opened locally in your own browser. To let anyone else on the internet request it, you need an actual web server. On cs50.dev, the command is simply:

```text
http-server
```

This starts a small web server that hands out the files in your current folder over HTTP. It can't use the default ports, though, because the cs50.dev environment itself already uses them:

> "By default we've chosen another common developer port number, 8080, which is interesting only insofar as it's 80 twice, but it's a human convention." (David Malan)

That's it: no build step, no compiler. The whole point of HTML is that the browser reads the file directly.

### The DOM: HTML becomes a tree

The moment your browser downloads an HTML file, it doesn't just display text top to bottom. It builds a structure in memory. This is the payoff of the earlier callback:

> "Let me propose that what we've really done is build a tree in the browser's memory. So we kind of have come full circle with week 5 when we talk about trees and other hierarchical structures." (David Malan)

For `hello.html` above, that tree looks like this:

```text
                html
               /    \
            head    body
             |         \
           title      "hello body"
             |
        "hello title"
```

One root node (`html`), exactly like the single root you built by hand for a binary search tree in Lesson 23, except this time the browser is the one allocating each node as it reads your file, left to right, top to bottom. This tree is called the **DOM**, the Document Object Model, and it's the same tree that Lesson 37's JavaScript will learn to reach into and change live, without reloading the page.

> 🔑 **The single most important takeaway of this part.** HTML is not code that runs. It's a description of a tree. Every tag you open becomes a node; every tag nested inside another becomes that node's child. Get the nesting right, and the tree the browser builds matches what you intended.

---

## Part 2: The building blocks (paragraphs, headings, lists, tables, media)

### Paragraphs, and why whitespace doesn't count

If you paste several paragraphs of plain text into `<body>` with blank lines between them, the browser ignores all that spacing and runs the text together into one blob. Malan is blunt about why:

> "Browsers not really caring about whitespace, you can put all the white space you want there. It's just going to ignore it in this particular case." (David Malan)

HTML has to be told explicitly where each paragraph begins and ends, using the `<p>` tag:

```html
<p>This is the first paragraph.</p>
<p>This is the second paragraph.</p>
```

> "Like if you want there to be more paragraphs, you need to tell the browser, Put a paragraph here, put a paragraph there." (David Malan)

### Headings: h1 through h6

For titles and section headings, HTML provides six levels, from most to least important:

```html
<h1>Chapter</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

> "So you've got H1 through H6 from biggest and boldest to smaller but still bold, and the browser decides on all of those settings for us." (David Malan)

The browser decides exactly how big and bold each level looks, but the *order* carries meaning too: an `<h1>` signals the single most important heading on the page, and everything nested under lower headings reads as supporting material: a hierarchy, not just a font-size shortcut.

### Lists: ul, ol, and li

A bulleted list needs `<ul>` (unordered list) wrapped around one or more `<li>` (list item) elements:

```html
<ul>
    <li>foo</li>
    <li>bar</li>
    <li>baz</li>
</ul>
```

Swap `<ul>` for `<ol>` (ordered list) and the exact same items become an automatically-numbered list instead: the browser does the counting, so inserting an item in the middle never means renumbering everything else by hand.

### Tables: table, tr, td, and thead/tbody/th

Tabular data (rows and columns) uses `<table>`, with one `<tr>` (table row) per row and one `<td>` (table data) per cell:

```html
<table>
    <tr>
        <td>1</td><td>2</td><td>3</td>
    </tr>
    <tr>
        <td>4</td><td>5</td><td>6</td>
    </tr>
</table>
```

For a table with column headings, add a `<thead>` section using `<th>` (table heading) cells, and wrap the data rows in `<tbody>`:

```html
<table>
    <thead>
        <tr>
            <th>Timestamp</th><th>Language</th><th>Problem</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>...</td><td>...</td><td>...</td></tr>
    </tbody>
</table>
```

### Images: img, src, and alt

An image is embedded with `<img>` and a `src` (source) attribute pointing at the file:

```html
<img src="bridge.png" alt="Harvard University">
```

Notice there's no closing `</img>` tag, and that's intentional, not a mistake:

> "Some tags just don't require an end tag if it's sort of obvious to the browser that the image should go there." (David Malan)

The `alt` (alternative text) attribute is not optional in practice. It's what a screen reader recites to a visually impaired visitor, and it's what shows up if the image is slow to load or simply broken:

> "If the image is slow to load or if someone is visually impaired and doesn't know what they're looking at, it would be nice to have some alternative text that something like screen reader software could recite." (David Malan)

### Video: the controls attribute

Video works similarly, but supports multiple source files (for different formats) and its own attributes:

```html
<video controls muted>
    <source src="video.mp4" type="video/mp4">
</video>
```

Without the `controls` attribute, a visitor has no play/pause/scrub bar at all:

> "It turns out you can put an HTML attribute on the video tag literally called controls that will enable those." (David Malan)

Notice `controls` and `muted` don't need a value: their mere presence is the signal. That's a small but real exception to the usual `key="value"` attribute pattern.

> ✅ **What to do about it:** treat `alt` on every image and `controls` on every video as non-negotiable defaults, not afterthoughts: they cost one attribute and they are the difference between a page that works for everyone and one that doesn't.

---

## Part 3: Links, forms, and validation

### Anchor tags, and the phishing trick hiding inside them

A clickable hyperlink uses the anchor tag, `<a>`, with an `href` (hyperreference) attribute holding the destination URL, and the visible text placed between the open and close tags:

```html
<a href="https://www.harvard.edu/">Visit Harvard</a>
```

> "If you want to have a tag, a link here to Harvard's website, you use open bracket A for anchor, H for hyperreference, set that equal to the URL to which you want to link, close the tag, and then in between the open tag and the close tag, put the actual word you want to link to." (David Malan)

The visible text and the actual `href` destination are completely independent: you can make text that says "harvard.edu" point anywhere at all. That's a convenient feature. It's also, unmodified, an attack:

> "It's all too easy to wage what are called phishing attacks, P H I S H I N G, which means to lead someone to what looks like the real site but is not, typically to get their username, their password, their credit card information, or something else." (David Malan)

> ❌ **The trap:** never trust link text at face value, yours or anyone else's. Hover over a link (or check the status bar / long-press on mobile) to see the real destination before you click, especially on anything asking for a password or payment details.

### Forms and the GET query string: build your own Google

Recall from Lesson 35 that a `GET` request can carry input as a **query string**: the part of a URL after `?`, made of `key=value` pairs. A `<form>` with `method="get"` is simply a way to *build* that query string by filling in a box, instead of typing a URL by hand:

```html
<form action="https://www.google.com/search" method="get">
    <input name="q" type="search" placeholder="Query" autocomplete="off" autofocus>
    <input type="submit" value="Google Search">
</form>
```

Submitting this form sends the browser to `https://www.google.com/search?q=cats`, the exact URL Google's own search box produces. The `name="q"` attribute is what becomes the key in that query string; whatever the visitor types becomes the value. As Malan puts it while building exactly this example:

> "The front end is what the user sees. The back end is what provides data to the front end." (David Malan)

Your form is a front end only: pointing `action` at Google's real search URL borrows *their* back end. Point `action` at your own server instead (something Module 11's Flask routes will do), and you own both halves.

### A crash course in regular expressions

Before you can validate what someone typed into a form field, you need a way to describe a *pattern* of acceptable text, not one exact string, but a shape. That's what **regular expressions** (regex, for short) are for:

> "There exists in computing what are called regular expressions ... a way of describing patterns which are quite useful when you want to validate input." (David Malan)

A handful of symbols cover most of what you'll need:

| Symbol | Meaning |
|---|---|
| `.` | any single character |
| `*` | zero or more of whatever came before it |
| `+` | one or more of whatever came before it |
| `?` | zero or one of whatever came before it |
| `{n}` | exactly `n` times |
| `[abc]` | any one character from the set `a`, `b`, or `c` |
| `\d` | any digit |
| `\D` | anything that is *not* a digit |
| `\.` | a literal period (the backslash "escapes" the dot's special meaning) |

Regex syntax isn't unique to HTML: you'll meet the same symbols in Python and in most other languages, and they're just as useful for finding data in a document as they are for validating it.

### Client-side validation: pattern and type="email"

An `<input>` can carry a `pattern` attribute, a regular expression the browser checks before it will submit the form:

```html
<input name="email" placeholder="email" pattern=".+@.+\.edu">
```

Roughly: one-or-more characters, an `@`, one-or-more characters, a literal period, then a TLD. Typing anything that doesn't match blocks submission with a "please match the requested format" message. There's also a shorthand that skips writing your own pattern:

> "There is actually an input of type email which just does all of that pattern matching for you, but the scary thing is that it's actually pretty involved to validate email addresses." (David Malan)

`<input type="email">` uses the browser's own, far more thorough built-in pattern: proof that even something as familiar as "is this an email address" is a genuinely hard pattern to get exactly right by hand.

### The W3C validator

Once you've written a page, you want a way to check that every tag you opened is actually closed, and that you haven't made some other structural mistake. That's exactly what the W3C's validator does:

> "There's a bunch of ways, but one tool that's worth knowing about is this one here at validator.w3.org is a website by the group that essentially standardizes this and other languages." (David Malan)

Paste your HTML into [validator.w3.org](https://validator.w3.org/#validate_by_input), click check, and it reports every unclosed tag, missing attribute, or other structural error, a second pair of eyes before you ever ship a page.

### Why none of this can be trusted

Here's the twist that matters most: the `pattern` and `type="email"` checks above run entirely inside the visitor's own browser, on a copy of your HTML that you have already handed them. Using the browser's own developer tools, anyone can open that copy and simply delete the attribute doing the checking:

> "Even though you will encounter not just today but over the coming weeks as you play with HTML, certain features, they are not to be trusted in general when it comes to security." (David Malan)

> "The point now is just not to trust the user's input at all." (David Malan)

This is the same lesson as SQL injection from earlier in the course, wearing a different hat: whatever validation happens on the page the visitor controls is a convenience for well-meaning visitors, never a security boundary. Module 11's Flask routes will need to check everything again, on the server, where the visitor can't reach in and delete the check.

> ❌ **The trap:** shipping a form with `pattern` or `type="email"` and calling the input "validated." It isn't: not until the server checks it too.

---

## Key takeaways

1. **HTML describes a tree, it doesn't run.** Two terms of art (tags and attributes) and no loops, conditionals, or variables. Every element you write becomes a node in the browser's DOM.
2. **The browser ignores whitespace; you must be explicit.** Paragraphs, line breaks, and spacing in your source file mean nothing until you mark them with the right tag (`<p>`, etc.).
3. **Each building block is verb-first.** `<p>`, `<h1>`-`<h6>`, `<ul>`/`<ol>`/`<li>`, `<table>`, `<img>`, `<video>` each tell the browser what kind of content is coming, and some (like `<img>`) never need a closing tag.
4. **A link's visible text and its real destination are independent.** That's what makes hyperlinks convenient, and what makes phishing possible.
5. **A GET form just builds a query string.** Filling in `<input name="q">` and submitting is the same as typing `?q=...` into the URL bar yourself.
6. **Client-side validation (`pattern`, `type="email"`) is a convenience, not security.** Anyone can delete it in their own browser copy of your page before submitting.
7. **The W3C validator is a free second pair of eyes.** Run every page you write through it before you consider it done.

## Common pitfalls

- ❌ Forgetting a closing tag and assuming it's fine because the page "looks okay": the DOM the browser actually built may not match what you intended, and the validator will catch it even when your eyes don't.
- ❌ Relying on blank lines or extra spaces in your HTML source to create visual separation: use `<p>`, headings, or (in the next lesson) CSS instead.
- ❌ Shipping an `<img>` with no `alt` attribute: it's invisible to screen readers and to anyone whose connection is too slow to load the image.
- ❌ Trusting `pattern` or `type="email"` as your only validation: it must be checked again on the server, which you'll start doing in Module 11.
- ❌ Clicking a link based on its visible text alone: check the actual `href` destination first, especially for anything requesting a password or payment information.

---

## 🛠️ Capstone Project: Build Your Personal Home Page

> This is the main hands-on project for the lesson. You'll build a single-file personal home page from scratch on cs50.dev, serve it with `http-server`, and get it to pass the W3C validator with zero errors, proving to yourself, in a green checkmark, that you can write structurally correct HTML by hand.

### What you will build

One file, `home.html`, served locally with `http-server` on port 8080. It will contain, at minimum: a heading structure, a list, a table, an image with `alt` text, a working hyperlink, and a search form that `GET`s to Google with a named input: every building block from this lesson, in one page.

| Lesson idea | Where you use it in this Capstone |
|---|---|
| Doctype, `html`/`head`/`body` (Part 1) | The skeleton every milestone below builds inside of. |
| `http-server` on port 8080 (Part 1) | How you actually view `home.html` in a browser tab. |
| Headings, paragraphs (Part 2) | Your name, a short bio, and section titles. |
| Lists (Part 2) | A bulleted or numbered list of interests, courses, or goals. |
| Tables (Part 2) | A small table of structured facts about yourself (favorites, a schedule, whatever fits). |
| Images with `alt` (Part 2) | A photo or graphic with real alternative text. |
| Anchor tags (Part 3) | At least one working link to a real site you'd recommend. |
| Forms and GET (Part 3) | A search box that submits to Google with `name="q"`. |
| W3C validator (Part 3) | The finish line: zero errors before you call it done. |

### Milestones (build them in order, each one works on its own)

1. **Scaffold the file.** On cs50.dev, create `home.html` with the doctype, `<html lang="en">`, a `<head>` with a `<title>`, and an empty `<body>`. Run `http-server`, open the green "Open in Browser" link (or the Ports tab), and confirm you see a blank but correctly-titled page.
2. **Add your headings and a short bio.** Add an `<h1>` with your name, one or two `<p>` paragraphs about yourself, and at least one `<h2>` subheading dividing the page into sections.
3. **Add a list.** Under an appropriate heading, add a `<ul>` or `<ol>` of at least three items: interests, favorite courses, goals, anything real.
4. **Add a table.** Build a small `<table>` (ideally with `<thead>`/`<th>` for column labels) showing some structured fact about yourself: a weekly schedule, a list of favorites with categories, or similar.
5. **Add an image with real alt text.** Embed an `<img>` (a photo, a logo, anything you have rights to use) with a `src` and a genuinely descriptive `alt` attribute, not a placeholder like `"image"`.
6. **Add a hyperlink.** Add an `<a>` tag linking to a real site, with visible text that honestly describes the destination, the opposite of the phishing trick from Part 3.
7. **Add a search form.** Add a `<form>` with `action="https://www.google.com/search"`, `method="get"`, and an `<input name="q">` plus a submit button. Confirm that typing a query and submitting lands you on a real Google results page.
8. **Validate.** Copy your full `home.html` into [validator.w3.org](https://validator.w3.org/#validate_by_input) and fix every error it reports (missing closing tags, missing `alt`, anything else) until it shows zero errors.
9. **Stretch goals.** Add a nested list (a sub-list inside one `<li>`), embed a `<video>` with `controls`, or add a second form field using `pattern` to validate an email address, then open developer tools and delete the `pattern` attribute yourself, to see the client-side trust warning from Part 3 firsthand.

### How you will know you are done

- ✅ `http-server` serves `home.html` from cs50.dev, and you can open it in a browser tab and read every section.
- ✅ The page contains at least one heading, one list, one table, one image with non-empty `alt` text, one working hyperlink, and one working search form.
- ✅ Submitting the search form actually lands you on a real Google search results page.
- ✅ Pasting your HTML into validator.w3.org shows **zero errors**.

> 💡 **Keep yourself honest:** don't just eyeball your HTML for correctness: actually run it through the validator. Passing on sight and passing validation are two different things, and only one of them is objective.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: hello.html from memory (foundational)
Without copying an existing file, type out `hello.html` from scratch: doctype, `<html lang="en">`, a `<head>` with a `<title>`, and a `<body>` with one line of text. Serve it with `http-server` and confirm the title shows correctly in the browser tab. Then delete the closing `</html>` tag on purpose and paste the file into validator.w3.org to see exactly what error message a missing closing tag produces.

### Exercise 2: structure a wall of text (intermediate)
Take three unstructured paragraphs of text (write your own, or generate some placeholder text), and turn them into a properly tagged page: an `<h1>` title, an `<h2>` for each paragraph's topic, the paragraph itself in `<p>`, and a `<ul>` list summarizing the three topics at the bottom. Validate the result.

### Exercise 3: a safer search form (advanced)
Build the mini Google clone from Part 3 (`<form method="get" action="https://www.google.com/search">` with `<input name="q">`), then add a second, separate form with an email field using `pattern=".+@.+\..+"`. Confirm the pattern blocks bad input. Then open developer tools, find the `<input>` in the Elements panel, and delete the `pattern` attribute directly in your browser's copy of the page. Submit again with obviously-invalid text and confirm it now goes through: direct, hands-on proof that client-side validation is not a security boundary.

---

## Cheat sheet

```text
MINIMAL HTML5 BOILERPLATE
  <!DOCTYPE html>
  <html lang="en">
      <head><title>...</title></head>
      <body>...</body>
  </html>

TERMS OF ART
  tag       = <p> or </p>              -- the bracketed marker
  element   = <p>text</p>              -- open tag + contents + close tag
  attribute = lang="en"                -- key="value" inside an opening tag
  DOM       = the tree the browser builds in memory from your HTML

SERVE IT LOCALLY (cs50.dev)
  http-server            -- serves current folder over HTTP on port 8080
                          -- (80 / 443 are already used by cs50.dev itself)

BUILDING BLOCKS
  <p>...</p>                       paragraph (whitespace alone does NOT create one)
  <h1>...</h1> ... <h6>...</h6>    headings, biggest/most-important to smallest
  <ul><li>...</li></ul>            bulleted list
  <ol><li>...</li></ol>            numbered list
  <table><tr><td>...</td></tr></table>   rows (tr) of cells (td)
  <thead><tr><th>...</th></tr></thead>   column headings
  <img src="..." alt="...">        image -- no closing tag; alt is not optional
  <video controls><source src="..." type="video/mp4"></video>

LINKS AND FORMS
  <a href="https://example.com">visible text</a>    -- text and href are independent!
  <form action="URL" method="get">
      <input name="q" type="search">
      <input type="submit" value="Go">
  </form>                                            -- GET = builds a ?key=value query string

REGEX QUICK REFERENCE
  .   any character        *  0 or more     +  1 or more     ?  0 or 1
  [abc]  one of a/b/c       \d digit         \D not-a-digit    \. literal period

VALIDATE
  https://validator.w3.org/#validate_by_input   -- paste HTML, fix every error, zero left = done

THE ONE RULE THAT MATTERS MOST
  Anything checked only in the browser (pattern, type="email", JS) can be deleted
  by the visitor before they submit. Never trust it as security -- only the server can enforce that.
```

## How this connects to the rest of the course

- **Earlier, Module 10 · Lesson 35 (HTTP and the browser):** gave you the envelope: verbs, status codes, headers; this lesson opened it and showed you what's actually inside: the HTML file itself.
- **Earlier callback, Module 6 · Lesson 23 (Trees, hash tables, and tries):** you already built a tree by hand out of nodes and pointers; today you saw the browser build one automatically from your HTML, called the DOM.
- **Next, Module 10 · Lesson 37 (CSS and JavaScript):** styles the exact same HTML you just wrote, and then teaches you to reach into the DOM tree and change it live, without reloading the page.
- **Later, Module 10/11 · Lesson 39:** the form you built here to `GET` a Google search will `POST` instead, to a real route on a server you wrote yourself: no more borrowing someone else's back end.
- **North star:** every template your Flask application renders in Module 11 is, underneath whatever Python generates it, exactly the HTML you learned to write by hand in this lesson.

---

*Source: "CS50x 2026 - Lecture 8 - HTML, CSS, JavaScript" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
