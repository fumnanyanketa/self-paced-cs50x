# Module 4 · Lesson 16: Recursion and Merge Sort

> **Course:** Self-Paced CS50x
> **Module 4:** Algorithms: measure and choose algorithms, not just write them.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 3 - Algorithms](https://www.youtube.com/watch?v=6Svu_ae5ebk) · [full transcript](../../transcripts/05-lecture-3-algorithms.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

A recursive function solves a problem by calling itself on a smaller version of that same problem until it reaches a **base case** simple enough to answer directly, and merge sort turns that one idea into a sorting algorithm (sort the left half, sort the right half, merge the two sorted halves) that runs in Θ(n log n) time, a decisive step down from the Θ(n²) selection sort and bubble sort you measured in the previous lesson.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you rebuild a Mario pyramid recursively (starting from an iterative version you already know how to write), trace merge sort by hand on eight numbers by drawing its split-and-merge tree, and then implement merge sort for real in C. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Lecture demos and specific programming languages will keep changing, but the mathematics of divide-and-conquer recursion is decades old and language-agnostic. For the timeless, tool-agnostic account:
>
> - **[*Introduction to Algorithms*](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) by Cormen, Leiserson, Rivest, and Stein (MIT Press).** Known universally as "CLRS," this is the standard reference computer science students and interviewers alike learn from. Its early chapters on divide-and-conquer walk through the exact recurrence behind merge sort (solve two half-sized problems, then spend Θ(n) work combining them) that this lesson derives by hand.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Recursion:** solving a problem by having a function call itself on a smaller version of the same problem, instead of using a loop to repeat steps.
- **Recursive function:** a function that, somewhere inside its own body, calls itself.
- **Base case:** the smallest, simplest version of the problem: one your function can answer immediately without calling itself again. This is what stops the recursion; without one, the function calls itself forever.
- **Recursive case:** the part of the function where, instead of solving the whole problem directly, it does a small amount of work and then calls itself again on a smaller piece of the problem.
- **Divide and conquer:** a strategy for solving a big problem by splitting it into smaller pieces of the exact same problem, solving each piece (often recursively), and then combining the results.
- **Merge:** to combine two lists that are *each already sorted* into one sorted list, by repeatedly taking whichever list's next item is smaller.
- **Stack overflow:** a crash that happens when a program calls itself (or other functions) so many times, without ever finishing, that the computer runs out of memory to keep track of all those unfinished calls.
- **Θ (theta) notation:** how computer scientists write "this algorithm's upper bound (Big O) and lower bound (Big Omega) are the same": meaning the algorithm behaves this way no matter how lucky or unlucky the input is.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In the previous lesson you measured selection sort and bubble sort and found they both cost Θ(n²): the number of steps grows with the *square* of how much data you have, whether or not you get lucky. That is exactly the kind of cost Malan warned would "grow very slowly" for a good algorithm and painfully fast for a bad one. This lesson introduces a genuinely different way of attacking a problem (recursion) and shows what happens when you apply it to sorting:

> "Recursion is a technique in mathematics and in programming that allows you to take sort of a fundamentally different approach to a problem." (David Malan)

That different approach, applied to sorting, is merge sort, and it beats Θ(n²) with Θ(n log n), a gap that becomes enormous the moment your data set stops being tiny. Recursion is also not just a sorting trick: it is the same base-case/recursive-case pattern you will use later in this course to walk a tree structure, and the habit of "solve a smaller version of this same problem" is one of the most transferable mental models in all of computer science.

## Learning objectives

By the end of this lesson you will be able to:

1. Define recursion, and identify the base case(s) and recursive case(s) inside a given recursive function.
2. Write a recursive C function (with a correct, terminating base case) that reproduces behavior you previously wrote with loops.
3. Explain, in your own words, why a missing or wrong base case causes infinite recursion and eventually a stack overflow.
4. Trace merge sort by hand on a list of numbers, drawing its "sort left, sort right, merge" structure as a split/merge tree.
5. Implement merge sort's merge step and its recursive structure in C.
6. Derive why merge sort's running time is Θ(n log n), and explain why that beats the Θ(n²) of selection sort and bubble sort as the input grows.

## Prerequisites

- **Module 4 · Lesson 15: Sorting, the slow way**: you should already be comfortable with Big O, Big Omega, and Big Theta notation, and with selection sort and bubble sort, since this lesson measures merge sort against them directly.
- **Module 2 · Lesson 8: Functions, code quality, and the limits of numbers**: you should be able to write a function, call it, and write its prototype above `main`, since every recursive function here is, first and foremost, still just a function.
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**): you'll compile and run real C code in the Capstone.

