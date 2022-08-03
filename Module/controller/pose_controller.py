#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.point import Point

from Config.input_map import INPUT_KEY_DICT

from Method.poses import \
    getMoveForwardPose, getMoveLeftPose, \
    getMoveRightPose, getMoveBackwardPose, \
    getMoveUpPose, getMoveDownPose, \
    getTurnLeftPose, getTurnRightPose, \
    getTurnUpPose, getTurnDownPose, \
    getHeadLeftPose, getHeadRightPose

from Module.controller.base_pose_controller import BasePoseController

class PoseController(BasePoseController):
    def __init__(self):
        super(PoseController, self).__init__()
        return

    def moveForward(self, move_dist):
        self.pose = getMoveForwardPose(self.pose, move_dist)
        return True

    def moveLeft(self, move_dist):
        self.pose = getMoveLeftPose(self.pose, move_dist)
        return True

    def moveRight(self, move_dist):
        self.pose = getMoveRightPose(self.pose, move_dist)
        return True

    def moveBackward(self, move_dist):
        self.pose = getMoveBackwardPose(self.pose, move_dist)
        return True

    def moveUp(self, move_dist):
        self.pose = getMoveUpPose(self.pose, move_dist)
        return True

    def moveDown(self, move_dist):
        self.pose = getMoveDownPose(self.pose, move_dist)
        return True

    def turnLeft(self, rotate_angle):
        self.pose = getTurnLeftPose(self.pose, rotate_angle)
        return True

    def turnRight(self, rotate_angle):
        self.pose = getTurnRightPose(self.pose, rotate_angle)
        return True

    def turnUp(self, rotate_angle):
        self.pose = getTurnUpPose(self.pose, rotate_angle)
        return True

    def turnDown(self, rotate_angle):
        self.pose = getTurnDownPose(self.pose, rotate_angle)
        return True

    def headLeft(self, rotate_angle):
        self.pose = getHeadLeftPose(self.pose, rotate_angle)
        return True

    def headRight(self, rotate_angle):
        self.pose = getHeadRightPose(self.pose, rotate_angle)
        return True

def demo():
    position = Point(2.7, 1.5, -3.0)
    look_at = Point(1.0, 0.5, -5.5)
    move_direction = Point(1.0, 1.0, 3.0)

    pose_controller = PoseController()

    pose = pose_controller.getPoseByLookAt(position, look_at)
    pose.outputInfo()

    agent_state = pose_controller.getAgentStateByAgentLookAt(position, look_at)
    agent_state = pose_controller.getAgentStateFromAgentLookAt(look_at, move_direction)

    input_key_list = INPUT_KEY_DICT.keys()
    for input_key in input_key_list:
        agent_state = pose_controller.getAgentStateByKey(input_key)
    return True

