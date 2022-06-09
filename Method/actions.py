#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr
import numpy as np
import magnum as mn

import habitat_sim

from habitat_sim.agent import ActuationSpec
from habitat_sim.utils.common import \
    quat_from_angle_axis, quat_rotate_vector

def getForwardDirection(scene_node):
    forward_ax = (
        np.array(scene_node.absolute_transformation().rotation_scaling())
        @ habitat_sim.geo.FRONT)
    return forward_ax

def getUpAngleDirection(scene_node, up_angle):
    forward_ax = getForwardDirection(scene_node)
    rotation = quat_from_angle_axis(np.deg2rad(up_angle), habitat_sim.geo.UP)
    move_ax = quat_rotate_vector(rotation, forward_ax)
    return move_ax 

def getLeftDirection(scene_node):
    left_ax = (
        np.array(scene_node.absolute_transformation().rotation_scaling())
        @ habitat_sim.geo.LEFT)
    return left_ax

def getRightDirection(scene_node):
    right_ax = (
        np.array(scene_node.absolute_transformation().rotation_scaling())
        @ habitat_sim.geo.RIGHT)
    return right_ax

def getBackDirection(scene_node):
    back_ax = (
        np.array(scene_node.absolute_transformation().rotation_scaling())
        @ habitat_sim.geo.BACK)
    return back_ax

def getUpDirection(scene_node):
    return habitat_sim.geo.UP

def getDownDirection(scene_node):
    return habitat_sim.geo.GRAVITY

def rotateWithDirection(scene_node, direction, amount):
    scene_node.rotate_local(mn.Deg(amount), direction)
    scene_node.rotation = scene_node.rotation.normalized()
    return True

def register_actions():
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
            move_ax = getLeftDirection(scene_node)
            scene_node.translate_local(move_ax * actuation_spec.amount)
            return True

    @habitat_sim.registry.register_move_fn(body_action=True)
    class MoveRight(habitat_sim.SceneNodeControl):
        def __call__(self,
                     scene_node: habitat_sim.SceneNode,
                     actuation_spec: ActuationSpec):
            move_ax = getRightDirection(scene_node)
            scene_node.translate_local(move_ax * actuation_spec.amount)
            return True

    @habitat_sim.registry.register_move_fn(body_action=True)
    class MoveBack(habitat_sim.SceneNodeControl):
        def __call__(self,
                     scene_node: habitat_sim.SceneNode,
                     actuation_spec: ActuationSpec):
            move_ax = getBackDirection(scene_node)
            scene_node.translate_local(move_ax * actuation_spec.amount)
            return True

    @habitat_sim.registry.register_move_fn(body_action=True)
    class MoveUp(habitat_sim.SceneNodeControl):
        def __call__(self,
                     scene_node: habitat_sim.SceneNode,
                     actuation_spec: ActuationSpec):
            move_ax = getUpDirection(scene_node)
            scene_node.translate_local(move_ax * actuation_spec.amount)
            return True

    @habitat_sim.registry.register_move_fn(body_action=True)
    class MoveDown(habitat_sim.SceneNodeControl):
        def __call__(self,
                     scene_node: habitat_sim.SceneNode,
                     actuation_spec: ActuationSpec):
            move_ax = getDownDirection(scene_node)
            scene_node.translate_local(move_ax * actuation_spec.amount)
            return True

    @habitat_sim.registry.register_move_fn(body_action=True)
    class TurnUp(habitat_sim.SceneNodeControl):
        def __call__(self,
                     scene_node: habitat_sim.SceneNode,
                     actuation_spec: ActuationSpec):

            #  rotate_ax = getRightDirection(scene_node)
            #  rotateWithDirection(scene_node, rotate_ax, actuation_spec.amount)

            rotate_ax = (
                np.array(scene_node.absolute_transformation().rotation_scaling())
                @ habitat_sim.geo.RIGHT)
            rotate_ax[0] = 0
            rotate_ax = [0.0, 1.0, 0.0]
            scene_node.rotate_local(mn.Deg(actuation_spec.amount), rotate_ax)
            scene_node.rotation = scene_node.rotation.normalized()
            return True

    @habitat_sim.registry.register_move_fn(body_action=True)
    class TurnDown(habitat_sim.SceneNodeControl):
        def __call__(self,
                     scene_node: habitat_sim.SceneNode,
                     actuation_spec: ActuationSpec):
            rotate_ax = getLeftDirection(scene_node)
            rotateWithDirection(scene_node, rotate_ax, actuation_spec.amount)
            return True

    habitat_sim.registry.register_move_fn(
        MoveLeft, name="move_left", body_action=True)
    habitat_sim.registry.register_move_fn(
        MoveRight, name="move_right", body_action=True)
    habitat_sim.registry.register_move_fn(
        MoveBack, name="move_back", body_action=True)
    habitat_sim.registry.register_move_fn(
        MoveUp, name="move_up", body_action=True)
    habitat_sim.registry.register_move_fn(
        MoveDown, name="move_down", body_action=True)
    habitat_sim.registry.register_move_fn(
        TurnUp, name="turn_up", body_action=True)
    habitat_sim.registry.register_move_fn(
        TurnDown, name="turn_down", body_action=True)
    return True

def demo():
    register_actions()

    agent_config = habitat_sim.AgentConfiguration()

    agent_config.action_space = {
        "move_forward": habitat_sim.agent.ActionSpec(
            "move_forward", habitat_sim.agent.ActuationSpec(amount=0.25)),
        "move_left": habitat_sim.agent.ActionSpec(
            "move_left", habitat_sim.agent.ActuationSpec(amount=0.25)),
        "move_right": habitat_sim.agent.ActionSpec(
            "move_right", habitat_sim.agent.ActuationSpec(amount=0.25)),
        "move_back": habitat_sim.agent.ActionSpec(
            "move_back", habitat_sim.agent.ActuationSpec(amount=0.25)),
        "move_up": habitat_sim.agent.ActionSpec(
            "move_up", habitat_sim.agent.ActuationSpec(amount=0.25)),
        "move_down": habitat_sim.agent.ActionSpec(
            "move_down", habitat_sim.agent.ActuationSpec(amount=0.25)),
        "turn_left": habitat_sim.agent.ActionSpec(
            "turn_left", habitat_sim.agent.ActuationSpec(amount=30.0)),
        "turn_right": habitat_sim.agent.ActionSpec(
            "turn_right", habitat_sim.agent.ActuationSpec(amount=30.0)),
        "turn_up": habitat_sim.agent.ActionSpec(
            "turn_up", habitat_sim.agent.ActuationSpec(amount=30.0)),
        "turn_down": habitat_sim.agent.ActionSpec(
            "turn_down", habitat_sim.agent.ActuationSpec(amount=30.0)),
    }

    action_space = agent_config.action_space
    action_names = action_space.keys()

    for action_name in action_names:
        print(action_space[action_name])
    return True

if __name__ == "__main__":
    demo()

