#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import pi
import numpy as np

from Data.rad import Rad

from Method.rotations import getDirectionFromRad

def getForwardDirection(pose):
    forward_rad = Rad(pose.rad.up_rotate_rad, 0.0)
    forward_direction = getDirectionFromRad(forward_rad)
    return forward_direction

def getLeftDirection(pose):
    left_rad = Rad(pose.rad.up_rotate_rad + pi / 2.0, 0.0)
    left_direction = getDirectionFromRad(left_rad)
    return left_direction

def getRightDirection(pose):
    right_rad = Rad(pose.rad.up_rotate_rad - pi / 2.0, 0.0)
    right_direction = getDirectionFromRad(right_rad)
    return right_direction

def getBackwardDirection(pose):
    backward_rad = Rad(pose.rad.up_rotate_rad + pi, 0.0)
    backward_direction = getDirectionFromRad(backward_rad)
    return backward_direction

def getUpDirection():
    up_rad = Rad(0.0, np.deg2rad(90.0))
    up_direction = getDirectionFromRad(up_rad)
    return up_direction

def getDownDirection():
    down_rad = Rad(0.0, np.deg2rad(-90.0))
    down_direction = getDirectionFromRad(down_rad)
    return down_direction

def getMovePose(pose, move_direction, move_dist):
    new_pose = pose
    move_point = move_direction.scale(move_dist)
    new_pose.position.add(move_point)
    return new_pose

def getMoveForwardPose(pose, move_dist):
    move_direction = getForwardDirection(pose)
    return getMovePose(pose, move_direction, move_dist)

def getMoveLeftPose(pose, move_dist):
    move_direction = getLeftDirection(pose)
    return getMovePose(pose, move_direction, move_dist)

def getMoveRightPose(pose, move_dist):
    move_direction = getRightDirection(pose)
    return getMovePose(pose, move_direction, move_dist)

def getMoveBackwardPose(pose, move_dist):
    move_direction = getBackwardDirection(pose)
    return getMovePose(pose, move_direction, move_dist)

def getMoveUpPose(pose, move_dist):
    move_direction = getUpDirection()
    return getMovePose(pose, move_direction, move_dist)

def getMoveDownPose(pose, move_dist):
    move_direction = getDownDirection()
    return getMovePose(pose, move_direction, move_dist)

def getRotatePose(pose, up_rotate_angle, right_rotate_angle):
    new_pose = pose
    rotate_rad = Rad(
        np.deg2rad(up_rotate_angle),
        np.deg2rad(right_rotate_angle))
    new_pose.rad.add(rotate_rad)
    return new_pose

def getTurnLeftPose(pose, rotate_angle):
    return getRotatePose(pose, rotate_angle, 0.0)

def getTurnRightPose(pose, rotate_angle):
    return getRotatePose(pose, -rotate_angle, 0.0)

def getTurnUpPose(pose, rotate_angle):
    return getRotatePose(pose, 0.0, rotate_angle)

def getTurnDownPose(pose, rotate_angle):
    return getRotatePose(pose, 0.0, -rotate_angle)

