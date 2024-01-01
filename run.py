from typing import List

import streamlit as st

from mechanics.players import PlayerManager
from mechanics.vote import show_results
from mechanics.conversation import conversation_full
from mechanics.utils.role_actions import RoleActions

def full_game(
    rounds: int,
    players: List[str]
    ):
    '''
    Execute full conversation and vote
    '''

    # initialize variables
    conversation = ''
    thoughts = []

    player_manager = PlayerManager(players_n=5)
    player_data = player_manager.construct_player_data()
    enriched_players = RoleActions().execute_all_actions(player_data)
    st.write(enriched_players)

    st.markdown('#### Deliberation')
    conversation, thoughts = conversation_full(rounds, enriched_players, conversation, thoughts)

    show_results(enriched_players, conversation)