# Une liste peut contenir plusieurs variables différentes
liste = [42, "texte", True]
print("liste =", liste)

# On utilise [] pour accéder a un élément, en partant de 0
print("liste[1] =", liste[1])

# On peut ajouter des éléments a la fin de la liste
liste.append(3.14)
print("liste après append:", liste)

# Et mesurer sa longueur
longueur = len(liste)
print("longueur de la liste:", longueur)

# Un dictionnaire associe chaque élément a une clé
dictionnaire = {"univers": 42, "pi": 3.14}
print("dictionnaire['univers'] =", dictionnaire["univers"])
