import re
import ast
from typing import List, Tuple

def parse_move_state_flag(response_text: str, num_disks: int) -> Tuple[List[int], List[List[int]]]:
    """Red-flagging parser: strict format enforcement"""
    
    def _validate_move(move):
        if not isinstance(move, list) or len(move) != 3 or not all(isinstance(x, int) for x in move):
            raise ValueError("'move' must be a list of exactly 3 integers.")
        if not (0 <= move[1] <= 2 and 0 <= move[2] <= 2):
            raise ValueError(f"Peg indices must be 0-2, got {move}")
        if move[1] == move[2]:
            raise ValueError(f"Cannot move from peg to same peg: {move}")
        return move

    def _validate_state(state, n):
        if not (isinstance(state, list) and len(state) == 3 and all(isinstance(t, list) for t in state)):
            raise ValueError("'next_state' must be a list of three lists.")
        flat = [x for t in state for x in t]
        if not all(isinstance(x, int) for x in flat):
            raise ValueError("All entries in 'next_state' must be integers.")
        if len(flat) != n or set(flat) != set(range(1, n + 1)):
            missing = sorted(set(range(1, n + 1)) - set(flat))
            extra = sorted(set(flat) - set(range(1, n + 1)))
            raise ValueError(f"State must contain 1..{n} exactly once. "
                           f"Missing: {missing or '[]'}, Extras: {extra or '[]'}")
        
        # Validate each peg is sorted (larger disks at bottom)
        for i, peg in enumerate(state):
            if peg != sorted(peg, reverse=True):
                raise ValueError(f"Peg {i} has invalid disk order: {peg}")
        
        return state

    # Match square brackets
    move_pat = re.compile(r"(?is)\bmove\b\s*=\s*(\[[^\[\]]*\])")
    state_pat = re.compile(
        r"(?is)\bnext_state\b\s*=\s*(\[\s*\[[^\[\]]*\]\s*,\s*\[[^\[\]]*\]\s*,\s*\[[^\[\]]*\]\s*\])"
    )

    move_matches = list(move_pat.finditer(response_text))
    if not move_matches:
        raise ValueError("No 'move = [...]' found.")
    move_str = move_matches[-1].group(1)

    state_matches = list(state_pat.finditer(response_text))
    if not state_matches:
        raise ValueError("No 'next_state = [[...],[...],[...]]' found.")
    state_str = state_matches[-1].group(1)

    try:
        move = ast.literal_eval(move_str)
    except Exception as e:
        raise ValueError("Could not parse 'move' as a Python list.") from e

    try:
        next_state = ast.literal_eval(state_str)
    except Exception as e:
        raise ValueError("Could not parse 'next_state' as Python lists.") from e

    return _validate_move(move), _validate_state(next_state, num_disks)


def validate_transition(current_state, move, next_state):
    """
    ✅ FIXED: Validates that next_state is EXACTLY the result of applying move to current_state.
    
    Key fixes:
    1. Check legality on CURRENT state (before move)
    2. Properly simulate the transition
    3. Compare simulated state with LLM's next_state
    """
    disk, from_peg, to_peg = move

    # 1. Validate the move is legal on CURRENT state
    if not current_state[from_peg]:
        raise ValueError(f"Invalid move: Peg {from_peg} is empty")

    if current_state[from_peg][-1] != disk:
        raise ValueError(
            f"Invalid move: Top disk on peg {from_peg} is "
            f"{current_state[from_peg][-1]}, not {disk}"
        )

    # 2. Check destination legality on CURRENT state (before move)
    if current_state[to_peg] and current_state[to_peg][-1] < disk:
        raise ValueError(
            f"Invalid move: Cannot place disk {disk} onto smaller disk "
            f"{current_state[to_peg][-1]} on peg {to_peg}"
        )

    # 3. Simulate applying the move
    simulated = [peg[:] for peg in current_state]  # Deep copy
    simulated[from_peg].pop()
    simulated[to_peg].append(disk)

    # 4. Verify LLM's next_state matches simulation
    if simulated != next_state:
        raise ValueError(
            f"Invalid next_state: Does not match applying move {move}.\n"
            f"Expected: {simulated}\n"
            f"Got:      {next_state}"
        )

    return True