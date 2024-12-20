from game import *

class Engine():

    def __init__(self):

        self.print_othello()
        self.user_name=str(input("Enter your Unicorn or Dragon name here : "))
        print(f'\nHi {self.user_name},\nWelcome to the most BEAUTIFUL & FUNNY & INTELLIGENT game ever!')
        self.user_color = self.ask_user_color()   # user_color est la couleur choisie par l'utilisateur : noir ou blanc
        _ = input('Ready? (Press a key)\n') 
        self.quit = False
        while not self.quit:
            self.play_game()
            self.quit = not self.ask_for_play_again()

    def play_game(self):
        self.game = Game()
        while self.game.in_progress:                    # tant que les conditions sont réunies, le jeu continue
            if self.user_color == self.game.color:
                position_is_found = False
                while not position_is_found:
                    position = input("\nYour call: ")
                    if position.strip().lower() in ['q', 'quit', 'exit', 'exit()']:
                        return None
                    else: 
                        position_is_found = self.game.define_user_position(position)
            else:
                self.game.define_computer_position()
            self.game.play_step()
            print(self.game.board)
        self.end_game()                                                             # une fois que les conditions d'arrêt de jeu changent le bool 'game.in_progress', on finit le jeu
        
    def ask_for_play_again(self):     
        again = input("\nPlay again? [Y/n]\n")
        return again.strip().lower() in ['y', 'yes', 'oui', 'o', '']

    def ask_user_color(self):
        user_color = input('Do you want to be Yellow as the Sun (Y) or Blue as the Sky (B)? ')
        user_color = user_color.strip().upper()
        if user_color == 'B':
            print("\nOk, you're blue, you start.")
            return False             # blue = false
        elif user_color == 'Y':
            print("\nOk, you're yellow, I start.")
            return True             # yellow = true
        else:
            return self.ask_user_color()

    def end_game(self):
        black_score, white_score = self.game.compute_score()
        if self.user_color:
            user_score, machine_score = white_score, black_score
        else:
            user_score, machine_score = black_score, white_score
        if user_score > machine_score:
            self.print_congrats()
            print(f"You won {user_score} - {machine_score} and destroy all our dreams.\nAre you happy with that, {self.user_name}?\n")
        elif user_score == machine_score:
            print(f"\nDraw : {user_score} - {machine_score}.\n")
        else:
            self.print_game_over()
            print(f"You lost {user_score} - {machine_score}.\nSorry {self.user_name}, you can't beat MAGIC !\n")

    def print_congrats(self):
        print("\n\n ▗▄▄▖ ▗▄▖ ▗▖  ▗▖ ▗▄▄▖▗▄▄▖  ▗▄▖▗▄▄▄▖▗▄▄▖    \n▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌ █ ▐▌       \n▐▌   ▐▌ ▐▌▐▌ ▝▜▌▐▌▝▜▌▐▛▀▚▖▐▛▀▜▌ █  ▝▀▚▖    \n▝▚▄▄▖▝▚▄▞▘▐▌  ▐▌▝▚▄▞▘▐▌ ▐▌▐▌ ▐▌ █ ▗▄▄▞▘\n\n")

    def print_game_over(self):
        print("\n\n ▗▄▄▖▗▞▀▜▌▄▄▄▄  ▗▞▀▚▖     ▗▄▖ ▄   ▄ ▗▞▀▚▖ ▄▄▄\n▐▌   ▝▚▄▟▌█ █ █ ▐▛▀▀▘    ▐▌ ▐▌█   █ ▐▛▀▀▘█    \n▐▌▝▜▌     █   █ ▝▚▄▄▖    ▐▌ ▐▌ ▀▄▀  ▝▚▄▄▖█    \n▝▚▄▞▘                    ▝▚▄▞▘\n\n")

    def print_welcome(self):
        string = "\n\n░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓██████████████▓▒░░▒▓████████▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        \n░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        \n░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░   \n░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        \n░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        \n ░▒▓█████████████▓▒░░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ \n\n"
        print(string)

    def print_othello(self):
        string = "\n\n\n\n\n\n\n\n░▒▓██████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓██████▓▒░  \n░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ \n ░▒▓██████▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░\n"
        string += '          designed by      Romain the Fluorescent Dragon,\n                              Sandrine the Sparkling Panda,\n                                  & Dimitri the Red Hermaphroditic Ibex\n\n'
        print(string)    