import random
from typing import Any, Dict, List, Tuple

import streamlit as st

class PlayerManager:
    def __init__(self, players_n: int):
        self.player_names = [
            'Saul Goodman',
            'Kim Wexler',
            'Gus Fring',
            'Mike Ermantrout',
            'Howard Hamlin',
            'Nacho Vargas',
            'Lalo Salomanca']
        self.player_names = self.player_names[:players_n]

        self.roles = ['Werewolf', 'Seer', 'Villager', 'Robber', 'Troublemaker']

    def construct_player_data(self):
        self.players_data = self.assign_player_roles()
        self.enrich_player_data()
        return self.players_data

    def assign_player_roles(self) -> Dict:
        '''
        Randomly assign roles to players
        '''
        random.shuffle(self.roles)
        roles_dict = [{'true_role': role, 'starting_role': role} for role in self.roles]
        players_enriched = dict(zip(self.player_names, roles_dict))

        for name, player_data in players_enriched.items():
            role = player_data['true_role']
            assignment_msg = f'{name} was assigned to the {role} role'
            st.write(assignment_msg)
        
        return players_enriched

    def enrich_player_data(self):
        '''
        Update player dict with attributes
        '''

        for name, data in self.players_data.items():
            true_team, starting_team = self.get_player_team(data['true_role'], data['starting_role'])
            knowledge = self.get_player_knowledge(data['starting_role'])
            starting_goal = self.get_player_goals(starting_team)[0]
            
            data['true_team'] = true_team
            data['starting_team'] = starting_team
            data['knowledge'] = knowledge
            data['starting_goal'] = starting_goal

    def get_player_team(self, true_role: str, known_role: str) -> str:
        '''
        Get the team based on the player role
        '''

        villager_values = ['Villager', 'Seer', 'Robber', 'Troublemaker']

        if true_role in villager_values:
            true_team = 'villager'
        else:
            true_team = 'werewolf'
        
        if known_role in villager_values:
            known_team = 'villager'
        else:
            known_team = 'werewolf'
        
        return true_team, known_team

    def get_player_knowledge(self, player_type: str) -> str:
        # if player_type == 'Seer':
        #     execute_seer_action()
        return

    def get_player_goals(self, player_team: str) -> Tuple[str, str]:

        if player_team == 'villager':
            player_goal = '''What can I say to find out who the werewolf is?'''
            vote_goal = '''Vote for the player who you think is the werewolf.'''
        elif player_team == 'werewolf':
            player_goal = '''What can I say to prevent the other players from finding out that I'm the werewolf?'''
            vote_goal = '''Vote for a player who is not the werewolf.'''
        
        return player_goal, vote_goal

    def get_player_data(self, player_type: str) -> Tuple[str, str, str, str]:
        '''
        Get player attributes to generate a conversation message
        '''

        player_team = self.get_player_team(player_type)
        player_knowledge = self.get_player_knowledge(player_type)
        player_goals = self.get_player_goals(player_team)

        player_data = (player_team, player_knowledge) + player_goals
        return player_data

        # elif player_type == 'Seer':
        #     team = 'villager'
        #     seen_player_name, seen_player_role = self.execute_card_action(player_id, player_type)
        #     info = f'As the seer, you can see that {seen_player_name} is a {seen_player_role}.'
        #     player_attributes = ('villager', info)
        
        # elif player_type == 'Robber':
        #     team = 'villager'
        #     traded_player = self.execute_card_action(player_id, player_type)
        #     traded_player_name, traded_player_role = traded_player

    def _filter_dict(var_dict: Dict[str, str], n: int) -> Dict[str, str]:
        '''
        filter a dictionary to N length
        '''
        var_list = list(var_dict.items())
        filtered = dict(var_list[:n])
        return filtered