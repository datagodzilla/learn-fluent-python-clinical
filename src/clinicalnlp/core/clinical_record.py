"""
clinical_record.py — PatientRecord class demonstrating the Python Data Model.

Fluent Python Chapters 1-3 | Module 1 (core/)

Clinical Problem:
    Build a PatientRecord that prints meaningfully, compares by MRN,
    deduplicates in sets, iterates over observations, and works in `with` blocks.

Dunders implemented (incrementally across sessions):
    Session 1.1: __repr__, __str__
    Session 1.2: __len__, __getitem__  (pending)
    Session 1.3: __iter__, __contains__  (pending)
    Session 1.4: __eq__, __hash__  (pending)
    Session 1.5: __add__  (pending)

Reference: example-code-2e/01-data-model/ (FrenchDeck, Vector2d)
"""

# Standard library — date will be used in Session 1.4 for age calculation
from __future__ import annotations


class PatientRecord:
    """A clinical patient record that speaks Python's data model protocols.

    This class is built incrementally across Module 1 sessions. Each session
    adds new special methods, showing how the Python Data Model lets your
    objects integrate with the entire Python ecosystem.

    Attributes:
        mrn: Medical Record Number (unique patient identifier)
        name: Patient full name
        dob: Date of birth as ISO string (YYYY-MM-DD)
        observations: List of clinical observations (labs, vitals, diagnoses)
    """

    def __init__(
        self,
        mrn: str,
        name: str,
        dob: str,
        observations: list[dict] | None = None,
    ) -> None:
        # WHY: mrn is the primary identifier in every health system — it's how
        # we match patients across encounters, departments, and even hospitals.
        self.mrn = mrn
        # WHY: name is the human-readable identifier — used in __str__ for
        # display but NOT in __eq__/__hash__ (two records with the same MRN
        # are the same patient even if the name is spelled differently).
        self.name = name
        # WHY: dob stored as string for simplicity — in production you'd use
        # datetime.date, but for teaching the data model we keep it simple.
        self.dob = dob
        # WHY: observations is the core clinical payload — labs, vitals,
        # diagnoses. Defaulting to empty list avoids mutable default arg trap.
        self.observations = observations if observations is not None else []

    # --- Session 1.1: String Representation ---

    def __repr__(self) -> str:
        """Developer representation — unambiguous, shows how to recreate.

        WHY: Called by the interactive console, debuggers, logging with %r,
        and f-strings with !r. This is the MOST IMPORTANT special method to
        implement. If you only implement one, implement __repr__.

        Uses !r on string attributes to show quotes — this distinguishes
        PatientRecord(mrn='MRN-10001') from PatientRecord(mrn=MRN-10001).
        The quotes tell you it's a string, not a variable name.

        Ramalho (p.36): "__repr__ should be unambiguous and, if possible,
        match the source code necessary to re-create the represented object."
        """
        return (
            f"PatientRecord(mrn={self.mrn!r}, name={self.name!r}, "
            f"dob={self.dob!r}, obs={len(self.observations)})"
        )

    def __str__(self) -> str:
        """Human-readable representation — clean, suitable for end users.

        WHY: Called by print() and str(). This is what a nurse, physician,
        or patient sees on screen. It should be readable, not technical.

        If __str__ is not defined, Python falls back to __repr__. So
        __repr__ is the baseline — __str__ is the optional upgrade for
        when you need a different human-friendly format.
        """
        return f"{self.name}, DOB: {self.dob}"

    # --- Sessions 1.2-1.5: Remaining dunders will be added incrementally ---

    # TODO: Session 1.2 — __len__, __getitem__
    # TODO: Session 1.3 — __iter__, __contains__
    # TODO: Session 1.4 — __eq__, __hash__
    # TODO: Session 1.5 — __add__
