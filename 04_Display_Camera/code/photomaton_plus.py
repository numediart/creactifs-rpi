# Importer toutes les librairies nécessaires
import datetime
import math

import cv2
import numpy as np
import pygame

# Ce bloc essaie d'importer la librairie Picamera2, spécifique aux caméras Raspberry Pi
try:
    from picamera2 import Picamera2

    PICAM_IMPORTED = True

# Sur une autre plateforme ou si la librairie n'est pas installée, ce code
# utilisera une caméra compatible OpenCV à la place
except ImportError:
    PICAM_IMPORTED = False

# Initialiser Pygame (pour l'interface graphique)
pygame.init()
pygame.font.init()  # Initialiser le module de police pour afficher du texte

# Définir la police pour le texte de compte à rebours
countdown_font = pygame.font.SysFont("dejavusansmono", 200)

# Récupérer les informations de l'écran (dimensions)
screen_info = pygame.display.Info()

# Mettre la fenêtre en plein écran
screen = pygame.display.set_mode(
    (screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN
)

# Définir le titre de la fenêtre
pygame.display.set_caption("Photomaton")

# Configurer et démarrer la caméra
# Avec Picamera2
if PICAM_IMPORTED:
    picam2 = Picamera2()
    # Options: résolution de l'image, format de couleur
    preview_config = picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    picam2.configure(preview_config)
    picam2.start()

# Sans Picamera2, utiliser une caméra compatible OpenCV (comme une webcam)
else:
    cvcam = cv2.VideoCapture(0)

# Horloge pour contrôler la fréquence de rafraîchissement
clock = pygame.time.Clock()


click_time = -1  # Variable pour retenir quand le clic a eu lieu
captured = False  # Variable pour savoir si une capture a été prise
DELAY_BEFORE_CAPTURE = 3  # Délai en secondes avant de capturer l'image après le clic
FLASH_DURATION = 0.5  # Durée de l'effet de flash en secondes
PREVIEW_DURATION = 2  # Durée d'affichage de l'image capturée

# Créer une surface blanche pour le flash
FLASH_SURFACE = pygame.Surface((screen_info.current_w, screen_info.current_h))
FLASH_SURFACE.fill((255, 255, 255))  # Surface blanche

# Boucle principale du programme
# C'est ici que toute la logique du photomaton se trouve
running = True
while running:
    # Gérer les événements (clavier, souris)
    for event in pygame.event.get():
        # Clic de souris: capturer une image
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Enregistrer le moment du clic si ce n'est pas déjà fait
            if click_time < 0:
                click_time = pygame.time.get_ticks()

        # Touche ESC: arrêter la boucle principale
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # Signal de fermeture de la fenêtre: arrêter la boucle principale
        elif event.type == pygame.QUIT:
            running = False

    # Récupérer une image de la caméra
    if PICAM_IMPORTED:
        # Avec Picamera2
        frame = picam2.capture_array()
    else:
        # Avec OpenCV
        _, frame = cvcam.read()

    # Convertir l'image de RGB à BGR
    surface = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Tourner l'image de 90 degrés pour correspondre à l'orientation de l'écran
    surface = pygame.surfarray.make_surface(np.rot90(surface))

    # Redimensionner l'image pour qu'elle remplisse l'écran
    surface = pygame.transform.scale(
        surface, (screen_info.current_w, screen_info.current_h)
    )

    # Afficher l'image à l'écran
    screen.blit(surface, (0, 0))

    # Si un clic a eu lieu
    if click_time >= 0:
        # Calculer le temps écoulé depuis le clic, en secondes
        elapsed_time = (pygame.time.get_ticks() - click_time) / 1000.0

        # Pendant le compte à rebours avant la capture
        if elapsed_time < DELAY_BEFORE_CAPTURE:
            # Calculer le temps restant avant capture
            remaining = DELAY_BEFORE_CAPTURE - elapsed_time
            remaining = math.ceil(remaining)  # Arrondir à l'entier supérieur

            # Créer une surface de texte pour le compte à rebours
            countdown_text = countdown_font.render(
                str(remaining), True, (255, 255, 255)
            )

            # Afficher le compte à rebours au centre de l'écran
            screen.blit(
                countdown_text,
                (
                    screen_info.current_w // 2 - countdown_text.get_width() // 2,
                    screen_info.current_h // 2 - countdown_text.get_height() // 2,
                ),
            )

        # Pendant l'effet de flash
        elif elapsed_time < DELAY_BEFORE_CAPTURE + FLASH_DURATION:
            # Si l'image n'a pas encore été capturée, la capturer et l'enregistrer
            if not captured:
                date = datetime.datetime.now()  # Enregistrer la date et l'heure
                filename = str(date) + ".jpg"  # Convertir en nom de fichier
                cv2.imwrite(filename, frame)  # Enregistrer l'image capturée
                captured = True  # Marquer que la capture est prise

                # Copier la surface pour l'affichage de l'image capturée
                captured_surface = surface.copy()

            # Calculer l'intensité du flash (de 0 à 1) en fonction du temps écoulé
            flash_percentage = 1 - (
                (elapsed_time - DELAY_BEFORE_CAPTURE) / FLASH_DURATION
            )
            # Convertir l'intensité du flash de 0 à 255
            flash_intensity = int(255 * flash_percentage)
            FLASH_SURFACE.set_alpha(flash_intensity)  # Appliquer l'intensité du flash

            screen.blit(captured_surface, (0, 0))  # Afficher l'image capturée à l'écran
            screen.blit(FLASH_SURFACE, (0, 0))  # Afficher le flash par-dessus

        # Pendant l'affichage de l'image capturée
        elif elapsed_time < DELAY_BEFORE_CAPTURE + FLASH_DURATION + PREVIEW_DURATION:
            screen.blit(captured_surface, (0, 0))  # Afficher l'image capturée à l'écran

        # La capture est terminée, réinitialiser les variables
        else:
            click_time = -1  # Réinitialiser le clic pour permettre une nouvelle capture
            captured = False  # Réinitialiser l'état de capture pour la prochaine fois

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Forcer le rafraîchissement à max 30 images par seconde
    clock.tick(30)

# Fin de la boucle: le programme se termine

if PICAM_IMPORTED:
    # Arrêter la caméra
    picam2.stop()

# Fermer la fenêtre
pygame.quit()
