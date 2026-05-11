#!/usr/bin/env python3

"""Link element for URDF robot descriptions."""

# --- std
from dataclasses import dataclass, field

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
    visuals: list[Visual] = field(default_factory=list)
    collisions: list[Collision] = field(default_factory=list)
    inertial: Inertial | None = None

    def add_visual(self, visual: Visual) -> "Link":
        """Append a :class:'Visual' element and return 'self' for chaining.

        Args:
            visual: The visual element to add.

        Returns:
            This :class:'Link' instance.
        """
        self.visuals.append(visual)
        return self

    def add_collision(self, collision: Collision) -> "Link":
        """Append a :class:'Collision' element and return 'self' for chaining.

        Args:
            collision: The collision element to add.

        Returns:
            This :class:'Link' instance.
        """
        self.collisions.append(collision)
        return self

    def set_inertial(self, inertial: Inertial) -> "Link":
        """Set the :class:'Inertial' element and return 'self' for chaining.

        Args:
            inertial: The inertial element to assign.

        Returns:
            This :class:'Link' instance.
        """
        self.inertial = inertial
        return self

    def to_xml(self, indent: str = "") -> str:
        """Return the '<link>' XML block string.

        Args:
            indent: Leading whitespace prepended to each line.

        Returns:
            A multi-line '<link>...</link>' XML string.
        """
        lines = [f'{indent}<link name="{self.name}">']
        if self.inertial:
            lines.append(self.inertial.to_xml(indent + "    "))
        for v in self.visuals:
            lines.append(v.to_xml(indent + "    "))
        for c in self.collisions:
            lines.append(c.to_xml(indent + "    "))
        lines.append(f"{indent}</link>")
        return "\n".join(lines)
