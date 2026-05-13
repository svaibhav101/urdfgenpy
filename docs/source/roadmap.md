# Roadmap

This page tracks planned improvements, roughly ordered by priority.

---

## High Priority

### DH Parameters → Skeleton URDF/Xacro

Accept a [Denavit-Hartenberg](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters)
parameter table and automatically generate a kinematic skeleton - links, joints,
and correct joint origins - ready to export as `.urdf` or `.xacro`.

This bridges the gap between classical robot kinematics textbooks (where robots
are described by DH tables) and ROS/Gazebo simulation (which requires URDF).

**DH conventions supported**

| Convention | Description |
|------------|-------------|
| Standard (Craig) | `a`, `α`, `d`, `θ` - rotation then translation |
| Modified (MDH) | `a`, `α`, `d`, `θ` - translation then rotation; used by most manufacturers |

**Input format**

```python
from urdfgenpy.dh import DHTable, DHRow, DHConvention

# UR5:  Standard DH Parameters
table = DHTable(convention=DHConvention.MODIFIED, rows=[
    #   joint     a       alpha        d       theta_offset   joint_type
    DHRow( 1,    0.0,      pi/2,     0.089159,     0.0,        "revolute"),
    DHRow( 2,   -0.425,    0.0,      0.0,          0.0,        "revolute"),
    DHRow( 3,   -0.39225,  0.0,      0.0,          0.0,        "revolute"),
    DHRow( 4,    0.0,      pi/2,     0.10915,      0.0,        "revolute"),
    DHRow( 5,    0.0,     -pi/2,     0.09465,      0.0,        "revolute"),
    DHRow( 6,    0.0,      0.0,      0.0823,       0.0,        "revolute"),
])
```

**Output**

```python
robot = table.to_robot(
    name="ur5",
    link_mass=1.0,           # uniform mass per link (kg); override per-link later
    link_geometry="cylinder", # placeholder visual geometry
)
robot.save("ur5_skeleton.urdf")
robot.save("ur5_skeleton.xacro")
robot.print_tree()
```

The generated skeleton uses placeholder `Cylinder` geometry (radius=0.04,
length derived from the DH `d`/`a` parameters) and uniform mass so the file is
immediately valid and loadable in RViz / Gazebo without requiring real mesh
files.  Users replace geometry and mass values incrementally.

**Joint origin derivation**

Each `<origin>` is computed from the homogeneous transform:

```
T_i = Rot_x(α_{i-1}) · Trans_x(a_{i-1}) · Trans_z(d_i) · Rot_z(θ_i)
```

The xyz/rpy of `<origin>` are the translation and ZYX Euler angles extracted
from T_i, matching exactly what URDF expects.

**Implementation plan**

- `src/urdfgenpy/dh.py` - `DHRow`, `DHTable`, `DHConvention` dataclasses
- Pure `math` / no numpy dependency for the 4×4 matrix arithmetic
- New test file `tests/test_dh.py` - verify known robots (Panda, UR5) against
  published DH tables
- Docs page `docs/source/dh_guide.md` with a worked example

### URDF Parser (round-trip import)

Currently `urdfgenpy` is write-only.  Adding a parser would let users load an
existing `.urdf` file into the Python object model, modify it, and re-export.

**Scope**

- `Robot.from_urdf(path)` / `Robot.from_urdf_string(xml)` class methods
- Parse all elements already supported by the exporter: links, joints,
  materials, geometry primitives, inertial, limits, dynamics, mimic
- Unknown XML tags preserved as raw strings so round-trips are lossless

**Design sketch**

```python
robot = Robot.from_urdf("pr2.urdf")
robot.get_link("base_link").inertial.mass = 100.0
robot.save("pr2_modified.urdf")
```

---

### Model Validation

The builder currently only checks for duplicate names and missing
parent/child links.  A `robot.validate()` method would surface physics
and geometry errors before they cause silent sim bugs.

**Checks planned**

| Check | Why it matters |
|-------|----------------|
| Inertia matrix positive-definite | Non-PD tensors crash many physics engines |
| Single kinematic root | Multiple roots → ambiguous world frame |
| No kinematic loops | URDF is a tree; loops require `<loop_joint>` |
| Joint axis is a unit vector | Zero or unnormalised axis silently misbehaves |
| `revolute`/`prismatic` must have `<limit>` | Required by ROS controllers |
| Mass > 0 for all dynamic links | Zero mass -> infinite acceleration |

**Design sketch**

```python
errors = robot.validate()   # returns list[ValidationError]
robot.validate(strict=True) # raises on first error
```

---

## Medium Priority

### SDF Export (Gazebo)

[Simulation Description Format](http://sdformat.org/) is the native format
for Gazebo.  Key differences from URDF:

- World and model are top-level concepts (not just `<robot>`)
- Inertia is expressed relative to the link frame, not a separate `<inertial>` origin
- Joints reference link names with `<parent>` / `<child>` elements

**Scope**

- `robot.to_sdf()` and `robot.save("model.sdf")`
- `SDF` exporter class mirroring `URDFExporter`
- Support SDF 1.9+

---

### Mesh-Based Inertia

`Inertial.from_geometry()` works for primitives only.  For real robots the
collision mesh is an `.stl` or `.obj`, and computing inertia requires
integrating over the mesh volume.

**Plan**

- Optional dependency: `numpy-stl` / `trimesh`
- `Inertial.from_mesh(filename, density)` - volumetric integration
- Graceful `ImportError` if the optional dep is absent

```python
inertial = Inertial.from_mesh("arm.stl", density=1200.0)  # kg/m³
```

---

### Sensor Elements

Robots in simulation need sensor tags.  URDF supports sensors via Gazebo
plugins, but the tags themselves (e.g. `<gazebo>`, `<sensor>`) are not part
of the core URDF spec and are currently not generated.

**Scope**

- `Sensor` base class with subclasses `Camera`, `Lidar`, `Imu`, `ForceTorque`
- `Link.add_sensor(sensor)` - appends `<gazebo>` extension block
- Xacro exporter emits the sensor macros alongside the link

```python
from urdfgenpy.sensors import Camera

cam = Camera(name="head_cam", fps=30, width=640, height=480,
             fov=1.047, origin=Origin(xyz=(0.05, 0, 0)))
head_tilt_link.add_sensor(cam)
```

---

## Low Priority

### ROS 2 Package Scaffolding

When building a new robot from scratch, the user also needs a ROS 2 package
directory.  A CLI command could generate the full scaffold:

```
urdfgenpy init my_robot_description
```

Generated structure:

```bash
my_robot_description/
├── urdf/             # .urdf / .xacro files go here
├── meshes/
├── launch/
├── package.xml
├── CMakeLists.txt
└── setup.py          # if ament_python
```

**Implementation**: `click`-based CLI entry point added to `pyproject.toml`
under `[project.scripts]`.

---

## Contributing

To propose a new feature or pick up an item from this roadmap, open an issue
at the [Bug Tracker](https://github.com/svaibhav101/urdfgenpy/issues) and
reference this page.
