import random
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
    Create players list of a certain length
    '''
    players = [
        'Saul Goodman',
        'Kim Wexler',
        'Gus Fring',
        'Mike Ermantrout',
        'Howard Hamlin',
        'Nacho Vargas',
        'Lalo Salomanca']

    players_filtered = players[:players_n]
    return players_filtered

def assign_player_roles(players: List) -> Dict[str, str]:
    '''
    Randomly assign roles to players
    '''
    
    roles = ['Werewolf', 'Seer'] + ['Villager'] * 2
    random.shuffle(roles)

    players_enriched = dict(zip(players, roles))
    return players_enriched
