from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

import tcod

from typing import Set, Iterable, Any

from game_map import GameMap

from player import Player
from screen_handlers import MainGameScreenHandler, ViewInventoryScreenHandler, DropScreenHandler

from message_log import MessageLog


MENU_TYPES = {
    'inventory': ViewInventoryScreenHandler,
    'drop': DropScreenHandler,
}


class Engine:
    def __init__(self, *,
            screen_handler: MainGameScreenHandler, 
            game_map: GameMap, 
            player: Player,
            message_log: MessageLog,
            context: Context,
            map_width: int,
            map_height: int
        ):
        
        self.game_map = game_map
        self.player = player
        self.message_log = message_log

        # Screen handlers render certain parts of the screen,
        # and also determine what user input does based on the
        # current screen.
        self.main_screen_handler = screen_handler
        self.screen_handler_list = [screen_handler]
        self.active_screen_handler = screen_handler

        self.context = context

        self.update_fov()

        self.map_width = map_width
        self.map_height = map_height

    def handle_events(self, events: Iterable[Any]) -> None:
        turn_code = 0
        
        self.active_screen_handler = self.screen_handler_list[-1]

        for event in events:
            new_code = self.active_screen_handler.handle_event(event, self)
            if new_code > turn_code:
                turn_code = new_code

        return turn_code
    
    def add_menu(self, menu_type):
        try:
            screen_handler = MENU_TYPES[menu_type](self)
            self.screen_handler_list.append(screen_handler)
            self.active_screen_handler = screen_handler
        except KeyError:
            self.message_log.log("Error: Cannot open menu", color=(255,0,0))

    def delete_current_screen_handler(self):
        del self.screen_handler_list[-1]

    def creatures_act(self):
        for creature in self.game_map.creatures:
            action = creature.act(self)
            action.perform(self, creature, self.message_log)

    def render(self, console: Console) -> None:
        for screen_handler in self.screen_handler_list:
            screen_handler.on_render(console, self)

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=6,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def main_loop(self, console):
        while True:

            self.context.present(console)
            console.clear()

            turn_code = 0
            while not turn_code > 0:
                events = tcod.event.wait()
                turn_code = self.handle_events(events)

            if turn_code > 0:
                if turn_code > 1:
                    new_creatures = []
                    for creature in self.game_map.creatures:
                        if not creature.is_dead():
                            new_creatures.append(creature)
                        else:
                            self.message_log.log(f"You defeated the {creature.name}!")
                
                    self.game_map.creatures = new_creatures
                            
                    self.creatures_act()

                    if self.player.is_dead():
                        print("Game over!")
                        break
            
                self.render(console)


            


