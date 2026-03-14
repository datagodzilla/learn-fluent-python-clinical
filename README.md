# learn-fluent-python-clinical

> Learn **Fluent Python** (2nd ed., Luciano Ramalho) through clinically realistic NLP problems — FHIR, OMOP, MIMIC, Synthea, and standard terminology systems.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: In Progress](https://img.shields.io/badge/status-in%20progress-yellow.svg)]()

---

## What Is This?

A structured Python package (`clinicalnlp`) that teaches **24 chapters of Fluent Python** through **clinical informatics** problems. Instead of card decks and toy examples, you build:

- A `PatientRecord` that works with `len()`, `for`, `in`, `sorted()`, `set()`
- An `OmopVocabulary` with O(1) lookups across 50K clinical concepts
- `@audit_log` and `@validate_phi` decorators for HIPAA-compliant endpoints
- A composable `NERPipeline` using Protocol and ABC (not inheritance hell)
- A generator pipeline that streams 2M clinical notes with constant memory

## Who Is This For?

- Python developers who want to write **Pythonic** code, not "Java in Python"
- Clinical informaticists / health AI engineers who want domain-relevant examples
- Anyone studying Fluent Python who wants a hands-on project to code along with

## Project Structure

```
clinicalnlp/
├── clinicalnlp/           # Package source (5 modules)
│   ├── core/              # Module 1: Python Data Model (dunders, protocols)
│   ├── containers/        # Module 2: Data Structures (dict, set, Counter)
│   ├── pipeline/          # Module 3: Decorators & Closures
│   ├── models/            # Module 4: OOP (Protocol, ABC, composition)
│   └── streaming/         # Module 5: Generators & Async
├── tutorials/             # Standalone .py tutorial scripts
├── data/                  # Synthetic clinical data (SNOMED, LOINC, RxNorm, OMOP)
├── tests/                 # pytest suite
├── docs/                  # Documentation & learning guides
└── app/                   # Streamlit capstone app
```

## Quick Start

```bash
git clone https://github.com/datagodzilla/learn-fluent-python-clinical.git
cd learn-fluent-python-clinical
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## Modules

| # | Module | Directory | Fluent Python Chapters | Clinical Problem |
|---|--------|-----------|----------------------|-----------------|
| 1 | Python Data Model | `core/` | 1-3 | PatientRecord with dunders |
| 2 | Data Structures | `containers/` | 2-6 | OMOP vocabulary, token frequency |
| 3 | Functions & Decorators | `pipeline/` | 7-10 | HIPAA audit, PHI validation, caching |
| 4 | OOP & Protocols | `models/` | 11-16 | Composable NER pipeline |
| 5 | Generators & Async | `streaming/` | 17-24 | Stream 2M notes, async FHIR |
| 6 | Capstone | `app/` | All | Interactive Streamlit demo |

## Documentation

| Document | Description |
|----------|-------------|
| [Python Skills Roadmap](docs/python_skills_roadmap.md) | What you'll learn, skill by skill, mapped to clinical applications |
| [Core Concepts & Best Practices](docs/core_concepts_and_best_practices.md) | Pythonic principles from the book — mental models, anti-patterns, key quotes |
| [Clinical Glossary](docs/clinical_glossary.md) | FHIR, OMOP, SNOMED, LOINC, RxNorm — domain terms explained |
| [Testing Guide](docs/testing_guide.md) | pytest patterns for clinical NLP |

## Tutorial Approach

Every concept follows the same structure:

```
1. THE PROBLEM        — Clinical scenario motivating the concept
2. THE NAIVE WAY      — How a beginner would do it (and why it breaks)
3. THE FLUENT WAY     — Proper Python idiom, fully annotated
4. THE CLINICAL WIN   — What this unlocks in real-world informatics
5. RESEARCH POINTS    — What to explore independently
6. MINI EXERCISE      — One modification to try before next session
```

## Clinical Domain

This project uses standard health informatics terminology and data models:

| System | Purpose | Example |
|--------|---------|---------|
| SNOMED CT | Clinical findings | `73211009` = Diabetes mellitus |
| LOINC | Lab observations | `2339-0` = Glucose |
| RxNorm | Medications | `860975` = Metformin 500mg |
| ICD-10-CM | Diagnosis coding | `E11.9` = Type 2 DM |
| OMOP CDM | Research data model | Standardized concept lookups |
| FHIR R4 | Data exchange | Patient, Observation, Bundle |

## Data Policy

All clinical data in `data/` is **synthetic** (Synthea-style or manually crafted). No real patient data, MRNs, or PHI of any kind.

## Contributing

This is an educational project. Contributions welcome:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-improvement`)
3. Commit your changes
4. Push and open a Pull Request

## License

[MIT](LICENSE)

## Acknowledgments

- **Fluent Python, 2nd Edition** by Luciano Ramalho (O'Reilly, 2022) — the book that inspired this project
- **OMOP CDM**, **FHIR R4**, **SNOMED CT**, **LOINC**, **RxNorm** — the clinical standards that ground every example

---

*Built as part of the [ClinicalBridge](https://github.com/clinicalaiinsider) portfolio.*
