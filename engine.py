from game import *

class Engine():

    def __init__(self):
        print('\nWelcome to the most beautiful Othello game ever!\n\n')
        # user_color est la couleur choisie par l'utilisateur : noir ou blanc
        self.user_color = self.ask_user_color()
        # on commence une partie
        self.game = self.start_new_game()
        # tant que les conditions sont réunies, le jeu continue
        while self.game.in_progress:
            step_played = False
            while not step_played:
                position = self.choose_position()
                # La prochaine étape est lancée avec le prochain pion posé à cette position
                step_played = self.game.play_next_step(position)
        # une fois que les conditions d'arrêt de jeu changent le bool game.in_progress, on finit le jeu
        self.end_game()

    def ask_user_color(self):
        user_color = input('Do you want to be Master of Blacks (B) or Whites (W)?')
        user_color = user_color.strip().upper()
        if user_color == 'B':
            print("Ok, you're black (X), you start.\n")
            return False             # noir = false
        elif user_color == 'W':
            print("Ok, you're white (O), I start.\n")
            return True             # blanc = true
        else:
            return self.ask_user_color()
        
    def start_new_game(self):
        _ = input('Ready?\n')           # met juste un temps de pause, l'utilisateur doit mettre entrée pour que ça lance la suite
        return Game()                   # crée une instance de game = une partie
    
    def choose_position(self):
        # si la couleur assignée à l'utilisateur est celle du prochain joueur
        if self.user_color == self.game.player:
            position = input('Your turn:')
        # si le prochain joueur est l'ordinateur
        else:
            position = input('I play:')
            print(f"I play {position}")
        return position

    def end_game(self):
        pass
