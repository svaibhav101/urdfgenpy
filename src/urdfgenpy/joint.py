"""Joint elements for URDF robot descriptions."""

# --- std
from dataclasses import dataclass, field
from typing import Literal, Optional, Tuple

# --- user
from .elements import Origin

# Reference: https://urdfpy.readthedocs.io/en/latest/generated/urdfpy.Joint.html
JointType = Literal["fixed", "prismatic", "revolute", "continuous", "planar", "floating"]


@dataclass
class JointLimit:
    """Motion limits for a joint.

    Args:
        lower: Lower position limit (rad or m).
        upper: Upper position limit (rad or m).
        effort: Maximum effort (N.m or N).
        velocity: Maximum velocity (rad/s or m/s).
    """

    lower: float = 0.0
    upper: float = 0.0
    effort: float = 0.0
    velocity: float = 0.0

    def to_xml(self, indent: str = "") -> str:
        return (
            f'{indent}<limit lower="{self.lower}" upper="{self.upper}" '
            f'effort="{self.effort}" velocity="{self.velocity}"/>'
        )


@dataclass
class JointDynamics:
    """Physical damping and friction for a joint.

    Args:
        damping: Viscous damping coefficient (N.m.s/rad).
        friction: Coulomb friction coefficient (N.m).
    """

    damping: float = 0.0
    friction: float = 0.0

    def to_xml(self, indent: str = "") -> str:
        return (
            f'{indent}<dynamics damping="{self.damping}" friction="{self.friction}"/>'
        )


@dataclass
class JointMimic:
    """Constraint that mirrors another joint's motion.

    Args:
        joint: Name of the joint to mimic.
        multiplier: Scale factor applied to the mimicked joint's value.
        offset: Constant offset added after scaling.
    """

    joint: str
    multiplier: float = 1.0
    offset: float = 0.0

    def to_xml(self, indent: str = "") -> str:
        return (
            f'{indent}<mimic joint="{self.joint}" '
            f'multiplier="{self.multiplier}" offset="{self.offset}"/>'
        )


@dataclass
class Joint:
    """
    Kinematic connection between two links.

    Args:
        name: Unique joint name.
        joint_type: One of "fixed", "prismatic", "revolute", "continuous", "planar" or "floating".
        parent: Name of the parent link.
        child: Name of the child link.
        origin: Transform from parent link frame to joint frame.
        axis: Unit vector defining the joint axis (ignored for 'fixed'/'floating').
        limit: Optional motion limits (:class:'JointLimit').
        dynamics: Optional damping/friction (:class:'JointDynamics').
        mimic: Optional mimic constraint (:class:'JointMimic').
    """

    name: str
    joint_type: JointType
    parent: str
    child: str
    origin: Origin = field(default_factory=Origin)
    axis: Tuple[float, float, float] = (1.0, 0.0, 0.0)
    limit: Optional[JointLimit] = None
    dynamics: Optional[JointDynamics] = None
    mimic: Optional[JointMimic] = None

    def to_xml(self, indent: str = "") -> str:
        lines = [f'{indent}<joint name="{self.name}" type="{self.joint_type}">']
        lines.append(self.origin.to_xml(indent + "    "))
        lines.append(f'{indent}    <parent link="{self.parent}"/>')
        lines.append(f'{indent}    <child link="{self.child}"/>')

        if self.joint_type not in ("fixed", "floating"):
            ax, ay, az = self.axis
            lines.append(f'{indent}    <axis xyz="{ax} {ay} {az}"/>')

        if self.limit is not None:
            lines.append(self.limit.to_xml(indent + "    "))
        if self.dynamics is not None:
            lines.append(self.dynamics.to_xml(indent + "    "))
        if self.mimic is not None:
            lines.append(self.mimic.to_xml(indent + "    "))

        lines.append(f"{indent}</joint>")
        return "\n".join(lines)
