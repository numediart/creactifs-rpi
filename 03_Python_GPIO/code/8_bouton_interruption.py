from time import sleep

from gpiozero import Button

# Créer un objet Button sur le port GPIO17 (pin 11)
button = Button(17)


# Créer une fonction a exécuter quand on appuie sur le bouton
def on_press():
    print("Bouton appuyé!")


# Associer la fonction a l'événement "when_pressed" du bouton
button.when_pressed = on_press

input("Appuyez sur Enter pour terminer le programme...")
