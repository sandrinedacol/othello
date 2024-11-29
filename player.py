# Classe Player

class Player():

    def __init__(self):
        self.menu_game_mode()
        self.player1_name=self.ask_for_player_name(game_mode=self.game_mode)

    def menu_game_mode(self):
        self.game_mode=0
        while not self.game_mode==1 or self.game_mode==2:
            try :
                self.game_mode=int(input("Choisis ton mode de jeu :\n\n    1 - Mode seul contre l'IA :\n    2 - Mode 2 joueurs:\n\n"))
            except:
                print("Choisis 1 ou 2")


    def ask_for_player_name (self,game_mode=1):
        self.player1_name=str(input("First player : enter your unicorn or dragon name here : "))
        if game_mode==2:
            self.player2_name=str(input("FSecond player : enter your unicorn or dragon name here :"))