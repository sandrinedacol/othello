from board import *
from piece import *

class Game():

    def __init__(self):
        self.in_progress = True
        self.board = Board()
        self.all_pieces = [Piece(i) for i in range(1,65)]
        self.step = 0
        self.player = False # False si noir True si blanc
        self.add_initial_pieces()
        print(self.board.df)

    def add_initial_pieces(self):
        for position in ['d4', 'e4', 'e5', 'd5']:
            self.put_piece_on_board(position)
            self.step += 1
            self.player = not self.player

    def put_piece_on_board(self, position):
        piece = self.all_pieces[self.step]
        piece.add_on_board(position, self.player)
        self.board.add_piece(piece)
        if self.step > 3:
            print(self.board.df)
        
    def play_next_step(self, position):
        self.verify_position(position)
        self.put_piece_on_board(position)
        self.turn_pieces_over()
        self.check_end_game()
        self.step += 1
        self.player = not self.player
        
    def verify_position(self, position):
        pass

    def turn_pieces_over(self):
        pass

    def check_end_game(self):
        pass
        