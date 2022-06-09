#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from math import sqrt, atan2

import habitat_sim
from habitat_sim.utils.common import quat_from_angle_axis

def getRotation(direction):
    up_rotate_rad = atan2(direction[1], direction[0])

    xoy_length = sqrt(direction[0] * direction[0] + direction[1] * direction[1])
    right_rotate_rad = atan2(direction[2], xoy_length)

    up_rotation = quat_from_angle_axis(up_rotate_rad, habitat_sim.geo.UP)
    right_rotation = quat_from_angle_axis(right_rotate_rad, habitat_sim.geo.RIGHT)

    rotation = up_rotation * right_rotation
    return rotation

