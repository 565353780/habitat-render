#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

import habitat_sim
from getch import getch

from Module.sim_loader import SimLoader

class SimController(SimLoader):
    def __init__(self):
        super(SimController, self).__init__()
        self.input_key_dict = {
            "e": "move_forward",
            "s": "move_left",
            "f": "move_right",
            "d": "move_back",
            "r": "move_up",
            "w": "move_down",
            "j": "turn_left",
            "l": "turn_right",
            "i": "look_up",
            "k": "look_down",
        }
        self.move_dist = 1.0
        self.rotate_angle = 10
        self.input_key_list = self.input_key_dict.keys()

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

    def keyBoardControl(self):
        input_key = getch()

        if input_key == "q":
            return False

        if input_key not in self.input_key_list:
            print("[WARN][SimController::keyBoardControl]")
            print("\t input_key not valid!")
            return True

        input_action = self.input_key_dict[input_key]

        if not self.stepAction(input_action):
            print("[ERROR][SimController::keyBoardControl]")
            print("\t stepAction [" + input_action + "] failed!")
            return False
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

