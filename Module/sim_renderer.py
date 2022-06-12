#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Module.plt_renderer import PltRenderer
from Module.cv_renderer import CVRenderer

class SimRenderer(object):
    def __init__(self):
        self.plt_renderer = PltRenderer()
        self.cv_renderer = CVRenderer()
        self.render_mode_list = ["plt", "cv"]
        self.init_func_dict = {
            "plt": self.plt_renderer.initPlt,
            "cv": self.cv_renderer.initCV,
        }
        self.render_func_dict = {
            "plt": self.plt_renderer.renderFrame,
            "cv": self.cv_renderer.renderFrame,
        }
        self.close_func_dict = {
            "plt": self.plt_renderer.closePlt,
            "cv": self.cv_renderer.closeCV,
        }
        self.wait_func_dict = {
            "plt": self.plt_renderer.pausePlt,
            "cv": self.cv_renderer.waitKey,
        }

        self.render_mode = None
        return

    def reset(self):
        self.plt_renderer.reset()
        self.cv_renderer.reset()
        return True

    def setRenderMode(self, render_mode):
        if render_mode not in self.render_mode_list:
            print("[ERROR][SimRenderer::setRenderMode]")
            print("\t render_mode not valid!")
            return False

        self.render_mode = render_mode
        return True

    def init(self):
        return self.init_func_dict[self.render_mode]()

    def renderFrame(self, observasions):
        return self.render_func_dict[self.render_mode](observasions)

    def close(self):
        return self.close_func_dict[self.render_mode]()

    def wait(self, wait_val):
        return self.wait_func_dict[self.render_mode](wait_val)

def demo():
    render_mode = "cv"

    sim_renderer = SimRenderer()

    sim_renderer.setRenderMode(render_mode)
    sim_renderer.init()
    sim_renderer.wait(0.001)
    sim_renderer.close()
    return True

if __name__ == "__main__":
    demo()

