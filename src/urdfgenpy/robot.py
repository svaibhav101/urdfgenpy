"""Top-level robot assembly."""

# --- std
from typing import Dict, List, Optional

# --- user
from .elements import Material
from .joint import Joint
from .link import Link


class Robot:
    """
    Root container that holds links, joints, and global materials.

    Build the robot by calling 
        :meth:'add_link' 
        :meth:'add_joint'
        :meth:'add_material', 
    then export with 
        :meth:'save'
        :meth:'to_urdf',
        :meth:'to_xacro'.

    Args:
        name: Robot name embedded in the <robot> tag.
    """

    def __init__(self, name: str):
        self.name = name
        self._links: Dict[str, Link] = {}
        self._joints: Dict[str, Joint] = {}
        self._materials: Dict[str, Material] = {}

    # --- builders ---

    def add_link(self, link: Link) -> "Robot":
        if link.name in self._links:
            raise ValueError(f"Link '{link.name}' already exists.")
        self._links[link.name] = link
        return self

    def add_joint(self, joint: Joint) -> "Robot":
        if joint.name in self._joints:
            raise ValueError(f"Joint '{joint.name}' already exists.")
        if joint.parent not in self._links:
            raise ValueError(f"Parent link '{joint.parent}' not found.")
        if joint.child not in self._links:
            raise ValueError(f"Child link '{joint.child}' not found.")
        self._joints[joint.name] = joint
        return self

    def add_material(self, material: Material) -> "Robot":
        self._materials[material.name] = material
        return self

    # --- accessors ---

    @property
    def links(self) -> List[Link]:
        return list(self._links.values())

    @property
    def joints(self) -> List[Joint]:
        return list(self._joints.values())

    @property
    def materials(self) -> List[Material]:
        return list(self._materials.values())

    def get_link(self, name: str) -> Link:
        if name not in self._links:
            raise KeyError(f"Link '{name}' not found.")
        return self._links[name]

    def get_joint(self, name: str) -> Joint:
        if name not in self._joints:
            raise KeyError(f"Joint '{name}' not found.")
        return self._joints[name]

    # --- export ---

    def to_urdf(self, output_path: Optional[str] = None) -> str:
        from .exporters.urdf import URDFExporter
        xml = URDFExporter().export(self)
        if output_path:
            with open(output_path, "w") as f:
                f.write(xml)
        return xml

    def to_xacro(self, output_path: Optional[str] = None) -> str:
        from .exporters.xacro import XacroExporter
        xml = XacroExporter().export(self)
        if output_path:
            with open(output_path, "w") as f:
                f.write(xml)
        return xml

    def save(self, output_path: str) -> None:
        """Infer format from file extension (.urdf or .xacro)."""
        if output_path.endswith(".xacro"):
            self.to_xacro(output_path)
        else:
            self.to_urdf(output_path)