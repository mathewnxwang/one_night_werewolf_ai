import json
from typing import Any, Dict, Tuple

from langchain import PromptTemplate
import streamlit as st

from ai.llm import call_llm
from ai.prompt_templates import synthesis_template, message_template
from ai.few_shot_examples import few_shot_mapping

def _get_player_response(player_name: str, prompt: PromptTemplate) -> Dict[str, Any]:
    '''
    Call LLM and structure response
    '''
    response = call_llm(prompt)
    
    structured_response = {'player_id': player_name, 'prompt': prompt, 'response': response}    
    return structured_response

def _get_few_shot_examples(player_data: Dict[str, Any]) -> str:
    try:
        examples = few_shot_mapping[player_data['starting_role']]
    except KeyError:
        return ''
    return examples

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

    few_shot_examples = _get_few_shot_examples(player_data)

    synthesis_prompt = synthesis_template.format(
        player_id=player_name,
        player_type=player_data['starting_role'],
        player_team=player_data['starting_team'],
        players=player_names_str,
        player_goal=player_data['starting_goal'],
        conversation=conversation,
        info=player_data['knowledge'],
        few_shot_examples=few_shot_examples
    )
    thought_process = _get_player_response(player_name, synthesis_prompt)
    st.write(thought_process)

    deciding_msg = f'{player_name} is deciding on what to say...'
    st.write(deciding_msg)
    message_prompt = message_template.format(
        player_id=player_name,
        player_type=player_data['starting_role'],
        player_team=player_data['starting_team'],
        players=player_names_str,
        thought_process=thought_process['response'],
        conversation=conversation
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