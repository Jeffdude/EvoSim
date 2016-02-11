import math
import time
import settings
import render

class map_manager:
    """
    Monitors interactions b/w sticks and bugs
    
    in charge of bugs senses and of killing them after collisions
    """

    def __init__(self, stick_man, bug_man):
        self.stick_man = stick_man
        self.bug_man = bug_man

    def tick(self):
        self.stick_man.tick()
        #self.bug_man.tick()

    def drawWorld(self):
        """
        aggregation function to draw all the the bugs
        and sticks of the world
        """
        render.drawSticks(self.stick_man.getSticks())
        render.drawBugs(self.bug_man.getBugs())

    def getColliders(self, bug, direction, getId=False):
        """
        returns list of sticks intersected by bugs vision vector

        bug: bug object used for point of origin
        direction: the direction of sight (in radians)
        """

        bug_x, bug_y = bug.location
        bug_slope = - math.tan(direction)
        colliders = []
        colliders_id = []
        for stk_id in self.stick_man.aggregatePoints():

            # retrieve stk info by unique identifier
            stk = self.stick_man.aggregatePoints()[stk_id]

            dx_start = stk.get('start')[0] - bug_x
            dx_stop = stk.get('stop')[0] - bug_x
            if (stk.get('start')[1] > bug_slope * dx_start + bug_y
                and stk.get('stop')[1] < bug_slope * dx_stop + bug_y):
                   # collision into stick with rotation < direction
                   if getId:
                       colliders_id.append(stk_id)
                   else:
                       colliders.append(stk.get('stick'))
            elif (stk.get('start')[1] < bug_slope * dx_start + bug_y
                and stk.get('stop')[1] > bug_slope * dx_stop + bug_y):
                   # collision into stick with rotation > direction
                   if getId:
                       colliders_id.append(stk_id)
                   else:
                       colliders.append(stk.get('stick'))

        if getId:
            return colliders_id
        else:
            return colliders

    def sightDistance(self, bug, direction):
        """
        bug looks in direction (radians)

        returns a floating point representation of the distance to the nearest
        stick in the bugs vision vector
        """

        bug_x, bug_y = bug.location
        v_slope = - math.tan(direction) 

        if direction > 0 and direction < math.pi:
            looking_up = True
        else:
            looking_up = False

        if ((direction < (math.pi / 2.0) and direction >= 0)
            or (direction <= (2 * math.pi) 
                and direction > ((3.0 * math.pi) / 2.0))):
            looking_right = True
        else:
            looking_right = False

        bug_b = bug_y - v_slope * bug_x # b = y - m*x
        int_pnts = []
        stk_details = self.stick_man.aggregatePoints()
        colliders_id = self.getColliders(bug, direction, getId=True)
        for stk_id in colliders_id:

            stk_dict = stk_details[stk_id]
            stk = stk_dict['stick']

            # filter the colliders on opposite side of vision
            if ((stk.location[1] - stk_dict['height']) > bug_y 
                    and looking_up):
                continue # skip
            elif (stk.location[1] + stk_dict['height']) < bug_y and not looking_up:
                continue # skip

            # skip debug stick
            if stk_id is 0:
                continue

            start_x, start_y = stk_dict['start']
            stop_x, stop_y = stk_dict['stop']
            stk_slope = float(start_y - stop_y) / float(start_x - stop_x)
            stk_b = start_y - stk_slope * start_x  # b = y - m * x
            """
            insections of vision and stick

            m1*x + b1 = m2*x + b2
                b2 - b1 = (m1 - m2)x
                x = (b2 - b1)/(m1 - m2)
            """
            int_x = float(stk_b - bug_b) / float(v_slope - stk_slope)
            int_y = bug_b + v_slope * int_x
            #int_y = stk_b + stk_slope * int_x
            int_pnts.append((int(int_x), int(int_y)))
        new_pnts = []
        for pnt_x, pnt_y in int_pnts:
            if (((pnt_y > bug_y) and looking_up)
                or ((pnt_y < bug_y) and not looking_up)
                or ((pnt_x < bug_x) and looking_right)
                or ((pnt_x > bug_x) and not looking_right)):
                    continue
            new_pnts.append((pnt_x, pnt_y))
        return (new_pnts, colliders_id)
