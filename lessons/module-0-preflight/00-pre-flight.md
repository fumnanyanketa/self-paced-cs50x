# Module 0 · Lesson 0: Pre-Flight: Your Tools, Accounts, and First Success

> **Course:** Self-Paced CS50x
> **Module 0:** Pre-flight: getting set up: the optional on-ramp before Lesson 1
> **Speaker:** Self-guided (no lecture for this one)
> **Source talk:** None: this lesson exists so Lesson 1 is spent learning, not fighting setup
> **Estimated time:** 30 to 45 minutes

---

## In one sentence

Before you learn a single concept, you will set up the two free tools this whole course runs on: a cloud programming workspace at cs50.dev and a Scratch account, and prove they work by running one command and one block of code.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you run your very first command in a real programmer's
> terminal and make a cartoon cat speak. Everything before the Capstone just
> gets your accounts ready. If you already have a cs50.dev codespace and a
> Scratch account, skim the checklist and skip ahead to Lesson 1.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Browser:** the app you are reading this in (Chrome, Edge, Safari, Firefox). Everything in this course happens inside it: you install nothing.
- **GitHub:** a free website where programmers store code. You need an account only because cs50.dev uses it as your login.
- **cs50.dev (Codespace):** CS50's free, cloud-hosted copy of VS Code, a professional code editor that runs on Harvard-configured computers you borrow through your browser.
- **VS Code:** the code editor itself: part text editor, part control panel for running programs.
- **Terminal:** the text window inside VS Code where you type commands instead of clicking buttons. It looks intimidating; it is just a text conversation with the computer.
- **Scratch:** a free visual programming language from MIT where code is drag-and-drop puzzle pieces. Lesson 4 is built in it.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

CS50's lectures quietly assume every student already has a working setup. Harvard students get one in their first problem set. Following along at home without one means hitting a wall in Lesson 5 ("write hello.c… wait, where?"). Thirty minutes now buys you eleven modules of friction-free learning. It also gets your first small win on the board today, which matters more for finishing a course than any amount of enthusiasm.

## Learning objectives

By the end of this lesson you will be able to:

1. Log into a working cs50.dev codespace from any browser.
2. Type a command into a terminal and read its output.
3. Create a Scratch account and run one block of Scratch code.
4. Describe the daily ritual you'll follow for the rest of the course.

## Prerequisites

- None. This is the start.

---

## Part 1: Create your GitHub account and open cs50.dev

cs50.dev is where you will write every line of C, Python, and SQL in this course. It is free, and because it runs in the cloud, it works identically on Windows, Mac, or a library computer.

1. Go to **github.com** and sign up for a free account if you don't have one. Pick a username you don't mind a future employer seeing. It tends to stick.
2. Go to **cs50.dev** and click to log in **with that GitHub account**.
3. Authorize it when GitHub asks, then wait. The first launch builds your personal codespace and can take a few minutes. A green-and-blue VS Code screen with a **terminal panel** at the bottom means you're in.

> 💡 **If the screen looks stuck**, refresh the browser tab once after a couple
> of minutes. The first build is the slowest thing you'll ever wait for here.

> ❌ **Don't install anything locally yet.** Late in the course (Module 12)
> you'll set up VS Code on your own machine, deliberately, once you know what
> everything is. For now the cloud version is identical for everyone, which
> means every instruction in this course will match your screen exactly.

## Part 2: Say hello to the terminal

At the bottom of your codespace is the terminal: a `$` sign waiting for you to type. Click next to it and type exactly:

```bash
echo "hello, world"
```

Press Enter. The computer prints `hello, world` back. That's the whole trick: you type a command, the computer does it and shows the result. Every scary-looking terminal session in every movie is just this, faster.

Now try one more:

```bash
ls
```

