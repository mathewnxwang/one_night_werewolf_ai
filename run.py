from typing import Tuple, Dict
from collections import Counter

import streamlit as st

from vote import all_vote
from conversation import conversation_full

def full_game(
    players: Dict[str, str],
    rounds: int
    ) -> Tuple[str, list, Counter]:
    '''
    Execute full conversation and vote
    '''

    conversation = ''
    thoughts = []

    # for player_id, player_role in self.players:
    #     info = self.execute_card_action(player_id, player_role)

    st.markdown('#### Deliberation')
    conversation_full(rounds)

    st.markdown('#### Results')
    winning_team, eliminated_player, eliminated_role, vote_data = all_vote(players, conversation)

    if eliminated_player == 'tie':
        st.write('Players couldn\'t agree on who to eliminate and the vote ended up tied.')
        st.write('As a result, the werewolf team wins!')
    else:
        st.write(f'{eliminated_player} was voted to be eliminated. They were a {eliminated_role}!')
        st.write(f'As a result, the {winning_team} team wins!')
    
    st.markdown('#### Vote breakdown')
    for name, count in vote_data.items():
        st.write(f'{name}: {count} votes')