#!/usr/bin/env python
# -*- coding: utf-8 -*-

from habitat_sim import AgentState

from Config.input_map import INPUT_KEY_DICT
from Config.init_pose import INIT_POSE

from Data.point import Point
from Data.pose import Pose

from Method.rotations import \
    getRotationFromRad, getRadFromDirection

class PoseController(object):
    def __init__(self):
        self.input_key_dict = INPUT_KEY_DICT
        self.input_key_list = self.input_key_dict.keys()

        self.action_names = None
        self.up_rotate_rad = 0.0
        self.right_rotate_rad = 0.0
        return

    def reset(self):
        self.input_key_dict = INPUT_KEY_DICT
        self.input_key_list = self.input_key_dict.keys()

        self.action_names = None
        self.up_rotate_rad = 0.0
        self.right_rotate_rad = 0.0
        return True

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

