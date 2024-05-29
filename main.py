import tcod

from engine import Engine

from game_map import GameMap

from player import Player

from item import Item

from screen_handlers import MainGameScreenHandler

from message_log import MessageLog


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 60
    map_height = 40

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    tileset = tcod.tileset.load_tilesheet(
        "font.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        
        player = Player(5,5, 20)

        game_map = GameMap(map_width, map_height)

        screen_handler = MainGameScreenHandler()
        
        message_log = MessageLog(10)

        engine = Engine(
            screen_handler = screen_handler, 
            game_map = game_map, 
            player = player, 
            message_log = message_log,
            context = context,
            map_width = map_width,
            map_height = map_height
        )

        engine.render(root_console)
        
        engine.main_loop(root_console)

if __name__ == "__main__":
    main()
