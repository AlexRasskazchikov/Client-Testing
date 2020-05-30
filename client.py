import os
import getpass
os.chdir(f'C:/Users/{getpass.getuser()}/Desktop/Client-master/')
from copy import copy

import pygame
from pygame.rect import Rect

from Engine.Characters import Player1
from Engine.Levels import Polygon, BackgroundObject
from functions import vertical_gradient, inventory_add_object, show_info, show_fps
from network import Network

WIN_WIDTH = 500
WIN_HEIGHT = 600
HALF_WIDTH = WIN_WIDTH // 2
HALF_HEIGHT = WIN_HEIGHT // 2

CAMERA_SLACK = 500
ch = 50
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Deepworld Client")

PACK = Player1

ground = pygame.Surface((ch, ch))
ground.fill((125, 125, 125))
construct = pygame.Surface((ch, ch))
construct.fill((156, 156, 159))

sprites = {
    "ground": ground,
    "construct": construct,
    "right": pygame.Surface((ch, ch)),
    "left": pygame.Surface((ch, ch)),
    "earth": pygame.Surface((ch, ch)),
}


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):
        """Gets the world coordinates by screen coordinates"""
        return pos[0] - self.state.left, pos[1] - self.state.top

    def apply_rect(self, rect):
        return rect.move(self.state.topleft)


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l + HALF_WIDTH, -t + HALF_HEIGHT, w, h)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + HALF_WIDTH, -t + HALF_HEIGHT, w, h

    l = min(0, l)  # stop scrolling at the left edge
    l = max(-(camera.width - WIN_WIDTH), l)  # stop scrolling at the right edge
    t = max(-(camera.height - WIN_HEIGHT), t)  # stop scrolling at the bottom
    t = min(0, t)  # stop scrolling at the top
    return Rect(l, t, w, h)


def check_connection(*ps):
    for p in ps:
        if p is None:
            raise SystemError("Сервер недоступен.")
        if isinstance(p, str):
            raise SystemError(p)


def redrawWindow(win, player, player2, keys, FramesClock, camera):
    p1, p2 = player.img.split(":"), player2.img.split(":")

    win.blit(PACK[p1[0]][int(p1[1])], camera.apply_rect(player.rect))
    win.blit(PACK[p2[0]][int(p2[1])], camera.apply_rect(player2.rect))

    player.update_frame(keys, FramesClock, PACK)


"""Ui elements"""
position_line = pygame.Surface((485, 7), pygame.SRCALPHA, 32)
position_line.fill((255, 255, 255, 110))
player_position = pygame.Surface((11, 21), pygame.SRCALPHA, 32)
player_position.fill((255, 255, 255, 110))
bar_ending_left = pygame.image.load(r"DEEPWORLD 3.0\bar.png")
bar_ending_right = pygame.transform.flip(bar_ending_left, True, False)
bar_background = pygame.Rect(80, 80, 130, 25)
bar = pygame.Rect(80, 80, 130, 25)
gradient = vertical_gradient((WIN_WIDTH, WIN_HEIGHT), (107, 116, 202), (211, 211, 211))
font = pygame.font.Font(r'C:\Windows\Fonts\Arial.ttf', 15)
font.set_bold(True)


