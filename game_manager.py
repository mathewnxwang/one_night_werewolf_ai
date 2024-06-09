from collections import Counter
import typing as t

import streamlit as st

from models import LLMManager
from prompt_templates import (
    MESSAGE_PROMPT,
    SYNTHESIS_PROMPT,
    VOTE_PROMPT)
from players_manager import ActionManager, Player, PlayersManager
from project_resource import (
    PlayerNames,
    Roles,
    UserInteractionOption,
    LLMOption,
    PlayerLLMResponse,
    PlayerTurnData,
    VoteResult)

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
        self.thoughts: t.List[PlayerLLMResponse] = []

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

        thinking_msg = f'{player.name} is collecting their thoughts...'
        st.write(thinking_msg)

        if self.use_llm_option == LLMOption.NO_LLM:
            player_turn_data = self._generate_dummy_player_turn_data(player)
        else:
            player_turn_data = self._generate_llm_player_turn_data(player)
        
        self.thoughts.append(player_turn_data.thought_process)
        self.conversation = self.conversation + '  \n' + player_turn_data.message

    def _generate_dummy_player_turn_data(self, player: Player) -> PlayerTurnData:
        '''
        Generate dummy data for a player's turn
        '''
        thought = PlayerLLMResponse(player_id=player.name, prompt='dummy prompt', response='dummy thought')
        st.write(thought)
        message = f'{player.name}: dummy message'
        st.write(message)
        return PlayerTurnData(thought_process=thought, message=message)

    def _generate_llm_player_turn_data(self, player: Player) -> PlayerTurnData:
        other_player_names = [player.name for player in self.players_manager.players]
        other_player_names.remove(player.name)
        other_player_names_str = ', '.join(other_player_names)

        PROMPT_PLAYER_INTRO = f'''You are {player.name} from the TV show Rick and Morty, and you speak like them.
You are a {player.starting_role}.
You are on the {player.known_team} team.
The other players in the game are {other_player_names_str}.'''

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
            thought_process=thought_process.response,
            conversation=self.conversation,
            player_id=player.name
        )
        message = self._get_player_response(player.name, message_prompt)
        st.write(message)

        formatted_message = f'{player.name}: {message.response}'
        st.write(formatted_message)

        return PlayerTurnData(thought_process=thought_process, message=formatted_message)

    def _get_player_response(self, player_name: str, prompt: str) -> PlayerLLMResponse:
        '''
        Call LLM and structure response
        '''
        response = self.llm_manager.call_llm(prompt)
        structured_response = PlayerLLMResponse(
            player_id=player_name,
            prompt=prompt,
            response=response
        )
        return structured_response

    def player_vote(self, player: Player) -> str:
        '''
        Based on all available info to an AI player, return a player name that the AI player votes for as the Werewolf
        '''
        if self.use_llm_option == LLMOption.NO_LLM:
            return 'MORTY'
        
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

    def all_vote(self) -> VoteResult:
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
            return VoteResult(
                winning_team='WEREWOLF',
                voted_player='tie',
                voted_player_role='tie',
                vote_counts=dict(counts)
            )        
        else:
            eliminated_player_name = counts[0][0]
            eliminated_player_data = self.action_manager._get_player_by_name(eliminated_player_name)
            eliminated_role = eliminated_player_data.true_role
            losing_team = eliminated_player_data.true_team

            if losing_team == 'VILLAGER':
                winning_team = 'WEREWOLF'
            elif losing_team == 'WEREWOLF':
                winning_team = 'VILLAGER'
            
            return VoteResult(
                winning_team=winning_team,
                voted_player=eliminated_player_name,
                voted_player_role=eliminated_role,
                vote_counts=dict(counts)
            )

    def show_results(self):
        st.markdown('#### Results')
        vote_result = self.all_vote()

        if vote_result.voted_player == 'tie':
            win_msg = '''Players couldn\'t agree on who to eliminate and the vote ended up tied.
            As a result, the werewolf team wins!'''
        else:
            win_msg = f'''{vote_result.voted_player} was voted to be eliminated. They were a {vote_result.voted_player_role}!
            As a result, the {vote_result.winning_team} team wins!'''
        st.write(win_msg)
        print(win_msg)
        
        st.markdown('#### Vote breakdown')
        for name, count in vote_result.vote_counts.items():
            vote_breakdown = f'{name}: {count} votes'
            st.write(vote_breakdown)
            print(vote_breakdown)