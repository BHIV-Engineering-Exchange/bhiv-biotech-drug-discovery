# BIOTECH_GAP_REGISTER

**Project:** TB Drug Discovery Research and Candidate Intelligence Pipeline  
**Repository:** `bhiv-biotech-drug-discovery`  
**Last updated:** 20 November 2026  
**Previous review:** 14 November 2026

---

## 1. Status Summary

All technical blockers across scoring, paths, provenance, modularity, integration contracts, and automated testing have been **resolved** as of 20 November 2026. The automated test suite passes 18/18 tests.

| Priority | Gap | Previous Status | Current Status |
|---|---|---|---|
| P1 | GAP-01 — Scoring scripts: broken CSV paths | ❌ FileNotFoundError | ✅ **FIXED** |
| P1 | GAP-02 — JSON files: `[1]` suffix naming | ❌ Files not found | ✅ **FIXED** |
| P1 | GAP-03 — Dataset limited to 10 candidates | ⚠️ Noted | ⚠️ Open (future research milestone) |
| P2 | GAP-04 — Potency/selectivity data incomplete | ⚠️ 8/10 UNKNOWN | ⚠️ Open (future scientific curation) |
| P2 | GAP-05 — ADME/PK/safety narrative only | ⚠️ Noted | ⚠️ Open (future scientific curation) |
| P2 | GAP-06 — Automated test script missing | ❌ No test script | ✅ **FIXED** (`test_suite.py` created, 18/18 pass) |
| P2 | GAP-07 — Repository layout anomalies | ❌ Placeholder files, `[1]` names | ✅ **FIXED** |
| P2 | GAP-08 — Broken import in `candidate_provenance.py` | ❌ AttributeError crash | ✅ **FIXED** |
| P3 | GAP-09 — Search/synonym test coverage | ⚠️ Noted | ✅ **FIXED** (covered in `test_suite.py`) |
| P3 | GAP-10 — BIQOS integration contract (JSON Schema) | ⚠️ Undefined | ✅ **FIXED** (`schema/` schemas validated) |
| P2 | GAP-11 — `score.score_inputs` populated in JSON records | ❌ INCOMPLETE status | ✅ **FIXED** (v2 scores 10/10 candidates COMPLETE) |
| P3 | GAP-12 — Modularity: importable functions across all scripts | ⚠️ CLI-only | ✅ **FIXED** (All 6 modules + `pipeline_api.py`) |
| P3 | GAP-13 — External database API integration client | ⚠️ None | ✅ **FIXED** (`external_api_client.py` operational) |

---

## 2. Resolved Gaps (Closed)

### GAP-01 — Scoring scripts used broken relative CSV paths ✅ CLOSED
**Root cause:** Scripts hardcoded `../candidate_compounds.csv`.  
**Fix applied:** Updated all scripts to script-relative path resolution using `__file__`.  
**Verified:** All scripts execute cleanly regardless of working directory. EXIT 0.

---

### GAP-02 — JSON files had `[1]` OneDrive sync suffix ✅ CLOSED
**Root cause:** OneDrive appended `[1]` to filenames during sync.  
**Fix applied:** Canonical names `candidate_records_v1.json` and `candidate_records_with_provenance.json` tracked; `[1]` duplicates removed.  
**Verified:** Both `candidate_provenance.py` and `calculate_scores_v2.py` load canonical files cleanly.

---

### GAP-06 — Automated test script was missing from repository ✅ CLOSED
**Fix applied:** Created `test_suite.py` with 18 automated tests covering CSV integrity, search, filtering, completeness, provenance, scoring engine, edge cases, JSON Schemas, modularity, and API client.  
**Verified:** 18/18 tests pass. EXIT 0.

---

### GAP-07 — Repository layout anomalies ✅ CLOSED
**Fix applied:** Removed 0-byte `sample_data` and `schema` placeholders, moved loose screenshots to `screenshorts/`, added `.gitignore` to prevent tracking `__pycache__` and byte-compiled files.

