import json
from typing import Dict, Any

from langchain import PromptTemplate
from langchain.llms import OpenAI
import streamlit as st

from mechanics.utils.fetch_data import get_player_data
from llms import call_llm

def player_turn(
    player_name: str,
    player_data: Dict[str, Any],
    prompt_template: PromptTemplate,
    conversation: str,
    thoughts: list[dict]
    ) -> None:
    '''
    Generate and store thoughts and a conversation message for a player
    '''

    thinking_msg = f'{player_name} is thinking...'
    st.write(thinking_msg)

    prompt = prompt_template.format(
        player_id=player_name,
        player_type=player_data['role'],
        player_team=player_data['team'],
        player_goal=player_data['goal'],
        info=player_data['knowledge'],
        conversation=conversation
    )

    raw_thought = call_llm(prompt)

    try:
        parsed_thought = json.loads(raw_thought)
    except json.JSONDecodeError:
        parsed_thought = 'I have a brain fart... I think I\'ll skip my turn.'
    
    structured_thought = {
        'player_id': player_name,
        'prompt': prompt,
        'thoughts': parsed_thought
    }
    print(structured_thought)
    thoughts.append(structured_thought)

    try:
        message = structured_thought['thoughts']['message']
    except TypeError:
        message = 'I have a brain fart... I think I\'ll skip my turn.'
    
    formatted_message = f'{player_name}: {message}'
    print(formatted_message)
    conversation = conversation + '  \n' + formatted_message

    chat_msg = f'{player_name}: {message}'
    st.write(chat_msg)
    st.write(structured_thought)

    return conversation, thoughts