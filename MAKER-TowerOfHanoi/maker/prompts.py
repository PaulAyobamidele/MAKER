# maker/prompts.py

# ======================================================================
# System prompt (unchanged)
# ======================================================================

SYSTEM_PROMPT = """You are a helpful assistant. Solve this puzzle for me.

There are three pegs and n disks of different sizes stacked on the first peg. The disks are
numbered from 1 (smallest) to n (largest). Disk moves in this puzzle should follow:
1. Only one disk can be moved at a time.
2. Each move consists of taking the upper disk from one stack and placing it on top of
   another stack.
3. A larger disk may not be placed on top of a smaller disk.

The goal is to move the entire stack to the third peg.

Requirements:
- Pegs are 0-indexed (0,1,2).
- You MUST output the next move ONLY in this format:
  '''move = [disk id, from peg, to peg]'''
- You MUST output the resulting next state ONLY in this format:
  '''next_state = [[...], [...], [...]]'''
"""


# ======================================================================
# USER TEMPLATES (for even/odd disk rotation rules)
# ======================================================================

ODD_TEMPLATE = """Rules:
- Only one disk can be moved at a time.
- Only the top disk can be moved.
- A larger disk may not be placed on top of a smaller disk.
- The full solution must move all disks from peg 0 to peg 2.
- For ODD number of disks, disk 1 always moves COUNTER-CLOCKWISE:
    0 → 2 → 1 → 0 → 2 → 1 → ...

Movement rule:
- If the previous move DID NOT involve disk 1, move disk 1 counter-clockwise.
- Else (if disk 1 was moved previously), make the only legal move that is NOT disk 1.

Previous move: {previous_move}
Current state: {current_state}

Provide exactly:
'''move = [disk id, from peg, to peg]'''
'''next_state = [[...], [...], [...]]'''
"""


EVEN_TEMPLATE = """Rules:
- Only one disk can be moved at a time.
- Only the top disk can be moved.
- A larger disk may not be placed on top of a smaller disk.
- The full solution must move all disks from peg 0 to peg 2.
- For EVEN number of disks, disk 1 always moves CLOCKWISE:
    0 → 1 → 2 → 0 → 1 → 2 → ...

Movement rule:
- If the previous move DID NOT involve disk 1, move disk 1 clockwise.
- Else (if disk 1 was moved previously), make the only legal move that is NOT disk 1.

Previous move: {previous_move}
Current state: {current_state}

Provide exactly:
'''move = [disk id, from peg, to peg]'''
'''next_state = [[...], [...], [...]]'''
"""


# ======================================================================
# get_user_template (required by main.py)
# ======================================================================

def get_user_template(num_disks: int) -> str:
    """Select correct template based on parity of number of disks."""
    if num_disks % 2 == 1:
        return ODD_TEMPLATE   # Odd → counter-clockwise
    else:
        return EVEN_TEMPLATE  # Even → clockwise
