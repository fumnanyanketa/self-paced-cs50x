# Module 9 · Lesson 32: Using AI Well: Prompts and Copilots

> **Course:** Self-Paced CS50x
> **Module 9:** Artificial intelligence: use AI well, and know how it works underneath.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Artificial Intelligence](https://www.youtube.com/watch?v=-9bo8HlSxwQ) · [full transcript](../../transcripts/10-artificial-intelligence.txt)
> **Estimated time:** 45 minutes (read plus exercises)

---

## In one sentence

CS50's duck went from silently quacking at confused students to holding real English conversations once it was built on two ideas anyone can use today (a **system prompt** that fixes an AI's personality and rules in advance, and a **user prompt** that asks it one specific question), and once you can spot those two ingredients inside CS50's own code and inside an AI pair-programmer like GitHub Copilot, you can use these tools to write real code responsibly instead of just accepting whatever they hand back.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you write three system prompts of increasing specificity for a study-buddy persona, test all three against CS50's own free duck, and then use that same duck to scaffold (and critique line by line) a small function you already understand. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk is recent, but the underlying idea is not.
>
> - **[The Pragmatic Programmer](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer)** (Andrew Hunt and David Thomas, 1999). This is the book generally credited with popularizing "rubber duck debugging", the practice this entire lesson's duck is named after: explaining your problem out loud, in complete and precise detail, to a silent listener, until the act of explaining it fully reveals the bug to *you*. Prompt engineering, which you'll meet in Part 3, is the same discipline aimed at an AI instead of a toy on your desk: the more completely and precisely you explain yourself, the better the answer you get back.

## A few plain-language basics first

This lesson uses some everyday-sounding terms in a specific way. Here they are in plain words:

- **Artificial intelligence (AI):** technology that finds patterns in large amounts of data and uses those patterns to produce an answer, a decision, or new content, instead of following a fixed list of `if/else` rules that a human wrote out in advance for every possible case.
- **Generative AI:** a kind of AI that produces new material (text, images, sound, video, even code) rather than just labeling or sorting things people already made. The duck, GitHub Copilot, and tools like ChatGPT, Claude, and Gemini all belong to this category.
- **Model:** the specific trained AI "engine" that a request gets sent to (for example, one particular version of GPT). Different models can be faster, cheaper, or more capable; you choose one by name.
- **API (application programming interface):** a set of features a company exposes so that other programmers can build on top of its software without recreating it themselves. CS50's duck is built on APIs from companies like OpenAI and Microsoft.
- **Prompt engineering:** the practice of writing clear, detailed, well-structured instructions to an AI so it's likely to hand back the answer you actually want. Despite the fancy-sounding name, as you'll read below, it's mostly just asking good questions.
- **System prompt:** standing instructions a programmer writes once, in advance, that shape how the AI behaves for every question that follows: its personality, its rules, its boundaries.
- **User prompt:** the specific question a person types in at that moment. This is what changes every single time, while the system prompt stays fixed.
- **GitHub Copilot:** an AI pair-programmer built into a code editor (here, Visual Studio Code) that can read the code you already have open and either autocomplete it or write new code from a plain-English chat request.

You do not need to memorise these. Each is explained again the first time it matters below.

## Why this lesson matters

Back in Lesson 1, you watched Malan build a ten-line chatbot and watched one sentence, a system prompt, turn it from a plain assistant into a cat. That felt like a toy. It wasn't. The exact same pattern, the same `client.responses.create()` call, is what's actually running behind CS50's own duck, and it's the same pattern behind every AI assistant you'll touch for the rest of this course, including, eventually, your own final project.

Malan is candid that using AI well changes what's possible for a beginner almost overnight. Comparing the hours students spend on a problem set to how fast an AI can scaffold a first draft, he says plainly that once you have the underlying vocabulary, "it will allow you to implement far grander projects, far greater projects than has been possible to date, certainly in just a few weeks we have to do it, because of this amplification of your own abilities." That's the promise. This lesson is also honest about the catch: amplification only helps if you can still tell good code from bad, which is exactly what the rest of this course is building in you.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain how CS50's duck evolved from a silent quacker to an English-speaking AI tutor, and why the silent version already worked for many students.
2. Given a system prompt and a user prompt, predict how each one shapes an AI's answer, and correctly identify which is which inside real code.
3. Trace, line by line, what `client.responses.create(model=..., input=..., instructions=...)` does, the exact code introduced in Lesson 1, using the terms "model," "user prompt," and "system prompt" correctly.
4. Use an AI assistant to scaffold a small function you already understand, and critique its output line by line instead of accepting it uncritically.
5. Write system prompts of increasing specificity for a persona, and describe concretely how the AI's behavior changes as the prompt gets more specific.