---

### GAP-08 — Broken import in `candidate_provenance.py` ✅ CLOSED
**Fix applied:** Path imports corrected to `from pathlib import Path`. Self-tests pass 7/7.

---

### GAP-09 — Search and filtering test coverage ✅ CLOSED
**Fix applied:** Full test coverage added in `test_suite.py` (TEST-05, TEST-06, TEST-17) verifying case-insensitive candidate name, synonym search, and multi-criteria filtering.

---

### GAP-10 — BIQOS integration contract (JSON Schema) ✅ CLOSED
**Fix applied:** Defined and committed standard JSON Schemas:
- `schema/candidate_record.schema.json`
- `schema/comparison_results.schema.json`  
**Verified:** Validated in `test_suite.py` via `jsonschema` (TEST-14, TEST-15).

---

### GAP-11 — `score.score_inputs` not populated in canonical JSON records ✅ CLOSED
**Fix applied:** Mapped the 8-dimension scoring matrix into `score.score_inputs` in `candidate_records_v1.json` and `candidate_provenance.py`.  
**Verified:** `calculate_scores_v2.py` processes all 10 candidates with status `COMPLETE`, producing ranks 1 to 10 in `candidate_comparison_results_v2.json`.

---

### GAP-12 — Three scripts had no importable functions (CLI-only) ✅ CLOSED
**Fix applied:** Refactored `calculate_completeness.py`, `calculate_scores.py`, and `generate_comparison.py` to expose pure callable functions with `if __name__ == "__main__"` guards. Added unified `pipeline_api.py`.  
**Verified:** Tested in TEST-16; all functions import and call without side effects.

---

### GAP-13 — External database API integration ✅ CLOSED
**Fix applied:** Created `external_api_client.py` providing PubChem PUG REST and ChEMBL query interfaces with local caching (`.api_cache.json`) and offline fallback.  
**Verified:** Tested in TEST-18.

---

## 3. APIs and Interfaces

To bridge previous gaps around pipeline extensibility, interoperability, and BIQOS integration, formal programmatic and schema contracts have been introduced:

### 3.1 Programmatic API Interface (`pipeline_api.py`)
Closes **GAP-12** by exposing pure Python functions without CLI side effects:
- `load_candidates(csv_path)`: Returns parsed candidate dictionaries.
- `search_candidates(term)`: Performs case-insensitive matching on names and synonyms.
- `filter_by_area(area)` & `filter_by_stage(stage)`: Substring filter methods.
- `assess_completeness(csv_path)`: Computes percentage and count of completed evidence fields.
- `score_candidates_v2(records)`: Invokes the 8-dimension scoring engine.
- `run_full_pipeline()`: End-to-end orchestration returning structured dictionary summary.

### 3.2 External Database Interfaces (`external_api_client.py`)
Closes **GAP-13** by replacing manual copy-paste with standardized data retrieval:
- `fetch_pubchem_compound(name_or_cid)`: PubChem PUG REST query with offline fallback.
- `fetch_chembl_compound(chembl_id)`: ChEMBL REST API molecule properties query.
- Caching: Persists query responses in `.api_cache.json` with provenance tracking (`retrieved_at`, `provenance_source`).

