from typing import List
import pygame as pg

vec = pg.math.Vector2
g = pg.sprite.Group
obj = pg.sprite.DirtySprite

WIN_WIDTH = 1024
WIN_HEIGHT = 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

onEvent = {}
def triggerOnEvent(event, call):
    if event in onEvent.keys():
        onEvent[event].append(call)
    else:
        onEvent[event] = [call]

onKeyPress = {}
def triggerOnKeyPress(key, call):
    if key in onKeyPress.keys():
        onKeyPress[key].append(call)
    else:
        onKeyPress[key] = [call]

# triggers = {"key press": {}, "key down": {}, "key up": {}, "mouse move": [], "mouse scroll": [], "mouse button up": {}, "mouse button down": {}}
# # func(key)
# def triggerKeyPress(key, func):
#     triggers["key press"][key] = func
# # func(key)
# def triggerKeyDown(key, func):
#     triggers["key down"][key] = func
# # func(key)
# def triggerKeyUp(key, func):
#     triggers["key up"][key] = func
# # func(button)
# def triggerMouseButtonDown(button, func):
#     triggers["mouse button down"][button] = func
# # func(button)
# def triggerMouseButtonUp(button, func):
#     triggers["mouse button up"][button] = func
# # func(pos: vec(x, y))
# def triggerMouseMove(func):
#     triggers["mouse move"].append(func)
# # func(scroll: vec(x, y))
# def triggerMouseScroll(func):
#     triggers["mouse scroll"].append(func)

groups = groups("all", "update", "player", "ground", "jelly", "particle", "text")
currentPlayer = None

class position(obj):
    def __init__(s, pos):
        s.rect = pg.Rect(pos.x, pos.y, 0, 0)

offsets = {"level": [vec(0, 0), None], "screen": [vec(0, 0), position(vec(0, 0))]}
animations = {}