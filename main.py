import pygame
import math
from pygame.locals import *  # for pygame constants
import settings              # access globals
import render                # rendering utils
import time                  # loop timing
from sticks import stick, stick_manager
from bugs import bug, bug_manager
from map_manager import map_manager  # entity management

old_mess = []

special_bug = bug(location=(512,427))
special_direction = 2.356
#0.785
def main():
    # create window
    settings.disp_dim = (1024, 750)
    

    stick_man = stick_manager(density=0.9, max_num=20)
    bug_man = bug_manager()
    settings.map_man = map_manager(stick_man = stick_man,
                                   bug_man = bug_man)
    # spawn initial sticks
    # debug
    special_stk = stick(location=(512, 427),
                    rotation=special_direction, 
                    lspeed=0, rspeed=0, length=1000.0,
                    color=(255,100,100), id=0)
    settings.stk_id += 1

    stick_man.spawnSticks(2)
    stick_man.getSticks().append(special_stk)

    render.initWindow()
    sys_font = pygame.font.SysFont(None, 25)
    settings.fps_surf = sys_font.render("", True, settings.white)
    #settings.disp_dim[1] - fps.get_height()

    fps_clock = pygame.time.Clock()
    settings.screen.fill( settings.black )
    
    settings.fps_dest = (10 , settings.disp_dim[1] - 20)
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
    # debug
    global special_bug
    global special_direction
    (collision_pnts, colliders) = settings.map_man.sightDistance(
                                                    special_bug,
                                                    special_direction)
    special_direction = (special_direction + 0.01) % (2 * math.pi)
    special_stk = settings.map_man.stick_man.getStickById(0)
    special_stk.rotation = special_direction

    settings.map_man.tick()
    settings.screen.fill( settings.black )

    # debug: drawing collision points/debug bug
    render.drawPoints(collision_pnts)
    render.drawPoints([special_bug.location], radias=20, color=settings.red)

    # drawing sticks
    t_sticks = settings.map_man.stick_man.getSticks()
    render.drawSticks( t_sticks )
    # drawing fps display
    settings.screen.blit(settings.fps_surf, settings.fps_dest)

    pygame.display.update()


if __name__ == '__main__':
    main()
    print("~ Quiting")