def main(level):
    camera = Camera(complex_camera, level.total_level_width, level.total_level_height)

    platforms = level.render_files()[:30]
    background_objects = list(map(lambda x: copy(x), level.background_objects))

    run = True
    n = Network()

    player = n.getP()

    clock = pygame.time.Clock()
    FramesClock = 1
    x = 0
    while run:
        new, rem = None, None
        clock.tick(300)
        FramesClock += 1
        display.fill((0, 0, 0))
        """display.blit(gradient, (0, 0))"""

        keys = pygame.key.get_pressed()
        events = list(map(lambda x: x.type, pygame.event.get()))
        mouse_pressed = pygame.mouse.get_pressed()
        mouse = camera.reverse(pygame.mouse.get_pos())


        if pygame.QUIT in events:
            run = False

        camera.update(player)

        for i in range(len(player.inventory)):
            if pygame.MOUSEBUTTONDOWN in events and pygame.mouse.get_pressed()[2] and player.inventory[i].choosen:
                colliding = list(map(lambda p: p.rect.collidepoint(mouse), platforms))
                if not any(colliding):
                    o = player.inventory[i]
                    new_coords = list(map(lambda x: x - x % ch, camera.reverse(pygame.mouse.get_pos())))
                    new = BackgroundObject(o.img, new_coords, name=o.name, act=True, hp=o.hp, type=o.type)
                    rect = sprites[player.inventory[i].img].get_rect(topleft=new_coords)
                    new.rect = rect
                    player.inventory[i].amount -= 1

                    if new.type != "BackgroundObject":
                        platforms.append(new)

                    # If material ended in player's inventory.
                    if player.inventory[i].amount <= 0:
                        del player.inventory[i]
                        break

            # Drawing before-placing rectangle
            elif player.inventory[i].choosen:
                mouse = camera.reverse(pygame.mouse.get_pos())
                colliding = list(map(lambda p: p.rect.collidepoint(mouse), platforms))
                if not any(colliding):
                    new_coords = list(map(lambda x: x - x % ch, mouse))
                    rect = sprites[player.inventory[i].img].get_rect(topleft=new_coords)
                    pygame.draw.rect(display, (255, 255, 255), camera.apply_rect(rect), 2)

        # Cheking on platforms
        for p in platforms:
            if mouse_pressed[0] and p.rect.collidepoint(mouse):
                player.hitting = True
                if not player.hitted:
                    p.hp -= player.damage
                    player.hitted = True

                    if p.hp <= 0:
                        platforms.remove(p)
                        inventory_add_object(player, p)

            if not player.hitting:
                player.hitted = False

        check_connection(player)
        player.move(keys, platforms)

        player.platforms = platforms
        p2 = n.send(
            {"player": player})
        platforms = p2["player"].platforms
        p1_img, p2_img = player.img.split(":"), p2["player"].img.split(":")
        p1_img, p2_img = PACK[p1_img[0]][int(p1_img[1])], PACK[p2_img[0]][int(p2_img[1])]
        display.blit(p1_img, camera.apply_rect(player.rect))
        display.blit(p2_img, camera.apply_rect(p2["player"].rect))

        # Drawing collidable objects.
        for p in platforms:
            display.blit(sprites[p.img], camera.apply_rect(p.rect))

        """show_fps(display, clock, font, color=(255, 255, 255))"""
        show_info(display, "alex", font, color=(200, 200, 200), coords=(84, 7))
        absolute_y = (700 - (player.rect.y + player.rect.h)) // 50
        absolute_x = 85 - player.rect.x // 50
        show_info(display,
                  f"- Honeyfoot Woods - {f'{absolute_x} west' if absolute_x >= 0 else f'{-absolute_x} east'},"
                  f" {f'{absolute_y} above' if absolute_y >= 0 else f'{-absolute_y} below'}",
                  font,
                  color=(114, 116, 51))

        player.update_frame(keys, FramesClock, PACK)
        player.draw_inventory(display, font, sprites, coords=(WIN_WIDTH // 3, 10))

        # Drawing map.
        display.blit(position_line, (440, 54))
        display.blit(player_position, (map_coords_calculate(player.rect.x, level.total_level_width), 33))

        # Drawing Bar1
        draw_bar(display, int(player.hp), coords=(73, 30), color=(154, 26, 34))
        draw_bar(display, int(player.steam_amount), coords=(207, 30), color=(145, 153, 155))
        if keys[pygame.K_F3]:
            show_fps(display, clock, font, color=(255, 255, 255))
        pygame.display.update()


def draw_bar(display, value, color=(207, 205, 95), bkg=(130, 126, 59), min_point=20, coords=(600, 100), l=125):
    x, y = coords
    l = l - 25
    bar.x, bar.y = x + 12, y
    bar.w, bar_background.w = l, l
    bar.w = int(value * l / 100)
    bar_background.x, bar_background.y = x + 12, y
    display.blit(bar_ending_left, (x, y))
    pygame.draw.rect(display, bkg, bar_background)
    pygame.draw.rect(display, color, bar)
    display.blit(bar_ending_right, (x + l + 12, y))
    """if value < min_point:
        show_info(display, str(value), font, (130, 80), color=(255, 100, 100))
    else:
        show_info(display, str(value), font, (125, 80))"""


def map_coords_calculate(player_x, level_width=2000, map_width=485, map_delta_x=440):
    return int((player_x / level_width) * map_width + map_delta_x)


main(Polygon())
