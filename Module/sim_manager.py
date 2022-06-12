#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
from tqdm import tqdm

from Data.point import Point
from Data.rad import Rad
from Data.pose import Pose

from Module.sim_loader import SimLoader
from Module.action_controller import ActionController
from Module.pose_controller import PoseController
from Module.sim_renderer import SimRenderer

class SimManager(object):
    def __init__(self):
        self.sim_loader = SimLoader()
        self.action_controller = ActionController()
        self.pose_controller = PoseController()
        self.sim_renderer = SimRenderer()
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
        self.sim_renderer.reset()
        self.control_mode_dict = {
            "action": self.keyBoardActionControl,
            "pose": self.keyBoardPoseControl,
        }
        self.control_mode_list = self.control_mode_dict.keys()

        self.control_mode = "pose"
        return

    def loadSettings(self, sim_settings):
        self.sim_loader.loadSettings(sim_settings)
        return True

    def setControlMode(self, control_mode):
        if control_mode not in self.control_mode_list:
            print("[WARN][SimManager::setControlMode]")
            print("\t control_mode not valid! set to [pose] mode")
            return True
        self.control_mode = control_mode
        return True

    def setRenderMode(self, render_mode):
        return self.sim_renderer.setRenderMode(render_mode)

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

        agent_state = self.pose_controller.getAgentStateByKey(
            input_key,
            self.sim_loader.sim_settings["move_dist"],
            self.sim_loader.sim_settings["rotate_angle"])

        self.sim_loader.setAgentState(agent_state)
        return True

    def keyBoardCircleControl(self, input_key):
        if input_key == "q":
            return False

        print("[WARN][SimManager::keyBoardCircleControl]")
        print("\t To be finished...")
        return True

    def keyBoardControl(self, input_key):
        return self.control_mode_dict[self.control_mode](input_key)

    def startKeyBoardControlRender(self, wait_val):
        #  self.resetAgentPose()
        self.sim_renderer.init()

        while True:
            if not self.sim_renderer.renderFrame(self.sim_loader.observations):
                break
            self.sim_renderer.wait(wait_val)

            agent_state = self.sim_loader.getAgentState()
            print("agent_state: position", agent_state.position,
                  "rotation", agent_state.rotation)

            input_key = getch()
            if not self.keyBoardControl(input_key):
                break
        self.sim_renderer.close()
        return True

def demo_test_speed():
    glb_file_path = \
        "/home/chli/habitat/scannet/scans/scene0474_02/scene0474_02_vh_clean.glb"
    control_mode = "pose"

    sim_settings = {
        "width": 256,
        "height": 256,
        "scene": glb_file_path,
        "default_agent": 0,
        "move_dist": 0.25,
        "rotate_angle": 10.0,
        "sensor_height": 0,
        "color_sensor": True,
        "depth_sensor": True,
        "semantic_sensor": True,
        "seed": 1,
        "enable_physics": False,
    }

    sim_manager = SimManager()
    sim_manager.loadSettings(sim_settings)
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
        "/home/chli/habitat/scannet/scans/scene0474_02/scene0474_02_vh_clean.glb"
    control_mode = "pose"
    render_mode = "cv"
    wait_val = 1

    sim_settings = {
        "width": 256,
        "height": 256,
        "scene": glb_file_path,
        "default_agent": 0,
        "move_dist": 0.25,
        "rotate_angle": 10.0,
        "sensor_height": 0,
        "color_sensor": True,
        "depth_sensor": True,
        "semantic_sensor": True,
        "seed": 1,
        "enable_physics": False,
    }

    sim_manager = SimManager()
    sim_manager.loadSettings(sim_settings)
    sim_manager.setControlMode(control_mode)
    sim_manager.setRenderMode(render_mode)

    sim_manager.pose_controller.pose = Pose(
        Point(1.7, 1.5, -2.5), Rad(0.2, 0.0))
    sim_manager.sim_loader.setAgentState(
        sim_manager.pose_controller.getAgentState())

    sim_manager.startKeyBoardControlRender(wait_val)
    return True

if __name__ == "__main__":
    demo()

