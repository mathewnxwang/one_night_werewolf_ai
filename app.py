import streamlit as st

from game_manager import GameManager
from project_resource import UserInteractionOption, LLMOption
from utils import get_enum_member_by_value

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
    game_option = st.selectbox(
        label='Game option',
        options=[option.value for option in UserInteractionOption]
    )

with run_col2:
    llm_option = st.selectbox(
        label='Select LLM option',
        options=[option.value for option in LLMOption]
    )

run = st.button(label='Start game!')

# Execute game
if run:
    st.markdown('#### Deliberation')
    game_option_member = get_enum_member_by_value(UserInteractionOption, game_option)
    llm_option_member = get_enum_member_by_value(LLMOption, llm_option)
    game_manager = GameManager(game_option_member, llm_option_member)
    game_manager.conversation_full(rounds_n)
    game_manager.show_results()