## Prerequisites

- **Module 1 · Lesson 1 (Welcome to CS50):** the user-prompt/system-prompt vocabulary and the ten-line chatbot script this lesson expands on line by line.
- **Module 8 · Lesson 31 (Indexes, injection, and race conditions):** the immediately preceding lesson. No SQL knowledge is needed here. This module is a self-contained detour into AI.
- Helpful but not required: having attempted the `speller` (`dictionary.c`) and Mario (`mario.c`) problem sets yourself in C, since both appear as live demos below. If you haven't reached them yet, the demos still make sense on their own.

---

## Part 1: The rubber duck's history (from silent quacker to English-speaking tutor)

Long before AI, there was already "sort of a thing in programming circles to have a rubber duck on your desk," as Malan puts it: a real, physical rubber duck you talk to when you're stuck. The idea: in the absence of a friend, family member, or teaching assistant to ask, you *verbalize* your confusion out loud to the duck. Quite often, simply forcing yourself to explain the problem clearly enough for a silent object to "understand" it is what makes the bug obvious to you. Nothing about the duck is smart. The thinking is entirely yours. This is exactly the "rubber duck debugging" technique named in this lesson's First-principles companion above.

CS50 gave every student a physical duck, then "virtualized" it inside the course's own programming environment (a tool called Visual Studio Code, reachable at cs50.dev). For its first few years, the virtual duck's chat window would accept any typed question, and no matter what you asked, it only ever quacked back at you, giving no real answer at all. And yet, by Malan's account, that alone was often enough: the *process* of typing out your confusion, not any answer from the duck, was what solved the problem.

Then, in 2023, everything changed. As Malan tells it, it came as no surprise, given the sudden rise of tools like ChatGPT, Claude, and Gemini, that "in 2023 the same duck started responding to students in English and that now is the tool that they have available, which is in effect meant to be a less helpful version of Chat GPT, one that doesn't just spoil answers outright, but tries to guide them to solutions akin to any good teacher or tutor." The duck kept its old job (provoke you into explaining yourself) but gained the ability to talk back like a patient tutor instead of a silent toy.

> 🔑 **The single most important takeaway of this part:** the duck's whole design philosophy, before and after 2023, is *guide, don't spoil*. A good tutor (and a well-designed AI tutor) doesn't hand you the answer; it asks the next useful question.

---

## Part 2: The AI-vs-reality game (how good has this gotten?)

To make the stakes of "generative AI" concrete before explaining how it works, Malan ran a live audience poll using real examples the *New York Times* had published comparing AI-generated content to the real thing. The game, each round: two items on screen, pick which one is AI.

**Round 1: two photographs.** More than 70% of the audience correctly picked the AI-generated photo. It had, in Malan's words, "looked a little too good or maybe a little too unreal."

**Round 2: two more photographs.** A majority guessed "left." The actual answer: it was a trick question. **Both** photographs were AI-generated. Neither person in either photo exists.

**Round 3: two short texts,** framed with the question "did a 4th grader write this, or the new chatbot?"

> **Text 1:** "I'd like to bring a yummy sandwich and a cold juice box for lunch. Sometimes I'll even pack a tasty piece of fruit or a bag of crunchy chips. As we eat, we chat and laugh and catch up on each other's day."

> **Text 2:** "My mother packs me a sandwich, a drink, fruit, and a treat. When I get into a lunchroom, I find an empty table and sit there and eat my lunch. My friends come and sit down with me."

The audience majority guessed Text 1 was the AI, and this time, they were right. As Malan explains, "the answer here, in fact, is that SA 1 is the AI, because indeed SA 2 is more akin to what a 4th, or if I may, a 5th grader would write." One tell: Text 1's grown-up phrase "catch up on each other's day" is not typical vocabulary for the age group it's imitating; Text 2's plainer, more literal sentences ("My mother packs me...") read as more genuinely childlike.

