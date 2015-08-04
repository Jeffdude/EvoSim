import pygame
from pygame.locals import *  # for pygame constants
import settings              # access globals
import render                # rendering utils
import time                  # loop timing
from sticks import stick, stick_manager

old_mess = []

def main():
    # create window
    settings.disp_dim = (1024, 855)

    # spawn initial sticks
    settings.stick_man = stick_manager()
    settings.stick_man.spawnSticks(2)

    render.initWindow()
    sys_font = pygame.font.SysFont(None, 25)
    settings.fps_surf = sys_font.render("", True, settings.white)
    #settings.disp_dim[1] - fps.get_height()

    fps_clock = pygame.time.Clock()
    settings.screen.fill( settings.black )
    
    settings.fps_dest = (10 ,830)
    settings.screen.blit(settings.fps_surf, settings.fps_dest)
    count = 0
    # main loop
    while True:
        loop()
        fps_clock.tick()
        count += 1
        if count >= 15:
            cur_fps = int(fps_clock.get_fps())
            settings.fps_surf = sys_font.render("fps: " + str(cur_fps), False, settings.white)
            count = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

def loop():
    settings.stick_man.tick()
    t_sticks = settings.stick_man.sticks
    settings.screen.fill( settings.black )
    render.drawSticks( t_sticks )
    settings.screen.blit(settings.fps_surf, settings.fps_dest)
    pygame.display.update()


if __name__ == '__main__':
    main()
    print("~ Quiting")
