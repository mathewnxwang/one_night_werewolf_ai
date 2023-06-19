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

game = WerewolfGame()
players_list = list(game.players.items())
players_list_filtered = players_list[:players_n]
game.players = dict(players_list_filtered)
input_col1, input_col2 = st.columns(2)

# create configurable text inputs for player names
with input_col1:
    player_names = []
    default_names = list(game.players.keys())

    # generate label and default value for every input
    for i, name in enumerate(default_names):
        player_name = st.text_input(
            label=f'Player {i+1} Name',
            value=name)
        player_names.append(player_name)

# create configurable picklist inputs for player roles
with input_col2:
    player_roles = []
    default_roles = list(game.players.values())
    possible_roles = ('Villager', 'Werewolf', 'Seer')

    # generate label, options, and default value for every input
    for i, role in enumerate(default_roles):
        role_index = possible_roles.index(role)

        player_role = st.selectbox(
            label=f'Player {i+1} Role',
            options=possible_roles,
            index=role_index)
        player_roles.append(player_role)

### Run options

run_col1, run_col2 = st.columns(2)

with run_col1:
    run = st.button(label='Simulate Game')
with run_col2:
    dev_run = st.button(label='Dev Run')

# Execute game

if run or dev_run:
    game.full_game(rounds_n)
