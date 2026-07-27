# Module 12 · Lesson 43: Shipping Your Final Project

> **Course:** Self-Paced CS50x
> **Module 12:** The finish line: ship something of your own.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 10 - The End](https://www.youtube.com/watch?v=ApQTgFkf8TU) · [full transcript](../../transcripts/13-lecture-10-the-end.txt)
> **Estimated time:** 60 minutes (plus the project itself, which is open-ended)

---

## In one sentence

This lesson is where CS50 lets go of your hand: you'll decide what to build and set good/better/best goals for it, move, if you choose, off cs50.dev to your own local editor with Git and Docker, pick a place to host what you make, and line up the AI tools and human communities you can lean on, then spend the Capstone writing a real, one-page plan for your own final project and taking its first three actual commits.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you write a one-page plan for your own final project (problem, users, good/better/best goals, data model, routes, and a hosting choice) and then take the first three real steps toward building it. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Dev environments and AI copilots will keep changing; the discipline of tracking your own work in versioned snapshots will not.
>
> - **[Pro Git](https://git-scm.com/book/en/v2)** (Scott Chacon and Ben Straub: free, official). The canonical, tool-agnostic explanation of what a commit, a repository, and version control actually are, independent of cs50.dev, GitHub, or any particular editor. Read chapters 1-2 if Part 4's three commands leave you wanting the "why," not just the "how."

## A few plain-language basics first

This lesson uses some everyday-sounding terms in a specific way. Here they are in plain words:

- **Local development environment:** the tools you use to write and run code that live on your own computer, instead of in a browser tab talking to a server somewhere else.
- **IDE (integrated development environment):** a program that bundles a code editor, a way to run your code, and tools for catching mistakes, all in one window. Visual Studio Code, the tool you've been using at cs50.dev this whole course, is one; Cursor and Windsurf are others.
- **Command line (terminal):** a text-only window where you type commands instead of clicking buttons. It's the same kind of window you've already used inside cs50.dev, just running on your own machine now, if you choose.
- **Containerization (Docker):** a way of packing up a whole pre-configured computing environment, every tool CS50 installed for you, into one file that runs the same way on any computer.
- **Git, repository, and commit:** Git is a tool that keeps a history of every saved version of your code. The project folder it's watching is called a **repository** ("repo"); each saved, labeled snapshot of your work is called a **commit**. This is what's been powering the "timeline" feature in cs50.dev all along.
- **Static site vs. web app:** a static site is just HTML/CSS/JavaScript files with no server-side code, a portfolio, say. A web app has a "back end": code like Flask that runs on a server, often talking to a database, so it can log users in, save their data, and change what it shows.
- **Hosting / deploying:** putting your finished project on a server somewhere on the internet, so anyone with a link, not just you, can open it.

You do not need to memorise these. Each is explained again the first time it matters below.

## Why this lesson matters

For ten weeks, every problem set arrived with Malan's own spec, his own starter files, and his own idea of what "done" looked like. Your final project has none of that: as Malan puts it, it "takes all of those training wheels off." The tools this lesson adds (your own dev environment, Git, a hosting account) aren't busywork. They're the difference between a project that only ever lives inside cs50.dev and one you can actually hand someone a link to, long after this course ends. And for the first time, you get real help doing it: "You essentially have a junior colleague next to you who can help solve bugs for you, point you in the right direction, even tackle features as well."

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why the final project "takes off the training wheels," and set your own good/better/best goals for it.
2. Choose between staying on cs50.dev, moving to a local VS Code + Docker setup, or trying an AI-native editor like Cursor or Windsurf, and state the trade-off each choice makes.
3. Run the three core Git commands (`git init`, `git add`, `git commit`) to version a project, and explain what a repository and a commit are.
4. Pick a hosting option (GitHub Pages, Netlify, or a cloud provider's student tier) that matches whether your project is a static site or a full web app.
5. Write a one-page plan for your own final project (problem, users, good/better/best goals, data model, and routes) and take the first real steps toward building it.

## Prerequisites

- **Module 11 (Lessons 38-41, Flask):** the routes, templates, forms, database, and session stack this lesson's Capstone assumes as your project's default shape.
- **Module 8 (SQL, Lessons 28-31):** table design with primary and foreign keys, needed for the data-model sketch below.
- **Module 12 · Lesson 42 (Abstraction, precision, and how far you've come):** the immediately preceding lesson.
- A free GitHub account (the same one behind cs50.dev): you'll use it again here for local Git, hosting, and the Student Developer Pack.

---

## Part 1: The final project: training wheels off

Every problem set so far came with Malan's own instructions, his own starter code, his own definition of "done." That changes today. As Malan tells students, "the intent of the final project is to be the very first of hopefully many projects that you decide to spec out for yourself." Where every pset before this one was "written by me and the team," and you were "following our instructions step by step," the final project "takes all of those training wheels off."

That doesn't mean starting from nothing. You're explicitly "welcome and encouraged to borrow code" from an earlier problem set (Problem Set 9 if you want something web-based, or an earlier one if you'd rather build something else) or to "start with a completely empty window and just a blinking prompt." Either is fine. What matters is that the result is, in the end, your own.

**Good, better, best.** The spec asks you to set three tiers of goal for yourself, and Malan quotes them directly: "a good goal which you intend to meet no matter what, a better goal, which is a bit more of a stretch and a best goal, which in practice rarely ever happens with software." Read that last clause carefully: even Malan, 25-plus years after taking CS50 himself, admits he still "consistently underappreciate[s] just how long it takes sometimes to solve problems." Best-tier goals are aspirational *by design*. Plan only for "best" and you'll likely finish nothing; plan around "good" and you finish something real, with "better" and "best" as bonuses.

> 🔑 **The single most important takeaway of this part:** write down a "good" goal you can actually finish, on purpose, before you write down anything more ambitious. Everything past "good" is a bonus, not the plan.

**AI as a junior colleague, not a replacement.** The one genuinely new ingredient since Malan's own CS50 days: "you essentially have a junior colleague next to you who can help solve bugs for you, point you in the right direction, even tackle features as well." That's Lesson 32's "amplify, don't replace" idea again, now applied to a project with no answer key to check yourself against, which makes your own judgment about what the AI hands back matter *more*, not less.

**The only real requirement.** Strip away the logistics and the ask is simple: "build something of interest to you, that you solve an actual problem." Try, in the spec's own words, to "change the world," or at least to "try to create something that outlives the course itself... and even continue on with it if you'd like in January and beyond."

> 🎯 **The goal, restated:** not a perfect project, but one real enough that you'd keep improving it after this course ends, and interesting enough that you'd want to.

## Part 2: Your support system: the hackathon and the CS50 Fair

Training wheels off doesn't mean alone. CS50 has two long-standing rituals built specifically to support the final project.

**The hackathon.** As Malan describes it, "a long standing tradition of CS50 is this epic late nighter, the CS50 hackathon": pizza, then ice cream, and for anyone still awake past midnight, "we'll get in a whole bunch of CS50 shuttles, drive down the road to the International House of Pancakes, which is open 24/7, and have some breakfast together if you choose, with some pancakes together at this local IHOP." It's a social work session, not a test.

Crucially, the staff's role there is deliberately limited. In Malan's words, "the teaching staff and I will be there on hand, not so much to answer any and all questions for you, but to help you help yourselves, point you at resources, point you at, uh, the requisite websites, the documentation, so as to empower you ultimately to solve this here problem, uh, for yourself." That's the whole final-project philosophy in one sentence: help still exists, but it now looks like being pointed at a resource, not handed an answer.

> 💡 **Taking this course on your own?** You don't need an official hackathon to get this benefit. Pick one evening, tell a friend what you're building and when you'll show them, and make "point myself at the documentation first" your own rule before asking an AI or a forum to just solve it for you.

**The CS50 Fair.** The other tradition is the finish line itself: "the goal ultimately is to prepare you for the end of semester exhibition, the so-called CS50 fair, which will be an opportunity to present your final projects on your phones or laptops" to anyone who walks by: faculty, students, staff, visitors. The payoff, in Malan's words, is "delighting in what it is you have achieved over these past few months alone," and, at the very end, "by the end of it you'll pick up your very own CS50 t-shirt which says hopefully proudly that you have now indeed taken CS50."

> ✅ **What to do about it:** build your project so you can demo it in under two minutes to a stranger who knows nothing about it. That constraint, not "does it have every feature," is what a fair (or a self-paced equivalent: a short video, a live demo to a friend) actually tests.

## Part 3: Leaving cs50.dev: your own local environment

Everything you've written in this course has run inside **cs50.dev**. As Malan explains, "this is just an adaptation of a commercial tool called GitHub CodeSpaces, which is like a cloud-based version of Visual Studio Code itself, or VS Code," and, he adds, "it is the tool that so many programmers around the world do use every day to write code." In other words: you haven't been learning a toy. "You have been learning all this time sort of industry standards," just with some menu options turned off and AI disabled by default.

Now that you're past Problem Set 9, you have a choice. cs50.dev remains completely valid for your final project: "you are welcome to keep using this for your final project if feeling more comfortable with it." But you're also free to install VS Code on your own Mac or PC directly.

Two honest warnings come with that choice. First: "it's fairly straightforward to install it, but invariably you'll run into probably some technical support headaches depending on the language that you're trying to use with it": Python, for instance, needs to be installed separately, and you'll want its latest version. Second, and more important: "just know a priori that sometimes just stuff happens and it just doesn't work and you have to Google or ask Chat GPT, and that's fine. And honestly that's kind of normal." Hitting a setup snag doesn't mean you're behind. It means you're doing what every working programmer does routinely.

If you want cs50.dev's exact pre-installed toolset, but running on your own machine, CS50 documents a technology called **containerization**: "you can use a technology known as containerization with a tool called Docker and actually run a CS50 environment on your Mac or PC or even in the cloud, but still run VS code on your own Mac and PC." The upside: "You can do everything offline, which is useful in general. You can do things more quickly sometimes if you're using the full capabilities of your own computer and not just a browser."

VS Code isn't the only option, either. "Perhaps the trendiest right now are these 3 here, not just Visual Studio Code itself, but a tool called Cursor, another one called Windsurf," both AI-native editors built for exactly the AI-amplified coding described in Part 1. Malan notes there are "dozens of other" IDEs beyond these three.

| Option | What it is | Best for |
|---|---|---|
| Stay on cs50.dev | The cloud VS Code you've used all course | Zero setup risk; entirely fine to ship your whole final project here |
| Local VS Code + Docker | Real VS Code on your own Mac/PC, containerized to match cs50.dev | Offline work, your computer's full speed, the industry-standard path |
| Cursor or Windsurf | VS Code-like editors built AI-first | Wanting AI woven into every keystroke, not just a chat panel |

> ❌ **The trap to avoid:** treating a rough local install as a reason to give up on the project, or on local tools altogether. As Malan says, hitting friction here is "kind of normal," and cs50.dev is still there if you'd rather spend your time building than debugging your setup. But "you can't go wrong transitioning from CS50 to VS code on your own Mac or PC if only because you're already familiar with it," so it's worth one afternoon of friction if you have it to spare.

## Part 4: Command line, Git, and working with others

**The command line was never new: just hidden.** Mac users, Malan notes, "might have found somewhere in your utilities folder a program called Terminal," and if not, "poke around there later today and you'll see that all this time you've had a command line interface available to you on Mac OS." Windows has an equivalent. CS50 has been abstracting one particular command-line tool for you this entire course: **Git**.

**What Git actually is.** In Malan's words, Git "is something that we actually in CS50 abstract on top of. This is essentially the de facto standard nowadays for collaborating with other people. Using a central cloud server in order to share your code with it and in turn other people for versioning your code so that you keep track of multiple versions thereof and changes that you've made." Put plainly: Git tracks a **repository** (the project folder it's watching), and every labeled snapshot you save is a **commit**. You've been making commits this whole course without typing the word "git" once: "if you've ever gone through your timeline in cs50.dev being able to roll back to previous versions of your code, we're just using Git" automatically, underneath.

From here on, you can drive it yourself, using three commands at the command line:

```text
git init                 # start tracking this folder as a repository
git add <file>            # stage a file's changes to be saved
git commit -m "message"   # save a labeled snapshot of everything staged
```

For a full walkthrough, Malan points students to "a tutorial by CS50's own Brian Yu introducing you to actual Git," worth watching once if you've never typed a Git command directly yourself.

**Working with a partner.** If your final project has more than one author, Git can coordinate that. But Malan offers an easier option for two people working together in real time: "I will encourage you to alternatively use Visual Studio Code's live share feature, which allows one of you to log into your code space, click some buttons, and then share access to your code space with your friend or your partner with whom you're working on the project, and you can both in real time, like Google Docs, edit the code or different files they're in using that one code space."

> 🔑 **The single most important takeaway of this part:** you don't need to learn Git perfectly before you start. `git init`, `git add`, and `git commit`, repeated often, cover the vast majority of a solo final project. Live Share covers real-time pair work without needing any Git knowledge at all.

## Part 5: Hosting your project, and who to ask when you're stuck

**If your project is a static site** (just HTML, CSS, and JavaScript, no server-side code), hosting is close to free. "Two popular places to go, if only because they offer free tiers," is "what's called GitHub Pages, which you can use to just host HTML, CSS and JavaScript with no Python, no Flask, no back end." Netlify is the other free option Malan names, aimed at the same kind of static, write-once-and-deploy content, a portfolio site, for instance.

**If your project needs a back end** (and a Flask app talking to a SQLite database, the default shape this course has built toward, does), the list of hosts gets longer, and, Malan is upfront, "all of these recommendations are essentially curated by the teaching staff, so they're all opinionated." Amazon, Microsoft, Google, and Cloudflare all offer cloud hosting; Heroku and Vercel are two other names that come up often. The good news for a student: "Amazon, Microsoft, Google, Cloudflare, they all have student-type accounts. So if you use your .edu email address... you can generally sign up for discounts and free access to a lot of these same services... without having to pay while you're just learning along the way." GitHub itself "has something similar called the Student Developer Pack." As Malan defines it, "by web app we mean not just HTML CSS and JavaScript, but maybe some Python, maybe some JavaScript on the server, maybe Ruby... when you actually need a back end in addition to the front end, maybe you need a database as well": exactly the Flask + SQLite shape from Modules 8 and 11.

**When you're stuck, you now have two channels of help.** The first is AI, freshly un-gated for the final project: Malan frames it as "moving away from the duck, which by design has been fairly limited and meant to be a good teacher, but not necessarily one that's going to be a good partner when it comes to building your final project," toward tools like ChatGPT, Claude, Gemini, and GitHub Copilot, which he singles out as probably the easiest to start with since it's built directly into the VS Code you already know.

The second channel is still human. "Among the places that programmers and technophiles have gone for years are Reddit, Stack Overflow, Server fault, where there's a rich history of questions and answers that ironically all of those AIs have been trained on... But when you actually want that human component, these are still good places to go." And if you want to go deeper into a topic than this course had time for (more Python, more SQL, a language called R, cybersecurity, game development), CS50 itself "has a rich history now over the past decade of creating all the more open courseware... All of those are linked at this URL here, edX.org/cs50, where you need not pay or sign up beyond the course and all of the content is freely available."

> ✅ **What to do about it:** decide whether your project is static or a web app *before* picking a host. That one question (does anything need to run on a server?) eliminates most of the list immediately.

**How it all fits together.** Every idea in this lesson is one path, walked once, from a cloud tab to a shipped link:

```text
  cs50.dev  (or local VS Code + Docker, or Cursor/Windsurf)
          |
          v
  Command line + Git   (git init -> git add -> git commit)
          |
          v
  Working with a partner?  --Live Share-->  real-time, no Git needed
          |
          v
  Push your code
          |
          v
  Hosting:  static (GitHub Pages / Netlify)  or  web app (cloud host + student pack)
          |
          v
  Stuck along the way?  AI (Copilot/ChatGPT/Claude/Gemini)  +  humans (Reddit/Stack Overflow)
          |
          v
  A real, shipped final project, demoed at the CS50 Fair
```

---

## Key takeaways

1. **Final projects have no answer key.** You write the spec (good, better, best), and AI is a junior colleague, not a replacement for your own judgment about what it hands back.
2. **Support doesn't disappear just because instructions do.** The hackathon and the CS50 Fair (or your own equivalent) exist to help you help yourself: pointed at resources, not spoon-fed answers.
3. **Moving to a local VS Code + Docker setup, or an editor like Cursor or Windsurf, is optional but mirrors real industry practice**, and hitting setup friction there is "kind of normal," not a sign you're behind.
4. **Git is what's been auto-saving your cs50.dev timeline all along.** Now you can drive it yourself with `git init`, `git add`, and `git commit`; Live Share covers real-time pair work without any Git at all.
5. **Static sites are nearly free to host (GitHub Pages, Netlify); a web app needs a back end and a database**, and student discounts plus the GitHub Student Developer Pack make the real cloud providers free while you're learning.
6. **When you're stuck, you have two channels:** AI (ChatGPT, Claude, Gemini, Copilot) for speed, and humans (Reddit, Stack Overflow, classmates) for the kind of judgment those very AIs were trained on.

## Common pitfalls

- ❌ Treating "best" as the plan: Malan's own goals "in practice rarely ever happen with software." Start from "good," the version you will actually finish.
- ❌ Abandoning the project over local setup pain: cs50.dev remains a completely valid choice for the entire final project if local tools fight you.
- ❌ Writing code before sketching the data model: sitting down to build before you've drawn your tables and keys is how database-backed projects stall halfway through.
- ❌ Asking AI to build the whole thing in one prompt, the same caution from Lesson 32 applies: without "an eye for what you're looking at," you can't safely trust or fix what it gives you.
- ❌ Choosing a host before knowing whether you need a back end: a static host like GitHub Pages cannot run Flask or Python. Check that fit first.

---

## 🛠️ Capstone Project: Your Final Project Plan and First Three Commits

> This is the main hands-on project for the lesson, and it isn't a simulation: this plan and these first commits are the actual, literal start of your real CS50 final project.

### What you will build

Two things: (1) a one-page written plan for your final project, and (2) a live, version-controlled repository containing that plan and a working Flask skeleton, the true first commits of the project you'll keep building after this lesson.

Default shape assumed below: a database-backed web app (Flask + SQLite + HTML/CSS/JS), the exact stack Modules 8-11 already taught you end to end. If you're building something else entirely (a game, a command-line tool, a pure static site), keep Milestones 1, 2, 6, and 7 as they are, and adapt 3 and 4 to your own project's equivalent of "state" and "actions," a Scratch game's variables and blocks instead of tables and routes, for instance.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Good / better / best goals (Part 1) | Milestone 2: you write all three tiers explicitly |
| "Help yourself" / point-at-resources framing (Part 2) | You write the plan alone first, before asking AI or a forum for help |
| Local dev environment or cs50.dev (Part 3) | Wherever you `git init`, in Milestone 6 |
| Git basics (Part 4) | Milestones 6-8: init, add, commit, for real |
| Hosting choice (Part 5) | Milestone 5 |
| Flask + SQLite stack (Modules 8, 11) | Milestones 3, 4, and 9 |

### Milestones (build them in order, each one works on its own)

1. **Name your problem and your users, in writing.** One paragraph: what problem does this solve, and who has it? ("A shared chore tracker for my apartment's four roommates" beats "a to-do app.") This alone is a real, usable artifact even if you go no further today.
2. **Write your good/better/best goals.** One sentence each, following the spec Malan quotes: a *good* goal you will finish no matter what; a *better* goal that's a real stretch; a *best* goal you may never reach. Be honest: "good" should be small enough that you aren't tempted to skip straight to "better."
3. **Sketch your data model.** List each table your app needs, its columns, and which column is the primary key (plus any foreign keys linking tables together): pen and paper or a plain text file is enough. A chore tracker might need `users(id, name)` and `chores(id, description, assigned_to, done)`, where `chores.assigned_to` is a foreign key into `users.id`.
4. **List your routes.** For each page or action your app needs, write the URL path and whether it's a GET (just viewing) or a POST (submitting or changing something): for example, `GET /` (home page), `GET /chores` (list), `POST /chores/new` (add one), `POST /chores/<id>/complete` (mark done).
5. **Pick a host, and write one sentence why.** Static site with no back end? GitHub Pages or Netlify. Flask + database, like the default shape above? A cloud provider's free or student tier: claim the GitHub Student Developer Pack first if you have a school email.
6. **`git init` a real repository for this project.** Wherever you're coding (cs50.dev, local VS Code, Cursor, or Windsurf), create a new folder for this project and run `git init` inside it.
7. **Commit a `README.md` containing your plan.** Paste in the paragraph, the three goals, the table sketch, and the routes list from Milestones 1-4. Then run `git add README.md` and `git commit -m "Add project plan"`. This one commit is your project's real starting line.
8. **Create the Flask skeleton from Lesson 38 and commit it.** A minimal `app.py` with one `@app.route("/")`, a `templates/` folder with a base layout, running locally or in whichever environment you chose. `git add` the new files and `git commit -m "Add Flask skeleton"`.
9. **Stretch goals.** Deploy the empty skeleton to your chosen host right now, before you've built any features: confirming your hosting pipeline works early saves a last-minute scramble later. If you have a partner, set up Live Share and make one small edit together, in real time.

### How you will know you are done

- ✅ A `README.md`, committed to a real Git repository, containing your problem/users paragraph, your three goal tiers, your table sketch (with primary and foreign keys marked), and your routes list.
- ✅ At least two real commits in your project's Git history (the plan, then the skeleton) visible with `git log`.
- ✅ A running Flask skeleton (or your project's own equivalent starting point) that loads without errors.
- ✅ You can say, in one sentence, which host you picked and why it fits your project's needs.

> 💡 **Keep yourself honest:** if your "good" goal takes more than a sentence to describe, it's probably actually your "better" goal in disguise. Split it and shrink "good" further. An over-ambitious "good" goal is the single most common way final projects stall.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Three Git commands, in your own words (foundational)
In any terminal (cs50.dev's, or your own machine's), create an empty folder, run `git init`, create one file, then run `git add` and `git commit -m "..."` on it. Run `git status` before and after each step, and write one sentence per command describing what changed.

### Exercise 2: Static or web app? (intermediate)
Take your own final-project idea (or the chore-tracker example above) and write two sentences: does it need a back end (server-side code, a database) or not, and which single hosting option from Part 5 follows from that answer?

### Exercise 3: Set up a local or AI-native environment (advanced)
Following CS50's own documentation, install either VS Code + Docker or one of Cursor/Windsurf on your own computer, and get a trivial "Hello, world" running outside cs50.dev. Write down the one hiccup you hit (there's usually exactly one) and how you solved it: Google, an AI assistant, and Stack Overflow all count as legitimate answers.

---

## Cheat sheet

```text
FINAL PROJECT, IN ONE LINE
  No more instructions from Malan. You write the spec. AI is a junior colleague, not the author.

GOOD / BETTER / BEST
  GOOD   = you will finish this, no matter what
  BETTER = a real stretch, might not happen
  BEST   = aspirational: "rarely ever happens with software," even for Malan

DEV ENVIRONMENT OPTIONS
  cs50.dev                zero setup risk, still fully valid to ship on
  Local VS Code + Docker  offline, full computer speed, matches cs50.dev exactly
  Cursor / Windsurf       AI-native editors, same idea as VS Code

GIT, THE THREE COMMANDS THAT COVER MOST OF A SOLO PROJECT
  git init                   start tracking this folder
  git add <file>             stage a change
  git commit -m "message"    save a labeled snapshot
  (working with a partner in real time? use VS Code Live Share instead)

HOSTING
  Static site (HTML/CSS/JS only)  -> GitHub Pages or Netlify (free)
  Web app (Flask + database)      -> cloud provider's student/free tier,
                                      or claim the GitHub Student Developer Pack first

WHEN STUCK
  AI:     ChatGPT, Claude, Gemini, GitHub Copilot
  Humans: Reddit, Stack Overflow, classmates
  Deeper dives (free): edX.org/cs50

THE PLAN, ONE PAGE
  1. Problem + users
  2. Good / better / best goals
  3. Data model (tables + primary/foreign keys)
  4. Routes (GET/POST + path)
  5. Hosting choice + why
```

## How this connects to the rest of the course

- **Earlier, Module 11 (Lessons 38-41):** Flask routes, templates, forms, server-side validation, SQLite persistence, and sessions gave you the exact stack this lesson's Capstone assumes as the default final-project shape.
- **Earlier, Module 12 · Lesson 42 (Abstraction, precision, and how far you've come):** the immediately preceding lesson, closing the loop on why precision and choosing the right level of abstraction, the two lessons from Malan's own first CS50 lecture notes, mattered in every language this course touched.
- **Next: life after this course.** There is no Lesson 44. From here, the official CS50 problem sets live at cs50.harvard.edu/x, if you want to work through the real course's own psets toward a verified certificate on edX, including its finance pset, which has you build exactly the kind of user registration, password hashing, and login system that Module 11's sessions lesson already gave you the pieces for. Beyond that, the project you scope and start shipping in this lesson's Capstone *is* the answer to "what's next": the whole point of the final project, in Malan's words, is to "create something that outlives the course itself... and even continue on with it if you'd like in January and beyond."

And with that, in Malan's own closing words to the room: "This is CS 50 and all right, this was CS 50, cake is now served."

---

*Source: "CS50x 2026 - Lecture 10 - The End" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to your own final project's language and framework.*
