# Core Concepts & Best Practices

> Pythonic principles extracted from Fluent Python (2nd ed., Luciano Ramalho) — the mental models and coding practices to internalize through the clinicalnlp project.

---

## The Central Thesis

> "Python is an easy to learn, powerful programming language." That is true, but there is a catch: because the language is easy to learn and put to use, many practicing Python programmers leverage only a fraction of its powerful features.
> — Luciano Ramalho, Preface

The book's core message: **Python has a rich metaobject protocol (the Data Model) that most programmers never learn.** When you implement special methods, your objects integrate seamlessly with the entire Python ecosystem — `for`, `with`, `in`, `sorted()`, `set()`, `len()` all work automatically.

---

## The 5 Pillars of Pythonic Code

### Pillar 1: The Data Model Is a Framework

**Principle:** Think of the Python Data Model as a framework you're coding against. The Python interpreter calls your special methods — you don't call them directly.

```python
# The interpreter calls __getitem__, not you
my_collection[key]  # → my_collection.__getitem__(key)

# The interpreter calls __len__, not you
len(my_object)  # → my_object.__len__()

# for calls __iter__ (or falls back to __getitem__)
for item in my_object:  # → iter(my_object) → my_object.__iter__()
```

**Best Practice:** Implement special methods to integrate with the language, not to create custom APIs. Users of your class shouldn't need to memorize `.get_count()` vs `.size()` vs `.length()` — they just use `len()`.

**Clinical application:** A `PatientRecord` that implements `__len__`, `__getitem__`, and `__iter__` works with every Python tool that processes sequences — no custom API needed.

---

### Pillar 2: Use What Exists Before Building Your Own

**Principle:** Ramalho emphasizes using existing collection types and their interfaces before creating custom ones. Know what `dict`, `set`, `defaultdict`, `Counter`, `NamedTuple`, `deque` give you for free.

**Best Practice:**
- Use `dict` for O(1) lookups (not `list` with linear scan)
- Use `set` for membership testing and deduplication
- Use `defaultdict` to avoid `if key not in d` boilerplate
- Use `Counter` for frequency counting (`.most_common()` is free)
- Use `NamedTuple` for immutable records, `@dataclass` for mutable ones
- Only build custom collections (Ch 12-13) after mastering the built-ins

**Clinical application:** An OMOP vocabulary store built on `dict` gives microsecond lookups across 50K concepts. The same data in a `list` would take seconds to scan.

---

### Pillar 3: Functions Are Objects

**Principle:** In Python, functions are first-class objects. They have attributes (`__name__`, `__doc__`, `__annotations__`), can be stored in data structures, passed as arguments, and returned from other functions.

**Best Practice:**
- Store functions in dicts to build registries and dispatch tables
- Use closures to encapsulate state without classes
- Use `functools.partial` to specialize general functions
- Always use `functools.wraps` when writing decorators
- Understand that `@decorator` is syntactic sugar for `f = decorator(f)`

**Clinical application:** `@audit_log` wraps data access functions with HIPAA logging. `@lru_cache` memoizes UMLS API calls. Both work because decorators are just functions that take and return functions.

---

### Pillar 4: Protocols Over Inheritance

**Principle:** Python is built on duck typing — "If it walks like a duck and quacks like a duck, it's a duck." Fluent Python formalizes this with `typing.Protocol` (structural subtyping) and contrasts it with ABC (nominal subtyping).

**Best Practice:**
- Prefer `Protocol` for interfaces — no coupling to a base class
- Use `ABC` only when you need enforced contracts that must fail at definition time
- **Composition over inheritance:** "Has-a" is almost always better than "is-a"
- Avoid deep inheritance hierarchies — they're brittle
- Use mixins for cross-cutting concerns (serialization, auditing)

**Clinical application:**
```python
# BAD — inheritance hell
MedicationExtractor(BioBERTExtractor(TransformerExtractor(BaseExtractor)))

# GOOD — composition
NERPipeline(
    extractors=[MedExtractor(), DiagExtractor(), ProcExtractor()],
    normalizer=OmopNormalizer(),
    validator=FHIRValidator()
)
```

