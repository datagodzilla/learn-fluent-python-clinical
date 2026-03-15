"""
Module 1, Session 1.1: __repr__ and __str__
============================================
The Two Faces of a Patient Record

Fluent Python Chapter 1, pages 36-37
Reference: example-code-2e/01-data-model/vector2d.py

Run this tutorial:
    uv run python Module-1-Data-Model/01_data_model.py
"""

# ============================================================================
#
#   "Here's the plan: when someone uses a feature you don't understand,
#    simply shoot them. This is easier than learning something new."
#                                    — Tim Peters (with a wink)
#
#   Tim was joking, obviously. But the quote opens Fluent Python for a
#   reason: most Python programmers use only a fraction of the language's
#   power. The Data Model — those double-underscore methods — is the
#   biggest fraction they miss.
#
#   This session is about just TWO of those methods. __repr__ and __str__.
#   By the end, you'll understand something that confused me for years:
#   why Python has TWO ways to turn an object into a string, and why
#   picking the right one matters in clinical systems where a wrong
#   print statement can leak Protected Health Information into a log file.
#
# ============================================================================


# ============================================================================
# 1. THE PROBLEM — Why Should a Clinical Informaticist Care About __repr__?
# ============================================================================
#
# Picture this. It's 2 AM. You're on call for the data pipeline team at a
# large academic medical center. An alert fires: the nightly OMOP ETL job
# failed on record validation. You SSH into the server, open a Python REPL,
# and load the offending patient record:
#
#     >>> patient = load_record("MRN-10001")
#     >>> patient
#     <clinicalnlp.core.clinical_record.PatientRecord object at 0x104a8f070>
#
# That's it. That's all Python gives you. An angle bracket, a fully qualified
# class name, and a memory address. You have no idea which patient this is,
# what's in the record, or why it failed.
#
# So you start writing ad-hoc print statements:
#
#     >>> print(patient.mrn, patient.name, patient.dob, len(patient.observations))
#     MRN-10001 Jane Doe 1957-03-12 4
#
# This works — once. But now you need to do this everywhere. In the debugger.
# In the log files. In the Slack message to your colleague. Every time you
# touch a patient record, you write a custom print statement.
#
# There's a better way. And it takes exactly 6 lines of code.
#
# ============================================================================


# ============================================================================
# 2. THE NAIVE WAY — Custom Methods That Python Ignores
# ============================================================================
#
# Here's what most programmers do when they come from Java, C#, or Go.
# They create custom methods with names like .display() or .to_string():

class PatientRecord_Naive:
    """The naive approach — custom display methods that Python doesn't know about."""

    def __init__(self, mrn, name, dob, observations=None):
        self.mrn = mrn
        self.name = name
        self.dob = dob
        self.observations = observations or []

    def display(self):
        """Custom method for human-readable output."""
        return f"{self.name}, DOB: {self.dob}"

    def debug_info(self):
        """Custom method for developer output."""
        return f"PatientRecord(mrn={self.mrn}, name={self.name})"


# Let's see what happens when we use this:

def demo_naive():
    """Demonstrate why custom display methods don't integrate with Python."""
    patient = PatientRecord_Naive("MRN-10001", "Jane Doe", "1957-03-12")

    print("=== THE NAIVE WAY ===")
    print()

    # What you WANT to see:
    #   PatientRecord(mrn='MRN-10001', name='Jane Doe', ...)
    # What you GET:
    print(f"  print(patient):        {patient}")
    #   <__main__.PatientRecord_Naive object at 0x...>

    # Your custom methods exist, but Python doesn't know about them:
    print(f"  patient.display():     {patient.display()}")
    print(f"  patient.debug_info():  {patient.debug_info()}")
    print()

    # Here's where it gets painful. Logging frameworks call repr(), not
    # your custom .debug_info() method:
    import logging
    logging.basicConfig(level=logging.INFO, format="  %(message)s")
    logging.info("Processing patient: %r", patient)
    # Output: Processing patient: <__main__.PatientRecord_Naive object at 0x...>

    # f-strings with the !r flag call repr(), not your method:
    print(f"  f-string !r: {patient!r}")
    # Output: <__main__.PatientRecord_Naive object at 0x...>

    # The list representation is even worse. Imagine a cohort of patients:
    cohort = [
        PatientRecord_Naive("MRN-10001", "Jane Doe", "1957-03-12"),
        PatientRecord_Naive("MRN-10002", "John Smith", "1970-08-25"),
    ]
    print(f"  Cohort list: {cohort}")
    # [<...object at 0x...>, <...object at 0x...>]
    # Completely useless. You can't tell which patients are in the list.
    print()

