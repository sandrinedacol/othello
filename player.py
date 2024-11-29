# Classe Player

class Player():

    def __init__(self):
        print('\nWelcome to the most BEAUTIFUL & FUNNY & INTELLIGENT game ever!')
        self.menu_game_mode()
        self.ask_for_player_name()
        

    def menu_game_mode(self):
        self.game_mode=0
        while not self.game_mode==1 or not self.game_mode==2:
            try :
                self.game_mode=int(input("Choisis ton mode de jeu :\n\n    1 - Mode seul contre l'IA :\n    2 - Mode 2 joueurs:\n\n"))
                break
            except:
                print("Choisis 1 ou 2")

    def ask_for_player_name (self):
        self.player1_name=str(input("\nFirst player : enter your unicorn or dragon name here : "))
        if self.game_mode==2:
            self.player2_name=str(input("\nSecond player : enter your unicorn or dragon name here :"))

        