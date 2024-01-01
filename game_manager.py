from collections import Counter
from typing import Any, Dict

from langchain import PromptTemplate
import streamlit as st

from llm import call_llm
from prompt_templates import (
    action_template,
    deliberate_template,
    message_template,
    synthesis_template,
    vote_template)
from players import PlayerManager
from role_actions import RoleActions

class GameManager:
    def __init__(self):

        player_manager = PlayerManager(players_n=5)
        role_actions = RoleActions()

        self.player_data = player_manager.construct_player_data()
        self.player_data = role_actions.execute_all_actions(self.player_data)
        st.write(self.player_data)

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
            prompt_template = deliberate_template
        elif round_counter >= 2:
            prompt_template = action_template

        # Every player contributes to the conversation once in order
        for player_name, player_i_data in self.player_data.items():        
            self.player_turn(player_i_data, player_name, prompt_template)

    def player_turn(
        self,
        player_i_data,
        player_name: str,
        prompt_template: PromptTemplate,
        ) -> None:
        '''
        Generate and store thoughts and a conversation message for a player
        '''
        player_names_list = list(self.player_data.keys())
        player_names_list.remove(player_name)
        player_names_str = ', '.join(player_names_list)

        thinking_msg = f'{player_name} is collecting their thoughts...'
        st.write(thinking_msg)

        PROMPT_PLAYER_INTRO = f'''Your name is {player_name}.
You are a {player_i_data['starting_role']}.
You are on the {player_i_data['starting_team']} team.
The other players in the game are {player_names_str}.'''

        PROMPT_SYNTHESIS_INFO = f'''Goal: {player_i_data['starting_goal']}
Conversation: {self.conversation}
Information: {player_i_data['knowledge']}'''

        synthesis_prompt = synthesis_template.format(
            player_intro=PROMPT_PLAYER_INTRO, player_info=PROMPT_SYNTHESIS_INFO
        )
        thought_process = self._get_player_response(player_name, synthesis_prompt)
        st.write(thought_process)

        deciding_msg = f'{player_name} is deciding on what to say...'
        st.write(deciding_msg)
        message_prompt = message_template.format(
            player_intro=PROMPT_PLAYER_INTRO,
            thought_process=thought_process['response'],
            conversation=self.conversation,
            player_id=player_name
        )
        message_dict = self._get_player_response(player_name, message_prompt)
        st.write(message_dict)

        message = message_dict['response']
        formatted_message = f'{player_name}: {message}'
        st.write(formatted_message)

        self.thoughts.append(thought_process)
        self.conversation = self.conversation + '  \n' + formatted_message

        chat_msg = f'{player_name}: {message}'

    def _get_player_response(self, player_name: str, prompt: PromptTemplate) -> Dict[str, Any]:
        '''
        Call LLM and structure response
        '''
        response = call_llm(prompt)
        
        structured_response = {'player_id': player_name, 'prompt': prompt, 'response': response}    
        return structured_response

    def player_vote(self, player_id: str) -> str:
        '''
        Based on all available info to an AI player, return a player name that the AI player votes for as the Werewolf
        '''

        player_list = list(self.player_data.keys())
        players_str = ', '.join(player_list)

        player_i_data = self.player_data[player_id]

        PROMPT_PLAYER_INTRO = f'''Your name is {player_id}.
You are a {player_i_data['starting_role']}.
You are on the {player_i_data['starting_team']} team.'''

        prompt = vote_template.format(
            player_intro=PROMPT_PLAYER_INTRO,
            vote_goal=player_i_data['starting_goal'],
            player_list=players_str,
            conversation=self.conversation
        )

        vote = call_llm(prompt)
        return vote

    def all_vote(self):
        '''
        Collect votes from all players and calculate the final result
        '''
        
        vote_results = []
        for player_name in self.player_data.keys():
            vote = self.player_vote(player_name)
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
            eliminated_player_data = self.player_data[eliminated_player]
            eliminated_role = eliminated_player_data['true_role']
            losing_team = eliminated_player_data['true_team']

            if losing_team == 'villager':
                winning_team = 'werewolf'
            elif losing_team == 'werewolf':
                winning_team = 'villager'
            
            return winning_team, eliminated_player, eliminated_role, dict(counts)

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