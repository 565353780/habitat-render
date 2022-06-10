#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, atan2, pi

import habitat_sim
from habitat_sim.utils.common import quat_from_angle_axis

def getRotationFromRad(up_rotate_rad, right_rotate_rad):
    up_rotation = quat_from_angle_axis(up_rotate_rad, habitat_sim.geo.UP)
    right_rotation = quat_from_angle_axis(right_rotate_rad, habitat_sim.geo.RIGHT)

    rotation = up_rotation * right_rotation
    return rotation

def getRotationFromDirection(direction):
    x, y, z = direction
    zox_length = sqrt(z*z + x*x)

    up_rotate_rad = atan2(x, z) - pi
    right_rotate_rad = atan2(y, zox_length)
    return getRotationFromRad(up_rotate_rad, right_rotate_rad)

