# Module 4 · Lesson 13: Thinking in Running Time: Big O

> **Course:** Self-Paced CS50x
> **Module 4:** Algorithms: measure and choose algorithms, not just write them.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 3 - Algorithms](https://www.youtube.com/watch?v=6Svu_ae5ebk) · [full transcript](../../transcripts/05-lecture-3-algorithms.txt)
> **Estimated time:** 45 minutes (read plus exercises)

---

## In one sentence

Running time measures how the *number of steps* an algorithm needs grows as its input grows (not how many seconds a clock shows), and Big O notation is the shorthand computer scientists use to say, at a glance, whether an algorithm scales gracefully (like repeatedly cutting a problem in half) or badly (like checking every item one at a time).

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *The Running-Time Lab*, where you count real steps for a brute-force strategy and a halving strategy across lists of 16, 64, and 256 items, tabulate the results, and sketch the growth curves yourself. Everything before the Capstone teaches the ideas you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** CS50's slides and examples will keep changing, but the notation itself is nearly fifty years old. For the timeless, tool-agnostic version:
>
> - **[Donald Knuth, "Big Omicron and Big Omega and Big Theta," *ACM SIGACT News*, 8(2), 1976](https://dl.acm.org/doi/10.1145/1008328.1008329).** This short paper is where computer science standardized exactly the three symbols this module uses: O for upper bound, Ω (Omega) for lower bound, Θ (Theta) for "both bounds match," borrowing notation mathematicians had used since the 1890s. The tools you'll measure with this course (C programs, timers, counters) are new; the vocabulary for describing what they measure is not.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Algorithm:** a step-by-step recipe for solving a problem (first defined in Module 1 · Lesson 3). Today's twist: we stop asking only "does it work?" and start asking "how well does it work as the problem grows?"
- **Running time:** how the *amount of work* an algorithm does (usually counted in steps, not seconds) changes as the size of its input changes.
- **Problem size (n):** the standard letter computer scientists use for "how many things you're working with": people in a room, entries in a list, rows in a database table.
- **Brute force:** solving a problem the plainest way possible, by trying or checking things one at a time, with no cleverness about skipping ahead.
- **Divide and conquer:** repeatedly splitting a problem into smaller pieces (often in half) and solving the smaller pieces instead of the whole thing at once.
- **Big O notation:** the shorthand for describing how an algorithm's running time grows as n grows, written `O(...)`, focused on the worst case and on the single fastest-growing term.
- **Linear growth, written O(n):** running time that grows in direct proportion to n: double the input, and the work roughly doubles too.
- **Logarithmic growth, written O(log n):** running time that grows very slowly, because the problem is repeatedly cut in half: doubling n adds only about one more step.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In Module 1 · Lesson 3 you watched a phone book get searched three different ways, and saw an informal picture of one search staying fast no matter how big the book got. Today's talk gives that picture a name. Malan opens the lecture by reminding everyone what an algorithm even is:

> "An algorithm is just step by step instructions for solving some problem." (David Malan)

Correctness (does it get the right answer at all) was Module 1's concern. From here on, this module's concern is the other half of "good design": does it stay fast as the problem gets big? That question turns out to matter far beyond a classroom demo. By the end of this course you'll ship a database-backed web app as your final project, and the single biggest difference between a page that loads instantly and one that crawls is almost always this exact idea: a slow query versus a fast one is this lesson, just running at the scale of a database table instead of a room full of people.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain, in plain language, what "running time" means and why computer scientists count steps instead of seconds.
2. Describe the three human algorithms from the attendance demo (counting by 1s, counting by 2s, and pairwise halving) and say which growth family each one belongs to.
3. Read a size-vs-time graph and identify which curve is linear and which is logarithmic.
4. Use Big O notation to name an algorithm's growth rate, and explain why a "divide by 2" doesn't change which family it's in.

## Prerequisites

- **Module 1 · Lesson 3: Your First Algorithms**: this lesson reuses that lesson's phone book example and its informal n-vs-log n graph directly, so you should already be comfortable with the words *algorithm*, *linear search*, and *binary search*.
- No coding tools required for the main capstone path (pen and paper are enough). A working cs50.dev codespace (set up in **Module 0: Pre-flight**) is only needed for the optional stretch milestone.

---

## Part 1: An algorithm is a recipe, and today we start grading the recipe

CS50's Lecture 3 opens with a callback to Week 0, and then a promise about where the course goes next:

> "An algorithm is just step by step instructions for solving some problem." (David Malan)

Nothing about that definition has changed since Lesson 3. What changes starting today is the question you're allowed to ask about an algorithm. Up to now, "does this recipe get the right answer?" was enough. From here forward, a second question sits right next to it: "how does this recipe behave as the problem gets bigger?" Two recipes can both be perfectly correct and still be worlds apart in practice: one finishes before you notice, the other makes you wait. Today's lecture teaches you to tell the difference on sight, using a live demonstration instead of a slide of equations.

> 🔑 **Correctness is necessary, not sufficient.** A working algorithm can still be a bad choice if it doesn't scale. This module is about learning to notice that *before* it costs you.

## Part 2: Three ways to take attendance

To make "how it scales" concrete, the lecture takes attendance in a lecture hall of roughly 141 people (live, on stage), using three different human algorithms.

### Algorithm 1: count by 1s

The simplest approach: point at each person in turn and recite the count out loud, "1, 2, 3, 4…" all the way to the end. It works, but every single person costs one more spoken step. If the room doubles in size, the counting takes twice as long. This is the human equivalent of **brute force**: no cleverness, just visiting everything once.

### Algorithm 2: count by 2s

A small optimization, borrowed from a grade-school trick: count off two people at a time, "2, 4, 6, 8…", which is noticeably faster in practice. But look closely at *why* it's faster: it's still visiting the room from one end to the other, just taking bigger bites. Double the room, and this still takes twice as long as before: it has simply been made faster by a constant factor, not changed into a different kind of algorithm.

### Algorithm 3: pairwise divide and conquer

The third algorithm looks nothing like the first two. Everyone in the room stands up holding the number 1 in their head. Then, repeatedly:

> "Pair off with someone standing, add their number to yours, and remember the sum." (David Malan)

One person in each pair sits down holding the pair's combined total; the other keeps standing and looks for a new partner still on their feet. Malan names exactly what's repeating:

> "So this is a loop." (David Malan)

Each round roughly halves the number of people still standing. Keep looping (pair, add, one sits) and the room's whole population collapses into fewer and fewer numbers, until only a couple of people (and eventually one running total) remain. This is the same trick Lesson 3's phone book used to jump straight to the right page:

> "…we were dividing and conquering, tearing half of the problem away, half of the problem away." (David Malan)

The live run landed on 141 people by this method, while a colleague named Kelly, counting the traditional way one person at a time out loud, arrived at a noticeably different total. Malan doesn't pretend the human execution was flawless:

> "Presumably that's just because of some bugs in execution of the algorithm, maybe some mental math didn't quite go according to plan." (David Malan)

That aside is worth sitting with: the *algorithm* (pair off, add, halve, repeat) is sound even when the *execution* by tired, distracted humans introduces small mistakes. Big O notation, later in this lesson, describes the algorithm's shape, not whether a particular run of it was executed perfectly. Keeping "is the recipe good?" separate from "did I follow the recipe correctly?" is the same distinction Module 3's debugging lesson trained you to make.

> 💡 **Nuance:** notice that Algorithm 3 needed one extra ingredient Algorithms 1 and 2 didn't: the room had to physically pair up and combine sub-totals. Divide-and-conquer strategies are often faster, but they usually cost you some extra bookkeeping to combine the pieces back together. That trade-off is worth noticing now. You'll meet it again whenever you design any divide-and-conquer algorithm.

Here's what changes as the room gets bigger, in Malan's own framing of the payoff:

> "…the amount of time it takes to solve the Attendance problem using that 3rd and final algorithm grows very slowly because it takes a huge number of more people in the room before you even begin to feel the impacts of that growth." (David Malan)

Concretely: if the room doubled from about 141 people to about 282, counting by 1s would take about twice as many spoken steps (141 → 282). Pairwise halving, by contrast, would need only about one extra round of pairing (roughly 8 rounds to whittle 141 people down to one total, versus roughly 9 rounds for 282), because each additional round doubles how many people it can absorb.

| Algorithm | How it works | Doubling the room (~141 → ~282) |
|---|---|---|
| Count by 1s | Visit each person once | Steps roughly double: ~141 → ~282 |
| Count by 2s | Visit each person once, in bigger bites | Steps roughly double: ~71 → ~141 |
| Pairwise halving | Repeatedly pair, add, and discard half | Rounds barely grow: ~8 → ~9 |

## Part 3: Reading a running-time graph, and giving it a name

To compare the three algorithms fairly, the lecture draws them as curves on a graph: the size of the problem (n: how many people, or how many pages) along the bottom, and the number of steps needed up the side. This is the exact same shape of picture Lesson 3 used for the phone book, just re-drawn for today's attendance demo, and Malan calls back to it directly:

> "We'll think back to week zero when we did the whole phone book example…" (David Malan)

Here is a sketch of that graph, reconstructed from the talk:

```text
steps
needed
   ^
   |                                             count by 1s: a straight line (grows as n)
   |                                          ,-'
   |                                       ,-'
   |                                    ,-'           count by 2s: a straight line, half the slope
   |                                 ,-'          ,-' (grows as n/2 -- still a straight line)
   |                              ,-'          ,-'
   |                           ,-'          ,-'
   |                        ,-'          ,-'
   |                     ,-'          ,-'
   |                  ,-'          ,-'   ________________ pairwise halving: nearly flat
   |               ,-'          ,-'  _-'                 (grows as log2 n)
   |            ,-'          ,-' _-'
   |         ,-'          ,-' _-'
   |______,-'_________,-'_-'____________________________________________________>
   0                                                                size of the room (n)
```

Two of these lines are perfectly straight; only their steepness differs. Malan describes the first one directly:

> "…this N number denoting number of people in the room is indeed a straight line. And on the x axis… we have the size of the problem in people and the time to solve in steps…" (David Malan)

Counting by 1s has "a slope of one": one more person costs exactly one more step, forever. Counting by 2s is also a straight line, just a flatter one; it's faster by a fixed multiplier, but it never stops climbing in direct proportion to n. Pairwise halving is the odd one out: it curves, flattening out so much that, as Malan puts it, doubling the room barely moves it.

Rather than track the exact numbers precisely, computer science uses a broad-strokes shorthand for these shapes:

> "…we're going to use what's called big O notation, which literally is like a big O and then some parentheses…" (David Malan)

By that notation: counting by 1s is **O(n)**, "on the order of n steps." Counting by 2s is **O(n/2)**, but here's the twist that trips up almost every beginner:

> "…you ignore lower order terms or equivalently you only worry about the dominant term in whatever mathematical expression is in question." (David Malan)

O(n) and O(n/2) are both, for Big O's purposes, considered the *same family*: linear. The "divide by 2" is a constant (it doesn't change as n grows), so Big O throws it away and keeps only the part that actually shapes the curve as n gets huge. As Malan puts it:

> "…computer scientists don't care about lower order terms like divide by 2 or base 2 or anything like that." (David Malan)

Pairwise halving belongs to a different family entirely: **O(log n)**, read "on the order of log n," or "logarithmic." You don't need to be fluent in logarithms to use this: just take on faith that "log₂ of n" means "how many times can you cut n in half before you're down to one?" That's precisely the question the attendance demo's third algorithm answers with its rounds of pairing.

> 🔑 **The single most important takeaway of this part.** Big O ignores constants and only cares about the *shape* of the growth. O(n) and O(n/2) both scale badly as n gets huge: they're both "linear." O(log n) scales gracefully, because each doubling of the problem only costs about one more step, not twice as many.

> ✅ **What to do about it:** when you're comparing two algorithms, don't ask "which one has a smaller constant?" Ask "which *family* do they belong to?" A linear algorithm with a small constant will still eventually lose to a logarithmic algorithm as n keeps growing.

Big O has more families than the two you've met today (a constant-time O(1), and faster- or slower-growing ones like O(n log n) and O(n²)), and you'll meet those as later lessons need them (Lesson 15, right in this module, introduces O(n²) sorting). For now, the two shapes on the graph above, a straight line and a flattening curve, are the ones to recognize on sight.

---

## Key takeaways

1. **An algorithm's correctness and its running time are two separate questions.** A recipe can get the right answer and still be a bad choice if it doesn't scale.
2. **Counting by 1s and counting by 2s are both O(n).** A constant speed-up (twice as fast) doesn't change which family an algorithm belongs to.
3. **Pairwise halving is O(log n)**, because each additional round of halving can absorb roughly twice as many items: doubling the problem costs only about one more step.
4. **Big O deliberately ignores constants and lower-order terms**, keeping only the single fastest-growing term, so the notation stays useful no matter how big n eventually gets.
5. **A graph of size versus steps is the fastest way to tell two algorithms apart at a glance**: a straight line versus a curve that flattens out.

## Common pitfalls

- ❌ **Treating "twice as fast" as "a different Big O family."** Counting by 2s feels much snappier than counting by 1s, but both are O(n): the improvement is a constant, and Big O is built to ignore constants on purpose.
- ❌ **Confusing an execution mistake with a bad algorithm.** The attendance demo's pairwise count came out slightly off from the manual count because of human arithmetic slips mid-demo, not because the divide-and-conquer *algorithm* was flawed. Keep "is the recipe sound?" separate from "did this particular run follow it exactly?"
- ❌ **Assuming any "cut it in half" trick is automatically O(log n).** The attendance demo's halving works because addition doesn't care what order you add numbers in: every pair can combine independently. Not every problem allows this; you'll see in later lessons (and in Lesson 14's binary search) that some divide-and-conquer tricks additionally require the data to already be sorted.
- ❌ **Reading Big O as an exact step count.** O(n) doesn't mean "exactly n steps": it means "grows in proportion to n, give or take constants." Big O describes a growth trend, not a precise number.

