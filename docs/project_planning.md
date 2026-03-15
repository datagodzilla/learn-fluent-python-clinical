# Project Planning

> From learning sandbox to production clinical NLP package.

---

## Project Evolution

### What We Started With

A **learning sandbox**: teach yourself Fluent Python through clinical examples. The deliverable was knowledge — the code was a byproduct.

### What We're Building

A **functional Python package**: `clinicalnlp` as a real tool that takes clinical data in, processes it, and produces useful artifacts out. The learning happens through building something real.

### These Two Goals Are Not In Conflict

In fact, the best way to learn Pythonic patterns is to build something you'll actually use.

---

## Input: Clinical Data Sources

| Source | Format | Example |
|--------|--------|---------|
| Clinical notes | Free text / JSON | MIMIC discharge summaries, Synthea notes |
| Terminology files | JSON / CSV | SNOMED, LOINC, RxNorm, ICD-10 code sets |
| FHIR resources | JSON / API | Patient, Observation, Condition bundles |
| OMOP tables | CSV / Parquet / DB | condition_occurrence, drug_exposure, note |

## Output: Meaningful Artifacts

| Artifact | What It Does | Who Uses It |
|----------|-------------|-------------|
| **Extracted entities** | Medications, diagnoses, procedures from free text | NLP researchers, data scientists |
| **Normalized codes** | Map raw text mentions to SNOMED/LOINC/RxNorm codes | ETL pipelines, OMOP CDM builders |
| **Patient cohorts** | Filter/group patients by diagnosis, medication, lab values | Clinical researchers |
| **Vocabulary lookups** | O(1) concept search across OMOP/SNOMED/LOINC | Any clinical app needing terminology |
| **FHIR bundles** | Construct/validate/merge FHIR resources | Interoperability engineers |
| **Audit trails** | HIPAA-compliant access logs | Compliance, security teams |
| **Frequency reports** | Token/code/medication frequency from note corpora | Epidemiologists, QI teams |
| **Streaming pipelines** | Process millions of notes with constant memory | Production NLP systems |

## How Fluent Python Skills Map to Real Functions

| Fluent Python Skill | Production Function | Module |
|--------------------|--------------------|--------|
| `__getitem__`, `__iter__`, `__contains__` | `PatientRecord` that works with `for`, `in`, slicing | core |
| `dict`, `set`, `Counter`, `defaultdict` | `OmopVocabulary.lookup()`, `NoteRegistry.frequency()` | containers |
| Decorators, closures, `lru_cache` | `@audit_log`, `@cache_lookup`, `@validate_phi` | pipeline |
| Protocol, ABC, composition | `NERPipeline` with pluggable extractors | models |
| Generators, `async/await` | `stream_notes()`, `async_fhir_fetch()` | streaming |

**Every Fluent Python concept maps 1:1 to a real clinical function.** You learn the idiom by building the tool.

---

## The Pivot: What Changes

| Aspect | Learning-Only | Production Package |
|--------|--------------|-------------------|
| **Code quality** | Annotated stubs with TODOs | Working, tested, documented functions |
| **Data** | Synthetic-only | Synthetic + real FHIR endpoints + OMOP-compatible |
| **Tests** | Teaching examples | Real unit + integration tests with coverage |
| **Docs** | Tutorial narratives | Tutorial narratives + API reference + usage recipes |
| **Audience** | Just you | You + GitHub community + blog readers |
| **pyproject.toml** | Educational package | Publishable to PyPI |
| **CLI/API** | None | Optional: `clinicalnlp process notes.json --extract medications` |

## What Stays the Same

- The `src/` layout (already set up correctly)
- The 5-module architecture (already maps to real functions)
- The Naive vs Fluent teaching approach in tutorials
- The Module-1 through Module-6 folder structure
- The synthetic data files (good for tests and demos)
- The blog post plan

---

## Dual-Purpose Architecture

