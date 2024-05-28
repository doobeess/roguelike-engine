import numpy as np  # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int, creatures=[], items=[]):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        self.tiles[30:33, 22] = tile_types.wall
        # Pathing will be added later.

        self.creatures = creatures
        self.items = items

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.rgb[0:self.width, 0:self.height] = self.tiles["dark"]
        for entity in self.creatures + self.items:
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