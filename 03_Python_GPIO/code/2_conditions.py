compteur = 0

# Les conditions permettent de faire des choix dans le programme
if compteur > 5:
    print("Compteur est strictement plus grand que 5")

# elif est une seconde condition, si la première est fausse
elif compteur == 5:
    print("Compteur vaut 5")

# on peut combiner les opérateurs logiques and, or, not
elif (False or True) and not True:
    print("Ceci ne se produira pas")

# else est la condition par défaut, si le autres sont fausses
else:
    print("Compteur <= 5")
