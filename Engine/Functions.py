import random
from copy import copy

import pygame


def bake_light(display, clear_image_filter, camera, player, light):
    image_filter = copy(clear_image_filter)
    coords = camera.apply(player)
    image_filter.blit(light, (coords[0] - 250, coords[1] - 170))
    display.blit(image_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)


def show_fps(display, clock, font, coords=(25, 140), color=(0, 0, 0)):
    """This function draws current fps on screen"""
    text = font.render("fps: " + str(int(clock.get_fps())), True, color)
    display.blit(text, coords)


def show_info(display, info, font, coords=(25, 170), color=(255, 255, 255)):
    """This function draws current fps on screen"""
    text = font.render(str(info), True, color)
    display.blit(text, coords)


def npc(player=None, reactionSpeed=250, sleepDiapasone=(100, 150), FramesClock=None, borders=True):
    """NPC Logic."""
    w, h = pygame.display.get_surface().get_size()
    if player is None:
        raise ValueError("There is no Player given.")
    if FramesClock is None:
        raise ValueError("There is no FramesClock given.")
    if FramesClock >= player.awakeFrame:
        if not FramesClock % reactionSpeed:
            if player.act == "left":
                player.act = "right"
                player.awakeFrame += random.randint(*sleepDiapasone)
            else:
                player.act = "left"
                player.awakeFrame += random.randint(*sleepDiapasone)
        if player.act == "left":
            if player.border_collision and borders:
                if player.coords[0] - player.speed < 0:
                    player.coords = [0, player.coords[1]]
                else:
                    player.left()
                    player.set_sprite_from_pack("run-left", FramesClock // 17 % 6)
                    player.direction = "left"
            else:
                player.left()
                player.set_sprite_from_pack("run-left", FramesClock // 17 % 6)
                player.direction = "left"
        else:
            if player.border_collision and borders:
                if player.coords[0] + player.width + player.speed > w:
                    player.coords = [w - player.width, player.coords[1]]

                else:
                    player.right()
                    player.set_sprite_from_pack("run-right", FramesClock // 17 % 6)
                    player.direction = "right"
            else:
                player.right()
                player.set_sprite_from_pack("run-right", FramesClock // 17 % 6)
                player.direction = "right"
    else:
        if player.direction == "right":
            player.set_sprite_from_pack("idle-right", FramesClock // 40 % 3)
        else:
            player.set_sprite_from_pack("idle-left", FramesClock // 40 % 3)


"""def calculate_coords(width, height, x_left, y_bottom=0):
    x1, y1 = x_left, y_bottom + height
    x2, y2 = x_left + width, y_bottom
    return (x1, y1), (x2, y2)"""
