#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

import numpy as np
import habitat_sim
from habitat_sim.utils.common import quat_from_angle_axis

from Data.config import make_cfg

from Method.info import print_scene_recur
from Method.render import display_sample

class SimLoader(object):
    def __init__(self):
        self.sim_settings = None

        self.cfg = None
        self.sim = None
        self.agent = None
        self.action_names = None
        return

    def reset(self):
        self.sim_settings = None

        self.cfg = None
        if self.sim is not None:
            self.sim.close()
        self.sim = None
        self.agent = None
        self.action_names = None
        return True

    def loadGLB(self, sim_settings):
        self.reset()
        self.sim_settings = sim_settings
        self.cfg = make_cfg(sim_settings)
        self.sim = habitat_sim.Simulator(self.cfg)
        return True

    def initAgent(self):
        self.agent = self.sim.initialize_agent(self.sim_settings["default_agent"])
        self.action_names = \
            list(self.cfg.agents[self.sim_settings["default_agent"]].action_space.keys())
        return True

    def stepAction(self, action, display=False):
        if action not in self.action_names:
            return False
        observations = self.sim.step(action)
        print("action: ", action)
        if not display:
            return True
        display_sample(rgb_obs=observations["color_sensor"],
                       depth_obs=observations["depth_sensor"],
                       semantic_obs=observations["semantic_sensor"])
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

    def getSemanticScene(self):
        if self.sim is None:
            return None
        semantic_scene = self.sim.semantic_scene
        print_scene_recur(semantic_scene)
        return semantic_scene

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

    sim_loader = SimLoader()
    sim_loader.loadGLB(sim_settings)
    sim_loader.initAgent()
    sim_loader.setAgentState([-0.6, 0.0, 0.0])

    agent_state = sim_loader.getAgentState()
    print("agent_state: position", agent_state.position, "rotation", agent_state.rotation)

    action_names = sim_loader.action_names
    print("Discrete action space: ", action_names)

    for _ in range(100):
        action = action_names[randint(0, len(action_names) - 1)]
        sim_loader.stepAction(action, True)
        agent_state = sim_loader.getAgentState()
        print("agent_state: position", agent_state.position, "rotation", agent_state.rotation)
    return True

if __name__ == "__main__":
    demo()

