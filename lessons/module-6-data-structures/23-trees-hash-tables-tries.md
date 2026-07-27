# Module 6 · Lesson 23: Trees, Hash Tables, and Tries

> **Course:** Self-Paced CS50x
> **Module 6:** Data structures: trade speed for memory deliberately
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 5 - Data Structures](https://www.youtube.com/watch?v=PmAI76OGE_E) · [full transcript](../../transcripts/07-lecture-5-data-structures.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

Arrays give you speed (binary search) but not flexibility, and linked lists give you flexibility but not speed, so this lesson mashes the two together into three new shapes: the binary search tree, the hash table, and the trie, each one buying back some speed by deliberately spending more memory, and the whole skill is choosing the right one for the problem in front of you.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a tiny hash table in C (26 buckets by first letter, chaining every collision with the linked lists you built in Lesson 22), insert a dozen names, look three of them up, and literally count how many comparisons that costs you versus a plain list. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** C, Python, and every language after them will keep changing; the mathematics of these three data structures will not. For the timeless, tool-agnostic account:
>
> - **[*Introduction to Algorithms*](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) by Cormen, Leiserson, Rivest, and Stein** (MIT Press). Known in the field simply as "CLRS," this is the standard reference textbook that formally treats binary search trees and hash tables as general algorithmic structures, independent of any one programming language. What Malan draws on a whiteboard here, CLRS proves with mathematics.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Node:** a single unit of a data structure that holds a piece of data plus one or more pointers to other nodes. You built these for linked lists in Lesson 22; every structure in this lesson is a variation on the same idea.
- **Tree:** a data structure built from nodes where each node can point to more than one other node (its "children"), unlike a linked list, where each node points to just one "next" node. This is why a tree is called **two-dimensional**: it can branch, not just extend in a line.
- **Binary search tree (BST):** a tree where every node has at most two children, and every value is greater than everything in its left child's branch and less than everything in its right child's branch.
- **Hash function:** a bit of code that takes an input (like a name) and always returns the same small number for it (like which of 26 buckets it belongs in). It is how you turn an unlimited number of possible inputs into a fixed, small set of "buckets."
- **Hash table:** an array of buckets, where a hash function decides which bucket a given piece of data belongs in. Each bucket is commonly implemented as a linked list, so more than one item can live in the same bucket.
- **Collision:** when a hash function sends two different inputs to the same bucket. Collisions are not a bug: they are an unavoidable consequence of mapping an unlimited number of possible inputs onto a small, fixed number of buckets.
- **Chaining:** the standard fix for collisions: instead of overwriting whatever is already in a bucket, you link the new item onto the existing ones with a linked list, so nothing is ever lost.
- **Trie** (pronounced "try," short for re**trie**val): a tree where each node is an array of pointers, one slot per possible next letter, so that a word is spelled out one node per letter instead of being stored as one chunk of data.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

By the end of Lesson 22 you had a working linked list, and you had also just hit a wall: everything about it (searching, inserting in order, deleting) was Big O of n. You'd freed yourself from the array's fixed size, but as Malan puts it, plainly:

> "We can now grow and shrink things without wasting time copying, but we've lost hold of our binary search, and that was very appealing as far back as week zero when we wanted to do something quite quickly." (David Malan)

This lesson is the answer to that loss. You'll see three different ways computer scientists have mashed arrays and linked lists together to get some of the array's speed back without giving up the linked list's flexibility to grow, and you'll see, honestly, what each of those three approaches costs you in memory. This is also where the course's running theme lands most concretely: every one of these structures is a real, calculated trade of memory for speed, and picking correctly among them is a skill you'll use for the rest of this course, right up through choosing a database index for your final project.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why arrays and linked lists each fail to give you both fast search and easy growth, using their Big O running times.
2. Write and trace a recursive binary search tree lookup by hand, state its O(log n) running time and roughly 3x memory cost versus an array, and explain how an unlucky insertion order degenerates a BST into a linked list.
3. Explain how a hash function maps an unlimited set of inputs onto a fixed set of buckets, build a hash table as an array of linked lists, and explain the trade-off between collision rate and the extra memory a longer hash key costs.
4. Explain why a trie achieves true O(1) lookup and why that speed costs heavy memory waste, and choose among a BST, a hash table, and a trie for a given problem based on its time-vs-memory trade-off.

## Prerequisites

- **Module 6 · Lesson 21: Stacks, queues, and resizable arrays**: the array-backed struct and the cost of growing an array with `malloc`/`realloc`, which this lesson uses as the baseline for comparison.
- **Module 6 · Lesson 22: Linked lists**: `struct node`, the `->` operator, and building/traversing a singly linked list. This lesson's hash table buckets *are* that linked list, reused directly.
- **Module 4 · Lesson 16: Recursion and merge sort**: the base-case/recursive-case pattern. The recursive BST search in Part 2 is that exact pattern, applied to a tree instead of an array.

---

## Part 1: Recap: why neither an array nor a linked list is enough

Before the new material, it's worth pinning down exactly what you're stuck with at the end of Lesson 22, because everything in this lesson exists to fix it.

| Operation | Sorted array | Linked list (Lesson 22's build) |
|---|---|---|
| Search | O(log n): binary search | O(n): no way to jump to the middle |
| Insert (in sorted position) | O(n): may need to shift/copy | O(n): must walk to the right spot |
| Delete | O(n): may need to shift/copy | O(n): must walk to find it |
| Growing the structure | O(n): copy every element into new, bigger memory | O(1): allocate one new node, no copying |

The array's whole appeal was that its values sit back-to-back in memory, so you can do simple arithmetic (divide by 2, divide by 2 again) to jump straight to the middle. That is exactly what makes binary search possible, and binary search is O(log n): fast even for huge data sets. The catch, which you lived through in Lesson 21, is that arrays are stuck at a fixed size the moment you compile your code; growing one means asking for a new, bigger block of memory and copying everything over.

The linked list solves the growing problem beautifully: one new node, a couple of pointers updated, done, no copying. But you pay for that dynamism with exactly the property that made binary search possible in the first place. As Malan explains it:

> "We can now grow and shrink things without wasting time copying, but we've lost hold of our binary search, and that was very appealing as far back as week zero when we wanted to do something quite quickly." (David Malan)

Why can't you binary-search a linked list? Because to jump to "the middle," you first have to know how long the list is, and the only way to find that out is to walk the whole thing, one node at a time, following pointer after pointer. There's no arithmetic shortcut when your values aren't sitting at predictable addresses next to each other.

> 🔑 **The single most important takeaway of this part.** Arrays are fast to search but expensive to grow; linked lists are cheap to grow but slow to search. Every data structure in the rest of this lesson exists to buy back some of that lost speed, and every one of them will cost you memory to do it.

---

## Part 2: Binary search trees: getting binary search back, recursively

If an array is one-dimensional (values sitting in a single row) and a linked list is essentially the same (values chained in a single sequence, wherever they happen to sit in memory), a **tree** adds a second dimension. Instead of a node pointing to just one "next" node, each node can point to two "children", and that second dimension is exactly what lets you binary-search a structure that can still grow one node at a time.

Take the sorted array `1 2 3 4 5 6 7`. Its binary-search midpoints are 4 (the middle), then 2 and 6 (the middles of the halves), then 1, 3, 5, 7 (the leftover leaves). A **binary search tree** stores those exact same seven values, but explodes them into two dimensions instead of one row:

```text
              4
            /   \
           2     6
          / \   / \
         1   3 5   7
```

The node at the very top is called the **root**. The nodes at the bottom with no children (1, 3, 5, 7) are called **leaves**, vocabulary borrowed, as Malan notes, from real trees. Every node here follows one rule: everything in its left branch is smaller than it, and everything in its right branch is bigger than it. In Malan's words:

> "Every element is going to be greater than its left child and less than its right child, assuming you don't have identical values, and that property is actually a recursive one." (David Malan)

That word *recursive* is doing real work. The BST property doesn't just describe the root's relationship to its two children: it's true of every single node and its own two children, all the way down. That's exactly the kind of self-similar structure Lesson 16 taught you to write recursive functions for, and it makes searching a BST a natural fit for the base-case/recursive-case pattern:

```c
typedef struct node
{
    int number;
    struct node *left;
    struct node *right;
}
node;

bool search(int number, node *tree)
{
    // Base case: an empty (sub)tree can't contain the number
    if (tree == NULL)
    {
        return false;
    }
    // Recursive case: the number is smaller, so it can only be in the left subtree
    else if (number < tree->number)
    {
        return search(number, tree->left);
    }
    // Recursive case: the number is bigger, so it can only be in the right subtree
    else if (number > tree->number)
    {
        return search(number, tree->right);
    }
    // Found it
    else
    {
        return true;
    }
}
```

Trace it by hand for `search(5, tree)` on the picture above: 5 > 4, so you recurse right to the subtree rooted at 6; 5 < 6, so you recurse left to the subtree rooted at 5; 5 == 5, return `true`. Three steps, for seven elements, and every additional level the tree grows only adds one more step, which is exactly what O(log n) means.

### The 3x memory cost

This speed is not free. Compare the node you built for a linked list (one value, one pointer) to the node above (one value, *two* pointers). Malan is explicit about the price:

> "I'm literally using 3 times as much memory now because even though it's not depicted here explicitly, each of these squares represents an integer and a pointer and another pointer, so that's like 16, that's like 20 bytes at this point of memory instead of just 4 bytes for each of the integers in an array." (David Malan)

An array spends 4 bytes per integer. A singly linked list roughly doubles that (value plus one pointer). A BST roughly triples it (value plus two pointers). Nowadays, as Malan notes, memory is comparatively cheap, but "roughly triples it" stops being a rounding error once you're storing millions of items, not seven.

### The unbalanced trap

Here's the catch that makes a BST trickier than the tidy picture above suggests: the shape you get depends entirely on the *order* you insert values in. Insert 2, then 1, then 3, and you get the balanced little tree above. But insert 1, then 2, then 3, then 4, always inserting the next-bigger value, and every new node has nowhere to go but to the right of the last one:

```text
1
 \
  2
   \
    3
     \
      4
```

That still obeys the BST rule (everything to the right is bigger), but Malan names exactly what it has become:

> "A link list which is like bad for all the reasons we discussed before the break because even though we're getting the dynamism, it's devolving into big O of N." (David Malan)

A BST's O(log n) search only holds if the tree stays roughly **balanced**: root near the middle of the values, branches of similar depth on both sides. Fed values in an unlucky (often sorted) order, an ordinary BST degenerates into a straight line: a linked list wearing a tree's name, with all the same O(n) problems from Part 1. (More advanced trees fix this by actively rebalancing themselves on every insert, out of scope for this lesson, but worth knowing the fix exists.)

> ✅ **What to do about it:** before you trust a BST's O(log n) claim for a real problem, ask what order the data actually arrives in. Random or shuffled insertion order tends to stay balanced; already-sorted or adversarial insertion order can degenerate it into O(n).

Even with that caveat, a balanced BST gets you real binary search back on a structure that still grows one node at a time: no copying, no fixed size. But it costs 3x the memory of an array, and it's still only O(log n), not the fastest thing theoretically possible. As Malan frames the ambition:

> "The holy grail of data structures is to achieve something that is big O of 1, like constant time." (David Malan)

That's the target for the rest of this lesson.

---

## Part 3: Hashing and hash tables: bucketizing infinity

To get to constant time, you need a new building block: **hashing**. Malan defines it by borrowing straight from high-school math:

> "So from high school math class, domain is the input, range is the output. So an infinite domain to a finite range is the goal here of hashing." (David Malan)

In plain terms: there is no upper limit on how many different names, words, or values could theoretically exist (an infinite domain), but you want to sort them into a small, fixed number of buckets (a finite range). The bit of code that decides which bucket a given input belongs in is called a **hash function**. The simplest possible hash function for names uses just the first letter (26 letters, 26 buckets):

> "If I pass in Mario to a hash function implemented in C or some other language, I would like to get back to the number 12 because M is the 13th letter of the alphabet." (David Malan)

(Bucket 12, not 13, because the buckets are an array indexed from 0.) In C, that hash function is almost embarrassingly short:

```c
#include <ctype.h>

unsigned int hash(const char *name)
{
    // toupper handles lowercase input; subtracting 'A' turns 'A'..'Z' into 0..25
    return toupper(name[0]) - 'A';
}
```

Now pair that hash function with an array of 26 buckets, where each bucket is a linked list (the exact linked list you built in Lesson 22):

```text
index (bucket)     chain (linked list, one node per name in that bucket)
  0  (A)  -> NULL
  ...
 11  (L)  -> Luigi -> Link -> NULL
 12  (M)  -> Mario -> NULL
  ...
 15  (P)  -> Peach -> NULL
  ...
 25  (Z)  -> Zelda -> NULL
```

This whole array-of-linked-lists structure is a **hash table**. Malan doesn't undersell how useful it is:

Malan calls hash tables "sort of the Swiss Army knives of data structures, the kind of thing that some computer scientists have been quoted as saying if they were stuck on a desert island with only one data structure, this is probably the one they would want."

### Collisions and chaining

Notice bucket 11 above holds *two* names: Luigi and Link both start with L. That's called a **collision**, and Malan is upfront that it's not a design flaw, it's math:

> "We're poised to have what we're going to call collisions, which is a downside of using a hash function. If you're going from something infinite to something finite, by definition you're going to have a heck of a lot of potential collisions." (David Malan)

The fix is **chaining**: instead of overwriting Luigi's slot when Link arrives, you prepend Link onto a linked list rooted at bucket 11, the same prepend operation from Lesson 22. Nothing gets clobbered; you just get a (hopefully short) linked list per bucket instead of one giant linked list for everybody.

### The trade-off: longer hash keys, fewer collisions, way more memory

You could shrink collisions further by hashing on more than one letter, say, the first three letters, giving each name a much more specific bucket. Fewer names sharing a bucket means shorter chains, which means faster lookups. But Malan is direct about the cost:

> "We're wasting a huge amount of space to reduce the probability of collision... but at what cost? Well, a heck of a lot more memory." (David Malan)

26 buckets (one letter) is cheap and still has plenty of collisions. 26³ = 17,576 buckets (three letters) has far fewer collisions, but the overwhelming majority of those buckets (`AAA`, `AAB`, `ZZQ`, and so on) will sit empty forever, because almost no real name starts that way. That's memory spent for speed you may not even need.

Even with chaining, a hash table's search time isn't *truly* constant. If n names are spread evenly across k buckets, each chain holds roughly n/k names, so search is O(n/k): dramatically faster in practice than a plain linked list's O(n), but asymptotically still O(n), because k is a fixed constant and Big O notation ignores constants. Faster, yes. The holy grail of true O(1), not quite yet.

---

## Part 4: Tries: true O(1), at a steep price

(One quick note before this part: the transcript's speech-to-text renders the term phonetically as "try." The correct written word is **trie**, pronounced the same way, and short for re*trie*val.)

There is one data structure in this lesson that actually reaches constant time. Malan introduces it like this:

> "There are tries in the world which weirdly is short for retrieval, even though we don't say retrieval." (David Malan)

A trie is a tree made of arrays. Every node is an array of 26 pointers, one slot per letter of the alphabet, and a word is spelled out one node, one letter, at a time, instead of being stored as a single chunk of data anywhere. To insert "toad," you follow (or create) the T slot at the root, then the O slot inside that node, then the A slot, then the D slot, and mark that final D node with a flag meaning "a word ends here":

```text
root:      [A][B]...[T]...[Z]     (array of 26 pointers)
                      |
                      v
          T-node:  [A][B]...[O]...[Z]
                              |
                              v
              O-node:  [A]...[D]...[E]...[M]...[Z]
                                |       |      |
                                v       v      v
                          D-node*   E-node*  M-node*
                          (word ends here: "TOAD" / "TOE" / "TOM")
```

Notice how "toe" and "tom" share the exact same T and O nodes as "toad": they only branch apart at the third letter. Looking someone up means walking the same path: hash on the first letter, follow that pointer; hash on the second letter, follow that pointer; and so on, checking for the end-of-word flag as you go. Malan's punchline is exactly the property this whole lesson has been chasing:

> "It doesn't matter if there's 3 names in this trie or 3 million names in this trie, how many steps did it take me to confirm or deny that Toad is in this trie? ...which is arguably constant." (David Malan)

Four letters, four steps: no matter whether the trie holds a dozen names or a hundred thousand. The number of steps depends only on the *length of the word you're looking up*, never on how much data is already stored. That is genuine O(1): Malan calls it exactly what this whole lesson has been driving toward, "the holy grail of data structures."

### The price: massive memory waste

So why doesn't every program just use a trie? Because that speed is bought with an enormous amount of wasted space. Every single node, even ones on a path used by only one word, is a full array of 26 pointers, and almost every slot in almost every node is unused:

> "There's a huge amount of wasted memory just as we saw with the hash function... most of the pointers in those arrays are just null and unused, and it just tends to result in you're using way more memory to solve the problem correctly." (David Malan)

For a handful of Nintendo character names, that waste is trivial. For 100,000+ English words, which is exactly what this week's problem set hands you, a trie's memory footprint balloons dramatically, because every node reserves room for all 26 possible next letters even though any given word only ever uses one of them.

> ❌ **The trap:** assuming "fastest" always means "best." A trie gets you true O(1) lookup, but at a memory cost so steep that CS50's own spell-checker problem set asks you to build a hash table instead: the Swiss Army knife, not the specialist tool.

---

## Part 5: Choosing among them: a real shelf, and what's next

Put the three structures from this lesson side by side against the array and linked list from before, and the whole lesson is really one table:

| Data structure | Typical search | Memory per item (roughly) | Can degrade to |
|---|---|---|---|
| Sorted array | O(log n) | 1x (baseline) | None (but O(n) to grow) |
| Linked list | O(n) | ~2x (value + 1 pointer) | already O(n) |
| Balanced BST | O(log n) | ~3x (value + 2 pointers) | O(n) if unbalanced |
| Hash table (chained) | ~O(n/k), asymptotically O(n) | modest (array of pointers + chains) | O(n) if all items collide |
| Trie | O(1): bounded by key length, not n | very high (mostly unused pointers) | never: it's already worst-case-proof |

This is not just a whiteboard exercise. Malan points out it's a real structure you've probably stood in front of:

> "...they hash your salad into a shelf like this." (David Malan)

He's describing the pickup shelf at Sweetgreen, a salad chain: your order gets filed under a bucket based on the first letter of your name, exactly like the hash table above.

> "This is the A through E bucket, the F through J bucket, the K through N bucket, and the O through Z bucket." (David Malan)

Notice that's not 26 buckets, it's 4: a coarser hash function (letter *ranges* instead of single letters) trading a higher collision rate for less physical shelf space, the exact same time-vs-memory knob from Part 3, just made out of wood instead of pointers.

That trade-off is precisely why this week's problem set doesn't have you build the fastest structure in this lesson. It has you build the most generally useful one:

> "The very last thing you'll do... this week is indeed implement your very own spell checker whereby we'll give you a very large file of all 100,000 plus English words. You'll have to come up with a clever and efficient way to load it up into memory." (David Malan)

A trie would technically look up each word faster, but at a memory cost that stops being reasonable at 100,000+ words. A hash table gets you most of the speed for a fraction of the memory, which is exactly why it, not the trie, is the tool CS50 asks you to build this week, and the tool you'll build in the Capstone below.

---

## Key takeaways

1. **Arrays are fast to search, slow to grow; linked lists are the reverse.** Every structure in this lesson exists to buy back some of the speed lost when you moved from arrays to linked lists.
2. **A binary search tree adds a second dimension.** Two child pointers per node let you binary-search a structure that still grows one node at a time: O(log n) search, at roughly 3x an array's memory per item.
3. **An unbalanced BST degenerates into a linked list.** The BST rule can still hold while the shape collapses into a straight line with O(n) search: the insertion order matters.
4. **A hash function maps infinite inputs onto finite buckets.** A hash table pairs that with an array of linked lists; collisions are inevitable and chaining is the fix, not a workaround for a bug.
5. **Longer hash keys trade memory for fewer collisions.** More buckets means shorter chains and faster lookups, but the overwhelming majority of those extra buckets sit empty.
6. **A trie achieves true O(1) lookup** (its running time depends on the length of the key, not on how much data is stored) by spending a full array of pointers per letter, most of them unused.
7. **There is no single "best" data structure.** The right choice always depends on which resource, time or memory, you can least afford to spend on this particular problem.

## Common pitfalls

- ❌ Assuming a BST is always O(log n) just because "trees are fast." Check the insertion order; sorted or adversarial input can degenerate it into a linked list.
- ❌ Treating a hash collision as a bug to eliminate rather than a normal outcome to handle with chaining.
- ❌ Reaching for a longer, more specific hash key (more letters, more buckets) without weighing the memory it costs: most of those extra buckets will sit empty.
- ❌ Assuming "fastest asymptotically" (a trie's O(1)) automatically means "best for this problem": it isn't, once memory is scarce or the data set is huge.
- ❌ Forgetting that a hash table's search is still technically O(n) in the worst case (everything collides into one bucket): a good hash function, not the data structure alone, is what keeps chains short in practice.

---

## 🛠️ Capstone Project: Build Your Own Sweetgreen Shelf

> This is the main hands-on project for the lesson. You'll build the exact structure Malan describes at Sweetgreen (an array of 26 buckets, each one a linked list, chaining every collision), insert a dozen real names, look three of them up, and count comparisons to prove to yourself, in numbers, that a hash table beats a plain linked list. This same idea, a structure that finds things faster than walking a list one by one, is what your database's indexes will be doing for you when you build your final project's database in Module 8; there, the "buckets" are a balanced tree instead of an array, but the goal is identical: don't check every row to find the one you want.

### What you will build

A single C program, `hashtable.c`, run on cs50.dev. It defines a `node` (a name plus a `next` pointer, exactly like Lesson 22's linked list), an array `table[26]` of 26 `node *` buckets, a `hash` function, an `insert` function that chains onto a bucket, and a `search` function that counts how many name-comparisons it needs before it finds (or fails to find) a name. You'll build a second, un-hashed linked list of the same dozen names purely to compare against.

| Lesson idea | Where you use it in this Capstone |
|---|---|
| Node + `->` (Lesson 22) | Every bucket is that exact linked-list node, reused as-is. |
| Hash function (Part 3) | `hash()` turns a name into a bucket index 0-25. |
| Chaining (Part 3) | `insert()` prepends onto whichever bucket's chain the name hashes to. |
| Big O of search (Parts 1 & 3) | Your comparison-counter turns "O(n) vs O(n/26)" from theory into an actual printed number. |

### Milestones (build them in order, each one works on its own)

1. **Set up the skeleton.** On cs50.dev, create `hashtable.c` with `#include <cs50.h>`, `#include <stdio.h>`, `#include <stdlib.h>`, and `#include <ctype.h>`. Define `typedef struct node { char name[26]; struct node *next; } node;` and, in `main`, declare `node *table[26] = {NULL};` (26 empty buckets). Compile it: an empty program that builds cleanly is a real milestone.
2. **Write the hash function.** Add `unsigned int hash(const char *name) { return toupper(name[0]) - 'A'; }`. Print `hash("Mario")` and `hash("Luigi")` to confirm you get 12 and 11.
3. **Write insert, and load a dozen names.** Write `void insert(node *table[], const char *name)` that `malloc`s a new node, copies the name into it with `strcpy`, points its `next` at whatever `table[hash(name)]` currently is, then updates `table[hash(name)]` to the new node (the exact prepend pattern from Lesson 22). Call it a dozen times with a mix of real first names, including at least three that share a first letter on purpose (so you're guaranteed at least one real collision).
4. **Write search with a comparison counter, and look three up.** Write `bool search(node *table[], const char *name, int *comparisons)` that walks the chain at `table[hash(name)]`, incrementing `*comparisons` each time it checks a node's name, and returns `true`/`false`. Call it for three names: one that's the only name in its bucket, one that shares a bucket with others, and one that isn't in the table at all, and print each one's comparison count.
5. **Build a plain list for comparison.** Separately, prepend the same dozen names onto one single linked list (ignore hashing entirely, everything goes on one chain). Reuse the same counting-`search` logic (walking one list instead of indexing into 26) to look up the same three names, and print those comparison counts side by side with step 4's.
6. **Stretch goals.** (a) Switch the hash function to use the first *two* letters (52² buckets is impractical by hand, try a small fixed scheme like `first-letter * 26 + second-letter` capped sensibly) and see your worst collision shrink or vanish; note how many bytes the bigger table array costs versus 26 pointers. (b) Sketch (in comments, no need to fully implement) what the same dozen names would look like stored in a trie instead, and compare its total pointer count to your hash table's.

### How you will know you are done

- ✅ `hashtable.c` compiles and runs with no warnings, inserting all twelve names without a crash or a leak (spot-check with `valgrind` if you want to be sure).
- ✅ Your program prints the comparison count for all three looked-up names from the hash table, and the same three names from the plain linked list, side by side.
- ✅ At least one of your three lookups involved a real collision (a bucket with more than one name in it), and you can point to exactly where chaining kept it correct.
- ✅ You can state, in your own words, why the hash table's comparison counts were lower, and explain what would happen to that advantage if all twelve names happened to start with the same letter.

> 💡 **Keep yourself honest:** don't hand-wave the plain-list comparison: actually build and run it. The whole point of this Capstone is seeing the counted numbers differ, not just believing they should.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Balanced vs. degenerate, by hand (foundational)
On paper, insert the sequence `4, 2, 6, 1, 3, 5, 7` one at a time into an empty binary search tree (smaller goes left, bigger goes right), drawing the tree after each insertion. Then start over with the sequence `1, 2, 3, 4, 5, 6, 7` and do the same. Label each final tree's height and state its Big O search time. You should end up with one balanced tree (height ~3, O(log n)) and one degenerate one (height 7, O(n)), from the exact same seven values.

### Exercise 2: Count the recursive calls (intermediate)
Take the `search` function from Part 2 and add an `int *comparisons` parameter, incrementing it once per call before you check the base case. Run it against both trees you drew in Exercise 1, searching for the value `7` in each. Confirm the balanced tree takes noticeably fewer comparisons than the degenerate one, even though both are valid binary search trees over the same seven numbers.

### Exercise 3: First letter vs. first two letters (advanced)
Pick 15-20 real first names (reuse your Capstone list plus a few more). Hash all of them into a 26-bucket table using only the first letter, and separately into a table using the first *two* letters (26 × 26 = 676 possible buckets, though you only need to allocate the ones you actually use). For each table, count total collisions (an insert into a bucket that already holds at least one name) and the total number of bucket pointers your table declared (26 vs. 676). Report both numbers side by side: you should see collisions drop as declared buckets rise by roughly 26x, turning the abstract trade-off from Part 3 into two concrete numbers.

---

## Cheat sheet

```text
THE FIVE STRUCTURES, SIDE BY SIDE
  Sorted array   : O(log n) search / O(n) to grow      / 1x memory
  Linked list    : O(n) search      / O(1) to grow      / ~2x memory (value + 1 pointer)
  Balanced BST   : O(log n) search  / O(1)-ish to grow  / ~3x memory (value + 2 pointers)
                   -> WARNING: degenerates to O(n) if inserted in sorted/adversarial order
  Hash table     : ~O(n/k) search, asymptotically O(n) / modest memory (array + chains)
                   -> k = number of buckets; more buckets = fewer collisions = more memory
  Trie           : O(1) search (bounded by key length)  / heavy memory (mostly unused pointers)

BST RECURSIVE SEARCH (base case first, always)
  if tree == NULL:            return false
  elif number < tree->number: return search(number, tree->left)
  elif number > tree->number: return search(number, tree->right)
  else:                       return true

HASH TABLE = ARRAY + LINKED LISTS
  bucket index = hash(key)            e.g. hash(name) = toupper(name[0]) - 'A'
  collision     = two keys, same bucket index (inevitable, not a bug)
  chaining      = fix: prepend onto that bucket's linked list, never overwrite

TRIE = TREE OF 26-POINTER ARRAYS
  one node per LETTER, not per word; end-of-word marked with a boolean flag
  lookup steps = length of the word you're checking, NEVER the size of the data set

THE ONE QUESTION THAT PICKS AMONG THEM
  "Which can I afford to spend more of on this problem: time, or memory?"
```

## How this connects to the rest of the course

- **Earlier, Module 6 · Lesson 22 (Linked lists):** gave you the `struct node`, the `->` operator, and the prepend pattern this lesson reuses directly as a hash table's chained buckets, and Module 4 · Lesson 16 (Recursion and merge sort) gave you the base-case/recursive-case pattern the BST's `search` function is built from.
- **Next, Module 7 · Lesson 24 ("Why Python? Your first scripts"):** Python's built-in `dict` type is a hash table exactly like the one in this lesson's Capstone, except the hash function, the collision handling, and the resizing are all written for you, which is a big part of why Python code gets so much shorter starting next lesson.
- **Later, Module 8's lesson on indexes:** when you speed up a slow database query on your final project by adding an index, that index is commonly implemented as a balanced tree: the same shape as this lesson's BST, doing the exact same job of turning an O(n) row-by-row search into an O(log n) one, just at database scale instead of in a C array.

---

*Source: "CS50x 2026 - Lecture 5 - Data Structures" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
