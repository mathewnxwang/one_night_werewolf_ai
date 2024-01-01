import random
from typing import Any, Dict, Tuple

import streamlit as st

class RoleActions:

    def _get_random_player(self, players, player_id: str) -> str:
        '''
        Get player name for a random player that is not the specified one
        '''
        eligible_players = players.copy()

        # exclude the player with the card in question
        del eligible_players[player_id]

        # get a random player's data
        player_list = list(eligible_players.keys())
        random_player_id = random.choice(player_list)
        return random_player_id

    def _get_name_from_role(self, players: Dict[str, Dict[str, Any]], true_role: str) -> str:
        '''
        Get the player name for the specified role
        '''
        for name, data in players.items():
            if data['true_role'] == true_role:
                return name
        return None

    def _switch_player_roles(self, players: Dict[str, Dict[str, Any]], player_1_name: str, player_2_name: str) -> Dict[str, Dict[str, Any]]:
        '''
        handles switching player roles for the Robber and Troublemaker actions
        '''
        player_1_update = {'true_role': players[player_2_name]['true_role'], 'true_team': players[player_2_name]['true_team']}
        player_2_update = {'true_role': players[player_1_name]['true_role'], 'true_team': players[player_1_name]['true_team']}
        players[player_1_name].update(player_1_update)
        players[player_2_name].update(player_2_update)
        return players

    def execute_seer_action(self, players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        '''
        The seer player gets information about the role of one other player randomly
        '''
        seer_player_name = self._get_name_from_role(players, 'Seer')
        target_player_name = self._get_random_player(players, seer_player_name)
        target_player_role = players[target_player_name]['true_role']
        knowledge = f'As the seer, you saw that {target_player_name} is a {target_player_role}.'
        players[seer_player_name]['knowledge'] = knowledge

        dev_msg = f'{seer_player_name}: {knowledge}'
        st.write(dev_msg)

        return players

    def execute_robber_action(self, players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        '''
        The robber player switches roles with another player,
        and knows which player they switched with and their role
        '''

        robber_player_name = self._get_name_from_role(players, 'Robber')
        target_player_name = self._get_random_player(players, robber_player_name)
        original_target_role = players[target_player_name]['true_role']

        players = self._switch_player_roles(players, robber_player_name, target_player_name)

        knowledge = f'You were previously the Robber. You robbed {target_player_name} who was a {original_target_role}. You are now a {original_target_role} and {target_player_name} is the Robber.'
        players[robber_player_name]['knowledge'] = knowledge

        dev_msg = f'{robber_player_name}: {knowledge}'
        st.write(dev_msg)

        return players

    def execute_troublemaker_action(self, players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        '''
        The troublemaker player switches the roles of two other players,
        and knows which players they switched
        '''

        troublemaker_player_name = self._get_name_from_role(players, 'Troublemaker')
        
        # get two other players that are not the troublemaker
        players_to_switch = []
        while len(players_to_switch) < 2: 
            target_player = self._get_random_player(players, troublemaker_player_name)
            if target_player not in players_to_switch:
                players_to_switch.append(target_player)
        
        player_1_name, player_2_name = players_to_switch
        players = self._switch_player_roles(players, player_1_name, player_2_name)

        player_1_new_role = players[player_1_name]['true_role']
        player_2_new_role = players[player_2_name]['true_role']

        knowledge = f'As the troublemaker, you switched the roles of {player_1_name} and {player_2_name}. Now {player_1_name} is {player_1_new_role} and {player_2_name} is {player_2_new_role}.'
        players[troublemaker_player_name]['knowledge'] = knowledge

        dev_msg = f'{troublemaker_player_name}: {knowledge}'
        st.write(dev_msg)

        return players

    def execute_all_actions(self, players: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        players = self.execute_seer_action(players)
        players = self.execute_robber_action(players)
        players = self.execute_troublemaker_action(players)
        return players