# Development Guide

This guide covers everything needed to work on `urdfgenpy` itself: setting up
the environment, running tests, linting, and contributing changes.

---

## Setting Up a Development Environment

### Step 1: Clone the repository

```bash
git clone https://github.com/svaibhav101/urdfgenpy
cd urdfgenpy
```

### Step 2: Create and activate a virtual environment

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Step 3: Install the package in editable mode with all dev dependencies

```bash
pip install -e ".[dev,docs]"
```

This installs:

| Group | Key packages |
|-------|-------------|
| `dev` | `pytest`, `pytest-cov`, `ruff`, `mypy` |
| `docs` | `sphinx`, `furo`, `myst-parser`, `sphinx-copybutton`, `sphinx-autodoc-typehints`, `sphinx-design` |

> **Note:** Examples in `examples/` import `urdfgenpy` as an installed package.
> Always run `pip3 install -e .` before executing them - no `sys.path` manipulation
> is needed or correct in a src-layout project.

---

## Project Layout

```
urdfgenpy/
├── src/urdfgenpy/        # library source
│   ├── __init__.py       # public namespace
│   ├── robot.py          # Robot class
│   ├── link.py           # Link class
│   ├── joint.py          # Joint, JointLimit, JointDynamics, JointMimic
│   ├── geometry.py       # Box, Cylinder, Sphere
│   ├── inertia.py        # InertiaMatrix and inertia helpers
│   ├── elements.py       # Origin, Material, Visual, Collision, Inertial
│   └── exporters/
│       ├── __init__.py
│       ├── urdf.py       # URDFExporter
│       └── xacro.py      # XacroExporter
├── tests/                # pytest test suite
├── docs/                 # Sphinx documentation source
│   ├── source/
│   └── Makefile
├── examples/             # standalone usage examples
│   ├── simple_arm.py     # 4-DOF serial arm
│   ├── hobu.py           # multi-link mobile base with wheels
│   └── base.py           # minimal single-link example
└── pyproject.toml        # project metadata and tool config
```

---

## Running the Tests

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=urdfgenpy --cov-report=term-missing
```

Run a single test file:

```bash
pytest tests/test_robot.py
```

Run a single test by name:

```bash
pytest tests/test_robot.py::TestRobotBuilding::test_add_link
```

---

## Linting and Formatting

The project uses [Ruff](https://docs.astral.sh/ruff/) for both linting and
formatting (line length 99, target Python 3.10+).

Check for issues:

```bash
ruff check src/ tests/
```

Auto-fix safe issues:

```bash
ruff check --fix src/ tests/
```

Format code:

```bash
ruff format src/ tests/
```

---

## Type Checking

```bash
mypy src/urdfgenpy
```

`mypy` is configured in `pyproject.toml` (`[tool.mypy]`) with
`strict = false`. New code should avoid `Any` where possible.

---

## Full Check Suite

Run all checks before opening a PR:

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/urdfgenpy
pytest --cov=urdfgenpy
```

---

## Adding a New Feature

1. **Create or modify** the relevant module under `src/urdfgenpy/`.
2. **Export** any new public symbols from `src/urdfgenpy/__init__.py`.
3. **Write tests** in `tests/` - follow the existing class-per-feature pattern.
4. **Add a docstring** to every public class and method (Google style - see
   [Building the Documentation](contributing_docs.md)).
5. **Run the full check suite** before opening a PR.

---

## Adding a New Exporter

Exporters live in `src/urdfgenpy/exporters/`. To add a new format (e.g. SDF):

1. Create `src/urdfgenpy/exporters/sdf.py` with a class that accepts a `Robot`
   and returns an XML string.
2. Register `robot.to_sdf()` / `robot.save("model.sdf")` in `robot.py` by
   dispatching on the `.sdf` extension.
3. Add tests in `tests/test_exporters.py` (or a new file).
4. Add an API reference page at `docs/source/api/exporters.rst`.

---

## Commit and PR Guidelines

- Keep commits focused - one logical change per commit.
- Open PRs against `main`. Reference any relevant roadmap item from
  [Roadmap](roadmap.md) in the PR description.
- All checks (lint, type-check, tests) must pass before merging.
