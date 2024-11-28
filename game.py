from board import *
from pawn import *

class Game():

    def __init__(self):
        self.in_progress = True                             # le bool qui change en False quand les conditions d'arrêt de jeu sont réunies
        self.board = Board()                                # instance de Bord qui représente l'échiquier
        self.all_pawns = [Pawn(i) for i in range(1,65)]     # liste de tous les pions, chaque pion est une instance de Pawn
        self.step = 0                                       # entier incrémental, qui suit à quelle étape on est
        self.player = False # False si noir True si blanc   # bool qui désigne qui doit jouer à l'étape (les noirs ou les blancs)
        self.neighbors_relative_position=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] # position en relatif des 9 voisins
        self.add_initial_pawns()                            # initialisation des 4 1er pions
        print(self.board)

    def add_initial_pawns(self):
        # pour chaque position, on joue une étape fictive :
        for position in ['d4', 'e4', 'e5', 'd5']:       # la liste est construite de manière à ce que les pions soient bien disposés : noir blanc noir blanc
            self.put_pawn_on_board(position)            # on place le pion sur l'échiquier
            self.step += 1                              # on passe à l'étape d'après
            self.player = not self.player               # on change le joueur qui doit jouer l'étape d'après

    def put_pawn_on_board(self, position):
        # on choisit de quel pion on parle, via son index dans la liste de tous les pions
        pawn = self.all_pawns[self.step]
        # on change les attributs de ce pion
        pawn.add_on_board(position, self.player)
        # on ajoute le pion sur l'échiquier
        self.board.add_pawn(pawn)
        # on montre le résulat du pion posé à l'utilisateur
        if self.step > 3:
            print(self.board)
        
    def play_next_step(self, position):
        # est-ce que le joueur a le droit de poser le pion à cette position ? 
        is_consistent = self.verify_position(position)
        if is_consistent:
            # si oui, on ajoute le pion sur l'échiquier
            self.put_pawn_on_board(position)
            # puis on retourne les pions à retourner
            self.turn_pawns_over(position)
            # on vérifie si les conditions d'arrêt de la partie sont atteintes
            self.check_end_game()
            # on passe à l'étape d'après et on change le joueur qui doit jouer l'étape d'après
            self.step += 1
            self.player = not self.player
        return is_consistent
        
    def verify_position(self, position):
        is_consistent = True
        for check_condition in [self.verify_and_convert_position_to_tuple,self.verify_if_position_exists, self.verify_if_position_is_empty]:
            is_consistent = check_condition(position)
            if not is_consistent:
                break
        if is_consistent==True:
            is_consistent=self.check_neighbors(position=self.position,list_relative_position=self.neighbors_relative_position,couleur=self.player)[0]
        if is_consistent==True:
            is_consistent=self.check_opposite_neighbors_to_switch(neighbors=self.neighbor_df_opposite_values)
        return is_consistent
    
    def verify_and_convert_position_to_tuple(self,position):
        if not len(position)==2:
            output=False
        else:
            try :
                col=position[0].upper()
                ind=int(position[1])

                self.position=ind,col
                output=True
            except:
                output=False
        return output

    def verify_if_position_exists(self,position):
        df_local=self.board.df.copy()
        output = self.position[0] in df_local.index and self.position[1] in df_local.columns
        return output


    def verify_if_position_is_empty(self, position):
        if pd.isna(self.board.df.at[self.position[0], self.position[1]]):
            output = True
        else:
            output = False
        return output
    
    def check_neighbors(self,position,list_relative_position,couleur):
        """
        Fait la liste des voisins existants (max 9 voisins). 
        Pour chaque voisin existant, ajoute dans une liste la position du voisin dans le df et la position relative par rapport à la case testée
        Puis pour chaque voisin existant, controle sa valeur dans le df, et si elle est NON NUL, ajoute dans une liste la position df, relative et sa valeur 
        Puis convertit la couleur du nouveau pion en valeur "X" ou "O" et la compare à chaque valeur des voisins existants non nul
        Ajoute dans une liste (position df, relative, valeur) pour chaque pion dont la valeur est différente de valeur du nouveau pion
        Si au moins une des valeurs des voisins est différente de la valeur du nouveau pion, retourne True. 
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
        # --> sort une liste (position df, position relative) des plus proches voisins
        neighbors_relative_position=list_relative_position.copy()
        neighbor_df_position=[]
        for relative_position in neighbors_relative_position:
            neighbor_position_col=position_local[1]+relative_position[1]
            neighbor_position_ind=position_local[0]+relative_position[0]
            if 0<=neighbor_position_col<8 and 0<=neighbor_position_ind<8 :
                neighbor_df_position.append(((df_local.index[neighbor_position_ind],df_local.columns[neighbor_position_col]),relative_position))

        #Valeur du df de chaque proche voisin si non nul 
        # --> sort une liste (position df, position relative, valeur) des plus proches voisins du uniquement pour celles non nulles. 
        neighbor_df_values=[]
        for df_position in neighbor_df_position:
            value=df_local.at[df_position[0][0],df_position[0][1]]
            if not pd.isna(value):
                neighbor_df_values.append((df_position[0],df_position[1],value))

        #Condition du jeu : retourne vrai si au moins une des couleurs de la liste 
        #--> sort une liste (position df, position relative, valeur) des plus proches voisins de valeur opposée
        if couleur==True:
            symbol="O"
        else:
            symbol="X"
        is_consistent=False
        self.neighbor_df_opposite_values=[]
        self.neighbor_df_same_values=[]
        for value in neighbor_df_values:
            if not value[2]==symbol:
                self.neighbor_df_opposite_values.append(value)
                is_consistent=True
            if value[2]==symbol:
                self.neighbor_df_same_values.append(value)
        print(self.neighbor_df_opposite_values)
        # print(position,"\n",neighbor_df_position,"\n",neighbor_df_values,"\n",neighbor_df_opposite_values,is_consistent)
        return is_consistent,self.neighbor_df_opposite_values,self.neighbor_df_same_values
    
    def check_opposite_neighbors_to_switch(self,neighbors):
        df_local=self.board.df.copy()
        neighbors_list=neighbors.copy()
        self.pawns_to_return_list=[]
        for neighbor in neighbors_list:
            stop=False
            pawns_to_return_list_local=[]
            while not stop==True:
                origin=neighbor[0]
                orientation=[]
                orientation.append(neighbor[1])
                value=neighbor[2]
                print(origin,orientation,value)
                resultat=self.check_neighbors(position=origin,list_relative_position=orientation,couleur=value)
                print(resultat)
                if resultat[0]==False and resultat[2]==[] and not pawns_to_return_list_local==[]:
                    print(origin,"Faux et vide",resultat)
                    pawns_to_return_list_local=None
                    stop=True
                    is_consistent=False
                elif resultat[0]==False and not resultat[2]==[] and pawns_to_return_list_local==[]:
                    print(origin,"Vraie",resultat)
                    pawns_to_return_list_local.append(origin)
                    stop=True
                    is_consistent=False
                elif resultat[0]==False and not resultat[2]==[]:
                    print(origin,"Faux et opposé",resultat)
                    pawns_to_return_list_local.append(origin)
                    neighbor=resultat[2][0]
                elif resultat[0]==True:
                    print(origin,"Vraie",resultat)
                    pawns_to_return_list_local.append(origin)
                    stop=True
                    is_consistent=True
            print ("templistfinboucle",pawns_to_return_list_local)
            try:
                for pawns in pawns_to_return_list_local:
                    self.pawns_to_return_list.append(pawns)
            except:
                None

        print(f"liste de pions à retourner {self.pawns_to_return_list}")
        return is_consistent


    def turn_pawns_over(self, position):
        pass

    def check_end_game(self):
        pass

        