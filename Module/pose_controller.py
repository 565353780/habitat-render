#!/usr/bin/env python
# -*- coding: utf-8 -*-

from habitat_sim import AgentState

from Config.input_map import INPUT_KEY_DICT
from Config.init_pose import INIT_POSE

from Data.point import Point
from Data.pose import Pose

from Method.rotations import \
    getDirectionFromRad, getRadFromDirection, \
    getRotationFromRad, getRotationFromDirection

from Method.poses import \
    getMoveForwardPose, getMoveLeftPose, \
    getMoveRightPose, getMoveBackwardPose, \
    getMoveUpPose, getMoveDownPose, \
    getTurnLeftPose, getTurnRightPose, \
    getTurnUpPose, getTurnDownPose, \
    getHeadLeftPose, getHeadRightPose

class PoseController(object):
    def __init__(self):
        self.input_key_dict = INPUT_KEY_DICT
        self.input_key_list = self.input_key_dict.keys()
        self.move_func_dict = {
            "move_forward": self.moveForward,
            "move_left": self.moveLeft,
            "move_right": self.moveRight,
            "move_backward": self.moveBackward,
            "move_up": self.moveUp,
            "move_down": self.moveDown,
        }
        self.rotate_func_dict = {
            "turn_left": self.turnLeft,
            "turn_right": self.turnRight,
            "turn_up": self.turnUp,
            "turn_down": self.turnDown,
            "head_left": self.headLeft,
            "head_right": self.headRight,
        }
        self.move_func_list = self.move_func_dict.keys()
        self.rotate_func_list = self.rotate_func_dict.keys()

        self.pose = INIT_POSE
        return

    def reset(self):
        self.input_key_dict = INPUT_KEY_DICT
        self.input_key_list = self.input_key_dict.keys()

        self.pose = INIT_POSE
        return True

    def resetPose(self):
        self.pose = INIT_POSE
        return True

    def getDirectionFromRad(self, rad):
        return getDirectionFromRad(rad)

    def getRadFromDirection(self, direction):
        return getRadFromDirection(direction)

    def getRotationFromRad(self, rad):
        return getRotationFromRad(rad)

    def getRotationFromDirection(self, direction):
        return getRotationFromDirection(direction)

    def getPoseByLookAt(self, position, look_at):
        direction_x = look_at.x - position.x
        direction_y = look_at.y - position.y
        direction_z = look_at.z - position.z
        direction = Point(direction_x, direction_y, direction_z)
        rad = getRadFromDirection(direction)
        pose = Pose(position, rad)
        return pose

    def getAgentStateFromPose(self, pose):
        agent_state = AgentState()
        agent_state.position = pose.position.toArray()
        agent_state.rotation = getRotationFromRad(pose.rad)
        return agent_state

    def getInitAgentState(self):
        return self.getAgentStateFromPose(INIT_POSE)

    def getAgentStateByAgentLookAt(self, position, look_at):
        pose = self.getPoseByLookAt(position, look_at)
        return self.getAgentStateFromPose(pose)

    def getAgentStateFromAgentLookAt(self, look_at, move_direction):
        position_x = look_at.x - move_direction.x
        position_y = look_at.y - move_direction.y
        position_z = look_at.z - move_direction.z
        position = Point(position_x, position_y, position_z)
        return self.getAgentStateByAgentLookAt(position, look_at)

    def getAgentState(self):
        return self.getAgentStateFromPose(self.pose)

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

    def getAgentStateByKey(self,
                           input_key,
                           move_dist=0.0,
                           rotate_angle=0.0):
        if input_key not in self.input_key_list:
            print("[WARN][PoseController::getAgentStateByKey]")
            print("\t input_key not valid!")
            return self.getAgentState()

        action = self.input_key_dict[input_key]
        if action in self.move_func_list:
            self.move_func_dict[action](move_dist)
            return self.getAgentState()
        if action in self.rotate_func_list:
            self.rotate_func_dict[action](rotate_angle)
            return self.getAgentState()

        print("[WARN][PoseController::getAgentStateByKey]")
        print("\t action not valid!")
        return self.getAgentState()

def demo():
    position = Point(2.7, 1.5, -3.0)
    direction = Point(1.0, 0.0, 0.0)
    look_at = Point(1.0, 0.5, -5.5)
    move_direction = Point(1.0, 1.0, 3.0)

    pose_controller = PoseController()

    direction.outputInfo()

    rad = pose_controller.getRadFromDirection(direction)
    rad.outputInfo()

    pose = pose_controller.getPoseByLookAt(position, look_at)
    pose.outputInfo()

    agent_state = pose_controller.getAgentStateByAgentLookAt(position, look_at)
    agent_state = pose_controller.getAgentStateFromAgentLookAt(look_at, move_direction)

    input_key_list = INPUT_KEY_DICT.keys()
    for input_key in input_key_list:
        agent_state = pose_controller.getAgentStateByKey(input_key)
    return True

