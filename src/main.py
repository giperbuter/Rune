import pygame as pg
from data import *
import data as da
import render as rd
import IO as io

# more triggers - key down key up key press mouse click, object collide with, object collided on top etc...
# dynamic scroll - an object can control if a scroll applies to it and wihch one(game world, ui menu etc)
# text support - object that accepts str as argument and optionaly the images for the lettres, 
#                and other things like width between letters, space width line height text size etc
# sound system - start with research and move from there
# particles - texture and square and polygon support, fix if emitEvery bigger than dt

class Main:
    def __init__(s):
        pg.init()
        s.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        # s.clock = pg.time.Clock()
        s.running = True
        s.elapsed = 1 / 60.0
        # s.dt = 1 / 60.0
        s.currentTime = pg.time.get_ticks() / 100.0
        s.rdSY = rd.RenderSystem()
        io.importLevel("level1.json")
        s.rdSY.focuseObject(da.currentPlayer)
    
    def inputs(s):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                s.running = False
                
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            s.running = False
        for key in triggers:
            if keys[key]:
                triggers[key](key)

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
            
            # dt = (s.clock.get_time() - start) / 1000.0
            # pg.display.set_caption(f"{dt:.2f}")


main = Main()
main.run()
pg.quit()