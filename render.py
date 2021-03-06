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
    pygame.display.set_caption('EvoSim 1.0')
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
        rect = pygame.draw.line(settings.screen, stk.color, 
                                start, stop, 1)
        dirty_rects.append(rect) 
    return dirty_rects

def drawPoints(coordinates, radias=6, color=settings.yellow):
    """
    helper function for debugging collision points
    coordinate is a list of tuples, (x,y), of points to be drawn
    """
    dirty_rects = []
    for coord in coordinates:
        rect = pygame.draw.circle(settings.screen, color, coord, radias, 0)
        dirty_rects.append(rect)

    return dirty_rects

def drawVisionRay(origin, direction, length, color=settings.red):
    """
    helper function for viewing the bug's vision rays
    origin: a tuple (x,y) of the origin of the vision
    direction: angle of vision in radias
    length: the distance of vision ray
    """
    tip_x = length * math.cos(direction) + origin[0]
    tip_y = origin[1] - length * math.sin(direction) 
    dirty_rect = pygame.draw.line(settings.screen, 
            color, origin, (tip_x, tip_y), 1)
    return [dirty_rect]

def drawBugs(bugs):
    """
    draw all bugs
    bugs: list of bugs to be draw/redrawn
    returns a list of dirty rectangles to be updated
    """
    dirty_rects = []
    for bug in bugs:
        dirty_rects += drawPoints([bug.location], color=settings.red)
        for eye_id in bug.eyes:
            eye = bug.eyes[eye_id]
            dirty_rects += drawVisionRay(bug.location, eye.direction, eye.length)
    return dirty_rects
