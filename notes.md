# LLMs Don’t Scale the Way You Think They Do  
## When Large Language Models Are the Wrong Tool

> **TL;DR**  
> Large Language Models (LLMs) are powerful, but they fail catastrophically on long-horizon, multi-step reasoning tasks due to unavoidable error accumulation. Scaling model size or context length is not a fundamental solution. Collective intelligence systems—such as MAKER—offer an orthogonal, mathematically grounded path to reliability.

---

## Motivation

Let me start with a simple, unintuitive observation.

There exist tasks that:
- Cost **$10–$15** to solve using an LLM
- Can be solved with **5–8 lines of classical code**
- Cost **$0** in compute

If you have a basic computer science background, your reaction is probably:  
**“That’s nonsense.”**

You would be correct.

Using an LLM for such tasks is like:
- Using an axe to open a bottle of beer  
- Expensive  
- Slow  
- Unreliable  

So why does this happen—and why does it matter?

---

## The Core Problem: Autoregressive Error Accumulation

LLMs are undeniably intelligent. However, they are:
- Trained
- Evaluated
- Benchmarked  

on tasks requiring **at most tens of reasoning steps**.

Real-world tasks are different.

### The Math (Not a Bug)

Assume a strong LLM has:
- **99% accuracy per reasoning step**

Then:

| Steps | Probability of Success |
|-----|------------------------|
| 100 | ~36.6% |
| 1,000 | ~0% |
| 1,000,000 | Impossible |

Errors **compound**.  
They **snowball**.  
Eventually, they **dominate**.

This is not a failure of engineering effort.  
It is a consequence of probability theory.

---

## A Realistic Example

Consider a mundane task:

> **Filing a comprehensive small business tax return**

Despite the task being well within human capability, the reasoning chain quickly becomes:
- Deep
- Branching
- Multi-level  

In practice, hallucinations emerge around **step ~100**, long before task completion.

This phenomenon is known as:

> **Autoregressive Error Accumulation**

Billions of dollars are currently being spent attempting to fix this by:
- Increasing model size
- Extending context windows
- Fine-tuning

Each approach helps marginally—but introduces new trade-offs:
- Attention dilution
- Loss of generalization
- Escalating costs

This raises a critical question:

> **Is chasing the “perfect” model even a realistic or cost-justified goal?**

---

## A Different Direction: Collective Intelligence

If you haven’t read it yet, see first:

- **Collective Intelligence: The Missing Ingredient for Reliable AI**  
- **Collective Intelligence: An Orthogonal Path to Reliable AI**

These ideas lead directly to a remarkable framework.

---

## MAKER: Solving Long-Horizon Reasoning

A team led by **Elliot Meyerson** asked a deceptively simple question:

> *How can we solve tasks with over a million dependent LLM steps without error?*

The answer was **MAKER**.

---

## An Intuitive Analogy

Imagine a 12-hour flight from London to New York.

### Option 1: One Super Pilot
- A literal genius
- Flies alone for 720 minutes straight

If they:
- Blink
- Misread one signal in hour eight

You end up in the ocean.

### Option 2: A Standard Cockpit Crew
- Captain
- Co-pilot
- Flight computer

Every action is:
- Verified
- Challenged
- Confirmed

The choice is obvious.

That difference is **collective intelligence**.

---

## Why the Tower of Hanoi Matters

Recall the “ridiculous” Tower of Hanoi example.

Solving Hanoi with **20 disks** requires:

2^20 − 1 = 1,048,575 steps


For a single LLM, this is a guaranteed failure.

Not because the model is weak—but because the task is *long*.

This makes Hanoi a **high-stress proxy** for real-world reasoning systems.

---

## MAKER’s Core Ideas

### 1. Extreme Decomposition  
*(Maximal Agentic Decomposition)*

- Break tasks into the smallest possible units
- Each step becomes a **micro-task**
- No agent reasons globally
- Each agent focuses on one trivial decision

**Goal:**  
Keep every step within the model’s high-confidence regime (~99%).

---

### 2. Error Correction via Voting  
*(First-to-Ahead-by-K)*

For every step:
- Query **multiple independent agents**
- Collect candidate answers
- Tally votes

But do **not** accept a simple majority.

Instead:
- Wait until one option is **K votes ahead**

This is:
- Statistics
- Redundancy
- The wisdom of crowds

---

### 3. Red-Flagging (Adversarial Checking)

Before a step is accepted:
- A specialized agent intervenes
- Its sole role is to **find reasons the step might fail**

If it detects inconsistency:
- The step is rejected
- Re-sampled

This is the final safety gate.

---

## Why This Works

With just **5 independent agents**:
- Error probability per step drops from  
  **1 in 100 → ~1 in 100,000**

Across **one million steps**:
- A single super-model collapses early
- MAKER continues:
  - Self-correcting
  - Detecting errors
  - Recovering from failures

---

## The Bigger Picture: Smarter Systems, Not Smarter Models

MAKER is not about building:
- Bigger models
- Longer chains of thought

It is about engineering **systems** that:
- Decentralize control
- Preserve independence
- Aggregate decisions
- Enable emergence
- Correct errors continuously

This mirrors how:
- Biological intelligence works
- Human institutions succeed
- Safety-critical systems are built

---

## Final Takeaway

Big Tech is currently betting on **super-models** that “think longer.”

But if the per-step error rate remains non-zero, longer thinking only delays failure.

**MAKER demonstrates an orthogonal truth:**

> The future of reliable AI lies not in smarter individuals,  
> but in smarter collectives.

We are finally engineering intelligence the way nature always has—  
**collectively.**

---
