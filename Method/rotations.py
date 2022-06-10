#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, atan2, pi

import habitat_sim
from habitat_sim.utils.common import quat_from_angle_axis

from Data.rad import Rad

def getRadFromDirection(direction):
    x, y, z = direction.toList()
    zox_length = sqrt(z*z + x*x)

    up_rotate_rad = atan2(x, z) - pi
    right_rotate_rad = atan2(y, zox_length)

    rad = Rad(up_rotate_rad, right_rotate_rad)
    return rad

def getRotationFromRad(rad):
    up_rotate_rad, right_rotate_rad = rad.toList()

    up_rotation = quat_from_angle_axis(up_rotate_rad, habitat_sim.geo.UP)
    right_rotation = quat_from_angle_axis(right_rotate_rad, habitat_sim.geo.RIGHT)

    rotation = up_rotation * right_rotation
    return rotation

def getDirectionFromRad(rad):
    rotation = getRotationFromRad(rad)
    direction = rotation * [0.0, 0.0, 1.0]
    return direction

def getRotationFromDirection(direction):
    rad = getRadFromDirection(direction)
    rotation = getRotationFromRad(rad)
    return rotation