### 3.3 Data Contract Schemas (`schema/`)
Closes **GAP-10** by formalizing schemas for integration validation:
- [`schema/candidate_record.schema.json`](file:///c:/Users/sharc/OneDrive/Documents/BEE/Biotech/bhiv-biotech-drug-discovery/schema/candidate_record.schema.json): Governs candidate record format, requiring candidate identifiers, target, mechanism, source evidence, provenance, and 8-dimension score inputs.
- [`schema/comparison_results.schema.json`](file:///c:/Users/sharc/OneDrive/Documents/BEE/Biotech/bhiv-biotech-drug-discovery/schema/comparison_results.schema.json): Governs scoring engine output format, requiring method version, maximum score, dimensions, and candidate rankings.

---

## 4. Test Runtime Execution

Automated test execution prevents regression of previously identified gaps and guarantees runtime integrity across clean checkouts:

### 4.1 Execution Protocol
```powershell
python test_suite.py
```

### 4.2 Runtime Execution Results
```text
TB Drug Discovery Pipeline — Automated Test Suite
============================================================
  PASS  TEST-01 CSV loads with 10 candidates
  PASS  TEST-02 CSV schema has 17 columns
  PASS  TEST-03 All candidate IDs present
  PASS  TEST-04 No duplicate candidate IDs
  PASS  TEST-05 Synonym 'Rifampin' resolves to C-001
  PASS  TEST-06 Unknown term returns empty result
  PASS  TEST-07 Evidence gaps detected (>=8 candidates)
  PASS  TEST-08 Missing score input flagged as INCOMPLETE
  PASS  TEST-09 C-999 not in dataset
  PASS  TEST-10 Empty dataset returns empty results list
  PASS  TEST-11 Comparison reproducibility
  PASS  TEST-12 Deterministic tie-breaking (C-001 before C-002)
  PASS  TEST-13 v2 scoring produces 10 COMPLETE ranked candidates
  PASS  TEST-14 JSON Schema validates candidate records
  PASS  TEST-15 JSON Schema validates comparison results v2
  PASS  TEST-16 All modules expose callable importable functions
  PASS  TEST-17 Pipeline API filtering and search functional
  PASS  TEST-18 External API client queries cached data
============================================================
Results: 18/18 tests passed
All tests passed.
```

- **Execution speed:** < 0.5s wall-clock time.
- **Exit codes:** Strict code 0 on all tests passed; code 1 on any failure to block faulty CI merges.
- **Offline independence:** Tests run fully offline without external network dependencies.

---

## 5. Check Dependencies

To verify the pipeline environment before execution, use the following validation procedures:

### 5.1 Verification Checklist
1. **Python Interpreter:** Python 3.9+ (`python --version`).
2. **Standard Library Verification:**
   ```powershell
   python -c "import csv, json, os, pathlib, urllib.request; print('Standard library dependencies verified.')"
   ```
3. **Third-Party Package Verification:**
   ```powershell
   python -c "import jsonschema; print(f'jsonschema version: {jsonschema.__version__}')"
   ```
4. **File Conformance Check:**
   - Canonical CSV: `candidate_compounds.csv` (10 rows, 17 columns)
   - Canonical JSON: `candidate_records_v1.json` (10 objects with `score.score_inputs`)
   - Schemas: `schema/candidate_record.schema.json`, `schema/comparison_results.schema.json`

If any prerequisite is missing, run:
```powershell
pip install jsonschema
```

---

## 6. Open Strategic Milestones (Non-blocking)

### GAP-03 — Dataset expansion beyond 10 candidates
- **Current status:** Canonical dataset intentionally focuses on 10 benchmark TB candidates.
- **Future milestone:** Ingest wider candidate library via `external_api_client.py`.

### GAP-04 / GAP-05 — Quantitative pharmacology curation
- **Current status:** Potency/selectivity/ADME documented primarily in descriptive text.
- **Future milestone:** Deep literature extraction for IC50 / MIC numerical values.

---

## 7. Definition of Ready for Integration Review

- [x] All Python scripts execute without errors (EXIT 0)
- [x] 18/18 automated tests pass
- [x] Canonical JSON files present and validated against JSON Schemas
- [x] Provenance metadata on all records
- [x] 0-byte placeholder files and cache artifacts cleaned
- [x] `score_inputs` populated in JSON records (GAP-11)
- [x] All modules expose importable functions (GAP-12)
- [x] JSON Schema defined and validated (GAP-10)
- [x] External API client with caching implemented (GAP-13)
- [x] Unified Python API (`pipeline_api.py`) operational
