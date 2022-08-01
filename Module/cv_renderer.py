#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from PIL import Image
from habitat_sim.utils.common import d3_40_colors_rgb

class CVRenderer(object):
    def __init__(self):
        return

    def reset(self):
        return True

    def initCV(self):
        cv2.namedWindow("CVRenderer",cv2.WINDOW_AUTOSIZE)
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

        arr = []

        if rgb_obs is not None:
            rgb_img = rgb_obs[..., 0:3][...,::-1] / 255.0
            arr.append(rgb_img)

        if depth_obs is not None:
            depth_img = np.clip(depth_obs, 0, 10) / 10.0
            depth_img = cv2.cvtColor(depth_img, cv2.COLOR_GRAY2BGR)
            arr.append(depth_img)

        if semantic_obs is not None:
            semantic_img = Image.new("P",
                (semantic_obs.shape[1], semantic_obs.shape[0]))
            semantic_img.putpalette(d3_40_colors_rgb.flatten())
            semantic_img.putdata((semantic_obs.flatten() % 40).astype(np.uint8))
            semantic_img = semantic_img.convert("RGBA")

            semantic_img = np.array(semantic_img)
            semantic_img = semantic_img[..., 0:3][...,::-1] / 255.0
            arr.append(semantic_img)

        image = np.hstack(arr)
        cv2.imshow("CVRenderer", image)
        return True

    def closeCV(self):
        cv2.destroyAllWindows()
        return True

    def waitKey(self, wait_key):
        cv2.waitKey(wait_key)
        return True

def demo():
    cv_renderer = CVRenderer()

    cv_renderer.initCV()
    cv_renderer.waitKey(1)
    cv_renderer.closeCV()
    return True

