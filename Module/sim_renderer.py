#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from habitat_sim.utils.common import d3_40_colors_rgb

from Module.sim_controller import SimController

class SimRenderer(SimController):
    def __init__(self):
        super(SimRenderer, self).__init__()
        return

    def renderFrame(self):
        if self.observations is None:
            return True

        observations_keys = self.observations.keys()

        rgb_obs = None
        depth_obs = None
        semantic_obs = None

        if "color_sensor" in observations_keys:
            rgb_obs = self.observations["color_sensor"]
        if "depth_sensor" in observations_keys:
            depth_obs = self.observations["depth_sensor"]
        if "semantic_sensor" in observations_keys:
            semantic_obs = self.observations["semantic_sensor"]

        if rgb_obs is None and \
                depth_obs is None and \
                semantic_obs is None:
            return True

        plt.cla()

        arr = []
        titles = []

        if rgb_obs is not None:
            arr.append(rgb_obs)
            titles.append('rgb')

        if depth_obs is not None:
            #  depth_img = np.clip(depth_obs, 0, 10) / 10.0
            arr.append(depth_obs)
            titles.append('depth')

        if semantic_obs is not None:

            #  semantic_img = Image.new("P",
                #  (semantic_obs.shape[1], semantic_obs.shape[0]))
            #  semantic_img.putpalette(d3_40_colors_rgb.flatten())
            #  semantic_img.putdata((semantic_obs.flatten() % 40).astype(np.uint8))
            #  semantic_img = semantic_img.convert("RGBA")

            arr.append(semantic_obs)
            titles.append('semantic')

        for i, data in enumerate(arr):
            ax = plt.subplot(1, 3, i+1)
            ax.axis('off')
            ax.set_title(titles[i])
            plt.imshow(data)
        return True

    def startKeyBoardControlRender(self):
        #  self.resetAgentPose()
        plt.figure(figsize=(24, 8))
        plt.ion()

        while True:
            if not self.renderFrame():
                break
            plt.pause(0.001)

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
        "sensor_height": 0,
        "color_sensor": True,
        "depth_sensor": True,
        "semantic_sensor": True,
        "seed": 1,
        "enable_physics": False,
    }

    sim_renderer = SimRenderer()
    sim_renderer.loadGLB(sim_settings)

    sim_renderer.initAgent()
    sim_renderer.setAgentPose([2.7, 1.5, -3.0], [1.0, 0.0, 0.0])
    sim_renderer.setAgentLookAt([1.7, 1.5, -2.5], [1.0, 0.5, -5.5])
    sim_renderer.setAgentFromLookAt([1.0, 0.5, -5.5], [1.0, 1.0, 3.0])

    sim_renderer.startKeyBoardControlRender()
    return True

if __name__ == "__main__":
    demo()

