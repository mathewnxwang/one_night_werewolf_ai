import streamlit as st

from mechanics.players import init_players
from run import full_game

page_title = 'One Night Werewolf, AI Version'
st.set_page_config(page_title=page_title)

### Configuration

st.header('Configuration')

col1, col2 = st.columns(2)

with col1:
    rounds_n = st.number_input(
        label='How many rounds of deliberation?', min_value=1, max_value=5, value=3
    )

# create configurable text inputs for player names
players = init_players(players_n=4)

with col2:
    player_names = []
    default_names = players.copy()

    # generate label and default value for every input
    for i, name in enumerate(default_names):
        player_name = st.text_input(
            label=f'Player {i+1} Name',
            value=name)
        player_names.append(player_name)

### Run options

run_col1, run_col2 = st.columns(2)

with run_col1:
    run = st.button(label='Simulate Game')
with run_col2:
    dev_run = st.button(label='Dev Run')

# Execute game

if run or dev_run:
    full_game(rounds_n, players)
