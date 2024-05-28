from actions import WaitAction, BumpAction

import random

def random_direction():
    return random.choice([
        (-1,-1), (0,-1), (1,-1),
        (-1,0),          (1,0),
        (-1,1),  (0,1),  (1,1)
    ])


def ai_action(creature, engine):
    ai_type = creature.ai_type
    
    if ai_type == "neutral":
        return neutral_action(creature, engine)
    elif ai_type == "hostile":
        return hostile_action(creature, engine)

def neutral_action(creature, engine):
    return BumpAction(*random_direction())

def hostile_action(creature, engine):
    player_x = engine.player.x
    player_y = engine.player.y

    dx = 0
    dy = 0
    if player_x > creature.x:
        dx = 1
    elif player_x < creature.x:
        dx = -1
    if player_y > creature.y:
        dy = 1
    elif player_y < creature.y:
        dy = -1

    return BumpAction(dx, dy)
