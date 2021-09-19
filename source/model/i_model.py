from __future__ import absolute_import
from __future__ import division

from .nn_model import SimpleRecurrentAgent
from .teapot_detectron import TeapotDetectron

import functools
import inspect
from torch import no_grad

class Model(object):

    def __init__(self, num_actions, num_parallel_games):

        self.simple_rec_agent = SimpleRecurrentAgent((4, num_actions))
        self.detectron = TeapotDetectron()

    def __getattr__(self, name):
        """Inject the client id into Bullet functions."""
        attribute = getattr(self.simple_rec_agent, name)

        if inspect.isbuiltin(attribute):
            attribute = functools.partial(attribute)

        return attribute

    def forward(self, images, prev_memory_state):
        image_with_mask = self.detectron.get_points(images)
        memory, output = self.simple_rec_agent(prev_memory_state, image_with_mask)

        return memory, output

    def get_action(self, images, prev_memory_state):
        self.simple_rec_agent.eval()
        with no_grad():
            image_with_mask = self.detectron.get_points(images)
            memory, output = self.simple_rec_agent(prev_memory_state, image_with_mask)

            return self.simple_rec_agent.sample_actions(output)
