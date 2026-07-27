# Module 1 · Lesson 3: Your First Algorithms: Search and Pseudocode

> **Course:** Self-Paced CS50x
> **Module 1:** Computational thinking: learn to think in inputs, outputs, and algorithms before any syntax
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 0 - Scratch](https://www.youtube.com/watch?v=UuIEbpQms8o) · [full transcript](../../transcripts/02-lecture-0-scratch.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

An algorithm is just a step-by-step recipe for solving a problem, and the same problem, finding a name in a phone book, can be solved by a slow recipe or a dramatically faster one, which is why computer scientists write that recipe down first as plain-English pseudocode, built from just four ingredients: functions, conditionals, Boolean expressions, and loops.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you physically search a real, sorted list two different ways, count your steps, and then write down the faster method as pseudocode. Everything before the Capstone teaches the ideas you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk is recent, but the underlying idea (that "obviously correct" algorithms can still hide subtle bugs) is not. For the timeless, tool-agnostic version:
>
> - **[Extra, Extra, Read All About It: Nearly All Binary Searches and Mergesorts are Broken](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/)** (Joshua Bloch, Google Research Blog, 2006). Binary search, the "jump to the middle" trick you'll practice in this lesson, is one of the oldest, simplest-sounding algorithms in computer science, and yet Bloch shows that a bug hid inside nearly every published implementation of it (including Java's own standard library) for decades. It is the best evidence you'll find that writing precise pseudocode, and thinking hard about corner cases, matters even when an idea feels obvious.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Algorithm:** a step-by-step recipe for solving a problem: instructions precise enough that anyone (or anything) following them gets the right answer every time.
- **Pseudocode:** a rough, plain-English sketch of an algorithm's steps, written before you worry about any particular programming language's exact rules or punctuation.
- **Linear search:** looking for something by checking items one at a time, in order, until you find it (or run out of items).
- **Binary search:** looking for something in a *sorted* list by repeatedly jumping to the middle and throwing away the half that can't contain what you want.
- **Boolean expression:** a question your code asks that can only be answered "yes" or "no" (true or false), named after the mathematician George Boole.
- **Loop:** an instruction that repeats a set of steps again and again, usually until some condition changes.
- **Compiler:** a program that translates human-friendly code (like C) into the 0s and 1s (machine code) that a computer's processor can actually run.
- **Abstraction:** hiding the complicated details of how something works so you (or anyone else) can use it, or build on top of it, without needing to understand every layer underneath.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In Lesson 2 you learned that a computer only ever sees patterns of 0s and 1s: that's the *representation* half of computer science. This lesson is about the other half: *processing* that information to solve a problem, and doing it well. Malan puts it plainly:

> "What computer science and what algorithms and about good design is about is figuring out what is the logic via which you can solve problems not only correctly but efficiently as well."

That distinction, correct versus efficient, is the whole lesson in one line. You already know how to solve "find a name in a phone book" correctly (just look at every page). The interesting question, and the one real software has to answer millions of times a second, is how to solve it *fast*. And before you can write that fast solution in any programming language, you need a language-independent way to write it down: pseudocode, built from four small, reusable ingredients.

## Learning objectives

By the end of this lesson you will be able to:

1. Compare linear search and binary search, and explain, using the size-vs-time graph, why one gets dramatically faster than the other as the problem grows.
2. Predict, for a sorted list of a given size, roughly how many "cuts" binary search needs, and explain why doubling the list barely changes that number.
3. Read and write short pseudocode using the four building blocks (functions, conditionals, Boolean expressions, and loops), including a clearly handled "not found" case.
4. Explain, in plain language, how machine code, compilers, and abstraction let you write instructions a computer can act on without ever having to think in 0s and 1s yourself.

## Prerequisites

- **Module 1 · Lesson 2 (bits and binary).** This lesson assumes you're comfortable with the idea that computers represent everything (numbers, letters, and, as you'll see below, even the instructions themselves) as patterns of 0s and 1s.
- No coding tools needed yet. You'll write pseudocode by hand or in a plain text file; Lesson 4 introduces Scratch, your first real programming environment.

