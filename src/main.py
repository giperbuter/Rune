import pygame as pg
from data import *
import data as da
import render as rd
import IO as io

# physics triggers - collide with group and/or side
# sound system - start with research and move from there
# jelly ai - A*?
# fix collidion - use the one in my notebook(the collsion detection rect is streched from before to after the assignment of the new position seperetly by x and y)

class Main:
    def __init__(s):
        pg.init()
        s.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        s.running = True
        s.elapsed = 1 / 60.0
        s.currentTime = pg.time.get_ticks() / 100.0
        s.rdSY = rd.RenderSystem()
        io.importLevel("level1.json")
    
    def inputs(s):
        for event in pg.event.get():
            # mouse move
            if event.type == pg.MOUSEMOTION:
                for f in triggers["mouse move"]:
                    f(vec(event.pos))
            # mouse move
            if event.type == pg.MOUSEWHEEL:
                for f in triggers["mouse scroll"]:
                    f(vec(event.x, event.y))
            # mouse button down
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button in triggers["mouse button down"]:
                    triggers["mouse button down"][event.button](event.button)
            # mouse button up
            if event.type == pg.MOUSEBUTTONUP:
                if event.button in triggers["mouse button up"]:
                    triggers["mouse button up"][event.button](event.button)
            # key down
            elif event.type == pg.KEYDOWN:
                if event.key in triggers["key down"]:
                    triggers["key down"][event.key](event.key)
            # key up
            elif event.type == pg.KEYUP:
                if event.key in triggers["key up"]:
                    triggers["key up"][event.key](event.key)
            elif event.type == pg.QUIT:
                s.running = False
        # key pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            s.running = False
        for k in triggers["key press"].keys():
            if keys[k]:
                triggers["key press"][k](k)


    def update(s, dt):
        for obj in groups["update"]:
            obj.update(dt)
        s.rdSY.update(dt)

    def run(s):
        while s.running:
            newTime = pg.time.get_ticks() / 100.0
            frameTime = newTime - s.currentTime
            s.currentTime = newTime
            
            while frameTime > 0.0:
                deltaTime = min( frameTime, s.elapsed );
                s.inputs()
                s.update(frameTime)
                frameTime -= deltaTime;
            
            s.screen.fill((0, 0, 0))
            s.rdSY.render(s.screen, groups["all"])
            pg.display.flip()
            # pg.display.set_caption(f"{deltaTime:.2f}")


main = Main()
main.run()
pg.quit()