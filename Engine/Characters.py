import pygame

display = pygame.display.set_mode((1200, 600))
from Engine.Player import *
from Engine.Animations import AnimationPack

"""Default Player"""
Player1 = AnimationPack("Assets/Hero")
Player1.add_animation_sets("run-right", "idle-right", "hit1-right", "hit2-right", "hit3-right")
Player1.create_flipped_animation_sets()
Player1.set_animation_count({"hit": 3})

"""Default Player"""
player1 = Player(
    controls={"left": pygame.K_a, "right": pygame.K_d, "reset-position": pygame.K_r, "hit": pygame.K_SPACE,
              "up": pygame.K_w, "reset": pygame.K_r, "speedup": pygame.K_LSHIFT},
    size=(175, 130), animation=Player1, speed=5)

player1.hit_animation_speed = 5
player1.idle_animation_speed = 3
player1.walk_animation_speed = 7
player1.name_delta_x = 140
player1.name_delta_y = 5
