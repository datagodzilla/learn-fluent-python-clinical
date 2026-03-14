"""
conftest.py — Shared test fixtures for clinicalnlp test suite.

Provides synthetic clinical data fixtures used across all test modules.
All data is SYNTHETIC — no real patient data.
"""

import json
import pytest
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture
def sample_patient():
    """A synthetic patient record for testing."""
    return {
        "mrn": "MRN-10001",
        "name": "Jane Doe",
        "dob": "1957-03-12",
        "observations": [
            {"code": "ICD10:E11.9", "description": "Type 2 diabetes mellitus"},
            {"code": "ICD10:I10", "description": "Essential hypertension"},
            {"code": "LOINC:2339-0", "value": 126, "unit": "mg/dL", "description": "Glucose"},
        ],
    }


@pytest.fixture
def snomed_concepts():
    """Load synthetic SNOMED concepts from data/."""
    path = DATA_DIR / "snomed_concepts.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@pytest.fixture
def loinc_codes():
    """Load synthetic LOINC codes from data/."""
    path = DATA_DIR / "loinc_codes.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@pytest.fixture
def rxnorm_drugs():
    """Load synthetic RxNorm drugs from data/."""
    path = DATA_DIR / "rxnorm_drugs.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@pytest.fixture
def omop_vocabulary():
    """Load synthetic OMOP vocabulary from data/."""
    path = DATA_DIR / "omop_vocabulary.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@pytest.fixture
def sample_notes():
    """Load synthetic clinical notes from data/."""
    path = DATA_DIR / "sample_notes.json"
    if path.exists():
        return json.loads(path.read_text())
    return []
