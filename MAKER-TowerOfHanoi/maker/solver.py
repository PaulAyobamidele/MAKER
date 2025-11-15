
from tqdm import tqdm
from typing import List
from maker.voting import do_voting

def generate_solution(client, initial_state: List[List[int]], 
                      num_steps: int, k: int, num_disks: int,
                      system_prompt: str, user_template: str) -> List[List[int]]:
    """Algorithm 1: generate_solution"""
    
    actions = []
    state = [peg[:] for peg in initial_state]
    prev_move = None
    
    print(f"Starting MAKER with k={k}, {num_steps} steps...")
    print(f"Initial state: {state}")
    
    for step in tqdm(range(num_steps), desc="Solving Tower of Hanoi"):
        move, state = do_voting(client, state, prev_move, k, num_disks, 
                               system_prompt, user_template)
        actions.append(move)
        prev_move = move
        
        if step < 10 or step % 100 == 0:
            tqdm.write(f"Step {step}: Move {move}, State: {state}")
    
    print(f"Final state: {state}")
    return actions


def verify_solution(actions: List[List[int]], num_disks: int) -> bool:
    """Verify solution"""
    
    state = [list(range(num_disks, 0, -1)), [], []]
    print(f"\nVerifying {len(actions)} moves...")
    
    for i, (disk, from_peg, to_peg) in enumerate(actions):
        if not state[from_peg]:
            print(f"❌ Step {i}: Peg {from_peg} is empty")
            return False
        
        if state[from_peg][-1] != disk:
            print(f"❌ Step {i}: Top disk is {state[from_peg][-1]}, not {disk}")
            return False
        
        if state[to_peg] and state[to_peg][-1] < disk:
            print(f"❌ Step {i}: Cannot place {disk} on {state[to_peg][-1]}")
            return False
        
        state[from_peg].pop()
        state[to_peg].append(disk)
        
        if i < 7:
            print(f"   Move {i}: {[disk, from_peg, to_peg]} → {state}")
    
    target_state = [[], [], list(range(num_disks, 0, -1))]
    
    if state == target_state:
        print(" Solution verified!")
        return True
    else:
        print(f" Final: {state} ≠ {target_state}")
        return False
