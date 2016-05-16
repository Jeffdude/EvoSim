import random
import settings

class bug:
    """
    bug: single bug object for world
    location: (x,y) coordinate of the bug's center
    direction: the direction the bug is facing in radians
    eyes: list of eye objects to give the bug
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
