from math import pi
import pygame as pg
from data import *
import data as da
import physics as ph
import render as rd


class Player(pg.sprite.DirtySprite):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "player"])

        s.rdCO = rd.RenderState(s, "ghost idle")
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s, True, 1, groups["ground", "jelly"],
                                 {"air": -0.7, groups["jelly"]: -0.7})

        s.jumpTimer = 0
        # trigger(pg.K_s, lambda key: s.phCO.push(pi/2, 1))  # down
        # trigger(pg.K_w, lambda key: s.phCO.push(3*pi/2, 1))  # up

        def left(key):
            if s.phCO.onFloor: s.phCO.push(0, 1)
            else: s.phCO.push(0, 0.5)
        trigger(pg.K_d, left)
        
        def right(key):
            if s.phCO.onFloor: s.phCO.push(pi, 1)
            else: s.phCO.push(pi, 0.5)
        trigger(pg.K_a, right)

        def jump(key):
            if s.phCO.onFloor and s.jumpTimer == 0:
                s.phCO.push(3*pi/2, 140)
                s.jumpTimer = 4
        trigger(pg.K_SPACE, jump)

    def update(s, dt):
        if s.jumpTimer > 0:
            s.jumpTimer -= dt
            if s.jumpTimer < 0:
                s.jumpTimer = 0
        s.rdCO.update(dt)
        s.phCO.gravity(vec(0, 1), 1)
        s.phCO.update(dt)


class NoLogic(pg.sprite.DirtySprite):
    def __init__(s, pos, groups, animation):
        super().__init__(groups)

        s.rdCO = rd.RenderState(s, animation)
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s)


class Jelly(pg.sprite.DirtySprite):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "jelly"])

        s.rdCO = rd.RenderState(s, "jelly idle")
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s, True, 0.1, groups["player", "ground"])

    def update(s, dt):
        s.rdCO.update(dt)
        s.phCO.gravity(vec(0, 1), 1)
        s.phCO.update(dt)
