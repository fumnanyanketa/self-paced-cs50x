# Module 5 · Lesson 17: Pixels, Hexadecimal, and Memory Addresses

> **Course:** Self-Paced CS50x
> **Module 5:** Memory: see the bytes (pointers, the heap, and files)
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 4 - Memory](https://www.youtube.com/watch?v=db0H0U13YsA) · [full transcript](../../transcripts/06-lecture-4-memory.txt)
> **Estimated time:** 45 minutes (read plus exercises)

---

## In one sentence

An image is just a grid of numbered dots, a color is just three of those numbers squeezed together, hexadecimal is nothing more than a compact way to write any number a computer uses, including colors and, as you'll see today for the first time, the actual address where one of your variables lives inside the computer.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** called *The Hex Fluency Drill*, where you convert numbers to and from hexadecimal by hand, decode real CSS colors into plain-language RGB, and write a small C program that prints your own variables' memory addresses. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk is recent, but the underlying idea is not.
>
> - **[Positional notation](https://en.wikipedia.org/wiki/Positional_notation)** (a mathematical idea dating back to Babylonian and Indian place-value systems). It's the one concept underneath everything in this lesson: any number system (binary, decimal, or hexadecimal) is the same trick of giving each digit's *position* its own weight (ones, sixteens, two-hundred-fifty-sixes…). Change how many digits you're allowed to use and you change the base; the way you read the columns never changes. Once you see that, hexadecimal stops being a special "computer thing" and becomes just one more base, the same way decimal and binary are.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Pixel:** one single colored (or, in this lesson's simplest example, just black-or-white) dot in the grid of dots that makes up a digital image.
- **Resolution:** how many pixels an image has, usually described as width × height (so many dots across, so many dots down).
- **RGB:** a way of building any color by mixing amounts (0-255 each) of red, green, and blue light. You met this in Module 1 · Lesson 2: nothing about it changes today, only how it's written.
- **Hexadecimal (hex, base 16):** a number system with 16 available digits (0 through 9, and then A through F standing in for 10 through 15) instead of decimal's 10 digits.
- **Place value:** the "weight" a digit's position gives it. In decimal, the columns are ones, tens, hundreds; in hexadecimal, the columns are ones, sixteens, two-hundred-fifty-sixes.
- **The `0x` prefix:** two characters written in front of a number to announce "everything after this is hexadecimal," so nobody mistakes `0x10` for the decimal number ten.
- **Memory address:** a number that names one specific byte-sized location inside a computer's memory, the same way a street address names one specific mailbox.
- **Format code:** the `%`-prefixed placeholder inside a `printf` string (like `%i`, `%s`, or `%p`) that tells `printf` how to interpret and display a value. `%p` specifically means "this value is a memory address: print it as one."

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In Module 1 · Lesson 2 you learned that a color is just three numbers (red, green, and blue, each from 0 to 255) and that an image is simply a grid of those numbers, called pixels. Nothing about that changes today. What changes is the *notation*: programmers almost never write those numbers the way you learned to in school. They write them in hexadecimal, and once you can read a diagram of a computer's memory in hex, you are exactly one small step away from asking the computer to show you where your own variables actually live. Malan introduces hexadecimal by deliberately lowering the stakes:

> "This doesn't add anything intellectually new. It's just an introduction to a common convention for how else we can represent numbers." (David Malan)

That framing is worth holding onto through the whole lesson. Hexadecimal is not a new idea. It is the same numbers you already know, spelled differently, for a very practical reason you'll see by the end: it takes exactly two hex digits to write one byte.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what resolution means and why a digital image is really just a grid of numbered pixels.
2. Read a 1-bit black-and-white image encoded directly as a grid of 0s and 1s.
3. Convert between an RGB color's decimal values and its 6-digit hexadecimal code (recognizing, for example, `000000`, `FFFFFF`, and `FF0000`).
4. Count in hexadecimal using place values of 1, 16, 256… and explain why two hex digits represent exactly one byte.
5. Recognize the `0x` prefix and explain the ambiguity it exists to prevent.
6. Print a variable's memory address in C using the `&` operator and the `%p` format code.

## Prerequisites

- **Module 1 · Lesson 2: Bits and Binary**: you should already be comfortable with bits, bytes, binary place value, and RGB as three decimal numbers from 0 to 255. This lesson revisits those exact same bytes in a new notation.
- **Module 2 · Lesson 6: Input, Variables, and the Command Line**: you should be able to declare a variable, call `printf` with a format code, and compile and run a program with `make` on cs50.dev.
- **Module 4 · Lesson 16: Recursion and Merge Sort** is the lesson immediately before this one in the course path, but nothing from it is required here: this lesson opens a new module and a new topic.

---

## Part 1: Images are just grids of numbered dots

Malan opens not with code but with art: two classmates built a picture out of Post-it notes, some green and some purple, arranged in a grid. Looked at from across the room, the grid resolves into a recognizable image, a cat, even though up close it is nothing but a pattern of two colors repeated over rows and columns. That is, quite literally, how a computer stores an image:

> "Even though this is fairly low resolution in that it only has a few pixels this way and a few pixels this way, it's actually representative of how computers do actually store images underneath the hood." (David Malan)

To show what happens at higher resolution, he zooms into a photograph of a bowl of stress balls sitting on the lectern. At first it looks like an ordinary photo. Zoom in further and you start to see more detail, but zoom in far enough and the detail runs out. You hit individual colored dots, and no further zooming reveals anything new. Those dots are **pixels**, and Malan defines the term that measures how many of them an image has:

> "By resolution I just mean how many dots go horizontally and how many dots go vertically, multiply those two together and you get some number of bytes, maybe in kilobytes, megabytes, or heck, if it's a massive image, it could be even bigger than that." (David Malan)

So an 8-dot-wide, 8-dot-tall image has a resolution of 8×8 = 64 pixels. A modern phone photo might be 4,000 dots wide and 3,000 dots tall: 12 million pixels, which is exactly where the term "12 megapixels" comes from. And:

> "Any image on a screen like this is represented by hundreds, thousands, millions of tiny little dots called pixels, and each of those pixels has a color that gives it collectively the appearance of stress balls in this case, or cats in this case." (David Malan)

> 🔑 **An image has no color of its own: it is a grid of numbered dots, and resolution is simply how many of those dots there are, width × height.** Everything else in this lesson is about how each dot's color gets written down as a number.

## Part 2: One bit per pixel (the smiley face hidden in 0s and 1s)

Before adding real color, Malan strips a pixel down to its simplest possible form: a single bit. He proposes a rule (any `0` in a grid is interpreted as black, any `1` as white) and shows a grid of 0s and 1s that, read that way, resolves into a smiley face:

> "Let me propose that in a picture like this, any zero will be interpreted as black, any 1 will be interpreted as white." (David Malan)

This is what's called a **1-bit image**: each pixel needs only a single bit, because there are only two possible colors to choose between. If you had a real file on your computer storing exactly this pattern of 0s and 1s, opening it in a photo viewer would show you precisely this grid, some dots white, some black, because the "color" of each pixel is nothing more than which bit is stored there.

Real images obviously need more than black and white. Malan is explicit that modern formats simply spend more bits per pixel to get there:

> "In modern times we would actually use 16 bits per color, 24 bits per color, maybe even more, and that's how we can get every color of the rainbow instead of just something black and white." (David Malan)

> 🔑 **Bit depth (bits per pixel) is what determines how many colors are possible.** One bit gives you exactly 2 colors. More bits per pixel means more possible colors, which is exactly the door that opens into Part 3, RGB.

## Part 3: RGB and the hexadecimal color code

Rewinding to the RGB you met in Module 1 · Lesson 2: a color is red, green, and blue, each from 0 to 255. Malan shows a screenshot of Photoshop's color picker, a professional photo-editing tool, to introduce the notation almost every image editor and web page actually uses for that same information: hexadecimal.

Black, in Photoshop's color picker, is typed as `000000`, which also reads as 0 red, 0 green, 0 blue. Malan describes choosing it this way:

> "I chose black by typing in 000000, which also... means that I want 0 red, 0 green, and 0 blue." (David Malan)

White works the same way, just at the opposite end of the range: `FFFFFF`, equivalently 255 red, 255 green, 255 blue. Recall from Part 4 that `FF` is the largest two-digit hex number there is, exactly 255 in decimal.

And the primary colors follow the same pattern, two hex digits per channel, in order red, green, blue:

> "If we wanted to represent something like Red, we're going to use FF 0000. If we want to represent green, we're going to use 00 FF 00. And lastly, to represent blue, we're going to use 0000 FF." (David Malan)

| Color | RGB (decimal) | Hex code |
|---|---|---|
| Black | 0, 0, 0 | `000000` |
| White | 255, 255, 255 | `FFFFFF` |
| Red | 255, 0, 0 | `FF0000` |
| Green | 0, 255, 0 | `00FF00` |
| Blue | 0, 0, 255 | `0000FF` |

Notice the pattern: every hex color code is exactly six hex digits (two for red, two for green, two for blue) written back to back with no punctuation between them. `FF0000` is not one mysterious number; it is the decimal number 255 (for red), then 0 (for green), then 0 (for blue), each just written as a two-digit hex pair instead of a plain decimal number.

> ✅ **What to do about it:** whenever you see a 6-digit hex color like `#2E8B57`, mentally split it into three 2-digit pairs (`2E`, `8B`, `57`) before you try to make sense of it: each pair is one RGB channel, and you'll convert those pairs to decimal in Part 4.

## Part 4: Hexadecimal itself (counting in base 16)

So why write 255 as `FF` instead of just `255`? To answer that, you have to actually learn to count in hexadecimal, the same way you already know how to count in binary.

Decimal (base 10) uses ten digits, 0 through 9. Binary (base 2) uses two, 0 and 1. Hexadecimal just picks a bigger number of digits, but decimal Arabic numerals run out after 9, so computer scientists borrowed letters:

> "We're sort of out of Arabic numerals here, but I could toss into the mix like A, B, C, D, E, and F either in lower case or uppercase. And in fact, that's what computer scientists do when they want to have... 16 digits available, and in fact when you want to use this many digits, you call it hexadecimal, implying that you've got 16 digits, aka base 16." (David Malan)

So the 16 hexadecimal digits, in order, are:

```text
0 1 2 3 4 5 6 7 8 9 A B C D E F
                    ↑  ↑  ↑  ↑  ↑  ↑
                   10 11 12 13 14 15
```

Just like decimal and binary, hexadecimal is read using **place value**. It's the exact same columns-and-weights idea you already use every day, just with a different set of weights:

> "Instead of using powers of 2 or powers of 10, we're going to today use powers of 16." (David Malan)

That means the columns, from right to left, are worth 1, 16, 256, 4096, and so on (16⁰, 16¹, 16², 16³ …), the same way decimal's columns are worth 1, 10, 100, 1000 (10⁰, 10¹, 10², 10³ …).

Counting through the first two hex digits looks like this:

```text
Hex:      00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 ...
Decimal:   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 ...
```

The interesting jump is right after `0F`. In decimal, running out of single digits means carrying a 1 and rolling back to 0: that happens after 9. In hexadecimal it happens after F (15), so `0F` is followed by `10`, and `10` in hexadecimal is **not** ten, it's sixteen, because it means (1 × 16) + (0 × 1) = 16.

This is exactly why two hex digits are so convenient: a single hex digit can represent any value from 0 through 15, which is exactly the range of 4 bits (a "nibble"). Put two hex digits side by side and you can represent 4 bits + 4 bits, a full byte, 0 through 255:

> "It turns out that it's just convenient to use two hexadecimal digits to represent numbers because a single hexadecimal digit can be used to represent 4 bits at once." (David Malan)

You can check this with the FF example from Part 3: F is 15, and 15 × 16 (the sixteens column) + 15 × 1 (the ones column) = 240 + 15 = 255, exactly the RGB maximum you'd expect for white or for a fully-saturated red, green, or blue channel.

Because hexadecimal is everywhere in computing but looks, at a glance, exactly like decimal, there's a real risk of ambiguity: if you see a label like `10` on a diagram with no other context, is that the 10th thing (decimal) or the 16th thing (hex)? To remove that ambiguity, programmers prefix every hexadecimal number with two characters, `0x`:

> "It's super common to literally prefix any number you ever write in hexadecimal notation using zero X... it just means what follows the 0x is a number in hexadecimal notation." (David Malan)

So `0x10` unambiguously means sixteen, never ten. From here on, any time you see `0x` in front of a number, read the rest of it in hex.

> 🔑 **Hexadecimal is not new information: it's a compact rewrite of numbers you already know, and two hex digits always represent exactly one byte (0-255).** The `0x` prefix exists purely to say "read what follows in base 16," nothing more.

## Part 5: A number even for memory (your first look at addresses.c)

Hexadecimal's usefulness doesn't stop at colors. Malan reintroduces the "canvas of memory" (the picture of a computer's memory as a long row of numbered bytes) and this time numbers those bytes in hex instead of decimal, for the exact same reason colors are written in hex:

> "We would actually number these from 0 on up through 9 and then keep going with A, B, C, D, E, F." (David Malan)

That means bytes 0 through 9 are numbered as you'd expect, and then the 10th through 15th bytes are `A` through `F`, followed by `10`, `11`, `12`, and so on, the identical counting pattern from Part 4, just applied to memory locations instead of colors.

Now, some real code. Malan writes a tiny program, `addresses.c`, that does nothing more exciting than declare a variable and print it:

```c
#include <stdio.h>

int main(void)
{
    int n = 50;
    printf("%i\n", n);
}
```

Running it prints `50`. Nothing new. But that `50` has to physically live *somewhere* inside the computer's memory the moment the program runs, at some specific location:

> "When I actually call printf and pass in n, clearly the computer is going to that location in memory and actually printing out that value, but that value is indeed at a specific memory address." (David Malan)

Up to now, you've never had a way to ask the computer *where*. Today you get one, in the form of a new operator: a single ampersand, `&`, placed directly in front of a variable's name.

> "The ampersand has a very simple straightforward one, which is to just get the address of a variable in memory. So if you've got a variable like n, if you prefix it with ampersand n, you can actually ask the computer at what address is this variable stored." (David Malan)

There's also a new format code to go with it. Because a memory address is technically a number but not one you'd ever want to do arithmetic on, it's conventional not to print it with `%i` (which is for ordinary integers). Instead, C gives you `%p` (short for "pointer"), a format code whose entire job is to print a value as a memory address:

```c
#include <stdio.h>

int main(void)
{
    int n = 50;
    printf("%p\n", &n);
}
```

Instead of `50`, this version prints something like `0x7fffd3c34ecc`, a long string of hexadecimal digits, prefixed with `0x` exactly as Part 4 predicted. Malan's own run of this program produced a similarly long hex address, and was quick to note the number itself is not the point:

> "It would be painful to do the mental math to figure out what the numeric address is, but we're seeing it indeed in this common hexadecimal notation, which is not going to be often useful for us as humans, but the computer is and has been using this information for some time." (David Malan)

Two things are worth holding onto here, and both are deliberately small for now:

- `&n` means "the address of `n`," not "the value of `n`." Swapping `n` for `&n` inside `printf` changes what question you're asking the computer.
- `%p` exists specifically so a `printf` call reads correctly: "print this as an address," the same way `%i` says "print this as an integer" and `%s` says "print this as a string."

You may have noticed Malan also mentions a second new symbol, the asterisk (`*`), used for something called *dereferencing*: actually following an address to the value stored there. This lesson stops on purpose before that: the next lesson, **Module 5 · Lesson 18: Pointers, and What Strings Really Are**, is entirely about what you can *do* once you can already read an address, including using `*` to go find what's stored at one.

### Putting it all together

Every idea in this lesson is the same raw material, bits, read through a different lens:

```text
bit (0 or 1)
  → byte (8 bits, 0-255)                    written in hex as 2 digits: 00-FF
     → RGB channel (one byte)               e.g. decimal 255 = hex FF
        → pixel (3 bytes: R, G, B)          e.g. (255,0,0) = FF0000 = red
           → image (a grid of pixels)       resolution = width × height
     → one numbered byte in memory          written in hex with a 0x prefix
        → a variable's address (&n)         e.g. 0x7fffd3c34ecc, printed with %p
```

Hexadecimal is the thread running through the whole diagram: the same base-16 counting from Part 4 is what makes a color code readable and what makes a memory address readable. Nothing about the underlying bytes changed all lesson: only the notation you now know how to read.

---

## Key takeaways

1. **An image is a grid of numbered pixels.** Resolution is just width × height: how many dots there are, not how big or beautiful the picture looks.
2. **Bit depth determines how many colors are possible.** A 1-bit image can only be two colors; modern images spend many more bits per pixel to get the full range of RGB.
3. **Hexadecimal is not new information.** It's the same RGB (or any other) numbers you already know, spelled with 16 digits instead of 10, in Malan's own words: it "doesn't add anything intellectually new."
4. **Hex place values are powers of 16** (1, 16, 256, 4096…), the same columns-and-weights idea as decimal and binary, just with a different base.
5. **Two hex digits always equal exactly one byte** (0 through 255, i.e. `00` through `FF`): that's the entire reason hex is convenient.
6. **The `0x` prefix removes ambiguity.** `0x10` is unambiguously sixteen; a bare `10` on a diagram could be either base.
7. **`&variable` gets an address, and `%p` prints one.** You now have a way to ask C exactly where one of your own variables lives in memory.

## Common pitfalls

- ❌ Reading `0x10` as "ten" out of habit. Fix: the `0x` prefix is your signal to switch your brain to base 16: `0x10` is sixteen.
- ❌ Assuming a pixel is always one byte. Fix: it depends entirely on bit depth: a 1-bit image spends 1 bit per pixel, while a full-color RGB image spends 3 bytes (24 bits) per pixel.
- ❌ Printing an address with `%i` instead of `%p`. Fix: `%i` is for integers you'd do arithmetic on; `%p` is specifically for memory addresses, and using the wrong format code is undefined behavior in C even if it happens to "look fine" once.
- ❌ Treating the specific digits of a printed address as meaningful or reproducible. Fix: the exact address your program prints will differ from run to run and from computer to computer: what matters is that it's a real, valid location, not its specific digits.
- ❌ Forgetting that F is worth 15, not "the 6th letter." Fix: anchor on the two endpoints (`0x0` is 0, `0xF` is 15) and count from there instead of re-deriving it each time.

---

## 🛠️ Capstone Project: The Hex Fluency Drill

> This is the main hands-on project for the lesson. You'll practice reading and writing hexadecimal by hand in the two contexts where you'll meet it constantly for the rest of this course, colors and memory addresses, then prove you can generate a real memory address yourself in C.

### What you will build

A short worked drill, done on paper or in a notes file plus one small C program on cs50.dev: a set of hand conversions between decimal and hexadecimal, a plain-language decode of five real CSS colors, and an `addresses.c` program that prints several of your own variables' values and their addresses.

### Why this is the perfect practice

| Lesson idea | Where you use it in the drill |
|---|---|
| Place value in base 16 (Part 4) | Milestone 1: hand conversions |
| RGB ↔ hex color codes (Part 3) | Milestone 2: decoding CSS colors |
| `&` and `%p` (Part 5) | Milestone 3: `addresses.c` |

### Milestones (build them in order, each one works on its own)

1. **Convert numbers by hand, both directions.** Without a calculator or converter, convert these decimal numbers to hexadecimal: `45`, `200`, `4000`. Then convert these hexadecimal numbers to decimal: `2A`, `FF`, `1A4`. Show your place-value work for each one (which powers of 16 you multiplied and added).
2. **Decode five CSS colors into plain-language RGB.** For each hex color below, split it into its three 2-digit pairs, convert each pair to a decimal number from 0-255, and write one plain-language sentence describing the mix (for example, "mostly blue, a little red, almost no green"):
   - `#1E90FF`
   - `#FFD700`
   - `#2E8B57`
   - `#8A2BE2`
   - `#DC143C`
3. **Write `addresses.c` and print real addresses.** On cs50.dev, create `addresses.c` declaring at least three variables of different types (for example an `int`, a `char`, and a `double`). For each one, use `printf` to print both its value (with the matching format code: `%i`, `%c`, `%f`) and its address (using `&` and `%p`). Compile with `make addresses` and run it with `./addresses`.
4. **Stretch goals.** Run your `addresses.c` a second time and compare the addresses printed: note that they're different from the first run, even though it's the exact same program. Separately, predict how many hex digits a 64-bit address needs (hint: each hex digit is 4 bits, so how many hex digits cover 64 bits?), then count the digits your own program actually printed.

### How you will know you are done

- ✅ You converted all six numbers in Milestone 1 by hand, and can explain the place-value math for at least one of each direction out loud.
- ✅ You produced decimal R, G, B values and a one-sentence plain-language description for all five colors in Milestone 2.
- ✅ `addresses.c` compiles with `make addresses` and, when run, prints both a value and a `0x`-prefixed address for at least three variables.
- ✅ You can explain, in your own words, the difference between what `printf("%i\n", n)` and `printf("%p\n", &n)` each print.

> 💡 **Keep yourself honest:** do Milestones 1 and 2 by hand before you check them against any calculator or online converter: the goal is to feel the place-value arithmetic, not just trust that a tool got it right.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Count in hex (foundational)
Write out hexadecimal counting from `00` to `20` by hand, the same way Part 4's table does, without looking back at the lesson. Circle the point right after `0F` where the second digit rolls over, and explain in one sentence why that happens where it does.

### Exercise 2: Reverse a color (intermediate)
You're given the plain-language description "a fully-saturated purple: full red, no green, full blue." Write its RGB decimal triplet, then its 6-digit hex code. Then do the reverse: given the hex code `#00CED1`, describe the color it makes in plain words before converting it.

### Exercise 3: Predict address behavior (advanced)
Take the `addresses.c` you wrote for the Capstone and add a second `int` variable declared right after the first one. Predict, before running it, whether the two variables' addresses will be close together or far apart, then run the program and check. (You don't need to explain *why* precisely yet. That's next lesson's topic. Just observe and describe what you see.)

---

## Cheat sheet

```text
IMAGES
  pixel        = one colored dot in an image
  resolution   = width x height, in pixels
  bit depth    = bits per pixel -> how many colors are possible
                 1 bit/pixel  = 2 colors (black/white)
                 24 bits/pixel = full RGB (3 bytes: R, G, B)

HEXADECIMAL (base 16)
  digits: 0 1 2 3 4 5 6 7 8 9 A B C D E F   (A-F = 10-15)
  place values: ... 4096  256   16    1
  0x prefix: "everything after this is hex" -> 0x10 = sixteen, not ten
  2 hex digits = 1 byte = 0-255 = 00-FF

RGB <-> HEX QUICK REFERENCE
  black = (0,0,0)       = 000000
  white = (255,255,255) = FFFFFF
  red   = (255,0,0)     = FF0000
  green = (0,255,0)     = 00FF00
  blue  = (0,0,255)     = 0000FF

MEMORY ADDRESSES
  &variable   -> "the address of this variable" (an operator, not a value)
  %p          -> the printf format code for printing an address
  printf("%p\n", &n);   prints something like 0x7fffd3c34ecc
  addresses differ every run -- the fact that one exists is the point, not its digits
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 2 (Bits and Binary):** you learned RGB as three decimal numbers and bytes as 8-bit patterns. This lesson is that exact same material, revisited: the same bytes, now read in hexadecimal, with real memory addresses attached.
- **Earlier, Module 4 · Lesson 16 (Recursion and Merge Sort):** the immediately preceding lesson in the course path; it doesn't feed into this one directly, but it's where Module 4 (Algorithms) closed before this lesson opens Module 5 (Memory).
- **Next, Module 5 · Lesson 18 (Pointers, and What Strings Really Are):** takes the `&` operator you just met and adds its partner, the dereference operator `*`, so you can not just *read* an address but actually *go to* it, and reveals that a C string has secretly been a memory address (a `char*`) since week one.
- **Later, Module 5 (Lessons 19-20):** `malloc`, `free`, and file I/O all lean on being able to read a hex address at a glance, exactly as practiced here.
- **Later, Module 10 (The Web: CSS):** the hex color codes you practiced decoding in this lesson's Capstone are exactly what you'll type into a stylesheet the moment you write CSS for your own final project's pages.

---

*Source: "CS50x 2026 - Lecture 4 - Memory" by David J. Malan, Harvard University (CS50x 2026). Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
