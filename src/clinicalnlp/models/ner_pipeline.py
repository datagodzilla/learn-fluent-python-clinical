"""
ner_pipeline.py — Composition over inheritance: the NERPipeline pattern.

Fluent Python Chapters 14-16 | Module 4 (models/)

Clinical Problem:
    Build a pipeline of NER extractors that can be combined flexibly.
    Avoid inheritance hell: MedicationExtractor(BioBERTExtractor(TransformerExtractor(...)))

Concepts taught:
    Composition over inheritance, Strategy pattern,
    operator overloading (__add__, __iadd__)

Reference: example-code-2e/14-inheritance/
"""

# TODO: Implement in deep-dive session — Module 4

# TODO: NERPipeline with extractors list, normalizer, validator (composition)
# TODO: __add__ to merge pipelines
# TODO: __iadd__ for pipeline += extractor
# TODO: Show anti-pattern first (deep inheritance), then fix with composition

pass
