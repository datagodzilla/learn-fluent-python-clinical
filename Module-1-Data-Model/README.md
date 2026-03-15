# The Python Data Model in Clinical Informatics

> How two lines of Python changed the way I think about patient records

---

## The Moment It Clicked

I still remember the first time I truly understood the Python Data Model. I was
debugging a clinical data pipeline — one of those OMOP CDM ETL jobs that runs
overnight and processes a hundred thousand patient records. The job had failed on
record 47,832, and the error log said:

```
ERROR: Validation failed for <clinicalnlp.core.clinical_record.PatientRecord object at 0x104a8f070>
```

That's it. An angle bracket, a fully qualified class name, and a hexadecimal memory
address. I had no idea which patient this was. No MRN. No name. No observation count.
Nothing useful.

I spent twenty minutes writing ad-hoc print statements, grep-ing through the input
file, cross-referencing the record count with line numbers — all because my Python
object didn't know how to introduce itself.

Then a colleague walked over, looked at my screen, and said: "Why doesn't your class
have a `__repr__`?"

Six lines of code later, my error logs said:

```
ERROR: Validation failed for PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=4)
```

That was the moment I realized: Python isn't just a language you write code *in* — it's
a framework you write code *for*. And the framework's API is called the Data Model.

---

## What Is the Python Data Model?

Here's the Feynman version — no jargon, just the core idea.

Imagine you're building a hospital. Every room needs doors. You *could* design custom
doors for every room — one that slides, one that swings, one that requires a
fingerprint, one that opens with a voice command. Each door works, but nobody can
use any door without reading its specific manual.

Or you could agree on a standard: all doors have handles. Push to open. Pull to close.
Everyone knows how doors work because they all follow the same interface.

Python's Data Model is the "door handle standard" for objects. It says: if your
object implements `__len__()`, then `len(your_object)` works. If it implements
`__getitem__()`, then `your_object[0]` works. If it implements `__iter__()`, then
`for item in your_object` works.

You don't call these methods directly. The Python interpreter calls them for you,
behind the scenes, whenever you use built-in syntax. That's why they're called
"special" methods — they're the hooks that connect your objects to the language
itself.

Luciano Ramalho, who wrote the book that inspired this entire project, puts it
beautifully:

> "You can think of the data model as a description of Python as a framework.
>  It formalizes the interfaces of the building blocks of the language itself."

In other words: Python is a framework. `__repr__`, `__len__`, `__getitem__` — these
are your framework callbacks. Implement them, and the entire Python ecosystem works
with your objects.

---

## Session 1.1: The Two Faces of Every Object

### `__repr__` and `__str__` — Developer View vs. Human View

Every object in Python has two string representations. This confused me for years.
Why two? Why not just one?

Here's the analogy that finally made it click.

Think about a medication in a hospital. It has two names:

- **The pharmacist's name**: `Metformin Hydrochloride 500mg Extended-Release Tablet,
  NDC 0093-7214-01, RxNorm CUI 860975` — unambiguous, precise, every detail a
  professional needs to identify exactly which formulation this is.

- **The patient's name**: `Metformin 500mg` — clean, readable, only what the patient
  needs to know.

Same medication. Two audiences. Two representations.

Python works the same way:

- **`__repr__`** is the pharmacist's label — unambiguous, detailed, designed for
  developers. It should look like valid Python code that could recreate the object.
  This is what shows up in debuggers, log files, and the interactive REPL.

- **`__str__`** is the patient's label — clean, readable, designed for end users.
  This is what `print()` calls. It's what appears on dashboards and in UI elements.

### The Naive Approach (And Why It Fails)

When programmers come from Java or C#, they instinctively write custom methods:

```python
class PatientRecord:
    def __init__(self, mrn, name, dob):
        self.mrn = mrn
        self.name = name
        self.dob = dob
        self.observations = []

    def display(self):
        return f"{self.name}, DOB: {self.dob}"

    def debug_info(self):
        return f"PatientRecord(mrn={self.mrn}, name={self.name})"
```

This looks reasonable. But watch what happens when you actually use it:

```python
>>> patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12")
>>> print(patient)
<__main__.PatientRecord object at 0x104a8f070>
```

Your `.display()` method exists, but Python doesn't know about it. `print()` calls
`__str__()`, which you didn't implement, so Python falls back to the default — that
ugly angle-bracket memory address.

It gets worse. Put your patients in a list:

```python
>>> cohort = [patient_a, patient_b, patient_c]
>>> print(cohort)
[<...object at 0x104a>, <...object at 0x104b>, <...object at 0x104c>]
```

Three patients. Zero information. Your `.display()` method is completely invisible
here because Python calls `__repr__()` on each list element, not your custom method.

And in logging — the tool you'll rely on most in production:

```python
>>> import logging
>>> logging.info("Processing: %r", patient)
INFO: Processing: <__main__.PatientRecord object at 0x104a8f070>
```

The `%r` format calls `repr()`. Your `.debug_info()` method? Invisible.

**This is the fundamental lesson**: Python has a protocol for string representation.
If you don't implement the protocol, you're building doors without handles. The doors
work, but nobody can open them with the standard mechanism.

### The Fluent Approach

Here's what changes when you implement `__repr__` and `__str__`:

```python
class PatientRecord:
    def __init__(self, mrn, name, dob, observations=None):
        self.mrn = mrn
        self.name = name
        self.dob = dob
        self.observations = observations if observations is not None else []

    def __repr__(self):
        return (
            f"PatientRecord(mrn={self.mrn!r}, name={self.name!r}, "
            f"dob={self.dob!r}, obs={len(self.observations)})"
        )

    def __str__(self):
        return f"{self.name}, DOB: {self.dob}"
