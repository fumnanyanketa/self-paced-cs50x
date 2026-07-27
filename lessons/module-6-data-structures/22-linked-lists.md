# Module 6 · Lesson 22: Linked Lists

> **Course:** Self-Paced CS50x
> **Module 6:** Data structures: trade speed for memory deliberately
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 5 - Data Structures](https://www.youtube.com/watch?v=PmAI76OGE_E) · [full transcript](../../transcripts/07-lecture-5-data-structures.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

A linked list stores each value next to a pointer to the next value instead of packing values back-to-back like an array, so adding a brand-new first node costs the same tiny, constant amount of work no matter how long the list already is: the trade is that searching, deleting, or reaching the end of that same list now costs one step per node, and nothing frees itself automatically, so you must walk the whole list and free every node yourself.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a linked list of numbers on cs50.dev by prepending, print it, upgrade it to keep itself sorted as you insert, and then prove with Valgrind that you freed every single node. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Malan's live-coded C is specific to 2026, but a "node containing a value and a pointer to the next node" is decades-old computer science, not a C quirk.
>
> - **[*The Art of Computer Programming, Volume 1: Fundamental Algorithms*](https://www-cs-faculty.stanford.edu/~knuth/taocp.html) by Donald Knuth (1968), Section 2.2.3, "Linked Allocation."** This is the classic, language-agnostic treatment of exactly the structure this lesson builds (values scattered anywhere in memory, stitched into an ordered chain purely by pointers), decades before any modern language shipped it as a built-in list type.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Pointer:** a variable that stores a memory address ("where" some other value lives) rather than storing the value itself. (You met this in Module 5.)
- **Struct (structure):** a custom data type you define yourself that bundles several related values together under one name, declared with the `struct` keyword.
- **Self-referential structure:** a struct that has, as one of its own fields, a pointer to another struct of that exact same type. This is the one new trick this lesson adds to `struct`.
- **Node:** a generic name for one "box" in a linked list. Each node holds a piece of data you actually care about (like a number) plus a pointer to the next node.
- **Arrow operator (`->`):** shorthand in C for "follow this pointer, then reach inside the struct it points to." `n->number` means exactly the same thing as `(*n).number`, just easier to type and read.
- **Metadata:** data whose job is to help you keep track of other data, rather than being the data you actually care about.
- **Traverse:** to visit every node in a data structure one at a time, by following its pointers from the first node to the last.
- **Big O (running time):** shorthand for how the number of steps an operation takes grows as the amount of data, `n`, grows. `O(1)` means "constant: the same number of steps no matter how big the structure is"; `O(n)` means "grows in direct proportion to the size of the structure."

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

**Module 6 · Lesson 21** left you with a working but unsatisfying answer to arrays' fixed-size problem: `realloc` a bigger block, and the standard library quietly copies everything over for you. That works, but Malan is upfront about what it costs at scale: copying isn't free, and for a 3-million-element array, it's a lot of wasted motion just to make room for one more value. This lesson asks a different question: what if you never had to move anything you already stored? Malan frames the whole idea around a single, load-bearing distinction:

> "So data is value or values you care about. Metadata is data that helps you maintain the data you care about." (David Malan)

A linked list spends a little extra memory (metadata, in the form of one pointer per value) so that every new value can be dropped in wherever there happens to be room, with the pointers doing the work of keeping everything in the right order. Nothing ever needs to be copied to make space. That flexibility isn't free, though, and quantifying exactly what it costs you in running time is the back half of this lesson.

## Learning objectives

By the end of this lesson you will be able to:

1. Define a self-referential `struct node` with a value field and a `next` pointer, and explain why the struct needs an internal tag name (`struct node` inside itself) to even compile.
2. Build a linked list from nothing by prepending nodes one at a time, and draw the pointer picture after each step, including the exact order of pointer updates that avoids orphaning the rest of the list.
3. Traverse and print every value in a linked list with a `while` loop, and rewrite the same logic as an equivalent `for` loop using a temporary pointer.
4. State the Big O running time of prepending, appending, searching, and deleting in a singly linked list, and explain in your own words why each one is what it is.
5. Walk through the four cases of inserting into a sorted linked list (empty list, belongs first, belongs last, belongs in the middle) and identify which case a given insertion falls into.
6. Write an `unload` function that frees every node in a list, one at a time, and explain why calling `free` on the list variable alone would not work.

## Prerequisites

- **Module 6 · Lesson 21: Stacks, Queues, and Resizable Arrays**: this lesson picks up exactly where that one left off: you've felt the pain of copying a whole array just to grow it, and now you'll solve growth a completely different way.
- **Module 5 · Lessons 18-19 (pointers, and `malloc`/`free`)**: including Lesson 19, "`malloc`, free, and hunting memory bugs." You should already be comfortable with what a pointer stores, dereferencing with `*`, calling `malloc`, checking its result for `NULL`, and calling `free`. This lesson uses all of that on nearly every line of code.

---

## Part 1: A self-referential struct, and the arrow that finally looks like one

An array's whole appeal is that its values sit back-to-back in memory, so you can jump anywhere with simple arithmetic. Its whole limitation is that exact same fact: the values *have* to be contiguous, which is why growing one means finding a bigger contiguous block and copying everything into it. Malan poses the obvious alternative:

> "What if we sort of try to preempt that kind of pain and try to just build up a list by linking it together no matter where the values actually are in memory?" (David Malan)

Suppose the number `1` ends up at address `0x123`, but the next value you store, `2`, happens to land at some unrelated address, `0x456`, because that's just where the computer had room. You can't use pointer arithmetic to hop from one to the other: they aren't a fixed number of bytes apart. So instead of relying on position, store the *address of the next value* right alongside each value. That's the whole idea:

> "Data is value or values you care about. Metadata is data that helps you maintain the data you care about." (David Malan)

Each value you care about (say, `1`) gets a neighbor in memory: a pointer to wherever the *next* value lives. Follow that pointer, and you've found the next value, and its own pointer tells you where the one after that lives, and so on, until you hit a pointer that's `NULL`, which marks the end. Malan gives this two-field package a name:

> "That's going to be a term of art we start using: a node. It's just a generic structure that contains data and metadata, usually like the number you care about and a pointer to the next such node." (David Malan)

In C, a **node** is a `struct` with two fields: the value, and a pointer to the next node of the *same type*. That second part, a struct containing a pointer to its own type, is called a **self-referential structure**, and it needs one small piece of new syntax to compile:

```c
typedef struct node
{
    int number;
    struct node *next;
}
node;
```

Two things here are new, and both matter:

- **`struct node *next;`**, not just `node *next;`. Malan explains why: "The compiler reads your code top to bottom, left to right." At the point the compiler reaches the `next` field, the `typedef`'d name `node` doesn't exist *yet*: it's only finished being defined once the closing `}` and its trailing `node;` are reached, several lines later. But `struct node` is a valid, in-progress name for the struct the very moment you write `struct node { ... }`, before the `typedef` finishes. So inside the struct's own body, you always refer to yourself as `struct node *`, never as the shorter `typedef` name.
- **The tag name `node` right after `struct`**: this is what makes `struct node` a legal thing to write on the very next line, even though the `typedef` alias `node` isn't ready yet.

That solves defining a node. Getting *inside* one you already have a pointer to needs new syntax too. You already know two operators for going inside a struct: the dot (`.`) for a plain struct variable, and dereferencing with `*` for a pointer. Combining them, `(*n).number`, works, but it's clumsy to type and read. So C gives you a shortcut:

> "Wonderfully today we're going to see that you can actually in some cases combine the dot and the asterisk into a single operator with two characters that literally looks like an arrow." (David Malan)

`n->number` means exactly `(*n).number`: follow the pointer `n`, then reach inside for the `number` field. `n->next` means the same for the `next` field. This is the **arrow operator**, and from here on it's how you'll do essentially everything with nodes.

> 🔑 **The single most important takeaway of this part.** A node is just a struct with a value and a pointer to the next node of its own type. The `struct node *next;` line (not `node *next;`) exists purely because the compiler hasn't finished reading the `typedef` yet when it reaches that line, and `n->field` is shorthand for "follow the pointer `n`, then reach inside."

---

## Part 2: Building a list by prepending (the pointer picture, step by step)

With the struct defined, an empty linked list needs exactly one variable: a single pointer that will hold the address of the first node, whenever one exists. If there are no nodes yet, that pointer is `NULL`.

```text
list
 |
 v
NULL
```

```c
node *list = NULL;
```

Now suppose the user types in `1`, `2`, and `3`, one at a time, and each one gets added to the *front* of the list, a strategy called **prepending**. For each number, the recipe is the same four steps:

1. `malloc` enough memory for one whole node, and check the result isn't `NULL`.
2. Store the user's number in the new node's `number` field.
3. Stitch the new node onto the existing list.
4. Update `list` to point at this new node.

Here's the code for one pass through that recipe:

```c
node *n = malloc(sizeof(node));
if (n == NULL)
{
    return 1;
}
n->number = number;
n->next = list;
list = n;
```

Walk through it in pictures. First, `n` points at a freshly `malloc`'d, still-garbage chunk of memory:

```text
list --> NULL

n --> [ number: ? | next: ? ]     (garbage values, nothing assigned yet)
```

After `n->number = number;` (say the user typed `1`) and, defensively, `n->next = NULL;`:

```text
list --> NULL

n --> [ number: 1 | next: NULL ]
```

Now for the two lines that actually attach this node to the list. Here is the exact wrong order, so you can see *why* order matters:

```text
WRONG ORDER:  list = n;  then  n->next = list;

list --> [ number: 1 | next: --+
                                |
                                v
n --> [ number: 1 | next: -----+     <-- n->next now points at ITSELF. Disaster.
```

That specific example is degenerate (there's only one node), so the real danger shows up on the *second* insertion, once `list` already points somewhere. Suppose `list` currently points at the node holding `1`, and you're prepending `2`:

```text
BEFORE:  list --> [ 1 | next: NULL ]

n --> [ 2 | next: NULL ]      (just malloc'd, not yet linked to anything)
```

If you carelessly do `list = n;` **first**:

```text
list --> [ 2 | next: NULL ]

        [ 1 | next: NULL ]     <-- ORPHANED. Nothing in your program points here anymore.
                                   This is a memory leak, permanently, until the program quits.
```

Malan catches himself making exactly this mistake live, and names it precisely:

> "I have orphaned the first node because now nothing in my code is actually pointing at it. I've got a duplication (two pointers pointing at this chunk of memory) so this thing... we have lost track of it in code, which means that is the definition of a memory leak." (David Malan)

The fix is to do the two lines in the **opposite order**: point the new node at the old list *before* you move `list` to point at the new node:

```text
STEP A:  n->next = list;

n --> [ 2 | next: ---+
                       |
                       v
list ---------------> [ 1 | next: NULL ]

STEP B:  list = n;

list --> [ 2 | next: ---> [ 1 | next: NULL ] ]
```

Nothing was lost: `list` now points at the new node, and the new node's `next` still points at everything that came before. Malan's own metaphor for this is worth keeping:

> "The metaphor I often think of is like around Christmas time... when people would stitch popcorn together... You're trying to stitch together these nodes or popcorn kernels, if you will, such that one can lead you to the next, can lead you to the next, but you can never let go of part of that strand." (David Malan)

Repeat the recipe for `3`, and the full list (after inserting `1`, then `2`, then `3`, always at the front) looks like this:

```text
list --> [ 3 ] --> [ 2 ] --> [ 1 ] --> NULL
```

Notice the order: it's the **reverse** of the order you typed the numbers in, because every new value jumps straight to the front. That's a direct, visible consequence of prepending, not a bug, and it's exactly the wrinkle Part 5 will fix.

> ✅ **What to do about it:** whenever you prepend, always set the new node's `next` to point at the current list *before* you move `list` to point at the new node. Reverse that order even once, and you permanently orphan everything the list used to hold.

---

## Part 3: Traversing the list (a `while` loop, and the equivalent `for` loop)

Building the list is only useful if you can read it back out. To do that without disturbing `list` itself (you still need it to find the list again later), use a second, throwaway pointer that walks along the chain:

```text
list --> [ 3 ] --> [ 2 ] --> [ 1 ] --> NULL

ptr = list;   (ptr now points at the same first node as list, without touching list)
```

The traversal logic in plain language: look at wherever `ptr` currently points, print its number, then move `ptr` to whatever *that* node's `next` field says. Repeat until `ptr` becomes `NULL`.

```c
node *ptr = list;
while (ptr != NULL)
{
    printf("%i\n", ptr->number);
    ptr = ptr->next;
}
```

Step by step, in pictures:

```text
ptr --> [ 3 ] --> [ 2 ] --> [ 1 ] --> NULL      print 3;  ptr = ptr->next;
         ptr --> [ 2 ] --> [ 1 ] --> NULL       print 2;  ptr = ptr->next;
                  ptr --> [ 1 ] --> NULL        print 1;  ptr = ptr->next;
                           ptr --> NULL         loop condition fails; stop.
```

This prints `3`, `2`, `1`, reversed from input order, exactly as Part 2 predicted.

Everything a `while` loop can do here, a `for` loop can do too, just packed onto one line. Malan shows the equivalent version:

```c
for (node *ptr = list; ptr != NULL; ptr = ptr->next)
{
    printf("%i\n", ptr->number);
}
```

The three parts of the `for` line map directly onto the `while` version: "start `ptr` at `list`" is the initializer, "keep going while `ptr` isn't `NULL`" is the condition, and "advance to the next node" is the update, it's just the `ptr = ptr->next;` line moved into the loop header instead of sitting as the last line inside the braces. Malan's own preference:

> "This is a little more elegant, in that you can express a whole lot of logic in one line of the `for` loop. Frankly, I do think the first version is nonetheless more readable." (David Malan)

Either form is correct; use whichever reads more clearly to you.

> 🔑 **The single most important takeaway of this part.** Never traverse a list with the `list` pointer itself: always copy it into a temporary pointer first (`ptr`), and advance *that*. The moment you overwrite `list`, you've lost your only way back to the front of the list.

---

## Part 4: Running time (why prepend is free but almost everything else isn't)

Now the payoff question: what does all this pointer-stitching actually cost, in Big O terms?

**Prepending is O(1).** Adding a new node to the front touches a small, fixed number of pointers (`n->next = list; list = n;`) no matter whether the list has 3 nodes or 3 million. The length of the rest of the list never enters into the work at all.

Everything else is worse, and the reasons are all the same shape: with no way to jump directly to a position, you have to walk there one node at a time.

| Operation | Running time | Why |
|---|---|---|
| **Prepend** (add to the front, no ordering) | **O(1)** | A fixed number of pointer reassignments: the list's length never matters. |
| **Append** (add to the back, with no tail pointer) | O(n) | You must follow `next` from the front until you find the node whose `next` is `NULL`, then attach there. |
| **Search** for a value | O(n) | Worst case, the value is the very last node, or isn't in the list at all, so you may have to check every node. |
| **Delete** a value | O(n) | Same as search: you must first walk to find it (and, since this is a *singly* linked list, the node *before* it too) before you can unlink it. |

Malan's own summary of the trade, once he's walked through search and delete: with arrays, a **sorted** array at least gives you binary search in O(log n): jump to the middle, then the middle of what's left, and so on. A linked list can't do that trick, sorted or not, because you cannot compute the address of "the middle node" the way you can with an array's contiguous arithmetic: you can only get there by walking, one `next` at a time, from the front. So the dynamism you gained (grow forever, no copying) comes at the cost of the search speed you had with a sorted array.

> 💡 **A nuance worth sitting with:** "O(1)" for prepend doesn't mean "instant": it means "the *same* small number of steps regardless of size." That's the entire reason prepending is the cheap operation and everything that requires finding a specific spot is not.

---

## Part 5: Sorted insertion (four cases, and why order comes out right this time)

Prepending is fast, but it leaves values in reverse-insertion order, not sorted order, and a real Contacts app or phone book needs its entries sorted. So instead of always inserting at the front, you now have to figure out, for every new value, exactly *where* in the list it belongs. Malan breaks the seemingly complicated problem into four separate, much smaller ones:

> "You've got scenarios in which you want to insert a new node into an empty list. You want to prepend the new node into the beginning of the list, append it to the end of the list, or somewhere in the middle." (David Malan)

**Case 1: the list is empty.** Trivial: just point `list` at the new node.

```c
if (list == NULL)
{
    list = n;
}
```

**Case 2: the new value belongs before everything currently in the list.** This is exactly the prepend logic from Part 2: point the new node's `next` at the current list, then move `list` to the new node.

```c
else if (n->number < list->number)
{
    n->next = list;
    list = n;
}
```

**Case 3: the new value belongs at the end.** Traverse with a pointer until you find a node whose `next` is `NULL` (that's the last node), then attach the new node there.

```c
for (node *ptr = list; ptr != NULL; ptr = ptr->next)
{
    if (ptr->next == NULL)
    {
        ptr->next = n;
        break;
    }
    ...
}
```

**Case 4: the new value belongs somewhere in the middle.** This is the fiddliest case, because you need *two* pointers at once: one on the node just before where the new value belongs, and one on the node just after. Suppose the list already holds `2 -> 4 -> NULL` and you're inserting `3`:

```text
BEFORE:      list --> [ 2 ] --> [ 4 ] --> NULL
                        ^          ^
                      trail       ptr

n --> [ 3 | next: NULL ]     (freshly malloc'd)

STEP 1:  n->next = ptr;        n --> [ 3 ] --> [ 4 ] --> NULL

STEP 2:  trail->next = n;      list --> [ 2 ] --> [ 3 ] --> [ 4 ] --> NULL
```

The order of those two steps matters exactly like it did in Part 2: you must point the *new* node forward, at `ptr`, before you point the *previous* node, `trail`, at the new node, otherwise you'd overwrite `trail->next` before you'd captured where it used to point, and orphan everything after it.

Running time-wise, this is worse news than plain prepending. Even though cases 1 and 2 are still instant, cases 3 and 4 require traversing to find the right spot first, so **sorted insertion, worst case, is O(n)**, same as search and delete. You traded away the one operation (unsorted prepend) that used to be free, in exchange for the list always coming out in order.

> ✅ **What to do about it:** before writing any insert code, ask which of the four cases you're in (empty, belongs first, belongs last, or belongs in the middle) and handle each with its own small block of code, in that order, rather than trying to write one clever line that covers all four at once.

---

## Part 6: Freeing the list (the `unload` function)

A linked list never leaks memory on its own just because you stop using it: you have to explicitly give every single node back. Malan is blunt about why you can't shortcut this:

> "It's not quite as simple as just saying free the whole list. Free is not that smart. [Malloc] is not that smart, and even though you have called [malloc] 123 times, you have to really call free. You have to call free 123 times." (David Malan)

In other words: `malloc` and `free` have no built-in concept of "linked list." Each call to `malloc` handed you back the address of one chunk of memory, and `free` only knows how to release exactly the address you hand it, one chunk at a time. Passing it your `list` pointer and hoping it "figures out" the rest of the chain does nothing of the sort.

The tricky part is that once you `free` a node, you can no longer safely read its `next` field: that memory isn't yours anymore. So you must save `next` in a temporary variable *before* freeing the node it came from:

```c
node *ptr = list;
while (ptr != NULL)
{
    node *next = ptr->next;   // remember where to go BEFORE destroying this node
    free(ptr);                // now safe to free this one
    ptr = next;                // move to the node we remembered
}
```

Pictorially, freeing `3 -> 2 -> 1 -> NULL`:

```text
ptr --> [ 3 ] --> [ 2 ] --> [ 1 ] --> NULL

1. next = ptr->next     (remember [2] before destroying [3])
2. free(ptr)             (destroy [3])
3. ptr = next            (move to [2]) ... repeat until ptr == NULL
```

This exact pattern (traverse, free, advance) is worth wrapping in its own function, `unload`, so you can call it once at the end of `main` (or anywhere else you need to discard a whole list) instead of copying this loop around by hand.

> 🔑 **The single most important takeaway of this part.** Every `malloc` needs its own matching `free`: a linked list has no shortcut for that. Always capture `ptr->next` into a temporary variable *before* you `free(ptr)`, or you'll be reading memory you no longer own.

---

## Key takeaways

1. **A node is a self-referential struct.** One value field, one `struct node *next` pointer, and the internal tag name (`struct node`) exists purely so the struct can name its own type before the `typedef` finishes.
2. **`n->field` is shorthand for `(*n).field`.** Follow the pointer, then reach inside.
3. **Prepend order matters.** Always set `n->next = list;` *before* `list = n;`. Reversing that order orphans the rest of the list, permanently.
4. **Prepend is O(1); almost everything else is O(n).** Search, delete, append (with no tail pointer), and even sorted insertion (worst case) all require walking the list one node at a time: the price paid for never having to copy the whole structure to grow it.
5. **Sorted insertion is four small problems, not one big one.** Empty list, belongs first, belongs last, belongs in the middle: handle each separately.
6. **Nothing frees itself.** `malloc` and `free` have no idea what a linked list is; you must traverse and `free` every node individually, saving `next` before you free the node it came from.

## Common pitfalls

- ❌ Writing `list = n;` before `n->next = list;` when prepending: this orphans every node the list used to hold, instantly and permanently (a memory leak you can't recover from at runtime).
- ❌ Traversing with the `list` pointer itself instead of a temporary `ptr`: the moment you advance `list`, you've lost your only way back to the front of the list.
- ❌ Forgetting that plain prepending stores values in *reverse* insertion order: if you need sorted order, you need the four-case sorted insert from Part 5, not plain prepending.
- ❌ Calling `free(list)` once and expecting the whole list to vanish: `free` only knows about the one address you hand it; every node needs its own call.
- ❌ Freeing a node and then reading its `next` field afterward: always save `ptr->next` into a temporary variable *before* you `free(ptr)`.

---

## 🛠️ Capstone Project: `numbers.c` (Prepend It, Sort It, Free It Clean)

> This is the main hands-on project for the lesson. You'll build a linked list of numbers on cs50.dev from scratch, watch it come out backwards on purpose, fix that by upgrading to sorted insertion, and then prove with Valgrind that every single node you allocated also got freed.

### What you will build

A single C program, `numbers.c`, on cs50.dev that:

- Defines a self-referential `struct node` (an `int` plus a `next` pointer).
- Reads integers from the user one at a time and builds a linked list by **prepending**.
- Prints the list with a `while` loop, then again with the equivalent `for` loop.
- Gets upgraded to insert every new number in **sorted order**, using the four cases from Part 5.
- Ends by calling an `unload` function that frees every node, verified leak-free with Valgrind.

This is, in miniature, exactly the kind of structure a real database engine or web framework builds and tears down for you invisibly whenever your program later queries and releases rows, the database-backed web app that caps this course. Building it by hand once, here, is what lets you actually understand (and debug) what's happening underneath when that magic occasionally breaks.

### Why this is the perfect practice

| Lesson idea | Where you use it in `numbers.c` |
|---|---|
| Self-referential `struct node` and the arrow operator (Part 1) | Your `struct node` definition and every `n->field` access. |
| Prepending, and the correct pointer order (Part 2) | Your first working version of the program. |
| Traversal with `while` and `for` (Part 3) | Your two printing loops. |
| Big O of each operation (Part 4) | A comment above each function stating its running time and why. |
| The four cases of sorted insertion (Part 5) | Your upgraded `insert` function. |
| The `unload` function (Part 6) | Your cleanup code at the end of `main`. |

### Milestones (build them in order, each one works on its own)

1. **Struct and an empty list.** Define your self-referential `struct node` (remember the internal tag name) and, in `main`, declare `node *list = NULL;`. Compile and run it. It should do nothing and crash nothing. That's a working, if boring, milestone.
2. **Prepend from user input.** In a loop, use `get_int` to read numbers until the user enters `-1` as a sentinel value. For each number: `malloc` a node, check for `NULL`, set its `number`, then stitch it onto the front of `list` in the correct order (`n->next = list;` before `list = n;`).
3. **Print it two ways.** Print the list with a `while` loop and a temporary pointer, then comment that version out and print it again with the equivalent `for` loop. Confirm both print identical output, in reverse order from how you typed the numbers in.
4. **Annotate the running time.** Add a one-line comment above your prepend loop and above your print loop stating each one's Big O and why (`O(1)` because it never touches the rest of the list; `O(n)` because it must visit every node).
5. **Upgrade to sorted insertion.** Replace your prepend-only logic with the four-case `insert` function from Part 5 (empty, belongs first, belongs last, belongs in the middle). Feed in the numbers out of order (say, `5 1 9 3 -1`) and confirm they print out sorted (`1 3 5 9`) regardless of the order you typed them.
6. **Write `unload` and prove zero leaks.** Write `void unload(node *list)` using the save-`next`-then-`free` pattern from Part 6, call it once at the end of `main`, then compile and run under `valgrind ./numbers`. Keep fixing your code until Valgrind reports "All heap blocks were freed -- no leaks are possible."
7. **Stretch goals.** (a) Add a `delete(int number)` function that removes a single value from anywhere in the list, handling "it's the first node" as its own case (since removing it means updating `list` itself, not just some node's `next`). (b) Rewrite the struct as a doubly linked list (add a `prev` pointer) and note in a comment which of today's four insertion cases actually get simpler as a result.

### How you will know you are done

- ✅ `make numbers` compiles with no warnings.
- ✅ Entering numbers out of order (e.g., `5 1 9 3`) prints them in sorted order after your Part 5 upgrade.
- ✅ `valgrind ./numbers` reports zero errors and zero leaked bytes after your `unload` function runs.
- ✅ You can point to the exact lines in your `insert` function that handle each of the four cases, and state out loud why sorted insertion is O(n) even though plain prepending was O(1).

> 💡 **Keep yourself honest:** run Valgrind after milestone 2, not just at the very end. A leak introduced while you're still prepending is far easier to spot and fix than one buried three milestones later under your sorted-insert logic.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Prepend five hardcoded numbers (foundational)
Skip user input entirely. In `main`, prepend the numbers `10, 20, 30, 40, 50` (in that order, using hardcoded values instead of `get_int`) onto a linked list, then print it with a `while` loop. Confirm the printed order is `50, 40, 30, 20, 10`, the reverse of how you inserted them, and explain in one sentence why.

### Exercise 2: Write and time-trace a `search` function (intermediate)
Write `bool search(node *list, int number)` that traverses the list and returns `true` if `number` is found, `false` otherwise. Build a 5-node list, then call `search` for a value you know is in the last node and count, by hand, exactly how many nodes your function visits before it returns. Confirm that number matches your expectation for O(n) worst-case behavior.

### Exercise 3: Delete a node from the middle (advanced)
Write `node *delete(node *list, int number)` that removes the node containing `number` from anywhere in the list and returns the (possibly updated) `list` pointer. Handle three cases explicitly: the value is in the first node (you must update `list` itself), the value is somewhere later (you need a trailing pointer to relink around the node you're removing), and the value isn't in the list at all (return the list unchanged). Don't forget to `free` the node you remove.

---

## Cheat sheet

```text
SELF-REFERENTIAL STRUCT
  typedef struct node
  {
      int number;
      struct node *next;   // "struct node", not "node" -- typedef isn't finished yet
  }
  node;

ARROW OPERATOR
  n->number   ==   (*n).number     "follow the pointer, then reach inside"

PREPEND (always in this order!)
  n->next = list;   // 1. point the NEW node at the OLD list
  list = n;         // 2. THEN move list to point at the new node
  (swap that order and you orphan everything list used to point to)

TRAVERSAL
  while:  node *ptr = list; while (ptr != NULL) { ...; ptr = ptr->next; }
  for:    for (node *ptr = list; ptr != NULL; ptr = ptr->next) { ... }

RUNNING TIMES (singly linked list)
  Prepend                        O(1)
  Append (no tail pointer)       O(n)
  Search                         O(n)
  Delete                         O(n)
  Sorted insert (4 cases)        O(n) worst case (cases 1-2 instant, 3-4 need a traversal)
  (a sorted ARRAY gets O(log n) search via binary search -- a linked list never can)

SORTED INSERT: 4 CASES
  1. Empty list        -> list = n;
  2. Belongs first      -> n->next = list; list = n;
  3. Belongs last        -> walk until ptr->next == NULL, then ptr->next = n;
  4. Belongs in middle    -> n->next = ptr; trail->next = n;   (in that order)

UNLOAD (free every node)
  node *ptr = list;
  while (ptr != NULL)
  {
      node *next = ptr->next;   // save BEFORE freeing
      free(ptr);
      ptr = next;
  }
```

## How this connects to the rest of the course

- **Earlier, Module 6 · Lesson 21:** "Stacks, queues, and resizable arrays" solved arrays' fixed-size problem with `realloc`-and-copy. This lesson solves the same growth problem a completely different way: one new node at a time, stitched in with a pointer, with nothing ever needing to be copied.
- **Earlier, Module 5 · Lessons 18-19:** the pointer fundamentals and `malloc`/`free` discipline from those lessons are what every line of code in this lesson actually leans on: a linked list is pointers and dynamic memory, applied deliberately.
- **Next, Module 6 · Lesson 23:** "Trees, hash tables, and tries" builds a hash table that is, quite literally, an array whose slots each hold their own linked list, so that when two different keys collide at the same array index, they chain together using exactly the node-and-`next` structure you built in this lesson.
- **Later, the course's north-star project:** the database-backed web app you build at the end of this course will store rows and query results using structures descended from exactly this idea: a linked list is the simplest version of "data plus the pointers that let you find more of it" that you'll ever build by hand.

---

*Source: "CS50x 2026 - Lecture 5 - Data Structures" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
