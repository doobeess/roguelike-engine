from tcod.context import Context
from tcod.console import Console

import tcod

from typing import Set, Iterable, Any

from game_map import GameMap

from player import Player
from input_handlers import MainGameScreenHandler, ViewInventoryScreenHandler, DropScreenHandler

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
        self.screen_handler = screen_handler
        self.game_map = game_map
        self.player = player
        self.message_log = message_log
        self.main_screen_handler = screen_handler
        self.screen_handler_list = [screen_handler]
        self.active_screen_handler = screen_handler
        self.context = context

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


            


