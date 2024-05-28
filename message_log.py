from typing import Tuple

class Message:
    def __init__(self, text, color):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, maxlines):
        self.maxlines = maxlines
        self.contents = []
        self.displayed_contents = []
    def log(self, text: str, color: Tuple[int, int, int] = (255,255,255)):
        message = Message(text, color)
        self.contents.append(message)
        self.displayed_contents.append(message)
        if len(self.displayed_contents) > self.maxlines:
            del self.displayed_contents[0]
    def render(self, start_x, start_y, root_console):
        current_x = start_x
        current_y = start_y
        for message in self.displayed_contents:
            root_console.print(current_x, current_y, message.text, fg=message.color)
            current_y += 1