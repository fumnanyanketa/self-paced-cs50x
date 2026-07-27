# Module 6 · Lesson 21: Stacks, Queues, and Resizable Arrays

> **Course:** Self-Paced CS50x
> **Module 6:** Data structures: trade speed for memory deliberately
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 5 - Data Structures](https://www.youtube.com/watch?v=PmAI76OGE_E) · [full transcript](../../transcripts/07-lecture-5-data-structures.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

A queue and a stack are the same idea underneath: a fixed-size array wrapped in a struct that tracks how much of it is actually in use. And once you feel the pain of that fixed size, you'll learn three increasingly clever ways (copy-and-free, then `realloc`) to grow the array on demand without leaking a single byte.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a to-do stack and a ticket queue over the exact same array-backed struct, then make that array grow with `realloc` once it fills up, and prove with Valgrind that nothing leaks. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Malan's live-coded C is specific to 2026, but stacks, queues, and the trade-off between array-based and pointer-based storage are decades-old computer science, not a C quirk.
>
> - **[*The Art of Computer Programming, Volume 1: Fundamental Algorithms*](https://www-cs-faculty.stanford.edu/~knuth/taocp.html) by Donald Knuth (1968), Section 2.2.1, "Stacks, Queues, and Deques."** This is the classic, language-agnostic treatment of exactly the two data structures this lesson opens with: what defines them abstractly, independent of whatever language or memory model you implement them in.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Abstract data type (ADT):** a description of *what a data structure can do* (its operations and the rules those operations follow), completely separate from *how it's built in code*. "First in, first out" is an ADT rule; an array with a size counter is one possible implementation of it.
- **FIFO ("first in, first out"):** the rule a queue follows: whoever got in line first gets served first.
- **LIFO ("last in, first out"):** the rule a stack follows: whoever got added most recently comes off first.
- **Capacity vs. size:** capacity is the total room a structure was built with (how many slots exist); size is how much of that room is actually occupied right now. A structure can have capacity 50 and size 3: 47 slots are just sitting empty.
- **Heap memory / `malloc`:** memory you request from the operating system while your program is running, at a size you choose on the spot, using the `malloc` function (declared in `stdlib.h`). It stays reserved for you until you explicitly give it back.
- **`realloc`:** a `stdlib.h` function that resizes a chunk of memory you already got from `malloc`: growing it in place if there's room, or finding a new, bigger chunk and copying your old data into it for you, if there isn't.
- **Memory leak:** memory you `malloc`'d but never freed, and also lost track of (no pointer in your program points to it anymore), so your program can neither use it nor give it back.
- **Dictionary (as an ADT):** a collection of key/value pairs: you look something up by its *key* (a word, a name) and get back its associated *value* (a definition, a phone number).

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In **Module 5 · Lesson 19** you learned to call `malloc`, check its return value for `NULL`, and call `free` when you were done. That lesson taught you the mechanics of asking for memory. This lesson is about *why* you'd want to ask for more of it later, and it opens by naming the theme for the rest of the course. As Malan puts it at the very start of this lecture:

> "This is our last week on C. Next week, of course, we transition to Python... thematic over this week and next is going to be the theme that we've seen before of trade-offs." (David Malan)

Every data structure in this module trades something for something else: usually speed for memory, or simplicity for flexibility. A plain array is simple and fast, but you have to guess its size before your program even runs. Guess too small, and a 51st customer, a 4th sweater, or a 1000th contact has nowhere to go. Guess too large, and you've wasted memory nobody will ever use. This lesson is where you stop guessing and start growing your data structures on demand: the same skill that lets a real Contacts app, a real ticket queue, or a real to-do list accept "just one more" without ever needing to be recompiled.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the FIFO property of a queue and the LIFO property of a stack, and name their defining operations (enqueue/dequeue, push/pop).
2. Implement an array-backed queue or stack as a `struct` that separately tracks capacity and size.
3. Define a dictionary as an abstract data type of key/value pairs, independent of any particular implementation.
4. Grow a `malloc`'d array safely: allocate new memory, copy the old values across, then free the old block, without ever losing a pointer to memory you still need.
5. Use `realloc` to grow an array in one call, still checking for `NULL` and still freeing what you no longer need.

## Prerequisites

- **Module 5 · Lesson 19: `malloc`, free, and hunting memory bugs**: you should already be comfortable calling `malloc`, checking its result for `NULL`, and calling `free`; this lesson builds directly on that habit.
- **Module 5 · Lesson 20: Pass-by-reference and file I/O**: this lesson reuses the `struct` and pointer syntax from that arc.

---

## Part 1: Trade-offs, and the story of Jack and Lou

Before any code, Malan sets up the theme for the rest of the course with a short animated fable (created by Professor Shannon Duvall at Elon University) about a character named Jack who "did not have the knack" for making friends. His friend Lou visits and discovers why: Jack keeps all his clothes in one pile in a box. Every morning, he grabs whatever is on *top*, so his favorite sweater gets worn constantly while the shirts underneath never see daylight. Lou's fix: hang the clothes in a closet, add today's laundry on the left, and every morning take clothes from the *right*, the end of the line. Now Jack wears "everything once before he wears something twice."

That fable is a picture of the two data structures this lesson opens with:

- Jack's pile is a **stack**: whatever went in *last* comes out *first*.
- Lou's closet line is a **queue**: whatever went in *first* comes out *first*.

Malan is careful to name what these actually are, technically:

> "What we just saw were what are known as abstract data types, whereby there are data structures in some sense, but it's really about the design thereof, what characteristics or features or functionality these structures offer, irrespective of how they are implemented in terms of lower level implementation details." (David Malan)

That distinction matters for everything that follows. "FIFO" and "LIFO" are promises about *behavior*, not instructions for *how to build them in memory*. You could implement a queue with an array (this lesson), a linked list (next lesson), or something fancier: the promise stays the same even as the implementation changes.

> 🔑 **The single most important takeaway of this part.** An abstract data type is a contract about behavior (FIFO, LIFO, key/value lookup); a data structure is one particular way of fulfilling that contract in actual memory. You'll see several different structures fulfill the same contract across this module.

## Part 2: Queues (FIFO, enqueue, dequeue)

A queue is the everyday line you stand in at a store or an event: whoever arrived first should be served first. Malan states the property directly:

> "Queues have what computer scientists would say is a FIFO property, first in, first out. That is, if you're the first person in line, you're the first person to get out of line." (David Malan)

A queue has exactly two operations: **enqueue** (get in line) and **dequeue** (get out of line, from the front). Here's one way to implement that in C, a struct holding a fixed-size array of people, plus a separate counter for how many of those slots are actually filled:

```c
typedef struct
{
    person people[50];
    int size;
}
queue;
```

Malan explains the reasoning behind the two numbers at play here:

> "We're going to make a distinction between the capacity, like how many total people can be there, and the size, like actually how many people are in line at that moment in time, so that you know which of the spots in the array are effectively empty." (David Malan)

`50` here is the **capacity**, a hard ceiling baked into the array's declared size. `size` is how many of those 50 slots currently hold a real person. The catch, as Malan immediately points out, is that this ceiling is a real limitation: a 51st person arriving has nowhere to go. You could just change `50` to `500` before compiling, but now you're trading one problem for another:

> "There's this trade-off, because you could still be undershooting the total number of people trying to get into maybe a big concert... but at the same time, if you over-allocate memory using 5000 locations in memory, what if only a few people show up? Now you're just wasting memory." (David Malan)

That single sentence is the whole reason the second half of this lesson exists: rather than guessing a capacity once and living with the guess, you'll learn to grow the array while the program is running.

## Part 3: Stacks (LIFO, push, pop)

A stack flips the fairness of a queue on its head, on purpose. Malan states its defining property using almost the exact words from the fable:

> "A stack, as we've just seen, has a LIFO property to it last in, first out." (David Malan)

The two stack operations are **push** (add to the top) and **pop** (remove from the top). Malan reaches for two everyday examples:

> "The analogs of NQ and DQ in the world of stacks are called push, which means push something onto the top of the stack, and pop, which means remove something from the top of the stack also. And the team in the cafeterias and dining halls on campus do this all day long." (David Malan)

A cafeteria tray dispenser is a stack: the tray on top is always the one people grab, and the bottom tray might sit there for days. Your email inbox is the same idea:

> "If you've checked your Gmail recently, odds are you've opened up gmail.com or Outlook.com, and you've looked at your inbox, and where does the new mail by default end up? At the top, at the top, at the top." (David Malan)

In code, a stack can reuse essentially the same struct as a queue, an array plus a size counter, because "the last in" is always right at index `size - 1`, so removing it never requires shifting anything else:

```c
typedef struct
{
    sweater sweaters[50];
    int size;
}
stack;
```

The struct is identical in shape to the queue's; only the *rule* for which end you add to and remove from differs. That's the abstract-data-type idea from Part 1 made concrete: same underlying storage, two different behavioral contracts.

> ✅ **What to do about it:** when you're deciding between a stack and a queue for a real problem, ask which fairness property you actually need. Need "oldest request handled first"? Queue. Don't care about fairness, and mostly need "give me back the most recent thing"? Stack, and it's usually the cheaper one to implement, since you never touch anything but the end of the array.

## Part 4: Dictionaries (an abstract data type for key/value pairs)

Before diving into the code that resizes arrays, Malan introduces one more abstract data type that will matter for the rest of the module: the **dictionary**. Its everyday meaning is exactly its technical meaning:

> "A dictionary is yet another abstract data type that's sort of everywhere in the world, literally in the world of dictionaries containing words and their definitions... you can think of a dictionary really in the abstract... as really just a two-column table." (David Malan)

An actual English dictionary has a word on the left and a definition on the right. A phone book (which is how this course opened, back in Module 1) has a name on the left and a number on the right. Computer science generalizes both:

> "A computer scientist would generalize the notion of a dictionary further and just call the thing on the left a key, and the thing on the right a value." (David Malan)

A **key/value pair** is any association between one piece of data (the key you look up by) and another (the value you get back). Malan ties this straight back to the fixed-capacity problem from Part 2: if Apple or Google had implemented the Contacts app as a plain 50-element array, you'd be capped at 50 friends. Obviously unacceptable. Somewhere underneath, a real Contacts app has to solve exactly the resizing problem this lesson is about to walk through in `list.c`. (You won't build a full dictionary implementation until **Lesson 23**, when hash tables enter the picture. For now, just hold onto the definition: a dictionary is key/value pairs, full stop, regardless of how it's built.)

## Part 5: `list.c` (from a static array to `malloc`, copying, and `realloc`)

This is the heart of the lesson: a single program, `list.c`, rewritten several times live, each version solving one more problem than the last. Malan starts about as simply as C allows.

### Version 1: a static array

```c
#include <stdio.h>

int main(void)
{
    int list[3];

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;

    for (int i = 0; i < 3; i++)
    {
        printf("%i\n", list[i]);
    }
}
```

This works, and prints `1`, `2`, `3`, but the `3` in `int list[3]` is baked into the compiled program. Malan calls this **static** allocation deliberately: "by static I mean literally hard coding... in a way that is permanent." If you later decide you need a 4th slot, you cannot simply add it: the three integers you already stored might have some other value (a string, another variable) sitting in memory right next to them, so you can't assume there's room to grow in place.

### Version 2: the same array, but on the heap with `malloc`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *list = malloc(3 * sizeof(int));

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;

    for (int i = 0; i < 3; i++)
    {
        printf("%i\n", list[i]);
    }
}
```

Nothing about the `list[0] = 1;` lines changed. Malan points out that this is deliberate:

> "These three lines here using square bracket notation is just syntactic sugar for the stuff we learned last week... The computer will essentially do the requisite pointer arithmetic to figure out where to put 1, 2, and 3." (David Malan)

`list` is now a genuine pointer returned by `malloc`, not a fixed-size array, but C lets you index a pointer with `[ ]` exactly like an array, because under the hood they're the same arithmetic. The payoff for switching to `malloc` isn't visible yet: it shows up the moment you want to resize.

### Version 3, the bug: resizing by just calling `malloc` again

Malan's first attempt at "I need a 4th slot now" is this single line:

```c
list = malloc(4 * sizeof(int));   // BUG: overwrites the only pointer to the old block
```

This compiles and even seems to work, but it is a genuine mistake, and Malan names it immediately:

> "What have I done wrong here?... I'm wasting all of the memory I had from line 5 because I'm essentially forgetting where it is. If the list pointer is literally a pointer, like a foam finger pointing somewhere in memory, what I'm really doing is saying point it over here now, but I've completely lost track of those other 3 integers in memory, and that's what we described last week as a memory leak, which you could find with Valgrind." (David Malan)

The moment you reassign `list` to a brand-new block, the *only* pointer to the original 3-integer block is gone. You can never `free` it, and you can never read the 1, 2, 3 you already stored there. That block is now a permanent memory leak for as long as the program runs.

### Version 4, the fix: a temporary pointer, copy, then free

The correct fix is to never overwrite your only pointer to memory you still need. Keep the old pointer alive in a temporary variable while you set up the new block, copy your data across, and only then let go of the old block:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *list = malloc(3 * sizeof(int));
    if (list == NULL)
    {
        return 1;
    }

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;

    int *tmp = malloc(4 * sizeof(int));
    if (tmp == NULL)
    {
        free(list);
        return 1;
    }

    for (int i = 0; i < 3; i++)
    {
        tmp[i] = list[i];
    }
    tmp[3] = 4;

    free(list);
    list = tmp;

    for (int i = 0; i < 4; i++)
    {
        printf("%i\n", list[i]);
    }

    free(list);
    return 0;
}
```

Every new line here answers a specific question Malan asks out loud during the walkthrough. "Any time you use `malloc`, what should you do or check for?"

> "You should always free... [and] check to see if NULL came back, which just means something is wrong, like it's out of memory or something else went wrong, and if you don't do that, your program may very well crash with one of those segmentation faults." (David Malan)

And there's a subtlety about *order*: if the second `malloc` (for `tmp`) fails, what do you do first, before returning?

> "I first want to free that original list, and say to the operating system, 'here's your memory back.'" (David Malan)

That's why `free(list);` appears inside the `if (tmp == NULL)` block above: even when you're aborting the program, any memory you're still holding onto needs to be freed first. Only after the copy loop succeeds do you `free(list)` for real and repoint `list` at `tmp`: at that instant, `tmp` was "effectively pointing here instead," and the old block can safely go.

### Version 5, the shortcut: `realloc`

Copying every old value into a new block by hand works, but it's a lot of code for something the standard library already knows how to do. `realloc` (also declared in `stdlib.h`) does the "allocate bigger, copy the old data across" dance for you:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *list = malloc(3 * sizeof(int));
    if (list == NULL)
    {
        return 1;
    }

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;

    int *tmp = realloc(list, 4 * sizeof(int));
    if (tmp == NULL)
    {
        free(list);
        return 1;
    }
    list = tmp;
    list[3] = 4;

    for (int i = 0; i < 4; i++)
    {
        printf("%i\n", list[i]);
    }

    free(list);
    return 0;
}
```

Malan describes what `realloc` actually does under the hood:

> "It reallocates memory, but a little smarter, in that it will try to grow your existing chunk of memory if it can, which is going to be super efficient... Or if there just isn't room there... it's going to do all of the copying for you." (David Malan)

The first argument to `realloc` is the address of the block you already have. Malan flags this as an easy detail to forget, since he initially wrote a version of the code without it:

> "The first argument to `realloc`... is to put the address of the chunk of memory that you already `malloc`'d earlier, so that it knows to go there." (David Malan)

Notice that even with `realloc` doing the hard work, you still assign its result to a *temporary* variable (`tmp`) rather than straight back into `list`, and you still check that temporary for `NULL` before touching `list` again:

> "If we just say `list = realloc(...)` and something does go wrong, `realloc` by definition will return NULL but not touch the original memory: in which case we have now lost track of where that original chunk of memory is, so we can never go back to it to print it, to change it, to free it. So we have to use this temporary variable here." (David Malan)

Same discipline as Version 4, one function call instead of a hand-written loop.

> 🔑 **The single most important takeaway of this part.** Never let your only pointer to a block of memory be overwritten before you've either freed that block or copied everything you need out of it. `tmp` isn't a style preference: it's the difference between a resize and a leak.

## Part 6: How the pieces fit together

Every version of `list.c` in Part 5 is really the answer to the exact problem raised in Part 2: a queue or stack backed by a fixed-size array can only hold `capacity` items, ever. Swap the queue's `person people[50]` for a `malloc`'d, `realloc`-able array, and "the queue is full" stops being a permanent limitation and becomes "grow the array, then keep going."

```text
STATIC ARRAY            int list[3];                     size fixed at compile time
     |
     v
