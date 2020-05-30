from random import randint

import pygame

from functions import collide


class Player():
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.spawn = (x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 3
        self.damage = 10
        self.inventory = []
        self.hp = 100

        self.speed = 30
        self.anim_count = 0
        self.animation_speed = 5
        self.img = "idle-right:0"
        self.hitting = False
        self.anim_id = 1
        self.direction = "right"
        self.xvel, self.yvel = 0, 0
        self.onGround = False
        self.jump = 15
        self.jumped = False

        self.controls = {"up": pygame.K_w, "right": pygame.K_d,
                         "left": pygame.K_a, "hit": pygame.K_SPACE,
                         "speedup": pygame.K_LSHIFT}
        self.inventory_controls = [pygame.K_1,
                                   pygame.K_2,
                                   pygame.K_3,
                                   pygame.K_4,
                                   pygame.K_5]
        self.steam_amount = 100
        self.platforms = []

    def update_frame(self, keys, FramesClock, PACK):
        """Animates player"""
        if "hit" in self.controls and keys[self.controls["hit"]]:
            self.hitting = True
        if self.hitting and PACK:
            if self.anim_count == (
                    PACK.get_len(f"hit{self.anim_id}-{self.direction}") - 1) * self.animation_speed:
                self.anim_count, self.hitting = 0, False
                self.anim_id = randint(1, PACK.get_count("hit"))
            else:
                self.anim_count += 1
                self.set_sprite_from_pack(f"hit{self.anim_id}-{self.direction}",
                                          self.anim_count // self.animation_speed)
        else:
            run_anim_speed = FramesClock // self.animation_speed % PACK.get_len("run-right")
            if "right" in self.controls and keys[self.controls["right"]]:
                self.set_sprite_from_pack("run-right", run_anim_speed)
                self.direction = "right"

            elif "left" in self.controls and keys[self.controls["left"]]:
                self.set_sprite_from_pack("run-left", run_anim_speed)
                self.direction = "left"
            else:
                idle_anim_speed = FramesClock // self.animation_speed // self.animation_speed % PACK.get_len(
                    "idle-right")
                if self.direction == "right":
                    self.set_sprite_from_pack("idle-right", idle_anim_speed)
                else:
                    self.set_sprite_from_pack("idle-left", idle_anim_speed)

    def set_sprite_from_pack(self, name, id):
        self.img = name + ":" + str(id)

    def move(self, keys, platforms):
        """Moves player"""

        for i in range(len(self.inventory_controls)):
            key = self.inventory_controls[i]
            if keys[key]:
                for elem in self.inventory:
                    elem.choosen = False
                if i < len(self.inventory):
                    self.inventory[i].choosen = True

        if "speedup" in self.controls and keys[self.controls["speedup"]]:
            self.speed = 10
            self.hit_animation_speed = 3
        else:
            self.speed = 7
            self.hit_animation_speed = 5

        if "up" in self.controls and keys[self.controls["up"]]:
            if self.steam_amount > 0 and self.rect.y > 0:
                self.yvel = -3
                self.steam_amount -= 0.5
        else:
            if self.steam_amount < 100:
                self.steam_amount += 0.3

        if "left" in self.controls and keys[self.controls["left"]]:
            self.xvel = -self.speed
        if "right" in self.controls and keys[self.controls["right"]]:
            self.xvel = self.speed
        if not self.onGround:
            self.yvel += 0.5
            if self.yvel > 100:
                self.yvel = 100
        if not (keys[self.controls["left"]] or keys[self.controls["right"]]):
            self.xvel = 0
        self.rect.left += self.xvel
        collide(self, self.xvel, 0, platforms)
        self.rect.top += self.yvel
        self.onGround = False
        collide(self, 0, self.yvel, platforms)
        if self.rect.y > 2000:
            self.yvel, self.xvel = 0, 0
            self.rect.x, self.rect.y = self.spawn

    def draw_inventory(self, display, font, sprites, border_color=(50, 50, 50), border_thicness=1, size=64,
                       coords=(600, 10)):

        back_slot = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        back_slot.fill((255, 255, 255, 30))
        back_slot_choosen = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        back_slot_choosen.fill((255, 255, 255, 50))

        w, h = pygame.display.get_surface().get_size()
        for i in range(len(self.inventory)):
            o = self.inventory[i]
            x, y = coords[0] + size * i, -coords[1] + h - size
            half = size // 2

            icon = sprites[o.icon]

            if o.choosen:
                display.blit(back_slot_choosen, (x, y))
                display.blit(icon, (x + 2, y + 2))
                pygame.draw.rect(display, (255, 255, 255), (x, y, size, size), border_thicness)
                text = font.render(str(o.amount), True, (255, 255, 255))
                display.blit(text, (x + half, y + half))
            else:
                display.blit(back_slot, (x, y))
                display.blit(icon, (x + 2, y + 2))
                pygame.draw.rect(display, border_color, (x, y, size, size), border_thicness)
                text = font.render(str(o.amount), True, (255, 255, 255))
                display.blit(text, (x + half, y + half))

    def check_hit(self, object, sprite1, sprite2):
        if self.collides(object, sprite1, sprite2) and self.hitting:
            if not self.hitted:
                self.hitted = True
                return "Hitted!"
        if not self.hitting:
            self.hitted = False

    def collides(self, other, sprite1, sprite2):
        """Perfect Pixel Collision Checker"""
        offset_x, offset_y = (other.rect.left - self.rect.left), (other.rect.top - self.rect.top)
        if self.get_mask(sprite1).overlap(other.get_mask(sprite2), (offset_x, offset_y)) is not None:
            return True

    def get_mask(self, image):
        return pygame.mask.from_surface(image)
