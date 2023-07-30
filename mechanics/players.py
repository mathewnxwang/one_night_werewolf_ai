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
    
    roles = ['Werewolf', 'Seer', 'Villager', 'Robber', 'Troublemaker']
    random.shuffle(roles)
    roles_dict = [{'true_role': role, 'starting_role': role} for role in roles]


    players_enriched = dict(zip(players, roles_dict))

    for name, player_data in players_enriched.items():
        role = player_data['true_role']
        assignment_msg = f'{name} was assigned to the {role} role'
        st.write(assignment_msg)
        print(assignment_msg)
    
    return players_enriched

def enrich_player_data(players_enriched: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    '''
    Update player dict with attributes
    '''

    for name, data in players_enriched.items():
        true_team, starting_team = get_player_team(data['true_role'], data['starting_role'])
        knowledge = get_player_knowledge(data['starting_role'])
        starting_goal = get_player_goals(starting_team)
        
        data['true_team'] = true_team
        data['starting_team'] = starting_team
        data['knowledge'] = knowledge
        data['starting_goal'] = starting_goal

    return players_enriched