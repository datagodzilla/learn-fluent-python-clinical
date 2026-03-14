"""
vocabulary.py — OMOP Vocabulary store using dict/set for O(1) lookups.

Fluent Python Chapters 2-6 | Module 2 (containers/)

Clinical Problem:
    Store 50,000+ OMOP concepts with microsecond lookup by concept_id.
    A list scan takes seconds; a dict lookup takes microseconds.
    This is the difference between real-time CDS and a slow batch job.

Structures used:
    dict, set, frozenset

Reference: OMOP CDM concept table
"""

# Standard library
from collections import defaultdict

# TODO: Implement in deep-dive session — Module 2


class OmopVocabulary:
    """Dict-based OMOP concept store with O(1) lookup.

    WHY: Container choice is an architectural decision. When you need to look up
    a concept by ID across 50,000 entries, dict gives you O(1) while list
    gives you O(n). This module teaches why hash tables matter in production.
    """

    # TODO: Implement __init__ loading concepts from JSON
    # TODO: Implement lookup_by_id(concept_id) -> ClinicalConcept
    # TODO: Implement lookup_by_code(vocabulary_id, concept_code) -> ClinicalConcept
    # TODO: Implement get_all_codes(vocabulary_id) -> frozenset of codes
    # TODO: Implement __len__, __contains__, __iter__

    pass
