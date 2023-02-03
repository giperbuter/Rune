from math import pi
import random as ra
import pygame as pg
from data import *
import data as da
import physics as ph
import render as rd


class Player(obj):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "player"])

        s.rdCM = rd.RenderComponent(s, "ghost idle", offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCM.getSpriteRect().size)
        s.phCM = ph.PhysicsComponent(s, True, 1, groups["ground", "jelly"],
                                     {"air": -0.7, groups["jelly"]: -0.7})

        s.velText = Text("player velocity", "Comic Sans MS", WHITE, (10, 10))
        s.jumpTimer = 0
        s.setTrigers()

    def setTrigers(s):
        def left(key):
            if s.phCM.onFloor:
                s.phCM.push(0, 0.8)
            else:
                s.phCM.push(0, 0.4)
            s.rdCM.setAnimationNoReset(animations["ghost right"])
        triggerOnKeyPress(pg.K_d, left)

        def right(key):
            if s.phCM.onFloor:
                s.phCM.push(pi, 0.8)
            else:
                s.phCM.push(pi, 0.4)
            s.rdCM.setAnimationNoReset(animations["ghost left"])
        triggerOnKeyPress(pg.K_a, right)

        def jump(key):
            if s.phCM.onFloor and s.jumpTimer == 0:
                s.jumpTimer = 2
        triggerOnKeyPress(pg.K_SPACE, jump)

    def update(s, dt):
        # jump
        if s.jumpTimer > 0:
            s.phCM.push(3*pi/2, 2)
            s.jumpTimer -= dt
            if s.jumpTimer < 0:
                s.jumpTimer = 0
        # emit particles
        if abs(s.phCM.vel.x) > 0.3 or abs(s.phCM.vel.y) > 0.3:
            Particle(
                vec(ra.randint(s.rect.left, s.rect.right),
                    ra.randint(s.rect.top, s.rect.bottom)),
                vec(0, 0), ra.uniform(1, 4), (200, 200, 200))
        # animation
        if s.phCM.frc == vec(0, 0):
            s.rdCM.setAnimationNoReset(animations["ghost idle"])
        s.rdCM.update(dt)
        s.phCM.push(pi/2, 1)
        s.phCM.update(dt)
        s.velText.set(f"Player: {s.phCM.vel.x:.4f}" +
                      " " + f"{s.phCM.vel.y:.4f}")


class NoLogic(obj):
    def __init__(s, pos, groups, animation):
        super().__init__(groups)

        s.rdCM = rd.RenderComponent(s, animation, offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCM.getSpriteRect().size)
        s.phCM = ph.PhysicsComponent(s)


class Particle(obj):
    def __init__(s, pos, vel, time, color) -> None:
        super().__init__(groups["all", "update", "particle"])
        s.pos = pos
        s.vel = vel
        s.time = time
        s.color = color
        s.rdCM = rd.RenderComponent(s, 0, offsets["level"])

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
        s.rdCM = rd.RenderComponent(s, 0, offsets["level"])

    def set(s, text):
        s.image = s.font.render(text, True, s.color)

    def pos(s, pos):
        s.pos = pos

    def draw(s, screen, scroll):
        screen.blit(s.image, s.pos)


class Jelly(obj):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "jelly"])

        s.rdCM = rd.RenderComponent(s, "jelly idle", offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.rdCM.getSpriteRect().size)
        s.phCM = ph.PhysicsComponent(s, True, 0.7, groups["player", "ground"])

        s.jumpTimer = 0
        s.velText = Text("jelly velocity", "Comic Sans MS", WHITE, (10, 40))
        s.setTriggers()

    def setTriggers(s):
        def right(key):
            if s.phCM.onFloor:
                s.phCM.push(0, 0.4)
            else:
                s.phCM.push(0, 0.2)
        triggerOnKeyPress(pg.K_RIGHT, right)

        def left(key):
            if s.phCM.onFloor:
                s.phCM.push(pi, 0.4)
            else:
                s.phCM.push(pi, 0.2)
        triggerOnKeyPress(pg.K_LEFT, left)

        def jump(key):
            if s.phCM.onFloor and s.jumpTimer == 0:
                s.jumpTimer = 3
        triggerOnKeyPress(pg.K_UP, jump)

    def update(s, dt):
        # jump
        if s.jumpTimer > 0:
            s.phCM.push(3*pi/2, 1.4)
            s.jumpTimer -= dt
            if s.jumpTimer < 0:
                s.jumpTimer = 0
        s.rdCM.update(dt)
        s.phCM.push(pi/2, 1)
        s.phCM.update(dt)
        s.velText.set(f"Jelly:   {s.phCM.vel.x:.4f}" +
                      " " + f"{s.phCM.vel.y:.4f}")