```
learn-fluent-python-clinical/
├── src/clinicalnlp/           # THE PACKAGE — real, installable, functional
│   ├── core/                  #   Production clinical data model classes
│   ├── containers/            #   Production vocabulary & data stores
│   ├── pipeline/              #   Production decorators & transforms
│   ├── models/                #   Production NER pipeline & protocols
│   └── streaming/             #   Production generators & async clients
│
├── Module-1-Data-Model/       # THE TUTORIALS — how & why each function was built
├── Module-2-Data-Structures/  #   Narrative walkthroughs (Naive → Fluent)
├── Module-3-Functions-Decorators/
├── Module-4-OOP-Protocols/
├── Module-5-Generators-Async/
├── Module-6-Capstone/
│
├── tests/                     # Real unit + integration tests
├── data/                      # Synthetic clinical data
└── docs/                      # API reference + tutorials + guides
```

The package teaches clinical informatics Python the same way `rich`, `httpx`, and `fastapi` teach Python — by being well-written, well-documented Python.

The blog post becomes: *"I built a Python package for clinical NLP — here's what Fluent Python taught me along the way."*

---

## Execution Plan

### Phase 1: Training (Module Tutorials)

Each module follows the pattern: **learn the concept in the tutorial, then implement it in `src/`.**

The tutorial (`Module-*/`) is the classroom. The package (`src/clinicalnlp/`) is the production codebase. Each session produces both.

#### Module 1 — Python Data Model (`Module-1-Data-Model/`)

| Session | Concept | Tutorial Deliverable | Production Deliverable (`src/clinicalnlp/core/`) |
|---------|---------|---------------------|------------------------------------------------|
| 1.1 | `__repr__` and `__str__` | Naive vs Fluent comparison with clinical output | `PatientRecord.__repr__()`, `__str__()` |
| 1.2 | `__len__` and `__getitem__` | Sequence protocol walkthrough | `PatientRecord.__len__()`, `__getitem__()` with slicing |
| 1.3 | `__iter__` and `__contains__` | Iteration protocol, `in` operator | `PatientRecord.__iter__()`, `__contains__()` |
| 1.4 | `__eq__` and `__hash__` | Hashability contract, set deduplication | `ClinicalConcept.__eq__()`, `__hash__()` |
| 1.5 | `__add__` and collection API | Bundle merging, `Collection` ABC | `FHIRBundle.__add__()`, `__iter__()`, `__len__()` |
| 1.6 | Integration | Combine all dunders, run full test suite | `test_core.py` with real assertions |

#### Module 2 — Data Structures (`Module-2-Data-Structures/`)

| Session | Concept | Tutorial Deliverable | Production Deliverable (`src/clinicalnlp/containers/`) |
|---------|---------|---------------------|------------------------------------------------------|
| 2.1 | `dict` internals | O(1) vs O(n) benchmark with clinical data | `OmopVocabulary.__init__()`, `lookup_by_id()` |
| 2.2 | `defaultdict` and `Counter` | Token frequency pipeline | `NoteRegistry` with `add_note()`, `most_common_tokens()` |
| 2.3 | `set` and `frozenset` | SNOMED code deduplication, set algebra | `OmopVocabulary.get_all_codes()`, set operations |
| 2.4 | `NamedTuple` vs `@dataclass` | Immutable vs mutable records | `LabResult` (NamedTuple), `ClinicalEntity` (dataclass) |
| 2.5 | Pattern matching | `match/case` on FHIR resource types | Resource type dispatching in vocabulary |
| 2.6 | Integration | Full container test suite | `test_containers.py` with real assertions |

#### Module 3 — Functions & Decorators (`Module-3-Functions-Decorators/`)

| Session | Concept | Tutorial Deliverable | Production Deliverable (`src/clinicalnlp/pipeline/`) |
|---------|---------|---------------------|-----------------------------------------------------|
| 3.1 | Functions as objects | Transform registry (dict of functions) | `transforms.py` registry pattern |
| 3.2 | Closures | `make_phi_checker()` factory | `transforms.py` closure factories |
| 3.3 | Basic decorators | `@audit_log` from scratch | `decorators.py` `@audit_log` |
| 3.4 | `functools.wraps` and decorator args | `@retry(max_attempts=3)` | `decorators.py` `@validate_phi`, `@cache_lookup` |
| 3.5 | `functools.lru_cache` and `partial` | Memoized UMLS lookups, pre-configured transforms | `decorators.py` caching, `transforms.py` partial |
| 3.6 | Decorator stacking + FastAPI | `@cache + @audit_log + @validate_phi` | `fastapi_layer.py` production endpoints |
| 3.7 | Integration | Full pipeline test suite | `test_pipeline.py` with real assertions |