Three rounds, three different outcomes: correctly spotted, completely fooled, and correctly spotted again. Malan's own conclusion: "this game is not something we can play for years to come, because it's just going to get too hard to discern something that's AI-generated or not." That's not a reason to panic. It's the reason the rest of this lesson (and this whole module) exists: if you can no longer tell by eye, you need to understand what's actually happening underneath.

---

## Part 3: Inside the duck (APIs, system prompts, and prompt engineering)

Here's the architecture, in Malan's description: a student uses a CS50 tool; that tool talks to a CS50-built website called **cs50.ai**; CS50's own code on that site talks to third-party **APIs** (from companies like OpenAI and Microsoft, who have done "the hard work of developing these models") plus, in Malan's words, "some local sauce that we CS50 add into the mix to make it specific, the duck's answers, to CS50 itself."

```text
   You (student)
        |
        v
   cs50.ai  (CS50's own website and code, the "local sauce")
        |
        v
   Third-party API  (OpenAI, Microsoft, ...)
        |
        v
   The underlying model
```

That "local sauce" is where **prompt engineering** comes in, a term Malan is quick to deflate: "prompt engineering really, it's not so much a form of engineering as it is a form of asking good questions. And being detailed in your question, giving context to the underlying AI, so that the answer with high probability is what you want back." No special credential is required: just clarity and detail.

Prompt engineering, as CS50 practices it, produces two distinct pieces of text:

- A **system prompt**: instructions written by CS50 staff, in English, once, that push the underlying AI toward a certain personality and a specific area of expertise.
- A **user prompt**: whatever the student actually types in that moment.

Malan reads the *essence* of the duck's real system prompt aloud:

> "You are a friendly and supportive teaching assistant for CS 50. You are also a rubber duck, and that is sufficient to turn an AI into a rubber duck, it turns out. Answer student questions only about CS 50 in the field of computer science. Do not answer questions about unrelated topics."

And crucially, one more line:

> "Do not provide full answers to problem sets, as this would violate academic honesty."

That last line is doing real work: it's the reason the duck will coach you toward a solution but won't just write your problem set for you. In the actual prompt CS50 sends, this whole block of instructions ends with the words "Answer this question:", and it's right after that point that CS50's code pastes in whatever the student typed, the user prompt, before sending the combined text off to the model.

| | System prompt | User prompt |
|---|---|---|
| Who writes it | CS50 staff, in advance | The student, each time |
| How often it changes | Rarely: it's standing policy | Every single question |
| What it controls | The duck's identity, topic, and boundaries (including "no full pset answers") | *What* is being asked right now |

> 🔑 **The single most important takeaway of this part:** the duck isn't a different, dumber AI model than ChatGPT. It's very likely the *same kind* of model, wrapped in a system prompt that tells it who to be and what not to do. Prompt engineering is how CS50 turned a general-purpose AI into a course-specific tutor without writing a single line of new AI itself.

---

## Part 4: The week-0 code, finally explained line by line

Recall the ten-line chatbot from Lesson 1. At the time, some of it was left unexplained. Now, with this architecture in hand, Malan revisits that exact code:

```python
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

Malan's own description of the one line that does the real work: "we created a variable called response which was meant to represent the response from OpenAI['s] server. We used `client.responses.create`, which is a function or method that OpenAI gives us that allows us to pass in three arguments: the input from the user, that is the user prompt; the instructions from us, that is the system prompt; and then the specific model or version of AI that we wanted to use."

Mapped onto the code:

- `model="gpt-5"`: which trained AI engine to send the request to.
- `input=user_prompt`: the student's specific question, changing every time.
- `instructions=system_prompt`: the standing rules, set once by the programmer (or, in CS50's real duck, by CS50 staff, the same "friendly and supportive teaching assistant" text you read in Part 3).

And the last line, `print(response.output_text)`, is simply, in Malan's words, how "we were able to answer questions like what is CS 50 or the like." This is not a simplified toy version of how the duck works. It is, structurally, exactly how the duck works. Swap the hardcoded `system_prompt` string for CS50's real one, point a browser interface at it instead of a terminal, and you have cs50.ai.

> ✅ **What to do about it:** any time you see an AI feature anywhere (a duck, a chatbot, a coding assistant), ask yourself what its system prompt probably says. That's usually the fastest way to understand *why* it behaves the way it does.

---

## Part 5: Watching Copilot write code (and why you still have to read it)

CS50 disables one particular AI feature for students from day one: **GitHub Copilot**, an AI pair-programmer built into Visual Studio Code. Malan notes it's "very similar in spirit to products from Google and Anthropic and other companies as well, but this is the one that comes from Microsoft," via GitHub. Students aren't allowed to use it until their final projects, which is deliberate, as you'll see below.

**Demo 1: filling in `speller`'s `dictionary.c`.** Weeks earlier, students had to implement several blank functions in a spell-checker, often taking, in Malan's estimate, "5 hours, 10 hours, 15 hours." With Copilot's chat panel open next to `dictionary.c`, Malan simply types a request: "implement the check function... using a hash table in C," and Copilot proposes working code, highlighted in green, that he can accept with one click. He does the same for the `load` function. Copilot isn't guessing blindly. It's using real context: the open file itself, the `//` comments students already had explaining each function's job, and the function's declared inputs and outputs. Malan is careful to name a limit here too: "co-pilot in general, as well as a lot of AI tools[,] are familiar with CS50 itself because it's been freely available as open courseware for years," meaning this demo's uncanny accuracy is partly because CS50's own problem sets are already in these tools' training data, not proof that any brand-new, private problem would go this smoothly.

**Demo 2: generating `mario.c` from scratch.** Malan creates a completely empty file, then types one plain-English instruction into Copilot's chat: "please implement a program in C that prints a left aligned pyramid of bricks using hash symbols for bricks and use the CS50 library to ask the user for a non-negative height as an integer." That single sentence is the entire English description of an assignment (Problem Set 1's Mario) that normally takes real effort to implement from a blank file. Copilot produces a complete, working program (a loop asking for a height using the CS50 library, then nested loops printing rows of `#` characters) in seconds.

Malan is unusually blunt about the risk right after clicking "keep" on the first demo: "I'll assume that it's correct, but that's actually quite a big assumption." He goes further, naming exactly what makes that assumption dangerous or safe: "if you don't have an eye for what you're looking at, there's no way you're going to be able to troubleshoot an issue in here, explain it to someone else, make marginal changes or the like." The payoff, though, is real, once you *do* have that eye: "this kind of functionality in AI amplifies your capabilities as a programmer sort of overnight."

> ❌ **The trap to avoid:** treating a green-highlighted Copilot suggestion as finished just because it appeared instantly. The muscle memory you're building in Modules 2 through 8 (reading C and Python by eye, tracing what a loop actually does) is precisely the "eye" Malan says you need before AI-written code is safe to keep.

---

## Part 6: How the pieces combine

Every idea in this lesson is one loop, repeated at every scale from the duck to Copilot:

```text
  YOUR QUESTION (user prompt)
          |
          v
  STANDING RULES (system prompt) -- shapes tone, topic, boundaries
          |
          v
  client.responses.create(model, input, instructions)  -- the API call
          |
          v
  GENERATED TEXT OR CODE
          |
          v
  YOU READ IT LINE BY LINE, BEFORE YOU TRUST IT   <-- the step this lesson insists on
```

The duck, the AI-vs-reality game, and Copilot are three different surfaces on top of the exact same underlying idea: a system prompt plus a user prompt, sent through an API, to a model, producing an output that is very often good, and occasionally, confidently, wrong. Knowing that loop is what lets you use any future AI tool well, not just these two.

---

## Key takeaways

1. **The duck didn't get "smarter" until 2023**: before that, quacking alone often worked, because verbalizing your own confusion out loud is frequently enough to spot the bug yourself.
2. **Prompt engineering is asking good, detailed questions**: in Malan's own words, "not so much a form of engineering as it is a form of asking good questions."
3. **Every AI request splits into two prompts:** a system prompt (standing rules, set once) and a user prompt (the question, set every time). CS50's duck's system prompt is what stops it from just handing out problem-set answers.
4. **`client.responses.create(model=, input=, instructions=)` from Lesson 1 is literally the same call running underneath cs50.ai**: the toy chatbot and the real duck share one architecture.
5. **AI-generated text, photos, and code are now good enough to fool most people, most of the time**: which is exactly why you must keep reading critically instead of clicking "keep" on faith.
6. **AI amplifies your capability; it does not replace your judgment**: which is why CS50 withholds Copilot until your final project, once you already have the vocabulary to check its work.