---

## 🛠️ Capstone Project: The Running-Time Lab

> This is the main hands-on project for the lesson. You'll physically count steps for a brute-force strategy and a halving strategy across three problem sizes, so the difference between O(n) and O(log n) shows up as numbers you counted yourself, not just a claim from a lecture.

### What you will build

A small, paper-first experiment (with an optional coded stretch) that produces two things: a table of real step counts, and a hand-sketched growth graph you drew from your own data. The database-backed web app you'll build by the end of this course will run queries against tables of rows: a slow, brute-force query and a fast, indexed one are exactly this experiment, just with database rows standing in for tally marks.

- A tally-mark count for the "count by 1s" strategy at three sizes
- A round-count for the "pairwise halving" strategy at the same three sizes
- A table and a hand-sketched graph comparing the two
- An optional C program that reproduces both counts automatically

### Why this is the perfect practice

| Lesson idea | Where you use it in The Running-Time Lab |
|---|---|
| Counting by 1s (Part 2) | Milestone 1: tally-mark counting at n = 16, 64, 256 |
| Pairwise halving (Part 2) | Milestone 2: round-counting at the same three sizes |
| The size-vs-steps graph (Part 3) | Milestone 4: sketching your own two curves from your own numbers |
| Big O ignoring constants (Part 3) | Milestone 3: seeing that your halving counts barely grow while your linear counts triple |

