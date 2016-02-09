import random


class bug:
    """
    bug: single bug object for world
    location: (x,y) coordinate of the bug's center
    """
    def __init__(self, location):
        self.location = location


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

    def addBug(bug):
        """
        add bug to list of managed bugs
        """
        self.bugs.append(bug)
