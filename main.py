import pygame
import math
from pygame.locals import *  # for pygame constants
import settings              # access globals
import render                # rendering utils
import time                  # loop timing
from sticks import stick, stick_manager
from bugs import bug, bug_eye, bug_manager
from map_manager import map_manager  # entity management

old_mess = []

special_eyes = []
for n in range(2):
    eye = bug_eye()
    special_eyes.append(eye)
special_bug = bug(location=(512,427), eyes=special_eyes)
#special_direction = special_bug.eyes['0'].direction
#special_direction = 2.356
#0.785
def main():
    # create window
    settings.disp_dim = (1024, 750)
    

    stick_man = stick_manager(density=0.9, max_num=20)
    bug_man = bug_manager()
    bug_man.addBug(special_bug)
    settings.map_man = map_manager(stick_man = stick_man,
                                   bug_man = bug_man)
    # spawn initial sticks
    # debug
    #special_stk = stick(location=(512, 427),
    #                rotation=special_direction, 
    #                lspeed=0, rspeed=0, length=1000.0,
    #                color=(255,100,100), id=0)
    #settings.stk_id += 1

    stick_man.spawnSticks(2)
    #stick_man.getSticks().append(special_stk)

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
        # for fps clock
        fps_clock.tick()
        count += 1
        if count >= 15:
            cur_fps = int(fps_clock.get_fps())
            settings.fps_surf = sys_font.render("fps: " + str(cur_fps), False, settings.white)
            count = 0
        # quit event 
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

def loop():
    """
    main loop of program execution
    """
    # debug
    global special_bug

    # first update the object locations
    settings.map_man.tick()
    settings.screen.fill( settings.black )
    sb0_direction = special_bug.eyes[0].direction 
    sb1_direction = special_bug.eyes[1].direction 

    distance, new_pnts, _ = settings.map_man.sightDistances(special_bug)

    # rotate vision
    special_bug.eyes[0].direction += 0.01 
    special_bug.eyes[0].direction %= (2 * math.pi)
    special_bug.eyes[1].direction -= 0.01 
    special_bug.eyes[1].direction %= (2 * math.pi)

    # debug: drawing collision points/debug bug
    render.drawPoints(new_pnts)

    # drawing bugs
    bugs = settings.map_man.bug_man.getBugs()
    render.drawBugs(bugs)
    # drawing sticks
    t_sticks = settings.map_man.stick_man.getSticks()
    render.drawSticks( t_sticks )
    # drawing fps display
    settings.screen.blit(settings.fps_surf, settings.fps_dest)

    pygame.display.update()


if __name__ == '__main__':
    main()
    print("~ Quiting")
