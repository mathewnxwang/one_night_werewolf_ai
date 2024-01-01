import streamlit as st

from mechanics.players import PlayerManager
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

### Run options

run_col1, run_col2 = st.columns(2)

with run_col1:
    run = st.button(label='Simulate Game')
with run_col2:
    dev_run = st.button(label='Dev Run')

# Execute game

if run or dev_run:
    full_game(rounds_n)
