import pygame
from pygame.rect import Rect


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Platform(Entity):
    def __init__(self, x, y, image, mat="Unknown", amount=1, hp=20):
        Entity.__init__(self)
        self.img = pygame.transform.scale(image, (32, 32))
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.img)
        self.mat = mat
        self.amount = amount
        self.name = mat
        self.start_hp = hp
        self.hp = hp
        self.collidable = True

    def update(self):
        pass
