#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import habitat_sim
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
        return True

    def getAgentState(self):
        agent_state = self.agent.get_state()
        return agent_state

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
    sim_controller.setAgentState([0.0, 0.0, 0.0])

    agent_state = sim_controller.getAgentState()
    print("agent_state: position", agent_state.position,
          "rotation", agent_state.rotation)

    action_names = sim_controller.action_names
    print("Discrete action space: ", action_names)

    for _ in range(100):
        action = action_names[randint(0, len(action_names) - 1)]
        print("action: ", action)
        sim_controller.stepAction(action)
        agent_state = sim_controller.getAgentState()
        print("agent_state: position", agent_state.position, "rotation", agent_state.rotation)
    return True

if __name__ == "__main__":
    demo()

