#!/usr/bin/env python3

"""
2-DOF pan-tilt unit (PTU).

Kinematic chain:
  base_plate  (box)
    -> pan_link    (cylinder)  revolute Z    ±pi      pan
      -> tilt_link (box)       revolute Y   -pi/2 / 0 tilt
        -> lens    (sphere)    fixed                  sensor tip

Demonstrates:
  - All three geometry primitives: Box, Cylinder, Sphere
  - Origin.above()          lift geometry so its bottom sits at z = 0
  - Inertial.from_geometry  auto-compute inertia from shape + mass
  - JointLimit / JointDynamics
  - robot.save()            infer .urdf or .xacro from the file extension
"""

# --- std
import math
import os

# --- urdfgenpy
from urdfgenpy import (
    Box,
    Collision,
    Cylinder,
    Inertial,
    Joint,
    JointDynamics,
    JointLimit,
    Link,
    Material,
    Origin,
    Robot,
    Sphere,
    Visual,
)

# ---------------------------------------------
# Materials
# ---------------------------------------------
charcoal = Material("charcoal", rgba=(0.22, 0.22, 0.25, 1.0))
dark_grey = Material("dark_grey", rgba=(0.35, 0.35, 0.38, 1.0))
amber = Material("amber", rgba=(1.0, 0.55, 0.0, 1.0))

# ---------------------------------------------
# base_plate  -  flat mounting box
# ---------------------------------------------
plate_geom = Box(length=0.14, width=0.14, height=0.025)
plate_origin = Origin.above(plate_geom)  # xyz = (0, 0, 0.0125)

base_plate = Link("base_plate")
base_plate.add_visual(Visual(geometry=plate_geom, origin=plate_origin, material=charcoal))
base_plate.add_collision(Collision(geometry=plate_geom, origin=plate_origin))
base_plate.set_inertial(Inertial.from_geometry(mass=0.8, geometry=plate_geom, origin=plate_origin))

# ---------------------------------------------
# pan_link  -  upright cylinder; rotates around Z
# ---------------------------------------------
pan_geom = Cylinder(radius=0.028, length=0.07)
pan_origin = Origin.above(pan_geom)  # xyz = (0, 0, 0.035)

pan_link = Link("pan_link")
pan_link.add_visual(Visual(geometry=pan_geom, origin=pan_origin, material=dark_grey))
pan_link.add_collision(Collision(geometry=pan_geom, origin=pan_origin))
pan_link.set_inertial(Inertial.from_geometry(mass=0.18, geometry=pan_geom, origin=pan_origin))

# ---------------------------------------------
# tilt_link  -  sensor head box; tilts around Y
# ---------------------------------------------
tilt_geom = Box(length=0.09, width=0.05, height=0.05)
tilt_origin = Origin(xyz=(0.045, 0.0, 0.0))  # centred along X from the pivot

tilt_link = Link("tilt_link")
tilt_link.add_visual(Visual(geometry=tilt_geom, origin=tilt_origin, material=amber))
tilt_link.add_collision(Collision(geometry=tilt_geom, origin=tilt_origin))
tilt_link.set_inertial(Inertial.from_geometry(mass=0.12, geometry=tilt_geom, origin=tilt_origin))

# ---------------------------------------------
# lens  -  rounded tip marking the sensor axis
# ---------------------------------------------
lens_geom = Sphere(radius=0.022)

lens = Link("lens")
lens.add_visual(Visual(geometry=lens_geom, material=charcoal))
lens.add_collision(Collision(geometry=lens_geom))
lens.set_inertial(Inertial.from_geometry(mass=0.03, geometry=lens_geom))

# ---------------------------------------------
# Joints
# ---------------------------------------------
pan_joint = Joint(
    name="pan_joint",
    joint_type="revolute",
    parent="base_plate",
    child="pan_link",
    origin=Origin(xyz=(0.0, 0.0, 0.025)),  # on top of the plate
    axis=(0.0, 0.0, 1.0),
    limit=JointLimit(lower=-math.pi, upper=math.pi, effort=10.0, velocity=1.5),
    dynamics=JointDynamics(damping=0.3, friction=0.02),
)

tilt_joint = Joint(
    name="tilt_joint",
    joint_type="revolute",
    parent="pan_link",
    child="tilt_link",
    origin=Origin(xyz=(0.0, 0.0, 0.07)),  # on top of the pan cylinder
    axis=(0.0, 1.0, 0.0),
    limit=JointLimit(
        lower=-math.pi / 2,  # -1.57
        upper=0.0,  # 0
        effort=6.0,
        velocity=1.5,
    ),
    dynamics=JointDynamics(damping=0.2, friction=0.01),
)

lens_joint = Joint(
    name="lens_joint",
    joint_type="fixed",
    parent="tilt_link",
    child="lens",
    origin=Origin(xyz=(0.09, 0.0, 0.0)),  # front face of the tilt box
)

# ---------------------------------------------
# Assemble
# ---------------------------------------------
robot = Robot("ptu")

for mat in [charcoal, dark_grey, amber]:
    robot.add_material(mat)

for link in [base_plate, pan_link, tilt_link, lens]:
    robot.add_link(link)

for joint in [pan_joint, tilt_joint, lens_joint]:
    robot.add_joint(joint)

# ---------------------------------------------
# Export
# ---------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), robot.name)
os.makedirs(out_dir, exist_ok=True)

robot.save(os.path.join(out_dir, f"{robot.name}.urdf"))
robot.save(os.path.join(out_dir, f"{robot.name}.xacro"))
robot.save_tree(os.path.join(out_dir, f"{robot.name}_tree.txt"))

print(f"Links : {len(robot.links)}")
print(f"Joints: {len(robot.joints)}")
print(f"urdf saved : {out_dir}")
print(f"xacro saved: {out_dir}")
print(f"tree saved : {out_dir}")

robot.print_tree()
