import openai
import os
openai.api_key = os.environ.get('OPENAI_API_KEY')
from langchain import PromptTemplate
from langchain.llms import OpenAI
call_llm = OpenAI()
import json
from collections import Counter
import streamlit as st

page_title = 'One Night Werewolf, AI Version'
st.set_page_config(page_title=page_title)

# Create prompt templates

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

# Define functions

def get_player_attributes(player_type):
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

def player_turn(player_id, player_type, conversation_input):
    global conversation
    global thoughts

    player_attributes = get_player_attributes(player_type)

    prompt = converse_template.format(
        player_id=player_id,
        player_type=player_type,
        player_team=player_attributes[0],
        player_goal=player_attributes[2],
        info=player_attributes[1],
        conversation=conversation_input
    )

    thought = call_llm(prompt)
    thoughts.append(thought)
    parsed_thought = json.loads(thought)
    message = parsed_thought['message']
    message = f'{player_id}: {message}'
    conversation = conversation + '\n' + message

def conversation_round(players):
    for key, value in players.items():
        player_id=key
        player_type=value
        player_turn(player_id=player_id, player_type=player_type, conversation_input=conversation)

def conversation_full(rounds):
    for _ in range(rounds):
        conversation_round(players)

def player_vote(players, player_id, player_type, conversation_input):
    player_raw = list(players.keys())
    players_list = ', '.join(player_raw)

    player_attributes = get_player_attributes(player_type)
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

def all_vote(players):
    vote_results = []

    for key, value in players.items():
        player_id=key
        player_type=value
        vote = player_vote(players=players, player_id=player_id, player_type=player_type, conversation_input=conversation)
        vote_results.append(vote)

    counter = Counter(vote_results)
    most_common_value = counter.most_common(1)[0][0]
    return most_common_value, vote_results, counter

def full_game(players, rounds):
    conversation = ''
    thoughts = []
    conversation_full(rounds)
    vote_results = all_vote(players)
    return vote_results


# Streamlit app

### Configuration


st.header('Configuration')

config_col1, config_col2 = st.columns(2)

with config_col1:
    players_n = st.number_input(
        label='How many players?',
        min_value=4,
        max_value=8,
        value=5)

with config_col2:
    rounds_n = st.number_input(
        label='How many rounds of deliberation?',
        min_value=1,
        max_value=5)

st.header('Players')

col1, col2 = st.columns(2)

with col1:
    player_1 = st.text_input(label='Player 1 Name', value='Saul Goodman')
    player_2 = st.text_input(label='Player 2 Name', value='Kim Wexler')
    player_3 = st.text_input(label='Player 3 Name', value='Lalo Salomanca')
    player_4 = st.text_input(label='Player 4 Name', value='Gus Fring')
    player_5 = st.text_input(label='Player 5 Name', value='Mike Ehrmantrout')

with col2:
    player_1_role = st.text_input(label='Player 1 Role', value='Villager')
    player_2_role = st.text_input(label='Player 2 Role', value='Villager')
    player_3_role = st.text_input(label='Player 3 Role', value='Werewolf')
    player_4_role = st.text_input(label='Player 4 Role', value='Seer')
    player_5_role = st.text_input(label='Player 5 Role', value='Villager')

run_button = st.button(label='Simulate Game')

# Define players

players = {
    player_1: player_1_role,
    player_2: player_2_role,
    player_3: player_3_role,
    player_4: player_4_role,
    player_5: player_5_role
}

# Execute game

conversation = ''
thoughts = []
if run_button:
    vote_results = full_game(players, rounds_n)
    st.markdown('#### Deliberation')
    st.write(conversation)
    st.markdown('#### Results')
    st.write(vote_results)

