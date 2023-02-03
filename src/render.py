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
	def __init__(s, obj, animation, offset):
		s.obj = obj
		s.offset = offset
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
		elif type(animation) == int:
			s.animation = "custom"


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

	def update(s, dt):
		for o in offsets.values():
			o[0].x += (o[1].rect.x-o[0].x -
						WIN_WIDTH/2+o[1].rect.width/2) * 0.0075
			o[0].y += (o[1].rect.y-o[0].y -
						WIN_HEIGHT/2+o[1].rect.height/2) * 0.0075

	def render(s, screen, objects):
		for obj in objects:
			if obj.rdCM.animation == "custom":
				obj.draw(screen, obj.rdCM.offset[0])
			elif not obj.rdCM.stopAnimation:
				screen.blit(obj.rdCM.animation.images[obj.rdCM.currentTexture], (
					obj.rect.x-obj.rdCM.offset[0].x, obj.rect.y-obj.rdCM.offset[0].y))
