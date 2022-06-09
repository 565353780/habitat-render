#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.actions import demo as action_demo

from Module.sim_loader import demo as load_demo
from Module.sim_controller import demo as control_demo
from Module.sim_renderer import demo as render_demo

if __name__ == "__main__":
    action_demo()
    #  load_demo()
    #  control_demo()
    #  render_demo()

