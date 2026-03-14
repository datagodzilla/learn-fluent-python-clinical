"""
fhir_bundle.py — FHIRBundle class demonstrating collection protocols.

Fluent Python Chapters 1-3 | Module 1 (core/)

Clinical Problem:
    Model a FHIR R4 Bundle as a Python collection that supports
    iteration, length, indexing, and merging (via + operator).

Dunders implemented:
    __iter__, __len__, __getitem__, __add__

Reference: FHIR R4 Bundle resource (collection of FHIR resources)
"""

# TODO: Implement in deep-dive session — Module 1


class FHIRBundle:
    """A collection of FHIR R4 resources that behaves like a Python sequence.

    WHY: FHIR Bundles are the standard transport container in health IT.
    Making them iterable and sliceable means they work naturally with
    Python's for loops, list comprehensions, and sorted().
    """

    # TODO: Implement __init__ with resource_type and entries list
    # TODO: Implement __iter__ -> iterate over entries
    # TODO: Implement __len__ -> number of entries
    # TODO: Implement __getitem__ -> index/slice entries
    # TODO: Implement __add__ -> merge two bundles (bundle_a + bundle_b)

    pass
