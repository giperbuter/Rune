from math import cos, sin
import pygame as pg
from data import *

# angle between two vectors in radians:
# acos(v1.normalize().dot(v2.normalize()))


class PhysicsComponent():
  def __init__(s, obj, dynamic = False, mass = 1, collideGroups=[], frictionGroups={"air": -0.7}):
    s.obj = obj
    s.frc = vec(0, 0)
    s.vel = vec(0, 0)
    s.pos = vec(obj.rect.x, obj.rect.y)
    s.mas = mass
    s.dyn = dynamic
    s.onFloor = False
    s.collideGroups = collideGroups
    s.frictionGroups = frictionGroups
    s.collided = []

  def push(s, angle, vel):
    force = vec(0, 0)
    force.y = sin(angle) * vel
    force.x = cos(angle) * vel
    s.frc += vec(force.x+s.frc.x/2, force.y+s.frc.y/2) / s.mas
      
  def pushV(s, vec):
    s.frc += vec
  
  # def gravity(s, dir, strength):
  #   s.frc += dir * strength

  def collide(s):
    s.obj.rect.left = s.pos.x
    for g in s.collideGroups:
      if hits := pg.sprite.spritecollide(s.obj, g, False):
        s.collided.append(g)
        dyn = False
        if hits[0].phCO.dyn:
          s.vel.x = ((hits[0].phCO.mas * hits[0].phCO.vel.x) + (s.mas * s.vel.x)) / (hits[0].phCO.mas + s.mas)
          hits[0].phCO.vel.x = s.vel.x
          dyn = True
        
        if s.vel.x > 0:  # right
          s.obj.rect.right = hits[0].rect.left
          s.pos.x = s.obj.rect.left
          if not dyn:
            s.vel.x = 0
        
        elif s.vel.x < 0:  # left
          s.obj.rect.left = hits[0].rect.right
          s.pos.x = s.obj.rect.left
          if not dyn:
            s.vel.x = 0

     
    s.obj.rect.top = s.pos.y
    for g in s.collideGroups:
      if hits := pg.sprite.spritecollide(s.obj, g, False):
        s.collided.append(g)
        dyn = False
        if hits[0].phCO.dyn:
          s.vel.y = ((hits[0].phCO.mas * hits[0].phCO.vel.y) + (s.mas * s.vel.y)) / (hits[0].phCO.mas + s.mas)
          hits[0].phCO.vel.y = s.vel.y
          dyn = True
     
        if s.vel.y > 0:  # down
          s.obj.rect.bottom = hits[0].rect.top
          s.pos.y = s.obj.rect.top
          if not dyn:
            s.vel.y = 0
          s.onFloor = True
        
        elif s.vel.y < 0:  # down
          s.obj.rect.top = hits[0].rect.bottom
          s.pos.y = s.obj.rect.top
          if not dyn:
            s.vel.y = 0
          
  def friction(s):
    total = []
    for g in s.frictionGroups:
      if g == "air" or g in s.collided:
        total.append(s.frictionGroups[g])
    s.pushV(sum(total)/len(total) * s.vel)  # Ff = mu * N
      
  def update(s, dt):
    s.friction()
    s.vel += s.frc * dt  # v = v0 + a * t
    s.pos += s.vel  # p = p0 + v

    s.onFloor = False
    s.collided = []
    s.collide()

    s.frc = vec(0, 0)
