import pygame

class Shape (pygame.sprite.Sprite):

    def __init__(self, surface):
        ## initialize parent class
        super().__init__() # "super()" here is = to "pygame.sprite.Sprite"

        ## setup the shape
        self.rect = surface.get_bounding_rect()
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image.blit(surface, (0,0), self.rect)