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
    def sightDistance(self, bug, direction):
        """
        bug looks in direction

        returns float representing the distance from the bug the nearest
        obstacle is
        """
        bug_x = bug.location[0]
        bug_y = bug.location[1]
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
