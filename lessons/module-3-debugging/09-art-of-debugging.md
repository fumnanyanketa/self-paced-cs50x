# Module 3 · Lesson 9: The Art of Debugging

> **Course:** Self-Paced CS50x
> **Module 3:** Debugging and what the compiler hides: debug systematically and see how C really stores data
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 2 - Arrays](https://www.youtube.com/watch?v=h5Gc1n8ZuU8) · [full transcript](../../transcripts/04-lecture-2-arrays.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Every programmer writes bugs constantly. What separates a frustrated beginner from a productive programmer is a repeatable process for finding them: read what the compiler is actually telling you, ask `printf` to show you what your variables really contain, step through your code one line at a time with a debugger, and explain your reasoning out loud before you let anyone, human or AI, fix it for you.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *The Bug Hunt*, where you take a deliberately broken 15-line C program and hunt down three separate bugs using three separate techniques. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Debuggers and AI chat windows will keep changing, but the discipline of debugging is old and tool-agnostic. For the timeless account of one of the techniques in this lesson:
>
> - **[*The Pragmatic Programmer: From Journeyman to Master*](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer) by Andrew Hunt and David Thomas (1999).** This book is widely credited with popularizing "rubber duck debugging": explaining your code line by line to an inanimate object until the bug reveals itself in your own words. The tool in front of you changes (a real duck, a plush duck, CS50's AI duck); the underlying idea, that articulating your reasoning out loud surfaces your own faulty assumptions, does not.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Bug:** any mistake in a program that makes it fail to compile, crash, or produce the wrong result.
- **Syntax error:** a mistake in the grammar of the language itself (a missing semicolon, a misspelled keyword). The compiler cannot even finish translating your code, so the program never gets built.
- **Logical error (also called a runtime bug):** a mistake in your reasoning, not your grammar. The code compiles and runs fine. It just does the wrong thing.
- **Compiler:** the program (called `clang` under the hood, automated for you by `make`) that translates the C you write into instructions the computer can run. It checks your grammar; it has no idea what you meant to accomplish.
- **Header file:** a file like `stdio.h` or `cs50.h` that tells the compiler "these functions exist, and here is what they look like," so you can use functions like `printf` or `get_string` that were written elsewhere.
- **Debugger:** a program (CS50 automates it for you as `debug50`) that lets you pause your program mid-execution and step through it one line at a time, inspecting variables as you go.
- **Breakpoint:** a marker you place on a specific line telling the debugger "pause execution right here."
- **Rubber duck debugging:** explaining your code and your confusion out loud, one line at a time, to an object (or an AI) that cannot answer back, often enough on its own to reveal the bug.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In Module 2 · Lesson 8 ("Functions, code quality, and the limits of numbers") you learned to package logic into functions with prototypes and well-defined inputs and outputs. The moment you write more than a couple of lines of C, though, some of them will be wrong: that is not a personal failing, it is the normal condition of programming. As Malan puts it plainly:

> "The compiler has no idea what you are trying to achieve logically. It only knows about the language C itself and the requisite syntax for actually writing and compiling code." (David Malan)

That sentence is the whole reason this lesson exists. The compiler will catch your grammar mistakes and refuse to build broken code, but it will happily compile and run code that does the *wrong thing* without complaint. You need your own systematic techniques for that gap, and debugging turns out to be one of the single most-used skills in any real software project, including the database-backed web app you'll design and ship as this course's final project.

## Learning objectives

By the end of this lesson you will be able to:

1. Distinguish a syntax error (stops compilation) from a logical error (compiles, runs, but misbehaves), and explain why the compiler only catches the first kind.
2. Read a `clang` compiler error message (file name, line number, and description) and use it to locate and fix the actual mistake.
3. Insert temporary `printf` tracing statements to reveal what a variable actually contains during execution, then remove them once the bug is found.
4. Set a breakpoint in `debug50`, and use "step over" and "step into" to walk through a program line by line while reading its variables pane and call stack.
5. Explain rubber-duck debugging and apply Malan's guidance on using an AI duck (like CS50.ai) as a last resort, not a first one.

## Prerequisites

- **Module 2 · Lesson 8: Functions, code quality, and the limits of numbers**: you should be comfortable writing a function, calling it, and writing its prototype above `main`, since the debugger walkthrough steps into a helper function.
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**): you'll compile and run real C code in the Capstone.

---

## Part 1: Two kinds of mistakes, and where the word "bug" came from

Before the debugging techniques, a bit of history. The term "bug" for a computer mistake is usually credited to Grace Hopper, a rear admiral in the U.S. Navy and one of the original programmers of the Harvard Mark I. Malan tells the story of the Harvard Mark II logbook:

> "They have found a problem with the computer this one day whereby there was literally a bug, a moth inside of the circuitry of the computer, and as was written here, 'first actual case of bug being found.'" (David Malan)

Ever since, "bug" and "debugging" describe the process of finding and removing mistakes in code, even though, as Malan notes, most of your bugs from here on will have nothing to do with actual insects.

Malan then deliberately writes a broken program, `buggy.c`, in front of the class, making the exact mistakes beginners tend to make. Here is what happened, bug by bug:

| # | What Malan typed (the bug) | What the compiler said | The fix |
|---|---|---|---|
| 1 | `printf("hello, world");` with no `#include <stdio.h>` at the top | `call to undeclared library function 'printf'` | Add `#include <stdio.h>`: that's the file where `printf`'s prototype lives. |
| 2 | Left the semicolon off the end of the `printf` line | `expected ';' after expression`, pointing at that exact line | Add the missing `;`. |
| 3 | Typed `#include <studio.h>` (a very common typo: an annual FAQ, in Malan's words) | The same "undeclared function" error, because no file called `studio.h` exists | Fix the spelling: `stdio.h`. |
| 4 | Wrote `name = get_string("What's your name? ");` without declaring a type first | `use of undeclared identifier 'name'` | Declare it with a type: `string name = get_string(...);`. |
| 5 | Used the word `string` without `#include <cs50.h>` | `use of undeclared identifier 'string'`, with a red-herring suggestion, "did you mean 'stdin'?" | Add `#include <cs50.h>`. That header is where CS50's training-wheels `string` type and `get_string` both live. `string` is not a real C keyword, only a CS50 convenience. |
| 6 | `printf("hello, world\n");` even though a `name` variable now existed | **No error at all.** It compiles and runs. | Add the placeholder and the variable: `printf("hello, %s\n", name);` |

Bugs 1 through 5 are **syntax errors**: mistakes in the grammar of C itself. The compiler refuses to finish translating the code until every one of them is fixed. You cannot even produce a runnable program. Bug 6 is different in kind: the program compiles cleanly and runs without complaint, it just doesn't say what you meant it to say. That is a **logical error**, and it is the harder of the two problems, because there is no red error message pointing you to the line.

> 🔑 **The single most important takeaway of this part.** Syntax errors are a conversation with the compiler about grammar: read the file name and line number it gives you, and fix exactly what it names. Logical errors are a conversation with yourself about intent, and the compiler cannot have that conversation for you.

---

## Part 2: When the code runs but lies to you: printf as a debugging tool

Logical errors need a different technique, because there's no error message to read. Malan's first tool for this: use `printf`, the very function you already know for printing output, to print out what your program is *actually doing* while it runs, temporarily, then delete those lines once you understand the bug.

> "So let's use printF as a debugging tool in that sense." (David Malan)

He demonstrates with a small program meant to print a stack of 3 bricks (like the ones Mario jumps over):

```c
for (int i = 0; i <= 3; i++)
{
    printf("#\n");
}
```

Running it prints **4** bricks, not 3. The loop is clearly the suspect, so instead of guessing, Malan adds a temporary trace line to see the loop variable's actual value on every pass:

```c
for (int i = 0; i <= 3; i++)
{
    printf("i is %i\n", i);   // temporary, delete once the bug is found
    printf("#\n");
}
```

The trace shows the loop running for `i` = 0, 1, 2, *and* 3: four iterations, not three. Once the values are visible, the mistake is obvious:

> "The solution of course is that I shouldn't be starting at 0 and iterating less than or equal to 3." (David Malan)

The fix is to change `i <= 3` to `i < 3` (or start at 1 and use `i <= 3`, but counting from 0 with a strict `<` is the idiomatic C style). This exact mistake, a loop that runs one time too many or too few, is common enough to have its own name: an **off-by-one error**.

> ✅ **What to do about it:** when a program compiles and runs but produces a suspicious number, print the value of the variable driving the suspicious behavior (usually a loop counter) at the point where you think the logic breaks down. Once you understand why the number is wrong, delete the temporary `printf` and fix the real line.

Malan also shows that this scales badly: once he moves the loop into its own function (`print_column`), there is more code to sprinkle with `printf` calls, and adding, recompiling, and removing trace statements over and over gets "very tedious quickly." That tedium is exactly what the next tool solves.

---

## Part 3: Stepping through time: the debug50 debugger

Rather than manually printing variable values and recompiling again and again, you can use a **debugger**: a program that pauses your code mid-run and lets you inspect it, one line at a time, without touching your source file. CS50 wraps the industry-standard debugger inside VS Code as a single command, `debug50`, but as Malan is careful to point out:

> "A debugger is a piece of software that is used in the real world that literally lets you do that: debug your code by letting you slow down or even pause execution and walk through execution of your code line by line." (David Malan)

To use it, you first need to tell the debugger where to pause: click just to the left of a line number in VS Code to set a **breakpoint** (a small red dot appears).

> "A break point is where your code will break, the point at which it will break." (David Malan)

Malan sets a breakpoint on the first line inside `main` and runs `debug50 buggy` from the terminal. Execution pauses before that line has even run. At this point the debugger's side panel shows two things worth knowing about:

- **Variables**: the current value of every variable in scope. Before a variable is ever assigned, it can show a **garbage value**: a leftover pattern of bits from whatever the computer's memory was used for previously. It is not a bug in your code: it is just uninitialized memory, and Malan flags that we'll come back to exactly what that means (and why it matters for security) in Module 5, when Valgrind enters the picture.
- **Call stack**: which function you're currently paused inside, and which function called it.

From here, two buttons matter most:

| Button | What it does | When to use it |
|---|---|---|
| **Step over** | "Step over this line and execute it, but only one line at a time" (Malan's words): runs the current line, including any function it calls, without pausing inside that function. | You trust the function being called and just want to see its result. |
| **Step into** | Jumps *inside* the function being called on the current line, so you can watch it execute line by line too. | You suspect the bug is inside that function, as Malan demonstrates: "Let me step into line 9 and walk through the print column function itself line by line." |

Stepping into `print_column` with the height set to 3, Malan watches the loop variable go from its garbage starting value to 0, then 1, then 2 (a hash mark printed on each pass), and finally to 3, where a fourth hash mark appears. The debugger doesn't name the bug for him; it just lets him watch the state change one step at a time until the mistake, the same `<=` off-by-one from Part 2, becomes visible with his own eyes.

> 🔑 **The single most important takeaway of this part.** A debugger doesn't find bugs for you: it removes the guesswork of "what is my program doing right now" so that your own reasoning has something reliable to work with. Step over what you trust; step into what you suspect.

---

## Part 4: Ask the duck before you ask a human (or an AI)

Sometimes printf tracing and debug50 stepping aren't the block. The block is your own thinking, and you don't have a teaching assistant nearby to talk it through with. That's the point of **rubber duck debugging**: explain your code and your confusion out loud, one line at a time, to something that cannot answer back. Often, hearing yourself describe the logic reveals the flawed assumption before you finish the sentence.

CS50 hands out hundreds of physical rubber ducks for exactly this reason, and also offers a virtual version: the AI-powered duck at CS50.ai, embedded directly into VS Code at cs50.dev. But Malan is explicit that the AI duck is not a replacement for doing the reasoning yourself:

> "It's less reasonable to say: copy paste your code into the duck and say, 'what's wrong with my code?' You should really be meeting the AI halfway." (David Malan)

> "After all, what's the point of actually doing this, or any other class, is to develop that muscle memory, develop those mental models, get some practical skills." (David Malan)

In other words: asking "what does this specific error message mean?" is a reasonable use of the AI duck. Pasting your whole file and asking it to diagnose and fix the problem for you skips the exact mental exercise the assignment exists to build.

Put together, the four techniques from this lesson form one workflow you can run on any bug:

```text
Won't compile?              -> Read the compiler's file name, line number, and message first.
Compiles, wrong output?     -> Add a temporary printf to show what a variable ACTUALLY is.
Still don't understand it?  -> debug50: set a breakpoint, step over what you trust,
                                step into what you suspect, watch the Variables pane.
Still stuck?                -> Explain the bug out loud, line by line, to a duck
                                (physical or CS50.ai), narrate your OWN reasoning first.
```

> ❌ **The trap:** treating the AI duck as step one instead of step four. Try reading the error, tracing with printf, and stepping with debug50 before you ask anything (human or AI) to look at your whole file.

---

## Key takeaways

1. **Syntax errors vs. logical errors.** Syntax errors stop compilation and the compiler tells you exactly where; logical errors compile and run fine while doing the wrong thing, and only your own reasoning (aided by tools) can catch them.
2. **printf tracing is temporary.** Print a variable's real value to understand a bug, then delete the trace line once you've fixed it: it isn't part of your finished program.
3. **debug50 gives you time, not answers.** Breakpoints tell it where to pause; step over trusts a function's result, step into walks through that function's own lines; the Variables pane and call stack show you the truth of the running program.
4. **Meet the AI duck halfway.** Ask it to explain an error message; don't hand it your whole file and ask it to diagnose and fix the bug for you.
5. **"Bug" predates software.** Grace Hopper's Harvard Mark II logbook entry about an actual moth is why we still say "debugging" today.

## Common pitfalls

- ❌ Reading only the first compiler error and panicking at the "whole bunch of scary looking messages": fix the *first* error and recompile; later errors are often just consequences of the first one.
- ❌ Submitting code with leftover debugging `printf` statements still in it: remove them once the bug is understood.
- ❌ Clicking "step over" when the bug is actually inside the function being called. You'll never see the faulty line execute. Step into when you suspect the helper function itself.
- ❌ Pasting an entire file into CS50.ai and asking "what's wrong with my code?" instead of narrating your own reasoning first, or asking a narrower question like "what does this error mean?"
- ❌ Assuming a strange starting value in the debugger's Variables pane is itself a bug: an uninitialized variable's garbage value is expected until the line that assigns it actually runs.

---

## 🛠️ Capstone Project: The Bug Hunt

> This is the main hands-on project for the lesson. You'll take one small, deliberately broken C program with three separate bugs and clear every one of them using the three techniques from this lesson, proving to yourself that each technique actually works, not just watching Malan use it.

### What you will build

A working `debug_me.c` on cs50.dev: a program that asks for a wall's height and prints that many brick rows, then reports how many bricks it placed. As given to you, it has three planted bugs:

1. **A syntax error**: the program won't even compile yet.
2. **An off-by-one error**: once it compiles, it prints one too many brick rows.
3. **A logic error**: the row count is right, but the reported total is wrong.

Here is the broken listing. Copy it into `debug_me.c` exactly as shown:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n = get_int("Height: ")
    int total = 0;

    for (int i = 0; i <= n; i++)
    {
        printf("#\n");
        total = total + n;
    }
    printf("Bricks placed: %i\n", total);
}
```

### Why this is the perfect practice

| Lesson idea | Where you use it in The Bug Hunt |
|---|---|
| Reading a compiler error message (Part 1) | Bug 1 (the missing semicolon) won't let the program compile at all. |
| printf tracing (Part 2) | Bug 2 (the off-by-one loop) is easiest to catch by tracing `i` each iteration. |
| debug50 breakpoints and stepping (Part 3) | Bug 3 (the miscounted total) is easiest to catch by watching `total` change in the Variables pane across iterations. |
| Rubber duck reasoning (Part 4) | Narrating each bug out loud before checking your fix, and using CS50.ai narrowly if you get stuck. |

### Milestones (build them in order, each one works on its own)

1. **Set up and hit the wall.** Create `debug_me.c` on cs50.dev with the listing above and run `make debug_me`. You should get a compiler error. Don't fix anything yet, just read it.
2. **Bug 1: fix it by reading the error.** Note the file name and line number `clang` reports, and what it says is missing. Fix only that (add the missing `;` after `get_int("Height: ")`), then re-run `make debug_me` until it builds cleanly.
3. **Bug 2: fix it with printf tracing.** Run `./debug_me` with a height of 3; you'll get 4 rows instead of 3. Add a temporary `printf("i is %i\n", i);` inside the loop, recompile, and run again to see the actual values of `i`. Once you see the extra iteration, fix the loop condition, then delete your temporary trace line.
4. **Bug 3: fix it with debug50.** Run `debug50 ./debug_me`, set a breakpoint on the `for` loop line, and step over each line of the loop while watching `total` in the Variables pane. Once you see it growing by `n` instead of by `1` each pass, fix the line that updates `total`.
5. **Cross-check with the other techniques (stretch).** Go back and re-find bug 2 using debug50 instead of printf, and re-find bug 3 using a temporary printf trace instead of the debugger. This proves each technique is general-purpose, not tied to one bug's shape.
6. **Rubber-duck it (stretch).** Before checking any single fix against the answer above, explain out loud (or type to CS50.ai as a narrow question, not "fix this for me") what you expect each line to do and why you think it's wrong.

### How you will know you are done

- ✅ `make debug_me` compiles with no errors or warnings.
- ✅ Running `./debug_me` with height 3 prints exactly 3 rows of `#` and reports `Bricks placed: 3`.
- ✅ You used `debug50` at least once with a breakpoint and both a step-over and a step-into.
- ✅ You can say out loud, for each of the three bugs, which technique caught it and why that technique was the right tool for that particular symptom.

> 💡 **Keep yourself honest:** don't peek at "the fix" for a bug before you've actually reproduced its symptom (the compiler error, the wrong row count, or the wrong total) yourself first. The value of this capstone is in the diagnosis, not the one-line patch.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Break it on purpose (foundational)
Take any working "hello, world" program you've already written. One at a time, introduce each of the six mistakes from Malan's `buggy.c` walkthrough in Part 1 (missing header, missing semicolon, misspelled header, undeclared variable, missing `cs50.h`, missing format placeholder). After each one, run `make` and read the exact error message before fixing it and moving to the next.

### Exercise 2: Trace a mystery loop (intermediate)
Write a `for` loop that is supposed to print the numbers 1 through 5 but deliberately gets the bounds wrong (for example, `for (int i = 1; i <= 6; i++)`). Without looking at the loop's declaration, add a temporary `printf` inside it to trace `i`, use only that output to figure out exactly what's wrong, then fix the bounds and delete the trace line.

### Exercise 3: Step into a helper function (advanced)
Write a small program with a `main` function that calls a helper function (for example, a function that squares a number but has a typo that makes it add instead of multiply). Use `debug50`, set your breakpoint at `main`, step over until you reach the call to your helper, then step into it and watch the Variables pane to catch the mistake. Rubber-duck what you expect to see out loud before each step.

---

## Cheat sheet

```text
SYNTAX ERROR              -> Compiler refuses to build. Read: file, line, message. Fix exactly that.
LOGICAL ERROR              -> Compiles and runs, wrong result. No error message to read.

printf DEBUGGING
  - Add a temporary printf to show a variable's REAL value, not what you assume it is.
  - Best for: loop counters, off-by-one errors.
  - Always delete the trace line once the bug is found.

debug50 DEBUGGING
  debug50 <program>          start the debugger (set >=1 breakpoint first, click left of a line number)
  Step over                  run this line (and anything it calls) without pausing inside it
  Step into                  jump inside the function this line calls, and pause there too
  Variables pane              current value of every in-scope variable (garbage value = not yet assigned)
  Call stack                  which function you're paused in, and who called it

RUBBER DUCK DEBUGGING
  - Explain your code out loud, line by line, before asking anyone (or any AI) for help.
  - CS50.ai / cs50.dev duck: OK to ask "what does this error mean?"
                             NOT ok to paste your file and ask "what's wrong with my code?"

WORKFLOW
  Won't compile      -> read the error
  Wrong output        -> printf trace
  Still confused      -> debug50 (step over / step into)
  Still stuck          -> rubber duck (physical or AI), narrate your own reasoning first
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 8:** functions, prototypes, and scope gave you the code structure (like `print_column`) that this lesson's debug50 walkthrough steps into.
- **Next, Module 3 · Lesson 10:** "From source code to machine code" pulls back the curtain on what `make` actually does in four stages (preprocess, compile, assemble, link): the same `buggy.c` and `hello.c` programs you debugged here.
- **Later, Module 5:** Valgrind adds a fourth kind of bug to your toolkit, memory bugs (leaks and invalid reads/writes), building directly on the "garbage value" idea introduced here in the debugger's Variables pane.

---

*Source: "CS50x 2026 - Lecture 2 - Arrays" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
