import random
from typing import Any, Dict, Tuple

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
    random_player_role = eligible_players[random_player_id]['role']

    return random_player_id, random_player_role

def _get_name_from_role(players: Dict[str, Dict[str, Any]], role: str) -> str:
    '''
    Get the player name for the specified role
    '''
    for name, data in players.items():
        if data['role'] == role:
            return name
    return None

def execute_seer_action(players: Dict[str, Dict[str, Any]]) -> Tuple[str, str]:
    '''
    If a player is a seer, they get information about the role of one other player randomly
    '''
    seer_player_name = _get_name_from_role(players, 'Seer')
    target_player_name, target_player_role = _get_random_player(players, seer_player_name)
    players[seer_player_name]['knowledge'] = f'As the seer, you saw that {target_player_name} is a {target_player_role}.'

    return players

def execute_robber_action(players: list, player_id: str, player_type: str) -> Tuple[str, str]:

    # to-do: update action to allow player to select who they want to trade with
    # existing behavior is that the player randomly trade with another player,
    # but knows who they traded with
    target_player_id, target_player_role = _get_random_player(player_id)
    players[player_id] = target_player_role
    players[target_player_id] = player_type

    return target_player_id, target_player_role

def execute_all_actions(players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    players = execute_seer_action(players)
    return players