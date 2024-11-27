class Pawn():

    def __init__(self, id : int):
        self.id = id
        self.is_on_board = False
    
    def add_on_board(self, position : str, color: bool):
        if self.is_on_board:
            raise ValueError("Cette pièce est déjà sur l'échiquier !")
        else:
            self.index, self.column = int(position[1]), position[0].upper()
            self.color = color
            self.is_on_board = True

    