from typing import List

import streamlit as st

from players import assign_player_roles
from mechanics.vote import show_results
from mechanics.conversation import conversation_full

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

    for name, role in players.items():
        assignment_msg = f'{name} was assigned to the {role} role'
        st.write(assignment_msg)
        print(assignment_msg)

    # for player_id, player_role in self.players:
    #     info = self.execute_card_action(player_id, player_role)

    st.markdown('#### Deliberation')
    conversation, thoughts = conversation_full(rounds, players, conversation, thoughts)

    show_results(players, conversation)