---

## Part 1: What recursion actually is

A **recursive function** is simply a function that calls itself. That sounds like it should spiral out of control, and in fact, you've technically already seen one without the label: binary search from earlier this same lecture. "Search the left half" and "search the right half" were both really saying *"do this whole algorithm again, just on fewer doors."* Malan makes the idea explicit:

> "More practically in the world of programming, a recursive function is a function that calls itself." (David Malan)

The reason this doesn't spin forever is that every recursive function needs two distinct kinds of logic:

- A **base case**: a condition simple enough to answer immediately, with no further self-calls. Malan describes it this way:

  > "Base cases are generally conditionals that ask a question to which the answer is going to be yes or no right then and there." (David Malan)

- A **recursive case**: where the function does a little work, then calls itself again on a *smaller* version of the same problem:

  > "You call yourself, but with a smaller version of the problem." (David Malan)

That last phrase is the whole trick. If a recursive call ever handed itself the exact same size of problem, it truly would never stop. Every legitimate recursive case must shrink the problem (one fewer door to search, one shorter row to draw) so that, step by step, it is guaranteed to eventually reach the base case.

> 🔑 **The single most important takeaway of this part.** Every recursive function needs a base case (stop and answer directly) and at least one recursive case (do a bit of work, then call yourself again on a smaller problem). Miss the base case, or fail to shrink the problem, and the recursion never ends.

### A CS in-joke, as a mnemonic

Recursion is common enough as a computer science idea that it has its own running joke. If you search Google for the word "recursion," here is what happens:

> "Google's asking me, did I mean recursion? And if I click on that, I just get the same ha ha page." (David Malan)

Try it yourself: search "recursion" and click the "Did you mean: recursion" suggestion. You'll land back on the same search results, a small joke that only makes sense once you know what recursion is, and a fun way to remember it: a recursive search for "recursion" never bottoms out, because the joke *is* the missing base case.

---

## Part 2: Recursion in code (the Mario pyramid, twice)

The clearest way to see recursion is to build the exact same thing two ways: once with loops (**iteration**), once by having a function call itself. Malan uses the half-pyramid from Problem Set 1 (the same shape from Super Mario Brothers) because it has a wonderfully simple recursive definition:

> "A pyramid of height 4 is really just a pyramid of height 3 plus one more row." (David Malan)

Keep asking "well, what's a pyramid of height 3... height 2... height 1?" and you eventually bottom out:

> "What's a pyramid of height 1? A single brick on the screen." (David Malan)

That single brick is the base case in plain English. Everything taller is "a smaller pyramid, plus one more row": the recursive case.

### The iterative version first

Here is a reconstruction of the loop-based `draw` function Malan writes first, in a file called `iteration.c`:

```c
#include <cs50.h>
#include <stdio.h>

void draw(int n);

int main(void)
{
    int height = get_int("Height: ");
    draw(height);
}

// draw a pyramid of height n, one row at a time, using nested loops
void draw(int n)
{
    for (int i = 0; i < n; i++)          // for each row
    {
        for (int j = 0; j < i + 1; j++)  // for each column in that row
        {
            printf("#");
        }
        printf("\n");
    }
}
```

Run with a height of 4, this prints a four-row pyramid. Nothing here is recursive: it is two nested loops, counting rows and, within each row, counting bricks.

### The recursive version

