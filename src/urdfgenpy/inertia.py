#!/usr/bin/env python3

"""
Inertia calculation.

Reference: https://en.wikipedia.org/wiki/List_of_moments_of_inertia

"""
from dataclasses import dataclass

DEFAULT_INERTIA_MULTIPLY = 1.0


@dataclass
class InertiaMatrix:
    ixx: float
    ixy: float
    ixz: float
    iyy: float
    iyz: float
    izz: float

    def to_xml(self, indent: str = "    ") -> str:
        return (
            f'{indent}<inertia '
            f'ixx="{self.ixx:.6g}" ixy="{self.ixy:.6g}" ixz="{self.ixz:.6g}" '
            f'iyy="{self.iyy:.6g}" iyz="{self.iyz:.6g}" izz="{self.izz:.6g}"/>'
        )


def box_inertia(m: float, length: float, w: float, h: float,
                inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY) -> InertiaMatrix:
    """
    Solid box inertia. length=x-dim, w=width(y), h=height(z).
        - width  w (x-direction) [length]
        - height h (y-direction) [width]
        - depth  d (z-direction) [height]
    """
    k = inertia_multiply * m / 12.0
    return InertiaMatrix(
        ixx=k * (w * w + h * h),
        ixy=0.0, ixz=0.0,
        iyy=k * (length * length + h * h),
        iyz=0.0,
        izz=k * (length * length + w * w),
    )


def sphere_inertia(m: float, r: float,
                   inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY) -> InertiaMatrix:
    """Solid sphere inertia."""
    val = inertia_multiply * (2.0 / 5.0) * m * r * r
    return InertiaMatrix(ixx=val, ixy=0.0, ixz=0.0, iyy=val, iyz=0.0, izz=val)


def cylinder_inertia(m: float, r: float, h: float,
                     inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY) -> InertiaMatrix:
    """Solid cylinder inertia. Axis of symmetry along z."""
    ixx_iyy = inertia_multiply * (m / 12.0) * (3.0 * r * r + h * h)
    izz = inertia_multiply * (m / 2.0) * r * r
    return InertiaMatrix(ixx=ixx_iyy, ixy=0.0, ixz=0.0, iyy=ixx_iyy, iyz=0.0, izz=izz)
