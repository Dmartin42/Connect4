import pyglet
from typing import List,Tuple

from pyglet.libs.win32.constants import NTM_BOLD
from player import piece as piece

class Board():
    MARGIN = 10
    GAME_COLORS: dict = {"white fade": (218, 219, 215),
                    "purple fade": (84,74,83),
                    "light blue" : (146,148,214), 
                    "light green" : (154,214,146),
                    "yellow player" : (184,186,56),
                    "red player": (240,20,20)} 
    def __init__(self, numRows: int, numCols: int, screen_size = [700,700]):
        self.rows = numRows
        self.cols = numCols
        self.screen_size = screen_size
        #Piece that was just placed
        #self.activePiece: Tuple[int,int,int,Tuple[int,int,int]] = (0,0,0,(0,0,0))
        self.blankPiece: piece = piece(y=0,row=0,col=0,width=0,color='grey',x=0)
        self.activePiece: piece = self.blankPiece
        self.pieces: List['piece'] = []
        self.turn = self.get_first_player()
        self.is_winner = False
        
        print(f"The {self.turn} player goes first!")

    def get_first_player(self) -> str:
        import random
        return "red" if random.choice(["red","yellow"]) == 'red' else "yellow"

    def get_screen_size(self):
        return self.screen_size

    def set_screen_size(self,screen_size: tuple):
        self.screen_size[0] = screen_size[0]
        self.screen_size[1] = screen_size[1]

    def get_cell_width(self):
        return (self.get_screen_size()[0] - (Board.MARGIN*2))/self.cols

    def get_cell_height(self):
        return (self.get_screen_size()[1] - (Board.MARGIN*2))/self.rows
    
    def get_board(self) -> List[List[str]]:
        the_board: List[List[str]] = [[" "] * self.cols for _ in range(self.rows)]
        for piece in self.pieces:
            row = piece.row
            col = piece.col
            if piece.color == Board.GAME_COLORS['yellow player']:
                the_board[row][col] = 'y'
            else:
                the_board[row][col] = 'r'
        return the_board

    def draw(self):
        SCREEN_SIZE = self.get_screen_size()
        MARGIN = Board.MARGIN
        WIDTH = self.get_cell_width()
        HEIGHT = self.get_cell_height()
        for i in range(self.cols+1):
            x = MARGIN + (i * WIDTH)
            y = MARGIN
            x2 = MARGIN + (i * WIDTH)
            y2 = SCREEN_SIZE[1] - (MARGIN)
            #Vertical Lines
            pyglet.shapes.Line(x,y,x2,y2,width=4,color=Board.GAME_COLORS["light blue"]).draw()
        for j in range(self.rows+1):
            x = MARGIN
            y = MARGIN + (j * HEIGHT)
            x2 = SCREEN_SIZE[0] - (MARGIN)
            y2 = MARGIN + (j * HEIGHT)
            #Horizontal Lines
            pyglet.shapes.Line(x,y,x2,y2,width=4,color=Board.GAME_COLORS["light green"]).draw()
    def draw_piece(self, piece):
        piece.draw(x=piece.x, y=piece.y)

    def draw_active_piece(self, piece: piece):
            y = piece.y
            col = piece.col
            color = piece.color
            MARGIN = Board.MARGIN
            WIDTH = self.get_cell_width()
            RADIUS = (WIDTH/2) - 4
            x = MARGIN+(col*WIDTH)+WIDTH/2
            pyglet.shapes.Circle(x,y,RADIUS,color=color).draw()
    
    def apply_gravity(self, piece: "piece"):
        if piece is None:
            return

        gravity = 9.81*3
        
        MARGIN = Board.MARGIN
        HEIGHT = self.get_cell_height()
        #convert piece's y-coord to a row
        row = int((piece.y - MARGIN) / HEIGHT) 
        # if the row of piece is the same as the converted y-coord row 
        if row == piece.row:
            piece.y-=gravity
            piece.y = MARGIN+(row*HEIGHT)+HEIGHT/2
            self.pieces.append(piece)
            self.activePiece = self.blankPiece
            self.turn = 'red' if self.turn == 'yellow' else 'yellow'
            if self.get_winner_positions(piece) is not None:
                self.is_winner = True
            return

        piece.y-=gravity
        self.draw_piece(piece=piece)

    def draw_player_turn_icon(self):
            row = self.rows - 1
            col = self.cols + 1
            color = Board.GAME_COLORS[f"{self.turn} player"]
            MARGIN = Board.MARGIN
            WIDTH = self.get_cell_width()
            HEIGHT = self.get_cell_height()
            RADIUS = WIDTH/2
            x = MARGIN+(col*WIDTH)+WIDTH/2
            y = MARGIN+(row*HEIGHT)+HEIGHT/2
            pyglet.shapes.Circle(x,y,RADIUS,color=color).draw()
    
    def draw_winner(self, positions: List[Tuple[int,int]]):
        if positions == None:
            return
        startCoords = positions[0]
        endCoords = positions[1]
        MARGIN = Board.MARGIN
        WIDTH = self.get_cell_width()
        HEIGHT = self.get_cell_height()
        x = MARGIN+(startCoords[1]*WIDTH)+WIDTH/2
        y = MARGIN+(startCoords[0]*HEIGHT)+HEIGHT/2
        x2 = MARGIN+(endCoords[1]*WIDTH)+WIDTH/2
        y2 = MARGIN+(endCoords[0]*HEIGHT)+HEIGHT/2
        pyglet.shapes.Line(x,y,x2,y2,width=8).draw()
    
    def verify(self, board: List[List[str]],row: int,col: int,Rstep: int = 1,Cstep: int = 0, letter: str = "r"):
            """Iterates through rows and cols from a pivot point in matrix according to step; checks
            each iteration if it matches the  letter"""
            n: int = 0
            #Number of matches to win (4)
            k: int = 4
            while n < k:
                try:
                    char = board[row][col]
                    if col < 0 or row < 0:
                        raise IndexError
                except IndexError:
                    break
                if char == letter:
                    if n == k - 1:
                        return (row,col)
                else:
                    break
                n += 1
                col += Cstep
                row += Rstep
            return None
    
    def check_diagonal_left(self,board: List[List[str]], letter: str,i: int, j: int):
        return self.verify(board=board, row=i, col=j, Rstep=1, Cstep=-1, letter=letter)

    def check_diagonal_right(self,board: List[List[str]], letter: str,i: int, j: int):
        return self.verify(board=board, row=i, col=j, Rstep=1, Cstep=1, letter=letter)

    def check_across(self,board: List[List[str]], letter: str,i: int, j: int):
        return self.verify(
            board=board, row=i, col=j, Rstep=0, Cstep=1, letter=letter
        ) or self.verify(
            board=board, row=i, col=j, Rstep=0, Cstep=-1, letter=letter
        )
    
    def check_down(self,board: List[List[str]], letter: str,i: int, j: int):
        return self.verify(
            board=board, row=i, col=j, Rstep=-1, Cstep=0, letter=letter
        ) or self.verify(
            board=board, row=i, col=j, Rstep=1, Cstep=0, letter=letter
        )

    def get_winner_positions(self, piece):
        player = 'y' if piece.get_color() == 'y' else 'r'
        board = self.get_board()
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.check_across(board=board, letter=player, j=col, i=row)
                if not cell:
                     cell = self.check_down(board=board, letter=player, j=col, i=row)
                     if not cell:
                          cell = self.check_diagonal_left(board=board, letter=player, j=col, i=row)
                          if not cell:
                               cell = self.check_diagonal_right(board=board, letter=player, j=col, i=row)
                if not cell:
                    continue
                else:
                    return [(row,col),cell]
        return None

