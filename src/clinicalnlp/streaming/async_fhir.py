"""
async_fhir.py — Async FHIR R4 API calls with httpx and asyncio.

Fluent Python Chapter 21 | Module 5 (streaming/)

Clinical Problem:
    Fetch patient data from a FHIR R4 server concurrently.
    Sequential: 100 patients x 200ms = 20 seconds.
    Concurrent: 100 patients via asyncio.gather = ~1 second.

Concepts taught:
    async def, await, asyncio.gather, async context managers,
    httpx.AsyncClient

Reference: example-code-2e/21-async/
Note: This module uses real FHIR endpoints (HAPI FHIR test server)
      per the Layered Data decision — Modules 1-4 use offline data.
"""

# Standard library
import asyncio

# TODO: Implement in deep-dive session — Module 5

# TODO: async fetch_patient(client, mrn) -> dict
# TODO: async fetch_observations(client, patient_id) -> list
# TODO: async batch_fetch(mrns) using asyncio.gather()
# TODO: Show sequential vs concurrent timing comparison

pass
