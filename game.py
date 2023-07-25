import os
import json
from collections import Counter
import random
from typing import Tuple

import openai
from langchain.llms import OpenAI
from langchain import PromptTemplate
import streamlit as st

from prompts import *

openai.api_key = os.environ.get('OPENAI_API_KEY')

# Class

# class Player:
#     def __init__(
#         self,
#         id,
#         role,
#         team,
#         knowledge,
#         goals
#     ):
#         self.id = id
#         self.role = role
#         self.team = team
#         self.knowledge = knowledge
#         self.goals = goals

class WerewolfGame:
    def __init__(self):
        self.conversation = ''
        self.thoughts = []
        self.players = {
            'Saul Goodman': 'Villager',
            'Kim Wexler': 'Villager',
            'Lalo Salomanca': 'Werewolf',
            'Gus Fring': 'Seer',
            'Mike Ehrmantrout': 'Villager',
            'Nacho Varga': 'Villager',
            'Chuck McGill': 'Werewolf',
            'Howard Hamlin': 'Villager'}
        self.round_counter = 0