#### Module 4 — OOP & Protocols (`Module-4-OOP-Protocols/`)

| Session | Concept | Tutorial Deliverable | Production Deliverable (`src/clinicalnlp/models/`) |
|---------|---------|---------------------|---------------------------------------------------|
| 4.1 | `Protocol` (structural typing) | `Extractable` interface | `protocols.py` with `Extractable`, `Normalizable` |
| 4.2 | `ABC` (nominal typing) | `BaseExtractor` with enforcement | `base_extractor.py` with concrete extractors |
| 4.3 | Composition over inheritance | NERPipeline design | `ner_pipeline.py` with pluggable extractors |
| 4.4 | `__slots__` and `@property` | Memory-efficient FHIR resources | `fhir_resource.py` with `__slots__`, validated fields |
| 4.5 | Descriptors | `ValidatedField` for reusable validation | `fhir_resource.py` custom descriptors |
| 4.6 | Operator overloading and mixins | `bundle + bundle`, `SerializableMixin` | `ner_pipeline.py` `__add__`, mixins |
| 4.7 | Integration | Full models test suite | `test_models.py` with real assertions |

#### Module 5 — Generators & Async (`Module-5-Generators-Async/`)

| Session | Concept | Tutorial Deliverable | Production Deliverable (`src/clinicalnlp/streaming/`) |
|---------|---------|---------------------|------------------------------------------------------|
| 5.1 | Generator functions | `stream_notes()` with `yield` | `generators.py` `stream_notes()` |
| 5.2 | Generator pipelines | Chain: stream → preprocess → extract → map | `generators.py` full pipeline |
| 5.3 | `itertools` | `chain()`, `islice()`, `groupby()` on notes | `generators.py` lazy combinators |
| 5.4 | Context managers | `ClinicalDBSession` with cleanup | `context_managers.py` |
| 5.5 | `async/await` | Async FHIR patient lookup | `async_fhir.py` `fetch_patient()` |
| 5.6 | `asyncio.gather()` | Batch concurrent FHIR calls | `async_fhir.py` `batch_fetch()` |
| 5.7 | `__init_subclass__` | Auto-registry for extractors | `metaclasses.py` |
| 5.8 | Integration | Full streaming test suite | `test_streaming.py` with real assertions |

#### Module 6 — Capstone (`Module-6-Capstone/`)

| Session | Deliverable |
|---------|-------------|
| 6.1 | Streamlit app skeleton, module selector sidebar |
| 6.2 | Module 1 demo: interactive PatientRecord exploration |
| 6.3 | Module 2 demo: dict vs list lookup benchmark visualization |
| 6.4 | Module 3 demo: decorator stacking visualization |
| 6.5 | Module 4 demo: NERPipeline builder UI |
| 6.6 | Module 5 demo: streaming progress + async FHIR timing |
| 6.7 | Polish, deploy, screenshot for blog |

---

### Phase 2: Production Hardening (`src/clinicalnlp/`)

After all modules are implemented through tutorials, harden the package for real-world use.

| Step | Task | Details |
|------|------|---------|
| 2.1 | **Test coverage >90%** | Fill in all test stubs, add edge cases, parametrize |
| 2.2 | **Type hints** | Add full type annotations to all public APIs |
| 2.3 | **Docstrings** | Google-style docstrings on every public class/function |
| 2.4 | **Error handling** | Validate inputs, meaningful error messages |
| 2.5 | **CLI interface** | `clinicalnlp process notes.json --extract medications` |
| 2.6 | **API reference** | Auto-generate from docstrings (pdoc or mkdocs) |
| 2.7 | **CI/CD** | GitHub Actions: test, lint, type check on every push |
| 2.8 | **PyPI publish** | `uv build && uv publish` — make it pip-installable |
| 2.9 | **Real data adapters** | Connectors for MIMIC, Synthea exports, HAPI FHIR |
| 2.10 | **Performance benchmarks** | dict vs list, generator vs list, async vs sync timing |

