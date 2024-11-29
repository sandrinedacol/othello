import numpy as np

from board import *
from pawn import *

class Game():

    def __init__(self):
        self.in_progress = True                             # le bool qui change en False quand les conditions d'arrêt de jeu sont réunies
        self.board = Board()                                # instance de Bord qui représente l'échiquier
        self.all_pawns = [Pawn(i) for i in range(1,65)]     # liste de tous les pions, chaque pion est une instance de Pawn
        self.step = 0                                       # entier incrémental, qui suit à quelle étape on est
        self.player = False                                 # bool qui désigne qui doit jouer à l'étape (les noirs ou les blancs)
        self.markers = {True: 'O', False: 'X'}
        self.neighbors_relative_position=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] # position en relatif des 9 voisins
        self.add_initial_pawns()                            # initialisation des 4 1er pions
        print(self.board)

    def add_initial_pawns(self):                            # pour chaque position, on joue une étape fictive :
        for position in ['d4', 'e4', 'e5', 'd5']:           # la liste est construite de manière à ce que les pions soient bien disposés : noir blanc noir blanc
            _ = self.convert_position_to_tuple(position)    # assigne la bonne valeur à self.position
            self.put_pawn_on_board()                        # on place le pion sur l'échiquier
            self.step += 1                                  # on passe à l'étape d'après
            self.player = not self.player                   # on change le joueur qui doit jouer l'étape d'après


    def put_pawn_on_board(self):
        pawn = self.all_pawns[self.step]                    # on choisit de quel pion on parle, via son index dans la liste de tous les pion   
        pawn.add_on_board(self.position, self.player)            # on change les attributs de ce pion
        self.board.add_pawn(pawn)                           # on ajoute le pion sur l'échiquier

        
        
    def play_next_step(self, position):
        if position == None:
            self.compute_best_position()
            is_consistent = True
        else:
            is_consistent = self.convert_position_to_tuple(position)

        if is_consistent:                                   
            is_consistent = self.check_position()       # est-ce que le joueur a le droit de poser le pion à cette position ? 

        if is_consistent:
            self.put_pawn_on_board()                # si oui, on ajoute le pion sur l'échiquier
            self.turn_pawns_over()                  # puis on retourne les pions à retourner
            self.check_end_game()                           # on vérifie si les conditions d'arrêt de la partie sont atteintes
            self.step += 1                                  # on passe à l'étape d'après et on change le joueur qui doit jouer l'étape d'après
            self.player = not self.player                   # et on change le joueur qui doit jouer l'étape d'après
            print(self.board)     

        if not is_consistent:
            print("Mauvais placement, recommence !")

        return is_consistent
        
    def check_position(self):
        for check_condition in [
            self.check_if_position_exists,
            self.check_if_position_is_empty
            ]:
            is_consistent = check_condition()
            if not is_consistent:
                break
        if is_consistent:
            is_consistent=self.check_neighbors(position=self.position,list_relative_position=self.neighbors_relative_position,couleur=self.player)
        if is_consistent:
            is_consistent=self.check_opposite_neighbors_to_switch(neighbors=self.neighbor_df_opposite_values)
        return is_consistent
    
    def convert_position_to_tuple(self, position):
        is_consistent = len(position) == 2
        if is_consistent:
            try :

                col=position[0].upper()
                ind=int(position[1])

                self.position=ind,col
                output=True
            except:
                output=False
        return output

    def verify_if_position_exists(self):
        df_local=self.board.df.copy()
        output = self.position[0] in df_local.index and self.position[1] in df_local.columns
        return output


    def check_if_position_exists(self):
        index_exists = self.position[0] in self.board.df.index
        column_exists = self.position[1] in self.board.df.columns
        return index_exists and column_exists

    def verify_if_position_is_empty(self, position):
        if self.board.df.at[self.position[0], self.position[1]]==" ":
            output = True
        else:
            output = False
        return output
    
    def check_neighbors(self,position,list_relative_position,couleur):
        """
        Fait la liste des voisins existants (max 9 voisins). 
        Pour chaque voisin existant, ajoute dans une liste la position du voisin dans le df et la position relative par rapport à la case testée
        Puis pour chaque voisin existant, controle sa valeur dans le df, et si elle est NON NUL, ajoute dans une liste la position df, relative et sa valeur 
        Puis convertit la couleur du nouveau pion en valeur True ("O") ou False ("X") et la compare à chaque valeur des voisins existants non nul
        Ajoute dans une liste_1 (position df, relative, valeur) pour chaque pion dont la valeur est différente de valeur du nouveau pion
        Ajoute dans une liste_2(position df, relative, valeur) pour chaque pion dont la valeur est la même que celle du nouveau pion
        Retourne un tuple (A,B,C):
            A : Si au moins une des valeurs des voisins est différente de la valeur du nouveau pion, retourne True 
            B : liste_1 (position df, relative, valeur) de pions de valeur opposée
            C : liste_2 (position df, relative, valeur) de pions de même valeur que le nouveau pion
        """
        df_local=self.board.df.copy()

        #Correspondance lettre position
        dict_col={}
        n=0
        for i in df_local.columns.tolist():
            dict_col[i]=n
            n+=1

        #Conversion position en int
        position_local=(position[0]-1,dict_col[position[1]])

        #Définition position relative voisins 
        # --> sort une liste (position df, position relative) des pions voisins
        neighbors_relative_position=list_relative_position.copy()
        neighbor_df_position=[]
        for relative_position in neighbors_relative_position:
            neighbor_position_col=position_local[1]+relative_position[1]
            neighbor_position_ind=position_local[0]+relative_position[0]
            if 0<=neighbor_position_col<8 and 0<=neighbor_position_ind<8 :
                neighbor_df_position.append(((int(df_local.index[neighbor_position_ind]),df_local.columns[neighbor_position_col]),relative_position))
        
        #Valeur du df de chaque proche voisin si non nul 
        # --> sort une liste (position df, position relative, valeur) des pions voisins uniquement si leur valeur est non nulle. 
        neighbor_df_values=[]
        for df_position in neighbor_df_position:
            value=df_local.at[df_position[0][0],df_position[0][1]]
            if value=="O" or value==True:
                value_TF=True
            elif value=="X" or value==False:
                value_TF=False
            else:
                value_TF=value
            if value_TF==True or value_TF==False:
                neighbor_df_values.append((df_position[0],df_position[1],value_TF))

        #Condition du jeu : retourne vrai si au moins un pion voisin de valeur opposé existe. 
        #--> sort une liste_1 (position df, position relative, valeur) des plus proches voisins de valeur opposée
        #--> sort une liste_2 (position df, position relative, valeur) des plus proches voisins de même valeur
        is_consistent=False
        self.neighbor_df_opposite_values=[]
        self.neighbor_df_same_values=[]
        for df_value in neighbor_df_values:
            if not df_value[2]==couleur:
                self.neighbor_df_opposite_values.append(df_value)
                is_consistent=True
            else:
                self.neighbor_df_same_values.append(df_value)

        return is_consistent
    
    def check_opposite_neighbors_to_switch(self,neighbors):
        """
        Prend en entrée la liste des pions voisins existants de valeurs opposés au pion "C" que l'on cherche à placer
        Pour chaque pions "V" de la liste, recherche son prochain voisin "V+1" avec la fonction "check_voisin":
        La boucle suivante est créé : 
            On stocke le pion "V" dans une liste temporaire
            On demande de checker le voisin "V+1" qui est dans la direction pion "C" - pion "V
            Si le pion "V+1" est de couleur différente du pion "V" --> Stoppe la boucle
            Si le pion "V+1" n'existe pas --> Stoppe la boucle et efface la liste temporaire
            Si le pion "V+1" est de même couleur que le pion "V" --> Le pion "V+1" devient le nouveau pion "V"
            On boucle ainsi "V+2","V+3",etc... jusqu'à ce qu'une des 2 premières conditions soit remplies. 
            (le nouveau pion est stockée en début de boucle, on a donc en sortie une liste ("V","V+1","V+2","V+3",...)
        Une fois sortie de la boucle, on stocke la liste temporaire dans la liste permanente de pions à retourner et on passe au pion "V" suivant.
        Si la liste de pions à retourner n'est pas vide, la méthode renvoie Vrai. Sinon la méthode renvoie Faux.
        """
        neighbors_list=neighbors.copy() # Copie la liste de pions voisins
        self.pawns_to_return_list=[]    # Creer une liste vide de pions à retourner comme attribut de classe
        is_consistent=False             # Définit le return de la méthode comme Faux par défaut
        
        # Boucle pour chaque élémént de la liste des pions voisins de valeur opposés
        for neighbor in neighbors_list:
            stop=False
            pawns_to_return_list_temp=[]  #Creer une liste temporaire de pions à retourner           

            #Boucle dans la direction "orientation" (position relative du pion voisin par rapport au pion d'origine)
            while not stop==True:         
                origin=neighbor[0]                  # origin = la position du pion dans le df ex:(4,'E')
                orientation=[]                      # orientation = la position relative du pion par rapport au pion d'origine                                
                orientation.append(neighbor[1])     # orientation :format liste --> ex:[(-1,0)]
                value=neighbor[2]                   # value = couleur du pion True (O) ou False (X)
                pawns_to_return_list_temp.append(origin)     # Ajoute le pion voisin dans la liste temporaire 
                
                # Appelle la fonction "check voisins" en prenant comme origine le piont voisin
                resultat=self.check_neighbors(position=origin,list_relative_position=orientation,couleur=value)

                if resultat==True :     # Si resultat[0] = booleen "pion voisin de valeur opposé existe" EST egale à True
                    stop=True              # --> stoppe la boucle while
                elif resultat==False and self.neighbor_df_same_values==[]:    #  Si resultat EST faux et liste_pions_voisins_même_couleur EST vide.
                    pawns_to_return_list_temp=[]                              # --> efface la liste temporaire
                    stop=True                                                 # --> stoppe la boucle while
                elif resultat==False and not self.neighbor_df_same_values==[]:      # Si resultat EST faux et liste_pions_voisins_même_couleur N'EST PAS vide.
                    neighbor=self.neighbor_df_same_values[0]                       # --> le pion voisin devient la nouvelle origine
                                                                                    # --> la boucle while continue avec la nouvelle position origine
        
            try:     # --> ajoute les valeurs de la liste temporaire dans la liste definitive et définit le return à True
                for pawns in pawns_to_return_list_temp:
                    self.pawns_to_return_list.append(pawns)
                    is_consistent=True  #Condition du jeu : retourne vrai s'il existe au moins un pion à retourner.
            except:
                None

        return is_consistent


    def turn_pawns_over(self):
        marker = self.markers[self.player]
        for pawn_position in self.pawns_to_return_list:
            self.board.df.at[pawn_position[0],pawn_position[1]] = marker
      
    def check_if_position_is_empty(self):
        value = self.board.df.at[self.position[0], self.position[1]]
        return value == ' '

    def check_end_game(self):
        # modifie game.in_progress si les conditions de fin de partie sont réunies
        empty_squares = [(self.board.df.index[x], self.board.df.columns[y]) for x, y in zip(*np.where(self.board.df.values == ' '))]
        is_consistent = False
        for square in empty_squares:
            self.position = square
            is_consistent = self.check_position()   # à remplacer par les 2 méthodes de Romain : 'adjcent' et 'encadre'
            if is_consistent:
                break
        if not is_consistent:
            self.in_progress = False

    def compute_score(self):
        # return black_score, white_score
        board_array = self.board.df.to_numpy()
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
        
    def compute_best_position(self):
        consistent_positions = [] # à faire : pour toutes les positions, celles qui passent les conditions sont retenues
        best_position, best_score = None, 0
        for pos in consistent_positions:
            fictive_board = Board()
            fictive_board.df = self.board.df.copy()
            self.position = pos
            n_turned_pawns = 0 # à remplacer par le calcul des pions qui seraient retournés (effectué sur fictive_board)
            if n_turned_pawns > best_score:
                best_position, best_score = pos, n_turned_pawns
        # self.position = best_position
        _ = self.convert_position_to_tuple(input(f"PC ({self.markers[self.player]}) : "))        # juste le temps d'écrire le reste