### Milestones (build them in order, each one works on its own)

1. **Count by 1s, three times.** For n = 16, then n = 64, then n = 256, make one tally mark per item, one at a time, and record the total tally count for each size. (Yes, 256 tally marks is tedious on purpose: that tedium *is* the O(n) lesson.)
2. **Count by pairwise halving, three times.** For the same three sizes, simulate the room's pairing-off process on paper without needing physical people or objects: start with n, divide by two (round up if it's odd), write down the result, and repeat until you reach 1. Count how many divisions (rounds) it took for each of n = 16, 64, and 256.
3. **Tabulate your results.** Build a table with one row per problem size and two columns: "steps counted by 1s" and "rounds counted by halving." Notice how the first column roughly matches n itself, while the second column barely grows at all across the same range.
4. **Sketch the growth curves.** On a single sheet of graph paper (or a plain sheet with hand-drawn axes), put problem size (16, 64, 256) along the bottom and step count up the side, then plot your two data sets from Milestone 3 as two separate lines. You should see one line climbing steeply and one line staying nearly flat: your own hand-drawn version of the graph in Part 3.
5. **Stretch: verify it in C.** On cs50.dev, write a short program with a `for` loop that counts from 0 to n − 1 by 1, incrementing a counter each time, and a second loop that starts at n and repeatedly divides by 2 (integer division, rounding as needed) until it reaches 1, also incrementing a counter each time. Print both counters for n = 16, 64, and 256, and confirm they match the numbers you counted by hand in Milestones 1-2.
6. **Stretch goals.** Predict, without counting, how many halving rounds you'd need for n = 1,024 and n = 1,000,000, then check your prediction with the C program from Milestone 5 if you built it. Notice how small the increase is compared to how much bigger n became.

