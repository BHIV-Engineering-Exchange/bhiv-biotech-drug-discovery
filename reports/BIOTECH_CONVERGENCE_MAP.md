# BIOTECH_CONVERGENCE_MAP

**Project:** TB Drug Discovery Research and Candidate Intelligence Pipeline  
**Repository:** `bhiv-biotech-drug-discovery`  
**Last updated:** 20 November 2026  
**Purpose:** Maps how data, evidence, interfaces, and logic flow from raw sources through to final scored outputs

---

## 1. Overview

The pipeline converges evidence from static and dynamic curated sources through a four-stage processing chain:  
**Collect → Validate → Score → Report**

```
┌─────────────────────────────────────────────────────────┐
│                   EVIDENCE SOURCES                       │
│  PubChem · ChEMBL · PubMed · UniProt                    │
│  (Manual Curation + external_api_client.py REST Ingest) │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  CANONICAL DATASET                       │
│            candidate_compounds.csv (17 fields)           │
│                    10 candidates                         │
└──┬──────────────┬──────────────────────┬────────────────┘
   │              │                      │
   ▼              ▼                      ▼
[Search/Filter] [Completeness]    [v1 JSON Records]
drug_discovery   calculate_         candidate_
pipeline.py      completeness.py    records_v1.json (with score_inputs)
   │              │                      │
   ▼              ▼                      ▼
[CLI Output]  [Stdout %]        candidate_provenance.py
                                (adds provenance & score block)
                                         │
                                         ▼
                              candidate_records_with_
                                provenance.json
                                         │
                           ┌─────────────┴──────────────┐
                           ▼                             ▼
                  calculate_scores_v2.py        calculate_scores.py
                  (JSON-driven, 8-dim)          (CSV-driven, baseline)
                           │                             │
                           ▼                             ▼
               candidate_comparison_          candidate_comparison_
                results_v2.json (COMPLETE)    results.csv (ranked)
                           │
                           ▼
               pipeline_api.py & test_suite.py (18/18 PASS)
```

---

## 2. Stage-by-Stage Convergence

### Stage 1 — Evidence Collection
**Input:** External databases (PubChem, ChEMBL, PubMed)  
**Process:** Evidence curation by researcher + automated fetching via `external_api_client.py`  
**Output:** `candidate_compounds.csv` — 10 TB candidates, 17 fields each  
**Convergence point:** All evidence enters the pipeline here as a single flat CSV  

| Candidate | Source Databases | Key Identifier |
|---|---|---|
| C-001 Rifampicin | PubChem, PubMed | PubChem CID 135398735; ChEMBL CHEMBL374478 |
| C-002 Isoniazid | PubChem, ChEMBL | PubChem CID 3767; ChEMBL CHEMBL64 |
| C-003 Pyrazinamide | PubChem, PubMed | PubChem CID 1046; CAS 98-96-4 |
| C-004 Ethambutol | PubChem, ChEMBL | PubChem CID 14052; ChEMBL CHEMBL46221 |
| C-005 Bedaquiline | PubChem, ChEMBL, PubMed | PubChem CID 5460011; ChEMBL CHEMBL2103833 |
| C-006 Delamanid | PubChem, ChEMBL | PubChem CID 9884685; ChEMBL CHEMBL2105759 |
| C-007 Pretomanid | PubChem, ChEMBL | PubChem CID 467980; ChEMBL CHEMBL2107779 |
| C-008 Linezolid | PubChem, ChEMBL | PubChem CID 441401; ChEMBL CHEMBL126 |
| C-009 Clofazimine | PubChem, PubMed | PubChem CID 2794; CAS 2030-63-9 |
| C-010 Sutezolid | PubChem, PubMed | PubChem CID 11378442; CAS 168828-58-8 |

---

### Stage 2 — Validation & Provenance
**Input:** `candidate_records_v1.json` (CSV data + `source_evidence` block + `score.score_inputs`)  
**Process:** `candidate_provenance.py` validates structure and injects provenance metadata  
**Output:** `candidate_records_with_provenance.json`  
**Convergence point:** Each record carries source, schema version (1.0.0), transformation history, and declared derived fields

**Provenance block injected per record:**
```json
{
  "record_source": "candidate_compounds.csv",
  "schema_version": "1.0.0",
  "transformation": "Mapped the original 17-field candidate registry into the version 1 canonical candidate structure while preserving source evidence separately from derived comparison and score fields.",
  "derived_fields": ["derived_comparison", "score", "interpretation"]
}
```

---

### Stage 3 — Scoring (Two Paths)

#### Path A — v1 Baseline Scorer (CSV-driven)
**Input:** `candidate_compounds.csv`  
**Process:** `calculate_scores.py` applies `calculate_candidate_scores()` function  
**Output:** Stdout & `generate_comparison.py` ranking  

#### Path B — v2 Scoring Engine (JSON-driven)
**Input:** `candidate_records_with_provenance.json`  
**Process:** `calculate_scores_v2.py` evaluates the 8 scoring dimensions for each candidate  
**Output:** `candidate_comparison_results_v2.json`  
**Current state:** ✅ **COMPLETE** — All 10 candidates scored with valid numeric totals and deterministic rank ordering.

