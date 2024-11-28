class Pawn():

    def __init__(self, id : int):
        self.id = id
        self.is_on_board = False
    
    def add_on_board(self, position : tuple, color: bool):
        if self.is_on_board:
            raise ValueError("Cette pièce est déjà sur l'échiquier !")
        else:
            self.index, self.column = position
            self.color = color
            self.is_on_board = True

    