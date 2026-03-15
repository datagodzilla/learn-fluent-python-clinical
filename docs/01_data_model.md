# Module 1: The Python Data Model

> Fluent Python Chapters 1-3 | Package: `src/clinicalnlp/core/`

## 1. Clinical Motivation

Every clinical system has patient records. Every developer who touches those records
needs to print them, compare them, iterate over their observations, and check if they
contain a specific diagnosis code. The question is: do you build custom methods for
each operation (`.display()`, `.contains_code()`, `.get_count()`), or do you implement
Python's built-in protocols so that `print()`, `in`, and `len()` just work?

The Python Data Model — those 80+ special methods with double underscores — is the
API that makes your objects work with the language itself. Implement `__repr__` and
`__str__`, and your objects work with print, logging, debuggers, and f-strings.
Implement `__len__` and `__getitem__`, and they work with len(), slicing, iteration,
and sorted(). This is not magic — it's a framework contract.

## 2. Key Concepts

| Session | Concept | Special Methods | Clinical Application |
|---------|---------|----------------|---------------------|
| 1.1 | String representation | `__repr__`, `__str__` | Developer debugging vs user display; HIPAA-safe logging |
| 1.2 | Sequence protocol | `__len__`, `__getitem__` | Observation count, record slicing |
| 1.3 | Iteration & membership | `__iter__`, `__contains__` | Iterate observations, check for ICD-10 codes |
| 1.4 | Identity & hashability | `__eq__`, `__hash__` | MRN-based equality, set deduplication |
| 1.5 | Collection merging | `__add__` | Merge FHIR bundles from two systems |

## 3. Session 1.1: `__repr__` and `__str__`

### The Problem

You're debugging a clinical data pipeline at 2 AM. A patient record fails validation.
You print it and see `<PatientRecord object at 0x104a8f070>`. Useless. You can't tell
which patient, what MRN, how many observations. You end up writing custom print
statements everywhere.

### The Insight

Python has a protocol for string representation. When you call `print()`, Python
calls `__str__()`. When a debugger displays your object, Python calls `__repr__()`.
Your custom `.display()` method is invisible to all of this — like building a door
that doesn't fit any standard doorframe.

### The Rules (from Ramalho, Ch 1 p.36-37)

1. **Always implement `__repr__`** — it's the fallback for `__str__` if `__str__` is missing
2. **`__repr__` should be unambiguous** — ideally match the constructor call
3. **Use `!r` in f-strings** — shows quotes around strings: `mrn='MRN-10001'` vs `mrn=MRN-10001`
4. **`__str__` is optional** — only add it when you need a different human-readable format

### What We Built

**Production code:** [src/clinicalnlp/core/clinical_record.py](../src/clinicalnlp/core/clinical_record.py)
- `PatientRecord.__repr__()` -> `PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=4)`
- `PatientRecord.__str__()` -> `Jane Doe, DOB: 1957-03-12`

**Tutorial:** [Module-1-Data-Model/01_data_model.py](../Module-1-Data-Model/01_data_model.py)
- Naive vs Fluent comparison with live output
- Clinical scenarios: HIPAA logging, ETL debugging, dashboard display

**Tests:** [tests/test_core.py](../tests/test_core.py)
- 12 tests covering `__repr__`, `__str__`, and `__init__`

### 7 Integrations from 2 Methods

By implementing `__repr__` and `__str__`, PatientRecord works with:
1. `print()` -> calls `__str__`
2. `repr()` -> calls `__repr__`
3. f-strings -> `__str__` by default, `__repr__` with `!r`
4. Logging with `%r` -> calls `__repr__`
5. Debuggers -> calls `__repr__`
6. List display -> calls `__repr__` on each element
7. Interactive REPL -> calls `__repr__`

## 4-6. Sessions 1.2-1.5

*To be completed in subsequent sessions.*

## 7. API Reference

### PatientRecord

```python
from clinicalnlp.core.clinical_record import PatientRecord

patient = PatientRecord(
    mrn="MRN-10001",          # Medical Record Number
    name="Jane Doe",          # Patient full name
    dob="1957-03-12",         # Date of birth (ISO format)
    observations=[...],       # List of observation dicts (optional)
)

repr(patient)  # PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=0)
str(patient)   # Jane Doe, DOB: 1957-03-12
```

## 8. Gotchas & Tips

- **If you only implement one, implement `__repr__`**. Python falls back from `__str__` to `__repr__`, but NOT the reverse.
- **Use `!r` in `__repr__` f-strings** to show quotes on string attributes. Without it, you can't distinguish `mrn='MRN-10001'` (string) from `mrn=MRN-10001` (could be a variable).
- **Avoid the mutable default argument trap**: `def __init__(self, observations=[])` shares one list across ALL instances. Use `None` and create inside `__init__`.
- **Don't put PHI in `__repr__`** if your logs are shipped to external monitoring (Datadog, Splunk, etc.).

## 9. Research Points

- [Python Data Model — `__repr__`](https://docs.python.org/3/reference/datamodel.html#object.__repr__)
- Fluent Python Chapter 1, p.35-37
- [f-string format specifiers: !r, !s, !a](https://docs.python.org/3/library/string.html#format-string-syntax)
- [Stack Overflow: __str__ vs __repr__](https://stackoverflow.com/questions/1436703)
