import adafruit_dht
import board

# Créer un objet DHT22 sur le port GPIO4 (pin 7)
dht = adafruit_dht.DHT22(board.D4)

# Lire la température et l'humidité
print("Température:", dht.temperature, "C")
print("Humidité:", dht.humidity, "%")