---

## Part 1: Linear search vs. binary search

Malan frames the whole idea of an algorithm around a problem you've solved a hundred times: finding a contact.

> "Step by step instructions for solving some problem."

That's his definition of **algorithm**, and the example he uses is a giant, physical, alphabetized phone book (the old paper kind, with a name and a number on every page) standing in for your phone's contacts list. The goal: find "John Harvard."

There are (at least) three ways to do it:

**1. Check every page, front to back.** Start at page one and keep turning pages until you find the name. It works. It is also, in Malan's words:

> "It's just slow. I mean this is crazy slow."

If John Harvard happens to be near the end of a 1,000-page book, you might turn nearly all 1,000 pages. This is **linear search**: checking items one at a time, in order.

**2. Check every second page.** Skip through the book two pages at a time, which is roughly twice as fast. But now you can overshoot and skip right past the name you want, so you need an extra rule ("if I've gone past it, double back one page") to fix the mistake. It's a real improvement, but it's still fundamentally the same *kind* of algorithm: still linear, just with a smaller multiplier.

**3. Jump to the middle, then the middle of what's left.** Open the book to the middle. The name you want is alphabetically before or after that page, so:

> "We can tear the problem in half."

Whichever half remains, jump to *its* middle, and repeat. This is **binary search** (from "binary," meaning two: you're always splitting the remaining problem into two halves and keeping just one). Because a sorted phone book lets you know instantly which half a name belongs in, you never have to look at most of the book at all.

### Why the difference matters so much: n vs. log n

Plot the size of the phone book (how many pages, which computer scientists commonly call **n**) on one axis, and the time (or number of pages you have to check) on the other. Malan describes the first, page-by-page algorithm this way:

> "The slope is N because if you think of N as a number for the number of pages, well, there's a 1 to 1 relationship."

Double the phone book, and linear search takes twice as long: every time, with no exceptions. Binary search behaves completely differently:

> "This curve is so much lower and flatter, if you will, than either of these two. Mathematically, more on this another time, the slope is going to be like log based 2 of N or just logarithmic in nature."

Here's the sketch, reconstructed from the talk:

```text
time to
find it
   ^
   |                                          straight line: check every page (grows as n)
   |                                       ,-'
   |                                    ,-'
   |                                 ,-'          straight line: check every 2nd page (grows as n/2)
   |                              ,-'          ,-'
   |                           ,-'          ,-'
   |                        ,-'          ,-'
   |                     ,-'          ,-'
   |                  ,-'          ,-'
   |               ,-'          ,-'   ______________________ jump to the middle, repeat (grows as log2 n)
   |            ,-'          ,-'  _-'
   |         ,-'          ,-' _-'
   |______,-'_________,-'_-'________________________________________________>
   0                                                             size of the problem (n)
```

The payoff shows up when the phone book grows. Malan imagines two towns merging their phone books overnight, doubling the page count:

> "If the phone book size doubles from this year, for instance, to next year, you can kind of in your mind's eye think about the green line. It's not going to go up that much higher."

The numbers make this concrete:

| Approach | Checks needed for a 1,000-page book | Checks needed for a 2,000-page book |
|---|---|---|
| Check every page | ~1,000 | ~2,000 (exactly double) |
| Check every 2nd page | ~500 | ~1,000 (exactly double) |
| Jump to the middle, repeat | ~10 | ~11 (barely more!) |

> 🔑 **The single most important takeaway of this part.** Linear search's cost grows in direct proportion to the size of the problem (n). Binary search's cost grows in proportion to how many times you can cut n in half (log₂ n), which grows so slowly that doubling the problem barely moves the needle. That is the difference between an algorithm that scales and one that doesn't.

---

## Part 2: Pseudocode and the four building blocks

Before Malan writes a single line of real code (that starts next lesson, in Scratch), he translates the "jump to the middle" phone-book algorithm into words: what programmers call pseudocode.

> "Pseudo code is not one formal thing, but every human will come up with their own way of representing pseudo code. It's an English-like or human-like formulation of step by step instructions just using terse correct English or whatever human language."

Here is a reconstruction of the pseudocode he talks through on stage:

```text
1. Pick up the phone book.
2. Open to the middle of the phone book.
3. Look at the page.
4. If the person is on the page,
       call them.
5. Else if the person is earlier in the book,
       open to the middle of the left half,
       and go back to step 3.
6. Else if the person is later in the book,
       open to the middle of the right half,
       and go back to step 3.
7. Else,
       quit. (The person is not in the book.)
```

Notice this pseudocode is built from just four ingredients, and every algorithm you'll ever write (in Scratch, in C, in Python, in SQL) is built from the same four:

**Functions.** Each numbered step ("pick up," "open to," "look at," "call") is a small, self-contained piece of work.

> "Functions are verbs or actions that really get some small piece of work done for you."

**Conditionals.** Steps 4-7 are a fork in the road: depending on the answer to a question, you go down a different path.

**Boolean expressions.** The question at each fork, "is the person on this page?", has to have a yes-or-no answer.

> "A boolean expression is just a question that has a yes or no answer or a true or false answer or a 1 or zero answer."

**Loops.** Steps 5 and 6 both say "go back to step 3." That's not a mistake: it's deliberate repetition, and it's safe *because* each trip through it works on a smaller half of the book than the last:

> "A loop which somehow induces cyclical behavior again and again."

### The step everybody forgets

Look closely at step 7 above. It isn't in the original three-step version of this algorithm. Malan adds it on stage, after pointing out a "perverse corner case": what if John Harvard simply isn't in the phone book at all? Without an explicit rule for that case, the loop in steps 5-6 has nothing to stop it, and the algorithm never terminates. Malan connects this directly to real-world software failures:

> "Some human at Google or Microsoft or Apple or the like made a mistake."

That is, when your phone or laptop freezes or crashes for no obvious reason, it's very often because some programmer, somewhere, forgot to handle exactly this kind of "uncommon but possible" case.

> ✅ **What to do about it:** whenever you write a loop, ask yourself "what condition makes this stop?" *and* "what happens if the thing I'm looking for was never there?" Write pseudocode for both before you write any real code.

---

## Part 3: Machine code, compilers, and abstraction

Pseudocode is written for humans. Eventually, though, every algorithm has to run on a computer that, as you learned in Lesson 2, only ever understands 0s and 1s. Malan shows this gap directly on stage with a slide of raw 0s and 1s that, translated, just prints "hello world":

> "It turns out that not only do computers standardize information, data like numbers and letters and colors and other things, they also standardize instructions."

Chip makers (Intel, AMD, Nvidia, and others) agree in advance on which patterns of 0s and 1s mean "add these two numbers," "load this from memory," or "print this to the screen." That raw language of 0s and 1s is **machine code**, and writing it by hand (the way the very earliest programmers did, literally punching holes in cards) is exactly as tedious as it sounds. So someone built a translator:

> "A compiler is just a program that translates one language to another."

A **compiler** takes code written in a more human-friendly language (Malan uses C as the example) and turns it into the machine code a processor can run. And it doesn't stop there: languages like Python exist so you don't have to write C either; something else (an interpreter, which you'll meet properly when this course covers Python) converts Python for you, layer upon layer, all the way down to 0s and 1s.

This layering is the idea Malan calls **abstraction**:

> "In computing there's this principle of abstraction where we start with the basics and thank God we can all trust that someone else solved these really hard problems way long ago."

You never had to invent machine code, or write a compiler, or design ASCII, to write the pseudocode in Part 2. And starting next lesson, you won't have to invent Scratch's building blocks either, to use them. That's the whole point:

> "We can stand on the shoulders of others so long as we know how to use and assemble these kinds of building blocks."

```text
your pseudocode / your program
            |
            v
   a higher-level language (Python, C, ...)
            |
            v
      compiler / interpreter
            |
            v
        machine code (0s and 1s)
            |
            v
      transistors switching on/off
```

Each layer hides the one below it. That's exactly why you were able to follow the phone-book pseudocode in Part 2 without knowing anything about compilers, and it's why, starting in Lesson 4, you'll be able to snap together Scratch's building blocks without knowing how MIT implemented any of them underneath.

---

## Key takeaways

1. **An algorithm is just step-by-step instructions for solving a problem.** Correctness is necessary, but it isn't sufficient. A slow, correct algorithm and a fast, correct algorithm can solve the exact same problem.
2. **Linear search's cost grows with n; binary search's cost grows with log₂ n.** That difference barely matters for a 10-item list, and matters enormously for a million-item one.
3. **Binary search only works on sorted data.** Jumping to the middle only tells you which half to search next because the phone book was alphabetized first.
4. **All pseudocode (and all real code) is built from four ingredients:** functions (small pieces of work), conditionals (forks in the road), Boolean expressions (yes/no questions), and loops (deliberate repetition).
5. **Abstraction is what lets you build without rebuilding.** Compilers hide machine code from you; pseudocode hides real syntax from you; every layer of computing exists so the layer above doesn't have to reinvent it.

## Common pitfalls

- ❌ **Forgetting the "not found" case.** A loop that only knows how to keep searching, with no rule for "the item isn't here," can run forever or crash. Always write the failure branch.
- ❌ **Running binary search on unsorted data.** If the list isn't ordered, "the middle" tells you nothing about which half to search next: the whole trick collapses.
- ❌ **Skipping items without a safety check.** Malan's "check every 2nd page" approach is faster than checking every page, but it can walk right past the target; any shortcut like this needs an explicit rule for catching what it might skip.
- ❌ **Assuming "correct" means "good enough."** A correct-but-slow algorithm can still be a bad choice once the problem gets big: always ask how the algorithm behaves as n grows, not just whether it works on today's small example.

---

## 🛠️ Capstone Project: The Phone-Book Experiment

> This is the main hands-on project for the lesson. You'll physically run both search algorithms on a real, sorted list, count your own steps instead of a computer's, and then write down the faster one as pseudocode, proving to yourself, with your own hands, why n vs. log n is not just a theory.

### What you will build

A small paper (or plain-text) experiment with three parts: step-count data comparing linear search to binary search, a simple graph of that data, and pseudocode for the binary search you performed, written using the four building blocks from Part 2.

- A sorted list you search by hand
- A table of how many items you had to check, for both methods, across a few targets
- Pseudocode for the binary-search algorithm, including its "not found" case

### Why this is the perfect practice

| Lesson idea | Where you use it in the Phone-Book Experiment |
|---|---|
| Linear vs. binary search | You physically perform both, on the same list |
| n vs. log n | Your own step counts become the data points on the graph |
| Functions, conditionals, Boolean expressions, loops | You write the binary-search pseudocode using exactly these four ingredients |
| Handling the "not found" corner case | Your pseudocode must say what happens when the target isn't in the list |

### Milestones (build them in order, each one works on its own)

1. **Build your sorted list.** Use a real dictionary, a printed phone book if you have one, or write out about 100 names, words, or numbers on paper and alphabetize (or numerically sort) them yourself.
2. **Time linear search.** Pick 5 target entries at random. For each one, search from the very first entry, checking one at a time, and count how many entries you looked at before you found it.
3. **Time binary search.** Using the same 5 targets, search by jumping to the middle of the list, deciding which half the target must be in, and repeating on that half only. Count how many entries you checked for each target.
4. **Graph it.** Make a simple table or hand-drawn plot of list size (or step count) for linear search vs. binary search, side by side. You should see linear search's numbers climb steadily while binary search's barely move.
5. **Write the pseudocode.** Using only the four building blocks, no real programming language, write down the exact steps of the binary search you just performed by hand, including the step for "the target isn't in the list at all."
6. **Stretch goal.** Repeat the experiment with a much bigger source (an actual dictionary with tens of thousands of entries works well) and see how few *additional* checks binary search needs even though the list is far bigger: Malan's "doubling" effect from Part 1, in your own numbers.

### How you will know you are done

- ✅ You have step counts for at least 5 targets under both linear search and binary search.
- ✅ You can explain, in your own words, why the binary-search line stays nearly flat while the linear-search line keeps climbing.
- ✅ Your pseudocode includes at least one conditional, one Boolean expression, and one loop, and it explicitly handles the case where the item is not found.

> 💡 **Keep yourself honest:** don't peek at where the target is before you start each search. The whole point of an algorithm is that it works mechanically, step by step, even when you already know the answer: that discipline of writing precise, corner-case-aware steps is exactly what you'll lean on later when you design a database lookup for your own final project's web app, long before you write a single line of SQL.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Pseudocode for a shopping list (foundational)
Write pseudocode, using functions, conditionals, and a loop, for linearly searching a shopping list of 20 items for one specific item. Make sure your pseudocode says what to do if the item isn't on the list.

### Exercise 2: The doubling effect, by hand (intermediate)
Without physically doing it, trace by hand roughly how many "cuts" binary search needs for a sorted list of 1,000 items, and then for 1,000,000 items. (Hint: each cut roughly doubles what you can rule out: how many times do you have to double 1 to pass 1,000? To pass 1,000,000?) Write a sentence or two explaining why the second answer isn't a thousand times bigger than the first.

### Exercise 3: Count and report (advanced)
Extend the binary-search pseudocode you wrote in the Capstone so that it also keeps a running count of how many times it looked at a page, and reports that count once it finds (or fails to find) the target. Make sure the "not found" branch reports its count too.

---

## Cheat sheet

```text
ALGORITHM = step-by-step instructions for solving a problem.

THREE WAYS TO SEARCH A 1,000-PAGE PHONE BOOK:
  check every page .......... ~1,000 checks .... grows with n
  check every 2nd page ....... ~500 checks ..... still grows with n
  jump to the middle, repeat . ~10 checks ...... grows with log2(n)

DOUBLE THE PHONE BOOK (1,000 -> 2,000 pages):
  linear search:  doubles too       (~1,000 -> ~2,000)
  binary search:  barely changes    (~10 -> ~11)

BINARY SEARCH NEEDS SORTED DATA. No sort, no shortcut.

PSEUDOCODE'S FOUR BUILDING BLOCKS:
  function            = one small verb/action ("open to the middle")
  conditional          = a fork in the road ("if / else if / else")
  Boolean expression    = a yes/no question ("is the target on this page?")
  loop                 = deliberate repetition ("go back to step 3")

ALWAYS WRITE THE "NOT FOUND" CASE. A loop with no exit for "it isn't here"
can run forever.

ABSTRACTION, layer by layer:
  your pseudocode -> higher-level language -> compiler/interpreter
  -> machine code (0s and 1s) -> transistors switching on/off
  Each layer hides the one below it. That's why you can use a layer
  without rebuilding it.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 2:** you learned that computers represent everything as 0s and 1s. This lesson used that fact directly: the phone book's names, and even the instructions that search it, are all just patterns of bits underneath.
- **Next, Module 1 · Lesson 4 (Programming in Scratch):** you'll take the exact same four building blocks (functions, conditionals, Boolean expressions, and loops) and start snapping them together as real, runnable puzzle pieces for the first time.
- **Later, Module 4 (Algorithms):** this lesson's informal n-vs-log n graph gets a formal name (Big O notation), and you'll implement linear search and binary search yourself in real C code, complete with running-time analysis.

---

*Source: "CS50x 2026 - Lecture 0 - Scratch" by David J. Malan, Harvard University. Pseudocode, diagrams, and step counts are illustrative reconstructions of the demonstrations described in the talk.*
