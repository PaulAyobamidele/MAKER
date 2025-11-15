import time
import json
from collections import defaultdict
from typing import List, Tuple
import openai
from maker.parser import parse_move_state_flag, validate_transition
from maker.config import TEMPERATURE_FIRST, TEMPERATURE_REST, MAX_TOKENS, USE_RED_FLAGGING, MODEL

def get_vote(client, current_state: List[List[int]], prev_move: List[int],
             temperature: float, num_disks: int, system_prompt: str, 
             user_template: str) -> Tuple[List[int], List[List[int]]]:
    """Algorithm 3: get_vote with proper previous move formatting"""
    
    attempt = 0
    max_attempts = 50
    
    while attempt < max_attempts:
        attempt += 1
        try:
            # Format previous move to help LLM understand
            if prev_move is None or prev_move == [0, 0, 0]:
                prev_move_str = "None (this is the first move)"
            else:
                disk = prev_move[0]
                if disk == 1:
                    prev_move_str = f"{prev_move} (disk 1 was moved)"
                else:
                    prev_move_str = f"{prev_move} (disk {disk} was moved, NOT disk 1)"
            
            # Call the LLM
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_template.format(
                        previous_move=prev_move_str,
                        current_state=current_state
                    )}
                ],
                temperature=temperature,
                max_tokens=MAX_TOKENS
            )

            response_text = response.choices[0].message.content

            # Parse and validate
            move, next_state = parse_move_state_flag(response_text, num_disks)
            validate_transition(current_state, move, next_state)

            return move, next_state

        except ValueError as e:
            if USE_RED_FLAGGING:
                if attempt % 10 == 0:
                    print(f"  Resampling (attempt {attempt}): {str(e)[:80]}")
                continue
            else:
                raise
        except Exception as e:
            print(f"API Error: {e}, retrying...")
            time.sleep(1)
            continue
    
    raise RuntimeError(f"Failed after {max_attempts} attempts")


def do_voting(client, state: List[List[int]], prev_move: List[int],
              k: int, num_disks: int, system_prompt: str, user_template: str) -> Tuple[List[int], List[List[int]]]:
    """Algorithm 2: do_voting"""
    
    votes = defaultdict(int)
    vote_mapping = {}

    # First vote (greedy)
    move, next_state = get_vote(
        client, state, prev_move, TEMPERATURE_FIRST, num_disks, 
        system_prompt, user_template
    )
    vote_key = json.dumps(move)
    votes[vote_key] = 1
    vote_mapping[vote_key] = (move, next_state)

    max_other = max([v for vk, v in votes.items() if vk != vote_key], default=0)
    if votes[vote_key] >= k + max_other:
        return move, next_state

    # Continue voting
    round_num = 1
    while round_num < 100:
        round_num += 1
        move, next_state = get_vote(
            client, state, prev_move, TEMPERATURE_REST, num_disks,
            system_prompt, user_template
        )
        vote_key = json.dumps(move)
        votes[vote_key] += 1
        vote_mapping[vote_key] = (move, next_state)

        max_other = max([v for vk, v in votes.items() if vk != vote_key], default=0)
        if votes[vote_key] >= k + max_other:
            if round_num > 10:
                print(f"  Note: {round_num} voting rounds needed")
            return vote_mapping[vote_key]
    
    # Fallback
    winner_key = max(votes, key=votes.get)
    print(f"  Warning: Voting timeout. Votes: {dict(votes)}")
    return vote_mapping[winner_key]
