# Python Packaging Guide

> How this project is structured, built, installed, and used — following modern Python packaging best practices.

---

## Why the `src/` Layout?

This project uses the **`src/` layout**, which is the layout recommended by the [Python Packaging Authority (PyPA)](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) and used by major Python projects like `pytest`, `pip`, `rich`, `httpx`, and `pydantic`.

### The Problem with Flat Layout

```
# Flat layout — the package is at the project root
my-project/
├── clinicalnlp/        # Package source AND importable directory
│   ├── __init__.py
│   └── core/
├── tests/
└── pyproject.toml
```

When you run `python` or `pytest` from the project root, Python adds the current directory to `sys.path`. This means:

```python
import clinicalnlp  # Imports from the LOCAL directory, not the installed package
```

This creates a **silent bug**: your tests pass because they import local source files directly, but they might fail for users who `pip install` your package — because the installed version could be missing files, have different paths, or have build-time transformations.

### How `src/` Solves It

```
# src/ layout — package is nested one level deeper
my-project/
├── src/
│   └── clinicalnlp/    # Package source (NOT directly importable)
│       ├── __init__.py
│       └── core/
├── tests/
└── pyproject.toml
```

Now `import clinicalnlp` **cannot** find `src/clinicalnlp/` by accident — it can only import the **installed** package. This guarantees that what works locally also works for users.

---

## Project Structure Explained

```
learn-fluent-python-clinical/
│
├── src/                               # PACKAGE SOURCE
│   └── clinicalnlp/                   #   The installable Python package
│       ├── __init__.py                #   Package root (version, metadata)
│       ├── core/                      #   Module 1: Python Data Model
│       │   ├── __init__.py
│       │   ├── clinical_record.py     #     PatientRecord class
│       │   ├── fhir_bundle.py         #     FHIRBundle class
│       │   └── concept.py             #     ClinicalConcept class
│       ├── containers/                #   Module 2: Data Structures
│       │   ├── __init__.py
│       │   ├── vocabulary.py          #     OmopVocabulary
│       │   ├── note_registry.py       #     NoteRegistry
│       │   └── record_store.py        #     NamedTuple vs @dataclass
│       ├── pipeline/                  #   Module 3: Decorators & Closures
│       │   ├── __init__.py
│       │   ├── decorators.py          #     @audit_log, @validate_phi
│       │   ├── transforms.py          #     Closures, partial, registry
│       │   └── fastapi_layer.py       #     Production endpoint patterns
│       ├── models/                    #   Module 4: OOP & Protocols
│       │   ├── __init__.py
│       │   ├── protocols.py           #     Extractable, Normalizable
│       │   ├── base_extractor.py      #     ABC with @abstractmethod
│       │   ├── ner_pipeline.py        #     Composition pattern
│       │   └── fhir_resource.py       #     __slots__, descriptors
│       └── streaming/                 #   Module 5: Generators & Async
│           ├── __init__.py
│           ├── generators.py          #     yield-based streaming
│           ├── async_fhir.py          #     async/await FHIR calls
│           ├── context_managers.py    #     with statement patterns
│           └── metaclasses.py         #     __init_subclass__
│
├── Module-1-Data-Model/               # TUTORIALS (not part of package)
├── Module-2-Data-Structures/          #   Each folder contains a standalone
├── Module-3-Functions-Decorators/     #   .py tutorial script that imports
├── Module-4-OOP-Protocols/            #   from the installed clinicalnlp
├── Module-5-Generators-Async/         #   package
├── Module-6-Capstone/                 #   Streamlit demo app
│
├── data/                              # SYNTHETIC DATA
│   ├── sample_notes.json              #   MIMIC-style discharge summaries
│   ├── snomed_concepts.json           #   20 SNOMED CT codes
│   ├── loinc_codes.json               #   15 LOINC lab codes
│   ├── rxnorm_drugs.json              #   15 RxNorm medications
│   └── omop_vocabulary.json           #   20 OMOP concept mappings
│
├── tests/                             # TEST SUITE
│   ├── conftest.py                    #   Shared fixtures
│   ├── test_core.py                   #   Module 1 tests
│   ├── test_containers.py             #   Module 2 tests
│   ├── test_pipeline.py               #   Module 3 tests
│   ├── test_models.py                 #   Module 4 tests
│   └── test_streaming.py              #   Module 5 tests
│
├── docs/                              # DOCUMENTATION
│
├── pyproject.toml                     # Build config (hatchling)
├── uv.lock                            # Locked dependencies (reproducible)
├── .python-version                    # Python 3.12 (used by uv)
├── pytest.ini                         # Test configuration
├── requirements.txt                   # Fallback pip dependencies
├── LICENSE                            # MIT
└── README.md
```

### What goes where?

| Directory | Contains | Part of installed package? |
|-----------|----------|--------------------------|
| `src/clinicalnlp/` | Python source code | **Yes** — this is what `pip install` installs |
| `Module-*/` | Tutorial scripts | No — educational, imports the installed package |
| `data/` | Synthetic JSON files | No — loaded at runtime via file paths |
| `tests/` | pytest test suite | No — development only |
| `docs/` | Documentation | No — reference material |

---

## How to Build

### Development Install (editable)

This is what you use while developing. Changes to `src/clinicalnlp/` are reflected immediately without reinstalling.

