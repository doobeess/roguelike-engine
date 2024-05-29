from actions import WaitAction, BumpAction

import random

DIRECTIONS = [
    (-1,-1), (0,-1), (1,-1),
    (-1,0),          (1,0),
    (-1,1),  (0,1),  (1,1) 
]

def random_empty_direction(x,y,engine):
    direction = None
    selected = False
    directions_left = DIRECTIONS[:]
    while not selected:
        direction = random.choice(directions_left)
        new_position = (x+direction[0], y+direction[1])
        if not engine.game_map.get_creature_at(*new_position):
            if (engine.player.x, engine.player.y) != (new_position[0], new_position[1]):
                try:
                    if engine.game_map.tiles["walkable"][new_position[0], new_position[1]]:
                        selected = True
                except IndexError:
                    pass
        if not selected:
            directions_left.remove(direction)

    return direction



def ai_action(creature, engine):
    ai_type = creature.ai_type
    
    if ai_type == "neutral":
        return neutral_action(creature, engine)
    elif ai_type == "hostile":
        return hostile_action(creature, engine)

def neutral_action(creature, engine):
    return BumpAction(*random_empty_direction(creature.x, creature.y, engine))

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
