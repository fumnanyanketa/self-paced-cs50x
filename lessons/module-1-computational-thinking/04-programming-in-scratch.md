# Module 1 · Lesson 4: Programming in Scratch

> **Course:** Self-Paced CS50x
> **Module 1:** Computational thinking: learn to think in inputs, outputs, and algorithms before any syntax.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 0 - Scratch](https://www.youtube.com/watch?v=UuIEbpQms8o) · [full transcript](../../transcripts/02-lecture-0-scratch.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

In Scratch you build a real, working program (a sprite that talks, listens, repeats itself, and reacts to what's touching it) by snapping together color-coded puzzle pieces, and every one of those pieces (functions with arguments, return values, side effects, loops, conditionals, variables, custom blocks) is an idea you will meet again, in text, in every language for the rest of this course.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you build your own small game at scratch.mit.edu. Everything
> before the Capstone teaches the skills you will use there. If you want to see
> the finish line first, jump to the **"Capstone Project"** section, then come
> back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Scratch's tools change; the theory
> behind why it's built this way does not.
>
> - **[Resnick et al., "Scratch: Programming for All," *Communications of the ACM* (2009)](https://web.media.mit.edu/~mres/papers/Scratch-CACM-final.pdf)**,
>   written by the MIT Media Lab team that built Scratch, this paper explains
>   the design philosophy in plain terms: block shapes that only fit together
>   when the combination is syntactically valid (so you can't get a "syntax
>   error"), and a focus on tinkering and sharing over memorizing rules. It is
>   the first-principles account of *why* Scratch looks and feels the way it
>   does, independent of any particular version of the software.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Sprite:** any character or object in a Scratch program: the default is a cat, but a sprite can look like a dog, a trash can, or a coat of arms. Each sprite has its own code.
- **Stage:** the rectangular "world" a sprite lives in and moves around, with its own coordinate system (more on that below).
- **Blocks palette:** the scrollable, color-coded list of puzzle pieces (blocks) on the left of the Scratch editor: one color per category, like purple for "Looks" or blue for "Sensing."
- **Script:** a stack of blocks snapped together, top to bottom, that runs as one unit. A sprite can have more than one script running at once.
- **Argument:** an input you plug into a block to customize what it does, like typing "Hello, world" into the white oval of a `say` block.
- **Return value:** a value a block hands back to your program for later use, instead of showing it on screen right away.
- **Side effect:** something a block does that a human can see or hear directly: text appearing in a speech bubble, a sound playing.
- **Loop:** a block that repeats the blocks inside it, either a fixed number of times or forever.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lesson 3 gave you algorithms and pseudocode on paper: step-by-step instructions, forks in the road, loops that go "back to step 3." This lesson gives those same ideas a body you can drag, snap, and click. As Malan frames it:

> "In Scratch, which is a graphical programming language designed about 20 years ago from our friends down the road at MIT's Media Lab, it represents pretty much everything we're going to be doing fundamentally over the next several weeks in more modern languages like C and Python, more textual languages if you will."

That is the whole reason this lesson exists before a single line of text-based code: once you've built something real out of puzzle pieces, the curly braces and semicolons coming in Module 2 are just a new *font* for ideas you already have.

## Learning objectives

By the end of this lesson you will be able to:

1. Navigate the Scratch editor, locate the blocks palette, the code (script) area, the sprite list, and the stage, and explain what the stage's X/Y coordinates are for.
2. Build a script using `say`, `ask`, and `join` that takes input from a person, transforms it, and produces output, correctly naming which part is the argument, which is the return value, and which is the side effect.
3. Replace repeated, copy-pasted blocks with a loop, and build your own custom block that takes a parameter (a "meow N times" block).
4. Combine a `forever` loop with an `if` conditional and a Boolean expression (`touching mouse-pointer?`) so a sprite reacts continuously, not just once.
5. Trace how a full game (Oscar Time, Ivy's Hardest Game) is built from these same pieces (sprites, costumes, variables, loops, conditionals, custom blocks) layered one small working version at a time.

## Prerequisites

- Module 1 · Lesson 3 (search and pseudocode): the idea of an algorithm as step-by-step instructions, and of a conditional as a fork in the road guarded by a Boolean expression.
- A free scratch.mit.edu account (created in the optional Module 0 pre-flight lesson, or create one now, no programming experience needed).

---

## Part 1: Touring the Scratch interface

Open scratch.mit.edu and click **Create**. Before you drag anything, just look around. Malan does the same tour before writing a single block:

> "This is the scratch programming environment and there's a few different parts of this world. This is the blocks palette, so to speak... there's a bunch of puzzle pieces or building blocks that represent functions and conditionals and... loops and other such constructs."

Four regions matter:

| Region | What it is |
|---|---|
| **Blocks palette** (left) | Color-coded puzzle pieces, grouped by category (Motion, Looks, Sound, Events, Control, Sensing, Operators, Variables, My Blocks). |
| **Code area** (middle) | Where you drag blocks and snap them into scripts. |
| **Sprite list** (bottom right) | Every sprite in your project. Click one to edit *its* code: each sprite's scripts are separate. |
| **Stage** (top right) | The world the sprites live in, and the only part your player actually sees when the program runs. |

As Malan puts it:

> "There's going to be the programming area here where you can actually write your code by dragging and dropping these puzzle pieces... There's a whole world of sprites here: by default Scratch is... a cat by design, but you can make Scratch look like a dog, a bird, a garbage can, or anything else."

The stage has a coordinate system, like graph paper:

> "There's sort of this XY plane here, so 0, 0 would be in the middle... Generally you don't need to worry about the numbers, but they exist so that when you say up or down, you can actually tell the program go up one pixel or 10 pixels or 100 pixels so that you have some definition of what this world actually is."

Concretely: `(0, 0)` is the dead center of the stage, positive X moves right, positive Y moves up, and the stage's edges are roughly `x = -240`/`x = 240` and `y = -180`/`y = 180`. You will use exactly these numbers later to make trash fall from the top of the screen and bounce a sprite off a wall.

> 🔑 **Browse before you build.** The palette looks overwhelming at first. Even Malan, 20 years in, says he hasn't used every block. You don't need to know them all; you need to know they're organized by color and category so you can go looking when you need one.

## Part 2: `say`, `ask`, and `join` (arguments, return values, and side effects)

Drag a **when green flag clicked** block (Events, yellow) into the code area, then snap a **say** block (Looks, purple) underneath it. Click the green flag (top right) and the sprite speaks. Double-click the white oval on the `say` block and you can change what it says: that oval is an **argument**.

> "The white oval... is actually editable by me because it turns out that some functions can take arguments or more generally inputs that influence their behavior."

In plain terms, a block is a **function**, a small, named piece of functionality someone else (MIT, in this case) already built for you:

> "So a function is just a piece of functionality implemented in code, which in turn implements an algorithm."

`say` produces a **side effect**, something a human can see happen:

> "A side effect in a computer program is often something that happens visually on the screen or maybe audibly out of a speaker. It's something that just kind of happens as a result of you using a function."

Now swap in the **ask _ and wait** block (Sensing, blue). It also takes an argument (the question), but instead of an immediate side effect, it hands you back whatever the person typed, stored automatically in a built-in variable called `answer`. That's a **return value**:

> "A side effect is something the human sees, but a return value is something only the computer sees. It's like the computer is handing me back the user's input."

If you snap `ask "What's your name?"` followed by `say "Hello, "` and then a second `say [answer]`, both messages flash by too fast to read as one: they're on two separate lines, executed one after another, just faster than a human eye can follow. The fix isn't a `wait` block (that only makes it *slower*, still two bubbles): it's the **join** block (Operators, green), which takes two arguments and returns one combined value:

> ✅ **What to do about it:** drag `join [hello] [world]` into the `say` block, replace its first slot with your greeting text (mind the trailing space before the comma) and its second slot with the `answer` variable. Now one `say` block shows "Hello, David" in a single breath, because you passed the *return value* of `join` in as the *argument* to `say`.

## Part 3: Loops and a custom block with a parameter

Suppose you want your sprite to meow three times, with a short pause between each. The naive way is to drag three copies of **play sound "Meow" until done** and three copies of **wait 1 second**, alternating. It works, but it's a trap:

> "Generally when you copy paste code or when you duplicate puzzle pieces, [you're] probably doing something wrong... It's better to keep things simple and ideally centralized by factoring out common functionality."

The fix is a **loop** (Control, orange): drag a **repeat 3** block around a single `play sound` + `wait` pair. Change the 3, or the wait time, and you only change it in one place.

Better still, you can invent your own block. Under **My Blocks**, click **Make a Block**, name it `meow`, and Scratch creates a matching **define meow** script for you:

> "Now I have in my code area here a define block, which literally means define meow as follows."

Put your `repeat` + `play sound` + `wait` combination inside that definition, and a new `meow` puzzle piece appears in the palette, one block that does the work of five. This is a **custom block**: a function you define yourself, the same way MIT's engineers defined `say` and `ask` for you.

You can go one step further and give it a **parameter**, an input the block itself declares, so callers can customize it:

> "Let's add an input, otherwise known as an argument to this meow block, and we'll call it maybe N... for the number of times I want it to meow."

Edit the block definition, add an input labeled `N`, then drag that `N` into the `repeat` block's count instead of a hard-coded number. Now `meow (3)` and `meow (10)` both work from the *same* block: no copy-pasting, no editing five places when you change your mind. (A **variable**, note, is the more general version of this idea: a labeled box, like `N`, or `score` later on, that holds a value your scripts can read and change.)

## Part 4: Conditionals (`forever`, `if`, and a Boolean question)

A **conditional** is a fork in the road: do this, or do that, based on a yes/no question. Scratch calls that question a **Boolean expression**:

> "A boolean expression is just a question that has a yes or no answer or a true or false answer or a 1 or zero answer. Just it's a binary state, yes or no typically."

Try this: under **Sensing**, grab the puzzle piece shaped like a question, `touching mouse-pointer?`, and drop it into an `if <> then` block's diamond slot (Control, orange). Inside the `if`, put `play sound "Meow" until done`. Click the green flag: nothing happens, because Scratch checked the question exactly once, at the instant you clicked, and you weren't touching the sprite yet.

Wrap the whole `if` inside a **forever** block, and everything changes:

> "By using the forever block... this ensures that Scratch is constantly checking the answer to that question." So if and when you do move the cursor onto the sprite, it will actually detect it.

> ✅ **What to do about it:** any `if` that's meant to react to something happening *over time* (a mouse moving, a key being held, two sprites approaching each other) needs to live inside a `forever` loop. Without it, Scratch asks the question once, gets an answer, and never asks again.

## Part 5: Putting it together (Oscar Time and Ivy's Hardest Game)

Everything above (sprites, `say`/`ask`/`join`, loops, custom blocks, `forever`/`if`, variables) is all a real game needs. Malan walks through two, built layer by layer.

**Oscar Time.** The goal, in Malan's words:

> "The goal is to drag as much falling trash as you can to Oscar's trash can before his song ends."

He builds it in versions, each one still a working program:

- **Version 0:** just a sprite (a trash can instead of a cat) and a **costume**, the specific image a sprite is currently wearing. No code at all yet.
- **Version 1:** the trash-can sprite switches costume (lid closed → lid open) inside a `forever` `if touching mouse-pointer?` / `else`, so hovering over it looks like the lid popping open. Switching costumes quickly is how Scratch fakes animation.
- **Version 2:** a trash sprite sets itself draggable, jumps to a random X (between -240 and 240) and Y = 180, the top of the stage, then, in a `forever` loop, changes its Y by -1 each step so it visibly falls. A second, parallel script says: `forever`, `if touching Oscar?`, teleport back to a random spot at the top (i.e., a fresh piece of "falls").
- **Version 3:** the repeated "jump to a random X, Y = 180" logic gets factored into one custom block, `go to top`, used in both scripts instead of being duplicated, exactly the lesson from Part 3.
- **Version 4:** a **variable** named `score` is created, set to 0 at the start, and incremented by 1 each time trash touches Oscar: Scratch displays it as an on-screen scoreboard automatically. Malan's naming advice generalizes well beyond Scratch:

  > "In computer programming it's best to name things, not silly simple words like X, Y, and Z, but full-fledged words that say what they are, like `score`."

His advice for building your own version:

> "Start by the simple problems and figure out what [bites] can I bite off in order to make progress (baby steps, if you will) to the final solution."

**Ivy's Hardest Game.** A Harvard-crest sprite lives on the stage between two walls, controlled with the arrow keys. Two scripts run in parallel: one listens for keyboard, one "feels" for walls:

> "If you're touching the left wall, change your X by 1. If you're touching the right wall, change your X by -1", because if you've gone so far right that you're touching the wall, you're already sitting on top of it, so you back up one pixel, as if bouncing off.

Layered on top, one level at a time:

- An enemy sprite (Yale) bounces on its own: `forever`, `if touching a wall then turn 180 degrees, else move (n) steps`. Raising the step count from 1 to 10 makes it faster, and harder.
- A second enemy (MIT) hunts you down: `forever`, `point towards Harvard-crest`, `move (n) steps`. Push the step count up too far, though, and it visibly overshoots and doubles back: Malan hits this bug live:

  > "It's moving so fast that it's sort of going 10 pixels this way, but then... it kind of overshot me, so then it's doubling back to follow me again."

  His fix: throttle the step count back down ("make it 5 or 2 or 3 instead of 10") until the motion looks deliberate instead of twitchy.
- The finished game stacks several of these enemies across multiple levels, with a win condition at the exit sprite.

```text
ONE SPRITE'S WORLD, ONE PIECE AT A TIME
  sprite + costume            → looks like something, does nothing yet
  + forever/if + touching?    → reacts to one thing (mouse, wall, a wall)
  + custom block              → repeated logic becomes one reusable piece
  + variable (score)          → the game remembers something over time
  + a second/third sprite     → obstacles, enemies, goals
  = a game
```

> 🎯 Notice the shape of this thinking: a sprite waits for an **event** ("when green flag clicked," "forever, if touching X") and *reacts*. That is the same event-driven habit of mind (wait for a request, react, respond) that your eventual final-project web app will need, just with a browser request standing in for a mouse click.

---

## Key takeaways

1. **Every block is a function.** The white oval you fill in is an argument; some blocks (`say`) just produce a visible side effect, others (`ask`) hand back a return value you can reuse.
2. **Repetition is a design smell.** Copy-pasted blocks mean every future change has to happen in every copy. A loop fixes "N times"; a custom block (optionally with its own parameter) fixes "this exact sequence, reusably."
3. **`forever` is what makes `if` alive.** A condition checked once, at the start, is checked once. Wrapping it in `forever` is what lets a sprite keep noticing something happening over time.
4. **A game is not one big idea: it's small pieces layered.** Oscar Time and Ivy's Hardest Game both started as a sprite that did nothing, and grew one working version at a time: costume, then reaction, then custom block, then variable, then a second sprite.

## Common pitfalls

- ❌ Building an `if` to catch something happening over time (a hover, a key press, a collision) without wrapping it in `forever`: Scratch checks once and moves on. Wrap it.
- ❌ Duplicating blocks (or copy-pasting a whole sequence) instead of building a loop or a custom block: now a "small" change means hunting down every copy.
- ❌ Chaining two `say` blocks to combine text: they'll flash by too fast to read as one message. Use `join` to combine them into a single `say`.
- ❌ Cranking up a "move N steps" value for difficulty without checking the result: too large a step and a chasing sprite (like MIT chasing you in Ivy's Hardest Game) will overshoot its target and visibly twitch back and forth.

---

## 🛠️ Capstone Project: Build a small Scratch game

> This is the main hands-on project for the lesson. By the end, you will have a
> small, playable, original game at scratch.mit.edu that you built yourself,
> block by block: proof that "input, algorithm, output" is something you can
> actually construct, not just diagram.

### What you will build

A short interactive game, in the same spirit as Oscar Time and Ivy's Hardest Game but your own: a sprite that greets the player, reacts to something, repeats an action cleanly via a custom block, keeps score, and ends with a win or lose message.

### Why this is the perfect practice

| Lesson idea | Where you use it in the capstone |
|---|---|
| `say` / argument / side effect | Milestone 1: your sprite's greeting |
| `ask` / return value / `join` | Milestone 2: responding to the player's input |
| Loop + custom block with a parameter | Milestone 3: an action that repeats cleanly |
| Variable | Milestone 4: keeping score |
| `forever` + `if` + Boolean expression | Milestones 3-5: reacting continuously, and the win/lose check |

### Milestones (build them in order, each one works on its own)

1. **Sprite says hello.** Create a free scratch.mit.edu account if you don't have one. New project, one sprite, `when green flag clicked` → `say "Hello!"`. Change the text so it says something in your own voice.
2. **Responds to input.** Add `ask "What's your name?" and wait`, then use `join` to combine a greeting with the `answer` variable in a single `say`. (Watch the space after the comma.)
3. **Uses a loop + custom block.** Build your own custom block with a parameter (for example, a `cheer (N)` block that says "Go!" N times with a short wait between each) and call it from your main script.
4. **Keeps score with a variable.** Create a `score` variable, set it to 0 at the start, and increment it by 1 whenever some event happens (touching another sprite, a key press, your choice), inside a `forever`/`if`.
5. **Win/lose condition.** When `score` reaches some target (or some bad thing happens), `say "You win!"` (or "Game over") and stop the scripts.
6. **Stretch goals.** Add a second sprite that moves on its own (bouncing off walls, or chasing your main sprite, like Yale and MIT in Ivy's Hardest Game); add sound timed to an action; add multiple costumes for a simple animation, as Oscar Time does with its trash-can lid.

### How you will know you are done

- ✅ Clicking the green flag runs your game from a clean start every time (no leftover state from a previous run).
- ✅ You can point to one block in your project and correctly name it as either an argument, a return value, or a side effect.
- ✅ At least one repeated action in your project uses a loop or a custom block instead of duplicated puzzle pieces.
- ✅ The game has a clear win or lose message that appears at the right moment.

> 💡 **Keep yourself honest:** after every milestone, click the green flag and actually play it: a milestone you haven't clicked doesn't count as built.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Ask and greet (foundational)
Build the `ask` → `join` → `say` script from Part 2 from scratch (no pun intended), typing your own name in when you test it. Then break it on purpose (remove the `join` and use two `say` blocks instead) and watch the bug Malan hit live.

### Exercise 2: A parameterized custom block (intermediate)
Build a custom block called `cheer` that takes one parameter, `N`, and says "Go team!" N times with a half-second wait between each. Call it twice in the same script with two different values of N and confirm both work without touching the block's definition.

### Exercise 3: React and react again (advanced)
Add a second sprite to a project. Give it a script that, inside a `forever` loop, checks `if touching [your first sprite]?` and does something visible (changes costume, plays a sound, or moves away). Then delete the `forever` wrapper and observe (and explain in one sentence) why the reaction stops working.

---

## Cheat sheet

```text
SCRATCH INTERFACE
  Blocks palette (left, color-coded)  ·  Code area (middle)
  Sprite list (bottom right)          ·  Stage (top right, X: -240..240, Y: -180..180)

FUNCTIONS, ARGUMENTS, RETURN VALUES
  argument   = the input you plug into a block (the white oval)
  side effect = what a human sees/hears happen (say, play sound)
  return value = what the computer hands back for reuse (ask -> "answer")
  join [a] [b]  -> combines two values into one, for a single say

LOOPS & CUSTOM BLOCKS
  repeat (n)     -> do the contents n times
  forever        -> do the contents endlessly (needed to keep an `if` alive)
  My Blocks > Make a Block -> your own reusable block; add an input for a parameter

CONDITIONALS
  if <boolean?> then ... [else ...]
  boolean expression = a yes/no question (e.g. touching mouse-pointer?)
  RULE: an `if` reacting to something ongoing MUST be wrapped in `forever`

GAME BUILDING, ONE STEP AT A TIME
  sprite + costume -> looks + change costume -> simple animation
  + forever/if      -> reacts to one thing
  + custom block    -> repeated logic, reusable
  + variable (score)-> the game remembers something
  + 2nd/3rd sprite  -> obstacles, enemies, a goal
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 3:** gave you algorithms, pseudocode, conditionals, and loops on paper. This lesson gave the same ideas a physical, draggable form you could actually run and watch.
- **Next, Module 2 · Lesson 5 ("Hello, C: from blocks to code"):** every block you used here has a direct textual twin: `say` becomes `printf`, `ask` becomes reading input, `repeat`/`forever` become `for`/`while` loops, `if` stays `if`, a custom block becomes a function, and a variable stays a variable, just declared with a type.
- **Later, Module 2:** as you meet each new C construct, look back here: every one of them maps to a Scratch block you already built and understood first.

---

*Source: "CS50x 2026 - Lecture 0 - Scratch" by David J. Malan, Harvard University. Code snippets and block descriptions are illustrative reconstructions of the patterns described in the talk. Adapt them to the current Scratch editor.*
