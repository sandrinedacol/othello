from board import *
from pawn import *

class Game():

    def __init__(self):
        self.in_progress = True                             # le bool qui change en False quand les conditions d'arrêt de jeu sont réunies
        self.board = Board()                                # instance de Bord qui représente l'échiquier
        self.all_pawns = [Pawn(i) for i in range(1,65)]     # liste de tous les pions, chaque pion est une instance de Pawn
        self.step = 0                                       # entier incrémental, qui suit à quelle étape on est
        self.player = False # False si noir True si blanc   # bool qui désigne qui doit jouer à l'étape (les noirs ou les blancs)
        self.add_initial_pawns()                            # initialisation des 4 1er pions
        print(self.board)

    def add_initial_pawns(self):
        # pour chaque position, on joue une étape fictive :
        for position in ['d4', 'e4', 'e5', 'd5']:       # la liste est construite de manière à ce que les pions soient bien disposés : noir blanc noir blanc
            self.put_pawn_on_board(position)            # on place le pion sur l'échiquier
            self.step += 1                              # on passe à l'étape d'après
            self.player = not self.player               # on change le joueur qui doit jouer l'étape d'après

    def put_pawn_on_board(self, position):
        # on choisit de quel pion on parle, via son index dans la liste de tous les pions
        pawn = self.all_pawns[self.step]
        # on change les attributs de ce pion
        pawn.add_on_board(position, self.player)
        # on ajoute le pion sur l'échiquier
        self.board.add_pawn(pawn)
        # on montre le résulat du pion posé à l'utilisateur
        if self.step > 3:
            print(self.board)
        
    def play_next_step(self, position):
        # est-ce que le joueur a le droit de poser le pion à cette position ? 
        is_consistent = self.verify_position(position)
        if is_consistent:
            # si oui, on ajoute le pion sur l'échiquier
            self.put_pawn_on_board(position)
            # puis on retourne les pions à retourner
            self.turn_pawns_over(position)
            # on vérifie si les conditions d'arrêt de la partie sont atteintes
            self.check_end_game()
            # on passe à l'étape d'après et on change le joueur qui doit jouer l'étape d'après
            self.step += 1
            self.player = not self.player
        return is_consistent
        
    def verify_position(self, position):
        is_consistent = True
        for check_condition in [self.verify_and_convert_position_to_tuple,self.verify_if_position_exists, self.verify_if_position_is_empty]:
            is_consistent = check_condition(position)
            if not is_consistent:
                break
        return is_consistent
    
    def verify_and_convert_position_to_tuple(self,position):
        if not len(position)==2:
            output=False
        else:
            try :
                col=position[0].upper()
                ind=int(position[1])
                self.position=ind,col
                output=True
            except:
                output=False
        return output

    def verify_if_position_exists(self,position):
        df_local=self.board.df.copy()
        output = self.position[0] in df_local.index and self.position[1] in df_local.columns
        return output


    def verify_if_position_is_empty(self, position):
        if pd.isna(self.board.df.at[self.position[0], self.position[1]]):
            output = True
        else:
            output = False
        return output

    def turn_pawns_over(self, position):
        pass

    def check_end_game(self):
        pass

        