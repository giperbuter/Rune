from turtle import window_width
import pygame as pg
import os.path as op
from math import copysign, sqrt
from data import *


def importImages(imagePath: list[str], width: int = 48, height: int = 48, colorkey: bool = False):
	images = []
	for path in imagePath:
		image = pg.image.load(op.join("data/images/", path)).convert_alpha()
		if colorkey:
			image.set_colorkey((255, 255, 255))
		images.append(pg.transform.scale(image, (width, height)))
	return images


class Animation:
	def __init__(s, images: list[pg.Surface], rate: float, oneCycle: bool):
		s.images: list(pg.Surface) = images
		s.length: int = len(images)-1
		s.rate: float = rate
		s.oneCycle: bool = oneCycle
		if rate == 0:
			s.noAnimation: bool = True
		else:
			s.noAnimation: bool = False


class RenderComponent:
	def __init__(s, obj, animation):
		s.obj = obj
		s.setAnimation(animation)

	def setAnimation(s, animation):
		s.stopAnimation = False
		s.timePassed = 0
		s.currentTexture = 0
		if type(animation) == str:
			s.animation = animations[animation]
		elif type(animation) == Animation:
			s.animation = animation
		elif type(animation) == int:
			s.animation = "custom"

	def setAnimationNoReset(s, animation):
		if s.currentTexture > len(animation.images):
			raise IndexError("cant set animation because type " +
							 type(animation) + " has fewer images than the current image index")
		if type(animation) == str:
			s.animation = animations[animation]
		elif type(animation) == Animation:
			s.animation = animation

	def getSpriteRect(s):
		return s.animation.images[s.currentTexture].get_rect()

	def update(s, dt):
		if s.animation.noAnimation:
			return
		s.timePassed += dt
		if s.timePassed > s.animation.rate:
			s.timePassed = 0
			s.currentTexture += 1
			if s.currentTexture > s.animation.length:
				if s.animation.oneCycle:
					s.stopAnimation = True
				else:
					s.currentTexture = 0


class RenderSystem:
	def __init__(s):
		s.scroll = vec(0, 0)
		s.focuseObjct = None

		animations["ghost idle"] = Animation(
			importImages(["ghost/idle-1.png"], 40, 54), 0, False)
		animations["ghost left"] = Animation(
			importImages(["ghost/left-1.png"], 40, 54), 0, False)
		animations["ghost right"] = Animation(
			importImages(["ghost/right-1.png"], 40, 54), 0, False)
		animations["jelly idle"] = Animation(importImages(
			["jelly/idle/"+str(i)+".png" for i in range(1, 16)], 32, 32, True), 0.3, False)
		animations["jelly left"] = Animation(importImages(
			["jelly/left/"+str(i)+".png" for i in range(1, 16)], 32, 32, True), 0.2, False)
		animations["jelly right"] = Animation(importImages(
			["jelly/right/"+str(i)+".png" for i in range(1, 16)], 32, 32, True), 0.2, False)
		animations["ground-1"] = Animation(
			importImages(["ground/grass-1.png"]), 0, False)
		animations["ground-2"] = Animation(
			importImages(["ground/grass-2.png"]), 0, False)
		animations["ground-3"] = Animation(
			importImages(["ground/grass-3.png"]), 0, False)
		animations["ground-4"] = Animation(
			importImages(["ground/grass-4.png"]), 0, False)
		animations["ground-5"] = Animation(
			importImages(["ground/grass-5.png"]), 0, False)
		animations["ground-6"] = Animation(
			importImages(["ground/grass+water.png"]), 0, False)
		animations["blank"] = Animation(
			[], 0, False
		)

	def focuseObject(s, obj):
		s.focuseObjct = obj

	def update(s, dt):
		s.scroll.x += (s.focuseObjct.rect.x-s.scroll.x -
					WIN_WIDTH/2+s.focuseObjct.rect.width/2)/4 * dt
		s.scroll.y += (s.focuseObjct.rect.y-s.scroll.y -
					WIN_HEIGHT/2+s.focuseObjct.rect.height/2)/4 * dt

	def render(s, screen, objects):
		for obj in objects:
			if obj.rdCO.animation == "custom":
				obj.draw(screen, s.scroll)
			elif not obj.rdCO.stopAnimation:
				screen.blit(obj.rdCO.animation.images[obj.rdCO.currentTexture], (
					obj.rect.x-s.scroll.x, obj.rect.y-s.scroll.y))
