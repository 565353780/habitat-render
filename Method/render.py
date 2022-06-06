#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from habitat_sim.utils.common import d3_40_colors_rgb

def display_sample(rgb_obs=None, depth_obs=None, semantic_obs=None):
    if rgb_obs is None and depth_obs is None and semantic_obs is None:
        return True

    depth_img = None
    semantic_img = None

    arr = []
    titles = []

    if rgb_obs is not None:
        arr.append(rgb_obs)
        titles.append('rgb')

    if depth_obs is not None:
        depth_img = Image.fromarray((depth_obs * 255).astype(np.uint8), mode="L")
        arr.append(depth_img)
        titles.append('depth')

    if semantic_img is not None:
        semantic_img = Image.new("P", (semantic_obs.shape[1], semantic_obs.shape[0]))
        semantic_img.putpalette(d3_40_colors_rgb.flatten())
        semantic_img.putdata((semantic_obs.flatten() % 40).astype(np.uint8))
        semantic_img = semantic_img.convert("RGBA")
        arr.append(semantic_obs)
        titles.append('semantic')

    plt.figure(figsize=(12 ,8))
    for i, data in enumerate(arr):
        ax = plt.subplot(1, 3, i+1)
        ax.axis('off')
        ax.set_title(titles[i])
        plt.imshow(data)
    plt.show()
    return True

