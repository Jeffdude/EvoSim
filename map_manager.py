import math
import settings

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
    def getColliders(self, bug, direction):
        """
        returns list of sticks intersected by bugs vision vector

        bug: bug object used for point of origin
        direction: the direction of sight (in radians)
        """

        bug_x, bug_y = bug.location
        bug_slope = - math.sin(direction) / math.cos(direction)
        colliders = []
        for stk in self.stick_man.aggregatePoints():

            dx_start = stk.get('start')[0] - bug_x
            dx_stop = stk.get('stop')[0] - bug_x
            if (stk.get('start')[1] > bug_slope * dx_start + bug_y
                and stk.get('stop')[1] < bug_slope * dx_stop + bug_y):
                   # collision into stick with rotation < direction
                   colliders.append(stk.get('stick'))
            elif (stk.get('start')[1] < bug_slope * dx_start + bug_y
                and stk.get('stop')[1] > bug_slope * dx_stop + bug_y):
                   # collision into stick with rotation > direction
                   colliders.append(stk.get('stick'))
        return colliders

    def sightDistance(self, bug, direction):
        """
        bug looks in direction (radians)

        returns a floating point representation of the distance to the nearest
        stick in the bugs vision vector
        """

        bug_x, bug_y = bug.location
        if direction > 0 and direction < 180:
            looking_up = True
        else:
            looking_up = False
        bug_b = bug_y - direction * bug_x # b = y - m*x
        int_pnts = []
        colliders = self.getColliders(bug, direction)
        for stk in colliders:

            # filter the colliders on opposite side of vision
            if stk.location[1] + (stk.length / 2) > bug_y and looking_up:
                continue
            elif stk.location[1] - (stk.length / 2) < bug_y and not looking_up:
                continue

            stk_dict = stk.getDimensions()
            start_x, start_y = stk_dict['start']
            stop_x, stop_y = stk_dict['stop']
            stk_slope = (start_y - stop_y) / (start_x - stop_x)
            stk_b = start_y - stk_slope * start_x  # b = y - m * x
            """
            m1*x + b1 = m2*x + b2
                b2 - b1 = (m1 - m2)x
                x = (b2 - b1)/(m1 - m2)
            (y - b1)/m1 = (y - b2)/m2 
                y - b1 = (y - b2)(m1/m2)
                y - y(m1/m2) = b1 - b2(m1/m2)
                y = (b1 - b2)/(1 - m1/m2) * (m1/m2)
            """
            int_x = (stk_b - bug_b) / (direction - stk_slope)
            int_y = ((stk_b - bug_b) / (1 - direction/stk_slope)) \
                        * (direction / stk_slope)
            int_pnts.append((int(int_x), int(int_y)))
        return (int_pnts, colliders)
