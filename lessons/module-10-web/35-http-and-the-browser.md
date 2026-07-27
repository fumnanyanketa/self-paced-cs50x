# Module 10 · Lesson 35: HTTP and the Browser

> **Course:** Self-Paced CS50x
> **Module 10:** The web: from packets to pages people can use
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 8 - HTML, CSS, JavaScript](https://www.youtube.com/watch?v=yYst7puZXjw) · [full transcript](../../transcripts/11-lecture-8-html-css-javascript.txt)
> **Estimated time:** 45 minutes (read plus exercises)

---

## In one sentence

Every time a browser loads a page it sends a small text message (a request, usually **GET** or **POST**) to a server named in the URL, and gets back a text message of its own (a **status code** like 200, 301, or 404, plus headers and content), and you can read both halves of that conversation yourself with a one-line terminal command or your browser's own DevTools.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called the **Status-Code Safari**, where you collect a 200, a 301, a 404, and (if you can find one) a 418 from real websites, then use your browser's DevTools to inspect a live request and live-edit a page's headline. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Browsers and terminal tools will keep changing, but the rules governing what they say to each other are written down and version-controlled like any other spec:
>
> - **[RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)** (IETF, 2022). This is the current official specification that defines the `GET` and `POST` methods and every status code you'll see today: 200, 301, 404, and yes, even 418 traces its lineage to this family of documents. Whatever browser or `curl` version you're using a decade from now, it will still be speaking this same underlying language.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **HTTP:** short for HyperText Transfer Protocol: the agreed-upon set of rules a browser and a web server use to ask for a web page and send one back. It's a *protocol*, not a programming language: just a standardized format for the text inside the "envelopes" from the last lesson.
- **URL:** short for Uniform Resource Locator: the full web address you type, click, or paste, like `https://www.harvard.edu/admissions`. Every URL is built from smaller, named parts, which Part 1 breaks apart piece by piece.
- **TLD:** short for top-level domain: the last segment of a domain name, like `.com`, `.edu`, `.org`, or `.io`. A small, controlled list decides who is allowed to hand out names ending in each one.
- **GET:** the HTTP request that means "send me this page (or file, or image)" without asking the server to change anything. Clicking almost any link on the web sends a GET.
- **POST:** the HTTP request that means "here is some data: please store it or act on it." Submitting a form (logging in, posting a comment) typically sends a POST instead.
- **Status code:** the three-digit number a server sends back with every response, summarizing what happened: found it, moved, not found, and so on. It rides inside the response before any of the actual page content.
- **Header:** one line of "information about the information" inside a request or a response, not the page's content itself, but metadata about it, like what type of file it is or where to go instead.
- **DevTools:** short for Developer Tools: a panel built into every modern browser (Chrome, Edge, Safari, Firefox) that lets you inspect the requests a page made and the code that built it, live, as it happens.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Last lesson you learned how a packet physically finds its way from your device to a server: IP addresses, ports, DNS, all the plumbing underneath the web. This lesson opens the envelope. Once IP and TCP have gotten your data to the right computer, HTTP is the language the browser and server actually speak to each other inside it, and it turns out you don't have to take that on faith. As Malan puts it:

> "We, as aspiring programmers, can actually see and poke around with these building blocks and ultimately today take advantage of them." (David Malan)

That's the whole point of this lesson: two free tools, a terminal command called `curl` and the DevTools already built into your browser, let you watch, in plain text, exactly what your browser is asking for and exactly what it's being told back. That skill isn't academic. Every route you write in your own web app, starting in Module 11, will be debugged with these exact same tools: is my server returning a 200 or a 500? Did that form actually POST what I think it did? What header is missing? You are about to learn to read the conversation your browser has been having, invisibly, your entire life online.

## Learning objectives

By the end of this lesson you will be able to:

1. Read any URL and correctly label its scheme, host name, domain, top-level domain (TLD), and path.
2. Explain what an HTTP GET request asks a server to do, and how a POST request differs.
3. Use `curl -I` in a terminal to read a real website's response headers without downloading or rendering the whole page.
4. Interpret the status codes 200, 301, 404, and 418, and say what each one tells the browser to do next.
5. Use a browser's DevTools **Network** tab to find the method, status code, and headers of any request a page made.
6. Use the DevTools **Elements** tab to make a live, temporary edit to a page's HTML, and explain why that edit disappears on reload.

## Prerequisites

- **Module 10 · Lesson 34: How the internet works**: this lesson assumes you already know what IP addresses, ports, and DNS are. Today opens the envelope that lesson showed you how to address and deliver.
- A modern browser: Chrome, Edge, Firefox, or Safari all work; this lesson's screenshots and instructions use Chrome, but every browser's DevTools looks almost identical.
- Comfortable at a terminal (from earlier modules) helps for the `curl` demos, but isn't required: the DevTools half of this lesson needs nothing but a browser.

---

## Part 1: Reading a URL like a browser does

Every URL looks like a jumble of punctuation until you know it's actually a small number of named parts, each doing one job. Take this one apart:

```text
   https   ://   www   .   harvard   .   edu   /admissions
   ─────         ───       ───────   ───      ───────────
   scheme        host      domain    TLD          path
```

| Part | What it means | In `https://www.harvard.edu/admissions` |
|---|---|---|
| **Scheme** | The protocol being used to fetch this resource, almost always `http` or `https` (`https` adds encryption). | `https` |
| **Host name** | The specific server, or cluster of servers, being asked for. It doesn't have to be one physical machine, as Malan notes, "`www` can refer to dozens of hundreds, thousands of servers." | `www` |
| **Domain + TLD** | The registered name, rented from a registrar, plus its top-level domain: the category it belongs to. | `harvard.edu` (`.edu` is the TLD) |
| **Path** | The specific file or folder being requested on that server. | `/admissions` |

If you leave the path off entirely (just `https://www.example.com/`), you're asking for the **root**, the site's default page. In Malan's words:

> "Root just means the default directory, the default folder, if you will." (David Malan)

Behind the scenes, that root usually corresponds to an actual file named something like `index.html`: you're just spared from having to type its name yourself.

TLDs used to be a short, memorable list (`.com`, `.gov`, `.net`, `.org`, `.edu`), but that list has grown into the hundreds. Some, like CS50's own `.io`, aren't what they look like at first glance:

> "CS50 uses `.io` a lot, which doesn't mean input-output. It's actually a two-letter country code that has been essentially rented to us." (David Malan)

> 🔑 **The single most important takeaway of this part.** A URL is not a blob of text: it's a small, ordered set of named fields (scheme, host, domain, TLD, path), and every one of them means something specific to the server reading it.

## Part 2: GET vs POST (the two verbs behind almost everything you click)

A URL only tells the browser *where* to ask. What actually goes inside the request is a short, plain-text message (not code, just a standardized sentence) and it starts with a verb:

> "HTTP supports a bunch of operations or verbs, namely GET, POST, and a few others." (David Malan)

The two you'll meet constantly:

- **GET**: "send me this." This is what your browser sends every single time you click a link, type a URL, or load an image. It asks the server to hand over a copy of something, and it isn't supposed to change anything on the server's end.
- **POST**: "here's data for you." This is what a browser sends when you submit a form: logging in, posting a comment, uploading a file. Instead of just asking for a copy of something, it's handing the server new information to store or act on.

Picture the "envelope" from Lesson 34 again. If you're requesting Harvard's homepage, the message inside that envelope is literally close to this:

```text
GET / HTTP/2
Host: www.harvard.edu
```

Malan describes exactly that scenario:

> "GET, in all caps, slash: if she just wants the root, or the default page from Brian's server." (David Malan)

And whatever comes back is also just text: a status line, then a batch of headers, then (usually) the actual page:

> "Brian's envelope would have contained a textual message that just confirms what version of HTTP he's using, a status code... and he would specify the type of content he's sending back to her." (David Malan)

You'll meet POST properly, and build a real form that uses it, in Lesson 39. For now, the important thing is knowing that GET and POST exist, and that "just loading a page" and "submitting something" are, underneath, two different kinds of message.

> ✅ **What to do about it:** whenever you're not sure what a button or a link on a page actually does, remember that a plain click is (almost always) a GET, and a submitted form is (almost always) a POST: you'll be able to confirm exactly which, for real, in Part 4.

## Part 3: Status codes (the server's one-line verdict)

Every HTTP response starts with a three-digit **status code**: the server's own summary of what just happened, before you even get to the content. You can see these yourself, from a terminal, using a program called `curl`:

> "Curl... stands for Connect URL... it's a headless browser that allows you to pretend to be a browser and grab the response from a server." (David Malan)

Adding the `-I` flag (capital `i`) asks `curl` to show *only* the response's status line and headers, not the page itself:

> "Curl -I... is only going to show me the headers, the text that we were just talking about, and it's not going to send any of the contents of Harvard's website." (David Malan)

> 💡 **A small technical nuance.** `curl -I` doesn't quite send the same request a browser sends when loading a page: it uses a request method called `HEAD`, which explicitly asks the server for "headers only, skip the body." That's why it comes back instantly even for a huge page: the server never bothers assembling the content at all.

Here's what a handful of real demos reveal:

**A healthy page returns `200 OK`**: the best possible outcome, meaning "here's exactly what you asked for":

```text
$ curl -I https://www.harvard.edu
HTTP/2 200
content-type: text/html; charset=UTF-8
...
```

**An insecure URL often returns `301 Moved Permanently`**: a redirect. Requesting the plain `http://` (not `https://`) version of Harvard's site doesn't return the page at all:

```text
$ curl -I http://www.harvard.edu
HTTP/1.1 301 Moved Permanently
Location: https://www.harvard.edu/
```

Malan explains exactly what that number means:

> "If a server responds to a browser with a numeric code of 301, that means that the browser is supposed to go to this location instead. It's sort of like putting a detour sign on the server that says there's nothing for you here." (David Malan)

That's why you and I never have to type `https://` by hand anymore: the server itself insists on it via a 301.

**A page that doesn't exist returns `404 Not Found`**: file not found, full stop:

```text
$ curl -I https://www.harvard.edu/cats
HTTP/2 404
```

> "404 is a weirdly public, arcane... status code that just means file not found... most everyone in this room is probably familiar with 404, even though its origin is this very low level arcane status code buried in the HTTP headers." (David Malan)

**And then there's `418`,** which is not a real, serious status code at all:

> "We included 418, which is not actually a thing, but it was a fun, sort of April Fool's joke years ago where a bunch of humans thought it would be funny to write up a whole specification for what it means for a server to respond with a number of 418." (David Malan)

The specification in question is real, even if the joke is the point: it's called the "Hyper Text Coffee Pot Control Protocol," and 418 officially means **"I'm a teapot."** Because it's a joke, almost no real production website returns it on purpose: you'll need a server built specifically to demonstrate it, and the Capstone points you to one.

Malan also uses `curl -I` to demonstrate one of the internet's oldest pranks: a domain called `safetyschool.org`:

> "For years now, someone has been paying for... the following behavior." (David Malan)
>
> "Oh my goodness, look at where we are." (David Malan)

Visiting it sends back a 301, not to anywhere related to "safety schools," but to Yale's biggest rival application essay topic:

> "For like 20 years, presumably some Harvard alum has been paying the bill to rent this domain name just to have this trick implemented such that 301 moved permanently is directing people ever since to yale.edu." (David Malan)

Nothing about that trick is secret or hidden: it's just a redirect, sitting in plain text in the response headers, waiting for anyone curious enough to run `curl -I` and look.

| Code | Name | What it means |
|---|---|---|
| **200** | OK | Here's exactly what you asked for. |
| **301** | Moved Permanently | Go here instead, a redirect. |
| **404** | Not Found | The server exists, but this specific path doesn't. |
| **418** | I'm a Teapot | An intentional April Fools' joke status code, not a real error. |
| *(400s in general)* | Client error | You (or your code) asked for something wrong. |
| *(500s in general)* | Server error | The server itself is broken or crashed. |

> 🔑 **The single most important takeaway of this part.** A status code is the server's one-line verdict, sent before any content, and you never have to guess at it. `curl -I <url>` shows it to you directly, in plain text, for any website in the world.

## Part 4: DevTools (watching every request, and touching the page itself)

`curl` is a terminal tool. Your browser has the exact same X-ray vision built in, under **DevTools**, usually opened by right-clicking anywhere on a page and choosing **Inspect**, or a menu option under the browser's settings:

> "Most any browser nowadays has the ability to give you developer tools natively." (David Malan)

DevTools has several tabs; this lesson focuses on two of them.

### The Network tab: every request, laid out

The **Network** tab lists every request the current page makes, not just the main page itself, but every image, script, and stylesheet it pulled in along the way:

> "I can also see the network connections the browser is making to the server, and that's where I thought we'd start our attention here." (David Malan)

Loading a single page can trigger dozens of these. Visiting `safetyschool.org` alone, for instance:

> "Notice that bottom left here, just going to safetyschool.org resulted in 61 HTTP requests, in effect, 61 envelopes going back and forth." (David Malan)

Click on any single row and the same information `curl -I` gave you in text shows up here too, plus the exact request headers your browser sent and the exact response headers it got back:

> "The message that came back was 301 moved permanently. The protocol, or the verb, being used was GET." (David Malan)

> 💡 **Two settings worth turning on immediately.** Check **Preserve log** (so the list doesn't clear when a page redirects or navigates away) and **Disable cache** (so you always see a fresh request instead of a stale, saved one), both are checkboxes right in the Network panel's toolbar.

### The Elements tab: the live page, and your own copy of it

The **Elements** tab shows the page's actual HTML, not as a downloaded file, but as it exists right now, live, in the browser's memory. Malan opens Stanford's homepage to show it off:

> "Here is all of this HTML that some humans, or software, at Stanford wrote in order to create Stanford's homepage." (David Malan)

This works because of something genuinely different about how the web works, compared to code you've run in earlier modules:

> "Inside of those envelopes are literally copies of what's on the server being sent to the browser, and so it's your browser, the so-called client, that's actually reading that code, HTML in this case, top to bottom, left to right, and figuring out how to display it. It's not executed on the server per se." (David Malan)

You received your own copy. That copy is yours to poke at. Right-click any element on a real page (the word "Stanford" in their logo, say) and choose **Inspect**, and DevTools jumps straight to the line of HTML responsible for it:

> "It's going to jump to the very line of code that created that Stanford brand name in the middle of the web page, and this is a wonderful teaching and learning tool." (David Malan)

From there, you can edit it (live, in the panel) and watch the page change instantly:

> "I can change it to Harvard, hit enter, and now Stanford's website looks like we've been there and rather hacked it. Of course it's not that easy to hack Stanford's website... I've changed my local copy of that particular website, so if I just click on the reload icon, I'll actually see that Stanford's website, for better or for worse, still looks like that." (David Malan)

That last sentence is the whole lesson in miniature: **you edited your browser's private, in-memory copy of the page, not the file sitting on Stanford's server.** Nobody else sees your edit, and it survives exactly as long as you leave that tab open without reloading. This is precisely the "not executed on the server" idea from a moment ago, made visible: what's on the screen is a local rendering of downloaded text, and downloaded text is yours to change.

> ❌ **The trap:** it's tempting to think you've "hacked" a site the first time you do this. You haven't touched their server at all: you've only edited the copy sitting in your own computer's memory, and a reload (or anyone else opening the same page) proves it.

## Part 5: How the pieces combine

`curl -I` and DevTools' Network tab are two windows onto the exact same conversation: one from a terminal, one from a browser. Once you can read either, you can read both:

```text
   your terminal                       your browser (DevTools)
 ┌──────────────────────┐            ┌──────────────────────────┐
 │ $ curl -I https://... │            │ Network tab               │
 │ HTTP/2 301             │  ═══════  │  Status: 301              │
 │ Location: https://...  │   same    │  Response Headers:        │
 │                        │  request/  │   location: https://...   │
 │                        │  response  │                            │
 └──────────────────────┘   cycle    └──────────────────────────┘
                                              │
                                              ▼
                                     Elements tab: the HTML body
                                     that came back, now rendered
                                     as a live, editable tree
```

`curl -I` gives you the status line and headers as raw text, fast, with no rendering at all. The Network tab gives you the exact same status line and headers, plus a GUI to click through requests one by one. The Elements tab picks up where both leave off, showing you what the browser *did* with the body of that response: turned it into the page on your screen, and left it fully editable in your own copy.

---

## Key takeaways

1. **A URL is a structured address, not a blob of text.** Scheme, host name, domain, TLD, and path each mean something specific to the server reading it.
2. **GET asks for something; POST sends something.** Nearly everything you click is a GET; submitting a form is typically a POST.
3. **Status codes are the server's one-line verdict**, sent before the content: 200 (OK), 301 (moved, go here instead), 404 (not found), and the joke one, 418 (I'm a teapot).
4. **`curl -I <url>` reads a response's status and headers instantly**, from any terminal, without downloading or rendering the actual page.
5. **DevTools' Network tab shows every request/response pair a page makes**; the Elements tab shows the live HTML tree the browser built from the response, and lets you edit your own copy of it.
6. **Editing a page in DevTools only changes what's in your browser's memory.** Reload the tab, or open the page on any other computer, and the real, unchanged page is exactly as it was.

## Common pitfalls

- ❌ Believing you've changed a real website after editing it in the Elements tab: you've only changed your local, in-memory copy; a reload proves nothing was actually touched on the server.
- ❌ Assuming the Network tab is "broken" because it looks empty: usually this means **Preserve log** wasn't checked before a redirect or navigation cleared the list.
- ❌ Treating every error as the same kind of problem: a 404 means *you* (or your code) asked for something that isn't there; a 500 means the *server itself* is broken. The fix is completely different depending on which one you see.
- ❌ Being surprised by a 301 when typing `http://` instead of `https://` for a site: that's not a glitch, it's the server intentionally forcing you onto the secure version.
- ❌ Expecting to find a real, live 418 on an ordinary website: it's an April Fools' joke status code by design, so most production sites never return it on purpose.

---

## 🛠️ Capstone Project: Status-Code Safari

> This is the main hands-on project for the lesson. You will go collect real HTTP status codes from real websites using `curl -I`, then use DevTools to inspect a live request and live-edit a page, proving to yourself, hands-on, that everything in this lesson is something you can see for yourself, on any site, at any time.

### What you will build

A short written log (a text file or notes doc is fine) recording:

- Three or more real `curl -I` results, including at least one 200, one 301, and one 404.
- Your best attempt at finding (or deliberately triggering) a 418.
- One request's method, status code, and two response headers, read from DevTools' Network tab.
- A screenshot or written note of a live-edited headline in DevTools' Elements tab, plus one sentence explaining why the edit isn't permanent.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| URL anatomy (Part 1) | Choosing and reading the URLs you test. |
| Status codes + `curl -I` (Part 3) | Milestones 1 and 2, collecting 200/301/404/418. |
| DevTools Network tab (Part 4) | Milestone 3, reading a request's method, status, and headers. |
| DevTools Elements tab (Part 4) | Milestone 4, the live edit, and explaining why it resets. |

### Milestones (build them in order, each one works on its own)

1. **Collect a 200 and a 301.** Open a terminal (cs50.dev or your own machine) and run `curl -I` against two or three real sites: try one plain `http://` URL for a well-known site to see if it redirects to `https://` on its own. Record the status code from each. Done when you have at least one clean `200 OK` and one `301 Moved Permanently` (note the `Location:` header it points to).
2. **Collect a 404, and try for a 418.** Run `curl -I` against a URL you're confident doesn't exist (append something like `/this-page-does-not-exist` to a real domain) to get a 404. Then try `curl -I https://httpbin.org/status/418`, a public test server built specifically to hand back joke status codes on demand. Done when you have a 404 from a real site and a 418 from anywhere.
3. **Read one request in the Network tab.** Open DevTools on any website, check **Preserve log**, reload the page, and click on the very first request in the list (the page itself). Write down its **method** (GET or otherwise), its **status code**, and two headers you can find (for example `content-type` and `date`). Done when you can point to all four values on your own screen.
4. **Live-edit a headline in the Elements tab.** On any real website, right-click a heading or piece of text and choose **Inspect**. Double-click the text in the Elements panel and change it to something else. Watch the page update. Then reload the page and note what happens. Done when you can explain, in your own words, why the edit disappeared.

### How you will know you are done

- ✅ You have real `curl -I` output showing a 200, a 301 (with its `Location:` header), and a 404.
- ✅ You have a 418, from `httpbin.org` or elsewhere.
- ✅ You can name one request's method, status code, and two headers straight off your own Network tab.
- ✅ You can explain in one sentence why editing HTML in the Elements tab doesn't survive a reload.

> 💡 **Keep yourself honest:** don't just read the status codes in this lesson. Run the commands yourself. The entire point of this lesson is that none of this is hidden; it's plain text, sitting one command or one click away, on every website you already use.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Take a URL apart (foundational)
Write down the scheme, host name, domain, TLD, and path for each of these: `https://cs50.harvard.edu/x/2026/`, `http://safetyschool.org`, and `https://www.bbc.co.uk/news`. (Hint: the last one has a two-part TLD: `.co.uk`.)

### Exercise 2: Predict, then check (intermediate)
Pick three real websites you use often. Before running anything, guess whether typing `http://` (not `https://`) in front of each will return a 301 redirect. Then run `curl -I http://<site>` for each and see whether you were right. Note the `Location:` header for any that redirect.

### Exercise 3: Full request inventory (advanced)
Open DevTools' Network tab, load a content-heavy page (a news homepage or online store works well), and find: the single largest request by size, the total number of requests the page made to fully load, and any response that returned something other than 200. For each, note its method and status code, and explain in a sentence what you think that request was for.

---

## Cheat sheet

```text
URL ANATOMY
  https :// www . harvard . edu / admissions
  scheme    host   domain   TLD      path

HTTP VERBS
  GET   "send me this"      - clicking a link, loading a page
  POST  "here's data"       - submitting a form

STATUS CODES
  200  OK                   here's exactly what you asked for
  301  Moved Permanently    go here instead (see Location: header)
  404  Not Found            server's fine, this path isn't
  418  I'm a Teapot         April Fools' joke code, not a real error
  4xx  (general)            you/your code asked for something wrong
  5xx  (general)            the server itself is broken

CURL
  curl -I <url>             show status + headers only, no page body
                            (uses a HEAD request, instant, even on huge pages)

DEVTOOLS
  Right-click → Inspect            opens DevTools on the clicked element
  Network tab                      every request/response the page made
    ☑ Preserve log                 keep the list across redirects/reloads
    ☑ Disable cache                always fetch fresh, not a saved copy
  Elements tab                     the live HTML tree, editable in place
    (edits are LOCAL ONLY: reload restores the real page)

GOLDEN RULE
  Nothing here is hidden. curl -I and DevTools show you, in plain text,
  exactly what your browser asked for and exactly what it was told back.
```

## How this connects to the rest of the course

- **Earlier, Module 10 · Lesson 34: How the internet works:** IP addresses, ports, and DNS got a packet to the right server at all. This lesson opened that envelope and read the HTTP conversation written inside it.
- **Next, Module 10 · Lesson 36: Building pages with HTML:** you've spent this whole lesson inspecting the *outside* of a response: status, headers, verbs. The response body itself, the actual HTML that DevTools' Elements tab was rendering, is what you'll learn to write by hand starting next lesson.
- **Later, Module 10 · Lesson 39:** you'll build a real HTML form and choose, deliberately, whether it should submit with GET or POST, the same two verbs you only read about today.
- **Later still, this course's capstone:** the database-backed web app you build at the end of the course will have its own routes, its own status codes, and its own request headers. In Module 11, you will debug that app's routes with `curl` and DevTools' Network tab, the exact same tools, pointed at code you wrote yourself.

---

*Source: "CS50x 2026 - Lecture 8 - HTML, CSS, JavaScript" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
