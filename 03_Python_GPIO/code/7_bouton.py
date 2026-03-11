from time import sleep

from gpiozero import Button

# Créer un objet Button sur le port GPIO17 (pin 11)
button = Button(17)

# Lire la valeur du bouton chaque seconde
for i in range(10):
    if button.is_pressed:
        print("Le bouton est appuyé!")
    else:
        print("Le bouton n'est pas appuyé.")
    sleep(1)
