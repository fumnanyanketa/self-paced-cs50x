# Module 10 · Lesson 37: CSS and JavaScript

> **Course:** Self-Paced CS50x
> **Module 10:** The web: from packets to pages people can use
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 8 - HTML, CSS, JavaScript](https://www.youtube.com/watch?v=yYst7puZXjw) · [full transcript](../../transcripts/11-lecture-8-html-css-javascript.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

You'll take the plain HTML page you already wrote and give it a personality, first with your own CSS selectors and one hover effect, then with Bootstrap's ready-made styles pulled in from a CDN, and then bring it to life with a few lines of JavaScript that reach into the page's DOM and change what the user sees the instant they click, with no reload.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you restyle your Lesson 36 home page three times over: your own CSS, then Bootstrap, then one JavaScript button that changes the page's colors live. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** CSS frameworks like Bootstrap will be replaced by newer ones, and browsers will keep adding features, but the rules for what a selector or a property or a method like `addEventListener` actually means are written down in places that outlive any one framework.
>
> - **[MDN Web Docs: CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)** and **[MDN Web Docs: JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)**, maintained by the Mozilla Foundation and the broader web standards community. This is the reference every working developer reaches for: plain-language, example-driven explanations of exactly what a selector, a property, or a method does.
> - **[The ECMAScript Language Specification](https://tc39.es/ecma262/)**, maintained by Ecma International's TC39 committee. This is the formal specification that every JavaScript engine (Chrome's V8, Firefox's SpiderMonkey, and the rest) is built to satisfy: the rulebook behind the `let`, `for`, and `function` syntax you're about to see.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **CSS (Cascading Style Sheets):** the language that controls how an HTML page *looks*: colors, sizes, spacing, layout, as opposed to HTML, which only controls what content exists.
- **Selector:** the part of a CSS rule that says *which* HTML elements the rule applies to: by tag name, by class, or by a unique ID.
- **Class and ID:** two ways to label an HTML element so CSS (or JavaScript) can find it. A class (written `.name` in CSS) can be reused on many elements at once; an ID (written `#name`) is meant for exactly one element on the page.
- **Cascade:** the "C" in CSS: a style property set on a parent element automatically flows down to everything nested inside it, unless a more specific rule overrides it.
- **DOM (Document Object Model):** the tree-shaped structure the browser builds in memory from your HTML. You met this in Lesson 36. CSS paints the nodes of that tree; JavaScript is what can add, remove, or change them while the page is running.
- **Event:** something that happens on a page that code can listen for and react to: a click, a key going up, a form being submitted.
- **Method:** a function that belongs to a specific object, called with a dot, like `document.querySelector(...)`: the same dot notation you've already used for structs in C and objects in Python.
- **CDN (Content Delivery Network):** a server run by someone else that hosts a popular file (like Bootstrap's CSS) so you can link to their copy instead of writing or hosting it yourself.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 36 gave you the skeleton of a page: tags, attributes, the tree the browser builds. Today you give that skeleton a surface, and then a nervous system. Malan draws the line between the two new languages of the day like this:

> "CSS is like the skin, the aesthetics thereof, the final mile that actually allows you to control the positioning of things more precisely, the colors, the font sizes, all of the aesthetics." (David Malan)

Nothing here starts from zero. The hex color codes from Lesson 17 (`#FF0000`) are exactly the values you'll type into a CSS `color` property, and the dot notation you used for C structs and Python objects is the same dot notation behind `document.querySelector(...)`. And it points forward too: every page your Module 11 Flask application serves will load this same CSS and this same JavaScript, unchanged, so this lesson is, quite literally, the entire look and feel of the database-backed web app you finish this course with.

## Learning objectives

By the end of this lesson you will be able to:

1. Apply an inline `style` attribute, then refactor repeated styles into a single `<style>` tag using type, class, and ID selectors.
2. Explain the "cascade" in CSS, how a property set on a parent flows down to its children, and use it to remove repetition.
3. Use the semantic tags `header`, `main`, and `footer`, add an HTML entity, and add a `:hover` rule that changes an element on mouseover.
4. Load a CSS framework (Bootstrap) from a CDN with one `<link>` tag and apply its classes without writing new CSS.
5. Read a short JavaScript snippet and explain how its variables, conditionals, and loops compare to the equivalent C or Python code.
6. Use `document.querySelector()`, `addEventListener()`, and `innerHTML` (or `.style`) together to find a DOM node, listen for a user event, and change the page live.

## Prerequisites

- **Module 10 · Lesson 36: Building pages with HTML**: you'll be styling and scripting the exact `home.html` you built there, and you already know the DOM tree that CSS and JavaScript both operate on.
- **Module 5 · Lesson 17: Pixels, hex, and addresses**: you already know hex color codes like `#FF0000`; today they show up again as CSS values.
- **Module 2 · Lesson 07: Conditionals and loops** (or your general comfort with C or Python): this lesson compares JavaScript's syntax directly against what you already know.
- A cs50.dev (GitHub Codespaces) account with `http-server`, from Lesson 36.

---

## Part 1: From inline styles to the style tag (and the cascade)

### The style attribute: CSS's first, clumsiest home

The simplest way to stylize one HTML element is to add a `style` attribute directly on its tag, with semicolon-separated `key: value` pairs. CSS calls these **properties**, the same key-value idea as HTML attributes, just with a colon instead of an equals sign:

```html
<div style="font-size: large; text-align: center;">John Harvard</div>
<div style="font-size: medium; text-align: center;">Welcome to my home page.</div>
<div style="font-size: small; text-align: center;">Copyright &#169; John Harvard</div>
```

This works, but it repeats `text-align: center` on every single line, the kind of duplication that should bother you by now from every earlier module.

### The cascade: say it once, on the parent

CSS's full name is *cascading* style sheets, and the cascade is exactly the fix for that duplication:

> "If you want one property or key value pair to sort of cascade down on all of the other tags inside of that one, you can do that." (David Malan)

Move the shared property up to the parent element (`body`, in this case) and every child inherits it automatically:

```html
<body style="text-align: center;">
    <div style="font-size: large;">John Harvard</div>
    <div style="font-size: medium;">Welcome to my home page.</div>
    <div style="font-size: small;">Copyright &#169; John Harvard</div>
</body>
```

`text-align: center` is now written exactly once, and it still applies to all three `div`s, because they are `body`'s children in the DOM tree from Lesson 36.

### Factoring it out: the style tag

Repeating `style="..."` on every tag is still clutter: it mixes your content (the data) with its presentation (the CSS) in the same line. CSS lets you factor all of it into one `<style>` tag in `<head>`, using **selectors** to say which elements each rule applies to:

```html
<head>
    <style>
        body {
            text-align: center;
        }
        header {
            font-size: large;
        }
        main {
            font-size: medium;
        }
        footer {
            font-size: small;
        }
    </style>
</head>
<body>
    <header>John Harvard</header>
    <main>Welcome to my home page.</main>
    <footer>Copyright &#169; John Harvard</footer>
</body>
```

Nothing looks different in the browser, but the HTML is now just content, and the `<style>` block is entirely presentation. `body`, `header`, `main`, and `footer` here are **type selectors**: a rule that names a tag applies to every element with that tag.

> 🔑 **The single most important takeaway of this part.** CSS properties are just key-value pairs, exactly like HTML attributes with different punctuation. The cascade means you almost never have to repeat a property on every element: set it once, on a shared parent or a shared selector, and let it flow down the tree.

---

## Part 2: Selectors, semantic tags, entities, and Bootstrap

### Type selectors aren't reusable enough

Tying `font-size: large` to the `header` tag works, but only because you happen to have one `header`. If you wanted "large and centered" for some other, unrelated element too, a type selector can't help: it's tied to the tag name. CSS offers two more ways to select elements for exactly this reason:

> "These properties can be applied to different selections of HTML type selectors, class selectors, ID selector, attribute selector." (David Malan)

A **class** (prefixed with `.` in CSS, written as `class="..."` in HTML) is a label you can put on *any number* of elements to reuse the same properties:

```css
.centered { text-align: center; }
.large    { font-size: large; }
.medium   { font-size: medium; }
.small    { font-size: small; }
```

```html
<body class="centered">
    <header class="large">John Harvard</header>
    <main class="medium">Welcome to my home page.</main>
    <footer class="small">Copyright &#169; John Harvard</footer>
</body>
```

An **ID** (prefixed with `#` in CSS, written as `id="..."` in HTML) is meant for exactly *one* unique element, the same uniqueness convention you'll rely on in Part 3 when JavaScript needs to find one specific node.

### Semantic tags: hints for machines, not just humans

Notice the example above already stopped using generic `<div>`s in favor of `<header>`, `<main>`, and `<footer>`. These carry no different *visual* behavior on their own, but they carry meaning:

> "There are literally tags like header which allows me to define the header of the page, main, which allows me to define the main part of the page, and then even footer, which allows me to define that too." (David Malan)

Search engines crawling a public page read these tags as hints about what matters most, the **semantic web**, in Malan's words: giving machines, not just people, a better sense of what they're looking at.

### HTML entities: characters HTML can't type directly

A copyright symbol isn't on most keyboards, and some characters (like `<`) are reserved by HTML's own syntax. HTML solves this with **entities**, a short, punctuated code the browser converts into a specific character:

> "HTML also has what are called entities." (David Malan)

`&#169;` renders as ©. The syntax is always an ampersand, a code, and a semicolon, the same trick that lets you write a literal `<` as `&lt;` when you need HTML syntax to appear as plain text instead of being interpreted.

### :hover: a selector for a state, not a tag

CSS also has **pseudo-selectors**: selectors that target a temporary *state* an element can be in, rather than its tag, class, or ID. The most common is `:hover`:

> "I can have these pseudo selectors whereby I say the name of the tag, then a keyword like hover, which browsers know to recognize, and when I hover over an anchor, what I want to do is change the text decoration to underline temporarily." (David Malan)

```css
a {
    color: #FF0000;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
```

Notice `#FF0000`, the exact hex color format from Lesson 17, now doing double duty as a CSS value. And `#harvard` here would be an ID selector, not a hex color, even though both use `#`: CSS tells them apart entirely from context (inside a `color` property, it's hex; as a bare selector, it's an ID).

### Bootstrap: someone else's CSS, one link away

Writing every property by hand doesn't scale, which is why **frameworks** exist, pre-written CSS (and often JavaScript) that you adopt by reading its documentation instead of authoring your own:

> "One of the most popular frameworks out there nowadays and among the simplest and best documented is one called Bootstrap, which is a set of CSS classes and other features that you can use because it's open source in your own code." (David Malan)

You load it from a CDN, a server someone else runs specifically to host popular files like this:

> "It's referencing a third party website, JSD Deliver, which is a CDN content delivery network, which is to say a server that just serves up content for other people to use." (David Malan)

(That "JSD Deliver" is jsDelivr, a real, widely-used CDN: the transcript's ear for a spoken URL, not a typo you need to reproduce.)

```html
<link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    rel="stylesheet">
```

Then a class does the rest, no new CSS required:

```html
<table class="table table-striped">
    ...
</table>
```

Two lines changed the whole look of a plain table into neatly striped rows, exactly as documented on Bootstrap's own site.

> ✅ **What to do about it:** before writing a CSS rule by hand, check whether Bootstrap already has a class that does it: read the docs, copy the class name, and save yourself the property-by-property work.

---

## Part 3: JavaScript (syntax you already know, wearing new punctuation)

### The one real programming language of the day

HTML describes a tree; CSS paints it. JavaScript is different: an actual programming language, with variables, conditionals, and loops, that runs inside the browser after being downloaded like everything else:

> "Most every website you use is made from not only HTML and CSS, but if it's in any way interactive, odds are it's using JavaScript, a programming language that is very commonly used client side, whereby humans write the code on the server, but then your browser, as before, downloads it to the client and then it runs in your own Mac, your PC or your phone." (David Malan)

Because you already know Scratch's blocks, Python, and C, JavaScript's syntax needs almost no new teaching, just a translation table:

| Concept | Scratch | Python | C | JavaScript |
|---|---|---|---|---|
| Declare a variable | `set counter to 0` | `counter = 0` | `int counter = 0;` | `let counter = 0;` |
| Increment | `change counter by 1` | `counter += 1` | `counter++;` | `counter++;` |
| Conditional | `if <...> then` | `if condition:` | `if (condition) { }` | `if (condition) { }` |
| Loop 3 times | `repeat 3` | `for _ in range(3):` | `for (int i = 0; i < 3; i++) { }` | `for (let i = 0; i < 3; i++) { }` |
| Loop forever | `forever` | `while True:` | `while (true) { }` | `while (true) { }` |

`let` replaces a type name (`int`, `char *`) because JavaScript variables don't declare a type up front. Curly braces are back (unlike Python's indentation), and semicolons are conventionally expected (unlike C, where they're required, but similar enough that you should just keep using them).

### The DOM, but now you can change it

Lesson 36 introduced the DOM, the tree the browser builds from your HTML. JavaScript is what turns that tree from a one-time snapshot into something you can edit while the page is running:

> "What you have most powerfully though is the ability in memory to mutate this tree in real time." (David Malan)

Think of your email inbox: a table row per message. Without JavaScript, seeing new mail means reloading the whole page, a whole new tree, downloaded from scratch. With JavaScript, code can add a single new table-row node to the existing tree the moment new mail arrives, leaving everything else untouched.

### Three building blocks: querySelector, addEventListener, innerHTML

Nearly everything interactive on the web reduces to three pieces working together.

**`document.querySelector(...)`** finds a node in the tree, using the exact same selector syntax as CSS, a tag name, a `.class`, or a `#id`:

> "Query selector is a fancy name for a function that lets me select specific elements of the page using CSS selector." (David Malan)

**`addEventListener(...)`** tells a node to wait for something to happen, then run a function when it does:

> "Add event listener is a function or method that you can call on any element that just tells it to listen subsequently for this event, and when that event is heard, submit in this case, call the following anonymous function, otherwise known as a lambda function." (David Malan)

This is the same idea as Scratch's "when green flag clicked", an **event** (a click, a key going up, a form submission) triggers code, instead of code just running top to bottom once.

**`innerHTML`** (to rewrite what's *inside* a node) and **`.style`** (to rewrite one of its CSS properties) are how your code actually changes something once it's found the right node and heard the right event.

One naming quirk trips up everyone the first time: CSS properties with a hyphen, like `background-color`, become camelCase in JavaScript:

> "Anything with hyphens in CSS is changed to Camelcase in JavaScript." (David Malan)

So `background-color` in a `<style>` tag is `element.style.backgroundColor` in JavaScript: a hyphen would be read as subtraction, which is why the language can't use it in a property name.

> 🔑 **The single most important takeaway of this part.** Every interactive feature on the web is some version of the same three-step pattern: find a node with `querySelector`, listen for an event with `addEventListener`, and change the node (its style, or its `innerHTML`) inside the function that runs.

---

## Part 4: The DOM, live (six demos that bring it together)

```text
   HTML (Lesson 36)  -->  builds the DOM tree, once, on load
   CSS  (Parts 1-2)  -->  paints each node: color, size, layout
   JS   (Part 3)     -->  listens for events, edits the tree, live

        event (click / keyup / submit)
              |
              v
     document.querySelector('#thing')   -- finds the node
              |
              v
     node.style.backgroundColor = 'red'    -- repaint (CSS via JS)
     node.innerHTML = '<li>word</li>'      -- rebuild (new child nodes)
```

### 1. A greeting form

Malan starts with a form, a text input, and a submit button, then wires it up three different ways to make the same point. The first attempt uses an `onsubmit` attribute directly on the `<form>` tag, calling a `greet()` function defined in a `<script>` in `<head>`. The refactored version moves the logic into an `addEventListener` call instead, placed at the very end of `<body>` (or guarded by a `DOMContentLoaded` listener), to make sure the form already exists by the time the code runs:

```html
<body>
    <form>
        <input id="name" placeholder="Name" type="text" autocomplete="off" autofocus>
        <input type="submit">
    </form>
    <script>
        document.querySelector('form').addEventListener('submit', function () {
            const name = document.querySelector('#name').value;
            alert('Hello, ' + name);
            return false;
        });
    </script>
</body>
```

`return false` stops the browser from actually submitting the form to a server: without it, the alert would flash and then the page would try to navigate away.

### 2. Color-change buttons

Three buttons, each with a unique `id`, each wired to change the whole page's background:

```html
<button id="red">R</button>
<button id="green">G</button>
<button id="blue">B</button>
<script>
    const body = document.querySelector('body');
    document.querySelector('#red').addEventListener('click', function () {
        body.style.backgroundColor = 'red';
    });
    document.querySelector('#green').addEventListener('click', function () {
        body.style.backgroundColor = 'green';
    });
    document.querySelector('#blue').addEventListener('click', function () {
        body.style.backgroundColor = 'blue';
    });
</script>
```

Notice `backgroundColor`, not `background-color`, the camelCase rule from Part 3 in action.

### 3. The blink tag, revived

HTML used to have an actual `<blink>` tag; it was ugly enough that it was removed from the language entirely, one of the rare tags to be deprecated outright. Malan brings the effect back with JavaScript instead:

> "This is what the blink tag used to do back in the day. Now this version is implemented instead in JavaScript code." (David Malan)

```html
<body>
    <p>hello, world</p>
    <script>
        window.setInterval(blink, 500);
        function blink() {
            const body = document.querySelector('body');
            if (body.style.visibility == 'hidden') {
                body.style.visibility = 'visible';
            } else {
                body.style.visibility = 'hidden';
            }
        }
    </script>
</body>
```

`window.setInterval(blink, 500)` calls the `blink` function every 500 milliseconds, forever. One more naming quirk to note along the way:

> "You would think that the opposite of visible would be invisible, but in CSS the opposite of visible is hidden. Just have to memorize stupid things like that." (David Malan)

### 4. Autocomplete search

Backed by a large JavaScript array of words (`large.js`, built from Problem Set 5's dictionary), a `keyup` listener filters that array on every keystroke and rewrites an empty `<ul>` with matching results:

```html
<input id="q" type="text" placeholder="Query" autocomplete="off">
<ul id="results"></ul>
<script src="large.js"></script>
<script>
    document.querySelector('#q').addEventListener('keyup', function () {
        const input = document.querySelector('#q');
        let html = '';
        if (input.value) {
            for (const word of WORDS) {
                if (word.startsWith(input.value)) {
                    html += '<li>' + word + '</li>';
                }
            }
        }
        document.querySelector('#results').innerHTML = html;
    });
</script>
```

This is exactly the pattern behind every search box you've ever typed into:

> "Someone wrote JavaScript that's listening for keyU or the like, and then dynamically populating an unordered list or in this case a much prettier list of the matching results." (David Malan)

### 5. A Bootstrap navbar

Bootstrap isn't only CSS classes: it ships its own JavaScript too, for things like a responsive navigation bar that collapses into a "hamburger" icon on narrow screens:

> "It's listening for clicks on this hamburger menu and revealing the menu options that way." (David Malan)

You get this by copying Bootstrap's documented navbar markup and including both their CSS `<link>` and their JavaScript `<script>`, no hand-written JavaScript of your own required.

### 6. Geolocation

One more built-in browser feature, exposed as a JavaScript object called `navigator`:

> "There exists another global variable in JavaScript in browsers called Navigator, which has a property called an object called geolocation which has a function called get current position that takes an argument which is just an anonymous function, which means call this code when you're ready to know the coordinates because it might take a while to figure out your GPS coordinates." (David Malan)

```html
<script>
    navigator.geolocation.getCurrentPosition(function (position) {
        document.querySelector('body').innerHTML =
            position.coords.latitude + ', ' + position.coords.longitude;
    });
</script>
```

The browser asks the visitor's permission first (for privacy), then hands your callback function the coordinates once they're known, the same building block behind every map or delivery app asking "can this site use your location?"

---

## Key takeaways

1. **CSS is skin, not skeleton.** Properties are key-value pairs, exactly like HTML attributes, applied to elements through selectors.
2. **Inline style → `<style>` tag → external `.css` file is a one-way street of "factoring out."** Each step separates content (HTML) from presentation (CSS) a little further.
3. **The cascade is the "C" in CSS.** A property set on a parent, or via a type selector, flows down to every descendant unless something more specific overrides it.
4. **Three selector types cover most needs.** Type (a tag name), class (`.name`, reusable across many elements), and ID (`#name`, unique to one), the same lookup JavaScript's `querySelector` uses.
5. **A framework is just someone else's classes, loaded from a CDN.** Bootstrap changes your page's whole look with one `<link>` and a couple of class names, no new CSS required.
6. **JavaScript is the one real programming language of the three.** Same variables, conditionals, and loops as C, with `let` instead of a type and no semicolons required (but keep using them).
7. **Everything interactive reduces to one pattern.** Find a node with `querySelector`, listen for an event with `addEventListener`, and change it: a `.style` property or its `innerHTML`.

## Common pitfalls

- ❌ Forgetting to reload the page after editing CSS or JavaScript: the browser is still showing the last downloaded copy, not your saved file.
- ❌ Writing a CSS property with a hyphen (`background-color`) inside JavaScript exactly as written. JavaScript needs the camelCase form (`backgroundColor`); the hyphenated version silently does nothing.
- ❌ Placing a `<script>` tag in `<head>` that tries to `querySelector` an element defined later in `<body>`: that element doesn't exist yet, so the selector returns nothing. Put the script at the end of `<body>`, or guard it with a `DOMContentLoaded` listener.
- ❌ Giving two elements the same `id`. IDs are supposed to be unique; JavaScript's `querySelector('#name')` will quietly return only the first match, changing the wrong element (or nothing at all) and leaving you confused about why.
- ❌ Assuming Bootstrap replaces the need to understand plain CSS. Bootstrap is just someone else's classes; when its default look isn't quite right, you still need type, class, and ID selectors to override it.
- ❌ Confusing a class (reusable, `.name`) with an ID (unique, `#name`), using one where you meant the other is a common reason a selector matches nothing, or matches too much.

---

## 🛠️ Capstone Project: Give Your Home Page a Personality

> This is the main hands-on project for the lesson. You'll restyle the exact `home.html` you built in Lesson 36 three times over, your own CSS, then Bootstrap, then one JavaScript button, proving to yourself that you can control both the look and the behavior of a page you already know how to build.

### What you will build

The same single file, `home.html`, still served locally with `http-server` on port 8080. By the end it will contain: a `<style>` tag using a type, a class, and an ID selector; one `:hover` effect; a swapped-in Bootstrap CDN link with at least one Bootstrap class applied; and one JavaScript button that changes the page's colors on click, with no reload.

| Lesson idea | Where you use it in this Capstone |
|---|---|
| Inline style → style tag (Part 1) | Refactoring your home page's look into one `<style>` block in `<head>`. |
| Cascade (Part 1) | Setting one property once, on `body` or `main`, instead of repeating it. |
| Type / class / ID selectors (Part 2) | Styling all paragraphs at once, a reusable class, and one unique element. |
| Semantic tags + entities (Part 2) | Wrapping your page in `header`/`main`/`footer` and adding a real copyright entity. |
| `:hover` (Part 2) | Making a link or button visibly react when the mouse moves over it. |
| Bootstrap via CDN (Part 2) | Swapping your hand-written CSS for Bootstrap's classes with one `<link>` tag. |
| `querySelector` + `addEventListener` + `.style` (Part 3-4) | The button that changes your page's colors without reloading. |

### Milestones (build them in order, each one works on its own)

1. **Reopen your home page.** On cs50.dev, open the `home.html` you built in Lesson 36 (or start a fresh copy with the same skeleton) and confirm `http-server` still serves it on port 8080.
2. **Write your own `<style>` tag.** In `<head>`, add a `<style>` block with at least one type selector (e.g. `body { }`), one reusable class applied to two or more elements (e.g. `.highlight { }`), and one ID selector for a single unique element (e.g. `#name { }`).
3. **Add semantic structure.** Wrap your existing sections in `<header>`, `<main>`, and `<footer>` instead of generic `<div>`s, and add a real HTML entity: a copyright symbol (`&#169;`) in your footer is a good fit.
4. **Add one `:hover` effect.** Pick a link or button and give it a rule like `a:hover { text-decoration: underline; }` so it visibly reacts the moment the mouse moves over it.
5. **Swap in Bootstrap.** Add Bootstrap's CDN `<link>` to `<head>`, then apply at least one real Bootstrap class (`table table-striped` on a table, or `btn btn-primary` on a button) and confirm the look changes with no new CSS of your own.
6. **Add one JavaScript behavior.** Add a button (or reuse three, for red/green/blue) with a unique `id`, then write a `<script>` that uses `document.querySelector()` to find it, `addEventListener('click', ...)` to listen for a click, and `.style.backgroundColor = '...'` to change the page's color live.
7. **Reload and verify everything.** Confirm every change (CSS and JavaScript alike) actually shows up after a manual reload. Trust what the browser shows you right now, not what you remember writing.
8. **Stretch goals.** Add a second and third color button; recreate the blink effect on one small element using `window.setInterval` and toggling `style.visibility`; or wire up a tiny autocomplete over an array of 10 words you choose, using `keyup` and `innerHTML`.

### How you will know you are done

- ✅ Your home page has a `<style>` tag with at least one type selector, one class selector (used on two or more elements), and one ID selector.
- ✅ At least one element visibly changes when you hover your mouse over it.
- ✅ Your page loads Bootstrap from a CDN `<link>`, and at least one Bootstrap class is visibly changing something (compare it against removing the class).
- ✅ Clicking your button changes the page's background or text color immediately, with no page reload, using `querySelector` + `addEventListener`.
- ✅ You reloaded the page after your very last edit and it behaves exactly as you expect.

> 💡 **Keep yourself honest:** open developer tools' Elements panel and confirm the CSS you expect is actually attached to the node you clicked, the same trick Malan uses throughout the lecture to debug his own examples live, on his own page, in real time.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: John Harvard's page, twice (foundational)
Build a three-section page (a name, a welcome line, and a copyright line) exactly as Malan does it live: first stylize each section with an inline `style` attribute (different `font-size` per section, `text-align: center` on all three), confirm it in the browser, then refactor into one `<style>` tag in `<head>` using `header`/`main`/`footer` type selectors, and move `text-align: center` up to `body` so it's written exactly once, thanks to the cascade.

### Exercise 2: Three-button mood ring (intermediate)
Build `background.html` from scratch: three buttons labeled R, G, and B, each with a unique `id`, plus a `<script>` that uses `querySelector` and `addEventListener('click', ...)` on each button to set `document.querySelector('body').style.backgroundColor`. Add a fourth button that resets the color back to white.

### Exercise 3: Tiny autocomplete (advanced)
Write a JavaScript array of 10 words you choose, a text `<input>`, and an empty `<ul>`. On the `keyup` event, loop over your array with `for (const word of words)`, check whether each word starts with the current input value using `.startsWith()`, and rewrite the `<ul>`'s `innerHTML` with one `<li>` per match, the same technique behind the search-box autocomplete you use every day.

---

## Cheat sheet

```text
CSS: THREE PLACES TO WRITE IT
  inline    <p style="color: red;">...</p>            -- one element, one-off
  internal  <style> p { color: red; } </style>         -- in <head>, whole page
  external  <link rel="stylesheet" href="style.css">   -- separate file, reusable

SELECTORS
  type      body { }        -- every <body> element
  class     .name { }       -- every element with class="name" (reusable)
  ID        #name { }       -- the one element with id="name" (unique)
  pseudo    a:hover { }     -- a state, not a tag -- fires on mouseover

CASCADE
  set a property on a parent (or use a type selector) and it flows down to
  every child unless a more specific rule overrides it

SEMANTIC TAGS + ENTITIES
  <header> <main> <footer>          -- hints for humans and search engines
  &#169;                             -- HTML entity for the copyright symbol (c)

BOOTSTRAP VIA CDN
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet">
  <table class="table table-striped">   -- someone else's CSS, one class away

JS SYNTAX VS C / PYTHON
  let x = 0;                 -- variable, no type
  x++;                       -- same as C, not Python
  if (x > 0) { }             -- curly braces, not indentation
  for (let i = 0; i < 3; i++) { }
  while (true) { }
  background-color  (CSS)  ->  backgroundColor  (JS)   -- hyphen becomes camelCase

DOM IN THREE PIECES
  document.querySelector('#id')       -- find a node
  node.addEventListener('click', fn)  -- listen for an event (click, keyup, submit...)
  node.innerHTML = '<li>...</li>'     -- rewrite what's inside a node
  node.style.backgroundColor = 'red'  -- rewrite a CSS property live

THE ONE RULE THAT MATTERS MOST
  Everything interactive on the web is: listen for an event, find a node,
  change it. That's the whole trick behind buttons, autocomplete, and navbars.
```

## How this connects to the rest of the course

- **Earlier, Module 10 · Lesson 36 (Building pages with HTML):** gave you the plain skeleton, and the exact DOM tree this lesson's CSS paints and JavaScript now reaches into and edits live.
- **Earlier callback, Module 5 · Lesson 17 (Pixels, hex, and addresses):** the hex color codes you met there (`#FF0000`) are exactly the values CSS's `color` and `background-color` properties accept.
- **Earlier callback, Module 2 (C) and Module 1 · Lesson 4 (Programming in Scratch):** JavaScript's `let`, `if`, and `for` are the same ideas as C's syntax and Scratch's blocks, just with different punctuation.
- **Next, Module 11 · Lesson 38 (Flask fundamentals: routes and templates):** a Python server starts generating the HTML you've been writing by hand, but it will still load exactly this CSS and this JavaScript, unchanged.
- **North star:** the style tag, the Bootstrap swap, and the color-change button you build today are, quite literally, the entire look and feel of the database-backed web app you'll finish this course with.

---

*Source: "CS50x 2026 - Lecture 8 - HTML, CSS, JavaScript" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
