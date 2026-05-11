#!/usr/bin/env python3

"""
Simple 4-DOF robot arm.

Kinematic chain:
  base_link -> shoulder_link (revolute, yaw Z)
             -> upper_arm_link (revolute, pitch Y)
             -> forearm_link (revolute, pitch Y)
             -> end_effector_link (fixed)

Demonstrates:
  - Origin.above(geometry)   lift geometry so its bottom sits at z=0
  - Inertial.from_geometry   auto-compute inertia from geometry + mass
  - JointLimit / JointDynamics
  - robot.save() for both .urdf and .xacro output

Test:
    - URDF: https://mymodelrobot.appspot.com/5629499534213120
        Use this web-based URDF viewer to quickly validate and preview your URDF file.

"""

# --- std
import math
import os

from urdfgenpy import (
    Box,
    Cylinder,
    Sphere,
    Origin,
    Collision,
    Inertial,
    Material,
    Visual,
    Link,
    Joint,
    JointDynamics,
    JointLimit,
    Robot,
)

# ------------
# Materials
# ------------
grey = Material("grey", rgba=(0.5, 0.5, 0.5, 1.0))
blue = Material("blue", rgba=(0.0, 0.3, 0.8, 1.0))
white = Material("white", rgba=(1.0, 1.0, 1.0, 1.0))

# ---------------------------------------------------------------------------
# base_link  : flat mounting plate (box 0.2 × 0.2 × 0.05)
# Origin.above() : lifts the box so its bottom face sits at z=0.
# ---------------------------------------------------------------------------
base_box = Box(length=0.2, width=0.2, height=0.05)
base_origin = Origin.above(base_box)  # xyz=(0, 0, 0.025)

base_link = Link("base_link")
base_link.add_visual(Visual(geometry=base_box, origin=base_origin, material=grey))
base_link.add_collision(Collision(geometry=base_box, origin=base_origin))
base_link.set_inertial(
    Inertial.from_geometry(mass=1.0, geometry=base_box, origin=base_origin)
)

# ---------------------------------------------------------------------------
# shoulder_link  : vertical cylinder (yaw joint; axis Z)
# Cylinder axis is Z by default, so Origin.above() is all that's needed.
# ---------------------------------------------------------------------------
shoulder_cyl = Cylinder(radius=0.04, length=0.15)
shoulder_origin = Origin.above(shoulder_cyl)  # xyz=(0, 0, 0.075)

shoulder_link = Link("shoulder_link")
shoulder_link.add_visual(
    Visual(geometry=shoulder_cyl, origin=shoulder_origin, material=blue)
)
shoulder_link.add_collision(Collision(geometry=shoulder_cyl, origin=shoulder_origin))
shoulder_link.set_inertial(
    Inertial.from_geometry(mass=0.5, geometry=shoulder_cyl, origin=shoulder_origin)
)

# ---------------------------------------------------------------------------
# upper_arm_link  : horizontal cylinder extending along X (pitch joint; axis Y)
# The cylinder's native axis is Z, so rotate -π/2 around Y to align it with X.
# ---------------------------------------------------------------------------
upper_arm_cyl = Cylinder(radius=0.03, length=0.20)
upper_arm_origin = Origin(xyz=(0.10, 0.0, 0.0), rpy=(0.0, -math.pi / 2, 0.0))

upper_arm_link = Link("upper_arm_link")
upper_arm_link.add_visual(
    Visual(geometry=upper_arm_cyl, origin=upper_arm_origin, material=blue)
)
upper_arm_link.add_collision(Collision(geometry=upper_arm_cyl, origin=upper_arm_origin))
upper_arm_link.set_inertial(
    Inertial.from_geometry(mass=0.4, geometry=upper_arm_cyl, origin=upper_arm_origin)
)

# ---------------------------------------------------------------------------
# forearm_link  : horizontal cylinder extending along X (pitch joint; axis Y)
# ---------------------------------------------------------------------------
forearm_cyl = Cylinder(radius=0.025, length=0.18)
forearm_origin = Origin(xyz=(0.09, 0.0, 0.0), rpy=(0.0, -math.pi / 2, 0.0))

forearm_link = Link("forearm_link")
forearm_link.add_visual(
    Visual(geometry=forearm_cyl, origin=forearm_origin, material=blue)
)
forearm_link.add_collision(Collision(geometry=forearm_cyl, origin=forearm_origin))
forearm_link.set_inertial(
    Inertial.from_geometry(mass=0.25, geometry=forearm_cyl, origin=forearm_origin)
)

# ------------------------------------------
# end_effector_link : sphere at the tip
# ------------------------------------------
ee_sphere = Sphere(radius=0.02)
ee_origin = Origin()

ee_link = Link("end_effector_link")
ee_link.add_visual(Visual(geometry=ee_sphere, origin=ee_origin, material=white))
ee_link.add_collision(Collision(geometry=ee_sphere, origin=ee_origin))
ee_link.set_inertial(
    Inertial.from_geometry(mass=0.05, geometry=ee_sphere, origin=ee_origin)
)

# ---------------------------------------------------------------------------
# Joints
# ---------------------------------------------------------------------------
base_to_shoulder = Joint(
    name="base_shoulder_joint",
    joint_type="revolute",
    parent="base_link",
    child="shoulder_link",
    origin=Origin(xyz=(0.0, 0.0, 0.05)),
    axis=(0.0, 0.0, 1.0),
    limit=JointLimit(lower=-math.pi, upper=math.pi, effort=50.0, velocity=2.0),
    dynamics=JointDynamics(damping=0.5, friction=0.01),
)

shoulder_to_upper = Joint(
    name="shoulder_upper_arm_joint",
    joint_type="revolute",
    parent="shoulder_link",
    child="upper_arm_link",
    origin=Origin(xyz=(0.0, 0.0, 0.15)),
    axis=(0.0, 1.0, 0.0),
    limit=JointLimit(lower=-math.pi / 2, upper=0, effort=30.0, velocity=2.0),
    dynamics=JointDynamics(damping=0.2, friction=0.005),
)

upper_to_forearm = Joint(
    name="upper_arm_forearm_joint",
    joint_type="revolute",
    parent="upper_arm_link",
    child="forearm_link",
    origin=Origin(xyz=(0.20, 0.0, 0.0)),
    axis=(0.0, 1.0, 0.0),
    limit=JointLimit(
        lower=-3 * math.pi / 4, upper=math.pi / 2, effort=20.0, velocity=2.5
    ),
    dynamics=JointDynamics(damping=0.1, friction=0.002),
)

forearm_to_ee = Joint(
    name="forearm_ee_joint",
    joint_type="fixed",
    parent="forearm_link",
    child="end_effector_link",
    origin=Origin(xyz=(0.18, 0.0, 0.0)),
)

# ------------------
# Assemble robot
# ------------------
robot = Robot("simple_arm")

for mat in [grey, blue, white]:
    robot.add_material(mat)

for link in [base_link, shoulder_link, upper_arm_link, forearm_link, ee_link]:
    robot.add_link(link)

for joint in [base_to_shoulder, shoulder_to_upper, upper_to_forearm, forearm_to_ee]:
    robot.add_joint(joint)

# -----------
# Export
# -----------
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