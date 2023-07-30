from typing import Tuple
import random

def _get_random_player(
    players,
    player_id: str
    ) -> Tuple[str, str]:

    eligible_players = players.copy()

    # exclude the player with the card in question
    del eligible_players[player_id]

    # get a random player and their role
    player_list = list(eligible_players.keys())
    random_player_id = random.choice(player_list)
    random_player_role = eligible_players[random_player_id]

    return random_player_id, random_player_role

def execute_seer_action(
    self,
    player_id: str
    ) -> Tuple[str, str]:
    '''
    If a player is a seer, they get information about the role of one other player randomly
    '''

    seen_player_name, seen_player_role = _get_random_player(player_id)
    return seen_player_name, seen_player_role

def execute_robber_action(
    players: list,
    player_id: str,
    player_type: str
    ) -> Tuple[str, str]:

    # to-do: update action to allow player to select who they want to trade with
    # existing behavior is that the player randomly trade with another player,
    # but knows who they traded with
    target_player_id, target_player_role = get_random_player(player_id)
    players[player_id] = target_player_role
    players[target_player_id] = player_type

    return target_player_id, target_player_role