`ls` lists the files in your current folder (it's short for "list"). It may print nothing at all: you haven't made any files yet. An empty answer is still an answer.

> 🔑 **The terminal is a conversation, not an exam.** Nothing you type in this
> course can break the codespace, and even if you somehow manage it, CS50 lets
> you rebuild a fresh one.

## Part 3: Create your Scratch account

Lesson 4 builds a small game in Scratch, and Lessons 1-3 borrow its ideas.

1. Go to **scratch.mit.edu** and click **Join Scratch** (free).
2. Once you're in, click **Create**. You'll see a cat on a white canvas and a palette of colorful blocks.
3. Drag the **"say Hello!"** block (purple, under *Looks*) into the big middle area, then click it. The cat speaks.

That single click was a program: an instruction you gave, a computer executed, a result you saw.

## Part 4: How this course works

Each lesson from here on follows the same rhythm, and the course works best if you do too:

```text
THE DAILY RITUAL
1. WATCH  the lecture segment linked at the top of the lesson (optional but ideal)
2. READ   the lesson top to bottom: every term is defined on first use
3. BUILD  the capstone at the end: never just read, always build
4. LOG    one line in PROGRESS.md: what you built, what broke
```

Two supporting files live in your course folder: `PROGRESS.md` (your checklist and daily log, tick lessons off, it's motivating) and `transcripts/` (the full text of every lecture, linked from each lesson if you want the source). The official problem sets at **cs50.harvard.edu/x** are excellent extra reps after each module: this course teaches the lectures; the psets make it stick.

---

## Key takeaways

1. **Everything runs in the browser.** cs50.dev gives you a professional setup with zero installation.
2. **The terminal is just typed conversation.** Command in, answer out.
3. **You already ran code today.** Twice, in two different languages' worth of tooling.
4. **The ritual beats the streak.** Watch, read, build, log: one lesson at a time.

## Common pitfalls

- ❌ Skipping setup and "just reading ahead": Lesson 5 will stop you cold. Do the capstone below first.
- ❌ Signing up for cs50.dev with an email instead of GitHub: the login **is** GitHub; create that account first.
- ❌ Trying to install C compilers or Python on your own machine now: you'll fight your operating system instead of learning. Cloud first, local in Module 12.

---

## 🛠️ Capstone Project: First Contact

> Prove your whole toolchain works, end to end, in under ten minutes. When
> something works on day zero, day one gets easier to start.

### What you will build

Nothing fancy, three verified small wins: a living codespace, a terminal that answers you, and a cat that talks. These are the exact three tools Lessons 1-5 assume.

### Milestones (build them in order, each one works on its own)

1. **Codespace alive.** Log into cs50.dev and get to the VS Code screen with a terminal.
2. **Terminal answers.** Run `echo "hello, world"` and `ls`. Read both outputs.
3. **Cat speaks.** In a new Scratch project, make the cat say something of your choosing.
4. **Ritual started.** Open `PROGRESS.md` and log today: "Day 1, setup done."
5. **Stretch goal.** In the terminal, run `code hello.txt`, type a sentence in the file that opens, save it, then run `ls` again and see your first file listed.

### How you will know you are done

- ✅ You can close the browser, reopen cs50.dev, and land back in your codespace.
- ✅ Both terminal commands produced output you can explain in one sentence.
- ✅ Your Scratch cat says your words, not the default "Hello!".

> 💡 **Keep yourself honest:** don't just do the steps: after each one, say out
> loud what happened and why. That habit is the actual skill.

---

## Cheat sheet

```text
ACCOUNTS  github.com (login for everything) · cs50.dev (code here) · scratch.mit.edu (Lesson 4)
TERMINAL  echo "text"  → prints text back        ls  → lists files here
RITUAL    watch → read → build → log (PROGRESS.md)
RULE      never just read: always build the capstone
HELP      cs50.ai: CS50's free AI "duck" tutor (log in with GitHub)
```

## How this connects to the rest of the course

- **Next, Module 1 · Lesson 1:** uses none of these tools yet (it teaches what programming *is*) but Lesson 4 (Scratch) and all of Module 2 (C, in your new codespace) depend on today's setup.
- **Later, Module 12:** you'll graduate from cs50.dev to a local setup on your own machine, with Git and hosting: the training wheels come off there.

---

*This is a self-guided setup lesson for "Self-Paced CS50x," an unofficial companion to CS50x 2026 by David J. Malan, Harvard University.*
