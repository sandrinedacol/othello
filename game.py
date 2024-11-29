import numpy as np
import pandas as pd
import itertools

from board import *

class Game():

    def __init__(self):
        self.markers = {True: 'O', False: 'X'}
        self.in_progress = True
        self.board = Board()
        self.step = 0
        self.color = False
        self.position = None, None
        self.add_initial_pawns()
        

    def convert_position_to_tuple(self, position):
        have_good_format = len(position) == 2
        if have_good_format:
            try :
                self.position = int(position[1]), position[0].upper()
            except ValueError:
                try:
                    self.position=int(position[0]), position[1].upper()
                except ValueError:
                    have_good_format = False
        return have_good_format


    def add_initial_pawns(self):
        for position in ['d4', 'e4', 'e5', 'd5']:
            _ = self.convert_position_to_tuple(position)
            self.put_pawn_on_board()
            self.step += 1
            self.color = not self.color
        print(self.board)



    def define_user_position(self, position):
        have_good_format = self.convert_position_to_tuple(position)
        if not have_good_format:
            is_valid = False
        else:                         
            for check_condition in [
            self.check_if_position_exists,
            self.check_if_position_is_free,
            self.check_if_surrounded_pawns
            ]:
                is_valid = check_condition()
                if not is_valid:
                    break
        if not is_valid:
            pass
        return is_valid

    def check_if_position_exists(self):
        index_exists = self.position[0] in self.board.df.index
        column_exists = self.position[1] in self.board.df.columns
        return index_exists and column_exists

    def check_if_position_is_free(self): 
        return self.board.df.at[self.position[0], self.position[1]] == ' '

    def check_if_surrounded_pawns(self):
        self.pawns_to_reverse = []
        opponent_color = self.markers[not self.color]

        def check_one_direction(delta_idx, delta_col):
            columns = self.board.df.columns.tolist()
            indexes = self.board.df.index.tolist()
            pawns_to_reverse = []
            idx, col = self.position
            marker = opponent_color
            while marker == opponent_color:
                i = indexes.index(idx)
                j = columns.index(col)
                try:
                    idx = indexes[i + delta_idx]
                    col = columns[j + delta_col]
                except IndexError:                      # quand le pion est posé sur une case au bord de l'échiquier
                    break
                marker = self.board.df[col][idx]
                if marker == opponent_color:
                    pawns_to_reverse.append((idx, col))
            if marker == self.markers[self.color]:
                self.pawns_to_reverse += pawns_to_reverse

        dir = [0,1,-1]
        for direction in list(itertools.product(dir, dir)):
            try :
                check_one_direction(*direction)
            except SyntaxError:
                pass

        return len(self.pawns_to_reverse) > 0





    def play_step(self):
        self.put_pawn_on_board()
        self.turn_pawns_over()
        self.check_end_game()
        self.step += 1 
        self.color = not self.color
        self.pawns_to_reverse = []

    def put_pawn_on_board(self):
        self.board.df.at[self.position[0], self.position[1]] = self.markers[self.color]

    def turn_pawns_over(self):
        marker = self.markers[self.color]
        for pawn_position in self.pawns_to_reverse:
            self.board.df.at[pawn_position] = marker
        
    def check_end_game(self):
        self.color = not self.color     # on simule l'étape d'après
        empty_squares = [(self.board.df.index[x], self.board.df.columns[y]) for x, y in zip(*np.where(self.board.df.values == ' '))]
        is_valid = False
        for square in empty_squares:
            self.position = square
            is_valid = self.check_if_surrounded_pawns()
            if is_valid:
                self.color = not self.color
                break
        if not is_valid:
            self.in_progress = False
        





    def compute_score(self):
        board_array = self.board.df.to_numpy()
        values, counts = np.unique(board_array, return_counts=True)
        black_score = counts[np.where(values=='X')[0][0]]
        white_score = counts[np.where(values=='O')[0][0]]
        if black_score + white_score < 64 and black_score != white_score:
            empty_squares = counts[np.where(values==' ')[0][0]]
            if black_score > white_score:
                black_score += empty_squares
            else:
                white_score += empty_squares
        return black_score, white_score
        
    


    def define_computer_position(self):
        self.compute_best_position()
        self.check_if_surrounded_pawns()
        
    def compute_best_position(self):
        valid_positions = self.make_inventory_of_valid_positions()
        best_position, best_score = None, 0
        for pos, turned_pawns in valid_positions.items():
            if len(turned_pawns) > best_score:
                best_position, best_score = pos, len(turned_pawns)
        self.position = best_position
        self.pawns_to_reverse = valid_positions[best_position]
        if self.position == None:
            pass
        else:
            _ = input('')
            print(f'I play {self.position[1]}{self.position[0]}')

    def make_inventory_of_valid_positions(self):
        valid_positions = dict()
        for col in self.board.df.columns:
            for idx in self.board.df.index:
                self.position = (idx, col)
                self.pawns_to_reverse = []
                is_valid = self.check_if_position_is_free()
                if is_valid:
                    is_valid = self.check_if_surrounded_pawns()
                if is_valid:
                    valid_positions[(idx, col)] = self.pawns_to_reverse[:]
        return valid_positions