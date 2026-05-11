#!/usr/bin/env python3

"""
Geometry primitives for URDF visual and collision elements.
"""

from dataclasses import dataclass


@dataclass
class Box:
    """Axis-aligned rectangular box.

    Args:
        length: Dimension along X (metres).
        width: Dimension along Y (metres).
        height: Dimension along Z (metres).
    """

    length: float
    width: float
    height: float

    def to_xml(self) -> str:
        """Return the '<box>' XML element string."""
        return f'<box size="{self.length} {self.width} {self.height}"/>'

    @property
    def shape(self) -> str:
        """Geometry type identifier: 'box'"""
        return "box"


@dataclass
class Cylinder:
    """Cylinder whose symmetry axis is aligned with Z by default.

    Args:
        radius: Radius (metres).
        length: Length along the symmetry axis (metres).
    """

    radius: float
    length: float

    def to_xml(self) -> str:
        """Return the '<cylinder>' XML element string."""
        return f'<cylinder radius="{self.radius}" length="{self.length}"/>'

    @property
    def shape(self) -> str:
        """Geometry type identifier: 'cylinder'"""
        return "cylinder"


@dataclass
class Sphere:
    """Sphere primitive.

    Args:
        radius: Radius (metres).
    """

    radius: float

    def to_xml(self) -> str:
        """Return the '<sphere>' XML element string."""
        return f'<sphere radius="{self.radius}"/>'

    @property
    def shape(self) -> str:
        """Geometry type identifier: 'sphere'"""
        return "sphere"
