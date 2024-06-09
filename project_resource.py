import typing as t
from enum import Enum

from pydantic import BaseModel

class Roles(Enum):
    WEREWOLF = "WEREWOLF"
    SEER = "SEER"
    VILLAGER = "VILLAGER"
    ROBBER = "ROBBER"
    TROUBLEMAKER = "TROUBLEMAKER"

class PlayerNames(Enum):
    MORTY = "Morty"
    RICK = "Rick"
    SUMMER = "Summer"
    BETH = "Beth"
    JERRY = "Jerry"

class Team(Enum):
    VILLAGER = 'VILLAGER'
    SEER = 'VILLAGER'
    ROBBER = 'VILLAGER'
    TROUBLEMAKER = 'VILLAGER'
    WEREWOLF = 'WEREWOLF'

class GoalPrompt(Enum):
    VILLAGER = "What can I say to find out who the werewolf is?"
    WEREWOLF = "What can I say to prevent the other players from finding out that I\'m the werewolf?"

class VotePrompt(Enum):
    VILLAGER = "Vote for a player who is the werewolf."
    WEREWOLF = "Vote for a player who is not the werewolf."

class UserInteractionOption(Enum):
    HUMAN_PLAYER = 'Play against AI'
    AI_ONLY = 'Watch AI play against each other'

class LLMOption(Enum):
    GPT_4 = 'Sophisticated (GPT-4)'
    GPT_3_5 = 'Unsophisticated (GPT-3.5)'
    NO_LLM = 'Use dummy data for testing'

class Player(BaseModel):
    name: str
    starting_role: str
    true_role: str
    true_team: str
    known_team: str
    starting_goal: str
    vote_goal: str
    knowledge: str = ""

class PlayerLLMResponse(BaseModel):
    player_id: str
    prompt: str
    response: str

class PlayerTurnData(BaseModel):
    thought_process: PlayerLLMResponse
    message: str

class VoteResult(BaseModel):
    winning_team: str
    voted_player: str
    voted_player_role: str
    vote_counts: t.Dict