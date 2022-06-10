#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from math import sqrt

class Point(object):
    def __init__(self, x=0, y=0, z=0):
        '''
        Input:
            [x, y, z] -> ZXY world
        '''
        self.x = x
        self.y = y
        self.z = z
        return

    def getNorm(self):
        norm2 = self.x * self.x + self.y * self.y + self.z * self.z
        return sqrt(norm2)

    def toList(self):
        point_list = [self.x, self.y, self.z]
        return point_list

    def toArray(self):
        point_list = self.toList()
        point_array = np.array(point_list, dtype=np.float32)
        return point_array

