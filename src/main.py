import pygame as pg
from data import *
import data as da
import render as rd
import IO as io

# call pos once at the end and the create func is created before it depending on the type(with default error type)
#{"type": "text", "pos": {"pos": [10, 10], "grid": false}, "text": "hello world!", "font": "Comic Sans MS", "color": [255, 255, 255]},
# physics triggers - collide with group and/or side
# sound system - start with research and move from there
# jelly ai - A*?
# fix collidion - use the one in my notebook(the collsion detection rect is streched from before to after the assignment of the new position seperetly by x and y)

class Main:
    def __init__(s):
        pg.init()
        s.screen = pg.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        s.running = True
        s.renderSystem = rd.RenderSystem()
        io.importLevel("level1.json")
        triggerOnKeyPress(pg.K_ESCAPE, lambda k: s.stop())

    def stop(s):
        s.running = False

    def inputs(s):
        while event := pg.event.poll():
            if event.type in onEvent.keys():
                [call(event) for call in onEvent[event.type]]
            if event.type == pg.QUIT:
                s.stop()

        keys = pg.key.get_pressed()
        for k in onKeyPress.keys():
            if keys[k]:
                [call(k) for call in onKeyPress[k]]

    def update(s, dt):
        for obj in groups["update"]:
            obj.update(dt)
        s.renderSystem.update(dt)

    def run(s):
        clock = pg.time.Clock()
        while s.running:
            s.inputs()
            s.update(1 / 60)
            pg.display.set_caption(f"{clock.get_fps()}")
            
            s.screen.fill((0, 0, 0))
            s.renderSystem.render(s.screen, groups["all"])
            pg.display.flip()
            
            clock.tick(60)


main = Main()
main.run()
pg.quit()