### How you will know you are done

- ✅ You have real step counts for both strategies at n = 16, 64, and 256, recorded in a table.
- ✅ Your "count by 1s" numbers roughly triple each time n roughly quadruples (16 → 64 → 256), while your "pairwise halving" numbers only climb by a couple of rounds each time.
- ✅ You have a hand-sketched graph, built from your own numbers, showing one steep line and one nearly flat curve.
- ✅ You can explain, in one or two sentences and without looking anything up, why the halving strategy is O(log n) and the counting strategy is O(n).

> 💡 **Keep yourself honest:** don't estimate the halving rounds in your head. Actually write down each division (256 → 128 → 64 → …) and count the rows. The whole point of this capstone is replacing "I'm pretty sure logarithms are slow-growing" with a table you produced yourself.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Name the family (foundational)
For each of the following, say whether it's most likely O(n) or O(log n), and explain why in one sentence: (a) reading every page of a book to find one sentence, (b) repeatedly folding a piece of paper in half until it's too thick to fold again, (c) checking every locker in a hallway one at a time for a lost key.

### Exercise 2: Predict before you compute (intermediate)
Without a calculator or computer, predict how many times you'd need to divide 1,000,000 by 2 (rounding as needed) before reaching 1. Write down your reasoning, then verify it by actually doing the divisions on paper. How does the answer compare to your intuition about how "big" a million is?

