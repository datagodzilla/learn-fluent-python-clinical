# Clinical Glossary

> Single source of truth for domain terms used throughout the clinicalnlp package.

## Terminology Systems

| System | Full Name | Purpose | Example |
|--------|-----------|---------|---------|
| **SNOMED CT** | Systematized Nomenclature of Medicine - Clinical Terms | Clinical findings, procedures, body structures | `73211009` = Diabetes mellitus |
| **LOINC** | Logical Observation Identifiers Names and Codes | Laboratory and clinical observations | `2339-0` = Glucose [Mass/vol] in Ser/Plas |
| **RxNorm** | RxNorm (NLM) | Normalized medication names and codes | `860975` = Metformin 500 MG Oral Tablet |
| **ICD-10-CM** | International Classification of Diseases, 10th Rev, Clinical Modification | Diagnosis coding for billing and epidemiology | `E11.9` = Type 2 DM without complications |
| **CPT** | Current Procedural Terminology | Procedure coding for billing | `99213` = Office visit, level 3 |
| **HCPCS** | Healthcare Common Procedure Coding System | Supplies, equipment, non-physician services | `J0178` = Aflibercept injection |
| **OMOP CDM** | Observational Medical Outcomes Partnership Common Data Model | Standardized research data model | `concept_id: 201826` = Type 2 DM |
| **UMLS** | Unified Medical Language System | Cross-vocabulary concept mapping | CUI-based lookup across all vocabularies |
| **FHIR R4** | Fast Healthcare Interoperability Resources, Release 4 | Healthcare data exchange standard | Patient, Observation, Bundle resources |
| **DICOM** | Digital Imaging and Communications in Medicine | Medical imaging standard | Image metadata, radiology reports |

## Data Standards

### FHIR R4 Resources Used in This Package

| Resource | Purpose | Package Location |
|----------|---------|-----------------|
| **Patient** | Demographics, identifiers (MRN) | `core/clinical_record.py` |
| **Observation** | Lab results, vitals | `containers/record_store.py`, `models/fhir_resource.py` |
| **Condition** | Diagnoses (ICD-10, SNOMED) | `core/clinical_record.py` |
| **MedicationRequest** | Prescriptions (RxNorm) | `containers/vocabulary.py` |
| **Bundle** | Collection of resources | `core/fhir_bundle.py` |
| **AuditEvent** | HIPAA audit trail | `pipeline/decorators.py` |
| **Practitioner** | Provider information | Data files |

### OMOP CDM Tables Referenced

| Table | Purpose | Package Location |
|-------|---------|-----------------|
| `concept` | concept_id, concept_name, vocabulary_id, concept_code | `containers/vocabulary.py` |
| `concept_relationship` | Maps between vocabularies | `containers/vocabulary.py` |
| `person` | Patient demographics | `core/clinical_record.py` |
| `condition_occurrence` | Diagnoses | `containers/note_registry.py` |
| `drug_exposure` | Medications | `containers/note_registry.py` |
| `measurement` | Lab values | `containers/record_store.py` |
| `note` | Clinical notes (for NLP) | `streaming/generators.py` |
| `note_nlp` | NLP output table | `models/ner_pipeline.py` |

## Common Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| **MRN** | Medical Record Number — unique patient identifier within a health system |
| **DOB** | Date of Birth |
| **PHI** | Protected Health Information — data covered by HIPAA privacy rules |
| **HIPAA** | Health Insurance Portability and Accountability Act |
| **EHR** | Electronic Health Record |
| **NER** | Named Entity Recognition — extracting clinical entities from text |
| **NLP** | Natural Language Processing |
| **CDS** | Clinical Decision Support |
| **ETL** | Extract, Transform, Load — data pipeline pattern |
| **CDM** | Common Data Model (usually OMOP CDM) |
| **CUI** | Concept Unique Identifier (UMLS) |
| **MAC** | Medicare Administrative Contractor |
| **DRG** | Diagnosis-Related Group |
| **T2DM** | Type 2 Diabetes Mellitus |
| **CKD** | Chronic Kidney Disease |
| **COPD** | Chronic Obstructive Pulmonary Disease |
| **HF** | Heart Failure |
| **AKI** | Acute Kidney Injury |
| **DVT** | Deep Vein Thrombosis |

## Data Sources

| Source | Type | Usage in Package |
|--------|------|-----------------|
| **Synthea** | Synthetic patient generator | Realistic but fictional patient records |
| **MIMIC** | De-identified ICU database | Conceptual reference for note structure (we use synthetic stand-ins) |
| **HAPI FHIR** | Public FHIR test server | Real async HTTP calls in Module 5 |

## Key Relationships

```
Patient (MRN) ──has──> Observations (LOINC codes)
                ──has──> Conditions (SNOMED/ICD-10 codes)
                ──has──> Medications (RxNorm codes)
                ──has──> Notes (free text for NLP)

OMOP concept table ──maps──> SNOMED, LOINC, RxNorm, ICD-10 codes
                    ──via──> concept_relationship table

FHIR Bundle ──contains──> Patient + Observation + Condition + MedicationRequest
```
