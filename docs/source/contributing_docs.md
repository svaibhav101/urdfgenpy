# Building the Documentation

This guide explains how to build the HTML documentation locally from source.

## Prerequisites

Install the docs dependencies (included in the `docs` extra):

```bash
pip3 install -e ".[docs]"
```

This installs:

| Package | Purpose |
|---|---|
| `sphinx` | Documentation generator |
| `furo` | Read the Docs HTML theme |
| `myst-parser` | Markdown support in Sphinx |

---

## Step-by-Step: Build HTML Docs

### Step 1: Navigate to the `docs/` directory

```bash
cd docs
```

### Step 2: Clean any previous build (optional but recommended)

```bash
# Linux / macOS
make clean

# Windows  (Not tested)
make.bat clean
```

### Step 3: Build the HTML output

```bash
# Linux / macOS
make html

# Windows (Not tested)
make.bat html
```

Sphinx reads source files from `docs/source/` and writes the built site to `docs/_build/html/`.

### Step 4: Open the docs in your browser

```bash
# Linux
xdg-open _build/html/index.html

# macOS
open _build/html/index.html

# Windows
start _build/html/index.html
```

---

## Auto-Generated API Reference

The API reference under `docs/source/api/` is generated automatically from
docstrings using `sphinx.ext.autodoc` and `sphinx.ext.autosummary`.

When you add or update a docstring in `src/urdfgenpy/`, re-running `make html`
picks up the changes - no manual edits to `.rst` files are needed.

### Adding a new module to the API reference

1. Create a new `.rst` file in `docs/source/api/`, e.g. `mymodule.rst`,
   using the same structure as the existing files in that directory - a
   section title followed by an `automodule` directive pointing at the
   fully-qualified module name, with `:members:`, `:undoc-members:`, and
   `:show-inheritance:` options.

2. Add it to `docs/source/api/index.rst` under the toctree.

3. Rebuild: `make html`.

---

## Docstring Style

The project supports both **Google** and **NumPy** style docstrings
(configured via `napoleon_google_docstring = True` and
`napoleon_numpy_docstring = True` in `conf.py`).

**Google style example:**

```python
def from_box(mass: float, l: float, w: float, h: float) -> "Inertial":
    """Compute inertia for a solid box.

    Args:
        mass: Total mass in kilograms.
        l: Length along the X axis.
        w: Width along the Y axis.
        h: Height along the Z axis.

    Returns:
        Inertial object with computed mass and inertia tensor.
    """
```

---

## Troubleshooting

**`sphinx-build: command not found`**
Install the docs dependencies: `pip3 install -e ".[docs]"`.

**`ModuleNotFoundError: No module named 'urdfgenpy'`**
Install the package in editable mode first: `pip3 install -e .`

**Stale output after editing `conf.py`**
Run `make clean` then `make html` to force a full rebuild.
