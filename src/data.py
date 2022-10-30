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

triggers = {"key press": []}
def triggerKeyPress(key, func): # func(key)
    triggers[key] = func
def triggerKeyUp(key, func): # func(key)
    pass
def triggerKeyDown(key, func): # func(key)
    pass
def triggerKeysPress(keys, func): # func(keys: [])
    pass
def triggerKeysUp(keys, func): # func(keys)
    pass
def triggerKeysDown(keys, func): # func(keys)
    pass
def mouseClick(button, func): # func(button, pos)
    pass
def mouseHover(obj, func): # func(obj, pos)
    pass
def mouseHoverClick(obj, button, func): # func(obj, pos, button)
    pass
def mouseScroll(func): # func(obj, pos, scroll)
    pass
def mouseHoverScroll(obj, func): # func(obj, pos, scroll)
    pass
def collide(obj, group, func): # func(obj, group, side)
    pass
def touch(obj, group, func): # func(obj, group, side)
    pass

groups = groups("all", "update", "player", "ground", "jelly", "particle", "text")
currentPlayer = None

class position(obj):
    def __init__(s, pos):
        s.rect = pg.Rect(pos.x, pos.y, 0, 0)

offsets = {"level": [vec(0, 0), None], "screen": [vec(0, 0), position(vec(0, 0))]}
animations = {}