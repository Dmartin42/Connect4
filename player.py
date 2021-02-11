import pyglet
from typing import Tuple
class piece():
    GRAVITY = 9.81*3
    def __init__(self, y: float, row: int, col: int, width: int, color: str, x: float = 0.0):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.width = width
        if color[0].lower() == 'y':
            #yellow
            self.color = (184,186,56)
        else:
            #red
            self.color = (240,20,20)

    def set_row(self, row: int):
        self.row = row
    
    def set_col(self, col: int):
        self.col = col

    def get_row(self) -> int:
        return self.row
    
    def get_col(self) -> int:
        return self.col
    
    def get_color(self):
        return 'y' if self.color == (184,186,56) else 'r'
    
    def draw(self, x: int, y: int) -> None:
            pyglet.shapes.Circle(x=x, y=y, radius=self.width, color=self.color).draw()
    