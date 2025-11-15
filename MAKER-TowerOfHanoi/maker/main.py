
import time
import openai

from maker.config import (
    OPENAI_API_KEY,
    NUM_DISKS,
    K_THRESHOLD,
    MODEL,
    USE_RED_FLAGGING,
    TEMPERATURE_FIRST,
    TEMPERATURE_REST,
    MAX_TOKENS
)


from maker.prompts import SYSTEM_PROMPT, get_user_template


from maker.solver import generate_solution, verify_solution


def main():
    if not OPENAI_API_KEY:
        print("ERROR: Please set OPENAI_API_KEY in maker/config.py")
        return

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    initial_state = [list(range(NUM_DISKS, 0, -1)), [], []]

    num_steps = 2**NUM_DISKS - 1

    user_template = get_user_template(NUM_DISKS)

    print("=" * 70)
    print("MAKER: Massively Decomposed Agentic Processes")
    print("=" * 70)
    print(f"Model: {MODEL}")
    print(f"Number of disks: {NUM_DISKS}")
    print(f"Strategy: {'ODD = counter-clockwise' if NUM_DISKS % 2 else 'EVEN = clockwise'}")
    print(f"Total optimal steps: {num_steps}")
    print(f"Voting threshold k = {K_THRESHOLD}")
    print(f"Temperature_first = {TEMPERATURE_FIRST}, Temperature_rest = {TEMPERATURE_REST}")
    print(f"Red-flagging enabled: {USE_RED_FLAGGING}")
    print("=" * 70)

    start = time.time()

    actions = generate_solution(
        client,
        initial_state,
        num_steps,
        K_THRESHOLD,
        NUM_DISKS,
        SYSTEM_PROMPT,
        user_template
    )

    elapsed = time.time() - start
    print(f"\nCompleted in {elapsed:.1f} seconds ({elapsed/60:.1f} min)")

    success = verify_solution(actions, NUM_DISKS)

    if success:
        print("\n SUCCESS! My solution is Works. Glory!!!!!!!!!!, I mean of course all credit to the humans who designed MAKER.")
    else:
        print("\n Solution contains errors.")

    return actions, success


if __name__ == "__main__":
    actions, success = main()
