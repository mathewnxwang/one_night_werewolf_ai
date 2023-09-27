villager_thought_example = '''Goal: What can I say to find out who the werewolf is?
Conversation:
Information: None
Thought Process: I should ask a specific player who they are and try to identify contradictions between players' responses that would allow me to deduce who the werewolf is.
'''

werewolf_thought_example = '''Goal: What can I say to prevent the other players from finding out that I'm the werewolf?
Conversation:
Information: None
Thought Process: I should consider pretending to be another role instead of the werewolf and accuse other players of being the werewolf.
'''

troublemaker_thought_example = '''Goal: What can I say to find out who the werewolf is?
Conversation:
Information: As the troublemaker, you switched the roles of Howard Hamlin and Gus Fring. Now Howard Hamlin is Werewolf and Gus Fring is Villager.
Thought Process: I know that Howard Hamlin is the Werewolf, unless the Robber robbed Howard Hamlin. I should ask to find out who the Robber is and who they robbed.'''

seer_thought_example = '''Goal: What can I say to find out who the werewolf is?
Conversation:
Information: As the seer, you saw that Mike Ermantrout is a Villager.
Thought Process: Unless the Troublemaker or the Robber swapped Mike's role with the Werewolf, Mike is not the Werewolf. I should ask to find out who the Troublemaker and Robber are and who they switched.'''

robber_thought_example = '''Goal: What can I say to find out who the werewolf is?
Conversation: Saul Goodman: Hey everyone, let's start by telling each other our roles. Kim, why don't you start? What kind of character are you in the game? Kim Wexler: I'm a villager! I'm looking for any suspicious behavior and clues that might point to who the werewolf is.
Information: You were previously the Robber. You robbed Kim Wexler who was a Werewolf. You are now a Werewolf and Kim Wexler is the Robber.
Thought Process: I know Kim was the Werewolf so they are lying about being the Villager. However, since I'm the Werewolf now I should consider pretending to be another role instead of the werewolf and accuse other players of being the werewolf.
'''

few_shot_mapping = {
    'Villager': villager_thought_example,
    'Werewolf': werewolf_thought_example,
    'Troublemaker': troublemaker_thought_example,
    'Seer': seer_thought_example,
    'Robber': robber_thought_example
}