---

### Pillar 5: Lazy Evaluation for Scale

**Principle:** Generators and `yield` let you process data one item at a time, never loading the full dataset into memory. This is the key to processing files larger than RAM.

**Best Practice:**
- Use generator functions (`yield`) for data streaming
- Chain generator expressions for zero-copy pipeline stages
- Use `itertools` for lazy combinators (`chain`, `islice`, `groupby`)
- Reserve `async/await` for I/O-bound concurrency (not CPU-bound)
- Use context managers (`with`) for resource lifecycle management

**Clinical application:** A generator pipeline processes 2M MIMIC notes with peak RAM of ~1 note:
```
stream_notes(file)  →  preprocess(note)  →  extract(note)  →  map_to_omop(note)  →  write_to_db
  ↑ yield              ↑ gen expr          ↑ gen expr        ↑ gen expr            ↑ materialize
```

---

## Special Methods Reference

### Table 1-1: Non-Operator Special Methods

| Category | Methods | When to Implement |
|----------|---------|-------------------|
| **String/bytes representation** | `__repr__`, `__str__`, `__format__`, `__bytes__`, `__fspath__` | Always implement `__repr__`; add `__str__` when human display differs |
| **Conversion to number** | `__bool__`, `__complex__`, `__int__`, `__float__`, `__hash__`, `__index__` | `__bool__` for truthiness; `__hash__` whenever you implement `__eq__` |
| **Emulating collections** | `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__contains__` | When your object is a container; `__getitem__` alone gives iteration |
| **Iteration** | `__iter__`, `__aiter__`, `__next__`, `__anext__`, `__reversed__` | When your object should be iterable; prefer `__iter__` over `__getitem__` |
| **Callable/coroutine** | `__call__`, `__await__` | `__call__` makes instances callable (stateful decorators) |
| **Context management** | `__enter__`, `__exit__`, `__aexit__`, `__aenter__` | For resource lifecycle (DB connections, file handles) |
| **Instance creation** | `__new__`, `__init__`, `__del__` | `__init__` always; `__new__` rarely (singletons, immutable types) |
| **Attribute management** | `__getattr__`, `__getattribute__`, `__setattr__`, `__delattr__`, `__dir__` | Dynamic attributes (JSON-to-object mapping) |
| **Attribute descriptors** | `__get__`, `__set__`, `__delete__`, `__set_name__` | Reusable field validation (how `@property` works) |
| **Class metaprogramming** | `__prepare__`, `__init_subclass__`, `__class_getitem__`, `__mro_entries__` | `__init_subclass__` for auto-registration; avoid metaclasses when possible |

### Table 1-2: Operator Special Methods

| Category | Symbols | Methods |
|----------|---------|---------|
| **Unary numeric** | `-`, `+`, `abs()` | `__neg__`, `__pos__`, `__abs__` |
| **Rich comparison** | `<`, `<=`, `==`, `!=`, `>`, `>=` | `__lt__`, `__le__`, `__eq__`, `__ne__`, `__gt__`, `__ge__` |
| **Arithmetic** | `+`, `-`, `*`, `/`, `//`, `%`, `@`, `**` | `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__mod__`, `__matmul__`, `__pow__` |
| **Reversed arithmetic** | (swapped operands) | `__radd__`, `__rsub__`, `__rmul__`, etc. |
| **Augmented assignment** | `+=`, `-=`, `*=`, etc. | `__iadd__`, `__isub__`, `__imul__`, etc. |

---

## Anti-Patterns the Book Warns Against

### 1. Calling Special Methods Directly
```python
# WRONG
my_object.__len__()

# RIGHT
len(my_object)
```
**Why:** Built-in functions are faster for built-in types (they read `ob_size` from the C struct directly). And they provide a consistent API.

### 2. Implementing `__str__` Without `__repr__`
```python
# If you only implement one, implement __repr__
# The object class calls __repr__ as fallback for __str__
```

### 3. Using `__repr__` That Isn't Unambiguous
```python
# WRONG: Vector('1', '2') vs Vector(1, 2) — which is it?
def __repr__(self):
    return f'Vector({self.x}, {self.y})'

# RIGHT: Use !r to show repr of attributes
def __repr__(self):
    return f'Vector({self.x!r}, {self.y!r})'
```

