# Python Skills Roadmap

> What you will learn by building clinicalnlp, mapped from Fluent Python (2nd ed.) to clinical informatics practice.

---

## The Big Picture

Fluent Python teaches the **Python-specific features** that most programmers never learn — the idioms, protocols, and patterns that separate "Python code written by someone who knows Java" from truly Pythonic code. This project takes those 24 chapters and grounds every concept in **clinical informatics** — the domain where you already have depth.

By the end, you won't just know Python. You'll think in Python.

---

## Skills by Module

### Module 1 — The Python Data Model (`core/`)
**Fluent Python Chapters 1-3 | Skill Level Target: Can teach it**

| Skill | What You'll Learn | Clinical Application | Naive Version | Fluent Version |
|-------|-------------------|---------------------|---------------|----------------|
| **Special methods (dunders)** | Python's "metaobject protocol" — the API that makes your objects work with built-in functions | `PatientRecord` works with `len()`, `for`, `in`, `sorted()`, `set()` | Writing `.get_count()`, `.get_item(i)` methods | Implementing `__len__`, `__getitem__` and getting iteration for free |
| **`__repr__` vs `__str__`** | Developer display vs user display; `repr` should be unambiguous | `<Patient MRN=12345 age=67>` in debugger, `"Jane Doe, DOB: 1957-03-12"` in UI | Only implementing `__str__` | Always implement `__repr__` first (it's the fallback for `__str__`) |
| **Hashability contract** | `__eq__` + `__hash__` must be consistent; mutable objects shouldn't be hashable | SNOMED codes deduplicated in `set()`, used as `dict` keys | Comparing codes with string matching | `__eq__` by vocabulary_id + concept_code, `__hash__` on the same fields |
| **Sequence protocol** | `__getitem__` alone gives you iteration, slicing, `in`, `reversed()` | `record[0]`, `record[1:3]`, `for obs in record` | Building explicit `.iterate()` methods | Delegating `__getitem__` to an internal list |
| **Collection ABCs** | `Iterable`, `Sized`, `Container` → `Collection` → `Sequence`, `Mapping`, `Set` | Understanding which interface your clinical objects implement | Not knowing which protocol to implement | Choosing the right ABC and getting free methods |

**Compound skill:** Understanding `__hash__` enables → using objects in `set()` → deduplicating SNOMED codes → building O(1) vocabulary lookups.

---

### Module 2 — Data Structures (`containers/`)
**Fluent Python Chapters 2-6 | Skill Level Target: Can choose the right one**

| Skill | What You'll Learn | Clinical Application | Why It Matters |
|-------|-------------------|---------------------|----------------|
| **dict internals** | Hash tables, O(1) lookup, key ordering (3.7+) | OMOP `concept_id → concept_name` with 50K entries in microseconds | The difference between real-time CDS and a slow batch job |
| **defaultdict & Counter** | Auto-initializing dicts, frequency counting | Patient → diagnoses grouping; medication mention counting | Eliminates 3 lines of boilerplate per lookup |
| **set operations** | Union, intersection, difference, frozenset | SNOMED code deduplication, code group comparisons | O(1) membership test vs O(n) list scan |
| **List comprehensions** | Declarative collection building | `[obs for obs in record if obs.code.startswith("LOINC")]` | Readable, fast, Pythonic |
| **Tuple unpacking** | Parallel assignment, `*` for excess, nested unpacking | Destructuring FHIR resource fields | Cleaner than indexing |
| **Pattern matching** | `match/case` (Python 3.10) | Matching FHIR resource types, ICD-10 code patterns | Structural pattern matching replaces chains of `if/elif` |
| **NamedTuple vs @dataclass** | Immutable records vs mutable entities | Lab results (immutable) vs clinical entities (mutable) | Right tool for the right record type |
| **array.array & deque** | Memory-efficient numerics, O(1) both-ends queue | Lab value time series; sliding window over note tokens | When `list` isn't the right choice |

**Compound skill:** Choosing `dict` over `list` for lookups → building `OmopVocabulary` → enabling real-time clinical decision support.

---

### Module 3 — Functions & Decorators (`pipeline/`)
**Fluent Python Chapters 7-10 | Skill Level Target: Can build production decorators**

| Skill | What You'll Learn | Clinical Application | Why It Matters |
|-------|-------------------|---------------------|----------------|
| **Functions as objects** | Functions have `__name__`, `__doc__`, can be stored in dicts | NLP transforms stored by name in a registry | Enables Strategy pattern, plugin architectures |
| **Closures** | Inner function captures outer scope variables | `make_phi_checker(phi_fields)` factory | Encapsulation without classes |
| **Decorators** | `@decorator` is just `f = decorator(f)` | `@audit_log` on every data access function | HIPAA compliance without modifying business logic |
| **`functools.wraps`** | Preserving decorated function metadata | `help(get_patient)` still works after decoration | Without it, debugging decorated functions is impossible |
| **Decorator with args** | `@retry(max_attempts=3)` — decorator factory pattern | Configurable retry for FHIR API calls | Production-grade decorator pattern |
| **`functools.lru_cache`** | Memoization of function calls | Cache UMLS/SNOMED API responses | Eliminates redundant API calls |
| **`functools.partial`** | Pre-configure function arguments | `clean_note = partial(preprocess, lowercase=True, strip_phi=True)` | Build specialized transforms from general ones |
| **Higher-order functions** | `map()`, `filter()`, `reduce()` on records | Functional pipeline: clean → extract → normalize | Composable data transformations |

**Compound skill:** Understanding closures → building decorators → stacking `@cache + @audit_log + @validate_phi` → production FastAPI endpoints that are audited, cached, and secured.

---

### Module 4 — OOP & Protocols (`models/`)
**Fluent Python Chapters 11-16 | Skill Level Target: Can design class hierarchies correctly**

| Skill | What You'll Learn | Clinical Application | Why It Matters |
|-------|-------------------|---------------------|----------------|
| **Protocol (structural typing)** | Duck typing formalized with `typing.Protocol` | `Extractable` — any object with `.extract(text)` qualifies | No forced inheritance; flexibility |
| **ABC (nominal typing)** | Contract enforcement at class definition time | `BaseExtractor` requires `.extract()` | Fail fast, not at runtime |
| **Composition over inheritance** | "Has-a" beats "is-a" for flexibility | `NERPipeline` HAS extractors, not IS an extractor | Avoids inheritance hell |
| **`__slots__`** | Memory-efficient attribute storage | `FHIRObservation` processing millions of records | 40-60% memory savings |
| **`@property`** | Computed/validated attributes | `Patient.dob` validation on assignment | Everyday descriptor pattern |
| **Descriptors** | How `@property` works under the hood | `ValidatedField` for reusable FHIR field validation | Understand the machinery |
| **Operator overloading** | `__add__`, `__iadd__`, `__eq__` | `bundle_a + bundle_b` merges FHIR bundles | Natural syntax for domain operations |
| **MRO & mixins** | Method Resolution Order, horizontal composition | `SerializableMixin`, `AuditableMixin` | Controlled multiple inheritance |

**Compound skill:** Protocol for interface → ABC for enforcement → composition for assembly → `NERPipeline(extractors=[Med(), Diag(), Proc()], normalizer=OmopNormalizer())`.

---

### Module 5 — Control Flow & Metaprogramming (`streaming/`)
**Fluent Python Chapters 17-24 | Skill Level Target: Can build streaming pipelines**

| Skill | What You'll Learn | Clinical Application | Why It Matters |
|-------|-------------------|---------------------|----------------|
| **Generator functions** | `yield` for lazy evaluation | `stream_notes(path)` — one note at a time from 10GB file | Peak RAM: ~1 note, not 2M notes |
| **Generator expressions** | `(x for x in iterable)` — memory-free transform | `(clean(n) for n in stream)` | Zero-copy pipeline stages |
| **`itertools`** | `chain()`, `islice()`, `groupby()` | Merge note streams, sample, group by patient | Lazy combinators in the stdlib |
| **`yield from`** | Sub-generator delegation | Transparent delegation to sub-pipelines | Clean multi-level generators |
| **Context managers** | `__enter__`/`__exit__`, `@contextmanager` | Clinical DB session lifecycle | Resource safety guarantee |
| **`async`/`await`** | Concurrent I/O without threads | 100 FHIR API calls in ~1 second vs 20 seconds sequential | Production-scale data fetching |
| **`asyncio.gather()`** | Batch concurrent operations | Parallel patient lookups from FHIR server | Real async parallelism |
| **`__init_subclass__`** | Auto-registration hook | Every NER extractor auto-registers in the registry | Light metaprogramming, no metaclasses |
| **Class decorators** | `@register_extractor` | Alternative to `__init_subclass__` | When to prefer each approach |

**Compound skill:** Generator pipeline → `stream → preprocess → extract → map_to_omop → write_to_db` → 2M notes processed with constant memory.

---

## Skill Progression Map

```
Module 1: DATA MODEL ──────────────────────> Foundation
    Objects speak Python's protocols
    Everything else builds on this

Module 2: DATA STRUCTURES ─────────────────> Containers
    Right container for the job
    O(1) vs O(n) is an architectural choice

Module 3: FUNCTIONS & DECORATORS ──────────> Behavior
    Functions are objects
    Decorators wrap behavior without modification

Module 4: OOP & PROTOCOLS ─────────────────> Architecture
    Protocol > ABC > Inheritance
    Composition over inheritance

Module 5: GENERATORS & ASYNC ──────────────> Scale
    Lazy evaluation for big data
    Concurrent I/O for real-time systems
```

---

## What This Unlocks in Your Career

| Skill Area | Before clinicalnlp | After clinicalnlp |
|-----------|--------------------|--------------------|
| **Python idioms** | Write Python "with a Java accent" | Think in protocols, generators, decorators |
| **Data pipeline design** | Load everything into RAM, process, save | Stream with generators, constant memory |
| **API development** | Copy-paste FastAPI examples | Understand the decorator machinery powering FastAPI |
| **Clinical NLP** | Black-box model calls | Build composable extraction pipelines with Protocol/ABC |
| **System design** | "It works" | "It works, it's Pythonic, it scales, and it's auditable" |
| **Code review** | Check if it runs | Evaluate Pythonic idiom, container choice, protocol compliance |

---

## How to Use This Roadmap

1. **Before each module:** Read this section to know what skills you're targeting
2. **During each session:** One concept at a time, following the Naive → Fluent pattern
3. **After each module:** Review the compound skill chain — can you trace how the skills connect?
4. **At project end:** Revisit this document and self-assess each skill level
