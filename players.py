from typing import Dict, List

import streamlit as st

def _filter_dict(var_dict: Dict[str, str], n: int) -> Dict[str, str]:
    '''
    filter a dictionary to N length
    '''
    var_list = list(var_dict.items())
    filtered = dict(var_list[:n])
    return filtered

def init_players(players_n: int) -> Dict[str, str]:
    '''
    Create players dictionary of a certain length
    '''
    players = {
        'Saul Goodman': 'Villager',
        'Kim Wexler': 'Seer',
        'Gus Fring': 'Werewolf',
        'Mike Ermantrout': 'Villager',
        'Howard Hamlin': 'Villager',
        'Nacho Vargas': 'Werewolf',
        'Lalo Salomanca': 'Villager'
    }

    players = _filter_dict(players, players_n)

    return players

# def player_name_inputs(players: Dict[str, str]) -> List[str]:
#     '''
#     create configurable text inputs for player names
#     '''
    
#     player_names = []
#     default_names = list(players.keys())

#     # generate label and default value for every input
#     for i, name in enumerate(default_names):
#         player_name = st.text_input(
#             label=f'Player {i+1} Name',
#             value=name)
#         player_names.append(player_name)
    