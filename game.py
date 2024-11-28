import numpy as np

from board import *
from pawn import *

class Game():

    def __init__(self):
        self.in_progress = True                             # le bool qui change en False quand les conditions d'arrêt de jeu sont réunies
        self.board = Board()                                # instance de Bord qui représente l'échiquier
        self.all_pawns = [Pawn(i) for i in range(1,65)]     # liste de tous les pions, chaque pion est une instance de Pawn
        self.step = 0                                       # entier incrémental, qui suit à quelle étape on est
        self.player = False                                 # bool qui désigne qui doit jouer à l'étape (noir = False ou blanc = True)
        self.add_initial_pawns()                            # initialisation des 4 1er pions
        print(self.board)

    def add_initial_pawns(self):                            # pour chaque position, on joue une étape fictive :
        for position in ['d4', 'e4', 'e5', 'd5']:           # la liste est construite de manière à ce que les pions soient bien disposés : noir blanc noir blanc
            _ = self.convert_position_to_tuple(position)    # assigne la bonne valeur à self.position
            self.put_pawn_on_board()                        # on place le pion sur l'échiquier
            self.step += 1                                  # on passe à l'étape d'après
            self.player = not self.player                   # on change le joueur qui doit jouer l'étape d'après

    def put_pawn_on_board(self):
        pawn = self.all_pawns[self.step]                    # on choisit de quel pion on parle, via son index dans la liste de tous les pions
        pawn.add_on_board(self.position, self.player)       # on change les attributs de ce pion
        self.board.add_pawn(pawn)                           # on ajoute le pion sur l'échiquier
        if self.step > 3:                                   # on montre le résulat du pion posé à l'utilisateur
            print(self.board)
        
    def play_next_step(self, position):
        is_consistent = self.convert_position_to_tuple(position)
        if is_consistent:                                   
            is_consistent = self.check_position()           # est-ce que le joueur a le droit de poser le pion à cette position ? 
        if is_consistent:
            self.put_pawn_on_board()                        # si oui, on ajoute le pion sur l'échiquier
            self.turn_pawns_over()                          # puis on retourne les pions à retourner
            self.check_end_game()                           # on vérifie si les conditions d'arrêt de la partie sont atteintes
            self.step += 1                                  # on passe à l'étape d'après 
            self.player = not self.player                   # et on change le joueur qui doit jouer l'étape d'après
        return is_consistent
        
    def check_position(self):
        for check_condition in [
            self.check_if_position_exists,
            self.check_if_position_is_empty
            ]:
            is_consistent = check_condition()
            if not is_consistent:
                break
        return is_consistent
    
    def convert_position_to_tuple(self, position):
        is_consistent = len(position) == 2
        if is_consistent:
            try :
                self.position = int(position[1]), position[0].upper()
            except ValueError:
                try:
                    self.position=int(position[0]), position[1].upper()
                except ValueError:
                    is_consistent = False
        return is_consistent

    def check_if_position_exists(self):
        index_exists = self.position[0] in self.board.df.index
        column_exists = self.position[1] in self.board.df.columns
        return index_exists and column_exists

    def check_if_position_is_empty(self):
        value = self.board.df.at[self.position[0], self.position[1]]
        return value == ' '

    def turn_pawns_over(self):
        pass

    def check_end_game(self):
        # modifie game.in_progress si les conditions de fin de partie sont réunies
        empty_squares = [(self.board.df.index[x], self.board.df.columns[y]) for x, y in zip(*np.where(self.board.df.values == ' '))]
        is_consistent = False
        for square in empty_squares:
            self.position = square
            is_consistent = self.check_position()   # à remplacer par les 2 méthodes de Romain : 'adjcent' et 'encadre'
            if is_consistent:
                break
        if not is_consistent:
            self.in_progress = False

    def compute_score(self):
        # return black_score, white_score
        board_array = self.board.df.to_numpy()
        values, counts = np.unique(board_array, return_counts=True)
        black_score = counts[np.where(values=='X')[0][0]]
        white_score = counts[np.where(values=='O')[0][0]]
        if black_score != white_score:
            empty_squares = counts[np.where(values==' ')[0][0]]
            if black_score > white_score:
                black_score += empty_squares
            else:
                white_score += empty_squares
        return black_score, white_score
        