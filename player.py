from fighter import Fighter

class Player(Fighter):
    def __init__(self, x, y, hp, inventory=[]):
        super().__init__(x,y,"@",(255,255,255),hp)
        self.attack = 2
        self.defence = 0
        self.inventory = inventory

    def pick_up(self, item, game_map):
        self.inventory.append(item)
        game_map.items.remove(item)

    def drop(self, item, game_map):
        self.inventory.remove(item)
        item.x = self.x
        item.y = self.y
        game_map.items.append(item)
