from math import pi
import pygame as pg
from data import *
import data as da
import physics as ph
import render as rd


class Player(pg.sprite.DirtySprite):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "player"])

        s.rdST = rd.RenderState(s, "ghost idle")
        s.rect = pg.Rect(pos.x, pos.y, *s.rdST.getSpriteRect().size)
        s.phST = ph.PhysicsState(s, True, 1, groups["ground", "jelly"],
                                 {"air": -0.7, groups["jelly"]: -0.7})

        s.jumpTimer = 0
        # trigger(pg.K_s, lambda key: s.phST.push(pi/2, 1))  # down
        # trigger(pg.K_w, lambda key: s.phST.push(3*pi/2, 1))  # up

        def left(key):
            if s.phST.onFloor: s.phST.push(0, 1)
            else: s.phST.push(0, 0.5)
        trigger(pg.K_d, left)
        
        def right(key):
            if s.phST.onFloor: s.phST.push(pi, 1)
            else: s.phST.push(pi, 0.5)
        trigger(pg.K_a, right)

        def jump(key):
            if s.phST.onFloor and s.jumpTimer == 0:
                s.phST.push(3*pi/2, 140)
                s.jumpTimer = 4
        trigger(pg.K_SPACE, jump)

    def update(s, dt):
        if s.jumpTimer > 0:
            s.jumpTimer -= dt
            if s.jumpTimer < 0:
                s.jumpTimer = 0
        s.rdST.update(dt)
        s.phST.gravity(vec(0, 1), 1)
        s.phST.update(dt)


class NoLogic(pg.sprite.DirtySprite):
    def __init__(s, pos, groups, animation):
        super().__init__(groups)

        s.rdST = rd.RenderState(s, animation)
        s.rect = pg.Rect(pos.x, pos.y, *s.rdST.getSpriteRect().size)
        s.phST = ph.PhysicsState(s)


class Jelly(pg.sprite.DirtySprite):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "jelly"])

        s.rdST = rd.RenderState(s, "jelly idle")
        s.rect = pg.Rect(pos.x, pos.y, *s.rdST.getSpriteRect().size)
        s.phST = ph.PhysicsState(s, True, 0.1, groups["player", "ground"])

    def update(s, dt):
        s.rdST.update(dt)
        s.phST.gravity(vec(0, 1), 1)
        s.phST.update(dt)