#
# WHY THIS FAILS:
#
# The fundamental problem is that Python has a PROTOCOL for string
# representation. When you call print(), Python calls __str__(). When a
# debugger or REPL displays an object, Python calls __repr__(). When
# logging frameworks format with %r, they call __repr__().
#
# Your custom .display() and .debug_info() methods are invisible to all
# of this. It's like building a door that doesn't fit any doorframe —
# the door works fine, but nobody can use it because it doesn't follow
# the standard dimensions.
#
# The "standard dimensions" in Python are the special methods. Ramalho
# calls them the "Data Model" — the API that makes your objects work
# with the language itself.
#
# ============================================================================


# ============================================================================
# 3. THE FLUENT WAY — Speaking Python's Protocol
# ============================================================================
#
# Here's the key insight from Fluent Python Chapter 1:
#
#   "You can think of the data model as a description of Python as a
#    framework. It formalizes the interfaces of the building blocks of
#    the language itself, such as sequences, functions, iterators,
#    coroutines, classes, context managers, and so on."
#
# In other words: Python is a framework, and __repr__/__str__ are the
# interface methods you implement to plug into it. Just like Django
# expects you to implement get_queryset(), Python expects you to
# implement __repr__().
#
# Let's do it the Pythonic way:

from clinicalnlp.core.clinical_record import PatientRecord


def demo_fluent():
    """Demonstrate how __repr__ and __str__ integrate with Python."""

    # --- Create a patient with some observations ---
    patient = PatientRecord(
        mrn="MRN-10001",
        name="Jane Doe",
        dob="1957-03-12",
        observations=[
            {"code": "ICD10:E11.9", "description": "Type 2 diabetes mellitus"},
            {"code": "ICD10:I10", "description": "Essential hypertension"},
            {"code": "LOINC:2339-0", "value": 126, "unit": "mg/dL", "description": "Glucose"},
            {"code": "LOINC:4548-4", "value": 7.2, "unit": "%", "description": "HbA1c"},
        ],
    )

    print("=== THE FLUENT WAY ===")
    print()

    # --- __repr__: The Developer's View ---
    #
    # When you type a variable name in the REPL, Python calls __repr__().
    # When a debugger shows your object, it calls __repr__().
    # When logging formats with %r, it calls __repr__().
    #
    # __repr__ should be UNAMBIGUOUS. Ramalho says: "if possible, match
    # the source code necessary to re-create the represented object."
    #
    # Notice the !r format spec in our implementation:
    #   f"PatientRecord(mrn={self.mrn!r}, ...)"
    #
    # The !r calls repr() on each attribute. For strings, this adds quotes:
    #   mrn='MRN-10001'  — you can see it's a string
    #   mrn=MRN-10001    — is this a variable? a number? unclear
    #
    # This tiny detail matters when you're reading log files at 2 AM.

    print(f"  repr(patient):")
    print(f"    {repr(patient)}")
    print()
    # PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=4)

    # --- __str__: The Human's View ---
    #
    # When you call print(), Python calls __str__().
    # When you use an f-string without !r, Python calls __str__().
    #
    # __str__ should be READABLE. It's what a nurse, physician, or
    # patient sees on screen. No implementation details, no memory
    # addresses, no Python syntax.

    print(f"  print(patient):")
    print(f"    {patient}")
    print()
    # Jane Doe, DOB: 1957-03-12

    # --- The !r Flag: Choosing Your Representation ---
    #
    # f-strings give you explicit control:
    #   {patient}    → calls __str__ → "Jane Doe, DOB: 1957-03-12"
    #   {patient!r}  → calls __repr__ → "PatientRecord(mrn='MRN-10001', ...)"
    #
    # This is incredibly useful in logging:

    print(f"  f-string default (str): {patient}")
    print(f"  f-string !r    (repr): {patient!r}")
    print()

    # --- Logging: __repr__ Is Your Best Friend ---
    #
    # Production logging should use repr(), because it's unambiguous.
    # If a log file says:
    #   Processing patient: Jane Doe, DOB: 1957-03-12
    #
    # ...you don't know the MRN, the observation count, or even which
    # class this object is. But if it says:
    #   Processing patient: PatientRecord(mrn='MRN-10001', ..., obs=4)
    #
    # ...you have everything you need to debug.

    import logging
    logging.basicConfig(level=logging.INFO, format="  %(message)s", force=True)
    logging.info("Processing patient: %r", patient)
    print()

    # --- Lists of Patients: __repr__ Shines ---
    #
    # When you have a list (or set, or dict) of objects, Python calls
    # __repr__ on each element to build the list's string representation.
    # This is where naive .display() methods completely fall apart.

    cohort = [
        patient,
        PatientRecord("MRN-10002", "John Smith", "1970-08-25", [
            {"code": "ICD10:I21.0", "description": "Acute STEMI"},
        ]),
        PatientRecord("MRN-10003", "Maria Garcia", "1952-11-30", [
            {"code": "ICD10:C34.11", "description": "NSCLC"},
            {"code": "ICD10:J44.1", "description": "COPD"},
            {"code": "ICD10:I48.91", "description": "Atrial fibrillation"},
        ]),
    ]

    print("  Patient cohort:")
    for p in cohort:
        print(f"    {p!r}")
    print()
    # PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=4)
    # PatientRecord(mrn='MRN-10002', name='John Smith', dob='1970-08-25', obs=1)
    # PatientRecord(mrn='MRN-10003', name='Maria Garcia', dob='1952-11-30', obs=3)