---

### Phase 3: Publication

| Step | Task | Details |
|------|------|---------|
| 3.1 | **Blog post draft** | Outline, narrative, code samples, architecture diagrams |
| 3.2 | **Blog diagrams** | Module flow, generator pipeline, architecture overview |
| 3.3 | **GitHub polish** | Badges, screenshots, contributing guide, issue templates |
| 3.4 | **Publish on datagodzilla** | Push final code, tag v0.1.0 release |
| 3.5 | **Sync to clinicalaiinsider** | Fork sync, publish blog on clinicalAIInsider.com |
| 3.6 | **Social sharing** | LinkedIn post, relevant communities |

---

## Session Workflow

Every session follows this flow:

```
1. READ the Fluent Python chapter section (PDF pages)
2. STUDY the example-code-2e/ reference implementation
3. WRITE the tutorial (Module-*/): Naive → Fluent with clinical context
4. IMPLEMENT the production code (src/clinicalnlp/): real, working functions
5. TEST: add assertions to the corresponding test file
6. DOCUMENT: update the module doc (docs/NN_*.md) and API reference
7. COMMIT: one concept per commit, push to GitHub
```

---

## Existing .claude/ Automation Pipeline

The project has a rich set of existing automation commands, agents, workflows, and templates in `.claude/` that integrate directly into Phase 3 (Publication). These are reusable tools already configured for the `datagodzilla` GitHub Pages site.

### Available Commands for Blog & Publishing

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/notebooklm-generate-blog-post` | Generate narrative blog post with Feynman Technique, Karpathy style, healthcare architect voice | Phase 3.1 — Write the blog post |
| `/notebooklm-publish-github` | Publish to GitHub Pages with Jekyll formatting, deployment verification | Phase 3.4 — Push to datagodzilla.github.io |
| `/notebooklm-queue-for-publish` | Queue posts for batch publishing | Phase 3.4 — If publishing multiple posts |
| `/notebooklm-generate-mindmap` | Generate concept mind maps (ASCII + Mermaid + SVG) | Phase 3.2 — Create architecture diagram |
| `/notebooklm-generate-slides` | Generate Marp presentation deck | Optional — conference/meetup presentation |
| `/notebooklm-generate-podcast` | Generate audio companion (two-host format) | Optional — audio version of blog |
| `/notebooklm-generate-flashcards` | Generate study flashcards from content | Optional — learning companion |
| `/notebooklm-generate-quiz` | Generate self-assessment quiz | Optional — interactive learning |
| `/notebooklm-generate-infographics` | Generate visual infographics | Phase 3.2 — Module overview graphics |
| `/notebooklm-generate-hero-image` | Generate blog post hero image | Phase 3.3 — GitHub/blog visual |

### Available Agents

| Agent | Role | When to Use |
|-------|------|-------------|
| `@notebooklm-blog-publisher` | Blog optimization, SEO, formatting | Phase 3.1 — Polish the post |
| `@notebooklm-clinical-expert` | Clinical accuracy review | Phase 3.1 — Verify clinical content |
| `@notebooklm-ai-expert` | Technical accuracy review | Phase 3.1 — Verify Python/code content |
| `@notebooklm-python-developer` | Python code review | Phase 2.1 — Code quality review |
| `@notebooklm-visual-designer` | Visual storytelling, diagrams | Phase 3.2 — Create visuals |
| `@notebooklm-github-publisher` | Git ops, Jekyll formatting, deployment | Phase 3.4 — Publish to GitHub Pages |
| `@notebooklm-doc-formatter` | Professional document formatting | Phase 3.3 — Final README polish |

### Available Workflows

| Workflow | Purpose | File |
|----------|---------|------|
| Blog Publishing | End-to-end blog post generation and publishing | `.claude/workflows/blog-publishing-workflow.md` |
| GitHub Publishing Ops | Git operations, Jekyll, deployment verification | `.claude/workflows/github-publishing-ops-workflow.md` |
| Visual Storytelling | Transform content into visual narratives | `.claude/workflows/visual-storytelling-workflow.md` |
| Mindmap | Generate concept maps in multiple formats | `.claude/workflows/mindmap-workflow.md` |

### Available Templates

| Template | Purpose | File |
|----------|---------|------|
| Blog Post | Full blog post structure with SEO, frontmatter, learning resources | `.claude/templates/blog-post-template.md` |
| GitHub Pages Post | Jekyll-compatible post with frontmatter | `.claude/templates/github-pages-post-template.md` |
| Mind Map | Concept visualization template | `.claude/templates/mindmap-template.md` |
| Slide Deck | Marp presentation template | `.claude/templates/slide-deck-template.md` |

### Blog Post Style Guide (from existing commands)

All blog posts follow these standards:
- **Writing Style**: Karpathy Narrative + Feynman Technique
- **Voice**: Seasoned healthcare data systems architect
- **Target Audience**: Junior clinical informatics students
- **Output**: 3 visualization versions (Mermaid, ASCII, Graphviz SVG)
- **SEO**: Optimized slugs, meta descriptions, keyword targeting
- **Enrichment**: Audio podcast, flashcards, quiz, mind map companions
- **Publishing Target**: `datagodzilla.github.io` via GitHub Pages (Jekyll)

### Phase 3 Execution Using .claude/ Pipeline

```
Phase 3 Publication Pipeline:

