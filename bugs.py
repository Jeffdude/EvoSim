import random
import settings
from bug_brain import bug_brain
import numpy as np

class bug:
    """
    bug: single bug object for world
    location: (x,y) coordinate of the bug's center
    direction: the direction the bug is facing in radians
    eyes: dict of {id, eye objects} to give the bug
    """
    def __init__(self, location, direction=None, eyes=None, eye_length=250,
            id=None, color=settings.red):
        self.location = location
        self.default_eye_length = eye_length

        if id is None:
            self.id = settings.bug_id
            settings.bug_id += 1
        else:
            self.id = id

        if direction is None:
            self.direction = random.randrange(0,314,2) / 100.0
        else:
            self.direction = direction

        if eyes is None:
            self.eye_count = 1
            new_eye = bug_eye(length=eye_length)
            self.eyes = {0: new_eye}
        else:
            self.eye_count = 0
            self.eyes = {}
            for eye in eyes:
                self.eyes[self.eye_count] = eye
                self.eye_count += 1

        # Initialize the brain with eyes as inputs
        self.brain = bug_brain(
                layer_sizes=[4],
                input_size=self.eye_count,
                output_size=4)   # four basic cardinal directions

    def getBrainInput(self):
        """
        queries the eyes and formats them into a numpy array
        for brain processing
        """

        distances, _, _ = settings.map_man.sightDistances(self)
        inputs = np.zeros((1, self.eye_count))
        for index, eye_id in enumerate(self.eyes.keys()):
            sight = distances[eye_id]
            val = 0
            if sight > 0:
                val = sight / self.eyes[eye_id].length
            inputs[0][index] = val
        return inputs

    def processSituation(self):
        """
        gets input, runs it through the brain, and executes the output
        """
        inputs = self.getBrainInput()
        print("Brain input: {}".format(inputs))
        response = self.brain.process(inputs)
        print("Brain response: {}".format(response))
        direction = response.argmax()
        dirstrings = ["Up", "Down", "Left", "Right"]
        print("Decision: {}".format(dirstrings[direction]))
        actions = [bug.moveUp, bug.moveDown, bug.moveLeft, bug.moveRight]
        actions[direction](self)


    def moveRandom(self, distance=5):
        """
        Bug moves randomly in one of the four cardinal directions
        """
        rand = random.random()
        if rand < 0.25:
            self.moveUp(distance=distance)
        elif rand < 0.5:
            self.moveDown(distance=distance)
        elif rand < 0.75:
            self.moveRight(distance=distance)
        else:
            self.moveLeft(distance=distance)
        self.wrapAround()

    def moveUp(self, distance=5):
        """
        Bug moves up (-y) distance pixels
        """
        self.location = tuple(map(lambda x, y: x + y, self.location,
            (0, -1*distance)))
        self.wrapAround()
        return

    def moveDown(self, distance=5):
        """
        Bug moves down (+y) distance pixels
        """
        self.location = tuple(map(lambda x, y: x + y, self.location,
            (0, 1*distance)))
        self.wrapAround()
        return

    def moveRight(self, distance=5):
        """
        Bug moves right (+x) distance pixels
        """
        self.location = tuple(map(lambda x, y: x + y, self.location,
            (1*distance, 0)))
        self.wrapAround()
        return
    def moveLeft(self, distance=5):
        """
        Bug moves left (-x) distance pixels
        """
        self.location = tuple(map(lambda x, y: x + y, self.location,
            (-1*distance, 0)))
        self.wrapAround()
        return
    
    def wrapAround(self):
        """
        Keep bug inside of display dimensions
        """
        self.location = (self.location[0] % settings.disp_dim[0],
                         self.location[1] % settings.disp_dim[1])

class bug_eye:
    """
    bug_eye: eye object for bugs
    direction: the direction the eye is pointing in radians
    length: the max length of the eye's sight vision
    """
    def __init__(self, direction=None, length=250):
        self.length = length
        if direction is None:
            self.direction = random.randrange(0,314,2) / 100.0
        else:
            self.direction = direction


class bug_manager:
    """
    bug_manager: manages the world bug objects
    """
    def __init__(self, bugs=None):
        """
        init bug_manager

        bugs: list of bug objects to begin with
        """
        self.bugs = []

    def addBug(self, bug):
        """
        add bug to list of managed bugs
        """
        self.bugs.append(bug)
    def getBugs(self):
        return self.bugs

    def tick(self):
        """
        run the bugs' brains
        """
        for bug in self.bugs:
            bug.processSituation()
