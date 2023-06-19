import os
import json
from collections import Counter
import random
from typing import Tuple

import openai
from langchain.llms import OpenAI
from langchain import PromptTemplate
import streamlit as st

from prompts import *

openai.api_key = os.environ.get('OPENAI_API_KEY')
call_llm = OpenAI()

# Class

# class Player:
#     def __init__(
#         self,
#         id,
#         role,
#         team,
#         knowledge,
#         goals
#     ):
#         self.id = id
#         self.role = role
#         self.team = team
#         self.knowledge = knowledge
#         self.goals = goals

class WerewolfGame:
    def __init__(self):
        self.conversation = ''
        self.thoughts = []
        self.players = {}
        self.round_counter = 0

    def get_random_player(
        self,
        player_id: str
        ) -> Tuple[str, str]:

        eligible_players = self.players.copy()

        # exclude the player with the card in question
        del eligible_players[player_id]

        # get a random player and their role
        player_list = list(eligible_players.keys())
        random_player_id = random.choice(player_list)
        random_player_role = eligible_players[random_player_id]

        return random_player_id, random_player_role

    def execute_robber_action(
        self,
        players: dict,
        player_id: str,
        player_type: str
        ) -> Tuple[str, str]:

        # to-do: update action to allow player to select who they want to trade with
        # existing behavior is that the player randomly trade with another player,
        # but knows who they traded with
        target_player_id, target_player_role = self.get_random_player(player_id)
        players[player_id] = target_player_role
        players[target_player_id] = player_type

        return target_player_id, target_player_role
    
    def execute_seer_action(
        self,
        player_id: str
        ) -> Tuple[str, str]:

        seen_player_name, seen_player_role = self.get_random_player(player_id)
        return seen_player_name, seen_player_role

    def get_player_team(
        self,
        player_type: str
        ) -> str:

        villager_values = ['Villager', 'Seer', 'Robber', 'Drunk']
        werewolf_values = ['Werewolf', 'Seer Werewolf']

        # if any(player_type == value for value in villager_values):
        if player_type in villager_values:
            return 'villager'
        elif player_type in werewolf_values:
            return 'werewolf'
    
    def get_player_knowledge(
        self,
        player_type: str
        ) -> str:
        # if player_type == 'Seer':
        #     execute_seer_action()
        return 'None'
    
    def get_player_goals(
        self,
        player_team: str
        ) -> Tuple[str, str]:

        if player_team == 'villager':
            player_goal = '''What can I say to find out who the werewolf is?'''
            vote_goal = '''Vote for the player who you think is the werewolf.'''
        elif player_team == 'werewolf':
            player_goal = '''What can I say to prevent the other players from finding out that I'm the werewolf?'''
            vote_goal = '''Vote for a player who is not the werewolf.'''
        
        return player_goal, vote_goal

    def get_player_data(
        self,
        player_id: str,
        player_type: str
        ) -> Tuple[str, str, str, str]:
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

    def player_turn(
        self,
        player_id: str,
        player_type: str,
        conversation_input: str,
        prompt_template: PromptTemplate
        ) -> None:
        '''
        Generate and store thoughts and a conversation message for a player
        '''

        global conversation
        global thoughts

        thinking_msg = f'{player_id} is thinking...'
        st.write(thinking_msg)

        player_team, player_knowledge, player_goal, _ = self.get_player_data(player_id, player_type)

        prompt = prompt_template.format(
            player_id=player_id,
            player_type=player_type,
            player_team=player_team,
            player_goal=player_goal,
            info=player_knowledge,
            conversation=conversation_input
        )

        raw_thought = call_llm(prompt)

        try:
            parsed_thought = json.loads(raw_thought)
        except json.JSONDecodeError as e:
            parsed_thought = 'I have a brain fart... I think I\'ll skip this turn.'
        
        structured_thought = {
            'player_id': player_id,
            'prompt': prompt,
            'thoughts': parsed_thought
        }
        self.thoughts.append(structured_thought)

        message = structured_thought['thoughts']['message']
        formatted_message = f'{player_id}: {message}'
        self.conversation = self.conversation + '  \n' + formatted_message

        chat_msg = f'{player_id}: {message}'
        st.write(chat_msg)
        st.write(structured_thought)

    def conversation_round(self):
        '''
        Generate one round of conversation where every player speaks once
        '''

        # Every player contributes to the conversation once in order
        for key, value in self.players.items():
            player_id=key
            player_type=value

            # Steer players toward making pointed contributions later in the game
            if self.round_counter == 0:
                prompt_template = deliberate_template
            elif self.round_counter >= 1:
                prompt_template = action_template
            
            self.player_turn(
                player_id,
                player_type,
                self.conversation,
                prompt_template)
            
        self.round_counter =+ 1

    def conversation_full(
        self,
        rounds: int
        ) -> None:
        '''
        Geerate N rounds of conversation
        '''
        
        for _ in range(rounds):
            self.conversation_round()

    def player_vote(
        self,
        player_id: str,
        player_type: str,
        conversation_input: str
        ) -> str:
        '''
        Based on all available info to an AI player, return a player name that the AI player votes for as the Werewolf
        '''

        player_raw = list(self.players.keys())
        players_list = ', '.join(player_raw)

        player_attributes = self.get_player_data(player_id, player_type)
        prompt = vote_template.format(
            player_id=player_id,
            player_type=player_type,
            player_team=player_attributes[0],
            vote_goal=player_attributes[3],
            player_list=players_list,
            conversation=conversation_input
        )

        vote = call_llm(prompt)
        return vote

    def all_vote(self):
        '''
        Collect votes from all players and calculate the final result
        '''
        
        vote_results = []

        for player_id, player_type in self.players.items():
            vote = self.player_vote(
                player_id=player_id,
                player_type=player_type,
                conversation_input=self.conversation)
            vote_results.append(vote)

        counter = Counter(vote_results)
        most_common_value = counter.most_common(1)[0][0]
        return most_common_value, vote_results, counter

    def full_game(
        self,
        rounds: int
        ) -> Tuple[str, list, Counter]:
        '''
        Execute full conversation and vote
        '''

        self.conversation = ''
        self.thoughts = []

        # for player_id, player_role in self.players:
        #     info = self.execute_card_action(player_id, player_role)

        st.markdown('#### Deliberation')
        self.conversation_full(rounds)
        vote_results = self.all_vote()
        return vote_results