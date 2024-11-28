import pandas as pd

class Board():
    def __init__(self):
        self.df = pd.DataFrame(index = list(range(1,9)), columns = list('ABCDEFGH'))

    def add_pawn(self, position, color):
        if color:
            marker = 'O'
        else:
            marker = 'X'
        self.df.at[position[0], position[1]] = marker

    def __str__(self):
        return str(self.df)