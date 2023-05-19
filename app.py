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

default_values = {
    'Saul Goodman': 'Villager',
    'Kim Wexler': 'Villager',
    'Lalo Salomanca': 'Werewolf',
    'Gus Fring': 'Seer',
    'Mike Ehrmantrout': 'Villager',
    'Nacho Varga': 'Villager',
    'Chuck McGill': 'Werewolf',
    'Howard Hamlin': 'Villager'
}

input_col1, input_col2 = st.columns(2)

with input_col1:
    player_names = []
    for i in range(1, players_n + 1):
        key = list(default_values.keys())[i-1]
        player_name = st.text_input(label=f'Player {i} Name', value=key)
        player_names.append(player_name)

with input_col2:
    player_roles = []
    for i in range(1, players_n + 1):
        value = list(default_values.values())[i-1]
        player_role = st.selectbox(
            label=f'Player {i} Role',
            options=('Villager', 'Werewolf', 'Seer')
        )
        player_roles.append(player_role)

run_col1, run_col2 = st.columns(2)

with run_col1:
    run = st.button(label='Simulate Game')
with run_col2:
    dev_run = st.button(label='Dev Run')

# Execute game

if run or dev_run:
    game = WerewolfGame()
    game.players = {key: value for key, value in zip(player_names, player_roles)}
    vote_results = game.full_game(rounds_n)
    st.markdown('#### Deliberation')
    st.write(game.conversation)
    st.markdown('#### Results')
    st.write(vote_results)

if dev_run:
    st.markdown('#### Thoughts')
    st.write(game.thoughts)
