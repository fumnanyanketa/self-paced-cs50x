# Module 3 · Lesson 12: Command-Line Arguments and a First Cipher

> **Course:** Self-Paced CS50x
> **Module 3:** Debugging and what the compiler hides: debug systematically and see how C really stores data
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 2 - Arrays](https://www.youtube.com/watch?v=h5Gc1n8ZuU8) · [full transcript](../../transcripts/04-lecture-2-arrays.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

You'll learn the real, two-parameter shape of `main`, use the words typed after your program's own name to make it interactive and to report an honest success-or-failure exit code, then put both skills to work building your first cipher: a program that scrambles a message with a secret shift key you supply on the command line, one that anyone patient enough to try all 26 possibilities could crack in seconds.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** called *Encrypt & Crack*, where you build `encrypt.c` (a program
> that reads a shift key from the command line and scrambles a message you
> type) and then crack a secret message of your own by trying every possible
> key. Everything before the Capstone teaches the skills you will use there.
> If you want to see the finish line first, jump to the **"Capstone Project"**
> section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** C's exact syntax for `main`, and
> the shape of a terminal prompt, will keep changing over your career. The
> shift cipher you'll implement will not. It is nearly 2,100 years old.
>
> - **[Suetonius, *The Lives of the Twelve Caesars*](https://www.gutenberg.org/ebooks/6400) ("The Deified Julius"), c. 121 CE.** Suetonius's biography of Julius Caesar records, in translation: "if there was occasion for secrecy, he wrote in cyphers; that is, he used the alphabet in such a manner, that not a single word could be made out. The way to decipher those epistles was to substitute the fourth for the first letter, as d for a, and so for the other letters respectively." That is a shift of three places: the exact algorithm, and even the exact kind of key, you will implement in code in this lesson's Capstone.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Command-line argument:** an extra word you type after a program's name when you run it (the `3` in `./encrypt 3`), which the program can read and react to.
- **argc:** short for "argument count," a number telling your program exactly how many words were typed at the prompt, including the program's own name.
- **argv:** short for "argument vector," a numbered list (an array) holding every one of those typed words as text, with the program's own name always sitting at position 0.
- **Exit status:** a number a program hands back when it finishes, by convention `0` for "everything worked" and any other number for a specific kind of failure.
- **Plaintext:** the original, readable message before it's been scrambled: the thing you actually want to say.
- **Ciphertext:** the scrambled version of a message, unreadable to anyone without the secret needed to unscramble it.
- **Caesar cipher:** a way of scrambling text by shifting every letter forward in the alphabet by the same fixed number of places (the "key"), wrapping back to A after Z.
- **Brute force:** solving a problem by trying every single possibility instead of being clever about it: slow if there are many possibilities, fast if there are only a few (like the 26 possible Caesar keys).

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 11 pulled back the curtain on how C actually stores a string: a null-terminated array of characters. This lesson spends that knowledge two ways: first, to finally reveal why `main` has been quietly hiding a second, more powerful form since week one, one that lets your program react to words typed at the prompt instead of only ones typed while it's running. Second, to open the lecture's real closing act (cryptography) because, as Malan puts it while introducing it, this is "the art of scrambling information so as to have secure communication. So important nowadays with passwords and credit card numbers and personal messages that you might want to send." Command-line arguments and a first cipher look like two unrelated tricks, but your Capstone fuses them: a program that reads a secret key straight off the command line and uses it to scramble (and unscramble) real text. That same instinct (never trust input, validate it before you use it) is one you'll need again in Module 8, when this course's north-star database-backed web app has to defend itself against SQL injection.

## Learning objectives

By the end of this lesson you will be able to:

1. Write `main`'s full two-parameter signature, `int main(int argc, string argv[])`, and explain what `argc` and `argv` contain, including why `argv[0]` always holds the program's own name.
2. Validate the number of command-line arguments *before* reading them, and explain why "check `argc` first, use `argv` second" prevents a whole class of crashes.
3. Return a meaningful exit status from `main` (`0` for success, a nonzero value for a specific failure) and read it back from the shell with `echo $?`.
4. Explain the difference between plaintext and ciphertext, and encrypt or decrypt a short message by hand using a Caesar shift key.
5. Explain why brute-forcing a Caesar cipher (or ROT13) is fast enough to be trivial, and connect that weakness to why the course will need much stronger cryptography later on.

## Prerequisites

- **Module 3 · Lesson 11: Arrays and strings under the hood:** you should already know that a string is really an array of `char`s ending in the null character `\0`, since `argv` is, quite literally, an array of strings.
- **Module 2:** comfortable writing a `for` loop, calling `get_string`, and using `%s`/`%c` with `printf`.

---

## Part 1: What `main` actually looks like (`argc` and `argv`)

Every program you've written so far has started with `int main(void)`. It turns out that was never the whole story: just the simpler of two supported forms. As Malan explains:

> "[main] is special insofar as in C, it is the function that will be called automatically after you've compiled and then run your code." (David Malan)

The `void` inside the parentheses is not decoration. It's a claim:

> "void in parenthesis here just means that [main] ... does not take command line arguments." (David Malan)

Every program you've written up to now (`hello`, `scores`, `uppercase`) has had `void` in that spot, and you've never typed an extra word after running any of them. But C supports a second, richer signature:

```c
int main(int argc, string argv[])
```

> "it just means that [main] can take zero arguments or it can take 2. If it takes 2, the first is an integer and the second is an array of strings." (David Malan)

Those two parameters have conventional names, and Malan is explicit about what each one means:

> "By convention those inputs are called [argc] and [argv]. [argc] is the count of arguments that are typed after the program's name. [argv] is the argument vector, AKA array of actual words." (David Malan)

Concretely:

- **`argc`** is a plain `int`: the total number of words at the prompt, *including the program's own name*.
- **`argv`** is an array of strings: one slot per word, in the order they were typed. Because arrays start counting at 0, `argv[0]` is the program's name, `argv[1]` is the first real argument, `argv[2]` the second, and so on.

Malan demonstrates by rewriting a small `greet.c`, first with the familiar `get_string`, then with `argc`/`argv` instead:

```c
#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[])
{
    printf("hello, %s\n", argv[1]);
}
```

Building this live surfaced a real bug worth knowing about:

| # | What changed | What happened | The fix |
|---|---|---|---|
| 1 | Swapped `void` for `int argc, string argv[]`, but had earlier deleted `#include <cs50.h>` | `use of undeclared identifier 'string'` | Put the include back. As Malan explains: "I should have kept the CS 50 library because it's in the CS 50 library that string is defined." `string` is CS50's own alias for a real C type: only `cs50.h` knows about it. |
| 2 | Ran `./greet` with no word typed after it | prints `hello, null` | Not a compiler bug. `argv[1]` simply doesn't exist when nobody typed a second word, so `printf` prints CS50's stand-in for "nothing here." This is the cue to *check first, print second*. |

That second row is the real lesson. Reading `argv[1]` when the user typed nothing is undefined territory you should never rely on. The fix is to check `argc` before ever touching `argv[1]`:

```c
if (argc == 2)
{
    printf("hello, %s\n", argv[1]);
}
else
{
    printf("hello, world\n");
}
```

Now typing extra, unwanted words is caught too, not just zero words:

> "if I don't quite cooperate and I say David Malan, enter, it similarly just ignores me because [argc] is not 2 anymore. It's now 3." (David Malan)

And that first slot, `argv[0]`, is never empty. It always holds the program's own name, no matter what you called the file:

> "you can use [argv][0], which will always contain the program's name no matter what the file has been named or renamed to." (David Malan)

Command-line arguments aren't only ever a single bare word, either. `cowsay` (a decades-old novelty program that prints an ASCII-art animal saying whatever you type) takes a whole a menu of them:

> "[cowsay] is a program that allows you to type in a word after the prompt like moo, and it will print out what's called [ASCII] Art, an adorable little cow with a speech bubble that says moo." (David Malan)

Running `cowsay -f dragon "hello"` passes *three* words after the program's name (`-f`, `dragon`, and `hello`): `argc` would be 4, and `argv[1]` through `argv[3]` would hold each one. Malan is candid that this demo is just for fun ("no academic value here. It's just fun to play with command line arguments sometimes") but it makes a real point: any word after a program's name, flag or otherwise, ends up in `argv`.

> 🔑 **The single most important takeaway of this part.** `argc` tells you how many words are safe to read from `argv`; always check it *before* you index into `argv`, not after. `argv[0]` is always the program's name; real arguments start at `argv[1]`.

---

## Part 2: Exit status (telling the world whether it worked)

Every program you've written has started with `int main`, not `void main`, and you've never once written a `return` statement that mattered, because until now it didn't need to. That `int` is a promise: `main` hands a number back when it finishes.

> "Technically, the value that [main] returns is going to be called a so-called exit status, which is a numeric status that indicates success or failure." (David Malan)

Numeric codes for "something happened" are everywhere: a confusing Zoom error like `1132` means nothing to a normal user, and on the web, "you're familiar with this number 404... this generally means file not found." An exit status works the same way, just smaller in scope: it's a message from your program to whatever ran it (the shell, or another program), and by strong convention:

> "By convention, a program, a function like main returns 0 on success if all is well." (David Malan)

Any other value signals a specific kind of failure: you decide what each number means, as long as you're consistent. Here's Malan's `status.c`, which returns different codes depending on whether the user cooperated:

```c
#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Missing command line argument\n");
        return 1;
    }
    printf("hello, %s\n", argv[1]);
    return 0;
}
```

The exit status isn't printed on screen. It's semi-secret, but the shell will show it to you if you ask right after running the program, with `echo $?`:

```text
$ ./status David
hello, David
$ echo $?
0

$ ./status
Missing command line argument
$ echo $?
1
```

This isn't a classroom-only curiosity. It's exactly how CS50's own grading tool works:

> "if you've ever wondered how Check 50 knows if your code was correct or not, among the ways we check for that is by checking the semi-secret status code, this exit status." (David Malan)

> ✅ **What to do about it:** validate `argc` first, and `return` a nonzero status immediately on bad input: before any of the "real" logic of your program runs. Reserve `0` exclusively for the path where everything actually succeeded.

---

## Part 3: A first cipher (plaintext, ciphertext, and the Caesar shift)

The lecture's closing topic is cryptography: scrambling a message so it's unreadable to anyone who intercepts it, but recoverable by the person it's meant for. Every scheme in this space shares the same shape:

```text
plaintext  --[ cipher, run with a shared secret key ]-->  ciphertext
ciphertext --[ same cipher, key reversed            ]-->  plaintext
```

**Plaintext** is the human-readable original: "the human readable version in English or any other language." **Ciphertext** is what comes out the other side, and turning one into the other needs more than just an algorithm:

> "you can't just give it plain text and run it through an algorithm and get ciphertext because you need to somehow have a secret typically for encryption to work." (David Malan)

The simplest such secret is a **shift key**: pick a number, and slide every letter of the alphabet forward by that many places, wrapping back to `A` after `Z`. Shift `HIM` by a key of 1, and every letter just moves one place later (`H`→`I`, `I`→`J`, `M`→`N`) giving the ciphertext `IJN`. Decryption reverses the exact same move: subtract the key instead of adding it. This is historically known as the **Caesar cipher**, because it is, quite literally, the scheme Julius Caesar used to write confidential letters, as Suetonius records above.

A famous specific key is 13, which shifts the alphabet exactly halfway around:

> "if you use 13 instead, you wouldn't get IJ, you'd get UV because [U] and V are 13 places away from H and I respectively." (David Malan)

This particular shift has its own name, **ROT13** ("rotate 13"), and a niche but genuine real-world use:

> "[ROT13] is an algorithm that's been used for many years online just to sort of avoid spoilers, like Reddit might do this or other websites where they want you to have to do some effort to see what the message says." (David Malan)

Push the key all the way to 26, though, and you get nothing at all, since every letter shifts exactly back onto itself:

> "It literally rotates all the way around. A becomes A, B becomes B." (David Malan)

That last observation is really about *security*, not arithmetic. A Caesar cipher only has 26 possible keys, and one of them (26, or 0) does nothing. That means an eavesdropper doesn't need to be clever, just patient:

> "they just try all possibilities (key of 1, key of 2, key of 3 ... 25) and at some point [they'll] see clearly that they guessed the key, which means that cipher is not very secure." (David Malan)

Trying every possible key until one produces readable text is called a **brute-force** attack, and it's exactly the vulnerability that makes the Caesar cipher a teaching tool rather than something you'd trust with an actual secret today: a computer (or even a patient human with a pencil) can try all 25 useful keys in well under a second.

Malan actually closes the lecture by doing this decryption live, in front of the class, on a message that had been shifted by a key of 1:

> "if we rotate all the letters in the opposite direction by subtracting one, [that] will be our final letters for today." (David Malan)

Letter by letter, the ciphertext resolves into plain English, Malan's actual sign-off for the lecture:

> "this was CS 50. We'll see you next time." (David Malan)

Notice how the three ideas from this lesson stack into one build: your Capstone's `encrypt.c` reads its shift key from `argv[1]` (Part 1), validates `argc` and returns a proper exit status for bad input (Part 2), and then does exactly this character-by-character shifting arithmetic on a message you type (Part 3).

> 🔑 **The single most important takeaway of this part.** A cipher's security lives entirely in the secrecy (and the size) of its key space. A Caesar cipher's key space is just 26 numbers, which is small enough to brute-force instantly; real cryptography (later in this course) is built to make that number astronomically larger.

---

## Key takeaways

1. **`main` has two legal shapes.** `int main(void)` takes no command-line arguments; `int main(int argc, string argv[])` takes as many words as the user cares to type after the program's name.
2. **`argc` counts, `argv` holds.** `argc` is the total word count (program name included); `argv` is the array of those words as text, with `argv[0]` always the program's own name and real arguments starting at `argv[1]`.
3. **Check `argc` before you touch `argv`.** Reading `argv[1]` when it doesn't exist is exactly the kind of bug that doesn't show up until a user runs your program the "wrong" way.
4. **Exit status is your program's honest signal.** `0` means success by strong convention; any other number means a specific failure you define, and `echo $?` (and tools like `check50`) can read it right back.
5. **A cipher's strength lives in its key space, not its cleverness.** The Caesar cipher's 26 possible keys make it brute-forceable almost instantly: a limitation this course will spend real time solving properly.

## Common pitfalls

- ❌ Reading `argv[1]` (or `argv[2]`, etc.) before checking that `argc` is large enough: this reads memory that was never given to your program and produces garbage or a crash, not a clean error.
- ❌ Forgetting `#include <cs50.h>` after switching `main`'s signature to use `string argv[]`: `string` is CS50's alias, not a built-in C keyword, and the compiler will say so with "undeclared identifier."
- ❌ Returning `0` out of habit even on the failure path, or forgetting to `return` at all: an exit status only means something if `0` is reserved exclusively for real success.
- ❌ Assuming a Caesar cipher (or ROT13) hides anything from a determined reader: with only 26 keys to try, brute force cracks it in a fraction of a second.
- ❌ Forgetting that C's `%` (remainder) operator can return a negative number for a negative left-hand side: shifting by a negative key without correcting for this gives array-index-style math that looks wrong until you add 26 back in.

---

## 🛠️ Capstone Project: Encrypt & Crack (A Caesar Cipher on the Command Line)

> This is the main hands-on project for the lesson. You'll build a real command-line encryption tool, then turn around and attack your own cipher the way an eavesdropper would: by trying every possible key until English falls out.

### What you will build

Two small programs on cs50.dev. `encrypt.c` reads a shift key from the command line, reads a plaintext message interactively, and prints the Caesar-shifted ciphertext, returning a proper exit status throughout. Then, without being told the key, you'll crack a ciphertext by brute force: writing a program that tries all 26 possibilities and shows you every candidate so you can spot the real message by eye.

### Why this is the perfect practice

| Lesson idea | Where you use it in Encrypt & Crack |
|---|---|
| `argc` / `argv` (Part 1) | Reading the shift key straight from the command line as `argv[1]`, instead of asking for it with `get_int`. |
| Exit status (Part 2) | `return 1` with a usage message on bad input; `return 0` on success; checked with `echo $?`. |
| Caesar shift + brute force (Part 3) | The character-shifting math inside `encrypt.c`, and trying all 26 keys automatically instead of being told the answer. |

### Milestones (build them in order, each one works on its own)

1. **Set up and validate `argc`.** Create `encrypt.c` with `#include <cs50.h>` and `#include <stdio.h>`, and give `main` the real signature `int main(int argc, string argv[])`. Before anything else, check `if (argc != 2)`, print a usage message, and `return 1`. Run `make encrypt` then `./encrypt` (no key) and confirm you see the usage message; run `echo $?` and confirm you see `1`.
2. **Turn the key into a usable number.** Add `#include <stdlib.h>` and convert `argv[1]` with `atoi`. Reduce it with `% 26`, and if the result is negative, add 26 back so any integer key (even a negative or oversized one) behaves like a proper Caesar key. Temporarily `printf` the adjusted key to confirm `./encrypt 29` and `./encrypt 3` produce the same key.
3. **Shift a message and print the ciphertext.** Add `#include <ctype.h>` and `#include <string.h>`. Call `string plaintext = get_string("plaintext: ");`, loop over every character with `strlen(plaintext)`, and shift uppercase and lowercase letters separately by the key (wrapping with `% 26`); print every other character (spaces, digits, punctuation) unchanged. Confirm `./encrypt 3` turns `hello` into `khoor`.
4. **Prove decryption is just encryption with the opposite key, then return 0.** Encrypt a message with some key `k`, then feed the resulting ciphertext back into `./encrypt` using key `26 - k`, and confirm you get your original message back exactly. Make sure the success path ends with `return 0;`, and confirm with `echo $?`.
5. **Crack a secret by brute force: no key given.** Without being told the key, decrypt this intercepted message: `VHH BRX LQ PRGXOH 4`. Write a short `crack.c` that loops a candidate `key` from 0 through 25, decrypts the message with each one, and prints every candidate labeled with its key number, so you can read down the list and spot the one written in plain English by eye.
6. **Stretch goals.** (a) Make `crack.c` score each candidate automatically instead of relying on your eyes: for example, counting how many two- and three-letter English words (`THE`, `AND`, `YOU`) appear in each candidate. (b) Handle ciphertext typed in mixed case. (c) Reject a key argument that isn't a valid whole number instead of silently treating it as `0`.

Here is a working reference implementation of `encrypt.c`. Code snippets in this course are illustrative reconstructions, so build your own version step by step rather than copying this directly:

```c
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./encrypt key\n");
        return 1;
    }

    int key = atoi(argv[1]) % 26;
    if (key < 0)
    {
        key += 26;
    }

    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char c = plaintext[i];
        if (isupper(c))
        {
            printf("%c", (c - 'A' + key) % 26 + 'A');
        }
        else if (islower(c))
        {
            printf("%c", (c - 'a' + key) % 26 + 'a');
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");
    return 0;
}
```

### How you will know you are done

- ✅ `./encrypt` with no key (or with two keys) prints a usage message and exits with status `1`, confirmed with `echo $?`.
- ✅ `./encrypt 3` followed by typing `hello` prints `khoor`, and exits with status `0`.
- ✅ Encrypting a message with key `k`, then encrypting the result with key `26 - k`, returns your original message.
- ✅ Your brute-force `crack.c` prints all 26 candidates for `VHH BRX LQ PRGXOH 4`, and you can point to the one key (there's exactly one) that reads as plain English.

> 💡 **Keep yourself honest:** once you've spotted the correct key by eye, don't go back and hardcode it into `crack.c`. The whole point is that the program tries all 26 keys itself: proving the cipher is breakable by brute force, not that you already knew the answer.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Shift it by hand (foundational)
Without writing any code, Caesar-shift the word `COMPUTER` by a key of 7, one letter at a time, on paper. Some letters will need to wrap around past `Z` back to `A` (for example, `T` shifted by 7 wraps around). Write out your final ciphertext, then double check a couple of the trickiest wrap-around letters against the alphabet.

### Exercise 2: A single-key ROT13 (intermediate)
Write a small standalone program, `rot13.c`, that always uses a key of exactly 13: no command-line argument needed at all, just `get_string` and `printf`. This is a smaller version of `encrypt.c`'s core loop, useful for getting the character-shifting math right before you also have to handle a variable key from `argv`.

### Exercise 3: Negative keys (advanced)
Extend your `encrypt.c` to correctly handle a negative shift key typed at the command line, such as `./encrypt -3`. Confirm that `./encrypt -3` on some ciphertext produces the same result as `./encrypt 23` on that same ciphertext (since shifting back by 3 is the same as shifting forward by 23). This exercises the `% 26` "add 26 if negative" logic from Capstone Milestone 2 in a case where it's easy to get wrong.

---

## Cheat sheet

```text
MAIN'S TWO SIGNATURES
  int main(void)                     no command-line arguments
  int main(int argc, string argv[])  argc = word count (name included)
                                      argv = array of those words, argv[0] = program's own name

RULE: check argc BEFORE reading argv[1], argv[2], ...

EXIT STATUS
  return 0;   -> success (the convention)
  return 1;   -> a specific failure (you define what each nonzero code means)
  $ echo $?   -> shows the exit status of the last command you ran

CAESAR CIPHER
  encrypt:  (letter - base + key) % 26 + base       base = 'A' or 'a'
  decrypt:  (letter - base - key + 26) % 26 + base   (+26 keeps it non-negative)
  ROT13  = shift key of 13 (its own inverse: shift twice, you're back where you started)
  ROT26  = shift key of 26 = no-op (A -> A, B -> B, ...)
  key space = 26 possibilities -> brute-forceable near-instantly, hence NOT secure
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 11 (Arrays and strings under the hood):** knowing that a string is an array of `char`s terminated by `\0` is exactly what makes `argv` (an array of strings) make sense, and is what your `for` loop over `strlen(plaintext)` relies on here.
- **Next, Module 4 · Lesson 13 (Thinking in running time: Big O):** trying all 26 keys in `crack.c` is your first taste of "just try everything": Lesson 13 gives that instinct a name and a way to measure how badly it scales when the number of possibilities isn't a friendly 26.
- **Later, Module 8 · Lesson 31 (SQL injection):** the discipline you practiced here (validate `argc` before you trust `argv`, never assume user input is safe to use as-is) returns in force when the north-star web app has to defend a real database against malicious input.

---

*Source: "CS50x 2026 - Lecture 2 - Arrays" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK. Quotes are taken verbatim from the lecture's auto-generated transcript; bracketed words like [main], [argc], [argv], [cowsay], [ASCII], and [ROT13] silently correct that transcript's phonetic mis-hearings of these technical terms (e.g., "Ma"/"Maine" for "main," "RC"/"RV" for "argc"/"argv") without altering the substance of what was said.*
