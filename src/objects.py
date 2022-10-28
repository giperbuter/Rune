from math import pi, cos, sin
import random as ra
import pygame as pg
from data import *
import data as da
import physics as ph
import render as rd


class Player(obj):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "player"])

        s.rdCO = rd.RenderComponent(s, "ghost idle")
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s, True, 1, groups["ground", "jelly"],
                                     {"air": -0.7, groups["jelly"]: -0.7})

        s.jumpTimer = 0

        def left(key):
            if s.phCO.onFloor:
                s.phCO.push(0, 0.6)
            else:
                s.phCO.push(0, 0.3)
        trigger(pg.K_d, left)

        def right(key):
            if s.phCO.onFloor:
                s.phCO.push(pi, 0.6)
            else:
                s.phCO.push(pi, 0.3)
        trigger(pg.K_a, right)

        def jump(key):
            if s.phCO.onFloor and s.jumpTimer == 0:
                s.jumpTimer = 2
        trigger(pg.K_SPACE, jump)

    def update(s, dt):
        if s.jumpTimer > 0:
            s.phCO.push(3*pi/2, 1.3)
            s.jumpTimer -= dt
            if s.jumpTimer < 0:
                s.jumpTimer = 0
        if abs(s.phCO.vel.x) > 0.3 or abs(s.phCO.vel.y) > 0.3:
            particle(
                vec(ra.randint(s.rect.left, s.rect.right), ra.randint(s.rect.top, s.rect.bottom)), 
                vec(0, 0), ra.uniform(1, 4), (200, 200, 200))
        s.rdCO.update(dt)
        s.phCO.push(pi/2, 1)
        s.phCO.update(dt)


class NoLogic(obj):
    def __init__(s, pos, groups, animation):
        super().__init__(groups)

        s.rdCO = rd.RenderComponent(s, animation)
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s)

class particle(obj):
    def __init__(s, pos, vel, time, color) -> None:
        super().__init__(groups["all", "update", "particle"])
        s.pos = pos
        s.vel = vel
        s.time = time
        s.color = color
        s.rdCO = rd.RenderComponent(s, 0)
    
    def update(s, dt):
        if s.time < 0:
            s.kill()
        s.pos += s.vel
        s.time -= dt

    def draw(s, screen, scroll):
        pg.draw.circle(screen, s.color, s.pos - scroll, s.time)

class Jelly(obj):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "jelly"])

        s.rdCO = rd.RenderComponent(s, "jelly idle")
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s, True, 0.1, groups["player", "ground"])

    def update(s, dt):
        s.rdCO.update(dt)
        s.phCO.push(3*pi/2, 1)
        s.phCO.update(dt)
