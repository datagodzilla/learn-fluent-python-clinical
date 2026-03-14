"""
concept.py — ClinicalConcept for terminology code identity and deduplication.

Fluent Python Chapters 1-3 | Module 1 (core/)

Clinical Problem:
    SNOMED CT, LOINC, and RxNorm codes must be comparable and hashable
    so they can be stored in sets and used as dictionary keys for O(1) lookup.

Dunders implemented:
    __eq__, __hash__, __repr__, __str__

Reference: OMOP CDM concept table (concept_id, concept_code, vocabulary_id)
"""

# TODO: Implement in deep-dive session — Module 1


class ClinicalConcept:
    """A terminology code (SNOMED, LOINC, RxNorm) with identity semantics.

    WHY: Two concepts with the same vocabulary_id + concept_code ARE the same
    concept, regardless of which object instance holds them. Implementing
    __eq__ and __hash__ correctly is what makes set() deduplication and
    dict key lookup work. This is the hashability contract from Chapter 3.
    """

    # TODO: Implement __init__ with concept_id, concept_code, vocabulary_id, concept_name
    # TODO: Implement __eq__ -> same vocabulary_id + concept_code = same concept
    # TODO: Implement __hash__ -> hash(vocabulary_id, concept_code)
    # TODO: Implement __repr__ -> <Concept SNOMED:73211009 'Diabetes mellitus'>

    pass
