from board import *
from pawn import *

class Game():

    def __init__(self):
        self.in_progress = True
        self.board = Board()
        self.all_pawns = [Pawn(i) for i in range(1,65)]
        self.step = 0
        self.player = False # False si noir True si blanc
        self.add_initial_pawns()
        print(self.board.df)

    def add_initial_pawns(self):
        for position in ['d4', 'e4', 'e5', 'd5']:
            self.put_pawn_on_board(position)
            self.step += 1
            self.player = not self.player

    def put_pawn_on_board(self, position):
        pawn = self.all_pawns[self.step]
        pawn.add_on_board(position, self.player)
        self.board.add_pawn(pawn)
        if self.step > 3:
            print(self.board.df)
        
    def play_next_step(self, position):
        self.verify_position(position)
        self.put_pawn_on_board(position)
        self.turn_pawns_over()
        self.check_end_game()
        self.step += 1
        self.player = not self.player
        
    def verify_position(self, position):
        pass

    def turn_pawns_over(self):
        pass

    def check_end_game(self):
        pass
        