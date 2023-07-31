from collections import Counter
from typing import Any, Dict

import streamlit as st

from ai.prompt_templates import vote_template
from ai.llm import call_llm
from mechanics.utils.fetch_data import get_player_data, get_player_team

def player_vote(
    players: Dict[str, Dict[str, Any]],
    player_id: str,
    conversation: str
    ) -> str:
    '''
    Based on all available info to an AI player, return a player name that the AI player votes for as the Werewolf
    '''

    player_list = list(players.keys())
    players_str = ', '.join(player_list)

    player_data = players[player_id]
    prompt = vote_template.format(
        player_id=player_id,
        player_type=player_data['starting_role'],
        player_team=player_data['starting_team'],
        vote_goal=player_data['starting_goal'],
        player_list=players_str,
        conversation=conversation
    )

    vote = call_llm(prompt)
    return vote

def all_vote(
    players: Dict[str, Dict[str, Any]],
    conversation: str):
    '''
    Collect votes from all players and calculate the final result
    '''
    
    vote_results = []
    for player_name in players.keys():
        vote = player_vote(players, player_name, conversation)
        vote_results.append(vote)

    counter = Counter(vote_results)
    counts = counter.most_common()

    # check if there are more than 1 players with votes
    # and if the 2 players with the greatest number of votes
    # are tied with the same number of votes
    if len(counts) != 1 and counts[0][1] == counts[1][1]:
        return 'werewolf', 'tie', 'tie', dict(counts)
    
    else:
        eliminated_player = counts[0][0]
        eliminated_player_data = players[eliminated_player]
        eliminated_role = eliminated_player_data['true_role']
        losing_team = eliminated_player_data['true_team']

        if losing_team == 'villager':
            winning_team = 'werewolf'
        elif losing_team == 'werewolf':
            winning_team = 'villager'
        
        return winning_team, eliminated_player, eliminated_role, dict(counts)

def show_results(players: Dict[str, Dict[str, Any]], conversation: str):
    st.markdown('#### Results')
    winning_team, eliminated_player, eliminated_role, vote_data = all_vote(players, conversation)

    if eliminated_player == 'tie':
        win_msg = '''Players couldn\'t agree on who to eliminate and the vote ended up tied.
        As a result, the werewolf team wins!'''
    else:
        win_msg = f'''{eliminated_player} was voted to be eliminated. They were a {eliminated_role}!
        As a result, the {winning_team} team wins!'''
    st.write(win_msg)
    print(win_msg)
    
    st.markdown('#### Vote breakdown')
    for name, count in vote_data.items():
        vote_breakdown = f'{name}: {count} votes'
        st.write(vote_breakdown)
        print(vote_breakdown)