#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch

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

    def resetAgentPose(self):
        init_agent_state = self.pose_controller.getInitAgentState()
        self.sim_loader.setAgentState(init_agent_state)
        return True

    def keyBoardActionControl(self):
        input_key = getch()

        if input_key == "q":
            return False

        action = self.action_controller.getAction(input_key)
        if action is None:
            print("[WARN][SimManager::keyBoardActionControl]")
            print("\t input key not valid!")
            return True

        self.sim_loader.stepAction(action)
        return True

    def keyBoardPoseControl(self):
        input_key = getch()

        if input_key == "q":
            return False

        agent_state = self.pose_controller.getAgentStateByKey(
            input_key,
            self.sim_loader.sim_settings["move_dist"],
            self.sim_loader.sim_settings["rotate_angle"])

        self.sim_loader.setAgentState(agent_state)
        return True

    def keyBoardCircleControl(self):
        input_key = getch()

        if input_key == "q":
            return False

        print("[WARN][SimManager::keyBoardCircleControl]")
        print("\t To be finished...")
        return True

    def keyBoardControl(self):
        return self.control_mode_dict[self.control_mode]()

    def startKeyBoardControlRender(self, pause_time):
        self.resetAgentPose()
        self.sim_renderer.initPlt()

        while True:
            if not self.sim_renderer.renderFrame(self.sim_loader.observations):
                break
            self.sim_renderer.pausePlt(pause_time)

            agent_state = self.sim_loader.getAgentState()
            print("agent_state: position", agent_state.position,
                  "rotation", agent_state.rotation)

            if not self.keyBoardControl():
                break
        self.sim_renderer.closePlt()
        return True

def demo():
    glb_file_path = \
        "/home/chli/habitat/scannet/scans/scene0474_02/scene0474_02_vh_clean.glb"
    control_mode = "pose"
    pause_time = 0.001

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

    #  sim_manager.setAgentPose([2.7, 1.5, -3.0], [1.0, 0.0, 0.0])
    #  sim_manager.setAgentLookAt([1.7, 1.5, -2.5], [1.0, 0.5, -5.5])
    #  sim_manager.setAgentFromLookAt([1.0, 0.5, -5.5], [1.0, 1.0, 3.0])

    sim_manager.startKeyBoardControlRender(pause_time)
    return True

if __name__ == "__main__":
    demo()

