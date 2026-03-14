"""
base_extractor.py — Abstract base class for NLP entity extractors.

Fluent Python Chapters 11-13 | Module 4 (models/)

Clinical Problem:
    Enforce that every NER extractor (medication, diagnosis, procedure)
    implements .extract(text) — fail fast at class definition time,
    not at runtime.

Concepts taught:
    ABC, @abstractmethod, contract enforcement,
    when to use ABC vs Protocol

Reference: example-code-2e/13-protocol-abc/
"""

# Standard library
from abc import ABC, abstractmethod

# TODO: Implement in deep-dive session — Module 4

# TODO: BaseExtractor ABC with @abstractmethod extract(text)
# TODO: MedicationExtractor(BaseExtractor)
# TODO: DiagnosisExtractor(BaseExtractor)
# TODO: ProcedureExtractor(BaseExtractor)
# TODO: Show failure when extract() not implemented

pass
