#!/usr/bin/env python3

"""
Xacro exporter.

Produces a self-contained xacro file with:
  - xacro property for INERTIA_MULTIPLY
  - xacro macros for box/sphere/cylinder inertial caluculations
"""

# --- std
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..robot import Robot

_HEADER = '<?xml version="1.0"?>'
_XMLNS = 'xmlns:xacro="http://www.ros.org/wiki/xacro"'

_INERTIA_MACROS = """\
    <xacro:property name="INERTIA_MULTIPLY" value="1.0"/>

    <xacro:macro name="box_inertia" params="m l w h xyz rpy">
        <inertial>
            <origin xyz="${xyz}" rpy="${rpy}"/>
            <mass value="${m}"/>
            <inertia
                ixx="${INERTIA_MULTIPLY * (m/12.0) * (w*w + h*h)}" ixy="0.0" ixz="0.0"
                iyy="${INERTIA_MULTIPLY * (m/12.0) * (l*l + h*h)}" iyz="0.0"
                izz="${INERTIA_MULTIPLY * (m/12.0) * (l*l + w*w)}"/>
        </inertial>
    </xacro:macro>

    <xacro:macro name="sphere_inertia" params="m r xyz rpy">
        <inertial>
            <origin xyz="${xyz}" rpy="${rpy}"/>
            <mass value="${m}"/>
            <inertia
                ixx="${INERTIA_MULTIPLY * (2.0/5.0) * m * r*r}" ixy="0.0" ixz="0.0"
                iyy="${INERTIA_MULTIPLY * (2.0/5.0) * m * r*r}" iyz="0.0"
                izz="${INERTIA_MULTIPLY * (2.0/5.0) * m * r*r}"/>
        </inertial>
    </xacro:macro>

    <xacro:macro name="cylinder_inertia" params="m r h xyz rpy">
        <inertial>
            <origin xyz="${xyz}" rpy="${rpy}"/>
            <mass value="${m}"/>
            <inertia
                ixx="${INERTIA_MULTIPLY * (m/12.0) * (3.0*r*r + h*h)}" ixy="0.0" ixz="0.0"
                iyy="${INERTIA_MULTIPLY * (m/12.0) * (3.0*r*r + h*h)}" iyz="0.0"
                izz="${INERTIA_MULTIPLY * (m/2.0) * r*r}"/>
        </inertial>
    </xacro:macro>"""


class XacroExporter:
    """Converts a :class:'~urdfgenpy.Robot' to a Xacro XML string.

    The output includes 'xacro:property' and 'xacro:macro' definitions for
    standard inertia calculations, making the file easy to parameterise further.
    """

    def export(self, robot: Robot) -> str:
        lines = [
            _HEADER,
            f'<robot name="{robot.name}" {_XMLNS}>',
            "",
            _INERTIA_MACROS,
        ]

        if robot.materials:
            lines.append("")
            for mat in robot.materials:
                lines.append(mat.to_xml("    "))

        lines.append("")
        for link in robot.links:
            lines.append(link.to_xml("    "))
            lines.append("")

        for joint in robot.joints:
            lines.append(joint.to_xml("    "))
            lines.append("")

        lines.append("</robot>")
        return "\n".join(lines) + "\n"
