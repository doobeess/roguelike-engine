from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

from message_log import MessageLog


class Action:
    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog) -> None:
        raise SystemExit()


class DirectionalAction(Action):
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy


class BumpAction(DirectionalAction):
    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_creature_at(dest_x, dest_y) or (engine.player.x, engine.player.y) == (dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity, message_log)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity, message_log)

class MovementAction(DirectionalAction):
    def __init__(self, dx: int, dy: int):
        super().__init__(dx, dy)

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return True # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return True # Destination is blocked by a tile.
        
        entity.move(self.dx, self.dy)


def construct_attack_sentence(attacker, target, player):
    text = ""

    if attacker == player:
        text += "You hit "
    else:
        text += "The " + attacker.name + " hits "

    if target == player:
        text += "you"
    else:
        text += "the " + target.name

    text += "!"

    if target == player:
        text_color = (255, 0, 0)
    elif attacker == player:
        text_color = (54, 131, 255)
    else:
        text_color = (255, 255, 255)

    return text, text_color


class MeleeAction(DirectionalAction):
    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        target = engine.game_map.get_creature_at(dest_x, dest_y)
        
        if not target:
            target = engine.player

        attacker = entity
        
        target.hp -= 1
        message_log.log(
            *construct_attack_sentence(attacker, target, engine.player)
        )

class WaitAction(Action):
    def __init__(self):
        super().__init__()

    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog) -> None:
        # The entity waits for one turn.
        pass

class PickUpAction(Action):
    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog):
        x = engine.player.x
        y = engine.player.y
        if engine.game_map.get_item_at(x,y):
            item = engine.game_map.get_item_at(x,y)
            engine.player.pick_up(item, engine.game_map)
            message_log.log(f"You pick up the {item.name}.", (0,255,0))
        else:
            message_log.log("There are no items here.")
            return True

class DropAction(Action):
    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog):
        if engine.player.has_items():
            engine.add_menu('drop')
        else:
            engine.message_log.log('You are carrying nothing.')
        return 1

class ViewInventoryAction(Action):
    def perform(self, engine: Engine, entity: Entity, message_log: MessageLog) -> None:
        if engine.player.has_items():
            engine.add_menu('inventory')
        else:
            engine.message_log.log('You are carrying nothing.')
        return 1