import settings
import random
import math

class stick:
    def __init__(self, location=None, rotation=None, lspeed=None, rspeed=None,
                 max_length=130.0, min_length=80.0, length=None, color=None,
                 id=None):
        if location is None:
            edgebuf = max_length / 2.0
            min_loc = edgebuf
            max_loc = settings.disp_dim[0] - edgebuf
            self.location = (random.randrange(int(min_loc), int(max_loc), 1), 0.0)
        else:
            self.location = location

        # linear velocity
        if lspeed is None:
            random.seed()
            self.lspeed = 0.8 + random.random() * 2.0
        else:
            self.lspeed = lspeed

        # rotational velocity
        if rspeed is None:
            random.seed()
            self.rspeed = random.random() * 0.015
        else:
            self.rspeed = rspeed

        if rotation is None:
            self.rotation = random.randrange(0, 314, 2) / 100.0
        else:
            self.rotation = rotation

        if length is None:
            self.length = random.randrange(min_length * 5, max_length * 5, 2) / 5.0
        else:
            self.length = length

        if color is None:
            self.color = settings.white
        else:
            self.color = color

        self.dim_dict = None

        # stick unique identifier
        if id is None:
            self.id = settings.stk_id
            settings.stk_id += 1
        else:
            self.id = id
    
    def tick(self):
        self.dim_dict = None
        new_height = self.location[1] + self.lspeed
        self.rotation = self.rotation + self.rspeed
        if new_height <= settings.disp_dim[1]:
            self.location = (self.location[0], new_height)
            return True
        else:
            return False

    def getDimensions(self):
        """
        returns a dictionary of helpful information
            caveat: moderately high constant time computation
            note: will only recompute once per tick

        height: the absolute height along the y-axis
        width: the absolute width along the x-axis
        start: tuple of coordinates of the highest end of the stick
        stop: tuple of coordinates of the lowest end of the stick
        """
        if self.dim_dict is None:
            height = (self.length / 2.0) * math.sin(self.rotation)
            width = (self.length / 2.0) * math.cos(self.rotation)
            if width < 0:
                width = abs(width)
                start = (self.location[0] - width,
                          self.location[1] - height)
                stop = (self.location[0] + width,
                          self.location[1] + height)
            else:
                start = (self.location[0] + width,
                          self.location[1] - height)
                stop = (self.location[0] - width,
                          self.location[1] + height)
            self.dim_dict = {'height': height, 'width': width, 
                            'start': start, 'stop': stop}
        return self.dim_dict


class stick_manager:

    def __init__(self, density=0.3, max_num=12, min_num=2):
        self.max_num = max_num
        self.min_num = min_num
        self.probability = density / 10.0
        self.sticks = []
        self.pointMap = None

        random.seed()
        self.randState = random.getstate()

    def tick(self):
        random.setstate(self.randState)
        num_sticks = len(self.sticks)
        if num_sticks >= self.max_num:
            pass
        elif num_sticks < self.min_num:
            self.spawnSticks(2)
        else:
            coin = random.random()
            if coin < self.probability:
                self.spawnSticks(1)

        doomed = []
        if self.sticks is not None:
            for stk in self.sticks:
                if not stk.tick():
                    doomed.append(stk)
        for stk in doomed:
            self.sticks.remove(stk)

        # save random state
        self.randState = random.getstate()
        # reset detail cache
        self.pointMap = None

    def aggregatePoints(self):

        if self.pointMap is None:
            self.pointMap = {}
            for stk in self.sticks:
                dims = stk.getDimensions()
                data = {'start': dims.get('start'), 
                        'stop': dims.get('stop'),
                        'height': dims.get('height'),
                        'width': dims.get('width'),
                        'stick': stk }
                self.pointMap[stk.id] = data

        return self.pointMap


    def spawnSticks(self, num_sticks):
        if num_sticks <= 0:
            print("= Can't spawn {} sticks".format(num_sticks))
            return
        for x in range(num_sticks):
            new_stick = stick()
            self.sticks.append(new_stick)
        if settings.debug > 2 and False:
            if num_sticks > 1:
                s_char = 's'
            else:
                s_char = ''
            print(">>  Spawned {} stick{}".format(num_sticks, s_char))

    def getSticks(self):
        return self.sticks

    def getStickById(self, id):
        return self.aggregatePoints()[id]['stick']
