import tcod.event

import color

from actions import (
    Action, 
    WaitAction, 
    EscapeAction, 
    BumpAction, 
    PickUpAction, 
    DropAction, 
    ViewInventoryAction
)

CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: -1,
    tcod.event.KeySym.DOWN: 1,
}

SELECT_KEYS = {
    tcod.event.KeySym.RETURN
}

ESCAPE_KEYS = {
    tcod.event.KeySym.ESCAPE
}


class ScreenHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown):
        raise NotImplementedError
    
    def on_render(self, console: tcod.console.Console, engine):
        raise NotImplementedError


class MainGameScreenHandler(ScreenHandler):
    def handle_event(self, event, engine):

        action = self.dispatch(event)

        if action is None:
            return 0
        
        is_timeless = action.perform(engine, engine.player, engine.message_log)
        if is_timeless:
            return 1
        
        engine.update_fov()
        return 2
    
    def ev_keydown(self, event: tcod.event.KeyDown):

        action = None

        key = event.sym

        if key == tcod.event.KeySym.UP:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT:
            action = BumpAction(dx=1, dy=0)
        elif key == tcod.event.KeySym.N1:
            action = BumpAction(dx=-1, dy=1)
        elif key == tcod.event.KeySym.N3:
            action = BumpAction(dx=1, dy=1)
        elif key == tcod.event.KeySym.N7:
            action = BumpAction(dx=-1, dy=-1)
        elif key == tcod.event.KeySym.N9:
            action = BumpAction(dx=1, dy=-1)
        
        elif key == tcod.event.KeySym.COMMA:
            action = PickUpAction()

        elif key == tcod.event.KeySym.PERIOD:
            action = WaitAction()

        elif key == tcod.event.KeySym.i:
            action = ViewInventoryAction()

        elif key == tcod.event.KeySym.d:
            action = DropAction()

        # No valid key was pressed
        return action

    def on_render(self, console, engine):
        engine.game_map.render(console)

        console.print(engine.player.x, engine.player.y, engine.player.char, engine.player.color)
        console.print(engine.map_width+1, 3, f"HP: {engine.player.hp}", (255,0,0))

        engine.message_log.render(0, engine.map_height, console)


class MultipleChoiceScreenHandler(ScreenHandler):
    '''
    Ordering systems:
    1: letters (a, b, c, ...)
    2: numbers (1, 2, 3, ...) # TODO: Add multiple systems
    '''

    def __init__(self, choices, ordering_system=1, title='Select an option'):
        self.choices = choices
        self.ordering_system = ordering_system
        self.pointer = 1
        self.title = title

    def handle_event(self, event, engine):
        scroll_distance = self.dispatch(event)

        if scroll_distance is None:
            return 0
        
        if scroll_distance == 'quit':
            del engine.screen_handler_list[-1]
            engine.active_screen_handler = engine.screen_handler_list[-1]
            return 1
        
        if scroll_distance != 0:
            self.scroll_pointer(scroll_distance)
        else:
            self.select(engine)
            engine.delete_current_screen_handler()
            return 2

        return 1
    
    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym

        if key in CURSOR_Y_KEYS:
            return CURSOR_Y_KEYS[key]
        
        elif key in SELECT_KEYS:
            return 0
        
        elif key in ESCAPE_KEYS:
            return 'quit'

    def on_render(self, console: tcod.console.Console, engine):
        
        x = 5
        y = 5

        console.draw_frame(
            x, y, 
            
            width=max(
                max([len(choice) for choice in self.choices]), # As wide as the longest choice
                len(self.title) # Or as long as the title
            )
            +4 # Make room for the alt choice method rendering
            +2, # Fit the frame
            
            height=len(self.choices)
            +2 # Fit all the choices. TODO: Add scrolling functionality.
            +2, # Add room for title. 
            fg=color.WHITE,
            bg=color.BLACK,
        )
        console.print(x+1, y+1, self.title)
        for i, choice in enumerate(self.choices):
            fg = color.WHITE
            bg = color.BLACK
            if i==self.pointer-1:
                fg = color.BLACK
                bg = color.WHITE
            console.print(x+1, y+i+3, str(i+1) + " - " + choice, fg, bg)


    def scroll_pointer(self, amount):
        self.pointer += amount
        if self.pointer < 1:
            self.pointer = len(self.choices)-self.pointer
        elif self.pointer > len(self.choices):
            self.pointer -= len(self.choices)

    def get_pointed(self):
        return self.choices[self.pointer-1]
    
    def select(self, engine):
        raise NotImplementedError


class ViewInventoryScreenHandler(MultipleChoiceScreenHandler):
    def __init__(self, engine):
        super().__init__(
            choices=[item.name for item in engine.player.inventory],
            title='Inventory'
        )

    def select(self, engine):
        raise NotImplementedError  # TODO: Implement Individual item screens
        

class DropScreenHandler(MultipleChoiceScreenHandler):
    def __init__(self, engine):
        super().__init__(
            choices=[item.name for item in engine.player.inventory],
            title='Select an item to drop'
        )
    
    def select(self, engine):
        for item in engine.player.inventory:
            if item.name == self.choices[self.pointer-1]:
                engine.player.drop(item, engine.game_map)
                engine.message_log.log("You drop the " + item.name + ".")
                return
        return