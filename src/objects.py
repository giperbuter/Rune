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

        s.renderComponent = rd.RenderComponent(
            s, "ghost idle", offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.renderComponent.getSpriteRect().size)
        s.physicsComponent = ph.PhysicsComponent(s, True, 1, groups["ground", "jelly"],
                                                 {"air": -4, groups["jelly"]: -7})

        s.velText = Text("player velocity", "Comic Sans MS", WHITE, (10, 10))
        s.jumpTimer = 0
        s.setTrigers()

    def setTrigers(s):
        def left(key):
            s.physicsComponent.push(0, 100)
            s.renderComponent.setAnimationNoReset(animations["ghost right"])
        triggerOnKeyPress(pg.K_d, left)

        def right(key):
            s.physicsComponent.push(pi, 100)
            s.renderComponent.setAnimationNoReset(animations["ghost left"])
        triggerOnKeyPress(pg.K_a, right)

        def jump(key):
            if s.jumpTimer <= 0:
                s.jumpTimer = 0.2
        triggerOnKeyPress(pg.K_SPACE, jump)
        triggerOnEvent(pg.MOUSEBUTTONDOWN, jump)

    def update(s, dt):
        # jump
        if s.jumpTimer > 0:
            s.physicsComponent.push(3*pi/2, 200)
            s.jumpTimer -= dt
        # emit particles
        if abs(s.physicsComponent.velocity.x) > 3 or abs(s.physicsComponent.velocity.y) > 3:
            Particle(
                vec(ra.randint(s.rect.left, s.rect.right),
                    ra.randint(s.rect.top, s.rect.bottom)),
                vec(0, 0), ra.uniform(0.5, 1.5), (200, 200, 200))
        # animation
        if s.physicsComponent.forces == vec(0, 0):
            s.renderComponent.setAnimationNoReset(animations["ghost idle"])
        s.renderComponent.update(dt)
        s.physicsComponent.push(pi/2, 100)
        s.physicsComponent.update(dt)
        s.velText.set(f"Player: {s.physicsComponent.velocity.x:.4f}" +
                      " " + f"{s.physicsComponent.velocity.y:.4f}")


class NoLogic(obj):
    def __init__(s, pos, groups, animation):
        super().__init__(groups)

        s.renderComponent = rd.RenderComponent(s, animation, offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.renderComponent.getSpriteRect().size)
        s.physicsComponent = ph.PhysicsComponent(s)


class Particle(obj):
    def __init__(s, pos, vel, time, color) -> None:
        super().__init__(groups["all", "update", "particle"])
        s.pos = pos
        s.vel = vel
        s.time = time
        s.color = color
        s.renderComponent = rd.RenderComponent(s, 0, offsets["level"])

    def update(s, dt):
        if s.time < 0:
            s.kill()
        s.pos += s.vel
        s.time -= dt

    def draw(s, screen, scroll):
        pg.draw.circle(screen, s.color, s.pos - scroll, s.time * 3)


class Text(obj):
    def __init__(s, text, font, color, topleft):
        super().__init__(groups["all", "text"])
        s.font = pg.font.SysFont(font, 16)
        s.color = color
        s.pos = topleft
        s.image = s.font.render(text, True, color)
        s.renderComponent = rd.RenderComponent(s, 0, offsets["level"])

    def set(s, text):
        s.image = s.font.render(text, True, s.color)

    def pos(s, pos):
        s.pos = pos

    def draw(s, screen, scroll):
        screen.blit(s.image, s.pos)


class Jelly(obj):
    def __init__(s, pos):
        super().__init__(groups["all", "update", "jelly"])

        s.renderComponent = rd.RenderComponent(
            s, "jelly idle", offsets["level"])
        s.rect = pg.Rect(pos.x, pos.y, *s.renderComponent.getSpriteRect().size)
        s.physicsComponent = ph.PhysicsComponent(
            s, True, 0.7, groups["player", "ground"])

        s.jumpTimer = 0
        s.velText = Text("jelly velocity", "Comic Sans MS", WHITE, (10, 40))
        s.setTriggers()

    def setTriggers(s):
        def right(key):
            s.physicsComponent.push(0, 50)
        triggerOnKeyPress(pg.K_RIGHT, right)

        def left(key):
            s.physicsComponent.push(pi, 50)
        triggerOnKeyPress(pg.K_LEFT, left)

        def jump(key):
            if s.jumpTimer <= 0:
                s.jumpTimer = 0.1
        triggerOnKeyPress(pg.K_UP, jump)

    def update(s, dt):
        if s.jumpTimer > 0:
            s.physicsComponent.push(3*pi/2, 250)
            s.jumpTimer -= dt
            
        s.renderComponent.update(dt)
        s.physicsComponent.push(pi/2, 100)
        s.physicsComponent.update(dt)
        s.velText.set(f"Jelly:   {s.physicsComponent.velocity.x:.4f}" +
                      " " + f"{s.physicsComponent.velocity.y:.4f}")
