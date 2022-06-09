#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import atan2

import habitat_sim
from habitat_sim.utils.common import \
    quat_from_angle_axis, quat_rotate_vector

def getRotation(direction):
    up_rotate_angle = atan2(direction[1], direction[0])
    right_rotate_angle = atan2(direction[2], direction[0])

    up_rotation = quat_from_angle_axis(up_rotate_angle, habitat_sim.geo.UP)
    right_rotation = quat_from_angle_axis(right_rotate_angle, habitat_sim.geo.RIGHT)

    rotation = up_rotation * right_rotation
    return rotation