HEAP ARRAY               int *list = malloc(3*sizeof(int));   size chosen at runtime
     |
     v
GROW (by hand)            malloc bigger block -> copy old values -> free old block -> repoint
     |
     v
GROW (via realloc)        realloc(list, bigger size) -> check NULL -> repoint -> done

Same discipline every time:
  1. Never overwrite your only pointer to memory you still need.
  2. Check every malloc/realloc result for NULL before using it.
  3. free exactly what you malloc'd, exactly once.
```

A queue's `people` array and a stack's `sweaters` array are both, underneath, just `int list[3]` waiting to become `int *list = malloc(...)`. That's the whole lesson in one line: the abstract behavior (FIFO or LIFO) doesn't change when you make the storage resizable: only the storage does.

---

## Key takeaways

1. **Abstract data type vs. data structure.** FIFO and LIFO are contracts about behavior; an array-backed struct with a size counter is just one way to fulfill either contract.
2. **Capacity is not size.** Capacity is the total room you allocated; size is how much of it is currently used. Confusing the two is how you either overflow an array or think it's fuller than it is.
3. **A dictionary is key/value pairs, nothing more.** Whether it's an English dictionary, a phone book, or a Contacts app, the abstract shape is identical: you'll see how to implement one efficiently starting in Lesson 23.
4. **Resizing safely means never losing your only pointer.** Allocate the new block into a temporary variable, copy or let `realloc` copy the old data, free what you no longer need, and only then repoint your real variable.
5. **`realloc` does the copy for you, but not the discipline.** You still assign its result to a temporary variable and still check for `NULL` before trusting it.
6. **Space for dynamism is a trade, not a freebie.** Every technique in this module, resizable arrays included, spends more memory or more time to buy you the ability to grow and shrink; you get to decide, per problem, whether that trade is worth it.

## Common pitfalls

- ❌ Writing `list = malloc(bigger_size);` directly, overwriting your only pointer to the old block before copying anything out of it or freeing it: this is a memory leak the instant that line runs.
- ❌ Forgetting that `realloc`'s first argument must be the address of the block you're resizing: `realloc` has no memory of what you `malloc`'d unless you hand its address back to it.
- ❌ Checking `list` for `NULL` after `list = realloc(list, ...)` instead of checking a separate temporary variable first: if `realloc` fails, it returns `NULL` without touching the original block, so overwriting `list` directly destroys your only way back to your existing data.
- ❌ Treating `capacity` and `size` as the same number: a struct with `capacity = 50` and `size = 3` still has only 3 real items in it; the other 47 slots are unused space, not data.
- ❌ Growing the array but forgetting to update `size` (or `capacity`, if you track it separately): the array now has room, but the rest of your code still thinks it's full or still thinks the old, smaller capacity applies.

---

## 🛠️ Capstone Project: The To-Do Stack and the Ticket Queue

> This is the main hands-on project for the lesson. You'll implement a stack and a queue over the *same* fixed-size struct, hit its capacity wall on purpose, then replace that wall with `realloc`, proving to yourself, with Valgrind, that growing memory correctly means growing it without leaking.

### What you will build

A single C program, `stacknqueue.c`, on cs50.dev containing:

- A **to-do stack**: push new tasks on, pop the most recently added task off (LIFO). The last thing you added is the first thing you do.
- A **ticket queue**: enqueue new support tickets, dequeue the oldest ticket (FIFO). First ticket in gets handled first.
- Both built on the exact same struct shape (a fixed array of strings plus a size counter). Only the add/remove rule differs.
- A **grow function** that, once the array fills up, uses `realloc` to double its capacity, verified leak-free with Valgrind.

Every request you handle on the web later in this course (a print job, a background task, an "undo" button) is one of these two shapes underneath: something waiting in FIFO order, or something waiting in LIFO order.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| FIFO / enqueue / dequeue (Part 2) | The ticket queue's `enqueue`/`dequeue` functions. |
| LIFO / push / pop (Part 3) | The to-do stack's `push`/`pop` functions. |
| Capacity vs. size in a struct (Part 2) | Both structures share one struct definition with `capacity` and `size` fields. |
| `malloc`/copy/free discipline (Part 5) | Your first grow function, before you simplify it. |
| `realloc` with a temporary pointer and NULL check (Part 5) | Your final grow function. |

### Milestones (build them in order, each one works on its own)

1. **Set up the shared struct.** On cs50.dev, create `stacknqueue.c`. Define one struct with a `char *items[4]` array (capacity 4, on purpose: small enough to hit the wall quickly), an `int size`, and helper functions `is_full` and `is_empty`. Compile and run a `main` that just creates one and prints its `size` (should be 0).
2. **Build the to-do stack.** Write `push(char *task)` (adds at `items[size]`, then `size++`) and `pop()` (decrements `size`, returns `items[size]`). Push 3 tasks, pop them, and confirm they come back in reverse order of how you added them.
3. **Build the ticket queue.** Using a fresh instance of the same struct, write `enqueue(char *ticket)` (same as push) and `dequeue()` (returns `items[0]`, then shifts everything else left by one and decrements `size`). Enqueue 3 tickets, dequeue them, and confirm they come back in the *same* order you added them, the opposite behavior from the stack, using nearly identical code.
4. **Hit the wall on purpose.** Try to push or enqueue a 5th item into your capacity-4 array. Confirm your `is_full` check correctly rejects it instead of silently overwriting memory.
5. **Grow it, the hard way first.** Write a `grow` function that `malloc`s a new, larger array, copies every existing item across with a loop, frees the old array, and repoints your struct's array pointer at the new one. Call it from inside `push`/`enqueue` whenever `is_full` is true, and confirm your 5th item now succeeds.
6. **Simplify with `realloc`.** Rewrite `grow` to use `realloc` instead of the manual copy loop: into a temporary pointer, checked for `NULL`, freeing the old block only on failure. Confirm the program still behaves identically.
7. **Verify with Valgrind.** Compile and run your program under `valgrind ./stacknqueue`, after making sure every `malloc`/`realloc`'d block gets `free`'d before the program exits. Confirm Valgrind reports "All heap blocks were freed -- no leaks are possible."
8. **Stretch goals.** (a) Make `dequeue` O(1) instead of shifting every element, by tracking a separate `front` index instead of always shifting from position 0. (b) Add a `shrink` step that `realloc`s the array smaller once `size` drops well below `capacity`, so a queue that spikes and drains doesn't hold onto memory it no longer needs.

### How you will know you are done

- ✅ The same struct definition backs both the stack and the queue; only the add/remove logic differs.
- ✅ Pushing/popping 3 items from the stack returns them in reverse order; enqueuing/dequeuing 3 items from the queue returns them in the same order.
- ✅ Pushing a 5th item into a capacity-4 array only works after your `grow` function runs, and it does grow, not crash or silently corrupt data.
- ✅ Valgrind reports zero leaks and zero errors on a full run that pushes past capacity, grows, and then frees everything.

> 💡 **Keep yourself honest:** before you trust your own `grow` function, temporarily comment out one `free` call and re-run Valgrind. Confirm you can *see* the leak it reports, then put the `free` back. Knowing what a leak looks like in Valgrind's output is as valuable as knowing how to avoid one.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: A queue that just says no (foundational)
Write a `queue` struct with `int numbers[5]` and `int size`. Write an `enqueue` function that checks whether `size == 5` (capacity) and, if so, prints `"queue full"` and returns without changing anything, no dynamic memory yet. Enqueue 6 numbers and confirm the 6th one is correctly rejected.

### Exercise 2: Grow it by hand (intermediate)
Starting from a `malloc`'d array of 3 integers (`1`, `2`, `3`), write the "hard way" resize from Part 5, Version 4: `malloc` a new 4-element block into a temporary pointer, copy the 3 old values across with a loop, add a 4th value, `free` the original block, and repoint your variable. Print all 4 values to confirm it worked, and run it under Valgrind to confirm no leaks.

### Exercise 3: Break it, then fix it, with Valgrind as your judge (advanced)
Take your Exercise 2 program and deliberately introduce the Version 3 bug from Part 5 (`list = malloc(4 * sizeof(int));` with no temporary pointer, no copy, and no `free` of the original block). Run it under Valgrind and read the leak report closely, note how many bytes it says are leaked, and compare that to `3 * sizeof(int)`. Then revert your fix and confirm Valgrind reports zero leaks again.

---

## Cheat sheet

```text
ABSTRACT DATA TYPES
  Queue: FIFO (first in, first out)  -> enqueue (add), dequeue (remove from front)
  Stack: LIFO (last in, first out)   -> push (add to top), pop (remove from top)
  Dictionary: key/value pairs        -> look up a key, get back its value

