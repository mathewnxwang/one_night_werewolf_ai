import random
from typing import Any, Dict, Tuple

import streamlit as st

def _get_random_player(players, player_id: str) -> Tuple[str, str]:
    '''
    Get player data for a random player that is not the specified one
    '''
    eligible_players = players.copy()

    # exclude the player with the card in question
    del eligible_players[player_id]

    # get a random player's data
    player_list = list(eligible_players.keys())
    random_player_id = random.choice(player_list)
    random_player_data = eligible_players[random_player_id]

    return random_player_id, random_player_data

def _get_name_from_role(players: Dict[str, Dict[str, Any]], true_role: str) -> str:
    '''
    Get the player name for the specified role
    '''
    for name, data in players.items():
        if data['true_role'] == true_role:
            return name
    return None

def execute_seer_action(players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    '''
    The seer player gets information about the role of one other player randomly
    '''
    seer_player_name = _get_name_from_role(players, 'Seer')
    target_player_name, target_player_data = _get_random_player(players, seer_player_name)
    target_player_role = target_player_data['true_role']
    knowledge = f'As the seer, you saw that {target_player_name} is a {target_player_role}.'
    players[seer_player_name]['knowledge'] = knowledge

    dev_msg = f'{seer_player_name}: {knowledge}'
    st.write(dev_msg)

    return players

def execute_robber_action(players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    '''
    The robber player switches roles with another player,
    and knows which player they switched with and their role
    '''

    robber_player_name = _get_name_from_role(players, 'Robber')
    target_player_name, target_player_data = _get_random_player(players, robber_player_name)

    target_player_role = target_player_data['true_role']
    robber_player_update = {'true_role': target_player_role, 'true_team': target_player_data['true_team']}
    players[robber_player_name].update(robber_player_update)
    knowledge = f'You were previously the Robber. You robbed {target_player_name} who is a {target_player_role}. You are now a {target_player_role}.'
    players[robber_player_name]['knowledge'] = knowledge

    target_player_update = {'true_role': 'Robber', 'true_team': 'villager'}
    players[target_player_name].update(target_player_update)

    dev_msg = f'{robber_player_name}: {knowledge}'
    st.write(dev_msg)

    return players

def execute_troublemaker_action(players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    '''
    The troublemaker player switches the roles of two other players,
    and knows which players they switched
    '''

    troublemaker_player_name = _get_name_from_role(players, 'Troublemaker')
    
    players_to_switch = []
    while len(players_to_switch) < 2: 
        target_player = _get_random_player(players, troublemaker_player_name)
        if target_player not in players_to_switch:
            players_to_switch.append(target_player)
    
    player_1, player_2 = players_to_switch

    player_1_name, player_1_data = player_1
    player_2_name, player_2_data = player_2

    player_1_update = {'true_role': player_2_data['true_role'], 'true_team': player_2_data['true_team']}
    player_2_update = {'true_role': player_1_data['true_role'], 'true_team': player_1_data['true_team']}

    players[player_1_name].update(player_1_update)
    players[player_2_name].update(player_2_update)

    player_1_new_role = players[player_1_name]['true_role']
    player_2_new_role = players[player_2_name]['true_role']
    knowledge = f'As the troublemaker, you switched the roles of {player_1_name} and {player_2_name}. Now {player_1_name} is {player_1_new_role} and {player_2_name} is {player_2_new_role}.'
    players[troublemaker_player_name]['knowledge'] = knowledge

    dev_msg = f'{troublemaker_player_name}: {knowledge}'
    st.write(dev_msg)

    return players

def execute_all_actions(players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    players = execute_seer_action(players)
    players = execute_robber_action(players)
    players = execute_troublemaker_action(players)
    return players