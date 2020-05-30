import random
from copy import copy

import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, coords=(50, 50), size=(148, 200), speed=5, jump=15,
                 animation=None, damage=10, hp=100,
                 controls={"up": pygame.K_w, "right": pygame.K_d,
                           "left": pygame.K_a, "hit": pygame.K_SPACE},
                 sounds=["Assets/sounds/hit/hit1.mp3",
                         "Assets/sounds/hit/hit2.mp3",
                         "Assets/sounds/hit/hit3.mp3",
                         "Assets/sounds/hit/hit4.mp3"]):
        Entity.__init__(self)
        self.inventory = []
        self.sounds = sounds
        self.width, self.height = size
        self.coords = coords
        self.start_coords = coords
        self.xvel, self.yvel = 0, 0
        self.onGround = False
        self.controls = controls
        self.anim_count, self.hitting = 0, False
        self.animation = animation
        self.hit_animation_speed = 5
        self.walk_animation_speed = 5
        self.idle_animation_speed = 5
        self.anim_id = 1
        self.direction = "right"
        self.speed = speed
        self.jump = jump
        self.hitted = False
        self.img = ""

        self.damage = damage
        self.hp = hp
        self.start_hp = hp
        self.inventory_controls = [pygame.K_1,
                                   pygame.K_2,
                                   pygame.K_3,
                                   pygame.K_4,
                                   pygame.K_5]

        if self.animation is not None:
            self.img = pygame.transform.scale(self.animation[list(self.animation.get_sets_names())[0]][0],
                                              (self.width, self.height))
            self.rect = self.img.get_rect(topleft=self.coords)
            self.mask = pygame.mask.from_surface(self.img)
            self.hitted_image = copy(self.img)
            self.hitted_image.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)

    def set_sprite_from_pack(self, name, index):
        """Change player's sprite to sprite from Pack"""
        if self.animation:
            self.img = pygame.transform.scale(self.animation.get_frame(name, index), (self.width, self.height))
        else:
            pass

    def update_frame(self, keys, FramesClock):
        """Animates player"""
        if "hit" in self.controls and keys[self.controls["hit"]]:
            self.hitting = True
        if self.hitting and self.animation:
            if self.anim_count == (
                    self.animation.get_len(f"hit{self.anim_id}-{self.direction}") - 1) * self.hit_animation_speed:
                self.anim_count, self.hitting = 0, False
                self.anim_id = random.randint(1, self.animation.get_count("hit"))
            else:
                self.anim_count += 1
                self.set_sprite_from_pack(f"hit{self.anim_id}-{self.direction}",
                                          self.anim_count // self.hit_animation_speed)
        else:
            run_anim_speed = FramesClock // self.walk_animation_speed % self.animation.get_len("run-right")
            if "right" in self.controls and keys[self.controls["right"]]:
                self.set_sprite_from_pack("run-right", run_anim_speed)
                self.direction = "right"

            elif "left" in self.controls and keys[self.controls["left"]]:
                self.set_sprite_from_pack("run-left", run_anim_speed)
                self.direction = "left"
            else:
                idle_anim_speed = FramesClock // self.idle_animation_speed // self.walk_animation_speed % self.animation.get_len(
                    "idle-right")
                if self.direction == "right":
                    self.set_sprite_from_pack("idle-right", idle_anim_speed)
                else:
                    self.set_sprite_from_pack("idle-left", idle_anim_speed)

    def update(self, keys, platforms):
        """Moves player"""
        if not self.hitting:

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
                if self.onGround:
                    self.yvel -= self.jump
            if "left" in self.controls and keys[self.controls["left"]]:
                self.xvel = -self.speed
            if "right" in self.controls and keys[self.controls["right"]]:
                self.xvel = self.speed
            if "reset" in self.controls and keys[self.controls["reset"]]:
                self.set_coords(self.start_coords)
            if not self.onGround:
                self.yvel += 0.5
                if self.yvel > 100:
                    self.yvel = 100
            if not (keys[self.controls["left"]] or keys[self.controls["right"]]):
                self.xvel = 0
            self.rect.left += self.xvel
            self.collide(self.xvel, 0, platforms)
            self.rect.top += self.yvel
            self.onGround = False
            self.collide(0, self.yvel, platforms)
            self.mask = pygame.mask.from_surface(self.img)

    def collide(self, xvel, yvel, platforms):
        """Check platform collision"""
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    # Colliding Right
                    self.rect.right = p.rect.left

                if xvel < 0:
                    # Colliding Left.
                    self.rect.left = p.rect.right

                if yvel > 0:
                    # Staying on ground.
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    def set_coords(self, coords, start=False):
        """Change player Position. If start - + set start coords"""
        if start:
            self.start_coords = coords
        self.rect = self.img.get_rect(topleft=(coords))

    def collides(self, other):
        """Perfect Pixel Collision Checker"""
        if other is not None:
            offset_x, offset_y = (other.rect.left - self.rect.left), (other.rect.top - self.rect.top)
            if self.mask.overlap(other.mask, (offset_x, offset_y)) is not None:
                return True
        return False

    def update_mask(self):
        self.hitted_image = copy(self.img)
        self.hitted_image.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)
        self.mask = pygame.mask.from_surface(self.img)

    def draw_mask(self, display, color=(255, 255, 255)):
        pygame.draw.lines(display, color, 1, self.mask.outline())

    def check_hit(self, object):
        if self.collides(object) and self.hitting and object.is_active():
            if not self.hitted:
                self.hitted = True
                return f"Hitted {object.name}!"
        if not self.hitting:
            self.hitted = False

    def inventory_add_object(self, o):
        names = list(map(lambda x: x.name, self.inventory))

        new = Block(o.mat, o.img, o.start_hp, type=o.type, name=o.name, )

        if o.name not in names:
            self.inventory.append(new)

        for i in range(len(self.inventory)):
            if self.inventory[i].name == o.name:
                self.inventory[i].amount += o.amount
            self.inventory[i].choosen = False
        self.inventory[-1].choosen = True

    def draw_inventory(self, display, font, border_color=(50, 50, 50), border_thicness=1, size=64, coords=(600, 10)):

        back_slot = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        back_slot.fill((255, 255, 255, 30))
        back_slot_choosen = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        back_slot_choosen.fill((255, 255, 255, 50))

        w, h = pygame.display.get_surface().get_size()
        for i in range(len(self.inventory)):
            o = self.inventory[i]
            x, y = coords[0] + size * i, -coords[1] + h - size
            half = size // 2

            if o.choosen:
                display.blit(back_slot_choosen, (x, y))
                display.blit(o.icon, (x + 2, y + 2))
                pygame.draw.rect(display, (255, 255, 255), (x, y, size, size), border_thicness)
                text = font.render(str(o.amount), True, (255, 255, 255))
                display.blit(text, (x + half, y + half))
            else:
                display.blit(back_slot, (x, y))
                display.blit(o.icon, (x + 2, y + 2))
                pygame.draw.rect(display, border_color, (x, y, size, size), border_thicness)
                text = font.render(str(o.amount), True, (255, 255, 255))
                display.blit(text, (x + half, y + half))


class Block:
    def __init__(self, img="none", hp=10, amount=0, name="Block", type="BackgroundObject"):
        self.img = img
        self.amount = amount
        self.hp = hp
        self.choosen = False
        self.name = name
        self.img = img
        self.icon = pygame.transform.scale(img, (60, 60))
        self.type = type

    def unpack(self, TEXTURE_DICT):
        self.img = TEXTURE_DICT[self.name]
        self.icon = pygame.transform.scale(self.img, (60, 60))

    def __iadd__(self, other):
        self.amount += other
        return self.amount

    def __isub__(self, other):
        self.amount -= other
        return self.amount

    def set_choosen(self, bool):
        self.choosen = bool
