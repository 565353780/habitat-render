#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, atan2, pi

import habitat_sim
from habitat_sim.utils.common import quat_from_angle_axis

def getRotation(direction):
    x, y, z = direction
    up_rotate_rad = atan2(x, z) - pi

    zox_length = sqrt(z*z + x*x)
    right_rotate_rad = atan2(y, zox_length)

    up_rotation = quat_from_angle_axis(up_rotate_rad, habitat_sim.geo.UP)
    right_rotation = quat_from_angle_axis(right_rotate_rad, habitat_sim.geo.RIGHT)

    rotation = up_rotation * right_rotation
    return rotation