### Exercise 3: Why the constant doesn't matter (advanced)
Explain, in your own words and without quoting the lesson, why an algorithm that takes exactly n/100 steps is still considered O(n) rather than some faster category, even though it's 100 times quicker than an algorithm that takes n steps. Then explain why that same algorithm, at n/100 steps, is still eventually slower than an O(log n) algorithm once n is large enough, and roughly how large "enough" has to be.

---

## Cheat sheet

```text
ALGORITHM = step-by-step instructions for solving a problem.
RUNNING TIME = how the number of steps grows as the problem (n) grows.

THREE WAYS TO TAKE ATTENDANCE:
  count by 1s ............ O(n)       -- one step per person
  count by 2s ............ O(n/2)     -- still O(n): a constant speed-up, same family
  pairwise halving ........ O(log n)  -- each round can absorb roughly 2x more people

DOUBLE THE PROBLEM (n -> 2n):
  O(n) and O(n/2):  steps roughly double
  O(log n):         only about ONE more round/step needed

BIG O RULES OF THUMB:
  - Drop constants:      O(n/2)  is the same FAMILY as O(n)
  - Keep the dominant term only: the fastest-growing part is what matters as n gets huge
  - Big O usually describes the WORST case, not an exact count

FAMILIES YOU'VE MET SO FAR (steepest to flattest):
  O(n)       straight line, grows in direct proportion to n
  O(log n)   curve that flattens fast; doubling n adds ~1 step

MORE FAMILIES COMING LATER: O(1) constant, O(n log n), O(n^2) -- Lesson 15+
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 3 (Your First Algorithms):** you saw an informal n-vs-log n graph for a phone book, without any formal notation attached to it. This lesson is that same graph, now with a name (Big O) and a vocabulary you can use with anyone else who's studied computer science.
- **Next, Module 4 · Lesson 14 (Searching arrays in C):** you'll implement linear search and binary search in real C code, apply Big O to them directly, and meet two new symbols: Ω (Omega, the best case) and Θ (Theta, when best and worst case match).
- **Later, Module 4 · Lesson 15 (Sorting, the slow way):** you'll meet a new, worse family, O(n²), and see exactly why it costs so much more than the O(n) and O(log n) you learned today.
- **Later, Module 6 (Data structures):** you'll choose which data structure to use for a job largely by comparing their Big O running times: this lesson's vocabulary is the tool you'll use to make that choice.
- **Later, Module 8 · Lesson 31 (Indexes):** you'll see how a database index turns a slow, linear table scan into a logarithmic lookup: Big O, at the scale of your own final project's database.

---

*Source: "CS50x 2026 - Lecture 3 - Algorithms" by David J. Malan, Harvard University (CS50x 2026). Quotes are transcribed from the talk; obvious auto-transcription artifacts (e.g., a missing "O" rendered as a stray period in "you pronounce it big[.] of such and such") have been silently corrected for readability while preserving Malan's exact wording and meaning. Diagrams are illustrative reconstructions of the graph shown in the talk.*
