#!/usr/bin/env python3

"""URDF element types: Origin, Material, Visual, Collision, Inertial."""

# --- std
import math
from dataclasses import dataclass, field

# --- user
from .geometry import Box, Cylinder, Sphere
from .inertia import (
    DEFAULT_INERTIA_MULTIPLY,
    InertiaMatrix,
    box_inertia,
    cylinder_inertia,
    sphere_inertia,
)

Geometry = Box | Cylinder | Sphere


@dataclass
class Origin:
    """Pose of a link or joint relative to its parent frame.

    Args:
        xyz: (x, y, z) translation in metres.
        rpy: (roll, pitch, yaw) rotation in radians.
    """

    xyz: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rpy: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def to_xml(self, indent: str = "") -> str:
        """Return the '<origin>' XML attribute string.

        Args:
            indent: Leading whitespace prepended to the element.

        Returns:
            A single-line '<origin xyz="..." rpy="..."/>' XML string.
        """
        x, y, z = self.xyz
        r, p, yw = self.rpy
        return f'{indent}<origin xyz="{x} {y} {z}" rpy="{r} {p} {yw}"/>'

    @classmethod
    def above(
        cls,
        geometry: Geometry,
        xy: tuple[float, float] = (0.0, 0.0),
        rpy: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> "Origin":
        """Return an origin that lifts geometry so its bottom sits at z=0.

        Computes the Z offset as half the height for a :class:'~urdfgenpy.Box',
        half the length for a :class:'~urdfgenpy.Cylinder', or the radius for a
        :class:'~urdfgenpy.Sphere'.

        Args:
            geometry: A :class:'Box', :class:'Cylinder', or :class:'Sphere' instance.
            xy: Optional (x, y) translation in metres (default '(0, 0)').
            rpy: Optional (roll, pitch, yaw) rotation in radians (default '(0, 0, 0)').

        Returns:
            An :class:'Origin' with Z set so the geometry rests on the XY plane.

        Raises:
            ValueError: If *geometry* is not a supported primitive type.
        """
        if isinstance(geometry, Box):
            z = geometry.height / 2.0
        elif isinstance(geometry, Cylinder):
            z = geometry.length / 2.0
        elif isinstance(geometry, Sphere):
            z = geometry.radius
        else:
            raise ValueError(
                f"Origin.above() does not support {type(geometry).__name__}. "
                "Pass a Box, Cylinder, or Sphere."
            )
        return cls(xyz=(xy[0], xy[1], z), rpy=rpy)

    @classmethod
    def wheel(cls, xy: tuple[float, float] = (0.0, 0.0), z: float = 0.0) -> "Origin":
        """Return an origin with −π/2 roll so a URDF cylinder becomes a wheel.

        URDF cylinders default to the Z axis; applying −π/2 roll reorients the
        symmetry axis to Y so the wheel disc lies in the XZ plane and rolls in
        the X direction.

        Args:
            xy: (x, y) position of the wheel centre in metres (default '(0, 0)').
            z: Height of the wheel centre in metres (default '0').

        Returns:
            An :class:'Origin' with 'rpy = (-π/2, 0, 0)'.
        """
        return cls(xyz=(xy[0], xy[1], z), rpy=(-math.pi / 2.0, 0.0, 0.0))


@dataclass
class Material:
    """Visual material — colour or texture.

    Args:
        name: Unique material name referenced by :class:'Visual'.
        rgba: (r, g, b, a) colour, each in ''[0, 1]''.
        texture: Path to a texture file (mutually exclusive with *rgba*).
    """

    name: str
    rgba: tuple[float, float, float, float] | None = None
    texture: str | None = None

    def to_xml(self, indent: str = "") -> str:
        """Return the '<material>' XML block string.

        Args:
            indent: Leading whitespace prepended to each line.

        Returns:
            A multi-line '<material>...</material>' XML string.
        """
        lines = [f'{indent}<material name="{self.name}">']
        if self.rgba is not None:
            r, g, b, a = self.rgba
            lines.append(f'{indent}    <color rgba="{r} {g} {b} {a}"/>')
        if self.texture is not None:
            lines.append(f'{indent}    <texture filename="{self.texture}"/>')
        lines.append(f"{indent}</material>")
        return "\n".join(lines)


@dataclass
class Visual:
    """Rendered appearance of a link.

    Args:
        geometry: Shape primitive or mesh.
        origin: Pose relative to the link frame.
        material: Optional material reference.
        name: Optional visual name.
    """

    geometry: Geometry
    origin: Origin = field(default_factory=Origin)
    material: Material | None = None
    name: str | None = None

    def to_xml(self, indent: str = "") -> str:
        """Return the '<visual>' XML block string.

        Args:
            indent: Leading whitespace prepended to each line.

        Returns:
            A multi-line '<visual>...</visual>' XML string.
        """
        name_attr = f' name="{self.name}"' if self.name else ""
        lines = [f"{indent}<visual{name_attr}>"]
        lines.append(self.origin.to_xml(indent + "    "))
        lines.append(f"{indent}    <geometry>")
        lines.append(f"{indent}        {self.geometry.to_xml()}")
        lines.append(f"{indent}    </geometry>")
        if self.material:
            # visuals reference material by name; full definition lives at robot level
            lines.append(f'{indent}    <material name="{self.material.name}"/>')
        lines.append(f"{indent}</visual>")
        return "\n".join(lines)


@dataclass
class Collision:
    """Collision shape of a link used by physics engines.

    Args:
        geometry: Shape primitive or mesh.
        origin: Pose relative to the link frame.
        name: Optional collision name.
    """

    geometry: Geometry
    origin: Origin = field(default_factory=Origin)
    name: str | None = None

    def to_xml(self, indent: str = "") -> str:
        """Return the '<collision>' XML block string.

        Args:
            indent: Leading whitespace prepended to each line.

        Returns:
            A multi-line '<collision>...</collision>' XML string.
        """
        name_attr = f' name="{self.name}"' if self.name else ""
        lines = [f"{indent}<collision{name_attr}>"]
        lines.append(self.origin.to_xml(indent + "    "))
        lines.append(f"{indent}    <geometry>")
        lines.append(f"{indent}        {self.geometry.to_xml()}")
        lines.append(f"{indent}    </geometry>")
        lines.append(f"{indent}</collision>")
        return "\n".join(lines)


@dataclass
class Inertial:
    """Mass and inertia of a link.

    Prefer the factory class methods over direct construction:

    * :meth:'from_geometry' - auto-dispatch from any supported geometry
    * :meth:'from_box', :meth:'from_cylinder', :meth:'from_sphere'

    Args:
        mass: Mass in kg.
        matrix: 3x3 symmetric inertia tensor (upper triangle).
        origin: Pose of the centre of mass relative to the link frame.
    """

    mass: float
    matrix: InertiaMatrix
    origin: Origin = field(default_factory=Origin)

    @classmethod
    def from_box(
        cls,
        mass: float,
        length: float,
        w: float,
        h: float,
        origin: Origin | None = None,
        inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY,
    ) -> "Inertial":
        """Create an :class:'Inertial' for a solid box.

        Args:
            mass: Mass in kg.
            length: Dimension along X (metres).
            w: Dimension along Y (metres).
            h: Dimension along Z (metres).
            origin: Pose of the centre of mass; defaults to the link frame origin.
            inertia_multiply: Scalar multiplier on all inertia components (default 1.0).

        Returns:
            An :class:'Inertial' with analytically computed box inertia.
        """
        return cls(
            mass=mass,
            matrix=box_inertia(mass, length, w, h, inertia_multiply),
            origin=origin or Origin(),
        )

    @classmethod
    def from_sphere(
        cls,
        mass: float,
        radius: float,
        origin: Origin | None = None,
        inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY,
    ) -> "Inertial":
        """Create an :class:'Inertial' for a solid sphere.

        Args:
            mass: Mass in kg.
            radius: Sphere radius in metres.
            origin: Pose of the centre of mass; defaults to the link frame origin.
            inertia_multiply: Scalar multiplier on all inertia components (default 1.0).

        Returns:
            An :class:'Inertial' with analytically computed sphere inertia.
        """
        return cls(
            mass=mass,
            matrix=sphere_inertia(mass, radius, inertia_multiply),
            origin=origin or Origin(),
        )

    @classmethod
    def from_cylinder(
        cls,
        mass: float,
        radius: float,
        length: float,
        origin: Origin | None = None,
        inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY,
    ) -> "Inertial":
        """Create an :class:'Inertial' for a solid cylinder.

        Args:
            mass: Mass in kg.
            radius: Cylinder radius in metres.
            length: Cylinder length (height) in metres.
            origin: Pose of the centre of mass; defaults to the link frame origin.
            inertia_multiply: Scalar multiplier on all inertia components (default 1.0).

        Returns:
            An :class:'Inertial' with analytically computed cylinder inertia.
        """
        return cls(
            mass=mass,
            matrix=cylinder_inertia(mass, radius, length, inertia_multiply),
            origin=origin or Origin(),
        )

    @classmethod
    def from_geometry(
        cls,
        mass: float,
        geometry: Geometry,
        origin: Origin | None = None,
        inertia_multiply: float = DEFAULT_INERTIA_MULTIPLY,
    ) -> "Inertial":
        """Create an :class:'Inertial' by dispatching on the geometry type.

        Delegates to :meth:'from_box', :meth:'from_sphere', or
        :meth:'from_cylinder' based on the runtime type of *geometry*.

        Args:
            mass: Mass in kg.
            geometry: A :class:'Box', :class:'Cylinder', or :class:'Sphere' instance.
            origin: Pose of the centre of mass; defaults to the link frame origin.
            inertia_multiply: Scalar multiplier on all inertia components (default 1.0).

        Returns:
            An :class:'Inertial' with analytically computed inertia.

        Raises:
            ValueError: If *geometry* is not a supported primitive type.
        """
        if isinstance(geometry, Box):
            return cls.from_box(
                mass,
                geometry.length,
                geometry.width,
                geometry.height,
                origin,
                inertia_multiply,
            )
        elif isinstance(geometry, Sphere):
            return cls.from_sphere(mass, geometry.radius, origin, inertia_multiply)
        elif isinstance(geometry, Cylinder):
            return cls.from_cylinder(
                mass, geometry.radius, geometry.length, origin, inertia_multiply
            )
        raise ValueError(
            f"Cannot auto-compute inertia for {type(geometry).__name__}. "
            "Provide an InertiaMatrix manually."
        )

    def to_xml(self, indent: str = "") -> str:
        """Return the '<inertial>' XML block string.

        Args:
            indent: Leading whitespace prepended to each line.

        Returns:
            A multi-line '<inertial>...</inertial>' XML string.
        """
        lines = [f"{indent}<inertial>"]
        lines.append(self.origin.to_xml(indent + "    "))
        lines.append(f'{indent}    <mass value="{self.mass}"/>')
        lines.append(self.matrix.to_xml(indent + "    "))
        lines.append(f"{indent}</inertial>")
        return "\n".join(lines)
