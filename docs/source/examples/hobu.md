# Hobu - Differential-drive mobile robot

::::{grid} 2
:gutter: 2

:::{grid-item}
```{image} ../_static/hobu_view1.png
:alt: hobu front-right view
:width: 100%
```
:::
:::{grid-item}
```{image} ../_static/hobu_view2.png
:alt: hobu side view
:width: 100%
```
:::
::::

```{image} ../_static/hobu_terminal.png
:alt: hobu kinematic tree in terminal
:align: center
:width: 480px
```

## Kinematic chain

```
base_footprint  (virtual root - no geometry)
  └─ base_joint  [fixed]
       base_link (box 0.6 × 0.4 × 0.2 m)
         ├─ base_right_wheel_joint  [continuous Y]
         │    right_wheel_link (cylinder r=0.1, l=0.05)
         ├─ base_left_wheel_joint  [continuous Y]
         │    left_wheel_link  (cylinder r=0.1, l=0.05)
         └─ base_caster_wheel_joint  [fixed]
              caster_wheel_link (sphere r=0.05)
```

## What this example demonstrates

- **`Origin.wheel()`** - applies a −π/2 roll so a URDF cylinder's Z-axis aligns
  with Y, the standard wheel orientation in ROS
- **Per-shape inertia factories** (`Inertial.from_box`, `Inertial.from_cylinder`,
  `Inertial.from_sphere`) with an `inertia_multiply` safety margin
- **Multi-branch kinematic trees** - two continuous joints hang off the same
  parent link
- **Virtual root link** - `base_footprint` carries no geometry and serves as the
  world-fixed anchor (standard ROS convention for mobile bases)

## Running the example

```bash
python3 examples/hobu.py
```

Output files are written to `examples/hobu/`:

| File | Description |
|------|-------------|
| `hobu.urdf` | URDF robot description |
| `hobu.xacro` | Xacro equivalent |
| `hobu_tree.txt` | Plain-text kinematic tree |

> **Quick visualisation**: copy `hobu.urdf` into the
> [online URDF viewer](https://mymodelrobot.appspot.com/5629499534213120)
> for instant validation and 3D preview without any local ROS install.

## Source

[`examples/hobu.py`](../../../examples/hobu.py)
