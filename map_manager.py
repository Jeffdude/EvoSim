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
        bug_slope = - math.tan(direction)
        colliders = []
        for stk_id in self.stick_man.aggregatePoints():

            # retrieve stk info by unique identifier
            stk = self.stick_man.aggregatePoints()[stk_id]

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
        v_slope = - math.tan(direction) 
        if v_slope < 0:
            looking_up = True
        else:
            looking_up = False
        """
        if direction > 0 and direction < math.pi:
            looking_up = True
        else:
            looking_up = False
        """
        bug_b = bug_y - v_slope * bug_x # b = y - m*x
        int_pnts = []
        stk_details = self.stick_man.aggregatePoints()
        colliders = self.getColliders(bug, direction)
        for stk in colliders:

            # filter the colliders on opposite side of vision
            if (stk.location[1] + (stk.length / 2)) > bug_y and looking_up:
                continue # skip
            elif (stk.location[1] - (stk.length / 2)) < bug_y and not looking_up:
                continue # skip

            stk_dict = stk_details[stk.id]
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
        return (int_pnts, colliders)
