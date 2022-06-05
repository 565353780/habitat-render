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
        self.cfg = None
        self.sim = None
        return

    def reset(self):
        self.cfg = None
        self.sim = None # TODO: close sim
        return True

    def loadGLB(self, sim_settings):
        self.cfg = make_cfg(sim_settings)
        self.sim = habitat_sim.Simulator(self.cfg)
        return True

    def getSemanticScene(self):
        if self.sim is None:
            return None
        semantic_scene = self.sim.semantic_scene
        print_scene_recur(semantic_scene)
        return semantic_scene

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

    return True

if __name__ == "__main__":
    demo()

