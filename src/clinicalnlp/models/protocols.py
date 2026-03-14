"""
protocols.py — Structural typing with Protocol for clinical NLP contracts.

Fluent Python Chapters 11-13 | Module 4 (models/)

Clinical Problem:
    Define what it means to be "extractable" or "normalizable" without
    forcing inheritance. Any object with the right methods qualifies.

Concepts taught:
    typing.Protocol, @runtime_checkable, structural subtyping,
    duck typing formalized

Reference: example-code-2e/13-protocol-abc/
"""

# Standard library
from typing import Protocol, runtime_checkable

# TODO: Implement in deep-dive session — Module 4

# TODO: Extractable protocol — anything with .extract(text) -> list
# TODO: Normalizable protocol — anything with .normalize(entity) -> str
# TODO: Serializable protocol — anything with .to_dict() -> dict
# TODO: Show isinstance() checks with @runtime_checkable

pass
