import pandas as pd

class Board():

    def __init__(self):
        self.df = pd.DataFrame(index = list(range(1,9)), columns = list('ABCDEFGH'))

    def add_pawn(self, pawn):
        if pawn.color:
            marker = 'O'
        else:
            marker = 'X'
        self.df.at[pawn.index, pawn.column] = marker

    def __str__(self):
        return self.df