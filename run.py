from typing import List

import streamlit as st

from mechanics.players import assign_player_roles, enrich_player_data
from mechanics.vote import show_results
from mechanics.conversation import conversation_full
from mechanics.utils.role_actions import execute_all_actions

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

    # assign player roles
    players = assign_player_roles(players)
    
    # enrich player data
    enriched_players = enrich_player_data(players)

    # execute role actions
    enriched_players = execute_all_actions(players)
    st.write(enriched_players)

    # for player_id, player_role in self.players:
    #     info = self.execute_card_action(player_id, player_role)

    st.markdown('#### Deliberation')
    conversation, thoughts = conversation_full(rounds, enriched_players, conversation, thoughts)

    show_results(enriched_players, conversation)