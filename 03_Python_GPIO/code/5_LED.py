# On n'importe que ce dont on a besoin ici
from time import sleep

from gpiozero import LED

# Créer un objet LED sur le port GPIO27 (pin 13)
led = LED(27)

# Faire clignoter la LED 10 fois
for i in range(10):
    led.on()  # Allumer la LED
    sleep(0.5)  # Attendre 0.5 secondes
    led.off()  # Éteindre la LED
    sleep(0.5)