Now Malan rewrites `draw` so that it is defined the same way he described the pyramid in English: a smaller pyramid, plus one more row.

> ❌ **The trap, live in lecture.** Malan's first attempt at the recursive version has no base case at all: just "draw a pyramid one shorter, then print one more row," forever. The compiler refuses to build it, flagging that every path through the function calls itself again with no way out. That error is the compiler protecting you from a function that would never stop calling itself.

Adding the missing base case fixes it:

```c
#include <cs50.h>
#include <stdio.h>

void draw(int n);

int main(void)
{
    int height = get_int("Height: ");
    draw(height);
}

void draw(int n)
{
    // base case: nothing left to draw
    if (n <= 0)
    {
        return;
    }

    // recursive case: draw a pyramid one row shorter first...
    draw(n - 1);

    // ...then print this row's own bricks
    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
    printf("\n");
}
```

Malan deliberately guards with `n <= 0` rather than just `n == 0`, so that an accidental negative height still stops cleanly instead of recursing forever. Run with a height of 4, this produces the *exact same output* as the iterative version, but the logic is now "smaller pyramid, then one more row" instead of "two nested loops."

> ✅ **What to do about it:** whenever you write a recursive function, write the base case *first* and ask yourself, out loud, "does every recursive call get a strictly smaller problem than the call before it?" If the answer isn't an obvious yes, you likely have an infinite recursion waiting to happen.

### The stack-overflow teaser

Out of curiosity, Malan then tries a very large height, and the program crashes, rather than just running slowly. He flags this as a preview of next lesson's territory:

> "Each time I call Draw, I'm using a little more memory, a little more memory, and my computer only has so much memory." (David Malan)

> "This program in its current form is using too much memory." (David Malan)

Notably, the *iterative* version of the same pyramid does not crash this way at very large heights. That asymmetry is your first hint that a recursive call isn't "free": each unfinished call to `draw` has to be remembered somewhere while it waits for its own recursive call to `draw(n - 1)` to finish, and that "somewhere" is a limited region of memory called the **call stack**. Run out of it, and the crash you get is called a **stack overflow**. The next lesson (Module 5, on memory addresses) is where that idea gets made concrete. For now, just remember: recursion trades a little elegance for a little memory, on every single call.

---

## Part 3: Merge sort (divide, conquer, merge) and why n log n wins

With recursion established, Malan turns it loose on the sorting problem from the previous lesson. Here is merge sort's entire pseudocode:

```text
function sort(list):
    if list has 0 or 1 elements:
        return list                # base case: already sorted
    sort the left half of list     # recursive case
    sort the right half of list    # recursive case
    merge the two sorted halves    # the one truly new idea
```

The base case is refreshingly simple: a list of one element is trivially already sorted, so there is nothing to do. Everything else, "sort the left half, sort the right half," is just recursion, this same algorithm called again on smaller pieces. The genuinely new idea is the third line: **merging** two lists that are each already sorted.

### The merge step, by itself

Suppose you already have two sorted lists of four numbers each: `1 3 4 6` on the left and `0 2 5 7` on the right. To merge them, point at the front of each list and, at every step, take whichever front value is smaller, then advance only that pointer:

| Step | Left pointer sees | Right pointer sees | Take | Merged output so far |
|---|---|---|---|---|
| 1 | 1 | 0 | 0 (right) | 0 |
| 2 | 1 | 2 | 1 (left) | 0 1 |
| 3 | 3 | 2 | 2 (right) | 0 1 2 |
| 4 | 3 | 5 | 3 (left) | 0 1 2 3 |
| 5 | 4 | 5 | 4 (left) | 0 1 2 3 4 |
| 6 | 6 | 5 | 5 (right) | 0 1 2 3 4 5 |
| 7 | 6 | 7 | 6 (left) | 0 1 2 3 4 5 6 |
| 8 | (empty) | 7 | 7 (only one left) | 0 1 2 3 4 5 6 7 |

> "What I just did is what I mean by merge the sorted halves." (David Malan)

