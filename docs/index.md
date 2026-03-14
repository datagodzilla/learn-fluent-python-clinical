# clinicalnlp Documentation

> Learn Fluent Python through Clinical Informatics NLP Problems

## Quickstart

```bash
cd learn-fluent-python-clinical/
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uv run pytest tests/ -v
```

## Module Documentation

| Module | Document | Status |
|--------|----------|--------|
| 1. Python Data Model | [01_data_model.md](01_data_model.md) | Pending |
| 2. Data Structures | [02_data_structures.md](02_data_structures.md) | Pending |
| 3. Functions & Decorators | [03_functions_decorators.md](03_functions_decorators.md) | Pending |
| 4. OOP & Protocols | [04_oop_protocols.md](04_oop_protocols.md) | Pending |
| 5. Generators & Async | [05_generators_async.md](05_generators_async.md) | Pending |
| 6. Capstone | [06_capstone.md](06_capstone.md) | Pending |

## Reference Documents

- [Python Skills Roadmap](python_skills_roadmap.md) — What you will learn and why
- [Core Concepts & Best Practices](core_concepts_and_best_practices.md) — Pythonic principles from Fluent Python
- [Testing Guide](testing_guide.md) — pytest patterns and async testing
- [API Reference](api_reference.md) — Classes, functions, parameters
- [Clinical Glossary](clinical_glossary.md) — Domain terms: FHIR, OMOP, SNOMED, etc.

## Project Structure

```
learn-fluent-python-clinical/
├── clinicalnlp/                       # Package source
│   ├── core/                          # Module 1: Python Data Model
│   ├── containers/                    # Module 2: Data Structures
│   ├── pipeline/                      # Module 3: Functions & Decorators
│   ├── models/                        # Module 4: OOP & Protocols
│   └── streaming/                     # Module 5: Generators & Async
├── Module-1-Data-Model/               # Tutorial scripts
├── Module-2-Data-Structures/
├── Module-3-Functions-Decorators/
├── Module-4-OOP-Protocols/
├── Module-5-Generators-Async/
├── Module-6-Capstone/                 # Streamlit app
├── data/                              # Synthetic clinical data (JSON)
├── tests/                             # pytest suite
└── docs/                              # This documentation
```