```

That's it. Six lines of actual code (two methods, three lines each). And now:

```python
>>> patient = PatientRecord("MRN-10001", "Jane Doe", "1957-03-12",
...     observations=[
...         {"code": "ICD10:E11.9", "description": "Type 2 diabetes mellitus"},
...         {"code": "ICD10:I10", "description": "Essential hypertension"},
...         {"code": "LOINC:2339-0", "value": 126, "unit": "mg/dL"},
...         {"code": "LOINC:4548-4", "value": 7.2, "unit": "%"},
...     ])
```

**The REPL and debugger** — calls `__repr__`:
```python
>>> patient
PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=4)
```

**print()** — calls `__str__`:
```python
>>> print(patient)
Jane Doe, DOB: 1957-03-12
```

**Logging** — calls `__repr__` via `%r`:
```python
>>> logging.info("Processing: %r", patient)
INFO: Processing: PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=4)
```

**f-strings** — you choose:
```python
>>> f"Patient: {patient}"       # __str__
'Patient: Jane Doe, DOB: 1957-03-12'

>>> f"Patient: {patient!r}"     # __repr__
"Patient: PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=4)"
```

**Lists** — calls `__repr__` on each element:
```python
>>> [patient_a, patient_b, patient_c]
[PatientRecord(mrn='MRN-10001', ..., obs=4),
 PatientRecord(mrn='MRN-10002', ..., obs=1),
 PatientRecord(mrn='MRN-10003', ..., obs=3)]
```

Seven integrations. Two methods. Zero custom API to remember.

---

## The `!r` Detail That Matters at 2 AM

There's a tiny detail in the `__repr__` implementation that's easy to miss but
matters enormously in practice. Look at this line:

```python
f"PatientRecord(mrn={self.mrn!r}, name={self.name!r}, ...)"
```

See the `!r` after `self.mrn`? That calls `repr()` on the attribute value before
inserting it into the f-string. For strings, `repr()` adds quotes:

```
With !r:    mrn='MRN-10001'    ← clearly a string
Without:    mrn=MRN-10001      ← string? variable? integer? unclear
```

When you're reading a log file at 2 AM trying to figure out why a record failed
validation, that visual distinction between "this is a string value" and "this is
something else" saves real time. Ramalho emphasizes this on page 36 of Fluent Python:

> "Note that the f-string in our `__repr__` uses `!r` to get the standard
>  representation of the attributes to be displayed. This is good practice,
>  because it shows the crucial difference between `Vector(1, 2)` and
>  `Vector('1', '2')`."

In our clinical context: `PatientRecord(mrn='MRN-10001')` tells you the MRN is a
string. `PatientRecord(mrn=MRN-10001)` leaves you guessing — and guessing at 2 AM
is how bugs survive.

---

## The Fallback Rule

Here's something that confused me early on: if you implement `__repr__` but NOT
`__str__`, then `print()` uses `__repr__` as a fallback. But the reverse is NOT true
— if you implement `__str__` but not `__repr__`, the REPL and debugger still show
`<object at 0x...>`.

This is why Ramalho says: **"If you only implement one of these special methods,
choose `__repr__`."**

Think of it this way:
- `__repr__` is the foundation. Everything can fall back to it.
- `__str__` is the optional upgrade. It adds a human-friendly layer on top.

In practice, I implement both for clinical objects because the audiences are different:
- A developer debugging a pipeline needs `PatientRecord(mrn='MRN-10001', obs=4)`
- A clinician using a Streamlit dashboard needs `Jane Doe, DOB: 1957-03-12`

---

## Why This Matters in Healthcare IT

Let me give you three scenarios where this isn't academic — it's operational.

### Scenario 1: HIPAA-Safe Logging

In healthcare, every log file is a potential HIPAA liability. If your logs contain
patient names and dates of birth, and those logs are shipped to Datadog or Splunk
or a third-party monitoring service, you've just created a PHI breach.

With `__repr__`, you control exactly what appears. You could design a production
version that shows only non-PHI identifiers:

```python
def __repr__(self):
    return f"PatientRecord(mrn={self.mrn!r}, obs={len(self.observations)})"