#
# WHAT JUST HAPPENED:
#
# By implementing TWO methods — __repr__ and __str__ — our PatientRecord
# now works with:
#   - print()          → calls __str__
#   - repr()           → calls __repr__
#   - f-strings        → calls __str__ (or __repr__ with !r)
#   - logging with %r  → calls __repr__
#   - debuggers        → calls __repr__
#   - list display     → calls __repr__ on each element
#   - interactive REPL → calls __repr__
#
# That's SEVEN integrations from TWO methods. This is the power of the
# Python Data Model — you implement the protocol once, and the entire
# ecosystem works with your object.
#
# Ramalho summarizes it perfectly (Chapter 1 summary, p.46):
#   "By implementing special methods, your objects can behave like the
#    built-in types, enabling the expressive coding style the community
#    considers Pythonic."
#
# ============================================================================


# ============================================================================
# 4. THE CLINICAL WIN — Why This Matters in Healthcare IT
# ============================================================================
#
# Let's talk about three real-world scenarios where __repr__ and __str__
# save you in clinical systems:
#
# SCENARIO 1: HIPAA-SAFE LOGGING
#
#   In healthcare, you can't just dump patient records into log files.
#   Protected Health Information (PHI) — names, DOBs, MRNs — must be
#   handled carefully. But you still need to debug.
#
#   With __repr__, you control exactly what appears in logs. You could
#   create a version that shows only the MRN and observation count:
#
#     PatientRecord(mrn='MRN-10001', obs=4)
#
#   ...without leaking the patient's name or date of birth. The str
#   representation (used in the UI) can show the full name, but the
#   repr (used in logs) keeps PHI out of your log files.
#
#
# SCENARIO 2: DEBUGGING ETL FAILURES
#
#   When your OMOP CDM ETL pipeline fails on record 47,832 out of
#   100,000, you need to know WHICH record failed. Without __repr__,
#   your error log says:
#
#     ERROR: Validation failed for <PatientRecord object at 0x104a8f070>
#
#   With __repr__, it says:
#
#     ERROR: Validation failed for PatientRecord(mrn='MRN-10001', obs=4)
#
#   Now you can find the record, examine it, and fix the pipeline.
#
#
# SCENARIO 3: CLINICAL DASHBOARDS
#
#   When a Streamlit dashboard displays a patient record, it calls
#   str() under the hood. With __str__, the user sees:
#
#     Jane Doe, DOB: 1957-03-12
#
#   Not implementation details. Not memory addresses. Just the human-
#   readable information they need.
#
# ============================================================================


