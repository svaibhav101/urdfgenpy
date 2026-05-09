#!/usr/bin/env python3

"""URDF XML exporter."""

# --- std
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..robot import Robot

_HEADER = '<?xml version="1.0"?>'


class URDFExporter:
    """Converts a :class:'~urdfgenpy.Robot' to a URDF XML string."""
    
    def export(self, robot: Robot) -> str:
        lines = [
            _HEADER,
            f'<robot name="{robot.name}">',
        ]

        for mat in robot.materials:
            lines.append(mat.to_xml("    "))

        for link in robot.links:
            lines.append(link.to_xml("    "))

        for joint in robot.joints:
            lines.append(joint.to_xml("    "))

        lines.append("</robot>")
        return "\n".join(lines) + "\n"
