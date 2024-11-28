from game import *

class Engine():


    def __init__(self):
        print('\nWelcome to the most beautiful Othello game ever!\n')
        self.user_color = self.ask_user_color()
        _ = input('Ready?\n') 
        self.quit = False
        while not self.quit:
            self.play_game()
            self.quit = not self.ask_for_play_again()

    def ask_user_color(self):
        user_color = input('Do you want to be Master of Blacks (B) or Whites (W)? ')
        user_color = user_color.strip().upper()
        if user_color == 'B':
            print("Ok, you're black (symbol: X), you start.\n")
            return False
        elif user_color == 'W':
            print("Ok, you're white (symbol: O), I start.\n")
            return True
        else:
            return self.ask_user_color()


    def play_game(self):
        self.game = Game()
        while self.game.in_progress:
            if self.user_color == self.game.color:
                position_is_found = False
                while not position_is_found:
                    position = input("\nIt's your call: ")
                    if position.strip().lower() in ['q', 'quit', 'exit', 'exit()']:
                        return None
                    else: 
                        position_is_found = self.game.define_user_position(position)
            else:
                self.game.define_computer_position()
            self.game.play_step()
            print(self.game.board)
        self.end_game() 


    def end_game(self):
        black_score, white_score = self.game.compute_score()
        if self.user_color:
            user_score, machine_score = white_score, black_score
        else:
            user_score, machine_score = black_score, white_score
        if user_score > machine_score:
            self.return_congrats()
            print(f"You won {user_score} - {machine_score}.\n")
        elif user_score == machine_score:
            print(f"\nDraw : {user_score} - {machine_score}.\n")
        else:
            self.return_game_over()
            print(f"You lost {user_score} - {machine_score}.\n")


    def ask_for_play_again(self):     
        again = input("\nPlay again? [Y/n]\n")
        return again.strip().lower() in ['y', 'yes', 'oui', 'o', '']


    def return_congrats(self):
        print("\n\n ▗▄▄▖ ▗▄▖ ▗▖  ▗▖ ▗▄▄▖▗▄▄▖  ▗▄▖▗▄▄▄▖▗▄▄▖    \n▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌ █ ▐▌       \n▐▌   ▐▌ ▐▌▐▌ ▝▜▌▐▌▝▜▌▐▛▀▚▖▐▛▀▜▌ █  ▝▀▚▖    \n▝▚▄▄▖▝▚▄▞▘▐▌  ▐▌▝▚▄▞▘▐▌ ▐▌▐▌ ▐▌ █ ▗▄▄▞▘\n\n")

    def return_game_over(self):
        print("\n\n ▗▄▄▖▗▞▀▜▌▄▄▄▄  ▗▞▀▚▖     ▗▄▖ ▄   ▄ ▗▞▀▚▖ ▄▄▄\n▐▌   ▝▚▄▟▌█ █ █ ▐▛▀▀▘    ▐▌ ▐▌█   █ ▐▛▀▀▘█    \n▐▌▝▜▌     █   █ ▝▚▄▄▖    ▐▌ ▐▌ ▀▄▀  ▝▚▄▄▖█    \n▝▚▄▞▘                    ▝▚▄▞▘\n\n")
