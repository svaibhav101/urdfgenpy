# urdfgenpy

A Python library for programmatically generating [URDF](http://wiki.ros.org/urdf) (Unified Robot Description Format) and [Xacro](http://wiki.ros.org/xacro) robot description files.

## Features

- Build robot kinematic trees with **links**, **joints**, and **materials** using a clean Python API
- Geometry primitives: **Box**, **Cylinder**, **Sphere**
- Automatic inertia calculation from geometry and mass
- Convenience helpers: `Origin.above()` (lift geometry to sit on a plane), `Origin.wheel()` (orient cylinder as a wheel)
- Export to `.urdf` or `.xacro` - format is inferred from the file extension
- ASCII kinematic tree visualisation with `robot.print_tree()` / `robot.tree_string()`

## Installation

```bash
pip3 install urdfgenpy
```

Or from source:

```bash
git clone https://github.com/svaibhav101/urdfgenpy
cd urdfgenpy
pip3 install -e ".[dev,docs]"
```

## Quick Start

```python
from urdfgenpy import (
    Robot, Link, Joint, JointLimit, JointDynamics,
    Box, Cylinder, Sphere,
    Origin, Material, Visual, Collision, Inertial,
)

# --- Materials ---
grey = Material("grey", rgba=(0.5, 0.5, 0.5, 1.0))
blue = Material("blue", rgba=(0.0, 0.3, 0.8, 1.0))

# --- Base link: flat box ---
base_box = Box(length=0.2, width=0.2, height=0.05)
base_link = Link("base_link")
base_link.add_visual(Visual(geometry=base_box, origin=Origin.above(base_box), material=grey))
base_link.add_collision(Collision(geometry=base_box, origin=Origin.above(base_box)))
base_link.set_inertial(Inertial.from_geometry(mass=1.0, geometry=base_box))

# --- Shoulder link: upright cylinder ---
shoulder_cyl = Cylinder(radius=0.04, length=0.15)
shoulder_link = Link("shoulder_link")
shoulder_link.add_visual(Visual(geometry=shoulder_cyl, origin=Origin.above(shoulder_cyl), material=blue))
shoulder_link.add_collision(Collision(geometry=shoulder_cyl, origin=Origin.above(shoulder_cyl)))
shoulder_link.set_inertial(Inertial.from_geometry(mass=0.5, geometry=shoulder_cyl))

# --- Joint ---
joint = Joint(
    name="base_shoulder_joint",
    joint_type="revolute",
    parent="base_link",
    child="shoulder_link",
    origin=Origin(xyz=(0.0, 0.0, 0.05)),
    axis=(0.0, 0.0, 1.0),
    limit=JointLimit(lower=-3.14, upper=3.14, effort=50.0, velocity=2.0),
    dynamics=JointDynamics(damping=0.5, friction=0.01),
)

# --- Assemble and export ---
robot = Robot("my_robot")
robot.add_material(grey).add_material(blue)
robot.add_link(base_link).add_link(shoulder_link)
robot.add_joint(joint)

robot.save("my_robot.urdf")   # or .xacro
robot.print_tree()
```

## API Reference

### `Robot`

| Method | Description |
|--------|-------------|
| `add_link(link)` | Add a `Link`; returns `self` for chaining |
| `add_joint(joint)` | Add a `Joint`; validates parent/child exist |
| `add_material(material)` | Register a global `Material` |
| `to_urdf(output_path=None)` | Return URDF XML string; optionally write file |
| `to_xacro(output_path=None)` | Return Xacro XML string; optionally write file |
| `save(output_path)` | Write `.urdf` or `.xacro` based on extension |
| `tree_string()` | Plain-text ASCII kinematic tree |
| `save_tree(output_path)` | Write `tree_string()` to file |
| `print_tree()` | Print coloured ASCII tree to stdout |

### Geometry

| Class | Parameters |
|-------|------------|
| `Box(length, width, height)` | Axis-aligned box |
| `Cylinder(radius, length)` | Cylinder along Z-axis |
| `Sphere(radius)` | Sphere |

### `Origin`

```python
Origin(xyz=(0,0,0), rpy=(0,0,0))           # explicit
Origin.above(geometry, xy=(0,0), rpy=...)  # lift so bottom sits at z=0
Origin.wheel(xy=(0,0), z=0)                # -pi/2 roll, cylinder becomes wheel
```

### `Inertial`

```python
Inertial.from_geometry(mass, geometry)               # auto-compute from Box/Cylinder/Sphere
Inertial.from_box(mass, length, w, h)
Inertial.from_cylinder(mass, radius, length)
Inertial.from_sphere(mass, radius)
Inertial(mass, matrix=InertiaMatrix(...))            # manual
```

### `Joint`

```python
Joint(
    name, joint_type,          # "fixed" | "revolute" | "continuous" | "prismatic" | ...
    parent, child,             # link names
    origin=Origin(),
    axis=(1, 0, 0),
    limit=JointLimit(lower, upper, effort, velocity),    # optional
    dynamics=JointDynamics(damping, friction),           # optional
    mimic=JointMimic(joint, multiplier, offset),         # optional
)
```

## Examples

Install the package first, then run any example directly:

```bash
pip3 install -e ".[dev]"
python examples/simple_arm.py   # 4-DOF serial arm
python examples/hobu.py         # multi-link mobile base with wheels
python examples/base.py         # minimal single-link robot
```

Each script writes its output files (`.urdf`, `.xacro`, `_tree.txt`) into a
subdirectory named after the robot.

## Running Tests

```bash
pip3 install -e ".[dev]"
pytest
```

Run with coverage:

```bash
pytest --cov=urdfgenpy --cov-report=term-missing
```

## Building Documentation

```bash
pip3 install -e ".[docs]"
cd docs
make html
# open docs/_build/html/index.html
```

## Project Structure

```
urdfgenpy/
├── src/urdfgenpy/        # library source
│   ├── robot.py          # Robot class
│   ├── link.py           # Link class
│   ├── joint.py          # Joint, JointLimit, JointDynamics, JointMimic
│   ├── geometry.py       # Box, Cylinder, Sphere
│   ├── inertia.py        # InertiaMatrix and inertia helpers
│   ├── elements.py       # Origin, Material, Visual, Collision, Inertial
│   └── exporters/        # URDFExporter, XacroExporter
├── tests/                # pytest test suite (77 tests)
├── docs/                 # Sphinx documentation source
├── examples/             # standalone usage examples
│   ├── simple_arm.py     # 4-DOF serial arm
│   ├── hobu.py           # multi-link mobile base with wheels
│   └── base.py           # minimal single-link example
└── pyproject.toml        # project metadata and tool config
```

## Roadmap

See [docs/source/roadmap.md](docs/source/roadmap.md) for the full list. Top items:

| Priority | Feature |
|----------|---------|
| High | DH parameters ->                   skeleton URDF/Xacro - generate kinematic chain from a DH table |
| High | URDF parser - round-trip import of existing `.urdf` files |
| High | Model validation - positive-definite inertia check, joint-limit sanity |
| Medium | SDF export - Gazebo Simulation Description Format |
| Medium | Mesh-based inertia - auto-compute from `.stl`/`.obj` + density |
| Medium | Sensor elements - `<camera>`, `<lidar>`, `<imu>` tags |
| Low | ROS 2 scaffolding - generate `package.xml` + `CMakeLists.txt` |
| Low | Visualiser - quick matplotlib / rerun 3-D preview |

## License

`urdfgenpy` is made available under the MIT License. For more details, see [LICENSE](./LICENSE)
