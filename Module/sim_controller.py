#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from math import cos, sin, pi

from tf import transformations

import habitat_sim
from getch import getch

from Module.sim_loader import SimLoader

class SimController(SimLoader):
    def __init__(self):
        super(SimController, self).__init__()
        self.move_forward_key = "e"
        self.move_left_key = "s"
        self.move_right_key = "f"
        self.move_back_key = "d"
        self.move_up_key = "r"
        self.move_down_key = "w"

        self.turn_left_key = "j"
        self.turn_right_key = "l"
        self.look_up_key = "i"
        self.look_down_key = "k"
        self.head_left_key = "u"
        self.head_right_key = "o"

        self.move_dist = 1.0
        self.rotate_angle = 10

        self.move_key_list = [
            self.move_forward_key, self.move_back_key,
            self.move_left_key, self.move_right_key,
            self.move_up_key, self.move_down_key
        ]
        self.rotate_key_list = [
            self.turn_left_key, self.turn_right_key,
            self.look_up_key, self.look_down_key,
            self.head_left_key, self.head_right_key
        ]

        self.agent = None
        self.action_names = None
        self.observations = None
        return

    def reset(self):
        self.sim_settings = None

        self.cfg = None
        if self.sim is not None:
            self.sim.close()
        self.sim = None
        self.agent = None
        self.action_names = None
        self.observations = None
        return True

    def initAgent(self):
        self.agent = self.sim.initialize_agent(
            self.sim_settings["default_agent"])
        self.action_names = list(
            self.cfg.agents[
                self.sim_settings["default_agent"]
            ].action_space.keys())
        return True

    def stepAction(self, action):
        if action not in self.action_names:
            print("[ERROR][SimController::stepAction]")
            print("\t action out of range!")
            return False
        self.observations = self.sim.step(action)
        return True

    def getAgentState(self):
        agent_state = self.agent.get_state()
        return agent_state

    def setAgentState(self, position, rotation):
        if position is None or rotation is None:
            print("[ERROR][SimController::setAgentState]")
            print("\t input contains None!")
            return False

        agent_state = habitat_sim.AgentState()
        agent_state.position = np.array(position)
        agent_state.rotation = np.array(rotation)
        self.agent.set_state(agent_state)

        self.observations = self.sim.get_sensor_observations()
        return True

    def getEulerAngleFromQuaternion(self, quaternion):
        (roll, pitch, yaw) = transformations.euler_from_quaternion([
            quaternion[0], quaternion[1], quaternion[2], quaternion[3]])
        return np.array([roll, pitch, yaw])

    def getQuaternionFromEulerAngle(self, euler_angle):
        quaternion = transformations.quaternion_from_euler(
            euler_angle[0], euler_angle[1], euler_angle[2])
        return np.array([quaternion[0], quaternion[1], quaternion[2], quaternion[3]])

    def getRotationMatrixFromEulerAngle(self, euler_angle):
        R_x = np.array([
            [1, 0, 0],
            [0, cos(euler_angle[0]), -sin(euler_angle[0])],
            [0, sin(euler_angle[0]), cos(euler_angle[0])]
        ])
                    
        R_y = np.array([
            [cos(euler_angle[1]), 0, sin(euler_angle[1])],
            [0, 1, 0],
            [-sin(euler_angle[1]), 0, cos(euler_angle[1])]
        ])
                    
        R_z = np.array([
            [cos(euler_angle[2]), -sin(euler_angle[2]), 0],
            [sin(euler_angle[2]), cos(euler_angle[2]), 0],
            [0, 0, 1]
        ])
                    
        rotation_matrix = np.dot(R_z, np.dot( R_y, R_x ))
        return rotation_matrix

    def getForwardDirection(self, agent_state):
        x_axis_direction = np.array([1, 0, 0])

        agent_orientation = agent_state.rotation

        agent_quaternion = [
            agent_orientation.x,
            agent_orientation.y,
            agent_orientation.z,
            agent_orientation.w]

        euler_angle = self.getEulerAngleFromQuaternion(agent_quaternion)

        rotation_matrix = self.getRotationMatrixFromEulerAngle(euler_angle)

        forward_direction = np.dot(rotation_matrix, x_axis_direction)
        forward_direction = np.array([forward_direction[0], forward_direction[1], 0])
        forward_direction_norm = np.linalg.norm(forward_direction)

        if forward_direction_norm == 0:
            print("[ERROR][SimController::getForwardDirection]")
            print("\t forward_direction_norm is 0!")
            return None

        forward_direction /= forward_direction_norm
        return forward_direction

    def getBackDirection(self, agent_state):
        forward_direction = self.getForwardDirection(agent_state)
        if forward_direction is None:
            print("[ERROR][SimController::getBackDirection]")
            print("\t forward_direction is None!")
            return None
        back_direction = -forward_direction
        return back_direction

    def getLeftDirection(self, agent_state):
        forward_direction = self.getForwardDirection(agent_state)
        if forward_direction is None:
            print("[ERROR][SimController::getLeftDirection]")
            print("\t forward_direction is None!")
            return None
        left_direction = \
            [-forward_direction[1], forward_direction[0], forward_direction[2]]
        return left_direction

    def getRightDirection(self, agent_state):
        forward_direction = self.getForwardDirection(agent_state)
        if forward_direction is None:
            print("[ERROR][SimController::getRightDirection]")
            print("\t forward_direction is None!")
            return None
        right_direction = \
            [forward_direction[1], -forward_direction[0], forward_direction[2]]
        return right_direction

    def getUpDirection(self, agent_state):
        up_direction = np.array([0, 0, 1])
        return up_direction

    def getDownDirection(self, agent_state):
        down_direction = np.array([0, 0, -1])
        return down_direction

    def moveAgent(self, agent_state, move_direction, move_dist):
        new_position = [
            agent_state.position[0] + move_dist * move_direction[0],
            agent_state.position[1] + move_dist * move_direction[1],
            agent_state.position[2] + move_dist * move_direction[2]
        ]

        agent_orientation = [
            agent_state.rotation.x,
            agent_state.rotation.y,
            agent_state.rotation.z,
            agent_state.rotation.w]

        if not self.setAgentState(new_position, agent_orientation):
            print("[ERROR][SimController::moveAgent]")
            print("\t setAgentState failed!")
            return False
        return True

    def rotateAgent(self, agent_state, rotate_angle, rotate_axis):
        agent_position = agent_state.position

        agent_orientation = [
            agent_state.rotation.x,
            agent_state.rotation.y,
            agent_state.rotation.z,
            agent_state.rotation.w]

        euler_angle = self.getEulerAngleFromQuaternion(agent_orientation)

        real_rotate_angle = rotate_angle * pi / 180.0

        if rotate_axis == 0:
            euler_angle[0] += real_rotate_angle
        elif rotate_axis == 1:
            euler_angle[1] += real_rotate_angle
        elif rotate_axis == 2:
            euler_angle[2] += real_rotate_angle
        else:
            print("[ERROR][SimController::rotateAgent]")
            print("\t rotate_axis out of range!")
            return False

        new_orientation = self.getQuaternionFromEulerAngle(euler_angle)

        if not self.setAgentState(agent_position, new_orientation):
            print("[ERROR][SimController::rotateAgent]")
            print("\t setAgentState failed!")
            return False
        return True

    def moveForward(self, move_dist):
        agent_state = self.getAgentState()

        move_direction = self.getForwardDirection(agent_state)
        if move_direction is None:
            print("[ERROR][SimController::moveForward]")
            print("\t move_direction is None!")
            return False

        if not self.moveAgent(agent_state, sim_move_direction, move_dist):
            print("[ERROR][SimController::moveForward]")
            print("\t moveAgent failed!")
            return False
        return True

    def moveBack(self, move_dist):
        agent_state = self.getAgentState()

        move_direction = self.getBackDirection(agent_state)
        if move_direction is None:
            print("[ERROR][SimController::moveBack]")
            print("\t move_direction is None!")
            return False

        if not self.moveAgent(agent_state, move_direction, move_dist):
            print("[ERROR][SimController::moveBack]")
            print("\t moveAgent failed!")
            return False
        return True

    def moveLeft(self, move_dist):
        agent_state = self.getAgentState()

        move_direction = self.getLeftDirection(agent_state)
        if move_direction is None:
            print("[ERROR][SimController::moveLeft]")
            print("\t move_direction is None!")
            return False

        if not self.moveAgent(agent_state, move_direction, move_dist):
            print("[ERROR][SimController::moveLeft]")
            print("\t moveAgent failed!")
            return False
        return True

    def moveRight(self, move_dist):
        agent_state = self.getAgentState()

        move_direction = self.getRightDirection(agent_state)
        if move_direction is None:
            print("[ERROR][SimController::moveRight]")
            print("\t move_direction is None!")
            return False

        if not self.moveAgent(agent_state, move_direction, move_dist):
            print("[ERROR][SimController::moveRight]")
            print("\t moveAgent failed!")
            return False
        return True

    def moveUp(self, move_dist):
        agent_state = self.getAgentState()

        move_direction = self.getUpDirection(agent_state)
        if move_direction is None:
            print("[ERROR][SimController::moveUp]")
            print("\t move_direction is None!")
            return False

        if not self.moveAgent(agent_state, move_direction, move_dist):
            print("[ERROR][SimController::moveUp]")
            print("\t moveAgent failed!")
            return False
        return True

    def moveDown(self, move_dist):
        agent_state = self.getAgentState()

        move_direction = self.getDownDirection(agent_state)
        if move_direction is None:
            print("[ERROR][SimController::moveDown]")
            print("\t move_direction is None!")
            return False

        if not self.moveAgent(agent_state, move_direction, move_dist):
            print("[ERROR][SimController::moveDown]")
            print("\t moveAgent failed!")
            return False
        return True

    def turnLeft(self, rotate_angle):
        agent_state = self.getAgentState()

        if not self.rotateAgent(agent_state, rotate_angle, 2):
            print("[ERROR][SimController::turnLeft]")
            print("\t rotateAgent failed!")
            return False
        return True

    def turnRight(self, rotate_angle):
        agent_state = self.getAgentState()

        right_rotate_angle = -rotate_angle

        if not self.rotateAgent(agent_state, right_rotate_angle, 2):
            print("[ERROR][SimController::turnRight]")
            print("\t rotateAgent failed!")
            return False
        return True

    def lookUp(self, rotate_angle):
        agent_state = self.getAgentState()

        up_rotate_angle = -rotate_angle

        if not self.rotateAgent(agent_state, up_rotate_angle, 1):
            print("[ERROR][SimController::lookUp]")
            print("\t rotateAgent failed!")
            return False
        return True

    def lookDown(self, rotate_angle):
        agent_state = self.getAgentState()

        if not self.rotateAgent(agent_state, rotate_angle, 1):
            print("[ERROR][SimController::lookDown]")
            print("\t rotateAgent failed!")
            return False
        return True

    def headLeft(self, rotate_angle):
        agent_state = self.getAgentState()

        left_rotate_angle = -rotate_angle

        if not self.rotateAgent(agent_state, left_rotate_angle, 0):
            print("[ERROR][SimController::headRight]")
            print("\t rotateAgent failed!")
            return False
        return True

    def headRight(self, rotate_angle):
        agent_state = self.getAgentState()

        if not self.rotateAgent(agent_state, rotate_angle, 0):
            print("[ERROR][SimController::headRight]")
            print("\t rotateAgent failed!")
            return False
        return True

    def keyBoardMove(self, move_dist, input_key):
        if input_key == self.move_forward_key:
            return self.moveForward(move_dist)
        if input_key == self.move_back_key:
            return self.moveBack(move_dist)
        if input_key == self.move_left_key:
            return self.moveLeft(move_dist)
        if input_key == self.move_right_key:
            return self.moveRight(move_dist)
        if input_key == self.move_up_key:
            return self.moveUp(move_dist)
        if input_key == self.move_down_key:
            return self.moveDown(move_dist)

        print("[WARN][SimController::keyBoardMove]")
        print("\t input_key out of range!")
        return True

    def keyBoardRotate(self, rotate_angle, input_key):
        if input_key == self.turn_left_key:
            return self.turnLeft(rotate_angle)
        if input_key == self.turn_right_key:
            return self.turnRight(rotate_angle)
        if input_key == self.look_up_key:
            return self.lookUp(rotate_angle)
        if input_key == self.look_down_key:
            return self.lookDown(rotate_angle)
        if input_key == self.head_left_key:
            return self.headLeft(rotate_angle)
        if input_key == self.head_right_key:
            return self.headRight(rotate_angle)

        print("[WARN][SimController::keyBoardRotate]")
        print("\t input_key out of range!")
        return True

    def keyBoardControl(self):
        input_key = getch()

        if input_key == "q":
            return False

        #  if input_key == self.move_forward_key:
            #  self.stepAction("move_forward")
            #  return True
        #  if input_key == self.turn_left_key:
            #  self.stepAction("turn_left")
            #  return True
        #  if input_key == self.turn_right_key:
            #  self.stepAction("turn_right")
            #  return True

        if input_key in self.move_key_list:
            if not self.keyBoardMove(self.move_dist, input_key):
                print("[ERROR][SimController::keyboardControl]")
                print("\t keyBoardMove failed!")
                return False
            return True
        if input_key in self.rotate_key_list:
            if not self.keyBoardRotate(self.rotate_angle, input_key):
                print("[ERROR][SimController::keyboardControl]")
                print("\t keyBoardRotate failed!")
                return False
            return True

        print("[WARN][SimController::keyBoardControl]")
        print("\t input_key out of range!")
        return True

    def startControl(self):
        while True:
            agent_state = self.getAgentState()
            print("agent_state: position", agent_state.position,
                  "rotation", agent_state.rotation)

            if not self.keyBoardControl():
                break
        return True

def demo():
    glb_file_path = \
        "/home/chli/habitat/scannet/scans/scene0474_02/scene0474_02_vh_clean.glb"

    sim_settings = {
        "width": 256,
        "height": 256,
        "scene": glb_file_path,
        "default_agent": 0,
        "sensor_height": 1.5,
        "color_sensor": True,
        "depth_sensor": True,
        "semantic_sensor": True,
        "seed": 1,
        "enable_physics": False,
    }

    sim_controller = SimController()
    sim_controller.loadGLB(sim_settings)

    sim_controller.initAgent()
    sim_controller.setAgentState([-0.6, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0])

    sim_controller.startControl()
    return True

if __name__ == "__main__":
    demo()

