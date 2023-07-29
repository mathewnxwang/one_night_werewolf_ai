from typing import Tuple, Dict
from collections import Counter

import streamlit as st

from mechanics.vote import show_results
from mechanics.conversation import conversation_full

def init_players(players):

    if players is None:
        players = {
            'Saul Goodman': 'Villager',
            'Kim Wexler': 'Seer',
            'Gus Fring': 'Werewolf',
            'Mike Ermantrout': 'Villager' 
        }

    return players

def full_game(
    rounds: int,
    players: Dict[str, str] = None,
    ):
    '''
    Execute full conversation and vote
    '''

    # initialize variables
    conversation = ''
    thoughts = []
    players = init_players(players)

    # for player_id, player_role in self.players:
    #     info = self.execute_card_action(player_id, player_role)

    st.markdown('#### Deliberation')
    conversation, thoughts = conversation_full(rounds, players, conversation, thoughts)

    show_results(players, conversation)