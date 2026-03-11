from time import sleep

from gpiozero import PWMLED

# Créer un objet PWMLED sur le port GPIO27 (pin 13)
led = PWMLED(27)

# Faire clignoter la LED 10 fois
for i in range(10):
    led.value = 0.7  # Allumer la LED a 70% de luminosité
    sleep(0.5)  # Attendre 0.5 secondes
    led.value = 0.2  # Diminuer la luminosité a 20%
    sleep(0.5)

led.value = 0.0  # Éteindre la LED
