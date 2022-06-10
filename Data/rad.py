#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class Rad(object):
    def __init__(self, up_rotate_rad=0.0, right_rotate_rad=0.0):
        self.up_rotate_rad = up_rotate_rad
        self.right_rotate_rad = right_rotate_rad
        return

    def toList(self):
        point_list = [self.up_rotate_rad, self.right_rotate_rad]
        return point_list

    def toArray(self):
        point_list = self.toList()
        point_array = np.array(point_list, dtype=np.float32)
        return point_array

    def outputInfo(self, info_level):
        line_start = "\t" * info_level

        print(line_start + "[Rad]")
        print(line_start + "\t up_rotate_angle = " + \
              str(np.rad2deg(self.up_rotate_rad)))
        print(line_start + "\t right_rotate_angle = " + \
              str(np.rad2deg(self.right_rotate_rad)))
        return True

