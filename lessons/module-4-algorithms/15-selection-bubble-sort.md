# Module 4 · Lesson 15: Sorting, the Slow Way: Selection and Bubble Sort

> **Course:** Self-Paced CS50x
> **Module 4:** Algorithms: measure and choose algorithms, not just write them.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 3 - Algorithms](https://www.youtube.com/watch?v=6Svu_ae5ebk) · [full transcript](../../transcripts/05-lecture-3-algorithms.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Selection sort and bubble sort are two honest, straightforward ways to put a jumbled array in order: one by repeatedly hunting for the smallest remaining value, the other by repeatedly swapping neighbors that are out of order, and both cost you O(n²) steps in the worst case, though bubble sort has a trick that drops its best case all the way down to Ω(n).

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you implement both algorithms in C, print the array after every pass to watch it evolve before your eyes, and add a swap counter that proves (with real numbers, not just a claim) that bubble sort's early-exit trick pays off on nearly-sorted data. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Programming languages and hardware keep changing, but comparison-based sorting is one of the oldest, most thoroughly analyzed problems in computer science. For the timeless, tool-agnostic account:
>
> - **Donald Knuth, *The Art of Computer Programming, Volume 3: Sorting and Searching*** (Addison-Wesley). This is the classic, rigorous treatment of comparison-based sorting algorithms, including selection sort and bubble sort by name, and the mathematics behind exactly why they cost what they cost. The algorithms in this lesson are decades old and studied precisely because their behavior doesn't change with the decade.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Array:** a block of memory holding a fixed number of values of the same type, back to back, each reachable by a numeric index starting at 0. Covered in Module 4 · Lesson 14.
- **Pseudocode:** a halfway language between plain English and real code: precise enough to translate directly into C, loose enough to read like instructions to a person.
- **Comparison:** a single question an algorithm asks, like "is this number smaller than that one?" Comparisons are the unit of work we count when analyzing a sorting algorithm.
- **Swap:** exchanging the positions of two values in an array. In C this always takes a temporary variable, because you can't hold two values in one memory slot at once.
- **Pass:** one full walk through the array (or the unsorted remainder of it) from one end to the other. Both algorithms in this lesson repeat passes until the whole array is sorted.
- **Big O notation (O):** an upper bound on an algorithm's running time: how many steps it takes in the *worst* case, as the input size *n* grows. Introduced in Lessons 13-14.
- **Omega notation (Ω):** a lower bound on an algorithm's running time: how few steps it could possibly take in the *best* case.
- **Theta notation (Θ):** used when an algorithm's Big O and Omega are the same, meaning its best case and worst case grow at the same rate, with no "lucky" scenario that's asymptotically faster.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 14 gave you binary search, a beautifully fast O(log n) way to find something, but only if the array is already sorted. Malan makes that dependency explicit right at the hinge between the two topics:

> "The efficiency of binary search... was predicated on Kelly having in advance sorted the values up front... We found that binary search was faster than linear search, but it required that we sort the data." (David Malan)

So binary search's speed is a loan against work done somewhere else: sorting. This lesson is where you learn how that work actually gets done, and why it isn't free. Selection sort and bubble sort are the two simplest, most teachable ways to sort an array, and understanding exactly why they're slow (O(n²), meaning the work roughly quadruples every time the input doubles) is what will let you appreciate, later in this course, why faster algorithms like merge sort (Lesson 16) or a database engine's own `ORDER BY` (Module 8) are worth their added complexity.

## Learning objectives

By the end of this lesson you will be able to:

1. Implement selection sort in C: repeatedly find the smallest remaining value and swap it into place.
2. Implement bubble sort in C: repeatedly compare and swap adjacent out-of-order pairs so the largest remaining value "bubbles" to the end.
3. Explain, in your own words, why both algorithms are O(n²) in the worst case, using the same nested-loop reasoning Malan uses.
4. Apply bubble sort's early-termination optimization and explain why it gives bubble sort a best case of Ω(n) that selection sort, as taught, does not share.

## Prerequisites

- **Module 4 · Lesson 14: Searching arrays in C**: you should already be comfortable with arrays, indices, `for` loops, and the ideas of Big O and Omega notation from linear and binary search.
- A working cs50.dev codespace (set up in **Module 0: Pre-flight**): you'll compile and run real C code in the Capstone.

---

## Part 1: Selection sort: repeatedly pick the smallest

To make sorting concrete, Malan brought eight student volunteers on stage, each holding a lit-up number, standing in this scrambled order:

```text
7   2   5   4   1   6   0   3
```

His first approach: scan the *whole* remaining list, remember the smallest value you've seen, and once you've checked everyone, swap that smallest value into the leftmost still-unsorted position.

> "I first went through all of them... I was doing N minus 1 comparisons because if I've got N people, I've got to compare the smallest number I found against everyone else." (David Malan)

Walking the full row of eight, the smallest value turns out to be 0 (held by a volunteer named Jayden). Malan swaps Jayden into position 0, but he can't just slide everyone else over, because an array's memory is fixed size, so whoever *was* in position 0 has to go somewhere:

> "We don't want to change data that doesn't belong to us... maybe Precious, you can go over there. So you just take Jayden's spot and we'll swap these two values." (David Malan)

That single move (find the smallest, then swap it with whatever currently sits in the target slot) is the entire algorithm, repeated with one fewer element to search each time:

> "What I just acted out is what the world would call selection sort, whereby on each iteration, each pass in front of the humans, I was selecting the smallest element I could find." (David Malan)

Malan's pseudocode for it:

```text
for i from 0 to n - 1:
    find the smallest number between numbers[i] and numbers[n - 1]
    swap it with the number at location i
```

Tracing that pseudocode against the volunteers' starting order shows exactly what "one problem solved per pass" looks like:

| Pass | Array before the pass | Smallest found (in the unsorted part) | Array after the swap |
|---|---|---|---|
| 1 | `7 2 5 4 1 6 0 3` | 0 | `0 2 5 4 1 6 7 3` |
| 2 | `0 2 5 4 1 6 7 3` | 1 | `0 1 5 4 2 6 7 3` |
| 3 | `0 1 5 4 2 6 7 3` | 2 | `0 1 2 4 5 6 7 3` |
| 4 | `0 1 2 4 5 6 7 3` | 3 | `0 1 2 3 5 6 7 4` |
| 5 | `0 1 2 3 5 6 7 4` | 4 | `0 1 2 3 4 6 7 5` |
| 6 | `0 1 2 3 4 6 7 5` | 5 | `0 1 2 3 4 5 7 6` |
| 7 | `0 1 2 3 4 5 7 6` | 6 | `0 1 2 3 4 5 6 7` |

After 7 passes (n − 1, for n = 8), the array is fully sorted: position 7 never needs its own pass, because if the other seven are correct, the last value has nowhere else to go.

> 🔑 **The single most important takeaway of this part.** Selection sort finds the correct *next* value and swaps it into place, one position at a time, from left to right. It never touches an already-placed position again.

---

## Part 2: How slow is selection sort? O(n²), Ω(n²), Θ(n²)

Now count the work. Malan reasons through it pass by pass:

> "It was like n minus 1 steps plus n minus 2 steps plus n minus 3 steps plus one final step... this series here can be more simply written as n times n minus 1, all divided by 2." (David Malan)

Multiplying that out gives roughly n²/2 − n/2 comparisons, and in Big O notation, you drop everything except the fastest-growing term, because that's the one that dominates as n gets large:

> "Selection sort... is indeed in big O of N², and that's actually the worst of the algorithms we've seen. Like that's way slower than linear search, because at least linear search was big O of N. Selection sort is n squared, which of course is n times n, which... will feel much, much slower than that." (David Malan)

Here's the part that stings: unlike linear search (which can get lucky and find its target on the very first try, giving it Ω(1)), selection sort's pseudocode has no way to notice when the array is already sorted. It searches for "the smallest remaining value" on every single pass regardless, even if nothing ever needs to move:

> "The omega notation for this algorithm, even in the best case where the data is already sorted, is crazily also n squared... We can also say that selection sort is in theta of N², which is not great because that's annoyingly slow." (David Malan)

That last line is the key idea of this part: when an algorithm's Big O (worst case) and Omega (best case) are the *same* growth rate, computer scientists say it's Θ (theta) of that rate. Selection sort is Θ(n²): there is no lucky input that makes it asymptotically faster.

> ✅ **What to do about it:** don't reach for selection sort when you expect your data to already be mostly sorted: its running time doesn't reward that. Bubble sort, next, can be taught to notice.

---

## Part 3: Bubble sort: repeatedly swap out-of-order neighbors

Malan's second approach starts the volunteers back at `7 2 5 4 1 6 0 3` and takes a narrower, more local view: compare only two *adjacent* people at a time, and swap them immediately if they're out of order.

> "Let's compare 7 and 2. They're obviously out of order, so let's just immediately swap you two... 7 and 5, clearly out of order... 7 and 4... 7 and 1... 7 and 6... 7 and 0... 7 and 3." (David Malan)

Because 7 was the largest value and lost every single comparison as Malan walked left to right, it ends up all the way at the far right end of the row by the end of just one pass:

> "Precious has essentially bubbled her way up to the end of the list. And indeed that's going to be the operative term here. Another algorithm... is called bubble sort, whereby the goal is to get the biggest elements to just bubble their way up to the top of, or the end of, the list one at a time." (David Malan)

Tracing a single pass over the volunteers' starting order:

| Comparing | Out of order? | Array after this step |
|---|---|---|
| start | N/A | `7 2 5 4 1 6 0 3` |
| (7, 2) | yes, swap | `2 7 5 4 1 6 0 3` |
| (7, 5) | yes, swap | `2 5 7 4 1 6 0 3` |
| (7, 4) | yes, swap | `2 5 4 7 1 6 0 3` |
| (7, 1) | yes, swap | `2 5 4 1 7 6 0 3` |
| (7, 6) | yes, swap | `2 5 4 1 6 7 0 3` |
| (7, 0) | yes, swap | `2 5 4 1 6 0 7 3` |
| (7, 3) | yes, swap | `2 5 4 1 6 0 3 7` |

One full pass over 8 elements, and exactly one value (the biggest) has "bubbled" all the way to its final resting place. Malan's pseudocode:

```text
repeat n times:
    for i from 0 to n - 2:
        if numbers[i] and numbers[i + 1] are out of order:
            swap them
```

The inner loop stops at `n - 2`, not `n - 1`, because it always looks one slot ahead of itself (`i` and `i + 1`): going any further would compare against a slot past the end of the array, which doesn't exist. Repeating that inner pass n times bubbles up the largest, then the second-largest, then the third-largest, and so on, one per pass, which is the same nested-loop shape as selection sort, just organized differently:

> "This is ultimately going to be on the order of big O of N squared... Bubble sort, based on this analysis, is also on the order of N squared." (David Malan)

So on the worst case, bubble sort is exactly as slow as selection sort: **O(n²)**.

---

## Part 4: The early-exit trick: why bubble sort's best case is only Ω(n)

Here's where bubble sort earns its keep over selection sort. Its pseudocode, as written above, has the same blind spot: it repeats the full pass n times no matter what, even against an already-sorted array. But bubble sort's structure makes it easy to add a check that selection sort's doesn't offer as naturally: *did any swap happen at all on this pass?*

> "Here's an enhancement to bubble sort that selection sort didn't really have room for. I can say after one pass of this inner loop walking from left to right, if I made no swaps, quit... because there's no more work clearly to be done." (David Malan)

If a full left-to-right pass makes zero swaps, every adjacent pair is already in order, which means the *entire array* is sorted, and there is nothing left to gain by repeating the outer loop. That single check changes bubble sort's best-case running time dramatically:

> "The lower bound of bubble sort's running time would be said to be an omega... of N... because I'm minimally going to need to make one pass through the list. You can't possibly claim that the list is sorted unless you actually check it once... So bubble sort can be said to be an omega of N." (David Malan)

That's Ω(n): on an already-sorted array, one single pass (n − 1 comparisons, zero swaps) is enough to both verify the array is sorted *and* finish the algorithm. Compare that to selection sort's Ω(n²): no shortcut exists there, because its pseudocode always searches the entire remaining unsorted region for the minimum, whether or not it needs to.

```text
repeat n times:
    swapped = false
    for i from 0 to n - 2:
        if numbers[i] and numbers[i + 1] are out of order:
            swap them
            swapped = true
    if not swapped:
        quit
```

> ✅ **What to do about it:** when you expect your data to arrive mostly sorted (a very common real-world situation: think of a leaderboard that's re-sorted after just one new score), bubble sort with the early-exit check can be dramatically cheaper than its worst-case O(n²) suggests. Selection sort, as taught here, cannot offer you that same guarantee.

---

## Part 5: Watching it happen: the bar-chart race

Numbers on a page are one thing; watching the work happen is another. Malan closes this section with an animated visualization: a row of vertical bars, one per value, height proportional to size, with two buttons to trigger selection sort or bubble sort on the same randomized data.

For selection sort:

> "What you'll see from left to right is in pink the current smallest element that's been discovered... you'll see clearly... the smallest element ended up over here, but it might take some time for [the largest]... to end up all the way over on the right, because with each pass we're really just fixing one problem at a time." (David Malan)

For bubble sort:

> "The pink bars work a little differently. It connotes which two numbers are being compared at that moment in time... the biggest elements... are indeed bubbling their way up to the top one after the other. But... this is where n squared is sort of visualizable: we're touching these elements or looking at them so many times again and again. We are making so many darn comparisons. This is taking frustratingly long." (David Malan)

Watching the bars, the difference between the two algorithms' *style* is obvious: selection sort's pink marker sweeps the whole remaining bar chart looking for a minimum before making one confident swap, while bubble sort's marker takes small local steps, swapping constantly but locally, but their overall *pace* looks about the same, because both are quadratic. That visual "this is taking frustratingly long" feeling is exactly what O(n²) looks like when n gets into the dozens or hundreds, and it's the motivation for Lesson 16's very different approach.

```text
selection sort:  [scan the whole unsorted region] -> [one confident swap]   x (n-1) passes
bubble sort:      [compare-and-maybe-swap neighbor] x (n-1)                 x n passes
                  (unless the early-exit check fires first)
```

---

## Key takeaways

1. **Selection sort: find the minimum, then swap it into place.** One confident swap per pass, always scanning the entire unsorted remainder: O(n²), Ω(n²), Θ(n²).
2. **Bubble sort: compare and swap neighbors, repeatedly.** The largest remaining value bubbles to the end each pass: O(n²) in the worst case, same as selection sort.
3. **Bubble sort's early-exit check is the difference-maker.** If a pass makes zero swaps, the array is already sorted and you can stop, giving bubble sort Ω(n), a best case selection sort (as taught) does not share.
4. **Θ means "no lucky input helps."** Selection sort is Θ(n²): its best and worst case grow at the same rate. Bubble sort is not Θ of anything simple, because its O(n²) and Ω(n) differ.
5. **Both are teaching tools, not production sorts.** Their value is that they're easy to reason about by hand: real code almost always reaches for something faster (Lesson 16's merge sort, or a database's built-in sort in Module 8).

## Common pitfalls

- ❌ Forgetting selection sort's inner search has to scan *the entire remaining unsorted region* every single pass, even when the array is already sorted: that's exactly why its Ω is n², not n.
- ❌ Writing bubble sort's inner loop to `n - 1` instead of `n - 2`: since it always compares `numbers[i]` against `numbers[i + 1]`, going to `i = n - 1` would read past the end of the array.
- ❌ Adding the early-exit check but forgetting to reset the `swapped` flag to `false` at the start of every outer pass: if you only set it once outside the loop, the algorithm will falsely think it never made a swap and quit early, even mid-array.
- ❌ Assuming the early-exit optimization also helps selection sort "for free." It doesn't: selection sort's structure doesn't produce a natural "did anything change?" signal the way a pairwise-swap pass does.
- ❌ Confusing "fewer swaps" with "faster." Bubble sort with early exit still does the same number of *comparisons* as unoptimized bubble sort on a scrambled array: the savings only show up when the data is nearly sorted.

---

## 🛠️ Capstone Project: Race Your Own Sorts

> This is the main hands-on project for the lesson. You'll implement both algorithms in C over the same small array, print its evolution pass by pass, and then prove (with a swap counter, not just a claim) that bubble sort's early-exit trick actually pays off.

### What you will build

A single C program on cs50.dev, `sorts.c`, that sorts a small hardcoded array of integers two different ways and reports how much work each way did. Pieces, each mapped to a lesson idea:

- A `print_array` helper, so you can literally watch the array change pass by pass (Parts 1 and 3).
- A selection sort implementation with a swap counter (Parts 1-2).
- A bubble sort implementation with a swap counter (Parts 3-4).
- Bubble sort's early-exit optimization, and a side-by-side comparison of swap counts on scrambled vs. nearly-sorted input (Part 4).

This is also your first hands-on taste of a question you'll meet again at the very end of this course: when your north-star database-backed web app grows to thousands of rows, its `ORDER BY` clause (Module 8) is running a sorting algorithm under the hood, and now you'll actually know, from having counted your own swaps, roughly what that costs.

### Why this is the perfect practice

| Lesson idea | Where you use it in Race Your Own Sorts |
|---|---|
| Selection sort pseudocode (Part 1) | Milestone 2: implement it, printing the array after every pass. |
| O(n²)/Ω(n²)/Θ(n²) analysis (Part 2) | Milestone 3: a swap counter that stays roughly the same size regardless of input order. |
| Bubble sort pseudocode (Part 3) | Milestone 4: implement it, printing the array after every pass. |
| Early-exit optimization, Ω(n) (Part 4) | Milestones 5-6: add the `swapped` flag and watch the swap counter crash on nearly-sorted input. |

### Milestones (build them in order, each one works on its own)

1. **Set up the array and a print helper.** In `sorts.c`, include `cs50.h` and `stdio.h`, declare `int numbers[] = {7, 2, 5, 4, 1, 6, 0, 3};` with `int n = 8;`, and write a `print_array` function that prints all `n` values space-separated on one line. Call it once before sorting anything and confirm it prints `7 2 5 4 1 6 0 3`.
2. **Implement selection sort, printing every pass.** For each `i` from `0` to `n - 2`, scan `numbers[i..n-1]` to find the index of the smallest value, swap it into position `i`, and call `print_array` right after the swap. Run it and confirm you see the array evolve exactly like the Part 1 trace table, ending fully sorted.
3. **Add a swap counter to selection sort.** Declare `int swaps = 0;` before the loop, increment it every time you perform the three-line swap (even if the "smallest" index equals `i`, for simplicity), and print the total after sorting. Run it once and note the number.
4. **Implement bubble sort, printing every pass, with its own swap counter.** Using a fresh copy of the original array, repeat `n` times: walk `i` from `0` to `n - 2`, swap `numbers[i]` and `numbers[i+1]` whenever they're out of order, incrementing a `swaps` counter each time. Print the array after every full outer pass.
5. **Add the early-exit optimization.** Introduce a `bool swapped` (from `cs50.h` or `stdbool.h`), set it to `false` at the start of each outer pass, set it to `true` whenever you swap, and `break` out of the outer loop if a pass ends with `swapped` still `false`. Re-run on the original scrambled array and confirm the final sorted output and swap count are unchanged (the array wasn't sorted early, so this shouldn't fire yet).
6. **Prove the early exit pays off on nearly-sorted data.** Change the array to something nearly sorted, like `{0, 1, 2, 3, 4, 5, 7, 6}` (just one pair out of place), and run both sorts again. Selection sort's swap count should barely change from its worst-case shape, while bubble sort's early exit should let it quit after very few passes: print and compare both swap counts side by side.
7. **Stretch goals.** Add a separate *comparison* counter (distinct from the swap counter) to both algorithms, and check whether it behaves the way Part 2 and Part 4 predict: does selection sort's comparison count stay essentially the same regardless of input order? Does bubble-sort-with-early-exit's comparison count shrink close to `n - 1` on the nearly-sorted array? For an extra visual stretch, replace `print_array`'s numbers with rows of `#` characters (bar-chart style) so each pass prints something closer to the visualization from Part 5.

### How you will know you are done

- ✅ `sorts.c` compiles cleanly with `make sorts` and runs both algorithms without crashing.
- ✅ Running selection sort on `{7, 2, 5, 4, 1, 6, 0, 3}` prints the array after every pass and ends sorted as `0 1 2 3 4 5 6 7`.
- ✅ Running bubble sort on the same array also ends sorted, and its swap count is reported.
- ✅ On the nearly-sorted input `{0, 1, 2, 3, 4, 5, 7, 6}`, bubble sort's swap count (and number of passes before its early exit fires) is visibly, measurably lower than on the scrambled input: you can point to the actual printed numbers as proof, not just recite the theory.

> 💡 **Keep yourself honest:** don't just trust that the early exit "should" help: print the pass count or swap count for both the scrambled and nearly-sorted runs and put the numbers side by side. If the nearly-sorted run doesn't show fewer passes, your `swapped` flag isn't wired up correctly.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Hand-trace it on paper (foundational)
Take the array `[5, 3, 8, 1]` and, without writing any code, hand-trace selection sort pass by pass the way the Part 1 table does: write down the array's contents after each swap. Then do the same for one full bubble sort pass over the same starting array. Compare: which value ends up in its final position first under each algorithm, and why?

### Exercise 2: Swap counts on shaped inputs (intermediate)
Using your Capstone's selection sort (with its swap counter), run it on three different 8-element arrays: already sorted (`0` through `7`), reverse sorted (`7` down to `0`), and randomly scrambled. Record the swap count each time. Are the counts close to each other? Explain, in terms of Ω(n²), why selection sort's swap count doesn't meaningfully reward an already-sorted input the way bubble sort's does.

### Exercise 3: Comparisons vs. swaps (advanced)
Add a *comparison* counter (separate from the swap counter) to both your selection sort and your early-exit bubble sort. Run both on the same reverse-sorted, random, and already-sorted 8-element arrays, and tabulate all four numbers (selection comparisons, selection swaps, bubble comparisons, bubble swaps) for each input. Which counter changes the most across input shapes, and which barely changes at all? Explain your results using the O(n²), Ω(n²), and Ω(n) claims from Parts 2 and 4.

---

## Cheat sheet

```text
SELECTION SORT
  for i from 0 to n-1:
      find the smallest value in numbers[i..n-1]
      swap it into numbers[i]
  Big O:    O(n^2)   -- always scans the full unsorted remainder
  Omega:    Omega(n^2) -- no shortcut for an already-sorted array
  Theta:    Theta(n^2) -- best case and worst case grow at the same rate

BUBBLE SORT
  repeat n times:
      swapped = false
      for i from 0 to n-2:
          if numbers[i] and numbers[i+1] out of order: swap them; swapped = true
      if not swapped: quit   <- the early-exit optimization
  Big O:    O(n^2)   -- worst case, e.g. reverse-sorted input
  Omega:    Omega(n) -- WITH early exit: one clean pass proves an already-sorted array

RULE OF THUMB
  Expect mostly-sorted data ariving repeatedly?  -> bubble sort (with early exit) can be cheap.
  No such guarantee, or a one-off sort?           -> selection sort costs the same either way,
                                                      so its simplicity doesn't buy you anything extra.
  Either way, both are O(n^2) -- see Lesson 16 for something genuinely faster.
```

## How this connects to the rest of the course

- **Earlier, Module 4 · Lesson 14 (Searching arrays in C):** binary search needed sorted data to work its O(log n) magic: this lesson is where that sorted data actually comes from, and what it costs to produce.
- **Next, Module 4 · Lesson 16 (Recursion and merge sort):** merge sort divides the array in half, sorts each half, and merges them: an O(n log n) algorithm that makes selection and bubble sort's O(n²) look, in Malan's words, "frustratingly long" by comparison.
- **Later, Module 8:** when you write `ORDER BY` in SQL for your database-backed capstone web app, the database engine is running a sorting algorithm on your behalf: after this lesson, you'll actually understand what kind of cost that hides, and why database engineers care so much about not reaching for an O(n²) sort at scale.

---

*Source: "CS50x 2026 - Lecture 3 - Algorithms" by David J. Malan, Harvard University (CS50x 2026). Quotes are transcribed from the talk; obvious auto-transcription artifacts (e.g., "ton" for "to n", "fader" for "theta") have been silently corrected for readability while preserving Malan's exact wording and meaning. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