ARRAY-BACKED STRUCT
  typedef struct { T items[CAPACITY]; int size; } thing;
  capacity = total slots that exist ever   size = slots actually in use right now

GROWING AN ARRAY SAFELY
  1. malloc/realloc into a TEMPORARY pointer, never straight into your real one.
  2. Check the temporary pointer for NULL before doing anything else with it.
  3. If growing by hand: copy every old value across with a loop before freeing the old block.
  4. If using realloc: it copies for you -- but you still need the temp pointer and NULL check.
  5. free the old block only after you no longer need it (and never free something twice).

realloc(ptr, new_size)
  - ptr must be the address of a block you already malloc'd (or realloc'd).
  - Grows in place if there's room; otherwise allocates elsewhere and copies your data over.
  - Returns NULL on failure WITHOUT touching the original block -- assign to a temp, check it,
    THEN repoint your real variable.

MEMORY LEAK = malloc'd memory you can no longer reach with any pointer.
  Classic cause: `list = malloc(bigger);` overwriting your only pointer to the old block.
  Detect it with: valgrind ./yourprogram
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 20:** "Pass-by-reference and file I/O" gave you the `struct` and pointer syntax this lesson leans on for the queue/stack struct, plus the `malloc`/`free`/NULL-check discipline from Lesson 19 that every resize here depends on.
- **Next, Module 6 · Lesson 22:** "Linked lists" solves the same growth problem a completely different way: instead of copying a whole array every time it fills up, you allocate one new node at a time and stitch it in with a pointer, trading array speed for even cheaper growth.
- **Later, Module 6 · Lesson 23:** "Trees, hash tables, and tries" builds a hash table that is, quite literally, an array whose slots each hold a linked list: this lesson's array-growing skill and Lesson 22's linked-list skill both have to be in place first for that mashup to make sense.

---

*Source: "CS50x 2026 - Lecture 5 - Data Structures" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
