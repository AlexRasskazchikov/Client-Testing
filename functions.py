import pygame


def vertical_gradient(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1, height)).convert_alpha()
    dd = 1.0 / height
    sr, sg, sb = startcolor
    er, eg, eb = endcolor
    rm = (er - sr) * dd
    gm = (eg - sg) * dd
    bm = (eb - sb) * dd
    for y in range(height):
        bigSurf.set_at((0, y),
                       (int(sr + rm * y),
                        int(sg + gm * y),
                        int(sb + bm * y)
                        ))
    return pygame.transform.scale(bigSurf, size)


def get_mask(image):
    return pygame.mask.from_surface(image)


def collides(first_mask, second_mask, rect1, rect2):
    """Perfect Pixel Collision Checker"""
    if second_mask is not None:
        offset_x, offset_y = (rect2.left - rect1.left), (rect2.top - rect1.top)
        if first_mask.overlap(second_mask, (offset_x, offset_y)) is not None:
            return True
    return False


def get_rect(image, coords):
    return image.get_rect(top_left=coords)


def get_image(name, dict):
    return dict[name]


def inventory_add_object(player, o):
    names = list(map(lambda x: x.name, player.inventory))

    new = Block(o.img, o.start_hp, type=o.type, name=o.name)

    if o.name not in names:
        player.inventory.append(new)

    for i in range(len(player.inventory)):
        if player.inventory[i].name == o.name:
            player.inventory[i].amount += o.amount
        player.inventory[i].choosen = False
    player.inventory[-1].choosen = True


def collide(player, xvel, yvel, platforms):
    """Check platform collision"""
    for p in platforms:
        if pygame.sprite.collide_rect(player, p):
            if xvel > 0:
                # Colliding Right
                player.rect.right = p.rect.left
                player.yvel -= 1

            if xvel < 0:
                # Colliding Left.
                player.rect.left = p.rect.right
                player.yvel -= 1

            if yvel > 0:
                # Staying on ground.
                player.rect.bottom = p.rect.top
                player.onGround = True
                player.yvel = 0
            if yvel < 0:
                player.rect.top = p.rect.bottom


class Block:
    def __init__(self, img="", hp=10, amount=0, name="Block", type="BackgroundObject"):
        self.img = img
        self.amount = amount
        self.hp = hp
        self.choosen = False
        self.name = name
        self.img = img
        self.icon = img
        self.type = type

    def __iadd__(self, other):
        self.amount += other
        return self.amount

    def __isub__(self, other):
        self.amount -= other
        return self.amount

    def set_choosen(self, bool):
        self.choosen = bool


def show_fps(display, clock, font, coords=(10, 10), color=(0, 0, 0)):
    """This function draws current fps on screen"""
    text = font.render("fps: " + str(int(clock.get_fps())), True, color)
    display.blit(text, coords)


def show_info(display, info, font, coords=(115, 7), color=(255, 255, 255)):
    """This function draws current fps on screen"""
    text = font.render(str(info), True, color)
    display.blit(text, coords)


def encode_parcel(data=[(100, 100), "idle-right:0"]):
    return str(data[0][0]) + ":" + str(data[0][1]) + ";" + data[1]


def decode_parcel(data):
    if data:
        coords, image = data.split(";")
        return list(map(int, coords.split(":"))), image
