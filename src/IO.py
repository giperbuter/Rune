import pygame as pg
from math import pi
import os.path as op
import json
from data import *
import data as da
import objects as ob
import random as ra

def importLevel(path):
	level = json.load(open(op.join("data/json/", path)))
	for o in level:
		# get pos
		def pos(call):
			if len(o["pos"]["pos"]) == 2:
				if o["pos"]["grid"]:
					call(vec(o["pos"]["pos"][0], o["pos"]["pos"][1]) * 48)
				else:
					call(vec(o["pos"]["pos"]))
			elif len(o["pos"]["pos"]) == 4:
				for x in range(min(o["pos"]["pos"][0],o["pos"]["pos"][2]), max(o["pos"]["pos"][0],o["pos"]["pos"][2])+1):
					for y in range(min(o["pos"]["pos"][1],o["pos"]["pos"][3]), max(o["pos"]["pos"][1],o["pos"]["pos"][3])+1):
						if o["pos"]["grid"]:
							call(vec(x, y) * 48)
						else:
							call(vec(x, y))
			else:
				call(vec(0))
					
		# player
		if o["type"] == "player":
			def call(pos):
				pl = ob.Player(pos)
				offsets["level"][0].x = pos.x  - WIN_WIDTH/2+pl.rect.width/2
				offsets["level"][0].y = pos.y - WIN_HEIGHT/2+pl.rect.height/2
				print(pos)
			pos(call)
			if o["main"]:
				offsets["level"][1] = groups["player"].sprites()[-1]

		# jelly
		elif o["type"] == "jelly":
			pos(lambda pos : ob.Jelly(pos))

		# ground
		elif o["type"] == "ground":
			def create(pos):
				if o["sprite"] == "random":
					ob.NoLogic(pos, groups["all", "ground"], animations["ground-"+str(ra.randint(1, 6))])
				elif 1 <= int(o["sprite"]) <= 5:
					ob.NoLogic(pos, groups["all", "ground"], animations["ground-"+int(o["sprite"])])
				else:
					ob.NoLogic(pos, groups["all", "ground"], animations["ground-1"])
			pos(create)
   
		elif o["type"] == "text":
			def create(pos):
				ob.Text(o["text"], o["font"], o["color"], pos)
			pos(create)