```bash
# Clone the repo
git clone https://github.com/datagodzilla/learn-fluent-python-clinical.git
cd learn-fluent-python-clinical

# Using uv (recommended — 10-100x faster than pip)
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Or using pip
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

The `-e` flag means **editable install**: Python creates a link from the virtual environment to your `src/clinicalnlp/` directory. When you edit source files, the changes are available immediately — no reinstall needed.

The `.[dev]` part installs the package plus its development dependencies (pytest, ruff, ipython, etc.).

### Build a Distribution (wheel)

If you want to create a distributable package:

```bash
# Build the wheel and sdist
uv build

# Output goes to dist/
ls dist/
# clinicalnlp-0.1.0-py3-none-any.whl
# clinicalnlp-0.1.0.tar.gz
```

### Publish to PyPI (optional)

```bash
# Upload to PyPI (requires account + API token)
uv publish

# Or using twine
pip install twine
twine upload dist/*
```

---

## How to Install

### From GitHub (anyone)

```bash
# Install directly from the GitHub repo
pip install git+https://github.com/datagodzilla/learn-fluent-python-clinical.git

# Or with uv
uv pip install git+https://github.com/datagodzilla/learn-fluent-python-clinical.git
```

### From PyPI (if published)

```bash
pip install clinicalnlp
# or
uv pip install clinicalnlp
```

### From Local Clone (developers)

```bash
cd learn-fluent-python-clinical
uv pip install -e ".[dev]"
```

---

## How to Use

Once installed (by any method above), the package is available anywhere in your Python environment:

### Basic Import

```python
from clinicalnlp.core.clinical_record import PatientRecord
from clinicalnlp.containers.vocabulary import OmopVocabulary
from clinicalnlp.pipeline.decorators import audit_log

# Create a patient record
patient = PatientRecord(mrn="MRN-10001", name="Jane Doe", dob="1957-03-12")

# Use Python protocols — these all work because of special methods
print(len(patient))           # __len__ → observation count
print(repr(patient))          # __repr__ → <Patient MRN=10001 age=67>
for obs in patient:           # __iter__ → iterate observations
    print(obs)
```

### In a FastAPI Application

```python
from fastapi import FastAPI
from clinicalnlp.pipeline.decorators import audit_log, validate_phi
from clinicalnlp.containers.vocabulary import OmopVocabulary

app = FastAPI()
vocab = OmopVocabulary("data/omop_vocabulary.json")

@app.get("/concept/{concept_id}")
@audit_log
@validate_phi
async def lookup_concept(concept_id: int):
    return vocab.lookup_by_id(concept_id)
```

### In a Script or Notebook

```python
from clinicalnlp.streaming.generators import stream_notes
from clinicalnlp.models.ner_pipeline import NERPipeline

# Stream 2M notes with constant memory
pipeline = NERPipeline(extractors=[...])
for note in stream_notes("data/sample_notes.json"):
    entities = pipeline.process(note)
    print(entities)
```

### Run Tutorials

```bash
# Each Module folder has a standalone tutorial
uv run python Module-1-Data-Model/01_data_model.py
uv run python Module-2-Data-Structures/02_data_structures.py
```

### Run Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=clinicalnlp --cov-report=term-missing

# Single module
uv run pytest tests/test_core.py -v
```

---

## Key Configuration Files

### `pyproject.toml` — The Single Source of Truth

```toml
[project]
name = "clinicalnlp"                    # Package name on PyPI
version = "0.1.0"                       # Semantic versioning
requires-python = ">=3.10"              # Minimum Python version
dependencies = [...]                    # Runtime dependencies

[build-system]
requires = ["hatchling"]                # Build backend
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/clinicalnlp"]          # Tell hatchling where the package is

[tool.pytest.ini_options]
pythonpath = ["src"]                    # Tell pytest where to find imports

[tool.ruff]
src = ["src"]                           # Tell ruff where source code lives
```

### `uv.lock` — Reproducible Dependencies

Generated by `uv lock`. Contains the exact versions of all 83 transitive dependencies. Ensures every developer and CI system gets identical environments.

```bash
uv lock          # Generate/update the lock file
uv sync          # Install exactly what's in the lock file
```

### `.python-version` — Python Version Pin

```
3.12
```

Used by `uv` to automatically select the right Python interpreter.

---

## Why `uv` Instead of `pip`?

| Feature | pip | uv |
|---------|-----|-----|
| **Speed** | Baseline | 10-100x faster |
| **Lock file** | Requires pip-tools | Built-in (`uv lock`) |
| **Resolution** | Sometimes inconsistent | Deterministic resolver |
| **Virtual env** | `python -m venv` | `uv venv` (faster) |
| **Python management** | External (pyenv, etc.) | Built-in (`uv python install`) |

`uv` is a drop-in replacement for `pip` + `pip-tools` + `virtualenv` + `pyenv` — written in Rust, developed by Astral (the creators of `ruff`).

---

## Common Workflows

### Add a new dependency

```bash
# Add to pyproject.toml [project.dependencies], then:
uv lock          # Regenerate lock file
uv sync          # Install the new dependency
```

### Update all dependencies

```bash
uv lock --upgrade
uv sync
```

### Run any command in the project environment

```bash
uv run python my_script.py
uv run pytest
uv run ipython
uv run ruff check src/
```

---

## Further Reading

- [PyPA Packaging Guide](https://packaging.python.org/) — Official Python packaging documentation
- [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) — PyPA's explanation of why `src/` is preferred
- [Hatchling docs](https://hatch.pypa.io/) — The build backend we use
- [uv docs](https://docs.astral.sh/uv/) — The package manager we use
- [PEP 517](https://peps.python.org/pep-0517/) — Build system interface
- [PEP 621](https://peps.python.org/pep-0621/) — Project metadata in pyproject.toml