---

### Stage 4 — Comparison & Reporting
**Input:** Scored records from Stage 3  
**Process:** `generate_comparison.py` and `calculate_scores_v2.py` rank all candidates  
**Outputs:** 
- `candidate_comparison_results.csv` (CSV format)
- `candidate_comparison_results_v2.json` (JSON format with dimension breakdown)

**Converged Final Ranking (v1 and v2 aligned):**

| Rank | Candidate | Compound Name | Score | Status |
|---|---|---|---|---|
| 1 | C-002 | Isoniazid | 34/40 | COMPLETE |
| 2 | C-005 | Bedaquiline | 32/40 | COMPLETE |
| 3 | C-001 | Rifampicin | 30/40 | COMPLETE |
| 4 | C-008 | Linezolid | 30/40 | COMPLETE |
| 5 | C-004 | Ethambutol | 29/40 | COMPLETE |
| 6 | C-006 | Delamanid | 29/40 | COMPLETE |
| 7 | C-007 | Pretomanid | 29/40 | COMPLETE |
| 8 | C-003 | Pyrazinamide | 28/40 | COMPLETE |
| 9 | C-009 | Clofazimine | 25/40 | COMPLETE |
| 10 | C-010 | Sutezolid | 24/40 | COMPLETE |

---

## 3. APIs and Interfaces

Convergence between modules is orchestrated through programmatic interfaces and JSON schema contracts:

```
┌────────────────────────────────────────────────────────┐
│                      PIPELINE API                      │
│                    pipeline_api.py                     │
└──────┬───────────────┬───────────────┬───────────┬─────┘
       │               │               │           │
       ▼               ▼               ▼           ▼
[Search/Filter]  [Completeness]  [Provenance]  [Scoring v2]
drug_discovery_  calculate_      candidate_    calculate_
pipeline         completeness    provenance    scores_v2
       │               │               │           │
       └───────────────┼───────────────┴───────────┘
                       ▼
           [JSON Schema Enforcement]
           schema/candidate_record.schema.json
           schema/comparison_results.schema.json
```

### 3.1 Interface Convergence Specifications

| Interface Module | Consumed By | Input Contract | Output Contract |
|---|---|---|---|
| `pipeline_api.load_candidates` | Downstream applications | Optional `csv_path: str` | `List[Dict[str, str]]` with 17 fields |
| `pipeline_api.search_candidates` | Interactive UI / CLI | `term: str`, candidate list | Filtered list matching names/synonyms |
| `pipeline_api.assess_completeness` | Intelligence reports | Optional `csv_path: str` | `List[Dict]` with completed count and % |
| `pipeline_api.score_candidates_v2` | BIQOS / Downstream ranking | Canonical records list | Ranked list with dimension breakdown |
| `external_api_client.fetch_pubchem_compound` | Data collection stage | Compound name or CID | Molecular properties dict with provenance |
| `external_api_client.fetch_chembl_compound` | Data collection stage | ChEMBL ID | Activity & phase properties dict |

---

## 4. Test Runtime Execution

Convergence integrity is verified continuously through the test suite:

### 4.1 Convergence Validation Map
- **Stage 1 Convergence Tested:** TEST-01 (CSV loads), TEST-02 (17 columns), TEST-03 (All IDs), TEST-04 (No duplicates).
- **Stage 2 Convergence Tested:** TEST-14 (Schema validation of candidate records and provenance).
- **Stage 3 Convergence Tested:** TEST-08 (Missing input handling), TEST-11 (Reproducibility), TEST-12 (Tie-breaking), TEST-13 (10 COMPLETE records).
- **Stage 4 Convergence Tested:** TEST-15 (Schema validation of comparison output results).
- **API & Interface Layer Tested:** TEST-05, TEST-06, TEST-16, TEST-17, TEST-18.

### 4.2 Runtime Invocation
```powershell
python test_suite.py
```
- **Execution duration:** ~0.45s
- **Success criteria:** All 18 tests reporting `PASS` with exit status `0`.

---

## 5. Check Dependencies

Before initiating pipeline data convergence, ensure all prerequisites are verified:

### 5.1 Verification Script
Run the automated dependency checker:
```powershell
python -c "
import csv, json, os, pathlib, urllib.request, jsonschema
files = ['candidate_compounds.csv', 'candidate_records_v1.json', 'candidate_records_with_provenance.json']
for f in files:
    assert os.path.exists(f), f'Missing: {f}'
print('Convergence dependency check passed: all modules, packages, and data files ready.')
"
```

### 5.2 Prerequisite Checklist
- [x] Python 3.9+ runtime available
- [x] `jsonschema` library installed
- [x] Standard library modules `csv`, `json`, `os`, `pathlib`, `urllib` operational
- [x] Canonical CSV data file (`candidate_compounds.csv`) present in working directory
- [x] JSON Schemas available under `schema/` directory
