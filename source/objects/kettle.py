import engine
import numpy as np


class Kettle(engine.ILoader):

    def __init__(self, pb_client):
        engine.ILoader.__init__(self)
        self.pb_client = pb_client

    def _load(self):
        self.kettle = self.pb_client.loadURDF(r"./ext/objects/kettle/urdf/kettle.urdf",
                                              basePosition=[-0.15, 0.85, 0.85],
                                              baseOrientation=self.pb_client.getQuaternionFromEuler(
                                                  [np.pi / 2, 0, np.pi / 10]))
        self.last_z = self.get_z_coordinate()
        self.delta_z = 0

    def _update(self):
        new_z = self.get_z_coordinate()
        self.delta_z = self.last_z - new_z
        self.last_z = new_z

    def get_z_coordinate(self):
        return self.pb_client.getBasePositionAndOrientation(self.kettle)[0][2]
