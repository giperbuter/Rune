from typing import Tuple
import pygame as pg

vec = pg.math.Vector2
g = pg.sprite.Group
obj = pg.sprite.DirtySprite

WIN_WIDTH = 1024
WIN_HEIGHT = 768

class groups(dict):
    def __init__(s, *keys: list[str]):
        for key in keys:
            super().__setitem__(key, g())

    def __getitem__(s, keys):
        if type(keys) == tuple:
            output = []
            for key in keys:
                output.append(super().__getitem__(key))
            return output
        else:
            return super().__getitem__(keys)

triggers = {}
def trigger(key, func):
    triggers[key] = func

groups = groups("all", "update", "player", "ground", "jelly", "particle")
currentPlayer = None

animations = {}