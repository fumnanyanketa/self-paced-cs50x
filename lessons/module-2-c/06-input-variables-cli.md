# Module 2 · Lesson 6: Input, Variables, and the Command Line

> **Course:** Self-Paced CS50x
> **Module 2:** First real programs in C: write, compile, run, and fix real code in a terminal.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 1 - C](https://www.youtube.com/watch?v=SlqjA04_dpk) · [full transcript](../../transcripts/03-lecture-1-c.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

You will look up how to use code you didn't write, capture what a user actually types with `get_string`, print it back inside a sentence using a placeholder like `%s`, and organize the growing pile of files this creates by driving the Linux command line instead of a mouse.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you build a tiny "greeter" program with `get_string` and
> `printf`, then go on a terminal scavenger hunt: making folders, moving and
> copying files, and running programs from inside subfolders. Everything
> before the Capstone teaches the skills you will use there. If you want to
> see the finish line first, jump to the **"Capstone Project"** section, then
> come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** cs50.dev, VS Code, and even C
> itself will keep changing shape over your career, but the discipline of
> "look it up in the official reference" does not.
>
> - **[The Linux man-pages project](https://man7.org/linux/man-pages/index.html)** (man7.org). This is the actual official Unix/Linux manual: the
>   real "man pages" that `manual.cs50.io` takes and rewrites in plainer
>   language for beginners. Once you outgrow the CS50 version, this is where
>   every professional programmer looks things up, on every Unix-like system,
>   forever.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Library:** code someone else already wrote that you're allowed to reuse instead of writing it yourself from scratch.
- **Header file:** a file ending in `.h` that tells the compiler "a library exists, and here's what's in it," so your program is allowed to use it.
- **Documentation (a "man page"):** the official written reference that explains exactly what a function or command does, what you feed it, and what you get back.
- **String:** a piece of text, zero or more characters, like `"David"` or `"hello world"`. Not a number.
- **Variable:** a named, labeled spot in the computer's memory where you can stash a value and use it again later.
- **Placeholder:** a stand-in symbol, like `%s`, that you put inside a string of text so `printf` can swap it out for a real value when the program actually runs.
- **Directory:** the computing word for what you'd call a "folder" on your Mac or PC.
- **Path:** the address of a file or folder: where it lives, relative to wherever you currently are.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 5 got you to `hello, world`, but that program can only ever say one fixed thing, and every new file you created just piled up loose in one folder. This lesson fixes both problems at once: you'll get a program to react to whatever a real person types, and you'll get comfortable enough with the terminal to keep your work organized the way professional programmers do, because, as Malan puts it, once you outgrow the mouse, "most every programmer tends to find themselves ultimately much more productive, much more powerful, using the keyboard more often, more quickly than, say, a traditional mouse or trackpad would allow." You'll also pick up a habit that outlasts every specific tool in this course: when you don't know how something works, you look it up.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the difference between a library and a header file, and look up any C library function using `manual.cs50.io` or the official man pages.
2. Capture a line of user-typed text with `get_string` and store the return value in a correctly typed variable.
3. Print that value back inside a sentence using the `%s` placeholder in `printf`, instead of gluing text together.
4. Navigate, create, move, copy, and delete files and folders from the Linux command line using `ls`, `mkdir`, `mv`, `cp`, `cd`, and `rm`, including the `./` and `../` shortcuts.

## Prerequisites

- **Module 2 · Lesson 5 (Hello, C):** writing `hello.c`, compiling it with `make`, running it, and reading a compiler error message. This lesson assumes you're comfortable typing a command at the `$` prompt.
- No prior command-line or terminal experience beyond that is assumed.

---

## Part 1: Look it up like a pro (documentation, libraries, and header files)

Lesson 5 had you type `#include <cs50.h>` and `#include <stdio.h>` at the top of every program without fully explaining why. Here's the why. `printf`, the function that prints to the screen, is not something you wrote, and it's not something built into the C language itself the way a keyword like `if` is. It's part of a **library**: as Malan defines it, "a library is code someone else wrote that you can use." If you forget to include it, the compiler doesn't guess what you meant: it just refuses, with an error like `call to undeclared library function 'printf'`.

So how does the compiler know a library exists? Through a **header file**, a file whose name ends in `.h` rather than `.c`. In Malan's words, "these so-called header files, which end in h, contain code that other people wrote that you can use in your own programs." Writing `#include <stdio.h>` tells the compiler, "I didn't write everything I'm about to use: please go find the definitions in this other file first."

> 🔑 **A header file doesn't contain the whole library: it's a promise that the library exists and a description of what's in it.** `stdio.h` covers "standard input/output": `printf` and its relatives. `cs50.h` covers CS50's own add-on functions, like `get_string`.

Now, how do you find out *what* to include, and how a given function actually works, before you've been taught it? You look it up. Malan describes the traditional answer: "the conventional way to look stuff up for the programming language called C is to look at the official manual pages or man pages." The catch is that most official man pages "were written decades ago... certainly written by fairly advanced programmers and not for a broad audience." That's why CS50 built its own front door onto that same material, hosted at **manual.cs50.io**: "we've essentially simplified it for those less comfortable... it's just useful to have it written in teaching-assistant-like language instead."

If you visit `manual.cs50.io/stdio.h`, you'll see the official `stdio.h` library broken down function by function. Click through to `printf`, and you'll see the standard shape every man page follows: which header file the function lives in, a short description in plain English, and example code. Malan is direct about why this matters even in an age of AI tutors: "this is the authoritative answer... all of today's AIs are trained on things like the official documentation", so the documentation isn't a fallback for when the AI duck fails you, it's the actual source the duck itself is quoting.

Alongside the standard library, CS50 also ships its own extra header file, `cs50.h`, with functions like `get_string`, `get_int`, and `get_char` that don't exist anywhere else in C. Malan is candid that these are a temporary crutch: "we use these really as training wheels for just the first few weeks of the course, and then we take these training wheels off." This lesson uses `get_string`; later lessons introduce its siblings, and Module 5 removes the training wheels entirely.

> ✅ **What to do about it:** any time you see an unfamiliar function name in this course, treat "look it up at manual.cs50.io" as step one, not a last resort.

## Part 2: Capturing what the user types (`get_string` and variables)

Last week's Scratch program used a blue "ask ... and wait" block to pause and collect typed input into a variable called `answer`. C has no `ask` function: CS50 built one and, in Malan's words, "deliberately named this function `get_string` just to make super clear what it is you are getting", namely, a **string**: "a string in programming speak means text, zero or more characters of text like H E L L O W O R L D... it's obviously not a number like 50, it's actual text that you would type on the keyboard."

Calling `get_string` alone doesn't do anything useful by itself: you have to keep the value it hands back. That's what a **variable** is for. Malan lays out the rule plainly: "if you want to keep return values around from a function, you literally use an equal sign, and then to the left of it you put the name of the variable into which you want to put that return value." Unlike Scratch, where MIT decided your input variable would always be called `answer`, in C you choose the name, but C also asks for one more thing Scratch never did: a **type**, declared right before the name, so the compiler knows what kind of value is going in that labeled memory slot.

Put together, capturing someone's name looks like this:

```c
string name = get_string("What's your name? ");
```

Reading it left to right: `string` is the type (this variable will hold text), `name` is the name you chose, `=` means "store whatever comes back on the right into the thing on the left," and `get_string("What's your name? ")` prints the prompt in the parentheses, waits for the user to type, and hands back what they typed. Notice `get_string` is quietly doing its own `printf` for you: that's why you never see a separate `printf` for the question itself.

> 🔑 **The equal sign in code means "copy the value on the right into the variable on the left," not "these two things are equal."** That distinction matters more once conditionals arrive next lesson.

## Part 3: Printing it back nicely (the `%s` placeholder)

The intuitive-but-wrong next move is to try to print the greeting and the name as if they were one glued-together phrase. Malan does exactly this on purpose, writing `printf("hello answer\n");`, and the program prints the literal word `answer`, because that's what you told it to print: a string in quotes is just text, not a reference to a variable. As he puts it while diagnosing the bug, "the computer's just doing literally what I told it to do."

C doesn't let you join a fixed phrase and a variable's value inside the quotes directly. Instead, you leave a **placeholder** where the value should go, then tell `printf` separately what to plug in there: "percent S is the placeholder for a string that you don't know when you're writing the code, but when someone else is running the code, it will be filled in and substituted for their input." The corrected line looks like this:

```c
printf("hello, %s\n", name);
```

The comma is the key piece of new grammar here. The comma *inside* the quotes is just ordinary English punctuation. The comma *outside* the quotes is meaningful to C: it separates the first input to `printf` (the phrase with the placeholder in it) from the second input (the variable whose value should replace that placeholder). When a student pointed out that the first input, the fixed question or phrase, doesn't feel like "input" the way typed text does, Malan agreed but held the line on the terminology: "these are both inputs because they're being provided as inputs to the function... the origins of those inputs though are entirely up to what I'm trying to achieve."

> ✅ **What to do about it:** whenever you want to print a mix of fixed text and a variable's value, reach for a placeholder (`%s` for a string) and a comma-separated second argument, never string concatenation, which C's `printf` doesn't support this way.

## Part 4: Leaving the mouse behind (the Linux command line)

Under the hood, cs50.dev is running **Linux**, the operating system most servers and most professional developer tools use. Every file you've created so far (`hello.c`, the compiled `hello` program) lives in a folder (a **directory**) on that machine, and so far you've only seen it appear in the File Explorer sidebar. Malan now shows the alternative: doing every one of those same things by typing, at the `$` prompt, rather than clicking.

Here is the core toolkit, in Malan's own words, one command per everyday action:

| Command | What it does |
|---|---|
| `ls` | "if I want to list the files in my current folder, I can type LS" |
| `mkdir <name>` | "if I want to create a new folder, otherwise known as a directory, I can use MKDIR to make a directory" |
| `mv <from> <to>` | "if I want to rename a file, I can use MV for move" (also moves a file into a folder) |
| `cp <from> <to>` | "if I want to copy a file, CP" |
| `cd <folder>` | "if I want to change directories, change into a folder, I can use CD" |
| `rm <file>` | "if I want to remove a file, I can use RM" |
| `rmdir <folder>` | "if I want to remove a directory, I can use RM directory" |

A few of these deserve a second look because the syntax is easy to misread the first time:

- **`mv` takes two arguments, not one.** Where `code hello.c` and `make hello` only ever took a single word after the command, `mv hello.c hello/` takes an *origin* first and a *destination* second: "the way the move command is designed is to expect the origin as the first word and the destination as the second." That same command also doubles as "rename": `mv` a file to a new filename in the same folder, and it's renamed, not moved.
- **`./` means "right here."** To run a program you just compiled, you type `./hello` rather than just `hello`. As Malan explains, "what the slash means is that after having just made a program called hello, that program's going to end up in my current folder... when I say slash, that's like saying go into the current folder and run the program therein called hello specifically."
- **`../` means "one level up."** Once your programs live inside subfolders, you'll need to climb back out of them. "A single dot, which we have seen before, means this folder, two dots means one step up. There's no triple dots or quadruple dots." Those two are the only shortcuts of their kind.

> 💡 **If you ever get lost, `cd` with no folder name at all takes you straight home.** Malan: "if you ever get yourself into a confusing mess, just type CD enter alone and you'll be magically whisked away to your default folder."

Putting all four parts together is the whole story of this lesson: you look up how a function works in the documentation (Part 1), you use it to capture text from a real person into a variable (Part 2), you print that text back inside a sentence using a placeholder (Part 3), and once you're writing more than one or two programs, you use the command line (Part 4) to keep them from turning, in Malan's phrase, into "a hot mess of files inside of this one main folder."

```text
manual.cs50.io  --tells you-->  get_string() exists in cs50.h
        |
        v
string name = get_string("What's your name? ");   <- captures input into a variable
        |
        v
printf("hello, %s\n", name);                        <- prints it back with a placeholder
        |
        v
mkdir greeter && mv greeter.c greeter/ && cd greeter/  <- keeps the resulting files organized
```

---

## Key takeaways

1. **Documentation isn't optional: it's the actual source of truth.** `manual.cs50.io` and the official man pages tell you what a library function expects and returns; even AI tutors are trained on this same material.
2. **A library needs a header file to be usable, and `get_string` comes from CS50's own `cs50.h`.** No `#include <cs50.h>`, no `get_string`.
3. **`=` stores a value in a variable; it does not test for equality.** `string name = get_string(...)` copies the returned string into `name`.
4. **`printf` can't glue text and a variable together directly: use a placeholder (`%s`) plus a comma-separated argument.**
5. **The command line does everything the File Explorer does, just typed.** `ls`, `mkdir`, `mv`, `cp`, `cd`, `rm`, `./`, and `../` are enough to organize an entire term's worth of programs.

## Common pitfalls

- ❌ Using `get_string` without `#include <cs50.h>`: you'll see `call to undeclared function 'get_string'`. Fix it by adding the include, not by rewriting the rest of your code.
- ❌ Writing `printf("hello, name\n");` and expecting it to print the variable's value: in quotes, `name` is just the four letters n-a-m-e. Use `printf("hello, %s\n", name);` instead.
- ❌ Forgetting the `./` when running a program you just compiled: typing `hello` instead of `./hello` in a shell that doesn't search the current folder by default will fail or run something unintended.
- ❌ Running `mv` with only one argument, or in the wrong order: remember origin first, destination second. `mv hello.c hello/` moves the file; `mv hello.c hello/` with `hello.c` and `hello/` swapped is not the same command.
- ❌ Typing `rm` on the wrong file without a backup: there's no undo, no recycle bin. If you're not sure, `cp` a backup copy first.

---

## 🛠️ Capstone Project: Greeter + Terminal Scavenger Hunt

> This is the main hands-on project for the lesson. You'll write a program
> that actually reacts to a real person, then prove you can keep it (and its
> future siblings) organized entirely from the keyboard, the same command
> line that, later in this course, will drive every server you ever deploy.

### What you will build

A tiny interactive program called `greeter.c` that asks for someone's name and greets them back by name, plus a small folder structure you build, rearrange, and clean up entirely with Linux commands. The pieces:

- `greeter.c`: uses `get_string` to capture a name and `printf` with `%s` to print a personalized greeting.
- A `greeter/` folder, created, populated, and navigated using `mkdir`, `mv`, `cd`, `./`, and `../`.
- A backup-and-cleanup pass using `cp` and `rm`, so you've touched every command in the toolkit at least once.

### Why this is the perfect practice

| Lesson idea | Where you use it in the project |
|---|---|
| Documentation (Part 1) | Look up `get_string`'s prototype at `manual.cs50.io` before you write a line of code. |
| `get_string` + variables (Part 2) | Capture the user's name into a `string` variable in `greeter.c`. |
| `printf` placeholder (Part 3) | Print `"hello, %s!\n"` with the name substituted in. |
| Linux CLI (Part 4) | Create `greeter/`, move your files into it, run the program from inside it, then reorganize and clean up. |

### Milestones (build them in order, each one works on its own)

1. **Look it up.** Visit `manual.cs50.io`, find the `cs50.h` page, and read the entry for `get_string`. Note its return type (`string`) and what it prints for you automatically.
2. **Write the greeter.** In your terminal, run `code greeter.c` and write a program that includes `cs50.h` and `stdio.h`, captures a name with `get_string("What's your name? ")` into a variable, and prints `hello, <name>!` using a `%s` placeholder.
3. **Compile and run it.** `make greeter` then `./greeter`. Type your own name and confirm the greeting is personalized, not the literal word "name".
4. **Start the scavenger hunt.** Run `mkdir greeter_files`, then `mv greeter.c greeter_files/` and `mv greeter greeter_files/` (or just `greeter.c` if you'd rather recompile inside the folder). Confirm with `ls` that your main folder is now tidy.
5. **Work from inside the folder.** `cd greeter_files`, run `ls` to confirm your files are there, then run `./greeter` from inside this new location.
6. **Back up, rename, clean up, and climb back out.** Inside `greeter_files`, `cp greeter.c backup.c` to make a spare copy, `mv greeter.c greeter_v1.c` to rename the original, then delete the backup with `rm backup.c`. Finally, use `mv greeter_v1.c ../` to send the renamed file back up to the parent folder, then `cd ..` (or `cd` alone) to follow it there and confirm with `ls`.
7. **Stretch goals.** Look up `get_int` at `manual.cs50.io` and add a second question to `greeter.c` (for example, asking for a lucky number and printing it back with `%i`). Or build a `psets/` folder containing a `pset1/` folder inside it, and move a program two levels deep, running it the whole way with the correct `./` and `../` paths.

### How you will know you are done

- ✅ `./greeter` (or `./greeter` from inside `greeter_files`) prints a greeting containing the actual name you typed, not the word "name" or "answer".
- ✅ You can explain, in one sentence each, what `mkdir`, `mv`, `cp`, `cd`, `rm`, `./`, and `../` each did in your scavenger hunt.
- ✅ Your main folder is not cluttered with a backup file you no longer need: you deleted it with `rm` on purpose, not by accident.

> 💡 **Keep yourself honest:** after every command, run `ls` and actually read
> the output before typing the next command. That's the whole muscle you're
> building today.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Read a man page cold (foundational)
Visit `manual.cs50.io`, find the entry for `get_int` (not `get_string`), and write down, in your own words: what type of value it returns, and one example situation where you'd use it instead of `get_string`.

### Exercise 2: Two placeholders, one sentence (intermediate)
Modify `greeter.c` to ask for both a first name and a favorite color with two separate `get_string` calls, then print a single sentence using two `%s` placeholders in one `printf` call, such as `"%s's favorite color is %s!\n"`.

### Exercise 3: Three folders deep (advanced)
Starting from your home folder, use `mkdir` three separate times to build `week1/`, then `week1/programs/`, then `week1/programs/greetings/` (you'll need to `cd` into each new folder before making the next one, since there's no shortcut for making all three at once yet). Move a copy of `greeter.c` all the way down into the deepest folder, compile it there, and run it using `./greeter`. Then navigate back to your starting folder using only `cd ..` three times, not `cd` alone, and confirm you're back with `ls`.

---

## Cheat sheet

```text
DOCS       manual.cs50.io  -- CS50's plain-language rewrite of the official man pages
           man7.org        -- the real, original Unix/Linux man pages
LIBRARY    code someone else wrote (e.g. printf's home, the C standard library)
HEADER     a .h file that tells the compiler a library exists (#include <cs50.h>, <stdio.h>)

CAPTURE INPUT     string name = get_string("What's your name? ");
PRINT IT BACK     printf("hello, %s\n", name);
PLACEHOLDERS      %s string   %i integer   %c char   %f float   %li long

LINUX CLI
  ls              list files in the current folder
  mkdir <name>    create a new folder
  mv <a> <b>      move OR rename a file/folder (origin first, destination second)
  cp <a> <b>      copy a file
  cd <folder>     change into a folder      cd .. -> go up one level     cd -> go home
  rm <file>       delete a file (no undo!)  rmdir <folder> -> delete an empty folder
  ./program       run a program in the CURRENT folder
  ..              the parent (one level up) folder; there is no "..." or beyond
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 5 (Hello, C):** you learned to write, compile with `make`, and run a single fixed program, and to read a compiler error. This lesson makes that program dynamic and gives you a way to keep the growing pile of programs organized.
- **Next, Module 2 · Lesson 7 (Conditionals and loops):** you'll use the values you now know how to capture and print, like the number from `get_int`, to make programs branch and repeat, turning `greeter.c`-style programs into real decision-makers.
- **Later, Module 5 (Memory):** CS50's `get_string` and friends are, in Malan's own words, "training wheels": that module removes them and shows you how to capture input using only standard C, once you understand pointers and memory well enough not to need the crutch.

---

*Source: "CS50x 2026 - Lecture 1 - C" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
