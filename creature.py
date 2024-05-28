from fighter import Fighter

from ai_types import ai_action

class Creature(Fighter):
    def __init__(self, x, y, char, color, hp, name="<Unnamed>", ai_type="neutral"):
        super().__init__(x, y, char, color, hp, name=name)
        self.hp = hp
        self.ai_type = ai_type
        self.attack = 5

    def act(self, engine):
        """
        The creature performs an action based on its hostility and its environment.
        """
        return ai_action(self, engine)

    def take_damage(self, damage):
        self.hp -= damage
