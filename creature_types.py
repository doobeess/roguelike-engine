from creature import Creature

class Goblin(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, "g", (230, 10, 28), 5, name="Goblin", ai_type="hostile")
    
