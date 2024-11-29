import pandas as pd
import numpy

def check_neighbors(df,position,couleur,list_relative_position):
    df_local=df.copy()

    #Correspondance lettre position
    dict_col={}
    n=0
    for i in df_local.columns.tolist():
        dict_col[i]=n
        n+=1

    #Conversion position en int
    position_local=(position[0]-1,dict_col[position[1]])

    #Définition position relative voisins --> sort une liste des positions des plus proches voisins en coordonnées df
    neighbors_relative_position=list_relative_position.copy()
    neighbor_df_position=[]
    for relative_position in neighbors_relative_position:
        neighbor_position_col=position_local[1]+relative_position[1]
        neighbor_position_ind=position_local[0]+relative_position[0]
        if 0<=neighbor_position_col<8 and 0<=neighbor_position_ind<8 :
            neighbor_df_position.append(((df_local.index[neighbor_position_ind],df_local.columns[neighbor_position_col]),relative_position))

    #Valeur du df de chaque proche voisin si non nul --> sort une liste (positions,valeurs) des plus proches voisins du df uniquement pour celles non nulles. 
    neighbor_df_values=[]
    for df_position in neighbor_df_position:
        value=df_local.at[df_position[0][0],df_position[0][1]]
        if not pd.isna(value):
            neighbor_df_values.append((df_position[0],df_position[1],value))

    #Condition du jeu : retourne vrai si au moins une des couleurs de la liste 
    if couleur==True:
        symbol="O"
    else:
        symbol="X"
    is_consistent=False
    neighbor_df_opposite_values=[]
    neighbor_df_same_values=[]
    for value in neighbor_df_values:
        if not value[2]==symbol:
            neighbor_df_opposite_values.append(value)
            is_consistent=True
        if value[2]==symbol:
            neighbor_df_same_values.append(value)

    # print(position,"\n",neighbor_df_position,"\n",neighbor_df_values,"\n",neighbor_df_opposite_values)

    return is_consistent,neighbor_df_opposite_values,neighbor_df_same_values

def check_opposite_neighbors_to_switch(df,neighbors):
    df_local=df.copy()
    neighbors_list=neighbors.copy()
    pawns_to_return_list=[]
    for neighbor in neighbors_list:
        stop=False
        pawns_to_return_list_local=[]
        while not stop==True:
            origin=neighbor[0]
            orientation=[]
            orientation.append(neighbor[1])
            value=neighbor[2]
            print(origin,orientation,value)
            resultat=check_neighbors(df=df_local,position=origin,list_relative_position=orientation,couleur=value)
            print(resultat)
            if resultat[0]==False and resultat[2]==[] and len(pawns_to_return_list_local)>1:
                print(origin,"Faux et vide",resultat)
                stop=True
                is_consistent=False

            elif resultat[0]==False and resultat[2]==[] and pawns_to_return_list_local==[]:
                print(origin,"Vrai et vide",resultat)
                pawns_to_return_list_local.append(origin)
                stop=True
                is_consistent=True

            elif resultat[0]==False and not resultat[2]==[]:
                print(origin,"Faux et opposé",resultat)
                pawns_to_return_list_local.append(origin)
                neighbor=resultat[2][0]
            elif resultat[0]==True :
                print(origin,"Vraie",resultat)
                pawns_to_return_list_local.append(origin)
                stop=True
                is_consistent=True
        print ("templistfinboucle",pawns_to_return_list_local)
        try:
            for pawns in pawns_to_return_list_local:
                pawns_to_return_list.append(pawns)
        except:
            None

    print(f"liste de pions à retourner {pawns_to_return_list},{is_consistent}")
    return is_consistent

df = pd.DataFrame(index = list(range(1,9)), columns = list('ABCDEFGH'))
df.at[4,"D"]=df.at[5,"E"]=df.at[6,"D"]=df.at[6,"C"]=df.at[5,"F"]=df.at[6,"B"]=df.at[4,"G"]="X"
df.at[5,"D"]=df.at[4,"E"]=df.at[3,"H"]="O"
# df.at[4,"D"]=df.at[5,"E"]="X"
# df.at[5,"D"]=df.at[4,"E"]="O"
print(df)

neighbors_relative_position=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
voisins=check_neighbors(df,position=(6,"E"),couleur=True,list_relative_position=neighbors_relative_position)
print(voisins)
check_opposite_neighbors_to_switch(df,voisins[1])