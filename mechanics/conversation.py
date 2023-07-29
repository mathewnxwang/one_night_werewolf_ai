from typing import Dict

from mechanics.llms import deliberate_template, action_template
from mechanics.turn import player_turn

def conversation_round(
    round_counter: int,
    players: Dict[str, str],
    conversation: str
    ) -> int:
    '''
    Generate one round of conversation where every player speaks once
    '''

    # Steer players toward making pointed contributions later in the game
    if round_counter == 0:
        prompt_template = deliberate_template
    elif round_counter >= 1:
        prompt_template = action_template
        
    # Every player contributes to the conversation once in order
    for player_id, player_type in players.items():        
        player_turn(
            player_id,
            player_type,
            conversation,
            prompt_template)
    
    round_counter += 1
    return round_counter

def conversation_full(
    rounds: int,
    round_counter: int
    ) -> None:
    '''
    Generate N rounds of conversation
    '''
    
    for _ in range(rounds):
        conversation_round(round_counter)