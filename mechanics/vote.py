from collections import Counter
from typing import Dict

from llms import call_llm, vote_template
from mechanics.utils.fetch_data import get_player_data, get_player_team

def player_vote(
    players: Dict[str, str],
    player_id: str,
    player_type: str,
    conversation: str
    ) -> str:
    '''
    Based on all available info to an AI player, return a player name that the AI player votes for as the Werewolf
    '''

    player_list = list(players.keys())
    players_str = ', '.join(player_list)

    player_attributes = get_player_data(player_type)
    prompt = vote_template.format(
        player_id=player_id,
        player_type=player_type,
        player_team=player_attributes[0],
        vote_goal=player_attributes[3],
        player_list=players_str,
        conversation=conversation
    )

    vote = call_llm(prompt)
    return vote

def all_vote(
    players: Dict[str, str],
    conversation: str):
    '''
    Collect votes from all players and calculate the final result
    '''
    
    vote_results = []
    for player_id, player_type in players.items():
        vote = player_vote(players, player_id, player_type, conversation)
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
        eliminated_role = players[eliminated_player]
        losing_team = get_player_team(eliminated_role)

        if losing_team == 'villager':
            winning_team = 'werewolf'
        elif losing_team == 'werewolf':
            winning_team = 'villager'
        
        return winning_team, eliminated_player, eliminated_role, dict(counts)