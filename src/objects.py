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

        s.rdCO = rd.RenderComponent(s, "ghost idle", offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s, True, 1, groups["ground", "jelly"],
                                     {"air": -0.7, groups["jelly"]: -0.7})

        s.jumpTimer = 0

        # trigger(pg.K_w, lambda key: s.phCO.push(3*pi/2, 1))
        
        def left(key):
            if s.phCO.onFloor:
                s.phCO.push(0, 0.8)
            else:
                s.phCO.push(0, 0.4)
            s.rdCO.setAnimationNoReset(animations["ghost right"])
        triggerKeyPress(pg.K_d, left)

        def right(key):
            if s.phCO.onFloor:
                s.phCO.push(pi, 0.8)
            else:
                s.phCO.push(pi, 0.4)
            s.rdCO.setAnimationNoReset(animations["ghost left"])
        triggerKeyPress(pg.K_a, right)

        def jump(key):
            if s.phCO.onFloor and s.jumpTimer == 0:
                s.jumpTimer = 2
        triggerKeyPress(pg.K_SPACE, jump)

    def update(s, dt):
        # jump
        if s.jumpTimer > 0:
            s.phCO.push(3*pi/2, 2)
            s.jumpTimer -= dt
            if s.jumpTimer < 0:
                s.jumpTimer = 0
        # emit particles
        if abs(s.phCO.vel.x) > 0.3 or abs(s.phCO.vel.y) > 0.3:
            particle(
                vec(ra.randint(s.rect.left, s.rect.right), ra.randint(s.rect.top, s.rect.bottom)), 
                vec(0, 0), ra.uniform(1, 4), (200, 200, 200))
        # animation
        if s.phCO.frc == vec(0, 0):
            s.rdCO.setAnimationNoReset(animations["ghost idle"])
        s.rdCO.update(dt)
        s.phCO.push(pi/2, 1)
        s.phCO.update(dt)


class NoLogic(obj):
    def __init__(s, pos, groups, animation):
        super().__init__(groups)

        s.rdCO = rd.RenderComponent(s, animation, offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s)

class particle(obj):
    def __init__(s, pos, vel, time, color) -> None:
        super().__init__(groups["all", "update", "particle"])
        s.pos = pos
        s.vel = vel
        s.time = time
        s.color = color
        s.rdCO = rd.RenderComponent(s, 0, offsets["level"])
    
    def update(s, dt):
        if s.time < 0:
            s.kill()
        s.pos += s.vel
        s.time -= dt

    def draw(s, screen, scroll):
        pg.draw.circle(screen, s.color, s.pos - scroll, s.time)

class Text(obj):
    def __init__(s, text, font, color, topleft):
        super().__init__(groups["all", "text"])
        s.font = pg.font.SysFont(font, 16)
        s.color = color
        s.pos = topleft
        s.image = s.font.render(text, True, color)
        s.rdCO = rd.RenderComponent(s, 0, "screen")
    
    def set(s, text):
        s.image = s.font.render(text, True, s.color)
    
    def pos(s, pos):
        s.pos = pos
        
    def draw(s, screen, scroll):
        screen.blit(s.image, s.pos)

class Jelly(obj):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "jelly"])

        s.rdCO = rd.RenderComponent(s, "jelly idle", offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCO.getSpriteRect().size)
        s.phCO = ph.PhysicsComponent(s, True, 0.7, groups["player", "ground"])
        
        s.jumpTimer = 0
        
        def right(key):
            if s.phCO.onFloor:
                s.phCO.push(0, 0.4)
            else:
                s.phCO.push(0, 0.2)
        triggerKeyPress(pg.K_RIGHT, right)

        def left(key):
            if s.phCO.onFloor:
                s.phCO.push(pi, 0.4)
            else:
                s.phCO.push(pi, 0.2)
        triggerKeyPress(pg.K_LEFT, left)
        
        def jump(key):
            if s.phCO.onFloor and s.jumpTimer == 0:
                s.jumpTimer = 3
        triggerKeyPress(pg.K_UP, jump)

    def update(s, dt):
        # jump
        if s.jumpTimer > 0:
            s.phCO.push(3*pi/2, 1.4)
            s.jumpTimer -= dt
            if s.jumpTimer < 0:
                s.jumpTimer = 0
        s.rdCO.update(dt)
        s.phCO.push(pi/2, 1)
        s.phCO.update(dt)
