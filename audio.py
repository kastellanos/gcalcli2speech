import pygame

class Audio:
    def __init__(self, filename):
        pygame.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

