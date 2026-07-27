# Module 1 · Lesson 1: Welcome to CS50: Computers, Thinking, and a Live AI Chatbot

> **Course:** Self-Paced CS50x
> **Module 1:** Computational thinking: learn to think in inputs, outputs, and algorithms before any syntax.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 0 - Scratch](https://www.youtube.com/watch?v=UuIEbpQms8o) · [full transcript](../../transcripts/02-lecture-0-scratch.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Programming is nothing more mysterious than taking an **input**, running it through a step-by-step **algorithm**, and producing an **output**, and you can prove that to yourself right now by watching a real AI chatbot get built in about ten lines of Python, then completely change its personality the moment one extra sentence, called a **system prompt**, gets added.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you write your own system prompt to give a free AI chatbot a persona, then test it live. Everything before the Capstone teaches the ideas you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk is recent, but the underlying idea is not.
>
> - **[How to Solve It](https://en.wikipedia.org/wiki/How_to_Solve_It)** (George Pólya, 1945). Decades before "computational thinking" was a phrase anyone used, the mathematician George Pólya wrote down almost the same loop Malan is teaching here: understand the problem (know your input and your goal), devise a plan (the algorithm), carry it out, and check the result (the output). CS50 applies that loop to computers; Pólya's book is the tool-agnostic original, and it works just as well on a jigsaw puzzle as on a chatbot.

## A few plain-language basics first

This lesson uses some everyday-sounding terms in a specific way. Here they are in plain words:

- **Computational thinking:** the habit of breaking any problem, not only a coding problem, down into a clear input, a clear goal (the output), and a step-by-step way to get from one to the other.
- **Input and output:** the *input* is whatever you hand a process to work with (a question, a number, a name); the *output* is the answer or result it hands back.
- **Algorithm:** a finite list of step-by-step instructions for turning an input into an output: a recipe that a person or a computer can follow exactly, with no guesswork.
- **Program (or code):** an algorithm written out in a language a computer can actually carry out, such as Python.
- **API (application programming interface):** a set of features one piece of software exposes so that other people can write their own programs on top of it, without rebuilding it themselves. Malan builds his chatbot on OpenAI's API instead of inventing an AI from scratch.
- **Variable:** a labeled box that stores a value (like `prompt`) so code can refer to "whatever the human just typed" without knowing in advance what that will be.
- **Prompt (user prompt vs. system prompt):** the text you hand an AI model. A **user prompt** is the one-off question a person types in. A **system prompt** is a standing instruction the programmer sets once, that quietly shapes every answer the AI gives afterward.
- **Terminal:** a text window where you type commands and see a program's output directly. This is where Malan actually runs his chatbot script.

You do not need to memorise these. Each is explained again the first time it matters below.

## Why this lesson matters

"CS 50... has never been about teaching you how to program," Malan tells the room in the opening minutes. "That's actually one of the side effects of taking a class like this, but the overarching goal is to teach you how to think, how to take input and produce correct output and how to master these and other tools." That distinction matters more, not less, now that AI can write code for you. Malan is candid that "you and I as humans have long been the bottleneck," but you still need to know what you're asking for and whether the answer you got back is actually right. His metaphor is worth keeping: even with an AI copilot alongside you, "you'll still be in the driver's seat, so to speak. You'll be the pilot, you'll be the conductor." This lesson is where that promise stops being abstract and becomes something you watch happen, live, in about ten lines of code.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain, in your own words, why CS50 teaches thinking rather than syntax, and connect that claim to the input → algorithm → output model of a problem.
2. Trace what each line of a small Python chatbot script does, from importing an API to printing the AI's reply.
3. Distinguish a **system prompt** from a **user prompt**, and predict how changing each one changes what an AI outputs.
4. Write your own system prompt to give an AI chatbot a specific persona, and test it using a free tool.

## Prerequisites

- None. No prior programming experience is assumed, and no account or tool setup is required to follow this lesson.
- Optional: the Module 0 pre-flight lesson (setup), if you eventually want to run this code yourself in a cs50.dev codespace. It is not needed for today's Capstone, which only needs a free browser-based AI chat.

---

## Part 1: Why CS50 doesn't actually teach you to program

Malan opens the entire course by addressing "the elephant in the room" (AI) head-on, rather than pretending it away. His point is not that AI makes learning to code pointless; it's closer to the opposite. Because AI can now write and debug code for you, the scarce skill isn't typing syntax anymore: it's knowing what you want, and knowing whether what came back is correct. That is exactly what CS50 has always tried to teach.

He draws a direct comparison to two older technologies that supposedly made a skill obsolete: calculators (didn't erase the need to understand arithmetic) and, in his own words, the "many darn ways in college [to] take derivatives and integrals," where after learning several methods by hand, the real point wasn't the methods themselves but understanding the idea well enough to then lean on a tool. AI and code are the same relationship, one level up.

> 🔑 **The single most important takeaway of this part:** learning to program is a side effect of this course, not its goal. The actual goal is learning to think in terms of input, algorithm, and output: a skill that keeps paying off no matter which tool (or AI) does the typing.

### The frame that runs through the whole course

Malan names the concrete outcome directly: by the end of the course "not only will you be acquainted with languages like Scratch... C and Python and SQL, HTML CSS and JavaScript, you'll be able to teach yourself new things ultimately." Learning several languages, in other words, isn't the point either: it's evidence that you've learned the underlying way of thinking well enough to apply it anywhere.

## Part 2: What a program actually is: input, algorithm, output

Strip away the code, the languages, and the AI, and Malan reduces "computer science" to one picture. A **problem**, he says, is "some input, which is like the problem we want to solve, and the output, which is the goal we want the solution there too." In between sits, in his words, "the proverbial black box, the sort of secret sauce" that turns the input into the output. That black box is the **algorithm**: the step-by-step recipe that gets you from what you started with to what you wanted.

```text
   INPUT            [ ALGORITHM ]            OUTPUT
(the problem   --->   (the step-by-step  --->  (the goal /
 you start with)        "secret sauce")          the answer)
```

Every example in this lesson, and in this entire course, is a variation on that one diagram. A chatbot answering a question is this diagram. A phone book search is this diagram. A Scratch cat saying "hello" is this diagram. Computer science, Malan says, is "really just the study of information": how you represent it (input and output) and how you process it (the algorithm).

> 🔑 **The single most important takeaway of this part:** before you ever write a line of code, you should be able to say, in plain English, what your input is, what your output should be, and roughly what has to happen in between. If you can't say that, you're not ready to code the solution yet, no matter how good your AI copilot is.

## Part 3: Watching a chatbot get built in about ten lines

To make all of this concrete, Malan opens Visual Studio Code (VS Code) ("popular, largely open source or free software... used by real world people in industry to write code") and, in the terminal at the bottom of the screen, writes a Python file called `chat.py`. "So here's how relatively easy it is nowadays to write even your own chatbot using the AI technologies that we already have," he says.

Rather than building an AI from scratch, he writes his program on top of an **API** ("an application programming interface that someone else provides") from a company called OpenAI. Here is a reconstruction of that first version:

```python
# chat.py - version 1: a hardcoded question
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="in one sentence, what is CS50?",
)

print(response.output_text)
```

Walking through it in plain English:

- `from openai import OpenAI`: borrow the tools OpenAI has already built, instead of reinventing them.
- `client = OpenAI()`: create what Malan calls "a so-called client," a program of your own that uses OpenAI's software.
- `response = client.responses.create(...)`: ask OpenAI's model for an answer, handing it your **input** (the question) and telling it which **model** ("a statistical model that ultimately drive[s] what the AI's can do") to use.
- `print(response.output_text)`: actually show that answer, because, as Malan puts it, "I want to know what the answer to that question is."

Running it worked immediately: the reply came back describing CS50 correctly. But there's a catch Malan names outright: "I've implemented my own chatbot that at the moment is hard coded, that is permanently configured to only answer one question for me." Nothing is broken: it's just static. To fix that, he adds one built-in Python function, `input()`, which pauses the program and waits for a human to type something:

```python
# chat.py - version 2: ask the human for the question
from openai import OpenAI

client = OpenAI()

prompt = input("What would you like to ask? ")

response = client.responses.create(
    model="gpt-5",
    input=prompt,
)

print(response.output_text)
```

Malan's own reasoning for the change: "Suppose you wanted to write code that actually asks the human what their question is, because very quickly might we want to learn something more than just this one question." The line `prompt = input(...)` stores whatever the human typed inside a **variable** called `prompt`: "just like in math," he says, "X, Y or Z." Now the same script can answer *any* question, not just one that was typed directly into the source code.

## Part 4: System prompt vs. user prompt: giving the AI a personality

With `input()` in place, Malan starts experimenting: "in one sentence, what is CS50?", then "in one word, what is CS50?", then, for fun, "in one word, which is better, Harvard or Stanford?" (The AI's careful answer: "Depends.") But he notices a pattern in his own behavior: he keeps re-typing the same style instruction ("in one sentence," "in one word") every single time. His fix is to stop asking the human to repeat that instruction, and instead tell the AI once, permanently:

> "If you want the AI to behave in a certain way, why don't we just tell the underlying system to behave in that way."

That standing instruction is a **system prompt**, and to make the distinction obvious, Malan renames his other variable to **user prompt**. Here's the reconstructed script with both:

```python
# chat.py - version 3: a system prompt and a user prompt
from openai import OpenAI

client = OpenAI()

user_prompt = input("What would you like to ask? ")
system_prompt = "Limit your answer to one sentence."

response = client.responses.create(
    model="gpt-5",
    input=user_prompt,
    instructions=system_prompt,
)

print(response.output_text)
```

| | User prompt | System prompt |
|---|---|---|
| Who writes it | The person using the chatbot, every time | The programmer, once, in advance |
| How often it changes | Every question | Rarely: it's the "standing instructions" |
| What it controls | *What* is being asked | *How* the AI should behave while answering |
| In this script | `user_prompt` (from `input()`) | `system_prompt` (a fixed string) |

Then Malan pushes the idea further, live, to make the point unmissable: "you might know that these GPTs nowadays have sort of personalities... Why don't we go into our system prompt here and say something silly like pretend you're a cat." He changes exactly one line (`system_prompt = "Pretend you're a cat."`), reruns the identical script with the identical question, "What is CS50?", and gets back:

> "CS 50 is Harvard University's introductory computer science course teaching programming, algorithms, data structures, and problem solving, and it's available free online meow."

Same model. Same code. Same question. One sentence changed, and the entire personality of the output changed with it.

> ✅ **What to do about it:** whenever you want an AI to behave consistently a certain way (a tone, a role, a constraint like "answer in one sentence"), put that instruction in the system prompt, once, instead of retyping it into every user prompt.

> 💡 **A nuance worth noting:** model names age fast. Malan uses `model="gpt-5"`, "the latest and greatest version at least as of today," in his words. By the time you read this, a newer model may be current. The *pattern* (client, user prompt, system prompt) is what's durable; the model name is not.

## Part 5: How the pieces combine

Zoom back out to Part 2's diagram, and the whole script is just one instance of it, with one addition. Malan calls the visible reply (the printed text) a **side effect**: "something that happens visually on the screen... as a result of you using a function." The system prompt doesn't show up in the output directly; it reshapes the *algorithm* itself before the input ever gets processed.

```text
   INPUT                    ALGORITHM                       OUTPUT
 user_prompt      --->   client.responses.create(       --->  printed
("What is CS50?")          model, input, instructions)         reply
                                   ^
                                   |
                          system_prompt shapes HOW
                          the algorithm behaves;
                          it is not typed by the user
```

Malan's own summary of what just happened: "with programming you have the ability in like 10 lines of text, not all of which you might understand yet... to build fairly powerful things." He immediately connects this pattern to something CS50 gives every student for free: "in the world of programming, it's kind of a thing to keep a rubber duck literally on your desk... because when you are struggling with some problem, some bug or mistake in your code... you literally are encouraged in programming circles to talk to the rubber duck." Then the payoff: "CS 50, drawing inspiration from this, will give to you a virtual duck in computer form" (at **cs50.ai**) and, in his words, "these are the AIs you can use in CS50 to solve problems and you are encouraged to do so." The exact user-prompt/system-prompt pattern from this lesson is what's running underneath that duck.

---

## Key takeaways

1. **Programming is input → algorithm → output.** CS50's real goal is that habit of mind, not memorizing syntax: syntax is, in Malan's words, "one of the side effects."
2. **A working AI chatbot is barely code at all.** An API import, a client, one function call carrying an input, and a `print` statement is enough for a first working version.
3. **`input()` is what turns a fixed script into a program.** A hardcoded question isn't broken: it just isn't listening yet.
4. **A system prompt is a standing instruction; a user prompt is the one-off question.** Same model, same code, different system prompt: completely different behavior, as the "pretend you're a cat" demo shows.
5. **This same pattern powers CS50's own free AI**, the "duck" at cs50.ai, which you're not just allowed, but explicitly encouraged, to use.

## Common pitfalls

- ❌ Treating "learn to code" and "learn to think" as the same goal: Malan explicitly separates them; writing correct syntax is a side effect of the class, not its point.
- ❌ Assuming a hardcoded script is "broken" because it always gives the same answer: it's working exactly as written; it just needs `input()` to become dynamic.
- ❌ Mixing up which prompt is which: the **system prompt** is what *you*, the programmer, set once; the **user prompt** is what a person types each time. Swapping these two up will make your mental model of every future AI feature wrong.
- ❌ Waiting until you understand every line before reasoning about what code does: Malan tells the room outright that this is a preview, "not all of which you might understand yet," and that's fine at this stage.

---

## 🛠️ Capstone Project: Give an AI a Persona With a System Prompt

> This is the main hands-on project for the lesson. You'll write a real system prompt, in plain English, and prove to yourself, with real, copy-pasted output, that it changes an AI's behavior. No paid API key required.

### What you will build

A short, written **system prompt** that gives a free AI chatbot a specific, testable persona, tested live against the same fixed question three different ways. You'll build it from these pieces, each mapped to an idea from this lesson:

- A **fixed user prompt**, the one question you won't change.
- A **system prompt** you write yourself, the persona.
- Three real outputs you compare side by side.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Input → algorithm → output | You'll label your own test's input, algorithm (the persona instructions), and output |
| System prompt vs. user prompt | The persona you write *is* a system prompt; your test question is the user prompt |
| Variables | You'll swap system prompts around one fixed user prompt, exactly as Malan swapped `system_prompt` while `prompt` stayed the question |
| CS50's duck | You'll use CS50's own free AI (cs50.ai) instead of a paid API key |

### Milestones (build them in order, each one works on its own)

1. **Get access to a free AI chat tool.** Go to **cs50.ai** (also reachable from cs50.dev) and sign in free with a GitHub account: this is the "virtual duck" Malan describes, and it is explicitly fine to use. (No GitHub, or no access? Any free chatbot with a "custom instructions" or "system prompt" field works identically for this exercise: the concept, not the specific tool, is what matters.)
2. **Pick a fixed user prompt.** Choose one plain question you will ask every time, unchanged: Malan's own example, "In one sentence, what is CS50?", works fine, or pick a question related to your eventual final-project topic.
3. **Write a plain-language system prompt.** In one or two sentences (no code), write standing instructions for a persona, the way Malan wrote "Pretend you're a cat." For example: "Answer like a patient kindergarten teacher" or "Pretend you're a grumpy 1990s dial-up modem."
4. **Run the test three times.** Ask your fixed user prompt with: (a) no system prompt at all, (b) Malan's own system prompt, "Limit your answer to one sentence," and (c) your own persona's system prompt. Save all three real answers.
5. **Label your input, algorithm, and output.** In three short lines, write down: the input (your fixed question), the algorithm (which system prompt was active), and the output (how the wording, tone, or length actually changed).

### How you will know you are done

- ✅ You have three real, copy-pasted answers to the same question, produced under three different system-prompt conditions.
- ✅ You can point to the exact sentence you wrote that is your system prompt, and the exact sentence that is your user prompt.
- ✅ You can explain, in one sentence, why the output changed even though the underlying AI model never did.

> 💡 **Keep yourself honest:** don't guess what the AI "should" say: actually run all three versions and paste the real output, even if one answer is a little odd. Malan's own live demo got an imperfect answer ("maybe Harvard or Stanford?" → "Depends") in front of the whole class; testing for real, including the messy results, is the entire point.

This is the same move you'll make for real once you know Python, in Module 9, and it previews the kind of small, testable component your eventual **final project** (a database-backed web app you'll design and ship at the end of this course) might one day need, such as a support chatbot with a defined, consistent voice.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Spot the input, algorithm, output (foundational)
Pick any everyday task: making toast, looking up a word in a dictionary, choosing what to wear. Write one sentence each for its input, its algorithm (the steps), and its output. This is the exact model Malan draws on the whiteboard, applied somewhere with no code at all.

### Exercise 2: Narrate the chatbot script (intermediate)
Without looking back at Part 3-4, write out in plain English, step by step, everything that happens between "a human types a question" and "an answer appears on the screen" in Malan's script, using the words `client`, `user prompt`, and `system prompt` correctly.

### Exercise 3: Predict, then test (advanced)
Write two more system prompts for the same fixed user prompt you used in the Capstone. Before testing either one, predict in writing how each will change the tone, length, or content of the answer. Then test both at cs50.ai (or your free tool of choice) and check your predictions against the real output.

---

## Cheat sheet

```text
INPUT  --->  ALGORITHM  --->  OUTPUT
(the problem)  (the step-by-step   (the answer /
                "secret sauce")     the goal)

CS50's real goal: teach you to THINK (input -> algorithm -> output),
not just to memorize syntax. Syntax is a side effect.

A tiny chatbot, line by line:
  from openai import OpenAI          # borrow someone else's API
  client = OpenAI()                  # your program's connection to it
  user_prompt = input("...")         # ask the HUMAN (a user prompt)
  system_prompt = "..."              # YOUR standing instructions, set once
  response = client.responses.create(
      model="gpt-5",
      input=user_prompt,
      instructions=system_prompt,
  )
  print(response.output_text)        # show the output

USER PROMPT   = the one-off question a person types, every time
SYSTEM PROMPT = the standing instruction the programmer sets, once

Free, no-API-key way to try this yourself: cs50.ai (sign in with GitHub)
```

## How this connects to the rest of the course

- **Earlier, Module 0 · Pre-flight (setup):** nothing from it is required to understand this lesson: it only assumed a browser. If you did complete it, you already have the cs50.dev codespace where Malan's actual script would run.
- **Next, Module 1 · Lesson 2, Bits and binary: how computers represent everything:** this lesson treated "input" and "output" as if they were obviously text. Lesson 2 goes one level deeper and asks how a computer represents that text (or a number, or a color) using nothing but 0s and 1s.
- **Later, Module 9 · Artificial intelligence:** revisits this exact chatbot code (the same `client`, the same system-prompt-vs-user-prompt idea) once you actually know Python and can write and modify it yourself instead of watching Malan type it.

---

*Source: "CS50x 2026 - Lecture 0 - Scratch" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current OpenAI SDK.*
