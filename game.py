import openai
import os
openai.api_key = os.environ.get('OPENAI_API_KEY')
from langchain import PromptTemplate
from langchain.llms import OpenAI
call_llm = OpenAI()
import json
from collections import Counter
import random
import streamlit as st

# Prompt templates

deliberate_prompt = '''You are playing a social deduction game.
Your name is {player_id}.
You are a {player_type}.
You are on the {player_team} team.
=====
The conversation so far: {conversation}
=====
You also have the following information: {info}
=====
Accomplish the following five tasks:
1. goal: {player_goal}
2. synthesis: Synthesize your goal with the information and conversation available.
3. truth: Should I tell the other player what kind of player I am?
4. lie: Should I lie to the other players about what kind of player I am?
5. message: Based on your answers to the previous tasks, add something new to the conversation to achieve your goal.
=====
Return a JSON object with the 5 keys of goal, synthesis, truth, lie, and message.
'''

action_prompt = '''You are playing a social deduction game.
Your name is {player_id}.
You are a {player_type}.
You are on the {player_team} team.
=====
The conversation so far: {conversation}
=====
You also have the following information: {info}
=====
Accomplish the following five tasks:
1. goal: {player_goal}
2. synthesis: Synthesize your goal with the information and conversation available.
3. defend: Do I need to defend myself of being accused as the werewolf?
4. accuse: Who should I accuse of being the werewolf?
5. Based on your answers to the previous tasks, either defend yourself or accuse someone else of being the werewolf.
=====
Return a JSON object with the 5 keys of goal, synthesis, defend, accuse, and message.
'''

vote_prompt = '''You are playing a social deduction game.
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

deliberate_template = PromptTemplate(
    input_variables=[
        'player_id',
        'player_type',
        'player_team',
        'player_goal',
        'info',
        'conversation'],
    template=deliberate_prompt)

action_template = PromptTemplate(
    input_variables=[
        'player_id',
        'player_type',
        'player_team',
        'player_goal',
        'info',
        'conversation'],
    template=action_prompt)

vote_template = PromptTemplate(input_variables=['player_id', 'player_type', 'player_team', 'vote_goal', 'player_list', 'conversation'], template=vote_prompt)

# Class

class WerewolfGame:
    def __init__(self):
        self.conversation = ''
        self.thoughts = []
        self.players = {}
        self.round_counter = 0

    def get_random_player(self, player_id):

        eligible_players = self.players.copy()

        # exclude the player with the card in question
        del eligible_players[player_id]

        # get a random player and their role
        player_list = list(eligible_players.keys())
        random_player_id = random.choice(player_list)
        random_player_role = eligible_players[random_player_id]

        return random_player_id, random_player_role

    def execute_robber_action(self, players, player_id, player_type):

        # to-do: update action to allow player to select who they want to trade with
        # existing behavior is that the player randomly trade with another player,
        # but knows who they traded with
        target_player_id, target_player_role = self.get_random_player(player_id)
        players[player_id] = target_player_role
        players[target_player_id] = player_type

        return target_player_id, target_player_role
    
    def execute_seer_action(self, player_id):

        seen_player_name, seen_player_role = self.get_random_player(player_id)
        return seen_player_name, seen_player_role

    def get_player_team(self, player_type):

        villager_values = ['Villager', 'Seer', 'Robber', 'Drunk']
        werewolf_values = ['Werewolf', 'Seer Werewolf']

        # if any(player_type == value for value in villager_values):
        if player_type in villager_values:
            return 'villager'
        elif player_type in werewolf_values:
            return 'werewolf'
    
    def get_player_knowledge(self, player_type):
        # if player_type == 'Seer':
        #     execute_seer_action()
        return 'None'
    
    def get_player_goals(self, player_team):

        if player_team == 'villager':
            player_goal = '''What can I say to find out who the werewolf is?'''
            vote_goal = '''Vote for the player who you think is the werewolf.'''
        elif player_team == 'werewolf':
            player_goal = '''What can I say to prevent the other players from finding out that I'm the werewolf?'''
            vote_goal = '''Vote for a player who is not the werewolf.'''
        
        return player_goal, vote_goal

    def get_player_data(self, player_id, player_type):

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
        player_id,
        player_type,
        conversation_input,
        prompt_template):

        global conversation
        global thoughts

        player_attributes = self.get_player_data(player_id, player_type)

        prompt = prompt_template.format(
            player_id=player_id,
            player_type=player_type,
            player_team=player_attributes[0],
            player_goal=player_attributes[2],
            info=player_attributes[1],
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

        print_msg = f'{player_id}: {message}'
        st.write(print_msg)
        st.write(structured_thought)

    def conversation_round(self):
        for key, value in self.players.items():
            player_id=key
            player_type=value

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

    def conversation_full(self, rounds):
        for _ in range(rounds):
            self.conversation_round()

    def player_vote(self, player_id, player_type, conversation_input):
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

        # for player_id, player_role in self.players:
        #     info = self.execute_card_action(player_id, player_role)

        st.markdown('#### Deliberation')
        self.conversation_full(rounds)
        vote_results = self.all_vote()
        return vote_results