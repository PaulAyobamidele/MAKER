# Breaking Down MAKER: How to Solve a Million-Step Task with Zero Errors (Paper Reproduction)

## The Big Idea

Imagine you're building a LEGO skyscraper. Would you rather:

- **Option A**: Have one person build the entire thing in one go (they'll probably mess up somewhere)
- **Option B**: Break it into tiny pieces, have multiple people check each piece, and only proceed when everyone agrees it's correct

MAKER chooses Option B. It's a system that solves tasks requiring over 1 million LLM steps **with zero errors** by:

1. Breaking tasks into the **smallest possible steps**
2. Having multiple AI agents **vote** on each step
3. **Rejecting** suspicious answers before they cause problems

---

## 🏗️ The Problem: Why LLMs Fail at Long Tasks

**The Math is Brutal:**

- If an LLM has a 1% error rate per step (which sounds good!)
- After 100 steps: 63% chance of failure
- After 1,000 steps: 99.996% chance of failure
- After 1,000,000 steps: You will definitely fail

**The Tower of Hanoi Test:**

- Classic puzzle where you move disks between pegs
- 20 disks = 1,048,575 moves required
- State-of-the-art LLMs couldn't get past ~500 steps before catastrophic failure

---

## 🔬 The Solution: Three Core Principles

### 1️⃣ Maximal Agentic Decomposition (MAD)

**What it means:** Break the task into the smallest possible chunks—one decision per agent.

**Traditional approach:**

