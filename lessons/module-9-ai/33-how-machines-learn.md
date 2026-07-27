# Module 9 · Lesson 33: How Machines Learn

> **Course:** Self-Paced CS50x
> **Module 9:** Artificial intelligence: use AI well, and know how it works underneath.
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Artificial Intelligence](https://www.youtube.com/watch?v=-9bo8HlSxwQ) · [full transcript](../../transcripts/10-artificial-intelligence.txt)
> **Estimated time:** 60 minutes (read plus exercises)

---

## In one sentence

Every "invisible" AI feature you already rely on (a spam filter, a movie recommendation, a video-game opponent) is running one of just a few underlying ideas: a **decision tree** of yes/no questions, a **scored game tree** searched by an algorithm called minimax, or, once the tree of possible choices gets too enormous to search by hand (as in chess or Go), a system trained by reward and punishment or by pattern-matching on huge amounts of data instead. Once you can tell which one is running, you can predict exactly where and why it will get something wrong.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you hand-draw a complete minimax game tree for a tic-tac-toe endgame and mathematically prove the best move, write a paddle's decision tree as real Python code, and (as a stretch) run your own 20-round explore-vs-exploit experiment with dice. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The demos are new; the mathematics underneath them is not.
>
> - **[Claude Shannon, "Programming a Computer for Playing Chess," *Philosophical Magazine*, 1950](https://www.pi.infn.it/~carosi/chess/shannon.pdf).** The paper that first proposed scoring a finished game position with a number and searching backward through a tree of future moves to decide the best one right now: exactly the minimax idea this lesson's tic-tac-toe example builds by hand.
> - **[Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, MIT Press.](https://mitpress.mit.edu/9780262039246/reinforcement-learning/)** The standard textbook account of learning through reward and punishment, including the exploration-vs-exploitation trade-off (and the epsilon-greedy strategy) that this lesson's pancake robot and maze demonstrate informally.
> - **[Warren McCulloch and Walter Pitts, "A Logical Calculus of the Ideas Immanent in Nervous Activity," *Bulletin of Mathematical Biophysics*, 1943.](https://home.csulb.edu/~cwallis/382/readings/482/mccolloch.logical.calculus.pdf)** The original proposal that a simple mathematical model of a neuron, wired together with others into a network, could compute anything: the seed of the neural networks and large language models in Part 6 and Part 7.

## A few plain-language basics first

This lesson uses some everyday-sounding terms in a specific way. Here they are in plain words:

- **Decision tree:** a flowchart of yes/no questions that leads, step by step, to one final action. It's a fork in the road, the same idea as `if`/`else`, just drawn as branches instead of code.
- **Minimax:** an algorithm for two-player games where one player tries to make the game's final score as high as possible and the other tries to make it as low as possible, by looking ahead through every possible sequence of remaining moves before choosing.
- **Combinatorial explosion:** what happens when the number of possible choices multiplies at every single step, so the total number of possibilities becomes too enormous to check one by one, even for a fast computer.
- **Machine learning:** writing code that learns how to solve a problem from examples of data, instead of a human writing out every rule by hand in advance.
- **Reinforcement learning:** a way of training an AI (or an animal, or a robot) where it tries actions, gets rewarded for good outcomes and penalized for bad ones, and gradually learns which actions pay off, without anyone telling it the "right" answer directly.
- **Exploration vs. exploitation (epsilon):** the trade-off between trying something new for a chance at an even better outcome ("explore") and just doing what has already worked ("exploit"). Epsilon is the probability, on any given turn, of choosing to explore instead of exploit.
- **Neural network:** a web of simple mathematical units ("neurons") connected by numeric weights, tuned automatically on huge amounts of training data until it can predict a useful output from a given input.
- **Hallucination:** a confident-sounding answer from an AI language model that is, in fact, wrong: not a rare software bug, but a predictable side effect of how these models generate text.

You do not need to memorise these. Each is explained again the first time it matters below.

## Why this lesson matters

Lesson 32 ended by promising to go "underneath prompts and APIs entirely, to the decision trees, reinforcement learning, and neural networks that make any of this (the duck, Copilot, the AI-vs-reality game) possible in the first place." This lesson keeps that promise. Malan draws a sharp line between the world of simple rules and the world of learned patterns: describing why brute-force approaches stop working on hard problems, he says plainly, **"you instead need to write code that doesn't solve the problem directly but in some sense indirectly... this is what we mean nowadays by machine learning."**

You've already met the "simple rules" half of this lesson without knowing it. Lesson 7's `if`/`else if`/`else` chain is, quite literally, a decision tree. Lesson 13's Big O notation is the vocabulary for exactly the kind of runaway growth that makes chess and Go too big to brute-force. And Lesson 16's recursion ("call yourself, but with a smaller version of the problem") is precisely how minimax scores a board: by scoring the boards that follow from it. This lesson takes all three of those tools and points them at a genuinely new problem: what do you do once a game (or a sentence, or a recommendation) has *too many* possibilities to just check them all?

## Learning objectives

By the end of this lesson you will be able to:

1. Name at least four everyday "invisible AI" features (spam filters, handwriting recognition, recommendation engines, voice assistants) and explain, in plain language, why none of them run on one giant hardcoded `if`/`else`.
2. Draw a decision tree for a paddle game (Pong or Breakout) and translate it directly into real Python `if`/`elif`/`else` code.
3. Score a finished tic-tac-toe board as `-1`, `0`, or `1`, and hand-trace minimax across a full game tree to identify the objectively optimal move from a near-endgame position.
4. Explain combinatorial explosion using real numbers (255,168 total tic-tac-toe games; roughly 85 billion chess openings; roughly 266 quintillion Go openings) and why it makes exhaustive search impossible for anything much bigger than tic-tac-toe.
5. Describe how reinforcement learning trains an agent through reward and punishment, and explain the explore-vs-exploit trade-off using the epsilon variable.
6. Explain, at a beginner level, how neural networks, deep learning, and large language models like GPT work, and explain why hallucinations happen.

## Prerequisites

- **Module 9 · Lesson 32 (Using AI well: prompts and copilots):** the immediately preceding lesson. Nothing from it is required line by line, but its closing promise, to look "underneath" prompts and APIs, is exactly what this lesson delivers.
- **Module 2 · Lesson 7 (Conditionals and loops):** you'll reuse `if`/`elif`/`else` directly to turn a decision tree into real Python code.
- **Module 4 · Lesson 13 (Thinking in running time: Big O):** combinatorial explosion is Big O's growth-rate warning, at war-story scale: the same "how does this scale?" question, just applied to a game tree instead of a loop.
- **Module 4 · Lesson 16 (Recursion and merge sort):** minimax is a recursive algorithm; the base-case/recursive-case habit of mind from that lesson transfers directly.

---

## Part 1: The AI you already use, every day

Before touching a single algorithm, Malan grounds the whole lesson in features you already trust without thinking about it. Start with spam:

> "There's not some human at Microsoft or Google sort of manually labeling the messages as they come in, deciding spam or not spam. They're figuring out, using code and nowadays using AI, that looks like spam, and therefore I'm going to put it in the spam folder, which is probably correct 99% of the time, but indeed there's potentially a failure rate." (David Malan)

Handwriting recognition works the same way: no company knows *your* handwriting in particular, but having trained on enough other people's handwriting, it can recognize yours with high probability anyway. Streaming recommendations are next:

> "There's no `if`, `if`, `if` construct for every movie or TV show in their database. It's sort of figuring out much more organically, dynamically, what you and I might like." (David Malan)

And voice assistants close the list:

> "There's no massive `if else if` that has all possible questions in the world just waiting for you or me to ask it." (David Malan)

Every one of these features quietly rules out the tool you already know best (a giant, hand-written chain of `if`/`else` statements) because no human could ever write enough branches to cover every email, every handwriting style, every taste in movies, or every possible question. Something else has to be running. The rest of this lesson is that "something else."

> 🔑 **None of these everyday AI features are one giant hardcoded rulebook.** They are all, in one way or another, systems that found patterns in data instead of being told the rules directly. Keeping that distinction in mind is what lets you spot, later in this lesson, exactly which kind of system is running underneath any AI feature you meet.

---

## Part 2: Decision trees (an if/else chain you can draw)

Not every game needs pattern-matching, though. Malan rewinds to Pong and its successor, Breakout (one paddle, one ball, bounce the ball off bricks for points), and points out that a human's instinct about where to move the paddle can be written down as a precise, always-correct recipe:

> "Decision trees are a concept from economics, strategic thinking, computer science as well. That's one way of solving this problem in such a way that you will always play this game well if you just follow this algorithm." (David Malan)

For Breakout, the whole recipe is three yes/no questions:

```text
                Is the ball to the left of the paddle?
               /                                       \
             yes                                        no
              |                                          |
      Move paddle LEFT              Is the ball to the right of the paddle?
                                    /                                      \
                                  yes                                      no
                                   |                                        |
                          Move paddle RIGHT                     Don't move the paddle
```

Malan is explicit that this tree maps one-to-one onto code: no cleverness, no training data, just three questions asked in a loop, in this cleaned-up form of the pseudocode read aloud in the talk:

> "While the game is ongoing: if the ball's to the left of the paddle, then move the paddle left; else if the ball's to the right of the paddle, move the paddle right; else, don't move the paddle." (David Malan)

That is exactly Lesson 7's `if`/`elif`/`else` chain, just drawn as branches before it's written as code:

```python
while game_is_ongoing:
    if ball_x < paddle_x:
        move_paddle("left")
    elif ball_x > paddle_x:
        move_paddle("right")
    else:
        pass  # the ball is already directly above the paddle, so don't move
```

Nothing here learns anything. Given the ball's position and the paddle's position, this code plays Breakout's paddle *perfectly*, every single time, forever. Whenever you can write down the full list of questions a problem needs answered, and there aren't too many of them, a decision tree is not a lesser cousin of "real AI": it's the right tool, full stop.

> 🔑 **A decision tree is just `if`/`else`, drawn as a tree.** If you can enumerate the questions and there's a small, fixed number of them, you don't need machine learning at all.

---

## Part 3: Tic-tac-toe and minimax (scoring a game to solve it)

Tic-tac-toe looks almost as simple as Breakout (get three in a row, horizontally, vertically, or diagonally), but Malan makes a bold claim about it:

> "If back in childhood or more recently you've ever lost a game of tic-tac-toe, like, you're just bad at tic-tac-toe, because logically there's no reason you should ever lose a game of tic-tac-toe if you're playing optimally. At worst you should force a tie, but at best you should win the game." (David Malan)

The algorithm that guarantees this is called **minimax**, and the trick is to strip the fun out of the game entirely by turning it into arithmetic. Malan proposes a single, consistent scoring rule for any finished board:

> "Anytime O wins, the score of the game is -1. Anytime X wins, the score of the game is a positive one. And anytime nobody wins, the score is 0." (David Malan)

Once every finished board has a number, the two players get opposite goals: **X tries to maximize the score** (push it toward `+1`), and **O tries to minimize it** (push it toward `-1`). As a sanity check, a board where X has already completed three in a row down the middle scores `1`; a board where nobody has won yet scores `0`.

### Working backward from the end of the game

The genuinely useful trick is applying this to boards that *aren't* finished yet, by looking ahead to how the game *will* end if both players keep playing well. Malan walks through a position with only two squares left, O's turn, where O can play either of two open squares:

```text
Current board: O to move, 2 squares empty (top-left, bottom-middle)

                        O's choices
              /                              \
     O plays top-left                O plays bottom-middle
              |                                |
     X plays bottom-middle              X plays top-left
     (X completes 3-in-a-row)      (no one completes 3-in-a-row)
              |                                |
        board value = 1                  board value = 0
          (X wins)                          (a tie)

O is MINIMIZING -> compares the two outcomes {1, 0} -> picks the LOWER one
O plays bottom-middle, forcing a tie (value 0) instead of letting X win (value 1)
```

Malan narrates the logic directly: **"O more mathematically and logically can decide: do I want an endpoint of 1 or an endpoint of 0? Well, 0 is probably the better option because that's less than 1, and thus it's the minimal possibility."** Nobody has to guess or trust an instinct: the value of *this* board is fully determined by the values of the boards it can turn into.

That's the whole algorithm, stated as code Malan describes on screen: **"If the player is X, for each possible move, calculate the score for the board at that point in time, and then choose the move with the highest score... else if the player is O, essentially do the same thing but choose the minimal possible score."**

```text
function best_move(board, player):
    if player == "X":                 # X is maximizing
        for each legal move:
            compute the resulting board's value      # via recursion
        play the move with the HIGHEST resulting value
    else:                              # O is minimizing
        for each legal move:
            compute the resulting board's value
        play the move with the LOWEST resulting value
```

Notice that "compute the resulting board's value" for a board that *isn't* finished means running this exact same process again, one level deeper: this is Lesson 16's recursion, applied to a game tree instead of a sorted list. To know a board's value, you need the values of every board it could turn into, all the way down to boards where the game is actually over.

> 🔑 **Minimax doesn't guess: it exhaustively proves the answer.** Every finished board gets a real number (`-1`, `0`, or `1`); every unfinished board's value is computed from the values of every board that follows from it, all the way down.

---

## Part 4: The combinatorial explosion (why brute force breaks)

Minimax feels almost like cheating for a 2-square-left position, because there's only one branch to check. But Malan is honest about what happens as more squares open up:

> "The catch is that the decision tree gets a lot bigger the more and more moves that are left. It gets sort of bigger and bushier, in that it's essentially doubling in size." (David Malan)

Even tic-tac-toe, small as it looks, has a surprisingly large total tree: **"How many ways are there to play tic-tac-toe though? Well, 255,168."** That's still small enough that a computer (or, with real patience, a determined human) can walk the whole tree and solve the game perfectly every time, which is exactly why the code sketch in Part 3 works so well for tic-tac-toe.

Chess and Go are a different story entirely. Counting only the first four moves each player makes (not the whole game, just the *opening*), Malan reports the totals: **"it turns out 85 billion just to get the game started"** for chess, and, for Go, **"266 quintillion possibilities."** His own reaction: **"this is where we sort of as humans, and even with our modern PCs and Macs and phones, kind of have to throw up our hands, because I don't have this many bits of memory in my computer. I don't have this many hours in my life left to actually crunch all of those numbers."**

| Game | Total possibilities counted | Can you brute-force it? |
|---|---|---|
| Tic-tac-toe (full game) | 255,168 | Yes, small enough for a computer (or a patient human) to walk the entire tree |
| Chess (first 4 moves only) | ~85 billion | No, and that's just the *opening* |
| Go (first 4 moves only) | ~266 quintillion | Absolutely not |

This is Lesson 13's Big O lesson, at a much larger scale. Lesson 13 showed you the difference between an algorithm that grows linearly (`O(n)`) and one that grows logarithmically (`O(log n)`). A game tree that "essentially doubles in size" with every move left is growing *combinatorially*, far faster than either of those families, and no amount of extra memory or a faster CPU rescues you from a curve that steep for long.

That's the exact gap machine learning exists to close. As Malan puts it, once brute force is off the table:

> "You instead need to write code that doesn't solve the problem directly but in some sense indirectly. You write code so that the computer figures out how to win... In other words, you train it... this is what we mean nowadays by machine learning: writing code via which machines learn how to solve problems generally by being trained on massive amounts of data, and then, in new problems, looking for patterns via which they can apply those past training data to the problem at hand." (David Malan)

> ✅ **What to do about it:** whenever a problem's tree of possibilities is small and fully known (tic-tac-toe, Breakout's paddle), exhaustive search or a decision tree is the right, simplest tool. The moment the count of possibilities explodes past what any computer could enumerate, that's your signal that you need a system that learns from examples instead of one that checks every possibility.

---

## Part 5: Reinforcement learning (reward, punishment, and epsilon)

**Reinforcement learning** is the machine-learning technique Malan reaches for first, because, as he notes, humans already use it constantly, on each other. He shows a lab recording of a researcher teaching a robot arm to flip a pancake:

> "Here's the key detail with reinforcement learning: behind the scenes, the human is probably rewarding the robot when it does a good job, like, better and better it flips, the more it's rewarded, as by hitting a key and giving it a point... or conversely, every time the robot screws up and drops the pancake on the floor, sort of a proverbial slap on the wrist, a punishment, so that it does less of that behavior the next time." (David Malan)

After roughly 50 trials of this reward-and-punishment loop, the robot reliably flips the pancake, not because anyone programmed the physics of a flip, but because good attempts were reinforced and bad ones were not.

### Explore vs. exploit, and the epsilon variable

Malan then turns to a maze: a player (a yellow dot) needs to reach an exit (a green dot) while avoiding lava pits, moving only up, down, left, or right, with no map. Bumping a lava pit is a punishment (remember: don't do that); reaching the exit is a reward (remember: do more of that). Given enough tries, the player eventually stumbles onto *a* working path and can always repeat it. But Malan asks the obvious follow-up:

> "Is this the best way to play? Am I as good at Super Mario Brothers as I might think? ... I've moved many more times than I need to." (David Malan)

A player that only ever repeats its first working path never discovers a shorter one: the same habit, Malan admits, as always ordering the same good dish at a restaurant instead of risking something that might be even better. This tension has a name:

> "There's this principle of exploring versus exploiting when it comes to using artificial intelligence to solve problems... what if I just sprinkle in a little bit of randomness along the way? And maybe 10% of the time, as represented by this **epsilon** variable, I, as the computer in the story, generate a random number between 0 and 1, and if it's less than that, which is going to happen 10% of the time, I'm going to make a random move instead of one that I know will get me closer to the exit. Otherwise I'll indeed make the move with the highest value." (David Malan)

That's the whole mechanism: on every decision, generate a random number; if it's less than epsilon, **explore** (try something new); otherwise, **exploit** (do whatever has worked best so far). Set epsilon too low, and the agent never finds a better path than the first one it stumbled on. Set it too high, and it wastes too many turns trying random things instead of using what it already knows works.

Applied to an AI actually playing Breakout, this loop produces something Malan calls "a little creepy":

> "If you let it play long enough... you might find a certain trick to the game. Turns out if you're smart enough to break through that top row, you can let the game just play itself for you and maximize your score without even touching the ball, something that I do find a little creepy, that I just figured out how to do that without being told. But it's just a logical continuation of rewarding it for good behavior and punishing it for bad behavior." (David Malan)

No one programmed that trick. Reward-and-punishment, repeated enough times with a bit of exploration mixed in, discovered it on its own.

> 🔑 **Reinforcement learning trades a known recipe for trial, reward, and punishment.** Epsilon is the one number that decides how much of the agent's behavior is "try something new" versus "do what already worked", and getting that balance wrong is the difference between a mediocre, well-worn path and the best solution available.

---

## Part 6: From rules to learning (supervised learning, deep learning, and neural networks)

Reinforcement learning solves problems with no obvious "right answer" to imitate: nobody hands the maze-solver a labeled list of correct moves. But some of Part 1's examples, like spam, actually do have a human supplying the right answer, at least at first:

> "There's specifically a category of learning that's supervised, and we've been using this for years. And in fact, our first example of spam early on was certainly supervised... maybe once a day I hit the keyboard shortcut in Gmail to say, 'ah, this is spam, you should have caught this', and that is training Google's algorithm further." (David Malan)

That's **supervised learning**: a human labels examples (spam or not spam), and the system learns to imitate those labels on new, unseen email. The catch, Malan points out immediately, is that it doesn't scale:

> "The catch is that labeling data in that way manually just doesn't scale very well... it's just not realistic for humans to label millions of pieces of data, billions of pieces of data." (David Malan)

That limitation is exactly what pushes the field toward **deep learning**, training systems that find their own patterns in raw, unlabeled data, using **neural networks**, loosely inspired by neurons in the brain: simple units, drawn as circles, connected by lines ("edges") that carry a signal from one to the next.

### A tiny neural network, solving a real problem

Malan builds the smallest possible example: a two-dimensional grid of dots, each either blue or red, with no rule given for which color goes where. A tiny network with just three neurons (one for the X-coordinate, one for the Y-coordinate, and one for the output) has to *discover* the rule from examples alone:

```text
      x  (X-coordinate) ---\
                             \
                              o----> output: predict "blue" or "red"
                             /
      y  (Y-coordinate) ---/
```

Given only a couple of dots, the best the network can do is guess a rough dividing line; given more dots, that line can be adjusted, angled, even curved, to fit the data better. Mathematically, this whole network reduces to finding three numbers, called **parameters** (or **weights**): **"an A, a B, and a C,"** plugged into the formula `A·x + B·y + C`. Malan gives the rule for turning that formula into a prediction: **"if that value mathematically gives me a number greater than 0, predict it's going to be blue; otherwise predict it's going to be red."**

Real neural networks scale this same idea up enormously: not three neurons, but billions, each edge carrying its own numeric weight, tuned automatically by training on vast amounts of data. And that scale comes at a cost of transparency:

> "Even though there'd be millions, billions of numbers going on there, I can't tell you what this neuron represents or why this edge has this weight. It's because of the massive amount of training data: that's just how the math works out." (David Malan)

That is the honest, slightly uncomfortable truth about deep learning: nobody, not even the people who built the network, can point to one neuron and say exactly what it means. The network works because the training data, in aggregate, pushed billions of numbers into a configuration that happens to predict well, not because a human designed each piece.

> ✅ **What to do about it:** when labeled data is scarce or too expensive to gather at scale, that's the signal to reach for deep learning instead of supervised learning, but expect to trade away the ability to explain *why* any single decision came out the way it did.

---

## Part 7: Inside an LLM (embeddings, attention, GPT, and why AI hallucinates)

The same neural-network idea, scaled up to enormous size and trained on text instead of colored dots, is what powers **large language models** (LLMs) like the GPT behind CS50's duck. GPT itself stands for "generative pre-trained transformer", a mouthful, but Malan is quick to note the familiar half: **"there's the GPT in ChatGPT."**

Before an LLM can reason about words, it needs a way to represent them as numbers. Malan uses a deliberately hard example (a paragraph about Massachusetts, ending on the (unstated) word "Boston") to show why this used to be difficult: the key words ("Massachusetts," "capital") are far apart in the sentence, and the same idea gets referred to with different words ("Massachusetts," then just "the state"), so an AI needs some way to notice that those far-apart words are actually connected. The fix has two parts. First, every word gets converted into a list of numbers, called an **embedding**:

> "The word Massachusetts, if you encode it in a certain way, is going to be represented with an array or vector of numbers, floating point values, so many so that the word Massachusetts, in one model, would use 1,536 floating point numbers to represent Massachusetts, essentially, in an N-dimensional space." (David Malan)

Second, the model computes **attention**, a measure of how strongly each word in a sentence relates to every other word:

> "Attention is calculated based on all of that data, whereby... the thicker lines imply more of a relationship between those two words. So Massachusetts and state is inferred as having a thicker line, a higher attention from one word to the other, whereas 'our' and 'and' and 'the's have thinner lines, because they're just not as much signal to the AI as to what the answer to this question is." (David Malan)

Embeddings plus attention are what let a model connect "the state's capital" all the way back to "Massachusetts," even though many other words sit in between. With that context assembled, Malan describes what the model is actually doing, in the end, with brutal simplicity:

> "All these LLMs, large language models, are just statistical models, like, what is the highest probability word that it should spit out at the end of this paragraph, based on all of the Reddit posts and Google search results and encyclopedias and Wikipedias that it's found and trained on online." (David Malan)

Almost always, that highest-probability word is correct: for the Massachusetts example, "Boston." But "highest probability" is not the same thing as "guaranteed true," and that gap has a name:

> "Even CS50's own duck is fallible, even though we've written lots of code to try to put downward pressure on those mistakes, and those mistakes are what we'll call **hallucinations**, where the AI just makes something up, perhaps because some crazy human on the internet made something up and it was interpreted as authoritative, or just by bad luck, because of a bit of that exploration... the AI sort of veered this way... and spit out an answer that, in fact, is not correct." (David Malan)

That's the whole mechanism behind a hallucination: it isn't a bug in the ordinary sense of broken code. It's the entirely predictable result of a system that always outputs its single most probable next word: a system that, occasionally, has been trained on bad information, or simply lands on a less likely (and wrong) word instead of the right one. Knowing that is exactly what makes Lesson 32's advice (read AI output critically, don't accept it on faith) make sense at a mechanical level, not just as a warning.

Malan closes the lecture on a fittingly imperfect note: a recitation of Shel Silverstein's poem "The Homework Machine," about a machine that answers any homework problem "in ten seconds' time," only for the child in the poem to ask it a simple addition problem and get back a nonsense answer: **"9 plus 4, and the answer is 33?"**, a decades-old joke about a machine that answers instantly and confidently, and is still sometimes wrong.

> 🔑 **A hallucination is a structural property of "predict the most likely next word," not a rare glitch.** The same statistical machinery that makes an LLM useful almost all of the time is exactly what occasionally makes it confidently wrong.

---

## Key takeaways

1. **Most everyday "smart" features are not hardcoded rulebooks.** Spam filters, handwriting recognition, recommendations, and voice assistants all replace an impossibly long `if`/`else` chain with patterns learned from data.
2. **A decision tree is just `if`/`else`, drawn as a tree.** Pong and Breakout's paddles can play perfectly with three yes/no questions, no learning required.
3. **Minimax scores a finished game (`-1`/`0`/`1`) and works backward.** X maximizes, O minimizes, and every unfinished board's value comes from recursively scoring the boards that follow it, exactly like Lesson 16's recursion.
4. **Combinatorial explosion (255,168 tic-tac-toe games; ~85 billion chess openings; ~266 quintillion Go openings) is Big O's warning at war-story scale.** Once a game tree "doubles in size" with every move, brute force stops being an option no matter how fast your computer is.
5. **Reinforcement learning replaces exhaustive search with reward and punishment**, and epsilon controls the balance between exploiting a known-good path and exploring for a possibly better one.
6. **Neural networks tune millions or billions of numeric parameters from training data**, rather than being hand-programmed rule by rule, which is powerful, and also why nobody can fully explain any single decision they make.
7. **Hallucinations are a structural side effect of predicting the statistically likely next word**, not a rare bug: the exact mechanism behind Lesson 32's warning to always read AI output critically.

## Common pitfalls

- ❌ Assuming every "smart" feature must be a neural network. Many everyday features (a game paddle, a simple rule engine) are just decision trees: check whether the questions can be fully enumerated before reaching for machine learning.
- ❌ Thinking minimax "peeks ahead a little." It doesn't estimate: it walks the *entire* remaining game tree and scores every possible ending, which is exactly why it stops being practical once the tree explodes (Part 4).
- ❌ Treating "explore sometimes" as a vague vibe instead of an actual mechanism. Epsilon is a concrete probability, checked with an actual random-number comparison on every single decision, not an occasional mood.
- ❌ Treating a hallucination as a rare bug you can fully eliminate. It's a structural property of predicting the most probable next word, not a lookup error, which is why even a well-engineered system like CS50's duck remains fallible.

---

## 🛠️ Capstone Project: Solve It Like a Machine

> This is the main hands-on project for the lesson. No accounts, tools, or spending required: just paper, a pencil, two six-sided dice, and (for the stretch) a way to generate a number from 1 to 10. You'll prove, by hand, that minimax genuinely solves tic-tac-toe; write a real decision tree as real code; and, if you want to go further, watch the explore-vs-exploit trade-off change your own score across 20 rounds.

### What you will build

Three small, independent artifacts:

1. **A fully hand-drawn minimax tree** for a specific tic-tac-toe endgame with three empty squares, with every leaf scored and every intermediate value backed up correctly, proving which move is objectively best.
2. **A real Python file**, `paddle.py`, implementing the Breakout paddle's decision tree from Part 2 as runnable `if`/`elif`/`else` code.
3. **(Stretch)** A hand-run, 20-round explore-vs-exploit experiment comparing total scores across three different epsilon values.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Scoring a board -1/0/1 (Part 3) | Milestone 1: scoring every leaf of your hand-drawn tree |
| Minimax recurses (Part 3, Lesson 16) | Milestone 1: backing values up from leaves to the root |
| Decision trees are if/else (Part 2, Lesson 7) | Milestone 2: the paddle's tree becomes real Python |
| Epsilon and explore vs. exploit (Part 5) | Milestone 3 (stretch): comparing epsilon = 0, 0.1, and 0.5 |

### Milestones (build them in order, each one works on its own)

1. **Hand-draw the full minimax tree and prove the optimal move.** Use this exact board (numbering cells 1-9, left to right, top to bottom, like a phone dial), with **X to move** and three empty squares remaining at 4, 6, and 8:

   ```text
    O | O | X
   -----------
      | X |  
   -----------
    O |   | X
   ```

   (Cell 1 = O, 2 = O, 3 = X, 4 = empty, 5 = X, 6 = empty, 7 = O, 8 = empty, 9 = X.) On paper, draw all three of X's opening options (playing 4, 6, or 8) as the top level of a tree. For each option that doesn't immediately end the game, draw O's possible replies below it, and keep going until every branch ends in a finished board. Score every finished (leaf) board `-1` (O wins), `0` (tie), or `1` (X wins). Then back the values up the tree: at every level where it's **X's** turn, the value is the **maximum** of the branches below it; at every level where it's **O's** turn, the value is the **minimum**. Write down, in one sentence, which of X's three opening moves is objectively optimal and why: you should be able to point to a real, immediate three-in-a-row as part of your proof.
2. **Turn the paddle's decision tree into real code.** In a new file `paddle.py`, write a function `move_paddle(ball_x, paddle_x)` that returns the string `"left"`, `"right"`, or `"stay"`, using the exact three-question tree from Part 2 (is the ball left of the paddle? is it right of the paddle? otherwise, stay). Test it by hand with at least five different `(ball_x, paddle_x)` pairs you choose yourself, including a case where they're equal, and confirm each returns the answer you'd expect.
3. **Stretch goal: run a 20-round explore-vs-exploit experiment.** Using two six-sided dice, secretly assign one die a "win" threshold of 1-4 (about 67%) and the other a threshold of 1-3 (about 50%): write these two thresholds on a slip of paper, fold it, and don't look again until Step 6. Call them Machine A and Machine B, but don't tell yourself which threshold belongs to which; you're only allowed to learn each machine's win rate by actually "playing" it. For each of three separate 20-round runs (one for epsilon = 0, one for epsilon = 0.1, one for epsilon = 0.5): each round, generate a number from 1-10 (roll two dice and take one, or use any random-number source); if that number is less than or equal to epsilon × 10, **explore** (play whichever machine you have less data on so far); otherwise **exploit** (play whichever machine currently has the better observed win rate from your own tally, picking randomly on a tie). Roll the corresponding die once to see if that round wins or loses, and update your running win/play tally for that machine. After 20 rounds, record the total wins out of 20 for that epsilon value, then repeat for the other two epsilon values. Finally, unfold your paper and compare your total wins across epsilon = 0, 0.1, and 0.5.

### How you will know you are done

- ✅ Your hand-drawn tree for Milestone 1 shows all three of X's opening moves, every reply beneath each non-terminal one, and a score on every leaf.
- ✅ You correctly identify that **playing cell 6** is X's optimal move (it completes column 3 (cells 3, 6, 9) for an immediate win, value `+1`), while playing 4 only forces a tie (value `0`) and playing 8 lets O force a win (value `-1`) if O replies optimally.
- ✅ `paddle.py` returns `"left"`, `"right"`, or `"stay"` correctly for every one of your five hand-picked test cases.
- ✅ (Stretch) You have three real total-win counts, one per epsilon value, and can say in one sentence whether a higher epsilon helped or hurt your score over just 20 rounds.

> 💡 **Keep yourself honest:** for Milestone 1, don't skip drawing a branch just because it "looks worse": minimax's whole proof rests on actually scoring every option, not on trusting your gut about which one wins. That discipline (check every branch, don't assume) is the same rigor you'll want later when you can't just eyeball whether a database query or an AI-suggested fix is correct.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Score three boards (foundational)
Score each of these three *finished* tic-tac-toe boards as `-1`, `0`, or `1`, using the scoring rule from Part 3 (X wins = `1`, O wins = `-1`, nobody wins = `0`): (a) `X X X / O O _ / _ _ _`, (b) `X O X / O X O / O X O`, (c) `O O O / X X _ / X _ _`. For each, name which line (row, column, or diagonal) determines the score.

### Exercise 2: Explore a tiny maze (intermediate)
On paper, draw a 4×4 grid. Mark one cell "start," one cell "exit," and two other cells "lava." First, trace a path from start to exit using only "always move toward the exit, avoiding lava" (pure exploitation): count how many moves it takes. Then trace a second path where, at exactly one random step along the way, you deliberately move in a different direction than the exploit rule would pick (simulating one exploration step) before returning to exploiting. Compare the two path lengths and write one sentence about whether the detour ever paid off.

### Exercise 3: Hand-fit a blue/red classifier (advanced)
Here are five points on a grid, each labeled blue or red: `(1, 1) blue`, `(2, 3) blue`, `(1, 4) blue`, `(4, 1) red`, `(5, 2) red`. Using the formula from Part 6 (`A·x + B·y + C`, predicting blue if the result is greater than 0 and red otherwise), pick your own whole-number values for `A`, `B`, and `C` and check, by computing the formula for all five points, whether your line correctly separates every blue point from every red point. If it doesn't, adjust one parameter and try again.

---

## Cheat sheet

```text
INVISIBLE AI, EVERYDAY EXAMPLES
  Spam filters, handwriting recognition, recommendations, voice assistants
  -> none of them run on one giant hardcoded if/else

DECISION TREE  =  if/else, drawn as a tree
  Small, fixed number of questions -> no learning needed (Pong, Breakout paddle)

MINIMAX (tic-tac-toe)
  Score every FINISHED board:  O wins = -1   tie = 0   X wins = +1
  X's turn  -> take the MAXIMUM of the options below
  O's turn  -> take the MINIMUM of the options below
  Recursive: a board's value = the values of every board that follows it

COMBINATORIAL EXPLOSION
  Tic-tac-toe (whole game): 255,168 possibilities        -- brute-forceable
  Chess (first 4 moves only): ~85 billion possibilities   -- not brute-forceable
  Go (first 4 moves only): ~266 quintillion possibilities -- nowhere close

REINFORCEMENT LEARNING
  Try an action -> reward (do more of that) or punishment (do less of that)
  EPSILON = probability of exploring (trying something new) instead of
            exploiting (doing what already worked best)
  epsilon too low  -> stuck with the first okay solution found
  epsilon too high -> wastes turns on things that don't pay off

SUPERVISED -> DEEP LEARNING
  Supervised: humans label the data (you marking email as spam)
  Deep learning: no human labels each example -- a neural network finds
  its own patterns instead, because labeling doesn't scale to billions of items

NEURAL NETWORK, SMALLEST VERSION
  inputs (x, y) -> one output neuron
  formula:  A*x + B*y + C
  if result > 0: predict blue   else: predict red
  real networks: billions of these "weights," tuned by training data,
  impossible for a human to interpret one at a time

LLMs (GPT, Claude, Gemini, CS50's duck)
  word -> embedding (a long list of numbers, e.g. 1,536 per word)
  attention -> how strongly each word relates to every other word
  output -> the single highest-probability next word, over and over
  HALLUCINATION = a confident, wrong answer -- a structural side effect
  of "predict the likely next word," not a rare bug
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 7 (Conditionals and loops):** the `if`/`else if`/`else` chain from that lesson is exactly what a decision tree becomes once you write it as code (Part 2). This lesson just draws it as branches first.
- **Earlier, Module 4 · Lesson 13 (Thinking in running time: Big O):** combinatorial explosion (Part 4) is that lesson's "how does this scale?" question, at a scale (255,168 to 266 quintillion) that makes the difference between O(n) and O(log n) look tame by comparison.
- **Earlier, Module 4 · Lesson 16 (Recursion and merge sort):** minimax (Part 3) recurses exactly the way merge sort does: a board's value depends on the values of smaller sub-problems (the boards that follow it), all the way down to a base case.
- **Earlier, Module 9 · Lesson 32 (Using AI well):** this lesson delivers on that lesson's closing promise, going underneath the prompts and APIs to the decision trees, reinforcement learning, and neural networks that make the duck, Copilot, and every other AI tool possible.
- **Next, Module 10 · Lesson 34 (How the internet works):** a different topic: the course moves from AI to networking. Nothing from this lesson is required there.
- **Later, your final project:** you won't hand-code minimax or a neural network into your database-backed web app, but the habit of mapping a decision to explicit, enumerable branches *before* writing a line of code (Part 2) is exactly how you'll design server-side logic like access checks and form validation when you get there.

---

*Source: "CS50x 2026 - Artificial Intelligence" by David J. Malan, Harvard University. Quotes are transcribed from the talk; obvious auto-transcription artifacts (stray words, garbled game names, and misheard phrasing) have been silently corrected for readability while preserving Malan's exact wording and meaning wherever possible. The closing poem, "The Homework Machine," is the copyrighted work of Shel Silverstein (from *A Light in the Attic*, 1981) and is only briefly excerpted here; seek out the full poem directly if you'd like to read it. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
