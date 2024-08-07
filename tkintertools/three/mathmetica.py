"""All 3D operations"""


import array
import dataclasses
import functools
import math

Vector: array.array = functools.partial(array.array, "f")
"""Efficient array"""


@dataclasses.dataclass
class Quaternion:
    """Incomplete implementation of quaternion"""

    w: float = 0
    x: float = 0
    y: float = 0
    z: float = 0

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        """quaternion multiplication"""
        w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z
        x = self.x*other.w + self.w*other.x - self.z*other.y + self.y*other.z
        y = self.y*other.w + self.z*other.x + self.w*other.y - self.x*other.z
        z = self.z*other.w - self.y*other.x + self.x*other.y + self.w*other.z
        return Quaternion(w, x, y, z)

    @property
    def conjugate(self) -> "Quaternion":
        """conjugate quaternion"""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    @property
    def imaginary(self) -> tuple[float, float, float]:
        """imaginary part"""
        return self.x, self.y, self.z


def rotate(coordinate: array.array, radian: float, *, axis: tuple[array.array, array.array]) -> None:
    """"""
    for i, v in enumerate(axis[0]):
        coordinate[i] -= v
        axis[1][i] -= v

    radian /= 2
    norm = math.hypot(*axis[1])

    q = Quaternion(math.cos(radian), *
                   (math.sin(radian)*i/norm for i in axis[1]))
    p = Quaternion(0, *coordinate)

    coordinate[:] = (q*p*q.conjugate).imaginary

    for i, v in enumerate(axis[0]):
        coordinate[i] += v
        axis[1][i] += v  # XXX Is it to be needed really?


def translate(coordinate: array.array, delta: array.array, *, reference: array.array | None = None) -> None:
    """"""
    if reference is None:
        for i, v in enumerate(delta):
            coordinate[i] += v
    else:
        pass


def scale(coordinate: array.array, delta: array.array, *, reference: array.array | None = None) -> None:
    """"""
    if reference is None:
        for i, v in enumerate(delta):
            coordinate[i] *= v
    else:
        for i, v in enumerate(delta):
            coordinate[i] += (coordinate[i]-reference[i]) * (v-1)


def reflect() -> None:
    """"""


def shear() -> None:
    """"""


def project(coordinate: array.array) -> None:
    """"""
