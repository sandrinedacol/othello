from game import *

class Engine():

    def __init__(self):
        print('\nWelcome to the most beautiful Othello game ever!\n\n')
        self.user_color = self.ask_user_color()         # user_color est la couleur choisie par l'utilisateur : noir ou blanc
        _ = input('Ready?\n') 
        self.quit = False
        while not self.quit:
            self.play_game()
            self.quit = not self.ask_for_play_again()

    def play_game(self):
        self.game = Game()
        while self.game.in_progress:                    # tant que les conditions sont réunies, le jeu continue
            step_played = False
            while not step_played:
                position = self.choose_position()
                if position.strip().lower() in ['q', 'quit', 'exit', 'exit()']:     # si l'utilisateur entre 'q' ou 'quit' ou 'exit' ou 'exit()',
                    return None
                else:                                                               # sinon
                    step_played = self.game.play_next_step(position)                # La prochaine étape est lancée avec le prochain pion posé à cette position
        self.end_game()                                                             # une fois que les conditions d'arrêt de jeu changent le bool 'game.in_progress', on finit le jeu
        
    def ask_for_play_again(self):     
        again = input("\nPlay again? [Y/n]\n")
        return again.strip().lower() in ['y', 'yes', 'oui', 'o', '']

    def ask_user_color(self):
        user_color = input('Do you want to be Master of Blacks (B) or Whites (W)?')
        user_color = user_color.strip().upper()
        if user_color == 'B':
            print("Ok, you're black (symbol: X), you start.\n")
            return False             # noir = false
        elif user_color == 'W':
            print("Ok, you're white (symbol: O), I start.\n")
            return True             # blanc = true
        else:
            return self.ask_user_color()
    
    def choose_position(self):
        if self.user_color == self.game.player:     # si la couleur assignée à l'utilisateur est celle du prochain joueur
            position = input('Your turn:')          # si le prochain joueur est l'ordinateur
        else:
            position = input('I play:')
            print(f"I play {position}")
        return position

    def end_game(self):
        black_score, white_score = self.game.compute_score()
        if self.user_color:
            user_score, machine_score = white_score, black_score
        else:
            user_score, machine_score = black_score, white_score
        if user_score > machine_score:
            print(f"You won {user_score}, {machine_score}.\n")
        elif user_score == machine_score:
            print(f"Draw : {user_score} - {machine_score}.\n")
        else:
            self.return_game_over()
            print(f"You lost {user_score}, {machine_score}.\n")

    def return_congrats(self):
        print("\n\n ▗▄▄▖ ▗▄▖ ▗▖  ▗▖ ▗▄▄▖▗▄▄▖  ▗▄▖▗▄▄▄▖▗▄▄▖    \n▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌ █ ▐▌       \n▐▌   ▐▌ ▐▌▐▌ ▝▜▌▐▌▝▜▌▐▛▀▚▖▐▛▀▜▌ █  ▝▀▚▖    \n▝▚▄▄▖▝▚▄▞▘▐▌  ▐▌▝▚▄▞▘▐▌ ▐▌▐▌ ▐▌ █ ▗▄▄▞▘\n\n")

    def return_game_over(self):
        print("\n\n ▗▄▄▖▗▞▀▜▌▄▄▄▄  ▗▞▀▚▖     ▗▄▖ ▄   ▄ ▗▞▀▚▖ ▄▄▄\n▐▌   ▝▚▄▟▌█ █ █ ▐▛▀▀▘    ▐▌ ▐▌█   █ ▐▛▀▀▘█    \n▐▌▝▜▌     █   █ ▝▚▄▄▖    ▐▌ ▐▌ ▀▄▀  ▝▚▄▄▖█    \n▝▚▄▞▘                    ▝▚▄▞▘\n\n")
