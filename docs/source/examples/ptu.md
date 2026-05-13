# PTU - 2-DOF pan-tilt unit

```{image} ../_static/ptu.gif
:alt: ptu RViz animation
:align: center
:width: 560px
```

```{image} ../_static/ptu_view1.png
:alt: ptu static view
:align: center
:width: 480px
```

## Kinematic chain

```
base_plate (box 0.14 × 0.14 × 0.025 m)
  └─ pan_joint  [revolute Z  −π … +π]
       pan_link (cylinder r=0.028, l=0.07)
         └─ tilt_joint  [revolute Y  −π/2 … 0]
              tilt_link (box 0.09 × 0.05 × 0.05 m)
                └─ lens_joint  [fixed]
                     lens (sphere r=0.022)
```

## What this example demonstrates

- **All three geometry primitives** (Box, Cylinder, Sphere) used together in one
  robot description
- **Deeply chained kinematic tree** - four links in a single serial chain
- **`JointDynamics`** (damping + friction) on both revolute joints
- **`Inertial.from_geometry()`** for every link - no manual inertia calculation
- **`robot.print_tree()`** - colour-coded ASCII tree output shown below:

```text
Robot: ptu

*  link  base_plate (box)
|
+-- joint pan_joint  [revolute]
|   \-- link  pan_link (cylinder)
|
|       +-- joint tilt_joint  [revolute]
|       |   \-- link  tilt_link (box)
|       |
|       |       \-- joint lens_joint  [fixed]
|       |           \-- link  lens (sphere)
```

## Running the example

```bash
python3 examples/ptu.py
```

Output files are written to `examples/ptu/`:

| File | Description |
|------|-------------|
| `ptu.urdf` | URDF robot description |
| `ptu.xacro` | Xacro equivalent |
| `ptu_tree.txt` | Plain-text kinematic tree |

> **Quick visualisation**: copy `ptu.urdf` into the
> [online URDF viewer](https://mymodelrobot.appspot.com/5629499534213120)
> for instant validation and 3D preview without any local ROS install.

## Source

[`examples/ptu.py`](../../../examples/ptu.py)
