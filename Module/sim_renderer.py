#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch

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

        rgb_obs = self.observations["color_sensor"]
        depth_obs = self.observations["depth_sensor"]
        semantic_obs = self.observations["semantic_sensor"]

        if self.rgb_obs is None and \
                self.depth_obs is None and \
                self.semantic_obs is None:
            return True

        plt.cla()

        depth_img = None
        semantic_img = None

        arr = []
        titles = []

        if self.rgb_obs is not None:
            arr.append(self.rgb_obs)
            titles.append('rgb')

        if self.depth_obs is not None:
            depth_img = Image.fromarray(
                (self.depth_obs * 255).astype(np.uint8),
                mode="L")
            arr.append(depth_img)
            titles.append('depth')

        if self.semantic_obs is not None:
            semantic_img = Image.new("P",
                (self.semantic_obs.shape[1], self.semantic_obs.shape[0]))
            semantic_img.putpalette(d3_40_colors_rgb.flatten())
            semantic_img.putdata((self.semantic_obs.flatten() % 40).astype(np.uint8))
            semantic_img = semantic_img.convert("RGBA")
            arr.append(semantic_img)
            titles.append('semantic')

        for i, data in enumerate(arr):
            ax = plt.subplot(1, 3, i+1)
            ax.axis('off')
            ax.set_title(titles[i])
            plt.imshow(data)
        plt.legend()
        return True

    def render(self):
        plt.figure(figsize=(12 ,8))
        plt.ion()

        while True:
            if not self.renderFrame():
                break
            plt.pause(0.001)
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
    sim_controller.setAgentState([0.0, 0.0, 0.0])

    agent_state = sim_controller.getAgentState()
    print("agent_state: position", agent_state.position,
          "rotation", agent_state.rotation)

    action_names = sim_controller.action_names
    print("Discrete action space: ", action_names)

    for _ in range(100):
        action = action_names[randint(0, len(action_names) - 1)]
        print("action: ", action)
        sim_controller.stepAction(action, True)
        agent_state = sim_controller.getAgentState()
        print("agent_state: position", agent_state.position, "rotation", agent_state.rotation)
    return True

if __name__ == "__main__":
    demo()