#-------------------------------------------------#-------------------------------------------------#
#-------------------------------------------------#-------------------------------------------------#
#-------------------------------------------------#-------------------------------------------------#
#-------------------------------------------------#-------------------------------------------------#
class MyWindow(pyglet.window.Window):
    from pyglet.window import key
    from pyglet.window import mouse
    def __init__(self,*args,**kwargs):
        super(MyWindow,self).__init__(*args,**kwargs)
        self.set_minimum_size(700,700)
        #background color
        backgroundColor = [84,74,83,255]
        backgroundColor = [i /255 for i in backgroundColor]
        pyglet.gl.glClearColor(*backgroundColor)
        self.board = Board(numRows=6,numCols=7) #6,7
        self.label = pyglet.text.Label(text="Shift + Esc to exit | c to clear", x = 700, y=15)
        self.board.set_screen_size(self.get_viewport_size())
        self.highlightedCell: Tuple[int,int] = (0,0)
        self.board.activePiece = self.board.blankPiece

    def on_window_close(self):
        try:
            pyglet.app.exit()
            exit(0)
        except:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol == self.key.ESCAPE:
            if modifiers & self.key.MOD_SHIFT:
                try:
                    pyglet.app.exit()
                    exit(0)
                except:
                    pass
            else:
                fullscreen = self._fullscreen
                if fullscreen:
                    self.set_fullscreen(fullscreen=False)
                else:
                    self.set_fullscreen(fullscreen=True)
        if symbol == self.key.C:
            self.board.pieces.clear()
            self.board.activePiece = self.board.blankPiece
            self.board.is_winner = False

    def on_mouse_motion(self, x, y, dx, dy):
        cell = self._get_cell(x,y)
        #Checks if user is hovering above a cell on board and if that cell does not contain a piece
        if cell is not None:
            self.highlightedCell = cell
        elif cell is None:
            self.highlightedCell = ()

    def on_mouse_press(self, x, y, button, modifiers):
        from player import piece as piece 
        if (self.board.activePiece != self.board.blankPiece) or self.board.is_winner:
            return
        if button == self.mouse.LEFT:
            cell = self._get_cell(x,y)
            if cell is not None:                
                clickedCol = cell[1]
                endRow = 0
                if self.board.pieces:
                    smallestRow = 0
                    for each_piece in self.board.pieces:
                        if each_piece.row == self.board.rows-1 and each_piece.col == clickedCol:
                            return
                        if each_piece.col == clickedCol and  each_piece.row >= smallestRow:
                            #the bottom row + 1
                            smallestRow = each_piece.row + 1
                    endRow = smallestRow
                cellWidth = self.board.get_cell_width()
                cellHeight = self.board.get_cell_height()
                pieceWidth = self.board.get_cell_width()/2 - 4
                startRow = Board.MARGIN+( ( self.board.rows) * cellHeight) + cellHeight/2
                color=f"{self.board.turn}"
                x = Board.MARGIN+(clickedCol*cellWidth)+cellWidth/2
                #Instantiaion of piece object
                self.board.activePiece = piece(x=x, y=startRow, row=endRow, col=clickedCol, width=pieceWidth, color=color)
     
    def _get_cell(self, x: int, y: int):
        boardWidth = self.board.get_cell_width() * self.board.cols
        boardHeight = self.board.get_cell_height() * self.board.rows
        MARGIN = Board.MARGIN
        #Checks if x and y within entire board
        if (MARGIN < x < boardWidth + MARGIN) and (MARGIN < y < boardHeight + MARGIN):
            cellWidth = self.board.get_cell_width()
            cellHeight = self.board.get_cell_height()
            #Find which cell x and y are at
            row = int((y - MARGIN) / cellHeight)
            col = int((x - MARGIN) / cellWidth)
            return (row,col)
        return None

    def on_draw(self):
        self.clear()
        self.board.draw()
        self.label.draw()
        self.main()
        
    def main(self):
        self.board.draw_player_turn_icon()
        if self.highlightedCell:
            self.highlight_cell(self.highlightedCell)
        for piece in self.board.pieces:
            self.board.draw_piece(piece)
            #check if winner
            self.board.draw_winner(self.board.get_winner_positions(piece))
        if self.board.activePiece != self.board.blankPiece:
            self.board.apply_gravity(self.board.activePiece)

    def highlight_cell(self, cell: Tuple[int,int]) -> None:
        row = cell[0]
        col = cell[1]
        MARGIN = Board.MARGIN
        cellWidth = self.board.get_cell_width()
        cellHeight = self.board.get_cell_height()
        x = MARGIN+(col*cellWidth)
        y = MARGIN+(row*cellHeight)
        rect = pyglet.shapes.Rectangle(x=x,y=y,width=cellWidth,height=cellHeight,color=Board.GAME_COLORS["white fade"])
        rect.opacity = 50
        rect.draw()

    
    
                        


    def update(self, dt):
        pass

frameRate = 30

if __name__ == "__main__":
    window = MyWindow(700,700,"connect 4",1/frameRate)
    window.set_fullscreen(fullscreen=True)
    pyglet.clock.schedule_interval(window.update,1/frameRate)
    pyglet.app.run()