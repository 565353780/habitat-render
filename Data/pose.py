#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.point import Point
from Data.rad import Rad

class Pose(object):
    def __init__(self, position=Point(), rad=Rad()):
        self.position = position
        self.rad = rad
        return

    def setPosition(self, position):
        self.position = position
        return True

    def setRad(self, rad):
        self.rad = rad
        return True

