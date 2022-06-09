#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr
import quaternion
import numpy as np
import magnum as mn

import habitat_sim

from habitat_sim.agent import ActuationSpec
from habitat_sim.utils.common import \
    quat_from_angle_axis, quat_rotate_vector

def moveWithDirection(scene_node, direction, amount):
    move_ax = (
        np.array(scene_node.absolute_transformation().rotation_scaling())
        @ direction)
    scene_node.translate_local(move_ax * amount)
    return True

def rotateWithDirection(scene_node, direction, amount):
    scene_node.rotate_local(mn.Deg(amount), direction)
    scene_node.rotation = scene_node.rotation.normalized()
    return True

@attr.s(auto_attribs=True, slots=True)
class DirectionSpec(object):
    def __init__(self, direction, amount):
        self.direction = np.array(direction, dtype=np.float32)
        self.amount = float(amount)
        return

@habitat_sim.registry.register_move_fn(body_action=True)
class MoveLeft(habitat_sim.SceneNodeControl):
    def __call__(self,
                 scene_node: habitat_sim.SceneNode,
                 actuation_spec: ActuationSpec):
        moveWithDirection(scene_node, habitat_sim.geo.LEFT, actuation_spec.amount)
        return True

@habitat_sim.registry.register_move_fn(body_action=True)
class MoveRight(habitat_sim.SceneNodeControl):
    def __call__(self,
                 scene_node: habitat_sim.SceneNode,
                 actuation_spec: ActuationSpec):
        moveWithDirection(scene_node, habitat_sim.geo.RIGHT, actuation_spec.amount)
        return True

@habitat_sim.registry.register_move_fn(body_action=True)
class MoveBack(habitat_sim.SceneNodeControl):
    def __call__(self,
                 scene_node: habitat_sim.SceneNode,
                 actuation_spec: ActuationSpec):
        moveWithDirection(scene_node, habitat_sim.geo.BACK, actuation_spec.amount)
        return True

@habitat_sim.registry.register_move_fn(body_action=True)
class HeadUp(habitat_sim.SceneNodeControl):
    def __call__(self,
                 scene_node: habitat_sim.SceneNode,
                 actuation_spec: ActuationSpec):
        rotateWithDirection(scene_node, habitat_sim.geo.RIGHT, actuation_spec.amount)
        return True

@habitat_sim.registry.register_move_fn(body_action=True)
class HeadDown(habitat_sim.SceneNodeControl):
    def __call__(self,
                 scene_node: habitat_sim.SceneNode,
                 actuation_spec: ActuationSpec):
        rotateWithDirection(scene_node, habitat_sim.geo.LEFT, actuation_spec.amount)
        return True

def demo():
    habitat_sim.registry.register_move_fn(
        MoveLeft, name="move_left", body_action=True)
    habitat_sim.registry.register_move_fn(
        MoveRight, name="move_right", body_action=True)
    habitat_sim.registry.register_move_fn(
        MoveBack, name="move_back", body_action=True)
    habitat_sim.registry.register_move_fn(
        HeadUp, name="head_up", body_action=True)
    habitat_sim.registry.register_move_fn(
        HeadDown, name="head_down", body_action=True)

    agent_config = habitat_sim.AgentConfiguration()

    agent_config.action_space["move_left"] = habitat_sim.ActionSpec(
        "move_left", ActuationSpec(0.25))
    agent_config.action_space["move_right"] = habitat_sim.ActionSpec(
        "move_right", ActuationSpec(0.25))
    agent_config.action_space["move_back"] = habitat_sim.ActionSpec(
        "move_back", ActuationSpec(0.25))
    agent_config.action_space["head_up"] = habitat_sim.ActionSpec(
        "head_up", ActuationSpec(30.0))
    agent_config.action_space["head_down"] = habitat_sim.ActionSpec(
        "head_down", ActuationSpec(30.0))

    action_space = agent_config.action_space
    action_names = action_space.keys()

    for action_name in action_names:
        print(action_space[action_name])
    return True

if __name__ == "__main__":
    demo()

