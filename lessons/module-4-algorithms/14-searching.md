# Module 4 · Lesson 14: Searching Arrays in C

> **Course:** Self-Paced CS50x
> **Module 4:** Algorithms: measure and choose algorithms, not just write them
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 3 - Algorithms](https://www.youtube.com/watch?v=6Svu_ae5ebk) · [full transcript](../../transcripts/05-lecture-3-algorithms.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

An array is nothing more exotic than a row of numbered lockers in memory that a computer can only open one at a time, and once you accept that one constraint, searching it comes down to a single design choice: check every locker in order (linear search) or exploit the fact they're sorted to skip half of what's left at every step (binary search). It's a choice you can now name precisely with Big O, Ω, and Θ, and implement in C over integers, strings, and your own custom struct.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *Mini Phonebook, Two Ways*, where you build an array of structs, search it two different ways, and literally count the steps each one takes. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Locker demos and C syntax are recent, but the mathematics of comparing algorithms by how their running time grows is decades old and language-agnostic. For the timeless, tool-agnostic version:
>
> - **[*Introduction to Algorithms*](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (MIT Press).** Often called "CLRS," it is the standard reference computer scientists cite for asymptotic notation. Its early chapters formally define O, Ω, and Θ with mathematical rigor: the same three symbols this lesson introduces informally with lockers and volunteers.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Array:** a block of memory that stores a fixed number of values of the same type, back-to-back, so the computer can jump straight to any one of them if it knows its position.
- **Index (and zero-indexing):** the numbered position of a value inside an array. In C, counting starts at 0, so an array of 7 values runs from index 0 through index 6, not 1 through 7.
- **Pseudocode:** a rough sketch of an algorithm in a mix of plain English and code-like structure (loops, conditionals), used to work out the logic before committing to a real programming language.
- **Big O notation:** shorthand for how many steps an algorithm takes in the *worst* case, as the size of its input (usually called `n`) grows large. Written `O(n)`, `O(log n)`, and so on.
- **Ω (Omega) and Θ (Theta):** two companion notations. Ω describes an algorithm's *best* case: the fewest steps it could possibly take. Θ is used only when the best case and worst case turn out to be the same, so it says both at once.
- **struct:** a C keyword for bundling several related values (of possibly different types) into one new custom data type, so you can treat them as a single unit instead of tracking several separate arrays by hand.
- **strcmp:** a function from the `string.h` library that compares two strings character by character and reports whether they are equal (returning `0`) or not, because C cannot compare strings with `==`.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 13 showed you, in the abstract, why divide-and-conquer beats brute force as a problem gets big: the phone book, the room full of people counting off in pairs. This lesson makes that idea concrete and code-shaped: the exact same "keep halving the problem" trick, applied to searching an array, with a name for how fast each approach runs and real C you can compile. Malan frames the whole exercise as a question of design, not just correctness:

> "The smarter you are with your design, the more efficient your algorithms ultimately are going to be." (David Malan)

That distinction, a program that works versus a program that works *well*, is exactly what separates a north-star database app that feels instant from one that grinds to a halt once real users show up. Every lookup your final project performs is, underneath, one of the two algorithms you write today.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the array memory model (contiguous, zero-indexed, one-locker-at-a-time access) and why it constrains every algorithm you write over it.
2. Write correct pseudocode for linear search and binary search, avoid the if/else early-return bug, and identify each algorithm's base case.
3. Classify an algorithm's running time with Big O (worst case / upper bound), Ω (best case / lower bound), and Θ (when the two match).
4. Implement linear search in C over an array of `int`s and, separately, over an array of strings using `strcmp` from `string.h`.
5. Define your own `struct` in C, build an array of them, and access fields with dot notation instead of tracking parallel arrays by hand.

## Prerequisites

- **Module 4 · Lesson 13: Thinking in running time: Big O.** This lesson assumes you already have an intuitive feel for why halving a problem beats stepping through it one piece at a time.
- Comfort writing a `for` loop, an `if`/`else if`/`else` chain, and a plain array declaration in C (Module 2 · Lessons 7-8, reinforced in Module 3 · Lesson 11).

---

## Part 1: The memory model: arrays as lockers

Last week's lesson introduced arrays as the simplest data structure in a computer: a chunk of memory broken into equal-sized pieces, storing values of one type (all integers, or all strings) back-to-back to back. This lesson starts by taking that idea seriously, because it explains *everything* that follows about how fast a search can possibly be.

Your eyes can scan a printed grid of seven numbers and spot the one you want instantly, because you have what Malan calls a "bird's eye view." A computer has no such luxury:

> "Really these arrays, these chunks of memory, are equivalent to a whole bunch of closed doors... If the computer wants to see what value is at a certain location, it has to do the metaphorical equivalent of going to that location, opening the door, and looking. Then closing it and moving on to the next." (David Malan)

> 🔑 **A computer can only look at or access one value at a time.** Every algorithm in this lesson, and every algorithm you'll ever write over an array, has to work within that one constraint. That's precisely why "how many steps did it take" is a meaningful question at all.

The second piece of the model is *how* those lockers are numbered. Programming, including all of C, counts from 0, not 1:

> "We're going to use our old zero indexing vernacular. That is to say we start counting from 0 instead of 1... if you hear something like location 6, that's actually implying that there's at least 7 total locations because we started counting at 0." (David Malan)

So an array of 7 values has lockers numbered 0 through 6:

```text
locker:  0     1     2     3     4     5     6
value:  [20] [500] [10]  [5] [100]  [1]  [50]
```

Keep that picture in mind for the rest of this lesson: to "check" a value, code has to open exactly one locker (index into the array at one position), look at what's inside, and decide what to do next before moving on.

## Part 2: Two ways to search: linear vs binary (the locker demo)

With seven real lockers on stage, filled with Monopoly money, the goal was to find one specific bill: the $50. Two volunteers each got a turn, with two different strategies.

**Jose went first, searching left to right.** Locker after locker came up empty ($10, $5, $100, $1) until, at the very last door, the $50 finally appeared. Asked to describe his own algorithm afterward, Jose put it simply:

> "My algorithm was basically walk up to the first door available, open it, check if the dollar bill was the dollar bill that I was looking for, and then put it back and then go [to] the next one." (Jose Garcia, student volunteer)

That's **linear search**: check every element, in order, until you find the one you want or run out of lockers. It needs no assumptions at all about how the values are arranged, but in the worst case, the value you want is the very last one you check.

**Caitlin went second, with an advantage: the lockers had been sorted from smallest to largest.** Instead of starting at the left, she started in the *middle*. The middle locker held 20: too small, so the answer had to be to the right. She jumped to the middle of that remaining group, got unlucky (100, too big), narrowed again, and found the $50.

That's **binary search**: check the middle of what's left, and (because the data is sorted) you know for certain whether to discard the left half or the right half. Each step throws away roughly half of the remaining problem, the same divide-and-conquer trick from the phone book and the room-counting demo in Lesson 13.

But that advantage comes with a hard requirement. Binary search only works because the data is already in order:

> "Binary search on an unsorted array is just incorrect, incorrect usage of the algorithm." (David Malan)

> ❌ **The trap:** running binary search on data that isn't actually sorted. You'll confidently discard the correct half of the array on every step and simply never find the value, not slower, just *wrong*.

There is also a real trade-off buried here, one Malan is candid about: sorting data costs time too, so if you're only going to search *once*, paying to sort first can be a net loss.

> "If it's going to take you some crazy long time... to sort... but you only need to search the data once, then what the heck are you doing? Like why are you wasting time sorting?" (David Malan)

> 💡 **A nuance worth keeping:** "faster" isn't just about the search step: it's about the total cost, including any sorting you do to earn the right to binary-search in the first place. Sometimes linear search on unsorted data is the smarter engineering call.

## Part 3: Writing pseudocode without shooting yourself in the foot

Once you have the algorithm in your head, the next skill is writing it down precisely enough that a computer (or a fellow programmer) can't misread it. This is where a subtle but very real bug hides.

Here's linear search, written correctly:

```text
For each door from left to right:
    if 50 is behind the door
        return true
return false
```

The `return false` sits at the very bottom, outside and after the loop entirely, running only if the loop finishes without ever finding a match. Now here's the version that looks almost identical but is wrong:

```text
For each door from left to right:
    if 50 is behind the door
        return true
    else
        return false
```

> "This version of this code would be wrong if I instead used our old friend if/else and made this conditional decision... because if the number 50 is not behind the first door, the [else] is telling you right then and there return false. But as we've seen in C code, whenever you return a value... that's it for the function, it is done doing its work." (David Malan)

In other words: the moment the first locker doesn't match, the `else` branch fires and the function quits, having checked exactly one out of seven lockers, and answering "not found" even if the $50 was sitting in locker 6 the whole time.

> ✅ **What to do about it:** write your "not found" case as an unconditional line that only runs after the entire loop finishes, never as an `else` attached to the very first comparison.

Translated into array notation, using zero-indexing from Part 1, linear search reads:

```text
for i from 0 to n - 1
    if 50 is behind doors[i]
        return true
return false
```

Why `n - 1` and not `n`? Because of zero-indexing:

> "If you start counting at 0 and you have n elements, the last one is going to be addressed as n minus 1, not N, because if it were N, then you actually have N + 1 elements, which is not what we're talking about." (David Malan)

Binary search's pseudocode needs one more thing linear search didn't: a **base case**: a check for when there's nothing left to search at all.

```text
if there are no doors left
    return false
if 50 is behind doors[middle]
    return true
else if 50 < doors[middle]
    search doors[0] through doors[middle - 1]      # left half
else if 50 > doors[middle]
    search doors[middle + 1] through doors[n - 1]   # right half
```

Notice the halves exclude the middle index itself. That's deliberate:

> "We already checked the middle door by asking this previous question, so you're just wasting everyone's time if you divide the half and still consider that door as checkable again." (David Malan)

> 🔑 **The single most important takeaway of this part:** every correct search needs an unconditional "give up" path (linear search's trailing `return false`, binary search's "no doors left" check), and binary search additionally must never re-examine the middle element it just ruled out.

## Part 4: Big O: naming the worst case

Rather than count steps exactly, computer scientists describe running time in broad strokes: **Big O notation**, which names the *worst-case* number of steps as the input size `n` grows large.

> "It's generally useful to use this big O notation in the context of worst case scenarios, because that really gives you a sense of how badly this algorithm could perform if you just get really unlucky with your data set." (David Malan)

Big O only cares about the *dominant* term, the one that matters most once `n` gets huge, and throws away everything smaller:

> "You ignore lower order terms, or equivalently, you only worry about the dominant term in whatever mathematical expression is in question." (David Malan)

Here is the cheat sheet of common running times, from fastest-growing to slowest-growing as `n` increases:

| Notation | Name | What it means |
|---|---|---|
| `O(1)` | constant | A fixed number of steps, no matter how big `n` gets |
| `O(log n)` | logarithmic | Steps grow *very* slowly: each step cuts the remaining problem in half |
| `O(n)` | linear | Steps grow in direct proportion to `n` |
| `O(n log n)` | "n log n" | You'll meet this properly with merge sort in Lesson 16 |
| `O(n²)` | quadratic | You'll meet this properly with selection and bubble sort in Lesson 15 |

Only two of these apply to what you've built so far:

- **Linear search is `O(n)`.** In the worst case, the value you want is in the very last locker, so you check all `n` of them.
- **Binary search is `O(log n)`.** Each comparison discards half of what's left, so the number of comparisons needed is the number of times you can halve `n` before reaching 1, which is exactly what a logarithm measures.

> 🔑 **The key contrast:** as `n` gets large, `O(log n)` pulls dramatically ahead of `O(n)`. Doubling the number of lockers costs linear search one more step on average, but it costs binary search only *one more halving*. That's the entire reason sorted data is worth having.

## Part 5: Ω and Θ: naming the best case (and when they match)

Big O tells you the worst that could happen. There's a matching symbol for the *best* that could happen:

> "Omega, a capital Omega symbol here is used for lower bounds." (David Malan)

Both of the search algorithms in this lesson can get lucky in exactly the same way, the value you want happens to be the very first thing checked:

- **Linear search's best case is Ω(1)**: Jose could, in principle, have opened the very first door and found the $50 immediately.
- **Binary search's best case is also Ω(1)**: the value you want could be sitting right at the middle on the first guess.

Whenever Big O and Ω turn out to describe the *same* running time, there's a third symbol that says both at once:

> "Capital theta is jargon you can use when big O and Omega happen to be the same." (David Malan)

Neither algorithm in this lesson qualifies yet: linear search is `O(n)` but `Ω(1)`, and binary search is `O(log n)` but `Ω(1)`, so for both, the worst case and best case are far apart. (You'll meet a real Θ in Lesson 15, once selection sort turns out to be exactly as slow no matter how lucky you get.)

| Algorithm | Big O (worst case) | Ω (best case) | Θ? |
|---|---|---|---|
| Linear search | O(n) | Ω(1) | Not equal, no Θ yet |
| Binary search | O(log n) | Ω(1) | Not equal, no Θ yet |

## Part 6: From pseudocode to C: ints, strings, and structs

Pseudocode becomes real once it compiles. Here's linear search over an array of integers, `search.c`, matching the seven Monopoly denominations from the demo:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int numbers[] = {20, 500, 10, 5, 100, 1, 50};

    int n = get_int("Number: ");

    for (int i = 0; i < 7; i++)
    {
        if (numbers[i] == n)
        {
            printf("Found\n");
            return 0;
        }
    }
    printf("Not found\n");
    return 1;
}
```

Searching for `50` finds it (at the last position); searching for `1000` correctly reports "Not found."

Now try the same program over strings instead of integers. Swap in six Monopoly game pieces and compare with `==` the way you would with integers:

```c
string strings[] = {"battleship", "boot", "cannon", "iron", "thimble", "top hat"};
string s = get_string("String: ");

for (int i = 0; i < 6; i++)
{
    if (strings[i] == s)   // looks reasonable, but it's wrong
    {
        printf("Found\n");
        return 0;
    }
}
```

Every single search reports "Not found," even for values that are clearly sitting in the array. The reason is a fact about how C sees strings versus integers:

> "For a computer it's super easy to compare two integers because they're either there or they're not in memory. But with a string... you have to compare each and every character in a string to make sure they're in fact the same." (David Malan)

`==` on strings compares *where* they live in memory, not what characters they spell out. So for today's purposes:

> "You cannot use equals equals apparently to compare two strings." (David Malan)

The fix is a function called `strcmp` ("string compare"), which walks both strings character by character and returns `0` if and only if they are identical. It lives in a header file that must be included:

> "I didn't include the string.h header library, so... [the compiler] is encountering literally the word [strcmp] and not knowing what it is, because we haven't taught it what it is by simply saying include string.h at the top." (David Malan)

The corrected loop:

```c
#include <string.h>
...
for (int i = 0; i < 6; i++)
{
    if (strcmp(strings[i], s) == 0)
    {
        printf("Found\n");
        return 0;
    }
}
```

> ❌ **The trap:** comparing C strings with `==`, or calling `strcmp` without `#include <string.h>` above `main`. Both compile-or-run problems show up exactly this way: a program that builds but silently gets every answer wrong, or a compiler error naming a function it's never heard of.

Now scale this up to something closer to week 0's phone book: names and numbers together. A first attempt uses two separate, same-length arrays:

```c
string names[]   = {"Kelly", "David", "John Harvard"};
string numbers[] = {"+1-617-495-1000", "+1-617-495-1000", "+1-949-468-2750"};
```

This works (searching `names` for `"John Harvard"` at index 2 and printing `numbers[2]` gives the right answer), but it depends on the two arrays always staying perfectly aligned by index, entry for entry, forever. Malan names the problem directly:

> "We're kind of on the honor system here, whereby the onus is on us to make sure we don't screw this up." (David Malan)

C's fix for this is a custom data type, a **struct**, that bundles a name and a number into one thing, so there's only one array to keep in sync:

```c
typedef struct
{
    string name;
    string number;
}
person;
```

> "These several lines together tell C: invent for me a new data type called person, and assume that every person in the world has a string called name and a string called number." (David Malan)

With `person` defined above `main`, you can build one array of them and fill in each record with **dot notation**:

```c
person people[3];

people[0].name = "Kelly";
people[0].number = "+1-617-495-1000";

people[1].name = "David";
people[1].number = "+1-617-495-1000";

people[2].name = "John Harvard";
people[2].number = "+1-949-468-2750";
```

> "You literally use a dot, a single period, to say go inside of that structure and access the name field, the name attribute, so to speak." (David Malan)

The search loop barely changes (it's still linear search, still using `strcmp`) but now it reads from one coherent record instead of trusting two arrays in lockstep:

```c
string name = get_string("Name: ");

for (int i = 0; i < 3; i++)
{
    if (strcmp(people[i].name, name) == 0)
    {
        printf("Found %s\n", people[i].number);
        return 0;
    }
}
printf("Not found\n");
return 1;
```

> 🔑 **What the struct actually buys you:** `people[i]` is now one indivisible record, a name *and* a number that can never drift out of sync, instead of an index you hope lines up correctly across two independent arrays. Keep this "one row, several fields" shape in mind; it is exactly the shape of a row in a database table, which you'll meet formally in Module 8.

---

## Key takeaways

1. **A computer reads memory like closed lockers.** Arrays store values contiguously and zero-indexed, and code can only inspect one element at a time. That's why counting steps is a meaningful exercise at all.
2. **Linear search always works; binary search needs sorted data.** Linear search checks every candidate in the worst case; binary search halves the remaining range each step, but only because it can trust the order.
3. **Big O is a worst-case upper bound; Ω is a best-case lower bound; Θ is when they agree.** Linear search is `O(n)`/`Ω(1)`; binary search is `O(log n)`/`Ω(1)`. Neither has a matching Θ yet.
4. **`==` cannot compare strings in C.** Use `strcmp` from `string.h`, and check its return value against `0` for equality.
5. **A `struct` bundles related fields into one type.** Dot notation (`person.name`) replaces the fragile "honor system" of keeping two parallel arrays aligned by index.
6. **Choosing an algorithm is a design decision, not just a correctness one.** Sometimes the "slow" algorithm is the right call, for instance, if you're only going to search the data once.

## Common pitfalls

- ❌ Writing linear search's "not found" case as an `else` instead of an unconditional line after the loop: the `else` returns false the instant the *first* element fails to match, without ever checking the rest.
- ❌ Running binary search on unsorted data: the less-than/greater-than branches only make sense because the array is ordered; on unsorted data you will confidently walk right past the answer.
- ❌ Re-checking the middle element after a wrong guess in binary search: the next range must exclude index `middle` (use `middle - 1` or `middle + 1`), or you waste a comparison re-asking a question you already answered.
- ❌ Comparing C strings with `==`: that compares two memory addresses, not the text inside them; always use `strcmp(a, b) == 0`.
- ❌ Forgetting `#include <string.h>` before calling `strcmp`: the compiler will refuse to build, exactly as happened live in lecture.

---

## 🛠️ Capstone Project: Mini Phonebook, Two Ways

> This is the main hands-on project for the lesson. You'll build a working array-of-structs phonebook on cs50.dev, then search it two different ways (linear and binary) and literally print how many steps each one takes, so the `O(n)` vs `O(log n)` gap stops being an abstraction and becomes a number on your own screen.

### What you will build

A single C program, `phonebook.c`, that defines a `person` struct (name + number), stores several contacts in an array of them, and can look up a contact by name two ways: a straightforward left-to-right linear search, and a binary search over a sorted copy of the same data. Both searches count and print how many comparisons ("steps") they needed, so the gap between `O(n)` and `O(log n)` shows up as a real number instead of a graph.

- The `person` struct and array → Part 6.
- Linear search with a step counter → Parts 2 and 3.
- A sorted array and binary search with a step counter → Parts 2, 3, 4, and 5.
- Comparing the two step counts side by side → Parts 4 and 5 (Big O and Ω made concrete).

### Why this is the perfect practice

| Lesson idea | Where you use it in Mini Phonebook, Two Ways |
|---|---|
| Arrays & the memory model (Part 1) | Your `person` array is a row of lockers you index into one at a time. |
| Linear vs binary search (Part 2) | You implement both, over the same data, searching by name. |
| Pseudocode pitfalls & base cases (Part 3) | Your loops need the same unconditional final "not found" and boundary checks. |
| Big O worst case (Part 4) | You'll watch linear search's step count grow as the phonebook grows. |
| Ω best case (Part 5) | You'll see both searches occasionally get lucky and finish in one step. |
| structs, strcmp, dot notation (Part 6) | Your whole data model, and every comparison, depends on getting these right. |

### Milestones (build them in order, each one works on its own)

1. **Define the record and load the data.** In `phonebook.c` on cs50.dev, `#include <cs50.h>`, `<stdio.h>`, and `<string.h>`. Define `typedef struct { string name; string number; } person;`, then hard-code an array of at least 6 `person`s (any names and numbers you like). Compile with `make phonebook`. It should build cleanly.
2. **Linear search by name, with a step counter.** Ask for a name with `get_string`. Loop over the array with an `int steps = 0` you increment on every comparison, using `strcmp`, never `==`, to compare names. Print the matching number if found, "Not found" if you exhaust the array, and always print the final step count.
3. **Build a sorted copy.** Manually re-type (or reorder) a second array, `sorted[]`, containing the exact same people arranged alphabetically by name. You're hand-sorting for now on purpose: Lesson 15 shows you how to make the computer do this itself.
4. **Binary search by name, with a step counter.** Search `sorted[]` using the middle-comparison pattern from Part 3: compare `strcmp(sorted[middle].name, query)` against `0` for a match, search the left half if the name comes before the middle, the right half if after, and stop and report "not found" once the range is empty. Count and print steps here too.
5. **Put them side by side.** Run both searches for the same three names (one near the front of the unsorted array, one near the back, and one that doesn't exist at all) and print both step counts for each. Confirm binary search never needs more steps than linear search, and usually needs far fewer.
6. **Stretch goals.** (a) Grow the phonebook to 20+ entries and rerun step 5. Watch the gap widen. (b) Try searching by phone number instead of name in the *unsorted* array only, since it isn't sorted by number, and explain in a comment why binary search isn't an option there. (c) Make the "not found" case report how many steps it took to determine that, for both algorithms.

### How you will know you are done

- ✅ `phonebook.c` compiles cleanly with `make phonebook`, and both search paths exist and run from the same file.
- ✅ Searching for a name near the end of the unsorted array takes noticeably more steps via linear search than the same name takes via binary search on the sorted copy.
- ✅ Searching for a name that isn't in the phonebook correctly prints "Not found" for both algorithms, without crashing.
- ✅ You can explain out loud, for your own code, why binary search would give a wrong answer if you ran it on the unsorted array instead of the sorted one.

> 💡 **Keep yourself honest:** don't hand-wave the step counter: make it a real integer you increment on every comparison. It's the difference between believing `O(n)` vs `O(log n)` and actually watching it happen in your own terminal.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Spot the if/else bug (foundational)
Here is a piece of linear search pseudocode with the exact bug from Part 3, hiding in plain sight:

```text
for i from 0 to n - 1
    if numbers[i] == target
        return true
    else
        return false
```

Before touching a keyboard, write down in one sentence why this returns the wrong answer whenever `target` isn't in `numbers[0]`. Then translate it into real C, run it against an array where the target is in the *last* position, and confirm your prediction.

### Exercise 2: Convert an int search to a string search (intermediate)
Starting from the ints version of `search.c` in Part 6, adapt it to search a small array of six of your favorite movie titles instead of numbers. Remember: `#include <string.h>`, and compare with `strcmp(...) == 0`, never `==`. Test it against a title at the front, one at the back, and one that isn't there.

### Exercise 3: Add a struct (advanced)
Extend Exercise 2 so each movie is paired with your own 1-10 rating, using a `typedef struct { string title; int rating; } movie;`. Ask the user for a title, and if found, print the rating you gave it using dot notation (`movies[i].rating`). If not found, print "Not found."

---

## Cheat sheet

```text
ARRAYS
  - Contiguous memory, one type, fixed size, zero-indexed: index 0 .. n-1
  - The computer inspects ONE element at a time ("open one locker at a time")

SEARCH ALGORITHMS
  Linear search   check every element left to right    needs NO particular order
  Binary search   check the middle, discard a half      needs SORTED data

PSEUDOCODE PITFALLS
  - "not found" = an unconditional line AFTER the loop, never an `else`
    off the first comparison (that quits after checking just 1 element)
  - Binary search needs a base case: "if no elements left, return false"
  - After checking middle, search middle-1 (left) or middle+1 (right) -- never middle again

RUNNING TIME (n = size of the input)
  O(1)          constant     -- a fixed number of steps
  O(log n)      logarithmic  -- binary search, worst case
  O(n)          linear       -- linear search, worst case
  O(n log n)    -- preview: merge sort (Lesson 16)
  O(n^2)        -- preview: selection/bubble sort (Lesson 15)

BIG O, OMEGA (Ω), THETA (Θ)
  O   worst case / upper bound  -- "how bad can it get"
  Ω   best case / lower bound   -- "how lucky can you get"
  Θ   used only when O and Ω are the same value

  Linear search:  O(n),     Ω(1)
  Binary search:  O(log n), Ω(1)

C SYNTAX INTRODUCED
  strcmp(a, b) == 0              correct way to test string equality (string.h)
  typedef struct { ... } name;   defines a custom data type
  variable.field                 dot notation -- accesses a field inside a struct
```

## How this connects to the rest of the course

- **Earlier, Module 4 · Lesson 13:** "Thinking in running time: Big O" gave you the intuition, divide-and-conquer beats brute force, and the running-time growth graph this lesson turns into named notation and real, compilable C.
- **Next, Module 4 · Lesson 15:** "Sorting, the slow way" answers the question this lesson leaves open: binary search needs sorted data, so how expensive is it to actually produce that order? (Selection sort and bubble sort, both O(n²).)
- **Later, Module 6:** binary search trees are binary search turned into a data structure that stays searchable even as you insert and delete entries.
- **Later, Module 8:** indexes make SQLite perform this same divide-and-conquer trick internally every time you query a table: the array of structs you built today is a preview of a database table's rows.

---

*Source: "CS50x 2026 - Lecture 3 - Algorithms" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
