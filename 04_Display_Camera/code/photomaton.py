# Importer toutes les librairies nécessaires
import cv2
import numpy as np
import pygame
from picamera2 import Picamera2

# Initialiser Pygame (pour l'interface graphique)
pygame.init()

# Récupérer les informations de l'écran (dimensions)
screen_info = pygame.display.Info()

# Mettre la fenêtre en plein écran
screen = pygame.display.set_mode(
    (screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN
)

# Définir le titre de la fenêtre
pygame.display.set_caption("Photomaton")

# Configurer et démarrer la caméra
# Options: résolution de l'image, format de couleur
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
picam2.configure(preview_config)
picam2.start()

# Horloge pour contrôler la fréquence de rafraîchissement
clock = pygame.time.Clock()

# Boucle principale du programme
# C'est ici que toute la logique du photomaton se trouve
running = True
while running:
    # Gérer les événements (clavier, souris)
    for event in pygame.event.get():
        # Clic de souris: capturer une image
        if event.type == pygame.MOUSEBUTTONDOWN:
            filename = "capture.jpg"
            picam2.capture_file(filename)

        # Touche ESC: arrêter la boucle principale
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # Signal de fermeture de la fenêtre: arrêter la boucle principale
        elif event.type == pygame.QUIT:
            running = False

    # Récupérer une image de la caméra
    frame = picam2.capture_array()

    # Convertir l'image de RGB à BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Tourner l'image de 90 degrés pour correspondre à l'orientation de l'écran
    surface = pygame.surfarray.make_surface(np.rot90(frame))

    # Redimensionner l'image pour qu'elle remplisse l'écran
    scaled_surface = pygame.transform.scale(
        surface, (screen_info.current_w, screen_info.current_h)
    )

    # Afficher l'image à l'écran et mettre à jour l'affichage
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()

    # Forcer le rafraîchissement à max 30 images par seconde
    clock.tick(30)

# Fin de la boucle: le programme se termine
# Arrêter la caméra et la fenêtre
picam2.stop()
pygame.quit()
