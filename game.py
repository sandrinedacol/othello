import numpy as np
import pandas as pd

class Game():

    def __init__(self):
        self.markers = {True: 'O', False: 'X'}
        self.in_progress = True
        self.board = pd.DataFrame(index = list(range(1,9)), columns = list('ABCDEFGH'))
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
            is_consistent = False
        else:                         
            for check_condition in [
            self.check_if_position_exists,
            self.check_if_position_is_free,
            self.check_if_surrounded_pawns
            ]:
                is_consistent = check_condition()
                if not is_consistent:
                    break
        return is_consistent

    def check_if_position_exists(self):
        index_exists = self.position[0] in self.board.index
        column_exists = self.position[1] in self.board.columns
        return index_exists and column_exists

    def check_if_position_is_free(self):
        return pd.isna(self.board.at[self.position[0], self.position[1]])

    def check_if_surrounded_pawns(self):
        opponent_color = self.markers[not self.color]
        self.pawns_to_reverse = []

        def check_one_direction(delta_idx, delta_col):
            columns = self.board.columns.tolist()
            indexes = self.board.index.tolist()
            pawns_to_reverse = []
            idx, col = self.position
            marker = opponent_color
            while marker == opponent_color:
                i = indexes.index(idx)
                idx = indexes[i + delta_idx]
                j = columns.index(col)
                col = columns[j + delta_col]
                marker = self.board[col][idx]
                if marker == opponent_color:
                    pawns_to_reverse.append((idx, col))
            if marker == self.markers[self.color]:
                self.pawns_to_reverse += pawns_to_reverse

        for direction in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
            check_one_direction(*direction)

        return len(self.pawns_to_reverse) > 0





    def play_step(self):
        self.put_pawn_on_board()
        self.turn_pawns_over()
        self.check_end_game()
        self.step += 1 
        self.color = not self.color

    def put_pawn_on_board(self):
        self.board.at[self.position[0], self.position[1]] = self.markers[self.color]

    def turn_pawns_over(self):
        marker = self.markers[self.color]
        for pawn_position in self.pawns_to_reverse:
            self.board.at[pawn_position] = marker
        
    def check_end_game(self):
        empty_squares = [(self.board.index[x], self.board.columns[y]) for x, y in zip(*np.where(pd.isna(self.board.values)))]
        is_consistent = False
        for square in empty_squares:
            self.position = square
            is_consistent = lambda x : True   # à remplacer par les 2 méthodes de Romain : 'adjcent' et 'encadre'
            if is_consistent:
                break
        if not is_consistent:
            self.in_progress = False





    def compute_score(self):
        board_array = self.board.to_numpy()
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
        
    


    def define_computer_position(self):
        self.compute_best_position()
        self.check_if_surrounded_pawns()
        
    def compute_best_position(self):
        consistent_positions = [] # à faire : pour toutes les positions, celles qui passent les conditions sont retenues
        best_position, best_score = None, 0
        for pos in consistent_positions:
            fictive_board = self.board.copy()
            self.position = pos
            n_turned_pawns = 0 # à remplacer par le calcul des pions qui seraient retournés (effectué sur fictive_board)
            if n_turned_pawns > best_score:
                best_position, best_score = pos, n_turned_pawns
        # self.position = best_position
        _ = self.convert_position_to_tuple(input("\n[dev mode] position du PC: "))        # juste le temps d'écrire le reste
        print(f'\nI play {self.position[1]}{self.position[0]}')