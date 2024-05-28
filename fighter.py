from entity import Entity

class Fighter(Entity):
    def __init__(self, x, y, char, color, hp, name="<Unnamed>", attack=5, defense=2):
        super().__init__(x,y,char,color,name)
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def is_dead(self):
        if self.hp <= 0:
            return True
        return False
