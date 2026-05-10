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

    def tree_string(self) -> str:
        """Return the kinematic chain as a plain-text ASCII tree."""
        
        children: dict = {n: [] for n in self._links}
        child_set: set = set()
        for j in self._joints.values():
            children[j.parent].append((j.name, j.child))
            child_set.add(j.child)

        roots = [n for n in self._links if n not in child_set]
        lines: list = []

        def _geom(link_name: str) -> str:
            lnk = self._links[link_name]
            return f" ({lnk.visuals[0].geometry.shape})" if lnk.visuals else ""

        def render(link_name: str, prefix: str) -> None:
            for i, (jname, cname) in enumerate(children[link_name]):
                is_last      = i == len(children[link_name]) - 1
                child_has_ch = bool(children[cname])
                use_tee = (not is_last) or child_has_ch
                conn = "+--" if use_tee else "\\--"

                joint = self._joints[jname]
                lines.append(f"{prefix}{conn} joint {jname}  [{joint.joint_type}]")
                lines.append(f"{prefix}{'|' if use_tee else ' '}   \\-- link  {cname}{_geom(cname)}")

                if child_has_ch:
                    lines.append(f"{prefix}{'|' if use_tee else ' '}")
                    render(cname, prefix + ("|   " if use_tee else "    ") + "    ")
                elif not is_last:
                    lines.append(f"{prefix}|")

        lines.append(f"\nRobot: {self.name}\n")
        for root in roots:
            lines.append(f"*  link  {root}{_geom(root)}")
            if children[root]:
                lines.append("|")
                render(root, "")

        return "\n".join(lines) + "\n"

    def save_tree(self, output_path: str) -> None:
        """Write the plain-text kinematic tree to a file."""
        with open(output_path, "w") as f:
            f.write(self.tree_string())
