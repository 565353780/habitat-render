#!/usr/bin/env python
# -*- coding: utf-8 -*-

import habitat_sim

from Config.config import make_cfg

from Method.infos import print_scene_recur

class SimLoader(object):
    def __init__(self):
        self.sim_settings = None

        self.cfg = None
        self.sim = None
        self.action_names = None
        self.observations = None
        return

    def reset(self):
        self.sim_settings = None

        self.cfg = None
        if self.sim is not None:
            self.sim.close()
        self.sim = None
        return True

    def initAgent(self):
        self.agent = self.sim.initialize_agent(
            self.sim_settings["default_agent"])
        self.action_names = list(self.cfg.agents[
            self.sim_settings["default_agent"]].action_space.keys())
        return True

    def loadSettings(self, sim_settings):
        self.reset()

        self.sim_settings = sim_settings
        self.cfg = make_cfg(sim_settings)
        self.sim = habitat_sim.Simulator(self.cfg)

        self.initAgent()
        return True

    def stepAction(self, action):
        if action not in self.action_names:
            print("[ERROR][ActionController::stepAction]")
            print("\t action out of range!")
            return False
        self.observations = self.sim.step(action)
        return True

    def updateObservations(self):
        self.observations = self.sim.get_sensor_observations()
        return True

    def getSemanticScene(self):
        if self.sim is None:
            return None
        semantic_scene = self.sim.semantic_scene
        print_scene_recur(semantic_scene)
        return semantic_scene

    def setAgentState(self, agent_state):
        self.agent.set_state(agent_state)
        self.observations = self.sim.get_sensor_observations()
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
        "move_dist": 0.25,
        "rotate_angle": 10.0,
        "sensor_height": 1.5,
        "color_sensor": True,
        "depth_sensor": True,
        "semantic_sensor": True,
        "seed": 1,
        "enable_physics": False,
    }

    sim_loader = SimLoader()
    sim_loader.loadSettings(sim_settings)
    print("[INFO][sim_loader::demo]")
    print("\t load scene success!")
    return True

if __name__ == "__main__":
    demo()

