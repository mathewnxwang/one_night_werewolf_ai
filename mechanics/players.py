import random
from typing import Any, Dict, List

import streamlit as st

from mechanics.utils.fetch_data import get_player_team, get_player_knowledge, get_player_goals

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
    
    roles = ['Werewolf', 'Seer', 'Villager', 'Robber']
    random.shuffle(roles)
    roles_dict = [{'role': role} for role in roles]

    players_enriched = dict(zip(players, roles_dict))

    for name, player_data in players_enriched.items():
        role = player_data['role']
        assignment_msg = f'{name} was assigned to the {role} role'
        st.write(assignment_msg)
        print(assignment_msg)
    
    return players_enriched

def enrich_player_data(players_enriched: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    '''
    Update player dict with attributes
    '''

    for name, data in players_enriched.items():
        team = get_player_team(data['role'])
        knowledge = get_player_knowledge(data['role'])
        goal = get_player_goals(team)
        
        data['team'] = team
        data['knowledge'] = knowledge
        data['goal'] = goal

    return players_enriched