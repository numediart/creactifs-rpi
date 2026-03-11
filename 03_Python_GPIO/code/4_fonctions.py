# Les fonctions peuvent etre appelées avec des arguments
# syntaxe: def nom_fonction(arguments):
def ajouter(a, b):
    print("Addition de", a, "et", b)

    # Et retourner une valeur
    return a + b


resultat = ajouter(3, 4)
print("Résultat:", resultat)

# On peut importer des librairies pour utiliser des fonctions existantes
import math

resultat = math.sqrt(2)
print("Racine carrée de 2:", resultat)
