"""
record_store.py — NamedTuple vs @dataclass comparison for clinical records.

Fluent Python Chapter 5 | Module 2 (containers/)

Clinical Problem:
    Represent FHIR Observations as lightweight records. Compare NamedTuple
    (immutable, typed, fast) with @dataclass (mutable, more features).

Structures used:
    typing.NamedTuple, @dataclass

Reference: FHIR R4 Observation resource
"""

# Standard library
from dataclasses import dataclass, field
from typing import NamedTuple

# TODO: Implement in deep-dive session — Module 2

# TODO: LabResult as NamedTuple (immutable FHIR Observation)
# TODO: ClinicalEntity as @dataclass (mutable, with field defaults)
# TODO: Compare memory usage, immutability, type hints, defaults
# TODO: Show when to use which pattern

pass