Step 1: Generate blog post
  /notebooklm-generate-blog-post docs/project_planning.md
  → Produces 3 versions: Mermaid, ASCII, Graphviz
  → Uses @notebooklm-clinical-expert + @notebooklm-ai-expert
  → Applies Karpathy narrative style + Feynman technique

Step 2: Generate companion artifacts
  /notebooklm-generate-mindmap [blog-post-path]
  /notebooklm-generate-infographics [blog-post-path]
  → Architecture diagram, module flow, generator pipeline visual

Step 3: Queue for publish
  /notebooklm-queue-for-publish [blog-post-path]
  → Validates frontmatter, content, images

Step 4: Publish to GitHub Pages
  /notebooklm-publish-github --queue
  → Copies to _posts/, handles assets, pushes, verifies deployment
  → Live at: https://datagodzilla.github.io/YYYY/MM/DD/slug/

Step 5: Cross-publish to clinicalaiinsider
  → Sync fork, or publish separately to clinicalaiinsider GitHub Pages
```

### Blog Post Series Plan

The clinicalnlp project can generate a multi-part blog series:

| Post # | Title | Source Content | When |
|--------|-------|---------------|------|
| 1 | "Building a Clinical NLP Package: Why Fluent Python Matters" | `docs/project_planning.md` + `docs/core_concepts_and_best_practices.md` | After Module 1 complete |
| 2 | "The Python Data Model in Clinical Informatics" | Module 1 tutorial + `src/clinicalnlp/core/` | After Module 1 complete |
| 3 | "Data Structures That Power Clinical Decision Support" | Module 2 tutorial + `src/clinicalnlp/containers/` | After Module 2 complete |
| 4 | "Decorators for HIPAA-Compliant AI Endpoints" | Module 3 tutorial + `src/clinicalnlp/pipeline/` | After Module 3 complete |
| 5 | "OOP Patterns for Clinical NLP Pipelines" | Module 4 tutorial + `src/clinicalnlp/models/` | After Module 4 complete |
| 6 | "Streaming 2M Clinical Notes with Python Generators" | Module 5 tutorial + `src/clinicalnlp/streaming/` | After Module 5 complete |
| 7 | "From Learning Project to PyPI Package: The Full Journey" | Capstone + full project retrospective | After Phase 2 complete |

Each post uses `/notebooklm-generate-blog-post` with the module tutorial as input, enriched with companion artifacts (podcast, flashcards, quiz, mind map).

---

## Timeline Summary

| Phase | Sessions | Focus |
|-------|----------|-------|
| **Phase 1: Training** | ~35 sessions | Module tutorials + production implementation |
| **Phase 2: Hardening** | ~10 sessions | Coverage, types, CLI, CI/CD, PyPI |
| **Phase 3: Publication** | ~5 sessions | Blog series (7 posts), diagrams, GitHub polish |

**Total: ~50 sessions at one concept per session.**

---

*Last updated: 2026-03-15*
*Project: learn-fluent-python-clinical / clinicalnlp v0.1.0*
