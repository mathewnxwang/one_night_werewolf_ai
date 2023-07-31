from typing import Any, Dict

from ai.prompt_templates import deliberate_template, action_template
from mechanics.turn import player_turn

def conversation_round(
    round_counter: int,
    players: Dict[str, Dict[str, Any]],
    conversation: str,
    thoughts: list
    ) -> int:
    '''
    Generate one round of conversation where every player speaks once
    '''

    # Steer players toward making pointed contributions later in the game
    if round_counter == 1:
        prompt_template = deliberate_template
    elif round_counter >= 2:
        prompt_template = action_template
        
    # Every player contributes to the conversation once in order
    for player_name, player_data in players.items():        
        conversation, thoughts = player_turn(
            players, player_name, prompt_template, conversation, thoughts
        )
    
    return conversation, thoughts

def conversation_full(
    rounds: int,
    players: Dict[str, Dict[str, Any]],
    conversation: str,
    thoughts: list
    ) -> None:
    '''
    Generate N rounds of conversation
    '''
    round_counter = 1
    
    while round_counter <= rounds:
        print(f'Executing round {round_counter}')
        conversation, thoughts = conversation_round(
            round_counter, players, conversation, thoughts
        )

        round_counter += 1
    
    return conversation, thoughts