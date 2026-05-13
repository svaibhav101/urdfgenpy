# Simple Arm - 4-DOF serial manipulator

```{image} ../_static/simple_arm.gif
:alt: simple_arm RViz animation
:align: center
:width: 560px
```

::::{grid} 2
:gutter: 2

:::{grid-item}
```{image} ../_static/simple_arm_view1.png
:alt: simple_arm front view
:width: 100%
```
:::
:::{grid-item}
```{image} ../_static/simple_arm_view2.png
:alt: simple_arm side view
:width: 100%
```
:::
::::

```{image} ../_static/simple_arm_terminal.png
:alt: simple_arm kinematic tree in terminal
:align: center
:width: 480px
```

## Kinematic chain

```
base_link (box)
  └─ base_shoulder_joint  [revolute Z]
       shoulder_link (cylinder)
         └─ shoulder_upper_arm_joint  [revolute Y]
              upper_arm_link (cylinder)
                └─ upper_arm_forearm_joint  [revolute Y]
                     forearm_link (cylinder)
                       └─ forearm_ee_joint  [fixed]
                            end_effector_link (sphere)
```

## What this example demonstrates

- **`Origin.above(geometry)`** - lifts each link so its bottom face sits at z = 0,
  avoiding manual offset arithmetic
- **`Inertial.from_geometry()`** - auto-dispatches to the correct inertia formula
  (box, cylinder, or sphere) from the geometry object alone
- **`JointLimit`** and **`JointDynamics`** on every revolute joint
- **`robot.save()`** writing both `.urdf` and `.xacro` by inferring the format
  from the file extension

## Running the example

```bash
python3 examples/simple_arm.py
```

Output files are written to `examples/simple_arm/`:

| File | Description |
|------|-------------|
| `simple_arm.urdf` | URDF robot description |
| `simple_arm.xacro` | Xacro equivalent |
| `simple_arm_tree.txt` | Plain-text kinematic tree |

> **Quick visualisation**: copy `simple_arm.urdf` into the
> [online URDF viewer](https://mymodelrobot.appspot.com/5629499534213120)
> for instant validation and 3D preview without any local ROS install.

## Source

[`examples/simple_arm.py`](../../../examples/simple_arm.py)
