#!/usr/bin/env python3

"""
hobu --> differential-drive mobile robot.

Kinematic chain:
  base_footprint -> base_link (fixed)
                 -> right_wheel_link (continuous, axis Y)
                 -> left_wheel_link  (continuous, axis Y)
                 -> caster_wheel_link (fixed)

Demonstrates:
  - Origin.wheel()       orient a cylinder as a rolling wheel (-pi/2 roll)
  - Origin.above()       lift a box so its bottom face sits at z=0
  - Inertial.from_*      per-shape inertia factory methods
  - inertia_multiply     scale factor for inertia (e.g. for safety margins)

Test:
    - URDF: https://mymodelrobot.appspot.com/5629499534213120
        Use this web-based URDF viewer to quickly validate and preview your URDF file.

"""

import os

from urdfgenpy import (
    Box,
    Collision,
    Cylinder,
    Inertial,
    Joint,
    Link,
    Material,
    Origin,
    Robot,
    Sphere,
    Visual,
)

INERTIA_MULTIPLY = 4.0

# ------------
# Materials
# ------------
# red  = Material("red",  rgba=(0.8, 0.0, 0.0, 1.0))
blue = Material("blue", rgba=(0.0, 0.0, 0.8, 1.0))
gray = Material("gray", rgba=(0.5, 0.5, 0.5, 1.0))

# -------------------------------------------------
# base_link  --> box 0.6 x 0.4 x 0.2, mass 3.5 kg
# -------------------------------------------------
base_box    = Box(length=0.6, width=0.4, height=0.2)
base_origin = Origin.above(base_box)

base_link = Link("base_link")
base_link.add_visual(Visual(geometry=base_box, origin=base_origin, material=blue))
base_link.add_collision(Collision(geometry=base_box, origin=base_origin))
base_link.set_inertial(
    Inertial.from_box(mass=3.5, length=0.6, w=0.4, h=0.2,
                      origin=base_origin, inertia_multiply=INERTIA_MULTIPLY)
)

# ---------------------------------------------------------------------------
# wheel links  --> cylinder r=0.1, len=0.05, mass 0.3 kg
# Origin.wheel() rotates -pi/2 around X so the disc lies in XZ (axis -> Y).
# ---------------------------------------------------------------------------
wheel_geom   = Cylinder(radius=0.1, length=0.05)
wheel_origin = Origin.wheel()

right_wheel_link = Link("right_wheel_link")
right_wheel_link.add_visual(Visual(geometry=wheel_geom, origin=wheel_origin, material=gray))
right_wheel_link.add_collision(Collision(geometry=wheel_geom, origin=wheel_origin))
right_wheel_link.set_inertial(
    Inertial.from_cylinder(mass=0.3, radius=0.1, length=0.05,
                           origin=wheel_origin, inertia_multiply=INERTIA_MULTIPLY)
)

left_wheel_link = Link("left_wheel_link")
left_wheel_link.add_visual(Visual(geometry=wheel_geom, origin=wheel_origin, material=gray))
left_wheel_link.add_collision(Collision(geometry=wheel_geom, origin=wheel_origin))
left_wheel_link.set_inertial(
    Inertial.from_cylinder(mass=0.3, radius=0.1, length=0.05,
                           origin=wheel_origin, inertia_multiply=INERTIA_MULTIPLY)
)

# -----------------------------------------------------
# caster_wheel_link  --> sphere r=0.05, mass 0.2 kg
# Spheres are symmetric, so no rotation needed.
# -----------------------------------------------------
caster_geom = Sphere(radius=0.05)

caster_wheel_link = Link("caster_wheel_link")
caster_wheel_link.add_visual(Visual(geometry=caster_geom, material=gray))
caster_wheel_link.add_collision(Collision(geometry=caster_geom))
caster_wheel_link.set_inertial(
    Inertial.from_sphere(mass=0.2, radius=0.05, inertia_multiply=INERTIA_MULTIPLY)
)

# -----------------------------------------
# base_footprint  --> virtual root link
# -----------------------------------------
base_footprint = Link("base_footprint")

# ---------
# Joints
# ---------
base_joint = Joint(
    name="base_joint",
    joint_type="fixed",
    parent="base_footprint",
    child="base_link",
    origin=Origin(xyz=(0.0, 0.0, 0.1)),
)

base_right_wheel_joint = Joint(
    name="base_right_wheel_joint",
    joint_type="continuous",
    parent="base_link",
    child="right_wheel_link",
    origin=Origin(xyz=(-0.15, -0.225, 0.0)),
    axis=(0.0, 1.0, 0.0),
)

base_left_wheel_joint = Joint(
    name="base_left_wheel_joint",
    joint_type="continuous",
    parent="base_link",
    child="left_wheel_link",
    origin=Origin(xyz=(-0.15, 0.225, 0.0)),
    axis=(0.0, 1.0, 0.0),
)

base_caster_wheel_joint = Joint(
    name="base_caster_wheel_joint",
    joint_type="fixed",
    parent="base_link",
    child="caster_wheel_link",
    origin=Origin(xyz=(0.2, 0.0, -0.05)),
)

# ---------------------------------------------------------------------------
# Assemble robot
# ---------------------------------------------------------------------------
robot = Robot("hobu")

for mat in [gray, blue]:
    robot.add_material(mat)

for link in [base_footprint, base_link, right_wheel_link, left_wheel_link, caster_wheel_link]:
    robot.add_link(link)

for joint in [base_joint, base_right_wheel_joint, base_left_wheel_joint, base_caster_wheel_joint]:
    robot.add_joint(joint)

# ----------------------
# Export
# ----------------------
out_dir = os.path.join(os.path.dirname(__file__), robot.name)
os.makedirs(out_dir, exist_ok=True)

robot.save(os.path.join(out_dir, f"{robot.name}.urdf"))
robot.save(os.path.join(out_dir, f"{robot.name}.xacro"))
robot.save_tree(os.path.join(out_dir, f"{robot.name}_tree.txt"))

print(f"Links : {len(robot.links)}")
print(f"Joints: {len(robot.joints)}")
print(f"urdf saved: {out_dir}")
print(f"xacro saved: {out_dir}")
print(f"tree saved: {out_dir}")

robot.print_tree()
