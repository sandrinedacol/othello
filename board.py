import pandas as pd

class Board():

    def __init__(self):
        # représentation de l'échiquier par un dataframe, ligne = chiffre colonnes = lettre
        self.df = pd.DataFrame(index = list(range(1,9)), columns = list('ABCDEFGH'))

    def add_pawn(self, pawn):
        # choix du marqueur à ajouter dans la case
        if pawn.color:
            marker = 'O'
        else:
            marker = 'X'
        # on change la case situé à la position demandée
        self.df.at[pawn.index, pawn.column] = marker

    def __str__(self):
        # truc à afficher dans le terminal pour montrer l'état de l'échiquier
        return str(self.df)