# ============================================================================
# 5. RESEARCH POINTS
# ============================================================================
#
# If you want to go deeper, here are things worth exploring:
#
# 1. READ Fluent Python Chapter 1, pages 35-37 on __repr__ vs __str__.
#    Pay attention to the Vector2d example and how !r is used in the
#    f-string inside __repr__.
#
# 2. TRY this experiment: delete __str__ from PatientRecord and call
#    print(patient). What happens? Python falls back to __repr__. This
#    is why Ramalho says: "If you only implement one, implement __repr__."
#
# 3. READ the Python docs on object.__repr__() and object.__str__():
#    https://docs.python.org/3/reference/datamodel.html#object.__repr__
#    Notice the phrasing: __repr__ should look like "a valid Python
#    expression that could be used to recreate an object."
#
# 4. THINK about HIPAA implications: in a production system, would you
#    want __repr__ to include the patient name? What if log files are
#    shipped to a third-party monitoring service like Datadog or Splunk?
#    How would you design __repr__ for PHI-safe logging?
#
# 5. EXPLORE the !r, !s, and !a format specifiers in f-strings:
#    https://docs.python.org/3/library/string.html#format-string-syntax
#    When would you use !a (ASCII) in a clinical context? Think about
#    patient names with accented characters in international systems.
#
# ============================================================================


# ============================================================================
# 6. MINI EXERCISE
# ============================================================================
#
# Build a ClinicalObservation class that represents a single lab result,
# vital sign, or diagnosis. It should have:
#
#   - code: str       (e.g., "LOINC:2339-0" or "ICD10:E11.9")
#   - description: str (e.g., "Glucose" or "Type 2 diabetes mellitus")
#   - value: float | None  (e.g., 126.0 for a glucose result, None for a diagnosis)
#   - unit: str | None (e.g., "mg/dL", None for diagnoses)
#
# Implement:
#   __repr__ → ClinicalObservation(code='LOINC:2339-0', desc='Glucose', value=126.0, unit='mg/dL')
#   __str__  → Glucose: 126.0 mg/dL  (for lab results)
#              Type 2 diabetes mellitus (E11.9)  (for diagnoses)
#
# Hint: In __str__, check if value is None to decide between the two formats.
#
# WHY THIS MATTERS: This class will become the element type inside
# PatientRecord.observations in the next session. Building it now
# means you'll have a rich, self-describing observation object instead
# of a plain dict.
#
# ============================================================================


# ============================================================================
# RUNNING THIS TUTORIAL
# ============================================================================

if __name__ == "__main__":
    print()
    print("=" * 70)
    print("  Module 1, Session 1.1: __repr__ and __str__")
    print("  The Two Faces of a Patient Record")
    print("=" * 70)
    print()

    demo_naive()
    print("-" * 70)
    print()
    demo_fluent()

    print("=" * 70)
    print()
    print("  KEY TAKEAWAYS:")
    print()
    print("  1. Always implement __repr__ — it's the single most useful")
    print("     special method for debugging, logging, and developer UX.")
    print()
    print("  2. __repr__ should be UNAMBIGUOUS — use !r on string attributes")
    print("     to show quotes, ideally match the constructor signature.")
    print()
    print("  3. __str__ is OPTIONAL — implement it when you need a different")
    print("     human-readable format (print, UI, dashboards).")
    print()
    print("  4. Python falls back to __repr__ if __str__ is missing.")
    print("     The reverse is NOT true. __repr__ is the foundation.")
    print()
    print("  5. In clinical systems, __repr__ controls what appears in log")
    print("     files — design it for debuggability AND HIPAA compliance.")
    print()
    print("=" * 70)
    print()
    print("  NEXT SESSION: 1.2 — __len__ and __getitem__")
    print("  Making PatientRecord work with len() and record[0:3] slicing")
    print()
