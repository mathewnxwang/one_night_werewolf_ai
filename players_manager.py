from colorama import Fore, Style
import random
import typing as t

import streamlit as st

from project_resource import Player, Team, GoalPrompt, VotePrompt

class PlayersManager:
    def __init__(self, player_names, roles):
        roles_list = list(roles)
        print('roles: ', roles)
        self.players = []
        for player_name, role in zip(player_names, roles_list):
            player = self._instantiate_player(player_name, role)
            self.players.append(player)
        print('Initialized all players: ', self.players)

    def _instantiate_player(self, player_name, role):
        true_team = Team[role.name].value
        known_team = Team[role.name].value
        player = Player(
            name=player_name.name,
            starting_role=role.name,
            true_role=role.name,
            true_team=true_team,
            known_team=known_team,
            starting_goal=GoalPrompt[true_team].value,
            vote_goal=VotePrompt[true_team].value
        )
        print('initialized player: ', player)
        return player

class ActionManager(PlayersManager):
    def __init__(self, players: t.List[Player]):
        self.players = players

    def execute_all_actions(self) -> None:
        _color_print('Executing all player actions.', Fore.GREEN)
        for player in self.players:
            if player.true_role == 'SEER':
                self._execute_seer_action(player.name)
            elif player.true_role == 'ROBBER':
                self._execute_robber_action(player.name)
            elif player.true_role == 'TROUBLEMAKER':
                self._execute_troublemaker_action(player.name)

    def _execute_seer_action(self, seer_player_name: str) -> None:
        '''
        The seer player gets information about the role of one other player randomly
        '''
        _color_print(f'Executing the seer action for {seer_player_name}.', Fore.GREEN)
        target_player_name = self._get_random_player(seer_player_name)
        print('checking players data: ', self.players)
        target_player_role = self._get_player_by_name(target_player_name).true_role
        knowledge = f'As the seer, you saw that {target_player_name} is a {target_player_role}.'

        self._get_player_by_name(seer_player_name).knowledge = knowledge
        dev_msg = f'{seer_player_name}: {knowledge}'
        _color_print(dev_msg, Fore.GREEN)
        st.write(dev_msg)

    def _execute_robber_action(self, robber_player_name: str) -> None:
        '''
        The robber player switches roles with another player,
        and knows which player they switched with and their role
        '''
        _color_print('Executing the robber action.', Fore.GREEN)
        target_player_name = self._get_random_player(robber_player_name)
        original_target_role = self._get_player_by_name(target_player_name).true_role
        self._switch_player_roles(robber_player_name, target_player_name)

        knowledge = f'You were previously the ROBBER. You robbed {target_player_name} who was a {original_target_role}. You are now a {original_target_role} and {target_player_name} is the Robber.'
        self._get_player_by_name(robber_player_name).knowledge = knowledge

        dev_msg = f'{robber_player_name}: {knowledge}'
        _color_print(dev_msg, Fore.GREEN)
        st.write(dev_msg)

    def _execute_troublemaker_action(self, troublemaker_player_name: str) -> None:
        '''
        The troublemaker player switches the roles of two other players,
        and knows which players they switched
        '''
        _color_print('Executing the troublemaker action.', Fore.GREEN)
        # get two other players that are not the troublemaker
        players_to_switch = []
        while len(players_to_switch) < 2: 
            target_player = self._get_random_player(troublemaker_player_name)
            if target_player not in players_to_switch:
                players_to_switch.append(target_player)
        
        player_1_name, player_2_name = players_to_switch
        self._switch_player_roles(player_1_name, player_2_name)

        player_1_new_role = self._get_player_by_name(player_1_name).true_role
        player_2_new_role = self._get_player_by_name(player_2_name).true_role

        knowledge = f'As the troublemaker, you switched the roles of {player_1_name} and {player_2_name}. Now {player_1_name} is {player_1_new_role} and {player_2_name} is {player_2_new_role}.'
        self._get_player_by_name(troublemaker_player_name).knowledge = knowledge

        dev_msg = f'{troublemaker_player_name}: {knowledge}'
        _color_print(dev_msg, Fore.GREEN)
        st.write(dev_msg)

    def _get_name_from_role(self, true_role: str) -> str:
        '''
        Get the player name for the specified role
        '''
        for player in self.players:
            print(f'checking if {player.name} is {true_role}')
            if player.true_role == true_role:
                print(f'{player.name} is {true_role}')
                return player.name
        raise ValueError(f'No player found with role: {true_role}')

    def _get_player_by_name(self, name: str):
        for player in self.players:
            if player.name == name:
                return player
        raise ValueError(f'No player found with name: {name}')

    def _get_random_player(self, excluded_player_name: str) -> str:
        '''
        Get player name for a random player that is not the specified one
        '''
        print('choosing a random player')
        eligible_players = [player for player in self.players if player.name != excluded_player_name]
        print('eligible players: ', eligible_players)

        # get a random player's data
        player_names = [player.name for player in eligible_players]
        random_player_name = random.choice(player_names)
        print('random player name: ', random_player_name)
        return random_player_name

    def _switch_player_roles(self, player_1_name: str, player_2_name: str) -> None:
        '''
        Handles switching player roles.
        This is used for roles like the Robber and Troublemaker.
        '''
        _color_print(f'Switching roles for {player_1_name} and {player_2_name}.', Fore.GREEN)
        player_1_new_role = self._get_player_by_name(player_2_name).true_role
        print(f'{player_1_name}\'s new role: {player_1_new_role}')
        player_2_new_role = self._get_player_by_name(player_1_name).true_role
        print(f'{player_2_name}\'s new role: {player_2_new_role}')
        self._get_player_by_name(player_1_name).true_role = player_1_new_role
        self._get_player_by_name(player_2_name).true_role = player_2_new_role

def _color_print(msg: str, color: str) -> None:
    print(f'{color}{msg}{Style.RESET_ALL}')
