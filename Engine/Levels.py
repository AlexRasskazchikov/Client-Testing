import pygame

from Engine.Tiles import Entity

cell_height = 50

pygame.init()


class Level:
    def __init__(self):
        self.map = []
        self.materials = {}
        self.total_level_width = 0
        self.total_level_height = 0
        self.background = (0, 0, 0)
        self.background_objects = []
        self.lighting = False

    def set_map(self, map):
        self.map = map
        self.total_level_width = len(self.map[0]) * cell_height
        self.total_level_height = len(self.map) * cell_height

    def render_files(self):
        platforms = []
        x = y = 0
        for row in self.map:
            for col in row:
                if col in self.materials:
                    p = BackgroundObject(image=self.materials[col],
                                         coords=(x, y),
                                         name=col, act=True, hp=10, type="Platform")
                    p.rect = pygame.Rect(x, y, cell_height, cell_height)
                    platforms += [p]
                x += cell_height
            y += cell_height
            x = 0
        return platforms

    def add_background_object(self, *other):
        self.background_objects += other

    def __eq__(self, other):
        return self.map == other.map


class BackgroundObject(Entity):
    def __init__(self, image, coords, size=None, name="Unknown", hp=100, act=True, amount=1,
                 type="BackgroundObject"):
        super().__init__()
        self.name = name
        self.img = image
        self.coords = coords
        if size is not None:
            self.size = (int(cell_height * size[0]), int(cell_height * size[1]))
        self.collidable = True
        self.amount = amount
        self.type = type
        self.hp, self.start_hp = hp, hp

        self.act = act

    def __eq__(self, other):
        return self.name == other.name and self.coords == other.coords

    def move(self, deltax, deltay):
        self.coords = (self.coords[0] + deltax, self.coords[1] + deltay)
        self.rect = self.img.get_rect(topleft=self.coords)
        self.mask = pygame.mask.from_surface(self.img)

    def __iadd__(self, other):
        self.hp += other

    def __isub__(self, other):
        self.hp -= other

    def is_active(self):
        return self.act

    def set_active(self, bool):
        self.act = bool


def Plain():
    """Plain level"""
    Plain = Level()
    Plain.set_map([
        "                                                                                        ",
        "                                                                                        ",
        "                                                                                        ",
        "                                                                                        ",
        "                                                                                        ",
        "                                                                                        ",
        "                                                                                     LGG",
        "                                                                                     PPP",
        "                                                                                    LPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "                                                                                    PPPP",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
    ])

    Plain.materials = {"G": "ground",
                       "L": "left",
                       "R": "right",
                       "P": "earth"}

    Plain.background = (105, 169, 204)
    Plain.spawn = (1000, 900)
    return Plain


def LightDemo():
    LightDemo = Level()
    LightDemo.lighting = True
    LightDemo.set_map([
        "                                                        ",
        "                                                        ",
        "                                                        ",
        "PPPGGGGR                                                ",
        "PPPPPPPPGGGGR                                       PPPP",
        "PPPPPPPPPPPPPGGR                                    PPPP",
        "PPPPPPPPPPPPPPPPGR                                  PPPP",
        "PPPPPPPPPPPPPPPPPPGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ])

    ground = pygame.image.load(r"Assets/Tiles/Tile_02.bmp")
    right = pygame.image.load(r"Assets/Tiles/Tile_03.bmp")
    left = pygame.image.load(r"Assets/Tiles/Tile_01.bmp")
    earth = pygame.image.load(r"Assets/Tiles/Tile_14.bmp")
    """earth = pygame.Surface((cell_height, cell_height))
    earth.fill((91, 49, 56))"""

    LightDemo.materials = {"G": ground,
                           "P": earth,
                           "L": left,
                           "R": right}
    return LightDemo


def Polygon():
    Polygon = Level()
    Polygon.set_map([
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                 wwwww                                                                                                                         ",
        "PPPPPPPPPPPPPPPP                wwwwwww                                                                                                                        ",
        "G  G  G  G  PGGPPP             wwwwwwwww                                                                                                                       ",
        "  G  G  G  GPGGPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        " G  G  G  G PGGPPG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   GGG G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G",
        "G  G  G  G  PGGPG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G GGG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G ",
        "  G  G  G  GPGGP   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G  GG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G  ",
        " G  G  G  G PGGP  G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   GG  G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   ",
        "G  G  G  G  PGGP G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   GGG G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G",
        "  G  G  G  GPGGPG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G GGG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G ",
        " G  G  G  G PGGP   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G  GG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G  ",
        "G  G  G  G  PGGP  G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   GG  G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   ",
    ])

    ground = pygame.Surface((cell_height, cell_height))
    ground.fill((125, 125, 125))
    construct = pygame.Surface((cell_height, cell_height))
    construct.fill((156, 156, 159))

    Polygon.materials = {"G": "construct",
                         "P": "ground"}

    Polygon.background = (105, 169, 204)
    Polygon.spawn = (464, 750)
    return Polygon
