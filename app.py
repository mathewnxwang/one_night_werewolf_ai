import openai
import os
openai.api_key = os.environ.get('OPENAI_API_KEY')
from langchain import PromptTemplate
from langchain.llms import OpenAI
call_llm = OpenAI()
import json
from collections import Counter
import streamlit as st
from game import WerewolfGame

page_title = 'One Night Werewolf, AI Version'
st.set_page_config(page_title=page_title)

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

# Execute game

if run_button:
    game = WerewolfGame()
    game.players = {
        player_1: player_1_role,
        player_2: player_2_role,
        player_3: player_3_role,
        player_4: player_4_role,
        player_5: player_5_role
    }
    vote_results = game.full_game(rounds_n)
    st.markdown('#### Deliberation')
    st.write(game.conversation)
    st.markdown('#### Results')
    st.write(vote_results)

