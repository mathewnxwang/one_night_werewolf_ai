from typing import List

import streamlit as st

from mechanics.players import PlayerManager
from mechanics.game_manager import GameManager
from mechanics.utils.role_actions import RoleActions

def full_game(rounds: int):
    '''
    Execute full conversation and vote
    '''
    st.markdown('#### Deliberation')
    game_manager = GameManager()
    game_manager.conversation_full(rounds)
    game_manager.show_results()