from typing import Dict

import streamlit as st

from players import init_players
from mechanics.vote import show_results
from mechanics.conversation import conversation_full

def full_game(
    rounds: int,
    players: Dict[str, str]
    ):
    '''
    Execute full conversation and vote
    '''

    # initialize variables
    conversation = ''
    thoughts = []

    # for player_id, player_role in self.players:
    #     info = self.execute_card_action(player_id, player_role)

    st.markdown('#### Deliberation')
    conversation, thoughts = conversation_full(rounds, players, conversation, thoughts)

    show_results(players, conversation)