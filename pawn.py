class Pawn():

    def __init__(self, id : int):
        self.id = id
        self.is_on_board = False
    
    def add_on_board(self, position : str, color: bool):
        # vérification qu'on prend bien un pion qui n'est pas encore posé sur l'échiquier
        if self.is_on_board:
            raise ValueError("Cette pièce est déjà sur l'échiquier !")
        else:
            self.index, self.column = int(position[1]), position[0].upper()     # on passe d'un string à des coordonnées x (int) et y (lettre)
            self.color = color      # la couleur du pion (sur quelle face il est posé
            self.is_on_board = True     # on passe le bool à True pour dire qu'il est bien posé sur l'échiquier

    