## Common pitfalls

- ❌ Assuming AI-generated code is correct because it compiled or looked plausible: Malan's own words: "I'll assume that it's correct, but that's actually quite a big assumption."
- ❌ Mixing up which prompt is which: the **system prompt** is the standing rules set once by whoever built the tool (including "do not provide full answers to problem sets"); the **user prompt** is only your one-off question.
- ❌ Writing vague, one-word prompts and expecting a great answer back: prompt engineering means being specific and giving context, not typing less.
- ❌ Asking an AI to scaffold something you don't understand at all yet: you won't have "an eye for what you're looking at" to catch its mistakes.
- ❌ Assuming Copilot's success on a CS50 problem set predicts equally good results on a brand-new, private problem: CS50's material is public and in these tools' training data; your own future projects generally won't be.

---

## 🛠️ Capstone Project: Build (and Break) a Study-Buddy Persona, Then Critique the Duck's Code

> This is the main hands-on project for the lesson. Using CS50's own free duck at **cs50.ai** (sign in with a free GitHub account, no paid API key needed), you'll prove to yourself, with real saved output, that specificity in a system prompt changes an AI's behavior, and that you cannot safely trust AI-written code without reading it line by line.

### What you will build

Two short, concrete artifacts:

1. **Three system prompts of increasing specificity** for a "study buddy" persona, each tested against the exact same user question, with your own written notes on how the behavior changed.
2. **One small C or Python function**, scaffolded by the duck, that you already understand well enough to critique line by line.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Prompt engineering ("asking good questions") | Writing three system prompts that get progressively more detailed |
| System prompt vs. user prompt | Your test question (user prompt) stays fixed while only the system prompt changes |
| CS50's real system prompt (identity + domain + "do not") | Your most detailed system prompt copies that same three-part structure |
| `client.responses.create(model, input, instructions)` | Exactly what's running behind the scenes every time you chat with the duck |
| "That's actually quite a big assumption" | The discipline behind your line-by-line critique of the duck's scaffolded function |

### Milestones (build them in order, each one works on its own)

1. **Sign in to cs50.ai for free.** Go to **cs50.ai** and sign in with a free GitHub account: this is the same duck Malan demos live, and it costs nothing. (No GitHub account? Create one free at github.com; it takes about two minutes.)
2. **Write System Prompt A: bare minimum.** One short sentence and nothing else, e.g., *"You are a study buddy."*
3. **Write System Prompt B: more specific.** Add a subject, a tone, and one boundary, e.g., *"You are a patient, encouraging study buddy helping a beginner learn Python. Use simple analogies. Never just give the final answer. Ask a guiding question instead."*
4. **Write System Prompt C: CS50-style.** Model it directly on the three-part structure from Part 3 (identity, domain, and an explicit "do not"), e.g., *"You are a friendly, patient study buddy for a beginner learning [pick one topic: loops, functions, or hash tables]. Answer only questions about that topic and general computer science; do not answer unrelated questions. If asked to just solve a problem outright, do not give the full solution. Ask a guiding question instead."*
5. **Fix one user prompt and test all three.** Pick one real, honest question: something like *"I don't understand how a for loop works, can you just show me the answer?"* (deliberately phrased to test the "don't just give the answer" boundary). Paste it, completely unchanged, against System Prompt A, then B, then C. Save all three real replies.
6. **Write your comparison.** In a few sentences per prompt, describe concretely how the reply changed (tone, whether it refused to "just give the answer," whether it stayed on topic) as the system prompt got more specific.
7. **Pick one function you already understand.** Choose something small you've implemented before and can explain without looking anything up: a `check` function, an `is_prime` function, a simple `average` or `swap` function, in C or Python.
8. **Ask the duck to scaffold it from a plain-English description**: following Malan's Mario demo, describe only the inputs, the task, and the return value in one or two sentences, without pasting your own code, and ask the duck to write the function.
9. **Critique the output line by line.** For every line the duck returns, write one honest note: correct, incorrect, or "I'd do this differently, because..." Don't skip a single line, and don't just "click keep."

