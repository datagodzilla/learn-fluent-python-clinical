"""
test_core.py — Tests for Module 1: Python Data Model (core/).

Tests PatientRecord, FHIRBundle, and ClinicalConcept dunders.
Written alongside module implementation (hybrid testing approach).
"""

from clinicalnlp.core.clinical_record import PatientRecord


# --- Session 1.1: __repr__ and __str__ ---

class TestPatientRecordRepr:
    """Tests for PatientRecord.__repr__ — developer representation."""

    def test_repr_contains_class_name(self):
        """repr should start with the class name for unambiguous identification."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        assert repr(patient).startswith("PatientRecord(")

    def test_repr_contains_mrn_with_quotes(self):
        """repr should show mrn with quotes (via !r) to indicate it's a string."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        assert "mrn='MRN-10001'" in repr(patient)

    def test_repr_contains_observation_count(self):
        """repr should show observation count, not the full list."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12", [
            {"code": "ICD10:E11.9", "description": "Type 2 diabetes"},
            {"code": "ICD10:I10", "description": "Hypertension"},
        ])
        assert "obs=2" in repr(patient)

    def test_repr_zero_observations(self):
        """repr should show obs=0 for a patient with no observations."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        assert "obs=0" in repr(patient)

    def test_repr_in_fstring_with_r_flag(self):
        """f-string with !r flag should call __repr__."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        result = f"{patient!r}"
        assert "PatientRecord(" in result
        assert "mrn=" in result


class TestPatientRecordStr:
    """Tests for PatientRecord.__str__ — human-readable representation."""

    def test_str_shows_name_and_dob(self):
        """str should show patient name and date of birth."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        assert str(patient) == "Jane Doe, DOB: 1957-03-12"

    def test_str_used_by_print(self):
        """print() calls __str__, which should be human-readable."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        # print() calls str() internally
        assert str(patient) == "Jane Doe, DOB: 1957-03-12"

    def test_str_does_not_contain_class_name(self):
        """str output should be for humans — no Python implementation details."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        assert "PatientRecord" not in str(patient)

    def test_str_in_fstring_default(self):
        """f-string without !r flag should call __str__."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        result = f"{patient}"
        assert result == "Jane Doe, DOB: 1957-03-12"


class TestPatientRecordInit:
    """Tests for PatientRecord.__init__ — construction."""

    def test_default_observations_is_empty_list(self):
        """observations should default to empty list, not None."""
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        assert patient.observations == []
        assert isinstance(patient.observations, list)

    def test_no_mutable_default_sharing(self):
        """Two patients should NOT share the same observations list."""
        patient_a = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
        patient_b = PatientRecord("MRN-10002", "John Smith", "1970-08-25")
        patient_a.observations.append({"code": "ICD10:E11.9"})
        assert len(patient_b.observations) == 0  # must not be affected

    def test_observations_accepted(self):
        """Observations passed at init should be stored."""
        obs = [{"code": "ICD10:E11.9", "description": "Type 2 DM"}]
        patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12", obs)
        assert len(patient.observations) == 1


# --- Sessions 1.2-1.5: Future tests ---

class TestPatientRecordSequence:
    """Tests for __len__, __getitem__ — Session 1.2."""
    # TODO: test_len, test_getitem_index, test_getitem_slice
    pass


class TestPatientRecordIteration:
    """Tests for __iter__, __contains__ — Session 1.3."""
    # TODO: test_iter, test_contains_icd10, test_contains_loinc
    pass


class TestPatientRecordIdentity:
    """Tests for __eq__, __hash__ — Session 1.4."""
    # TODO: test_eq_same_mrn, test_hash_in_set, test_hash_as_dict_key
    pass


class TestFHIRBundle:
    """Tests for FHIRBundle collection protocol — Session 1.5."""
    # TODO: test_iter, test_len, test_getitem, test_add
    pass


class TestClinicalConcept:
    """Tests for ClinicalConcept identity and hashability — Session 1.4."""
    # TODO: test_eq, test_hash, test_set_deduplication
    pass
