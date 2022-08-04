#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
from tqdm import tqdm

from Config.config import SIM_SETTING

from Data.point import Point
from Data.rad import Rad
from Data.pose import Pose

from Module.sim_loader import SimLoader
from Module.controller.action_controller import ActionController
from Module.controller.pose_controller import PoseController
from Module.controller.circle_controller import CircleController
from Module.renderer.cv_renderer import CVRenderer

class SimManager(object):
    def __init__(self):
        self.sim_loader = SimLoader()
        self.action_controller = ActionController()
        self.pose_controller = PoseController()
        self.circle_controller = CircleController()
        self.cv_renderer = CVRenderer()
        self.control_mode_dict = {
            "action": self.keyBoardActionControl,
            "pose": self.keyBoardPoseControl,
            "circle": self.keyBoardCircleControl,
        }
        self.control_mode_list = self.control_mode_dict.keys()

        self.control_mode = "pose"
        return

    def reset(self):
        self.sim_loader.reset()
        self.action_controller.reset()
        self.pose_controller.reset()
        self.cv_renderer.reset()
        self.control_mode_dict = {
            "action": self.keyBoardActionControl,
            "pose": self.keyBoardPoseControl,
        }
        self.control_mode_list = self.control_mode_dict.keys()

        self.control_mode = "pose"
        return

    def loadSettings(self, glb_file_path):
        self.sim_loader.loadSettings(glb_file_path)
        return True

    def setControlMode(self, control_mode):
        if control_mode not in self.control_mode_list:
            print("[WARN][SimManager::setControlMode]")
            print("\t control_mode not valid! set to [pose] mode")
            return True
        self.control_mode = control_mode
        return True

    def resetAgentPose(self):
        init_agent_state = self.pose_controller.getInitAgentState()
        self.sim_loader.setAgentState(init_agent_state)
        return True

    def keyBoardActionControl(self, input_key):
        if input_key == "q":
            return False

        action = self.action_controller.getAction(input_key)
        if action is None:
            print("[WARN][SimManager::keyBoardActionControl]")
            print("\t input key not valid!")
            return True

        self.sim_loader.stepAction(action)
        return True

    def keyBoardPoseControl(self, input_key):
        if input_key == "q":
            return False

        agent_state = self.pose_controller.getAgentStateByKey(input_key)

        self.sim_loader.setAgentState(agent_state)
        return True

    def keyBoardCircleControl(self, input_key):
        if input_key == "q":
            return False

        agent_state = self.circle_controller.getAgentStateByKey(input_key)

        self.sim_loader.setAgentState(agent_state)
        return True

    def keyBoardControl(self, input_key):
        return self.control_mode_dict[self.control_mode](input_key)

    def startKeyBoardControlRender(self, wait_key):
        #  self.resetAgentPose()
        self.cv_renderer.init()

        while True:
            if not self.cv_renderer.renderFrame(self.sim_loader.observations):
                break
            self.cv_renderer.waitKey(wait_key)

            agent_state = self.sim_loader.getAgentState()
            print("agent_state: position", agent_state.position,
                  "rotation", agent_state.rotation)

            input_key = getch()
            if not self.keyBoardControl(input_key):
                break
        self.cv_renderer.close()
        return True

def demo_test_speed():
    glb_file_path = \
        "/home/chli/scan2cad/scannet/scans/scene0474_02/scene0474_02_vh_clean.glb"
    control_mode = "pose"

    sim_manager = SimManager()
    sim_manager.loadSettings(glb_file_path)
    sim_manager.setControlMode(control_mode)

    sim_manager.pose_controller.pose = Pose(
        Point(1.7, 1.5, -2.5), Rad(0.2, 0.0))
    sim_manager.sim_loader.setAgentState(
        sim_manager.pose_controller.getAgentState())

    input_key_list = sim_manager.pose_controller.input_key_list
    for i in tqdm(range(1000)):
        input_key = list(input_key_list)[i % (len(input_key_list) - 2)]
        sim_manager.keyBoardPoseControl(input_key)
    return True

def demo():
    glb_file_path = \
        "/home/chli/scan2cad/scannet/scans/scene0474_02/scene0474_02_vh_clean.glb"
    control_mode = "circle"
    wait_key = 1

    sim_manager = SimManager()
    sim_manager.loadSettings(glb_file_path)
    sim_manager.setControlMode(control_mode)

    sim_manager.circle_controller.pose = Pose(
        Point(1.8, -0.25, -2.2), Rad(0.2, 0.0))
    sim_manager.sim_loader.setAgentState(
        sim_manager.pose_controller.getAgentState())

    sim_manager.startKeyBoardControlRender(wait_key)
    return True

