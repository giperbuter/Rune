from math import cos, sin
import pygame as pg
from data import *

# angle between two vectors in radians:
# acos(v1.normalize().dot(v2.normalize()))


class PhysicsComponent():
	def __init__(s, obj, dynamic=False, mass=1, collideGroups=[], frictionGroups={"air": -4}):
		s.obj = obj
		s.mas = mass
		s.dynamic = dynamic
		s.collideGroups = collideGroups
		s.frictionGroups = frictionGroups
		s.forces = vec(0, 0)
		s.velocity = vec(0, 0)
		s.position = vec(obj.rect.x, obj.rect.y)
		s.collided = []
		s.collidedGroups = []
		s.triggers = {}

	# func(obj, group, side)
	# side: 0-any 1-top 2-right 3-bottom 4-left
	def trigger(s, group, side, func):
		s.triggers[[group, side]] = func

	def push(s, angle, velocity):
		force = vec(0, 0)
		force.y = sin(angle) * velocity
		force.x = cos(angle) * velocity
		s.forces += vec(force.x, force.y) / s.mas

	def pushV(s, vec):
		s.forces += vec

	def collide(s):
		s.obj.rect.left = s.position.x
		for g in s.collideGroups:
			if hits := pg.sprite.spritecollide(s.obj, g, False):
				s.collided.append(g)
				dynamic = False
				if hits[0].physicsComponent.dynamic:
					s.velocity.x = ((hits[0].physicsComponent.mas * hits[0].physicsComponent.velocity.x) + (
						s.mas * s.velocity.x)) / (hits[0].physicsComponent.mas + s.mas)
					hits[0].physicsComponent.velocity.x = s.velocity.x
					dynamic = True

				if s.velocity.x > 0:  # right
					s.obj.rect.right = hits[0].rect.left
					s.position.x = s.obj.rect.left
					if not dynamic:
						s.velocity.x = 0

				elif s.velocity.x < 0:  # left
					s.obj.rect.left = hits[0].rect.right
					s.position.x = s.obj.rect.left
					if not dynamic:
						s.velocity.x = 0

		s.obj.rect.top = s.position.y
		for g in s.collideGroups:
			if hits := pg.sprite.spritecollide(s.obj, g, False):
				s.collided.append(g)
				dynamic = False
				if hits[0].physicsComponent.dynamic:
					s.velocity.y = ((hits[0].physicsComponent.mas * hits[0].physicsComponent.velocity.y) + (
						s.mas * s.velocity.y)) / (hits[0].physicsComponent.mas + s.mas)
					hits[0].physicsComponent.velocity.y = s.velocity.y
					dynamic = True

				if s.velocity.y > 0:  # down
					s.obj.rect.bottom = hits[0].rect.top
					s.position.y = s.obj.rect.top
					if not dynamic:
						s.velocity.y = 0
					s.onFloor = True

				elif s.velocity.y < 0:  # down
					s.obj.rect.top = hits[0].rect.bottom
					s.position.y = s.obj.rect.top
					if not dynamic:
						s.velocity.y = 0

	def friction(s):
		total = []
		for g in s.frictionGroups:
			if g == "air" or g in s.collided:
				total.append(s.frictionGroups[g])
		return sum(total)/len(total) * s.velocity  # Ff = mu * N

	def update(s, dt):
		s.forces += s.friction()
		s.velocity += s.forces * dt  # v = v0 + a * t
		s.position += s.velocity  # p = p0 + v
		s.collided.clear()
		s.collide()
		s.forces = vec(0, 0)
