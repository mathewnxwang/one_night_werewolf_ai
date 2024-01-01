import json
from typing import Any, Dict, Tuple

from langchain import PromptTemplate
import streamlit as st

from ai.llm import call_llm
from ai.prompt_templates import synthesis_template, message_template

def _get_player_response(player_name: str, prompt: PromptTemplate) -> Dict[str, Any]:
    '''
    Call LLM and structure response
    '''
    response = call_llm(prompt)
    
    structured_response = {'player_id': player_name, 'prompt': prompt, 'response': response}    
    return structured_response

def player_turn(
    players,
    player_name: str,
    prompt_template: PromptTemplate,
    conversation: str,
    thoughts: list[dict]
    ) -> Tuple[str, Dict[str, Any]]:
    '''
    Generate and store thoughts and a conversation message for a player
    '''
    
    player_data = players[player_name]
    player_names_list = list(players.keys())
    player_names_list.remove(player_name)
    player_names_str = ', '.join(player_names_list)

    thinking_msg = f'{player_name} is collecting their thoughts...'
    st.write(thinking_msg)

    PROMPT_PLAYER_INTRO = f'''Your name is {player_name}.
You are a {player_data['starting_role']}.
You are on the {player_data['starting_team']} team.
The other players in the game are {player_names_str}.'''

    PROMPT_SYNTHESIS_INFO = f'''Goal: {player_data['starting_goal']}
Conversation: {conversation}
Information: {player_data['knowledge']}'''

    synthesis_prompt = synthesis_template.format(
        player_intro=PROMPT_PLAYER_INTRO, player_info=PROMPT_SYNTHESIS_INFO
    )
    thought_process = _get_player_response(player_name, synthesis_prompt)
    st.write(thought_process)

    deciding_msg = f'{player_name} is deciding on what to say...'
    st.write(deciding_msg)
    message_prompt = message_template.format(
        player_intro=PROMPT_PLAYER_INTRO,
        thought_process=thought_process['response'],
        conversation=conversation,
        player_id=player_name
    )
    message_dict = _get_player_response(player_name, message_prompt)
    st.write(message_dict)

    message = message_dict['response']
    formatted_message = f'{player_name}: {message}'
    st.write(formatted_message)

    thoughts.append(thought_process)
    conversation = conversation + '  \n' + formatted_message

    chat_msg = f'{player_name}: {message}'

    return conversation, thoughts