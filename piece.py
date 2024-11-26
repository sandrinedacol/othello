class Piece():

    def __init__(self, id : int):
        self.id = id
        self.is_on_board = False
    
    def add_on_board(self, position : str, color: bool):
        self.index, self.column = int(position[1]), position[0].upper()
        self.color = color
        self.is_on_board = True

    