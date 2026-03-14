"""
note_registry.py — Token frequency analysis using defaultdict and Counter.

Fluent Python Chapters 2-6 | Module 2 (containers/)

Clinical Problem:
    Count medication mentions, diagnosis codes, and NLP tokens across
    clinical notes. Group diagnoses by patient without KeyError boilerplate.

Structures used:
    defaultdict(list), Counter

Reference: OMOP note_nlp table, MIMIC discharge summaries
"""

# Standard library
from collections import Counter, defaultdict

# TODO: Implement in deep-dive session — Module 2


class NoteRegistry:
    """Registry for clinical note token analysis.

    WHY: defaultdict eliminates the if-key-not-in-dict boilerplate.
    Counter gives you .most_common() for free. These are the workhorses
    of any NLP frequency analysis pipeline.
    """

    # TODO: Implement __init__
    # TODO: Implement add_note(patient_id, note_text)
    # TODO: Implement get_token_frequencies() -> Counter
    # TODO: Implement get_patient_diagnoses(patient_id) -> list
    # TODO: Implement most_common_tokens(n) -> list of (token, count)

    pass
