#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import habitat_sim
from random import randint
from habitat_sim.utils.common import quat_from_angle_axis, d3_40_colors_rgb
from PIL import Image
from matplotlib import pyplot as plt

def display_sample(rgb_obs=None, semantic_obs=None, depth_obs=None):
    if rgb_obs is None and semantic_obs is None and depth_obs is None:
        return True

    rgb_img = None
    semantic_img = None
    depth_img = None

    arr = []
    titles = []

    if rgb_obs is not None:
        rgb_img = Image.fromarray(rgb_obs, mode="RGB")
        arr.append(rgb_obs)
        titles.append('rgb')

    if semantic_img is not None:
        semantic_img = Image.new("P", (semantic_obs.shape[1], semantic_obs.shape[0]))
        semantic_img.putpalette(d3_40_colors_rgb.flatten())
        semantic_img.putdata((semantic_obs.flatten() % 40).astype(np.uint8))
        semantic_img = semantic_img.convert("RGBA")
        arr.append(semantic_obs)
        titles.append('semantic')

    if depth_obs is not None:
        depth_img = Image.fromarray((depth_obs * 255).astype(np.uint8), mode="L")
        arr.append(depth_img)
        titles.append('depth')

    plt.figure(figsize=(12 ,8))
    for i, data in enumerate(arr):
        ax = plt.subplot(1, 3, i+1)
        ax.axis('off')
        ax.set_title(titles[i])
        plt.imshow(data)
    plt.show()
    return True

def make_simple_cfg(settings):
    sim_cfg = habitat_sim.SimulatorConfiguration()
    sim_cfg.scene_id = settings["scene"]

    rgb_sensor_spec = habitat_sim.CameraSensorSpec()
    rgb_sensor_spec.uuid = "color_sensor"
    rgb_sensor_spec.sensor_type = habitat_sim.SensorType.COLOR
    rgb_sensor_spec.resolution = [settings["height"], settings["width"]]
    rgb_sensor_spec.position = [0.0, settings["sensor_height"], 0.0]

    agent_cfg = habitat_sim.agent.AgentConfiguration()
    agent_cfg.sensor_specifications = [rgb_sensor_spec]

    return habitat_sim.Configuration(sim_cfg, [agent_cfg])

test_scene = "/home/chli/habitat/scannet/scans/scene0474_02/scene0474_02_vh_clean.glb"

sim_settings = {
    "scene": test_scene,
    "default_agent": 0,
    "sensor_height": 1.5,
    "width": 256,
    "height": 256}
cfg = make_simple_cfg(sim_settings)

sim = habitat_sim.Simulator(cfg)

agent = sim.initialize_agent(sim_settings["default_agent"])

agent_state = habitat_sim.AgentState()
agent_state.position = np.array([-0.6, 0.0, 0.0])
agent.set_state(agent_state)

agent_state = agent.get_state()
print("agent_state: position", agent_state.position, "rotation", agent_state.rotation)

action_names = list(cfg.agents[sim_settings["default_agent"]].action_space.keys())
print("Discrete action space: ", action_names)

display = True

def navigateAndSee(action=""):
    if action in action_names:
        observations = sim.step(action)
        print("action: ", action)
        if display:
            display_sample(observations["color_sensor"])

for _ in range(100):
    action = action_names[randint(0, len(action_names) - 1)]
    navigateAndSee(action)

