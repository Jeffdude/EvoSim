import pygame
from pygame.locals import *  # TODO figure out if this is necessary
import settings  # access globals
from sticks import stick, stick_manager
import matplotlib.pyplot as plt
import math
# ------------------------------------------------------------------------------
# Setting up the window
# ------------------------------------------------------------------------------


def initWindow(fullscreen=False):
    """
    Set up pygame window
    default to windowed mode
    """
    if settings.debug:
        print("~ Initializing pygame window")
    pygame.init()
    pygame.display.set_caption('Parcae')
    dispInfo = pygame.display.Info()
    if settings.debug > 1:
        print(">   Available Height: {}".format(dispInfo.current_h))
        print(">   Available Width: {}".format(dispInfo.current_w))
    dispStyle = 0
    if(fullscreen):
        if settings.DEBUG:
            print("~ Pygame window is fullscreen")
        dispStyle = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        settings.disp_dim = (dispInfo.current_h, dispInfo.current_w)
    settings.screen = pygame.display.set_mode(settings.disp_dim, dispStyle)
    settings.screen.set_alpha(None)
    settings.screen.fill(settings.black)
    if settings.debug:
        print("~ Done initializing pygame window")

# ------------------------------------------------------------------------------
# Rendering and helper functions
# ------------------------------------------------------------------------------

def drawSticks(sticks, color=settings.white):
    """
    draw sticks takes a list of sticks to be drawn or redrawn and returns a list
    of dirty rectangles to be updated
    """
    dirty_rects = []
    for stk in sticks:
        stk_info = stk.getDimensions()
        start = stk_info.get('start')
        stop = stk_info.get('stop')
        rect = pygame.draw.line(settings.screen, settings.white, 
                                start, stop, 1)
        dirty_rects.append(rect) 
    return dirty_rects
