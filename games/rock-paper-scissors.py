"""
Rock Paper Scissors game for two players.

Logic of the game:
1. Ask both players for their choice (rock, paper, or scissors).
  - Internally these have values 0, 1 and 2.
  - input function asks for 1, 2 or 3. I feel like it's easier for the user?
2. Use the win_conditions list to determine the winner.
  - If the value in win_condition index player_a is the same as player_b's choice,
    player_a is the winner.
  - Example:
      player_a = 1 # picks scissors (index 1)
      player_b = 2 # picks paper (index 2)

      win_conditions[player_a] == player_b

  - Checking the other way determines if player_b wins or not.
  - If both checks are false, it's a draw.
"""

action_names = ["Kivi", "Sakset", "Paperi"]
win_conditions = [1, 2, 0]  # index beats value at that index

# Generate instructions prompt based on action_names
instructions_prompt = "Valitse:\n"
for index, action in enumerate(action_names):
    instructions_prompt += f"({index + 1}) {action}\n"


def get_input():
    return (
        int(input(instructions_prompt)) - 1
    )  # cheating to get the proper index, 1-3 more user friendly than 0-2


def main():
    print("Pelaaja 1:")
    player_a = get_input()
    print("Pelaaja 2:")
    player_b = get_input()

    if win_conditions[player_a] == player_b:
        print(f"Pelaaja 1 voittaa! {action_names[player_a]} > {action_names[player_b]}")
    elif win_conditions[player_b] == player_a:
        print(f"Pelaaja 2 voittaa! {action_names[player_b]} > {action_names[player_a]}")
    else:
        print(f"Tasapeli... {action_names[player_a]} == {action_names[player_b]}")


if __name__ == "__main__":
    main()
