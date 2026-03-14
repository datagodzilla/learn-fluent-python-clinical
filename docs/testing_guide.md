# Testing Guide

> pytest patterns and clinical NLP testing idioms

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=clinicalnlp --cov-report=term-missing

# Run single module
pytest tests/test_core.py -v

# Run async tests
pytest tests/test_streaming.py -v
```

## Fixtures
<!-- conftest.py fixtures: sample_patient, snomed_concepts, etc. -->

## Testing Patterns
<!-- Will be populated as modules are implemented -->

### Parametrize
### Fixtures with scope
### Async tests (pytest-asyncio)
### Mocking external APIs
### Testing special methods (__eq__, __hash__, __repr__)

## Coverage Goals
<!-- Per-module coverage targets -->
