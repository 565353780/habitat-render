#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy

from Method.rotations import \
    getDirectionFromRad, getRadFromDirection
from Method.poses import getMovePose, getRotatePose

def getCenterPose(pose, radius):
    rad = deepcopy(pose.rad)

    print("source rad")
    rad.outputInfo()

    direction = getDirectionFromRad(rad)

    print("source direction")
    direction.outputInfo()

    inverse_direction = direction.inverse()

    print("source inverse direction")
    inverse_direction.outputInfo()

    print(" check direction")
    direction.outputInfo()

    inverse_rad_1 = getRadFromDirection(inverse_direction)
    inverse_rad_2 = rad.inverse()

    print("2 inverse:")
    inverse_rad_1.outputInfo()
    inverse_rad_2.outputInfo()

    move_dist = direction.scale(radius)

    center_pose = deepcopy(pose)
    center_pose.position.add(move_dist)
    return center_pose

