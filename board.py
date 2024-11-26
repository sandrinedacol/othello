import pandas as pd

class Board():

    def __init__(self):
        self.df = pd.DataFrame(index = list(range(1,9)), columns = list('ABCDEFGH'))

    def add_piece(self, piece):
        if piece.color:
            marker = 'O'
        else:
            marker = 'X'
        self.df.at[piece.index, piece.column] = marker

    def __str__(self):
        return self.df