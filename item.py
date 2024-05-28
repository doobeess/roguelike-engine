from entity import Entity

class Item(Entity):
    def apply(self, engine):
        # Apply the item for usage.
        raise NotImplementedError