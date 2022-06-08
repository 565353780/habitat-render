#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import habitat_sim
from getch import getch
from random import randint
from habitat_sim.utils.common import quat_from_angle_axis

from Module.sim_loader import SimLoader

class SimController(SimLoader):
    def __init__(self):
        super(SimController, self).__init__()
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

    def stepAction(self, action):
        if action not in self.action_names:
            print("[ERROR][SimController::stepAction]")
            print("\t action out of range!")
            return False
        self.observations = self.sim.step(action)
        return True

    def initAgent(self):
        self.agent = self.sim.initialize_agent(
            self.sim_settings["default_agent"])
        self.action_names = list(
            self.cfg.agents[
                self.sim_settings["default_agent"]
            ].action_space.keys())
        return True

    def setAgentState(self, position=None, rotation=None):
        if position is None and rotation is None:
            return True

        agent_state = habitat_sim.AgentState()
        if position is not None:
            agent_state.position = np.array(position)
        if rotation is not None:
            agent_state.rotation = np.array(rotation)
        self.agent.set_state(agent_state)

        self.observations = self.sim.get_sensor_observations()
        return True

    def getAgentState(self):
        agent_state = self.agent.get_state()
        return agent_state

    def keyboardControl(self):
        input_key = getch()

        if input_key == "q":
            return False

        if input_key == "e":
            self.stepAction("move_forward")
            return True
            
        if input_key == "j":
            self.stepAction("turn_left")
            return True

        if input_key == "l":
            self.stepAction("turn_right")
            return True

        print("[WARN][SimController::keyboardControl]")
        print("\t input_key out of range!")
        return True

    def startControl(self):
        while True:
            agent_state = self.getAgentState()
            print("agent_state: position", agent_state.position,
                  "rotation", agent_state.rotation)

            if not self.keyboardControl():
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
    sim_controller.setAgentState([-0.6, 0.0, 0.0])

    sim_controller.startControl()
    return True

if __name__ == "__main__":
    demo()

