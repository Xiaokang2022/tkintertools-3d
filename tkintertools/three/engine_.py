"""Core codes of 3D"""

import abc
import array
import dataclasses
import math
import platform
import statistics
import tkinter
import typing

from ..core import constants, containers


class Scene:
    """存储真实数据，静止"""

    def __init__(self) -> None:
        """"""
        self._lights: list[Light] = []
        self._components: list[Component] = []
        self._geometries: list[Geometry] = []
        self._cameras = list[Camera] = []

    @property
    def components(self) -> tuple["Component", ...]:
        """Return all `Component` of this Scene"""
        return tuple(self._components)

    @property
    def geometries(self) -> tuple["Geometry", ...]:
        """Return all `Geometry` of this Scene"""
        return tuple(self._geometries)

    @property
    def lights(self) -> tuple["Light", ...]:
        """Return all `Light` of this Scene"""
        return tuple(self._lights)

    @property
    def cameras(self) -> tuple["Camera", ...]:
        """"""
        return tuple(self._cameras)


class Camera:
    """数据转换规则集，被动调用"""

    def __init__(
        self,
        scene: Scene,
        position: tuple[int, int, int] = (0, 0, 0),
        towards: tuple[float, float, float] = (1, 0, 0),
        *,
        hFOV: float = math.pi/3
    ) -> None:
        """"""
        self.scene = scene
        self.position = position
        self.towards = towards
        self.hFOV = hFOV

        self.canvas: Canvas | None = None

        scene._cameras.append(self)

    def project(self, coordinate: tuple[float, float, float]) -> tuple[float, float]:
        """"""
        distance = math.dist(self.position, coordinate)
        relative_dis = distance - coordinate[0]
        if relative_dis <= 1e-16:
            return math.inf, math.inf
        k = distance / relative_dis
        return coordinate[1]*k, coordinate[2]*k


class Canvas(containers.Canvas):
    """显示画布"""

    def __init__(
        self,
        master: containers.Tk | containers.Canvas,
        *,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        zoom_item: bool = False,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        **kwargs,
    ) -> None:
        """"""
        containers.Canvas.__init__(self, master, expand=expand, zoom_item=zoom_item,
                                   keep_ratio=keep_ratio, free_anchor=free_anchor, **kwargs)
        # self["bg"] = "black"
        self["highlightthickness"] = 0

        self.camera: Camera = None

        self._components: dict[int, Component] = {
            component.draw(self): component for component in self.scene.components}

        self.update_draw()

    def update_draw(self) -> None:
        """"""
        for item, component in self._components.items():
            component.update(item, camera=self)

        for item in sorted(self._components, key=lambda x: self._components[x].distance(self.position)):
            self.lift(item)


class Light:
    """光线，作用于 Scene"""


class Shade:
    """阴影，作用于 Scene"""


class Component(abc.ABC):
    """"""

    def __init__(
        self,
        scene: Scene,
        *coordinates: tuple[float, float, float],
    ) -> None:
        """"""
        self.coordinates = [array.array("f", lst) for lst in coordinates]
        scene._components.append(self)

    @abc.abstractmethod
    def draw(self, camera: Canvas) -> int:
        """"""

    @abc.abstractmethod
    def distance(self, pivot: tuple[float, float, float]) -> float:
        """"""

    def update(self, item: int, *, camera: Canvas) -> None:
        """"""
        x, y = list(map(camera.project, self.coordinates))
        camera.coords(item, x-3, y-3, x+3, y+3)


class Point(Component):
    """"""

    def __init__(
        self,
        scene: Scene,
        position: tuple[float, float, float],
        *,
        fill: str = "#000000",
    ) -> None:
        """"""
        Component.__init__(self, scene, list(position))
        self.fill = fill

    def draw(self, canvas: Canvas) -> int:
        return canvas.create_oval(0, 0, 0, 0, fill=self.fill)

    def distance(self, pivot: tuple[float, float, float]) -> float:
        return math.dist(self.coordinates[0], pivot)


class Line(Component):
    """"""

    def __init__(
        self,
        scene: Scene,
        start: tuple[float, float, float],
        end: tuple[float, float, float],
    ) -> None:
        """"""
        Component.__init__(self, scene, list(start), list(end))

    def draw(self, canvas: Canvas) -> int:
        return canvas.create_line(0, 0, 0, 0)

    def distance(self, pivot: tuple[float, float, float]) -> float:
        return math.dist(map(statistics.mean, zip(*self.coordinates)), pivot)


class Curve:
    """"""


class Plane(Component):
    """"""

    def __init__(
        self,
        scene: Scene,
        *position: tuple[float, float, float],
    ) -> None:
        """"""
        Component.__init__(self, scene, *map(list, position))

    def draw(self, canvas: Canvas) -> int:
        return canvas.create_polygon(0, 0, 0, 0)

    def distance(self, pivot: tuple[float, float, float]) -> float:
        return math.dist(map(statistics.mean, zip(*self.coordinates)), pivot)


class Surface:
    """"""


class Text:
    """"""


class Image:
    """"""


class Geometry:
    """"""
