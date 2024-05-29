import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int, tiles=[], creatures=[], items=[]):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), tile_types.floor)

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

        self.creatures = creatures
        self.items = items

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )
        for entity in self.creatures + self.items:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, entity.color)

    def get_creature_at(self, x, y):
        for creature in self.creatures:
            if (creature.x, creature.y) == (x,y):
                return creature
        return None

    def get_item_at(self, x, y):
        for item in self.items:
            if (item.x, item.y) == (x,y):
                return item
        return None