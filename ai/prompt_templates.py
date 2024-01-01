from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

synthesis_prompt = '''You are playing a simplified version of the social deduction game One Night Ultimate Werewolf.
Your name is {player_id}.
You are a {player_type}.
You are on the {player_team} team.
The other players in the game are {players}.
===
Synthesize the Goal, Conversation, and Information into a thought process that you can use to decide what to say to the other players.
===
{few_shot_examples}
===
Goal: {player_goal}
Conversation: {conversation}
Information: {info}
Thought Process: 
'''

synthesis_template = PromptTemplate(
    input_variables=[
        'player_id', 'player_type', 'player_team', 'players', 'player_goal', 'conversation', 'info', 'few_shot_examples'
        ],
    template=synthesis_prompt)

message_prompt = '''
You are playing a simplified version of the social deduction game One Night Ultimate Werewolf.
Your name is {player_id}.
You are a {player_type}.
You are on the {player_team} team.
The other players in the game are {players}.
===
Thought Process: {thought_process}
===
Use the above thought process to decide what to say to the other players.
===
{conversation}
{player_id}: 
'''

message_template = PromptTemplate(
    input_variables=[
        'player_id', 'player_type', 'player_team', 'players', 'thought_process', 'conversation'
    ],
    template=message_prompt
)

deliberate_prompt = '''You are playing a simplified version of the social deduction game One Night Ultimate Werewolf.
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

deliberate_template = PromptTemplate(
    input_variables=[
        'player_id',
        'player_type',
        'player_team',
        'player_goal',
        'info',
        'conversation'],
    template=deliberate_prompt)

action_prompt = '''You are playing a simplified version of the social deduction game One Night Ultimate Werewolf.
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

action_template = PromptTemplate(
    input_variables=[
        'player_id',
        'player_type',
        'player_team',
        'player_goal',
        'info',
        'conversation'],
    template=action_prompt)

vote_prompt = '''You are playing a simplified version of the social deduction game One Night Ultimate Werewolf.
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

vote_template = PromptTemplate(
    input_variables=[
        'player_id',
        'player_type',
        'player_team',
        'vote_goal',
        'player_list',
        'conversation'],
    template=vote_prompt)