```

The MRN is still identifiable (it's a pseudonym, not direct PHI), but the patient's
name and date of birth never touch the log file. The `__str__` version — used in the
clinical UI — can show everything the clinician needs.

Two audiences. Two representations. Same object.

### Scenario 2: ETL Pipeline Debugging

When your nightly OMOP ETL fails on record 47,832, the error log needs to tell you
*which* record failed. Without `__repr__`:

```
ERROR: Validation failed for <PatientRecord object at 0x104a8f070>
```

With `__repr__`:

```
ERROR: Validation failed for PatientRecord(mrn='MRN-10001', obs=4)
```

The second version lets you grep the input file, find the record, examine the
observations, and fix the pipeline — all without adding a single ad-hoc print
statement.

### Scenario 3: Cohort Inspection

When a researcher builds a patient cohort for a clinical study, they need to verify
the cohort composition. With `__repr__` on each patient:

```python
print(f"Cohort ({len(cohort)} patients):")
for p in cohort:
    print(f"  {p!r}")
```

Output:
```
Cohort (3 patients):
  PatientRecord(mrn='MRN-10001', name='Jane Doe', dob='1957-03-12', obs=4)
  PatientRecord(mrn='MRN-10002', name='John Smith', dob='1970-08-25', obs=1)
  PatientRecord(mrn='MRN-10003', name='Maria Garcia', dob='1952-11-30', obs=3)
```

Every patient identified. Every observation count visible. No custom display
method to remember.

---

## The Mutable Default Argument Trap

There's one more detail in our `__init__` that deserves attention, because it's one
of the most common Python bugs — and it's especially dangerous in clinical systems
where data integrity matters:

```python
# DANGEROUS — DO NOT DO THIS
def __init__(self, mrn, name, dob, observations=[]):
    self.observations = observations
```

The problem? That empty list `[]` is created ONCE, when the class is defined, and
shared across ALL instances. If you add an observation to patient A, it magically
appears in patient B:

```python
>>> patient_a = PatientRecord("MRN-001", "Alice", "1990-01-01")
>>> patient_b = PatientRecord("MRN-002", "Bob", "1985-05-15")
>>> patient_a.observations.append({"code": "ICD10:E11.9"})
>>> print(patient_b.observations)
[{"code": "ICD10:E11.9"}]  # Bob has Alice's diabetes!
```

In a clinical system, this isn't just a bug — it's a patient safety issue. The fix
is simple:

```python
# SAFE — the Pythonic way
def __init__(self, mrn, name, dob, observations=None):
    self.observations = observations if observations is not None else []
```

Now each patient gets their own list. This pattern — `None` default with interior
creation — is so fundamental that you'll see it in every well-written Python codebase.

---

## What We Built

### Production Code

**File:** `src/clinicalnlp/core/clinical_record.py`

The `PatientRecord` class with:
- `__init__()` — MRN, name, DOB, observations (with mutable default protection)
- `__repr__()` — unambiguous developer representation with `!r` format specifiers
- `__str__()` — clean human-readable display for clinicians and patients

### Tests

**File:** `tests/test_core.py`

12 tests covering:
- `__repr__` contains class name, MRN with quotes, observation count
- `__str__` shows name and DOB, no implementation details
- `__init__` default observations, no mutable default sharing

### Tutorial

**File:** `Module-1-Data-Model/01_data_model.py`

Runnable script showing naive vs fluent comparison with live output:
```bash
uv run python Module-1-Data-Model/01_data_model.py
```

---

## What's Next

In Session 1.2, we implement `__len__` and `__getitem__` — the sequence protocol.
This is where things get exciting, because implementing just ONE method
(`__getitem__`) gives you iteration, slicing, `in` operator, and `reversed()` — all
for free.

Ramalho calls this "the most common use of special methods" and demonstrates it with
his famous `FrenchDeck` example: a class with just `__len__` and `__getitem__` that
suddenly works with `random.choice()`, `sorted()`, and `for` loops — without
implementing any of those protocols explicitly.

We'll do the same thing, but with patient observations instead of playing cards.

---

## Key Takeaways

1. **The Python Data Model is a framework API.** Implement its special methods and
   the entire ecosystem works with your objects.

2. **Always implement `__repr__`.** It's the fallback for `__str__`, the default in
   debuggers, the format in `%r` logging, and the representation in list displays.
   If you implement nothing else, implement this.

3. **`__repr__` is for developers; `__str__` is for humans.** In clinical systems,
   this distinction maps directly to developer debugging vs. patient-facing display.

4. **Use `!r` in `__repr__` f-strings.** It adds quotes around strings, which
   eliminates ambiguity at 2 AM when you're reading log files.

5. **Never use mutable default arguments.** Use `None` and create inside `__init__`.
   In clinical systems, shared state between patient records isn't just a bug — it's
   a patient safety risk.

6. **Two methods. Seven integrations.** `__repr__` and `__str__` make your objects
   work with print, repr, f-strings, logging, debuggers, lists, and the REPL. This
   is the power of protocols over custom APIs.

---

*Next: [Session 1.2 — `__len__` and `__getitem__`: The Sequence Protocol](02_len_getitem.md)*
