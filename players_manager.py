import random
from typing import Any, Dict, List, Tuple

import streamlit as st

class PlayersManager:
    def __init__(self, players_n: int):
        self.player_names = [
            'Morty',
            'Rick',
            'Summer',
            'Beth',
            'Jerry']
        self.player_names = self.player_names[:players_n]

        self.roles = ['Werewolf', 'Seer', 'Villager', 'Robber', 'Troublemaker']
        self.players_data = self.assign_player_roles()
        self.enrich_player_data()

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
        team_mapping = {
            'Villager': 'villager',
            'Seer': 'villager',
            'Robber': 'villager',
            'Troublemaker': 'villager',
            'Werewolf': 'werewolf'
        }
        true_team = team_mapping.get(true_role)
        known_team = team_mapping.get(known_role)
        
        return true_team, known_team

    def get_player_knowledge(self, player_type: str) -> str:
        # if player_type == 'Seer':
        #     execute_seer_action()
        return

    def get_player_goals(self, player_team: str) -> Tuple[str, str]:
        goals_mapping = {
            'villager': (
                'What can I say to find out who the werewolf is?',
                'Vote for the player who you think is the werewolf.'
            ),
            'werewolf': (
                'What can I say to prevent the other players from finding out that I\'m the werewolf?',
                'Vote for a player who is not the werewolf.'
            )
        }
        player_goal, vote_goal = goals_mapping.get(player_team)
        return player_goal, vote_goal
