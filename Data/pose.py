#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.point import Point
from Data.rad import Rad

class Pose(object):
    def __init__(self, position=Point(), rad=Rad()):
        self.position = position
        self.rad = rad

        self.scale = [1.0, 1.0, 1.0]
        return

    def setPosition(self, position):
        self.position = position
        return True

    def setRad(self, rad):
        self.rad = rad
        return True

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level

        print(line_start + "[Pose]")
        self.position.outputInfo(info_level + 1)
        self.rad.outputInfo(info_level + 1)
        return True

