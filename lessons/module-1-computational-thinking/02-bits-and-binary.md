# Module 1 · Lesson 2: Bits and Binary: How Computers Represent Everything

> **Course:** Self-Paced CS50x
> **Module 1:** Computational thinking: learn to think in inputs, outputs, and algorithms before any syntax
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 0 - Scratch](https://www.youtube.com/watch?v=UuIEbpQms8o) · [full transcript](../../transcripts/02-lecture-0-scratch.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Every letter, emoji, color, photo, video, and song your computer touches is nothing more than a pattern of 0s and 1s that everyone has agreed in advance to interpret the same way, and once you can count in binary and read a lookup table, you can decode any of it by hand.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you hand-encode a short message in binary and ASCII, have someone decode it, and hand-build a tiny pixel-art image out of raw RGB bytes. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk is recent, but the underlying idea is not.
>
> - **[*Code: The Hidden Language of Computer Hardware and Software*](https://www.charlespetzold.com/code/)** (Charles Petzold, book). It builds up, from first principles, exactly the path this lesson takes: from on/off switches, to binary counting, to ASCII, to how a computer represents anything at all. It is the classic, timeless account of the idea Malan compresses into one lecture.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Bit:** short for "binary digit": the smallest unit of information a computer stores, always either a 0 or a 1.
- **Byte:** a group of 8 bits treated as one unit. 8 bits can form 256 different patterns.
- **Binary (base 2):** a number system that uses only two digits, 0 and 1, instead of the ten digits (0-9) you use every day (decimal, or base 10).
- **Transistor:** a microscopic electronic switch inside a computer chip. It is either "on" (representing 1) or "off" (representing 0).
- **ASCII:** a fixed table that assigns every English letter, digit, and punctuation mark a number, so computers can agree on what a byte of text means.
- **Unicode:** a much bigger table than ASCII that assigns a number to every character in every human language, plus symbols and emoji.
- **RGB:** a way of building any color by mixing amounts (0-255 each) of red, green, and blue light.
- **Pixel:** one single colored dot in the grid of dots that together makes up a digital image.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Last lesson you built a chatbot in ten lines of Python without ever telling the computer what a "letter" or a "sentence" was. It just worked. This lesson explains why that was possible: everything you typed was already reducible to numbers the machine understands. As Malan puts it, at the most basic level, **"You only have zeros and ones as the solution to these problems."** Once you see how a light switch becomes a letter, a letter becomes a color, and a color becomes a photograph, you stop seeing computers as magic. You see them as very fast, very literal-minded counting machines, and that changes how you debug, design, and reason about every program you'll write for the rest of this course.

## Learning objectives

By the end of this lesson you will be able to:

1. Count in binary by hand and convert any binary number up to 8 bits to and from decimal.
2. Explain how a computer stores a letter using ASCII, and look up or derive any letter's numeric code from a table.
3. Explain why Unicode exists, how it differs from ASCII, and why the same emoji can look different on different devices.
4. Explain how RGB numbers encode a color, and how bits stack up to represent pixels, images, video, and sound.

## Prerequisites

- **Module 1 · Lesson 1** (welcome to CS50, the AI chatbot demo): you should already be comfortable with the idea of input → algorithm → output.
- No coding, accounts, or installed tools are needed for this lesson. Paper and a pencil are enough.

---

## Part 1: Counting without ten fingers (unary and binary)

Before computers can represent anything (a letter, a color, a sound), they need a way to represent *numbers*, because as you'll see all the way through this lesson, numbers are the only raw material a computer has.

Malan starts with the simplest possible counting system, **unary (base 1)**, where you use one digit per unit, like fingers on a hand: **"the unary notation, which means you essentially use single digits like fingers on your hand, for instance, unary AKA base one, is something you can do on your own human hand."** With five fingers, you can count 0 through 5 and no higher. It's simple, but wasteful.

Binary does something smarter: instead of just counting how many fingers are up, it gives each *position* a different weight (1, 2, 4, 8, 16 …), the same way each position in a decimal number has a weight (1s, 10s, 100s). Because each position can only be 0 or 1, a hand of five fingers can now represent any number from 0 to 31, not just 0 to 5, simply by which fingers are up or down.

This is exactly how a computer works, except instead of fingers, it uses **transistors** (**"millions of tiny little things called transistors"**), microscopic electrical switches that are either letting electricity through (on, representing 1) or not (off, representing 0). A single one of these positions is called a **bit** (short for binary digit): **"Binary digit is not really something anyone really says, but the shorthand for that is going to be bit."**

Here's how the place values work for a 3-bit number, using light bulbs as a stand-in for transistors:

```text
Place value:     4    2    1
Light bulbs:    off  off  off   →  0
Light bulbs:    off  off   on   →  1
Light bulbs:    off   on  off   →  2
Light bulbs:    off   on   on   →  3
Light bulbs:     on  off  off   →  4
Light bulbs:     on  off   on   →  5
Light bulbs:     on   on  off   →  6
Light bulbs:     on   on   on   →  7
```

To read a binary number, multiply each "on" position by its place value and add them up. `110` in binary is `(1×4) + (1×2) + (0×1) = 6`.

> 🔑 **A bit is just a 0 or a 1, but its *position* gives it a weight.** Reading binary is the same mental math you already do for decimal: you're just using place values of 1, 2, 4, 8, 16 … instead of 1, 10, 100, 1000.

Three bits can only count to 7 (eight total values, including 0), and four bits only to 15. Real computers group bits into bigger chunks. The most common chunk has a name: **"A byte is just that. 1 byte is 8 bits."** Eight bits gives you 256 possible patterns, the numbers 0 through 255, which is why **256** shows up constantly in computing (256 colors, 256-value bytes, and so on). Modern computers commonly work in 32-bit or 64-bit chunks at once, letting them represent numbers into the billions.

### Why not just use ten symbols, like we do for decimal?

Because electricity is simplest to build as a two-state system: flowing or not flowing. Building hardware that could reliably distinguish ten different voltage levels would be far more complex and error-prone than building a switch that is simply on or off. Binary isn't the "natural" choice for numbers: it's the natural choice for *electricity*, and numbers just came along for the ride.

## Part 2: From bits to letters (ASCII and the "BOW" demo)

So far we've only represented numbers. But a computer also needs to store the letter A. Since bits are the only material available, the solution has to be an agreement: pick a number, and declare that whenever a computer sees that number *in a context expecting text*, it should be treated as the letter A.

That agreement already exists, and it was made by a committee of people, not derived from any deep logic: **"a bunch of humans in a room years ago decided that this pattern of zeros and ones shall be known globally as a capital letter English A."** The number they chose is **65**. B is 66, C is 67, and so on: this scheme is called **ASCII** (the American Standard Code for Information Interchange), and it uses one byte (8 bits) per character.

A few useful facts fall out of this table once you look at it:

- **Digits and punctuation have codes too.** The exclamation point `!` is 33.
- **Lowercase letters are always uppercase + 32.** `a` is 97, `A` is 65, and 97 − 65 = 32; `b` is 98, `B` is 66, and so on. This means a computer can lowercase a letter just by flipping one bit: adding 32 in binary only changes the bit in the "32s" place.
- **Text messages are just bytes.** If you text a friend "HI!" in all caps, you are sending exactly three bytes: 72, 73, 33 (H, I, and `!`).

To make this concrete, Malan brought 8 student volunteers on stage, one per bit position (1, 2, 4, 8, 16, 32, 64, 128), and had the audience read off each volunteer's raised or lowered hand as a 0 or 1 to reconstruct a byte. Round 1 produced 66 (**B**), round 2 produced 79 (**O**), and round 3 produced 87 (**W**), spelling **BOW**. None of the volunteers individually knew what letter they were spelling; each only knew their own bit. Malan's takeaway: **"we indeed spelled out bow, and that's just because we all standardized on representing information in exactly the same way, which is why when you type BOW on your phone or your computer, the recipient sees the exact same thing."**

> 🔑 **Text is just numbers that everyone agreed on in advance.** There is nothing "letter-like" about the number 65: the ASCII table is the entire agreement, and every keyboard, screen, and messaging app on Earth honors it.

> ✅ **What to do about it:** when you need to decode or hand-encode text as numbers, always work from a table (the cheat sheet at the end of this lesson has one) rather than trying to derive the mapping: it's arbitrary by design, so there's nothing to derive.

## Part 3: Beyond English (Unicode and emoji)

ASCII's one byte per character gives you only 256 possible characters, enough for English uppercase, lowercase, digits, and punctuation, but not enough for accented letters, most non-English alphabets, or the images-that-are-secretly-characters you send every day: emoji.

The fix is **Unicode**, a much larger standard that assigns a number to a character using more bits: 16, 24, or even 32 bits instead of ASCII's 8. With 32 bits available you can represent billions of distinct characters, which is exactly why there's room for thousands of emoji. Malan is careful to point out that an emoji is not a picture file at all. It is a *character*, just like the letter A, that happens to render as a colorful image: **"You're sending characters. You're not sending images per se… these are just like characters in a different font, and that font happens to be very colorful and graphical as well."**

This also explains a puzzling everyday experience: the same emoji looking slightly different depending on whether you send it from an iPhone, an Android phone, or an app like Telegram. Unicode standardizes *which number* means "face with tears of joy," but each company is free to draw that number however it likes: the way one font might draw a letter "a" with a curl and another without. The underlying bits sent between your friend's phone and yours are identical; only the "font" rendering them differs.

> 💡 **Nuance:** **"emoji have been designed to really represent people and places and things and emotions in a way that transcends human language."** But, Malan adds, "even then they're somewhat open to interpretation": a fixed number doesn't fully pin down how an image is drawn.

## Part 4: Painting with numbers (RGB, pixels, video, and sound)

Numbers, then letters. What about a color? Once again, the only tool available is agreeing on numbers: **"integers is the exact same answer as before. We just need to agree on what number do we use for red, what do we use for green, what do we use for blue."**

The standard scheme, **RGB**, mixes three amounts of light (red, green, and blue), each ranging from 0 to 255 (one byte, just like an ASCII character). A few reference points:

| Red | Green | Blue | Result |
|---|---|---|---|
| 0 | 0 | 0 | Black (no light at all) |
| 255 | 255 | 255 | White (maximum of all three) |
| 72 | 23 | 33 | A dark shade of yellow (Malan's example) |

Because each of the three channels is a byte, one RGB color takes 3 bytes (24 bits) to store. (You may have also seen colors written as pairs of characters like `00` or `FF` on web pages or in Photoshop: that's the same 0-255 range written in a different base, hexadecimal, which you'll meet properly in Module 5's memory lesson.)

A digital image is simply a grid of tiny colored dots called **pixels**, each one carrying its own RGB triplet. Zoom far enough into any photo or emoji and the individual colored squares become visible: Malan shows this by zooming into the "face with tears of joy" emoji until individual pixels appear. A modern photograph with millions of pixels, each needing 3 bytes, is why image files are measured in megabytes.

From there, the same building-block logic extends outward:

- **Video** is just many images shown quickly in sequence: **"It's like 30 images per second flying across the screen or maybe slightly fewer than that, that collectively tricks our mind into thinking we are seeing motion pictures."** A flip-book is the same idea on paper.
- **Sound** can be broken into a handful of numbers per note. Malan proposes: **"we could represent each of these notes using 3 numbers, maybe 0 to 255 or some other range that represents the frequency or the pitch of the note"**, plus duration (how long the note lasts) and loudness (how hard the key was struck).

Stack these ideas together and you get the full hierarchy this lesson has built, bottom to top:

```text
transistor (on/off)
   → bit (0 or 1)
      → byte (8 bits, 0-255)
         → ASCII character (a byte, by agreement)          e.g. 72 = 'H'
         → RGB channel (a byte, by agreement)               e.g. 72 = amount of red
            → pixel (3 bytes: R, G, B)
               → image (a grid of pixels)
                  → video (~30 images per second)
         → musical note (frequency + duration + loudness, each a byte)
```

Every layer above "byte" is the *same* raw material: it's just a matter of what the programmer told the computer to expect. As Malan puts it, the computer can only tell a number from a letter from a color "because the programmer tells the computer how to display the information."

---

## Key takeaways

1. **Everything is bits.** Computers only ever store 0s and 1s; what a given pattern "means" (a number, a letter, a color, a sound) is agreed upon in advance, not discovered from the bits themselves.
2. **A byte is 8 bits, giving 256 possible patterns (0-255).** That's why 256 (and its neighbors, like 255 and 32) shows up everywhere in computing.
3. **ASCII maps letters to numbers by committee, not by logic.** A is 65 because humans decided so; lowercase is always uppercase + 32.
4. **Unicode is ASCII's much bigger sibling.** It spends more bits per character so it can represent every human language and thousands of emoji, which are characters, not pictures.
5. **Color, images, video, and sound are all just more numbers, in agreed formats.** RGB gives each pixel 3 bytes; an image is a grid of pixels; video is many images per second; a sound can be described with a few numbers per note.

## Common pitfalls

- ❌ Reading a binary number as if it were decimal (e.g., assuming `100` in binary is "one hundred"). Fix: always write the place values (1, 2, 4, 8, 16 …) above the digits and multiply before adding.
- ❌ Trying to *derive* a letter's ASCII code from logic instead of looking it up. Fix: the mapping is an arbitrary, memorized agreement. Use a table, and remember only the two anchors (A=65, a=97) plus the +32 rule.
- ❌ Assuming an emoji is a small image file, like a `.png` you download. Fix: it's a Unicode *character* (a number). The picture you see is just one company's rendering ("font") of that number.
- ❌ Thinking one byte can hold a full RGB color. Fix: one byte is only *one channel* (just red, or just green, or just blue); a full RGB color needs 3 bytes.

---

## 🛠️ Capstone Project: Encode yourself in bits

> This is the main hands-on project for the lesson. You'll hand-encode a real message and a tiny image into raw bits (no computer required) so you feel, in your own hands, that "everything is bits" isn't just a slogan.

### What you will build

A small "byte card" you make entirely on paper: a binary-to-decimal cheat sheet you build yourself, a short message hand-encoded in ASCII binary that someone else decodes without help, and a tiny pixel-art image described entirely as a list of RGB byte triplets. All three pieces are free, need no accounts, and work completely offline.

| Lesson idea | Where you use it in the capstone |
|---|---|
| Binary place values | Milestone 1 |
| ASCII text-to-number mapping | Milestone 2 |
| Bits as a shared agreement (the BOW demo) | Milestone 3 |
| RGB bytes per pixel | Milestone 4 |
| Frequency/duration/loudness as numbers | Milestone 5 (stretch) |

### Milestones (build them in order, each one works on its own)

1. **Build your place-value cheat sheet.** On paper, write the columns `128 64 32 16 8 4 2 1`. Practice by converting the decimal numbers 5, 12, 20, and 100 into 8-bit binary using only addition and these columns.
2. **Encode your name (or a nickname) in ASCII.** Look up each letter's decimal ASCII code (use the cheat sheet below), then convert each code into 8-bit binary using Milestone 1's columns. You now have your name written entirely as 0s and 1s.
3. **Send a hidden message.** Pick a short word or phrase (3-6 letters). Write out its full binary encoding (like the volunteers' light-bulb pattern) on a sheet of paper, hand it to a friend or family member along with the ASCII cheat sheet, and have them decode it back into letters without you telling them what it says. (If no one's around, encode a message, set it aside for an hour, then decode your own message "cold" to prove the process works.)
4. **Build a tiny pixel-art image as a byte map.** Sketch a simple 5×5-pixel grid (a heart, a smiley, your initial). For every pixel, write down its RGB triplet, e.g. `(255,0,0)` for red or `(0,0,0)` for black. When you're done you'll have 25 triplets: a literal byte-by-byte description of an image, the same way a real image file works, just smaller.
5. **Stretch goals.** Encode a 3-note "song" as triples of (frequency 0-255, duration in seconds, loudness 0-255) and have someone try to hum it back from just the numbers. Or, pick your favorite emoji and note how many bits (8, 16, 24, 32?) it would need beyond plain ASCII, and why.

### How you will know you are done

- ✅ You can convert any whole number from 0-255 to 8-bit binary and back, on paper, without a calculator.
- ✅ You produced a full binary/ASCII encoding of a real word or short phrase.
- ✅ Someone else (or you, later) correctly decoded that message using only the cheat sheet, proving the encoding was unambiguous.
- ✅ You have a complete list of RGB triplets describing every pixel of a small image you designed.

> 💡 **Keep yourself honest:** don't peek at a calculator or converter tool until *after* you've worked each conversion by hand at least once: the whole point is to feel the place-value math, not just trust that it works.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Binary warm-up (foundational)
Convert the decimal numbers 5, 12, and 20 to 8-bit binary by hand, using the place-value columns `128 64 32 16 8 4 2 1`. Then convert `01101101` back to decimal to check you can go both directions.

### Exercise 2: Decode a byte stream (intermediate)
Given the three ASCII decimal codes `72 101 108 108 111`, use the cheat sheet below to decode the word they spell. Then encode your own 4-letter word into decimal ASCII codes.

### Exercise 3: Reverse-engineer a color (advanced)
Given the RGB triplet `(128, 0, 128)`, predict what color it produces before checking (hint: it's a common color name). Then, for a color you know by name (like "sky blue" or "forest green"), estimate a plausible RGB triplet and explain your reasoning for each channel.

---

## Cheat sheet

```text
BITS & BYTES
  bit          = a single 0 or 1
  byte         = 8 bits = 256 possible patterns = decimal 0-255
  place values (8-bit): 128 64 32 16 8 4 2 1  →  multiply "on" positions, then add

QUICK ASCII REFERENCE (decimal)
  A-Z  =  65-90        a-z  =  97-122   (always uppercase + 32)
  0-9 (digit characters) = 48-57
  space = 32            !   = 33
  H=72 I=73 !=33   →  "HI!"
  B=66 O=79 W=87   →  "BOW"

UNICODE
  ASCII: 8 bits/char, 256 characters max
  Unicode: 16-32 bits/char, billions possible → room for every language + emoji
  An emoji is a CHARACTER (a number); how it's drawn is up to Apple/Google/etc.

COLOR: RGB
  each channel (R, G, B) = 1 byte = 0-255
  (0,0,0) = black   (255,255,255) = white   (72,23,33) ≈ dark yellow
  1 pixel = 3 bytes = 24 bits

IMAGES, VIDEO, SOUND
  image = grid of pixels, each pixel = 3 bytes
  video ≈ 30 images/second
  sound (per note) ≈ frequency + duration + loudness, each a number
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 1:** you framed programming as input → algorithm → output and saw a system prompt shape an AI's output. This lesson is what actually flows through that pipe: bits, standing in for text, numbers, and more.
- **Next, Module 1 · Lesson 3 ("Your first algorithms: search and pseudocode"):** once information can be represented, the next question is how to *find* it efficiently: you'll compare linear and binary search and write pseudocode, using the ASCII/RGB style of "agree on a representation first" thinking you practiced here.
- **Later, Module 5 (Memory, Lesson 17, "Pixels, hexadecimal, and memory addresses"):** you'll revisit these exact same bytes, but read and write them in hexadecimal, a more compact base for writing the binary you learned to count in today, and see them sitting at real addresses in a computer's memory.

---

*Source: "CS50x 2026 - Lecture 0 - Scratch" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
