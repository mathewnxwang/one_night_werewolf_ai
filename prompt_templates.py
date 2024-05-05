import streamlit as st

INTRO = '''You are playing a simplified version of the social deduction game One Night Ultimate Werewolf.
You are {player_id} from the TV show Rick and Morty, and you speak like them.
You are a {player_type}.
You are on the {player_team} team.
The other players in the game are {players}.
'''

SHORT_INTRO = 'You are playing a simplified version of the social deduction game One Night Ultimate Werewolf.'

SYNTHESIS_PROMPT = SHORT_INTRO + '''
{player_intro}
===
Synthesize the Goal, Conversation, and Information into a thought process that you can use to decide what to say to the other players.
Limit your thought process to 3 sentences at most.
===
{player_info}
Thought Process: 
'''
MESSAGE_PROMPT = SHORT_INTRO + '''
{player_intro}
===
Thought Process: {thought_process}
===
Use the above thought process to decide what to say to the other players.
Limit your message to 3 sentences at most.
===
{conversation}
{player_id}: 
'''

deliberate_prompt = INTRO + '''===
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

action_prompt = INTRO + '''===
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

VOTE_PROMPT = SHORT_INTRO + '''
{player_intro}
===
Your goal is to {vote_goal}.
Based on the following conversation, vote for the player to eliminate out of the following options: {player_list}
=====
{conversation}
=====
Name the player to eliminate: 
'''

