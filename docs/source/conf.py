import os
import sys
from importlib.metadata import version as _pkg_version

sys.path.insert(0, os.path.abspath("../../src"))

# ---------------------------------------------------------------------------
# Project metadata
# ---------------------------------------------------------------------------
project = "urdfgenpy"
author = "Vaibhav Shende"
copyright = "2024, Vaibhav Shende"

try:
    release = _pkg_version("urdfgenpy")
except Exception:
    release = "0.0.0+unknown"

version = ".".join(release.split(".")[:2])   # e.g. "0.1" from "0.1.0"

# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------
extensions = [
    # Core autodoc
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    # Google / NumPy docstring support
    "sphinx.ext.napoleon",
    # "View source" links on API pages
    "sphinx.ext.viewcode",
    # Cross-references to stdlib
    "sphinx.ext.intersphinx",
    # Pull PEP 484 type annotations into signatures and parameter tables
    "sphinx_autodoc_typehints",
    # Copy button on every code block
    "sphinx_copybutton",
    # Markdown (.md) support
    "myst_parser",
    # Grid layouts and card directives on the landing page
    "sphinx_design",
    "myst_parser",
]

# ---------------------------------------------------------------------------
# autodoc / autosummary
# ---------------------------------------------------------------------------
autosummary_generate = True

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}

# Keep __init__ docstrings on the class page
autoclass_content = "both"

# sphinx-autodoc-typehints options
always_document_param_types = True
typehints_fully_qualified = False
simplify_optional_unions = True

# ---------------------------------------------------------------------------
# Napoleon (docstring style)
# ---------------------------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_use_rtype = False          # puts return type in signature, not a section

# ---------------------------------------------------------------------------
# MyST (Markdown)
# ---------------------------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",      # ::: fences as an alternative to ```
    "deflist",          # definition lists
    "fieldlist",        # RST-style field lists in Markdown
    "tasklist",         # - [ ] / - [x] checkboxes
    "smartquotes",      # curly quotes
    "substitution",     # |var| substitution syntax
]

myst_heading_anchors = 3    # auto-anchor h1–h3

# ---------------------------------------------------------------------------
# Intersphinx
# ---------------------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# ---------------------------------------------------------------------------
# Source handling
# ---------------------------------------------------------------------------
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Suppress noisy "duplicate label" warnings from autosummary stubs
suppress_warnings = ["autosummary.import_cycle"]

# ---------------------------------------------------------------------------
# HTML output - Furo theme
# ---------------------------------------------------------------------------
html_theme = "furo"
# html_title = f"urdfgenpy {version}"
html_title = "urdfgenpy"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "source_repository": "https://github.com/svaibhav101/urdfgenpy/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/svaibhav101/urdfgenpy",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0"
                     viewBox="0 0 16 16" height="1em" width="1em"
                     xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd"
                    d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                       0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                       -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87
                       2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95
                       0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21
                       2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04
                       2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82
                       2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48
                       0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8
                       c0-4.42-3.58-8-8-8z"/>
                </svg>
            """,
            "class": "",
        },
    ],
}

# ---------------------------------------------------------------------------
# sphinx-copybutton
# ---------------------------------------------------------------------------
# Strip shell prompts and output lines from copied text
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = False