Notice what's absent: no back-and-forth. Every pointer only ever moves forward, and each of the eight numbers is looked at exactly once. That is the whole reason merging is fast: it costs exactly n steps to merge two sorted lists totaling n elements.

### The full recursive demo, on eight numbers

Malan then applies all three steps (sort left, sort right, merge) to the unsorted list `6 3 4 1 5 2 7 0`, all the way down to single elements and back up. Drawn as a tree, splitting downward and merging upward, it looks like this:

```text
                       [6 3 4 1 5 2 7 0]
                      /                  \
              [6 3 4 1]                  [5 2 7 0]
              /       \                  /       \
          [6 3]       [4 1]          [5 2]       [7 0]
          /   \        /   \          /   \        /   \
        [6]   [3]    [4]   [1]      [5]   [2]    [7]   [0]
          \   /        \   /          \   /        \   /
         [3 6]        [1 4]          [2 5]        [0 7]
              \        /                  \        /
              [1 3 4 6]                  [0 2 5 7]
                      \                  /
                       [0 1 2 3 4 5 6 7]
```

Reading the diagram top to bottom is the *recursive* half (sort left, sort right, splitting down to single elements, the base case). Reading it bottom to top is the *merging* half: the exact same "compare fronts, take the smaller" process from the table above, just applied at three different levels.

> 🔑 **The single most important takeaway of this part.** Merge sort never compares the same pair of numbers over and over the way bubble sort and selection sort do. It splits the problem down to base cases, then merges pairs of already-sorted lists back together, doing a clean n steps of comparisons at *each level* of the tree.

### Deriving Θ(n log n)

Count the levels in that tree: eight elements split down to one-element lists takes exactly 3 levels of splitting (8 → 4 → 2 → 1), and merging climbs back up through those same 3 levels. That number, 3, is not a coincidence: it's log₂(8), because repeatedly halving 8 hits 1 after exactly 3 halvings.

> "The big O running time of merge sort is apparently not n squared, but it's log n times n, or more conventionally, n times log n." (David Malan)

> "In big O notation we would say that merge sort is on the order of N log N." (David Malan)

So merge sort's running time is **Big O of n log n**: at each of the log₂(n) levels of the tree, merging touches every element exactly once, which costs n steps per level: n steps, log n times, or n log n total.

What about the *lower* bound (Big Omega)? Bubble sort had an optimization that let it finish early on an already-sorted list, earning it Ω(n) in the best case. Merge sort's pseudocode has no equivalent shortcut: it always splits all the way down and merges all the way back up, no matter how the input started. So its lower bound is also Ω(n log n). When Big O and Big Omega match, you get to use the tighter **Θ(n log n)**: merge sort behaves this way in the best case, the worst case, and everything in between.

| Algorithm | Big O (upper bound) | Big Ω (lower bound) | Θ (tight bound)? |
|---|---|---|---|
| Selection sort | O(n²) | Ω(n²) | Θ(n²) |
| Bubble sort | O(n²) | Ω(n) | not defined (O and Ω differ) |
| Merge sort | O(n log n) | Ω(n log n) | Θ(n log n) |

### Seeing it, with music

To close the lecture, Malan cues up a side-by-side visualization: selection sort on top, bubble sort on the bottom, and merge sort in the middle, all racing to sort the same randomized bars, scored to music. Merge sort visibly finishes while the other two are still grinding through comparisons: the same gap the Θ(n²) versus Θ(n log n) numbers predict, just made visible.

> "The music just makes sorting more fun, but that's it for today. We will see you next time." (David Malan)

---

## Key takeaways

