compteur = 0

# Les boucles while tournent tant que la condition est vraie
while compteur < 10:
    print("Compteur:", compteur)
    compteur = compteur + 1

# Les boucles for itèrent sur une séquence d'éléments
for index in range(5):
    print("index:", index)

# On peut "casser" une boucle en avance avec break
while True:
    print("Ceci tourne pour toujours")
    compteur = compteur + 1

    if compteur > 20:
        break
