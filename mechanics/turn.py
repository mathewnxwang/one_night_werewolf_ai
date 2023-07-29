import json

from langchain import PromptTemplate
from langchain.llms import OpenAI
import streamlit as st

from mechanics.utils.fetch_data import get_player_data

def player_turn(
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

    player_team, player_knowledge, player_goal, _ = get_player_data(player_id, player_type)

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
    except json.JSONDecodeError:
        parsed_thought = 'I have a brain fart... I think I\'ll skip my turn.'
    
    structured_thought = {
        'player_id': player_id,
        'prompt': prompt,
        'thoughts': parsed_thought
    }
    thoughts.append(structured_thought)

    try:
        message = structured_thought['thoughts']['message']
    except TypeError:
        message = 'I have a brain fart... I think I\'ll skip my turn.'
    
    formatted_message = f'{player_id}: {message}'
    conversation = conversation + '  \n' + formatted_message

    chat_msg = f'{player_id}: {message}'
    st.write(chat_msg)
    st.write(structured_thought)