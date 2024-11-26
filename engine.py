from game import *

class Engine():

    def __init__(self):
        print('\nWelcome to the most beautiful Othello game ever!\n\n')
        self.user_color = self.ask_user_color()
        self.game = self.start_new_game()
        while self.game.in_progress:
            self.game.play_next_step()
        self.end_game()

    def ask_user_color(self):
        user_color = input('Do you want to be the master of Blacks (B) or Whites (W)?')
        user_color = user_color.strip().upper()
        if user_color == 'B':
            print("Ok, you're black, you start.\n")
            return True
        elif user_color == 'W':
            print("Ok, you're white, I start'.\n")
            return False
        else:
            return self.ask_user_color()
        
    def start_new_game(self):
        _ = input('Ready?\n')
        return Game()

    def end_game(self):
        pass
