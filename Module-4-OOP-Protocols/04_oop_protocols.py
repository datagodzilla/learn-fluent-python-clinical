"""
Module 4: OOP & Protocols — Protocol, ABC, Composition, and Descriptors
========================================================================

Clinical systems integrate multiple subsystems: lab feeds, pharmacy
dispensing, radiology PACS, NLP pipelines.  Good OOP design makes
these composable and testable.

This module maps *Fluent Python* Ch. 11-13, 22-23 onto clinical
architecture:

  - typing.Protocol          -> structural subtyping for ClinicalResource
  - abc.ABC / abstractmethod -> enforce interface contracts on adapters
  - Composition over inherit -> PatientTimeline contains encounters,
                                 labs, meds — not "is-a" each one
  - Descriptors              -> validated clinical fields (e.g., heart
                                 rate must be 20-300 bpm)
  - __init_subclass__        -> auto-registration of NLP annotators
  - Mixins                   -> JSONSerializableMixin for FHIR export

Concepts from *Fluent Python* Ch. 11-13, 22-23:
  - Protocols vs ABCs: when to use which
  - __set_name__, __get__, __set__ descriptor protocol
  - __init_subclass__ for plugin registration
  - Composition patterns and delegation
"""


# ============================================================
# 1. THE PROBLEM — A clinical data platform must support
#    multiple EMR adapters (Epic, Cerner, Athena), each
#    exposing patient data differently.  NLP annotators
#    (negation detection, section tagging, ICD coding) must
#    be plug-and-play.  Vital-sign fields need range
#    validation that cannot be bypassed.
# ============================================================

pass


# ============================================================
# 2. THE NAIVE WAY — Deep inheritance hierarchies
#    (BaseAdapter -> FHIRAdapter -> EpicAdapter -> ...) that
#    are fragile and hard to test; validation scattered across
#    __init__ methods with repeated if/else blocks; NLP
#    annotators registered via a growing if/elif in a factory.
# ============================================================

pass


# ============================================================
# 3. THE FLUENT WAY — A ClinicalResource Protocol defines the
#    structural contract; ABC with abstractmethod enforces it
#    for adapters.  Composition assembles PatientTimeline from
#    separate Encounter, LabPanel, and MedicationOrder objects.
#    A ValidatedVital descriptor enforces range constraints.
#    __init_subclass__ auto-registers NLP annotators.
# ============================================================

pass


# ============================================================
# 4. THE CLINICAL WIN — New EMR adapters pass type-checking
#    without touching existing code; vital-sign descriptors
#    prevent physiologically impossible values from entering
#    the database; auto-registration lets researchers drop in
#    new NLP annotators without modifying a central registry.
# ============================================================

pass


# ============================================================
# 5. RESEARCH POINTS
#    - When should a clinical data interface be a Protocol
#      (structural) vs. an ABC (nominal)?
#    - How do descriptors compare to @property for validating
#      dozens of vital-sign fields?
#    - What are the trade-offs of __init_subclass__ vs.
#      metaclass-based registration for plugin systems?
#    - How does composition simplify unit testing of a
#      PatientTimeline compared to a monolithic
#      PatientRecord subclass?
# ============================================================

pass


# ============================================================
# 6. MINI EXERCISE
#    a) Define a Protocol `ClinicalDocument` with methods
#       get_text() -> str, get_metadata() -> dict, and
#       get_sections() -> list[str].
#    b) Write a ValidatedField descriptor that accepts a
#       (min, max) range and raises ValueError on __set__
#       if the value is out of range.  Use it for heart_rate
#       (20-300), systolic_bp (50-300), and temperature
#       (85.0-110.0 Fahrenheit).
#    c) Create a base Annotator class using __init_subclass__
#       that auto-registers every subclass in a class-level
#       registry dict.  Implement NegationAnnotator and
#       SectionAnnotator subclasses.
#    d) Build a PatientTimeline using composition: it holds
#       a list of encounters, a list of lab results, and a
#       list of medications, with methods to query across all.
# ============================================================

pass
