import pybullet as pb

from .matrix import Matrix, rotate

from utils import Comutating, Setter


class ContractVMArgs(object):
    def __init__(self, camera_pos, target_pos, up_vector):
        self.camera_pos = camera_pos
        self.target_pos = target_pos
        self.vector_up = up_vector


class ViewMatrixData(Comutating):
    def __init__(self, position, angles, up_vector, orient, offset):
        super().__init__()

        self.position = position
        self.angles = angles
        self.up_vector = up_vector
        self.orient = orient
        self.offset = offset

    def get(self) -> ContractVMArgs:

        angles = [-self.angles[0], -self.angles[1], -self.angles[2]]

        orient_rot = rotate(self.orient, angles)
        offset_rot = rotate(self.offset, angles)

        camera_pos = self.position + offset_rot
        target_pos = camera_pos + orient_rot
        up_vector = self.up_vector

        return ContractVMArgs(camera_pos, target_pos, up_vector)

    class SetCameraPos(Setter):
        def call(self, data):
            data.position = self.value

    class SetEulerAngles(Setter):
        def call(self, data):
            data.angles = self.value

    class SetUpVector(Setter):
        def call(self, data):
            data.up_vector = self.value

    class SetOrient(Setter):
        def call(self, data):
            data.orient = self.value


class ViewMatrix(Matrix):

    def __init__(self, data: ViewMatrixData):
        self._data = data
        super().__init__()

    def _update(self):
        args = self._data.get()
        self._matrix = pb.computeViewMatrix(
            args.camera_pos,
            args.target_pos,
            args.vector_up
        )

    def update_set(self, setters):
        for setter in setters:
            self._data.com.action(setter)

        self._update()