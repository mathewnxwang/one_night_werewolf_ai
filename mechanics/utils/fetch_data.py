from typing import Tuple

def get_player_team(true_role: str, known_role: str) -> str:
    '''
    Get the team based on the player role
    '''

    villager_values = ['Villager', 'Seer', 'Robber', 'Troublemaker']

    if true_role in villager_values:
        true_team = 'villager'
    else:
        true_team = 'werewolf'
    
    if known_role in villager_values:
        known_team = 'villager'
    else:
        known_team = 'werewolf'
    
    return true_team, known_team

def get_player_knowledge(player_type: str) -> str:
    # if player_type == 'Seer':
    #     execute_seer_action()
    return

def get_player_goals(player_team: str) -> Tuple[str, str]:

    if player_team == 'villager':
        player_goal = '''What can I say to find out who the werewolf is?'''
        vote_goal = '''Vote for the player who you think is the werewolf.'''
    elif player_team == 'werewolf':
        player_goal = '''What can I say to prevent the other players from finding out that I'm the werewolf?'''
        vote_goal = '''Vote for a player who is not the werewolf.'''
    
    return player_goal, vote_goal

def get_player_data(
    player_type: str
    ) -> Tuple[str, str, str, str]:
    '''
    Get player attributes to generate a conversation message
    '''

    player_team = get_player_team(player_type)
    player_knowledge = get_player_knowledge(player_type)
    player_goals = get_player_goals(player_team)

    player_data = (player_team, player_knowledge) + player_goals
    return player_data

    # elif player_type == 'Seer':
    #     team = 'villager'
    #     seen_player_name, seen_player_role = self.execute_card_action(player_id, player_type)
    #     info = f'As the seer, you can see that {seen_player_name} is a {seen_player_role}.'
    #     player_attributes = ('villager', info)
    
    # elif player_type == 'Robber':
    #     team = 'villager'
    #     traded_player = self.execute_card_action(player_id, player_type)
    #     traded_player_name, traded_player_role = traded_player