#!/usr/bin/env python3

"""
Inertia calculation.

Reference: https://en.wikipedia.org/wiki/List_of_moments_of_inertia

"""

from dataclasses import dataclass

DEFAULT_INERTIA_MULTIPLY = 1.0


@dataclass
class InertiaMatrix:
    """Symmetric 3x3 inertia tensor stored as its six unique components.

    Args:
        ixx: Moment of inertia about the X axis (kg·m²).
        ixy: Product of inertia XY (kg·m²).
        ixz: Product of inertia XZ (kg·m²).
        iyy: Moment of inertia about the Y axis (kg·m²).
        iyz: Product of inertia YZ (kg·m²).
        izz: Moment of inertia about the Z axis (kg·m²).
    """

    ixx: float
    ixy: float
    ixz: float
    iyy: float
    iyz: float
    izz: float

    def to_xml(self, indent: str = "    ") -> str:
        """Return the '<inertia>' XML element string.

        Args:
            indent: Leading whitespace prepended to the element.

        Returns:
            A single-line '<inertia ... />' XML string.
        """
        return (
            f"{indent}<inertia "
            f'ixx="{self.ixx:.6g}" ixy="{self.ixy:.6g}" ixz="{self.ixz:.6g}" '
            f'iyy="{self.iyy:.6g}" iyz="{self.iyz:.6g}" izz="{self.izz:.6g}"/>'
        )


def box_inertia(
    m: float,
    length: float,
    w: float,
    h: float,
    inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY,
) -> InertiaMatrix:
    """Compute the inertia tensor for a solid box about its centre of mass.

    Args:
        m: Mass in kg.
        length: Dimension along the X axis (metres).
        w: Dimension along the Y axis (metres).
        h: Dimension along the Z axis (metres).
        inertia_multiply: Scalar multiplier applied to all components (default 1.0).

    Returns:
        An :class:'InertiaMatrix' for the box.
    """
    k = inertia_multiply * m / 12.0
    return InertiaMatrix(
        ixx=k * (w * w + h * h),
        ixy=0.0,
        ixz=0.0,
        iyy=k * (length * length + h * h),
        iyz=0.0,
        izz=k * (length * length + w * w),
    )


def sphere_inertia(
    m: float, r: float, inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY
) -> InertiaMatrix:
    """Compute the inertia tensor for a solid sphere about its centre of mass.

    Args:
        m: Mass in kg.
        r: Radius in metres.
        inertia_multiply: Scalar multiplier applied to all components (default 1.0).

    Returns:
        An :class:'InertiaMatrix' for the sphere.
    """
    val = inertia_multiply * (2.0 / 5.0) * m * r * r
    return InertiaMatrix(ixx=val, ixy=0.0, ixz=0.0, iyy=val, iyz=0.0, izz=val)


def cylinder_inertia(
    m: float, r: float, h: float, inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY
) -> InertiaMatrix:
    """Compute the inertia tensor for a solid cylinder about its centre of mass.

    The symmetry axis is aligned with Z.

    Args:
        m: Mass in kg.
        r: Radius in metres.
        h: Height (length along Z) in metres.
        inertia_multiply: Scalar multiplier applied to all components (default 1.0).

    Returns:
        An :class:'InertiaMatrix' for the cylinder.
    """
    ixx_iyy = inertia_multiply * (m / 12.0) * (3.0 * r * r + h * h)
    izz = inertia_multiply * (m / 2.0) * r * r
    return InertiaMatrix(ixx=ixx_iyy, ixy=0.0, ixz=0.0, iyy=ixx_iyy, iyz=0.0, izz=izz)
