from collections import Counter
from enum import Enum
from typing import Any, Dict

import streamlit as st

from models import LLMManager
from prompt_templates import (
    MESSAGE_PROMPT,
    SYNTHESIS_PROMPT,
    VOTE_PROMPT)
from players_manager import ActionManager, Player, PlayersManager
from project_resource import PlayerNames, Roles, UserInteractionOption, LLMOption

class GameManager:
    def __init__(self, user_interaction_option: UserInteractionOption, use_llm_option: LLMOption):

        self.players_manager = PlayersManager(PlayerNames, Roles)
        self.action_manager = ActionManager(self.players_manager.players)
        self.action_manager.execute_all_actions()
        st.write(self.players_manager.players)

        self.llm_manager = LLMManager()

        self.user_interaction_option = user_interaction_option
        self.use_llm_option = use_llm_option

        self.conversation = ''
        self.thoughts = []

    def conversation_full(self, rounds: int) -> None:
        '''
        Generate N rounds of conversation
        '''
        round_counter = 1
        while round_counter <= rounds:
            print(f'Executing round {round_counter}')
            self.conversation_round(round_counter)
            round_counter += 1        

    def conversation_round(self, round_counter: int) -> None:
        '''
        Generate one round of conversation where every player speaks once
        '''

        # Steer players toward making pointed contributions later in the game
        if round_counter == 1:
            pass # use a template that steers a player to deliberate
        elif round_counter >= 2:
            pass # use a template that steers a player to take action

        # Every player contributes to the conversation once in order
        for player in self.players_manager.players:
            self.player_turn(player)

    def player_turn(self, player: Player) -> None:
        '''
        Generate and store thoughts and a conversation message for a player
        '''
        player_names_list = [player.name for player in self.players_manager.players]
        player_names_list.remove(player.name)
        player_names_str = ', '.join(player_names_list)

        thinking_msg = f'{player.name} is collecting their thoughts...'
        st.write(thinking_msg)

        PROMPT_PLAYER_INTRO = f'''You are {player.name} from the TV show Rick and Morty, and you speak like them.
You are a {player.starting_role}.
You are on the {player.known_team} team.
The other players in the game are {player_names_str}.'''

        PROMPT_SYNTHESIS_INFO = f'''Goal: {player.starting_goal}
Conversation: {self.conversation}
Information: {player.knowledge}'''

        synthesis_prompt = SYNTHESIS_PROMPT.format(
            player_intro=PROMPT_PLAYER_INTRO, player_info=PROMPT_SYNTHESIS_INFO
        )
        thought_process = self._get_player_response(player.name, synthesis_prompt)
        st.write(thought_process)

        deciding_msg = f'{player.name} is deciding on what to say...'
        st.write(deciding_msg)
        message_prompt = MESSAGE_PROMPT.format(
            player_intro=PROMPT_PLAYER_INTRO,
            thought_process=thought_process['response'],
            conversation=self.conversation,
            player_id=player.name
        )
        message_dict = self._get_player_response(player.name, message_prompt)
        st.write(message_dict)

        message = message_dict['response']
        formatted_message = f'{player.name}: {message}'
        st.write(formatted_message)

        self.thoughts.append(thought_process)
        self.conversation = self.conversation + '  \n' + formatted_message

        chat_msg = f'{player.name}: {message}'

    def _get_player_response(self, player_name: str, prompt: str) -> Dict[str, Any]:
        '''
        Call LLM and structure response
        '''
        response = self.llm_manager.call_llm(prompt)
        
        structured_response = {'player_id': player_name, 'prompt': prompt, 'response': response}    
        return structured_response

    def player_vote(self, player: Player) -> str:
        '''
        Based on all available info to an AI player, return a player name that the AI player votes for as the Werewolf
        '''
        players_list = [player.name for player in self.players_manager.players]
        players_str = ', '.join(players_list)

        PROMPT_PLAYER_INTRO = f'''Your name is {player.name}.
You are a {player.starting_role}.
You are on the {player.known_team} team.'''

        prompt = VOTE_PROMPT.format(
            player_intro=PROMPT_PLAYER_INTRO,
            vote_goal=player.starting_goal,
            player_list=players_str,
            conversation=self.conversation
        )

        vote = self.llm_manager.call_llm(prompt)
        return vote

    def all_vote(self):
        '''
        Collect votes from all players and calculate the final result
        '''
        
        vote_results = []
        for player in self.players_manager.players:
            vote = self.player_vote(player)
            vote_results.append(vote)

        counter = Counter(vote_results)
        counts = counter.most_common()

        # check if there are more than 1 players with votes
        # and if the 2 players with the greatest number of votes
        # are tied with the same number of votes
        if len(counts) != 1 and counts[0][1] == counts[1][1]:
            return 'werewolf', 'tie', 'tie', dict(counts)
        
        else:
            eliminated_player_name = counts[0][0]
            eliminated_player_data = self.action_manager._get_player_by_name(eliminated_player_name)
            eliminated_role = eliminated_player_data.true_role
            losing_team = eliminated_player_data.true_team

            if losing_team == 'villager':
                winning_team = 'werewolf'
            elif losing_team == 'werewolf':
                winning_team = 'villager'
            
            return winning_team, eliminated_player_data, eliminated_role, dict(counts)

    def show_results(self):
        st.markdown('#### Results')
        winning_team, eliminated_player, eliminated_role, vote_data = self.all_vote()

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