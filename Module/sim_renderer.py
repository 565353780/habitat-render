#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from habitat_sim.utils.common import d3_40_colors_rgb

class SimRenderer(object):
    def __init__(self):
        return

    def initPlt(self):
        plt.figure(figsize=(24, 8))
        plt.ion()
        return True

    def renderFrame(self, observations):
        if observations is None:
            return True

        observations_keys = observations.keys()

        rgb_obs = None
        depth_obs = None
        semantic_obs = None

        if "color_sensor" in observations_keys:
            rgb_obs = observations["color_sensor"]
        if "depth_sensor" in observations_keys:
            depth_obs = observations["depth_sensor"]
        if "semantic_sensor" in observations_keys:
            semantic_obs = observations["semantic_sensor"]

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

    def closePlt(self):
        plt.ioff()
        return True

    def pausePlt(self, pause_time):
        plt.pause(pause_time)
        return True

def demo():
    sim_renderer = SimRenderer()

    sim_renderer.initPlt()
    sim_renderer.pausePlt(0.001)
    sim_renderer.closePlt()
    return True

if __name__ == "__main__":
    demo()

