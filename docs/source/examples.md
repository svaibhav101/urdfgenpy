# Examples

Three annotated robots, each in its own page.

Run any example from the repo root after `pip install -e .`:

```bash
python3 examples/simple_arm.py
python3 examples/hobu.py
python3 examples/ptu.py
```

Each script writes `.urdf`, `.xacro`, and a `_tree.txt` kinematic-tree file
to a sub-directory named after the robot.

---

```{toctree}
:hidden:

examples/simple_arm
examples/hobu
examples/ptu
```

::::{grid} 3
:gutter: 3

:::{grid-item-card} Simple Arm
:link: examples/simple_arm
:link-type: doc

```{image} _static/simple_arm_view2.png
:alt: simple_arm
:width: 100%
```

4-DOF serial manipulator. Demonstrates `Origin.above()`,
`Inertial.from_geometry()`, joint limits and dynamics.
:::

:::{grid-item-card} Hobu
:link: examples/hobu
:link-type: doc

```{image} _static/hobu_view2.png
:alt: hobu
:width: 100%
```

Differential-drive mobile base. Demonstrates `Origin.wheel()`,
multi-branch trees, and inertia safety margins.
:::

:::{grid-item-card} PTU
:link: examples/ptu
:link-type: doc

```{image} _static/ptu_view1.png
:alt: ptu
:width: 100%
```

2-DOF pan-tilt unit. Uses all three geometry primitives in one robot.
:::

::::
