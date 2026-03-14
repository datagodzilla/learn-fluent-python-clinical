"""
test_core.py — Tests for Module 1: Python Data Model (core/).

Tests PatientRecord, FHIRBundle, and ClinicalConcept dunders.
Written alongside module implementation (hybrid testing approach).
"""

# TODO: Tests will be implemented during Module 1 deep-dive sessions

class TestPatientRecord:
    """Tests for PatientRecord special methods."""

    # TODO: test_repr — verify <Patient MRN=12345 age=67> format
    # TODO: test_str — verify human-readable string
    # TODO: test_len — verify observation count
    # TODO: test_getitem — verify indexing and slicing
    # TODO: test_iter — verify iteration over observations
    # TODO: test_eq — verify MRN-based equality
    # TODO: test_hash — verify set membership and dict key usage
    # TODO: test_contains — verify "ICD10:E11" in record

    pass


class TestFHIRBundle:
    """Tests for FHIRBundle collection protocol."""

    # TODO: test_iter, test_len, test_getitem, test_add

    pass


class TestClinicalConcept:
    """Tests for ClinicalConcept identity and hashability."""

    # TODO: test_eq, test_hash, test_set_deduplication

    pass
