import openai
import os
openai.api_key = os.environ.get('OPENAI_API_KEY')
from langchain import PromptTemplate
from langchain.llms import OpenAI
call_llm = OpenAI()
import json
from collections import Counter
import streamlit as st

# Prompt templates

converse_prompt = '''There are 5 players: 3 villagers, 1 seer, and 1 werewolf.
Your name is {player_id}.
You are a {player_type}.
You are on the {player_team} team.
The conversation so far: {conversation}
You also have the following information: {info}
=====
Accomplish the following five tasks:
1. goal_thought: {player_goal}
2. synthesis_thought: Synthesize your goal with the information and conversation available.
3. truth_thought: Should I tell the other player what kind of player I am?
4. lie_thought: Should I lie to the other players about what kind of player I am?
5. message: Based on your answers to the previous tasks, say something new to the conversation to achieve your goal.
=====
Return a JSON object with the 5 keys of goal_thought, synthesis_thought, truth_thought, lie_thought, and message.
'''

vote_prompt = '''
There are 5 players: 3 villagers, 1 seer, and 1 werewolf.
Your name is {player_id}.
You are a {player_type}.
You are on the {player_team} team.
Your goal is to {vote_goal}.
Based on the following conversation, vote for the player to eliminate out of the following options: {player_list}
=====
{conversation}
=====
Name the player to eliminate: 
'''

converse_template = PromptTemplate(
    input_variables=[
        'player_id',
        'player_type',
        'player_team',
        'player_goal',
        'info',
        'conversation'],
    template=converse_prompt)

vote_template = PromptTemplate(input_variables=['player_id', 'player_type', 'player_team', 'vote_goal', 'player_list', 'conversation'], template=vote_prompt)

# Class

class WerewolfGame:
    def __init__(self):
        self.conversation = ''
        self.thoughts = []
        self.players = {}

    def get_player_attributes(self, player_type):
        if player_type == 'Villager':
            team = 'villager'
            info = 'None'
        elif player_type == 'Werewolf':
            team = 'werewolf'
            info = 'None'
        elif player_type == 'Seer':
            team = 'villager'
            info = 'As the seer, you can see that Ryan is the werewolf.'
        
        if team == 'villager':
            player_goal = '''What can I say to find out who the werewolf is?'''
            vote_goal = '''Vote for the player who you think is the werewolf.'''
        elif team == 'werewolf':
            player_goal = '''What can I say to prevent the other players from finding out that I'm the werewolf?'''
            vote_goal = '''Vote for a player who is not the werewolf.'''
        
        return team, info, player_goal, vote_goal

    def player_turn(self, player_id, player_type, conversation_input):
        global conversation
        global thoughts

        player_attributes = self.get_player_attributes(player_type)

        prompt = converse_template.format(
            player_id=player_id,
            player_type=player_type,
            player_team=player_attributes[0],
            player_goal=player_attributes[2],
            info=player_attributes[1],
            conversation=conversation_input
        )

        thought = call_llm(prompt)
        self.thoughts.append(thought)

        parsed_thought = json.loads(thought)
        message = parsed_thought['message']
        message = f'{player_id}: {message}'
        self.conversation = self.conversation + '\n' + message

    def conversation_round(self):
        for key, value in self.players.items():
            player_id=key
            player_type=value
            self.player_turn(player_id=player_id, player_type=player_type, conversation_input=self.conversation)

    def conversation_full(self, rounds):
        for _ in range(rounds):
            self.conversation_round()

    def player_vote(self, player_id, player_type, conversation_input):
        player_raw = list(self.players.keys())
        players_list = ', '.join(player_raw)

        player_attributes = self.get_player_attributes(player_type)
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
        vote_results = []

        for key, value in self.players.items():
            player_id=key
            player_type=value
            vote = self.player_vote(player_id=player_id, player_type=player_type, conversation_input=self.conversation)
            vote_results.append(vote)

        counter = Counter(vote_results)
        most_common_value = counter.most_common(1)[0][0]
        return most_common_value, vote_results, counter

    def full_game(self, rounds):
        self.conversation = ''
        self.thoughts = []
        self.conversation_full(rounds)
        vote_results = self.all_vote()
        return vote_results