### 4. Mutable Objects as Dict Keys
```python
# If you implement __eq__, Python makes __hash__ = None (unhashable)
# If you need hashability, the object must be immutable
# Rule: __eq__ + __hash__ must be consistent
```

### 5. Deep Inheritance Hierarchies
```python
# AVOID: MedicationExtractor(BioBERTExtractor(TransformerExtractor(BaseExtractor)))
# PREFER: Composition with pluggable components
```

### 6. Loading Everything into RAM
```python
# AVOID: data = json.load(open("10gb_file.json"))
# PREFER: Generator-based streaming with yield
```

### 7. Sequential I/O When Concurrent Would Work
```python
# AVOID: for mrn in mrns: patient = fetch(mrn)  # 100 x 200ms = 20s
# PREFER: asyncio.gather(*[fetch(mrn) for mrn in mrns])  # ~200ms total
```

---

## Key Quotes to Remember

> "By implementing special methods, your objects can behave like the built-in types, enabling the expressive coding style the community considers Pythonic."
> — Chapter 1 Summary

> "Container choice is an architectural decision."
> — Module 2 principle (from Chapter 3 on dict performance)

> "Premature abstraction is as bad as premature optimization."
> — Preface

> "Special cases aren't special enough to break the rules."
> — The Zen of Python (quoted in Chapter 1)

> "Practicality beats purity."
> — The Zen of Python (quoted re: why `len()` is a function, not a method)

> "We're all consenting adults here."
> — Python community principle on encapsulation

---

## Mental Models

### The Iceberg Model (Chapter 1)
What you see: `len(collection)` instead of `collection.len()`
What's underneath: The entire Python Data Model — 80+ special methods that make your objects play with the language.

### The Framework Model
Think of the Data Model as **a framework you code against**. Just like Django expects you to implement `.get_queryset()`, Python expects you to implement `__getitem__()`. The interpreter is the caller.

### The Protocol Model
Python has informal protocols: the iteration protocol (`__iter__`, `__next__`), the sequence protocol (`__getitem__`, `__len__`), the context manager protocol (`__enter__`, `__exit__`). Implement the right protocol, and the entire standard library works with your objects.

### The Container Hierarchy
```
            Iterable        Sized       Container
            __iter__        __len__     __contains__
                \            |            /
                 \           |           /
                  Collection (new in 3.6)
                 /     |     \
                /      |      \
           Sequence  Mapping   Set
```

### The Generator Pipeline Model
```
Source (disk) → yield → transform → yield → transform → yield → Sink (DB)
Peak RAM: O(1) items, regardless of dataset size
```

---

## Lessons to Remember at Project Completion

1. **The Data Model is Python's superpower.** Implementing 2-3 special methods gives you the entire standard library for free.

2. **Container choice determines performance.** `dict` vs `list` for lookups is not a preference — it's an O(1) vs O(n) architectural decision.

3. **Decorators are production patterns.** Every FastAPI route, every cached function, every audited endpoint uses the decorator machinery you learned in Module 3.

4. **Protocol > ABC > Inheritance.** Reach for `Protocol` first, `ABC` when enforcement matters, inheritance only as a last resort. Composition is almost always the right answer.

5. **Generators make big data possible.** If you can't fit it in RAM, yield it one item at a time. This is how real clinical NLP pipelines work at scale.

6. **`async` is for I/O, not compute.** Use `asyncio.gather()` for concurrent HTTP calls, not for CPU-bound NLP processing.

7. **Always implement `__repr__`.** It's the single most useful special method for debugging, logging, and developer experience.

8. **`functools.wraps` is mandatory in decorators.** Without it, your decorated functions lose their identity, and debugging becomes a nightmare.

9. **Composition over inheritance is not just advice — it's an architectural principle.** Build systems from pluggable components, not deep class trees.

10. **The Zen of Python is real engineering guidance.** "Practicality beats purity" and "Simple is better than complex" are design decisions, not platitudes.