1. **A recursive function calls itself, on a smaller problem, until a base case stops it.** No base case (or one that doesn't actually shrink the problem) means the function never stops calling itself.
2. **Recursion isn't free.** Each unfinished call sits on the call stack using real memory; enough of them (as with an unbounded pyramid height) crashes the program with a stack overflow.
3. **Merge sort is "sort left, sort right, merge."** The two recursive calls are the divide-and-conquer half; the merge step, walking two sorted lists front-to-back, taking the smaller each time, is the one genuinely new idea.
4. **Merging is cheap: exactly n steps per level.** Because pointers only ever move forward, merging two sorted halves touches each element once.
5. **Θ(n log n) beats Θ(n²) as n grows.** For 8 elements the gap looks small; for millions of elements it is the difference between practical and unusable.

## Common pitfalls

- ❌ Writing a recursive function with no base case, or a base case that never actually gets reached: the classic symptom is a compiler warning ("all paths through this function will call itself") or a runtime crash after the program seems to hang.
- ❌ Writing a recursive case that doesn't shrink the problem (for example, calling `draw(n)` instead of `draw(n - 1)`): this compiles fine and still recurses forever, because nothing guarantees you'll ever reach the base case.
- ❌ Assuming "sort left, sort right, merge" means there's nothing to actually build: the recursive calls are almost free to write; the merge step is where the real logic (and the real code) lives.
- ❌ Thinking Θ(n log n) is *always* faster in wall-clock time than a Θ(n²) sort: for very small lists (a handful of elements), the overhead of all those recursive calls can make merge sort no faster, or even slightly slower, in practice. The asymptotic win only dominates once n is large.
- ❌ Forgetting that merge sort needs extra space for the halves and the merged output: unlike selection sort and bubble sort, which rearrange the original array in place, merge sort's clean version needs roughly double the memory.

---

## 🛠️ Capstone Project: Recursive Mario and Merge Sort

> This is the main hands-on project for the lesson. You'll rebuild something you already know how to write (a Mario pyramid) using recursion instead of loops, trace merge sort entirely on paper, and then implement it for real: proving to yourself that "sort left, sort right, merge" actually works, not just watching Malan act it out.

### What you will build

Three small, connected artifacts on cs50.dev: a recursive pyramid-drawer, a hand-drawn merge sort trace, and a working `merge_sort.c`. The habit of mind you build here (solve a smaller version of the exact same problem, then combine the results) is the same recursive thinking you'll lean on much later in this course, when your north-star database-backed web app needs to walk a nested structure (like threaded comments or categories) inside a single query.

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Base case / recursive case (Parts 1-2) | Milestone 2: `draw()` calling itself needs a correct, shrinking base case or it will crash. |
| "Sort left, sort right, merge" (Part 3) | Milestone 3: your hand-drawn tree shows the split down to base cases and the merge back up. |
| The merge step (Part 3) | Milestone 4: the `merge()` helper inside your C implementation. |
| Θ(n log n) derivation (Part 3) | Stretch goal: counting your own program's comparisons to see the growth rate for yourself. |

### Milestones (build them in order, each one works on its own)

1. **Build the iterative pyramid.** On cs50.dev, write `iteration.c`: ask for a height with `get_int`, then use two nested loops to print that many rows of a half-pyramid (each row `i` has `i + 1` hash marks). Confirm it prints a correct 4-row pyramid before moving on.
2. **Convert it to recursion.** Copy it to `recursion.c`. Replace the loop over rows with a `draw` function that calls itself: base case `if (n <= 0) return;`, recursive case `draw(n - 1);` followed by printing that row's own hashes. Run it with the same heights as Milestone 1 and confirm the output is character-for-character identical.
3. **Trace merge sort by hand.** On paper (or in a text file), trace merge sort on these eight numbers: `5 2 8 1 9 3 7 4`. Draw the full split/merge tree the way this lesson did (splitting down to single elements, then merging pairs back together level by level) until you reach the fully sorted list. This milestone needs no computer at all.
4. **Implement merge sort in C.** Write `merge_sort.c`: a `merge_sort(int arr[], int n)` function that copies the left and right halves into temporary arrays, recursively sorts each half, and then merges them back into `arr` (the same left-pointer/right-pointer process from Part 3). Test it on the same eight numbers from Milestone 3 and confirm the program's printed output matches your hand trace exactly, number for number.
5. **Stretch goals.** (a) Add a counter that increments on every comparison inside `merge`, print the total after sorting, and compare it against `n` × log₂(`n`) for a few different array sizes. (b) Feed your program an array that already contains duplicate values and confirm it still sorts correctly. (c) Generate an array of 1,000 random integers, time your `merge_sort` against a selection sort you wrote in Lesson 15, and note which one finishes first.

### How you will know you are done

- ✅ `iteration.c` and `recursion.c` both compile cleanly and produce identical pyramid output for the same height.
- ✅ Your hand-drawn tree for `5 2 8 1 9 3 7 4` shows every split down to single elements and every merge back up, ending in a fully sorted list.
- ✅ `merge_sort.c` compiles, runs, and sorts `5 2 8 1 9 3 7 4` into an order that matches your hand trace from Milestone 3.
- ✅ You can explain out loud, without notes, why merge sort is Θ(n log n) and why that is faster than Θ(n²) once the input is large.

> 💡 **Keep yourself honest:** don't skip straight to Milestone 4's code. The value of Milestone 3 is that your hand trace becomes the answer key you check your C program against: if they disagree, you've found a bug in one of them, and you'll know exactly where to look.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: A recursive countdown (foundational)
Write a recursive C function `void countdown(int n)` that prints `n`, then `n - 1`, and so on down to `1`, then prints `"Liftoff!"`. Identify, in a comment above each part of the function, which lines are the base case and which are the recursive case.

### Exercise 2: Trace a different list (intermediate)
Trace merge sort by hand on the four numbers `9 1 6 3`, drawing the split/merge tree the same way this lesson did for eight numbers. Since four elements split down to one-element lists in exactly 2 levels, confirm for yourself that log₂(4) = 2.

### Exercise 3: Count the comparisons (advanced)
Take your `merge_sort.c` from the Capstone and add a global counter that increments once per comparison inside `merge`. Run it on random arrays of size 10, 100, and 1,000, printing the counter each time. Compare the growth of that counter against `n` × log₂(`n`) for each size, and write one sentence describing how closely they track.

---

## Cheat sheet

```text
RECURSION
  Recursive function  -> a function that calls itself
  Base case            -> stops the recursion; answer directly, no further self-call
  Recursive case        -> does a little work, then calls itself on a SMALLER problem
  No shrinking base case -> infinite recursion -> eventually a STACK OVERFLOW (out of memory)

MARIO PYRAMID, RECURSIVELY
  draw(n):
      if n <= 0: return                 # base case
      draw(n - 1)                       # recursive case: smaller pyramid first...
      print one row of n hashes         # ...then this row

MERGE SORT
  sort(list):
      if list has 0 or 1 elements: return list     # base case
      sort the left half                            # recursive case
      sort the right half                           # recursive case
      merge the two sorted halves                   # the new idea: n steps, pointers only move forward

RUNNING TIME
  Selection sort   Θ(n²)
  Bubble sort      O(n²), Ω(n)  (no tight theta)
  Merge sort       Θ(n log n)   <- wins decisively as n grows

  n log n derivation: log2(n) levels of splitting/merging x n steps of merging per level = n log n total
```

## How this connects to the rest of the course

- **Earlier, Module 4 · Lesson 15 (Sorting, the slow way):** gave you Big O, Big Omega, and Big Theta notation, plus selection sort and bubble sort at Θ(n²), the baseline this lesson's Θ(n log n) is measured against.
- **Next, Module 5 (Pixels, hexadecimal, and memory addresses):** the stack-overflow crash you triggered in Part 2, running out of memory as unfinished recursive calls pile up, is your first hint that every variable and function call lives at an actual memory address, which the next lesson makes explicit.
- **Later, Module 6 · Lesson 23:** looking up a value in a binary search tree is this same base-case/recursive-case pattern made permanent: instead of an array you throw away after sorting, the tree *is* the sorted structure, and searching it means recursing into the left or right subtree exactly the way you recursed into the left or right half here.

---

*Source: "CS50x 2026 - Lecture 3 - Algorithms" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
