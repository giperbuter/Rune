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

triggers = {"key press": {}, "key down": {}, "key up": {}, "mouse move": [], "mouse scroll": []}
# func(key)
def triggerKeyPress(key, func):
    triggers["key press"][key] = func
# func(key)
def triggerKeyDown(key, func):
    triggers["key down"][key] = func
# func(key)
def triggerKeyUp(key, func):
    triggers["key up"][key] = func
# # func(keys: [])
# def triggerKeysPress(keys, func):
#     pass
# # func(keys: [])
# def triggerKeysUp(keys, func):
#     pass
# # func(keys: [])
# def triggerKeysDown(keys, func):
#     pass
# # func(button, pos)
# def mouseClick(button, func):
#     pass
# func(pos: vec(x, y))
def triggerMouseMove(func):
    triggers["mouse move"].append(func)
# func(scroll: vec(x, y))
def triggerMouseScroll(func):
    triggers["mouse scroll"].append(func)
# def collide(obj, group, func): # func(obj, group, side)
#     pass
# def touch(obj, group, func): # func(obj, group, side)
#     pass

groups = groups("all", "update", "player", "ground", "jelly", "particle", "text")
currentPlayer = None

def down(key):
    print("key t down")

def down1(pos):
    print("mouse", pos)


# triggerMouseMove(down1)
triggerKeyDown(pg.K_t, down)

class position(obj):
    def __init__(s, pos):
        s.rect = pg.Rect(pos.x, pos.y, 0, 0)

offsets = {"level": [vec(0, 0), None], "screen": [vec(0, 0), position(vec(0, 0))]}
animations = {}