"""Link element for URDF robot descriptions."""

# --- std
from dataclasses import dataclass, field
from typing import List, Optional

# --- user
from .elements import Collision, Inertial, Visual


@dataclass
class Link:
    """
    A rigid body in the robot kinematic tree.

    Args:
        name: Unique link name.
        visuals: List of :class:'Visual' elements (rendered appearance).
        collisions: List of :class:'Collision' elements (physics shape).
        inertial: Optional :class:'Inertial' element (mass/inertia).
    """

    name: str
    visuals: List[Visual] = field(default_factory=list)
    collisions: List[Collision] = field(default_factory=list)
    inertial: Optional[Inertial] = None

    def add_visual(self, visual: Visual) -> "Link":
        self.visuals.append(visual)
        return self

    def add_collision(self, collision: Collision) -> "Link":
        self.collisions.append(collision)
        return self

    def set_inertial(self, inertial: Inertial) -> "Link":
        self.inertial = inertial
        return self

    def to_xml(self, indent: str = "") -> str:
        lines = [f'{indent}<link name="{self.name}">']
        if self.inertial:
            lines.append(self.inertial.to_xml(indent + "    "))
        for v in self.visuals:
            lines.append(v.to_xml(indent + "    "))
        for c in self.collisions:
            lines.append(c.to_xml(indent + "    "))
        lines.append(f'{indent}</link>')
        return "\n".join(lines)