### How you will know you are done

- ✅ Three real, saved replies from the duck (persona A, B, and C) to the identical question.
- ✅ A short written comparison naming at least one concrete behavior change as the system prompt got more specific.
- ✅ A duck-scaffolded function, plus a line-by-line critique that addresses every line.
- ✅ You can state, in one sentence, one thing the duck's code got right and one thing you would change.

> 💡 **Keep yourself honest:** pick a function for step 7 that you can already explain cold, not one you're secretly hoping the duck will teach you for the first time. Malan's caution is the whole point: "if you don't have an eye for what you're looking at, there's no way you're going to be able to troubleshoot an issue in here." This same duck, used with this same discipline, is exactly what you'll lean on later to move faster on your final project, a database-backed web app, without letting it think for you.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Redraw the architecture (foundational)
From memory, describe or sketch CS50's duck architecture from Part 3 (student → cs50.ai → third-party API → model), labeling exactly where the system prompt and the user prompt each live in that chain.

### Exercise 2: Predict the boundary (intermediate)
Reread CS50's real system prompt quoted in Part 3. Predict, in writing, what the duck would do if a student's user prompt were "Just give me the full code for pset3." Then name the exact sentence in the system prompt that determines that behavior.

### Exercise 3: Play the game yourself (advanced)
Write two short paragraphs on the same everyday topic (for example, "my weekend"): one entirely in your own words, one generated by an AI from a plain prompt. Ask a friend to guess which is which, the way Malan's audience did in Part 2, and write down what gave it away.

---

## Cheat sheet

```text
RUBBER DUCK, THEN AND NOW
  Pre-2023: silent duck, quacks only   -> verbalizing your bug was often enough
  2023+:    English-speaking AI duck  -> guides you, doesn't just hand you the answer

DUCK ARCHITECTURE
  You -> cs50.ai (CS50's code) -> third-party API (OpenAI / Microsoft) -> model
                    ^
                    CS50's own "local sauce": the system prompt

TWO KINDS OF PROMPT
  SYSTEM PROMPT = standing rules, written once, by the programmer/course staff
  USER PROMPT   = the one-off question, written every time, by the person asking

THE DUCK'S REAL SYSTEM PROMPT, IN THREE PARTS
  1. Identity:  "You are a friendly and supportive teaching assistant... a rubber duck."
  2. Domain:    "Answer student questions only about CS50 ... Do not answer ... unrelated topics."
  3. Boundary:  "Do not provide full answers to problem sets, as this would violate academic honesty."

WEEK-0 CODE, FULL CIRCLE
  response = client.responses.create(
      model="gpt-5",                 # which AI engine
      input=user_prompt,             # the question -- changes every time
      instructions=system_prompt,    # the standing rules -- set once
  )
  print(response.output_text)

BEFORE YOU ACCEPT AI-WRITTEN CODE
  - Do you already understand what this function is supposed to do?
  - Read every line -- does it match what YOU would have written?
  - "I'll assume that it's correct, but that's actually quite a big assumption." -- Malan
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 1 (Welcome to CS50):** introduced the ten-line chatbot and the system-prompt/user-prompt split as a brand-new idea; this lesson finally walks that same `client.responses.create()` call line by line and shows it running for real, as CS50's own duck.
- **Earlier, Module 8 · Lesson 31 (Indexes, injection, and race conditions):** the immediately preceding lesson; nothing from it is required here: this module is a deliberate, self-contained detour into AI before the course returns to building.
- **Next, Module 9 · Lesson 33 (How machines learn):** goes underneath prompts and APIs entirely, to the decision trees, reinforcement learning, and neural networks that make any of this (the duck, Copilot, the AI-vs-reality game) possible in the first place.
- **Later, your final project:** the same duck and the same prompt-engineering discipline from this lesson's Capstone is exactly what you're encouraged to lean on when you build your database-backed web app at the end of this course, a fast, tireless junior colleague that speeds you up, never a replacement for your own judgment about what it hands you back.

---

*Source: "CS50x 2026 - Artificial Intelligence" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current OpenAI SDK and cs50.ai interface.*
