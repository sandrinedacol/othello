import pandas as pd

class Board():
    '''Creation de l'echiquier'''
    def __init__(self):
        # représentation de l'échiquier par un dataframe, ligne = chiffre colonnes = lettre
        self.df = pd.DataFrame(index = list(range(1,9)), columns = list('ABCDEFGH')).fillna(' ')
        self.create_dict()

        
    def create_dict(self):
        '''Crée une un dictionnaire contenant une liste avec le nom des colonnes espacés correctement et une liste de separateur et enregistre dans le dico'''    
        #Crée la liste contenant le nom des colonnes
        self.dico_board = {}
        lst_for_names = ['    ']
        for name in 'ABCDEFGH':
            lst_for_names.append(name)
            lst_for_names.append('   ')
        self.dico_board['name_col'] = lst_for_names

        #Crée une liste a utiliser comme séparateur de lignes et enregistre dans le dico
        lst_for_sep = ['  +']
        for i in range(8):
            lst_for_sep.append('---+')
        self.dico_board['sep'] = lst_for_sep

    def add_pawn(self, pawn):
        # choix du marqueur à ajouter dans la case
        if pawn.color:
            marker = 'O'
        else:
            marker = 'X'
        # on change la case situé à la position demandée
        self.df.at[pawn.index, pawn.column] = marker

    def __str__(self):
        #Crée une liste pour chaque ligne numérotée et enregistre dans le dico
        for i in self.df.index:
            lst_for_row = []
            lst_for_row.append(f'{i} | ')
            for j in self.df.columns:
                lst_for_row.append(self.df.loc[i,j])
                lst_for_row.append(' | ')
            self.dico_board[i] = lst_for_row
        
        #Crée un string pour imprimer le board
        str_to_print = ''.join(self.dico_board['name_col']) + '\n' + ''.join(self.dico_board['sep'])
        for i in range(1,9):
            str_to_print += '\n' + ''.join(self.dico_board[i]) + '\n' + ''.join(self.dico_board['sep'])
        return str_to_print