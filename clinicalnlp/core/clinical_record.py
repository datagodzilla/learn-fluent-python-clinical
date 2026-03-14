"""
clinical_record.py — PatientRecord class demonstrating the Python Data Model.

Fluent Python Chapters 1-3 | Module 1 (core/)

Clinical Problem:
    Build a PatientRecord that prints meaningfully, compares by MRN,
    deduplicates in sets, iterates over observations, and works in `with` blocks.

Dunders implemented:
    __repr__, __str__, __len__, __getitem__, __iter__,
    __eq__, __hash__, __contains__, __enter__, __exit__

Reference: example-code-2e/01-data-model/ (FrenchDeck, Vector2d)
"""

# Standard library
from datetime import date

# TODO: Implement in deep-dive session — Module 1, Concept: Python Data Model
# The PatientRecord class will demonstrate how implementing special methods
# makes your objects work with Python's built-in functions and operators.


class PatientRecord:
    """A clinical patient record that speaks Python's data model protocols.

    WHY: By implementing __len__, __getitem__, __iter__, this record works
    with len(), for loops, slicing, sorted(), set(), and the `in` operator
    — for free. This is the core lesson of Fluent Python Chapter 1.

    Attributes:
        mrn: Medical Record Number (unique patient identifier)
        name: Patient full name
        dob: Date of birth
        observations: List of clinical observations (labs, vitals, diagnoses)
    """

    # TODO: Implement __init__ with mrn, name, dob, observations
    # TODO: Implement __repr__ -> <Patient MRN=12345 age=67>
    # TODO: Implement __str__ -> "Jane Doe, DOB: 1957-03-12"
    # TODO: Implement __len__ -> observation count
    # TODO: Implement __getitem__ -> record[0], record[1:3] (slicing)
    # TODO: Implement __iter__ -> for obs in record
    # TODO: Implement __eq__ -> same MRN = same patient
    # TODO: Implement __hash__ -> store in set, use as dict key
    # TODO: Implement __contains__ -> "ICD10:E11" in record

    pass
