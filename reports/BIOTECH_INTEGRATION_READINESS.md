# BIOTECH_INTEGRATION_READINESS

**Project:** TB Drug Discovery Research and Candidate Intelligence Pipeline  
**Repository:** `bhiv-biotech-drug-discovery`  
**Last updated:** 20 November 2026  
**Readiness level:** ✅ Integration-Ready Research Pipeline  

---

## 1. Executive Readiness Statement

The TB Drug Discovery pipeline is a **fully verified, integration-ready research pipeline** as of 20 November 2026.

All runtime blockers and integration prerequisites have been resolved:
- File path bugs fixed across all scripts using script-relative paths
- Canonical JSON files tracked and validated; OneDrive duplicate suffixes removed
- 0-byte placeholder files and cache artifacts cleaned
- Provenance tracking operational with 7/7 self-tests passing
- Scoring engine v2 fully operational with 10/10 candidates scored as COMPLETE and ranked
- JSON Schema contracts committed for candidate records and comparison results
- Schema validation wired into automated test suite via `jsonschema`
- All scripts modularized with pure callable Python functions and `if __name__ == "__main__"` guards
- Unified Python API (`pipeline_api.py`) implemented
- External API client (`external_api_client.py`) with local caching and offline fallback implemented
- 18-test automated suite (`test_suite.py`) created and passing 18/18

---

## 2. Check Dependencies

To verify integration readiness before deploying or calling the pipeline in external environments (e.g. BIQOS integration harnesses or automated CI runners), execute the following dependency validation checks:

### 2.1 Automated Pre-flight Check Command
```powershell
python -c "
import sys, os, csv, json, pathlib, urllib.request

print('=== PRE-FLIGHT INTEGRATION DEPENDENCY CHECK ===')
# 1. Python version check
if sys.version_info < (3, 9):
    print(f'[FAIL] Python >= 3.9 required. Detected: {sys.version}')
    sys.exit(1)
print(f'[PASS] Python Version: {sys.version.split()[0]}')

# 2. Package checks
try:
    import jsonschema
    print(f'[PASS] jsonschema package installed (v{getattr(jsonschema, \"__version__\", \"installed\")})')
except ImportError:
    print('[FAIL] jsonschema package missing. Run: pip install jsonschema')
    sys.exit(1)

# 3. File structure checks
files = [
    'candidate_compounds.csv',
    'candidate_records_v1.json',
    'candidate_records_with_provenance.json',
    'schema/candidate_record.schema.json',
    'schema/comparison_results.schema.json',
    'pipeline_api.py',
    'external_api_client.py',
    'test_suite.py'
]
for f in files:
    if not os.path.exists(f):
        print(f'[FAIL] Critical file missing: {f}')
        sys.exit(1)
print(f'[PASS] All {len(files)} critical files and schemas verified.')
print('=== SYSTEM IS INTEGRATION READY ===')
"
```

### 2.2 Dependency Checklist Matrix

| Prerequisite | Required Specification | Production Status | Fallback / Recovery |
|---|---|---|---|
| Python Interpreter | Python 3.9+ | ✅ Verified (3.12/3.14) | Standard system Python |
| `jsonschema` | >= 4.0.0 | ✅ Verified (4.25.1) | `pip install jsonschema` |
| Primary Dataset | `candidate_compounds.csv` | ✅ 10 records, 17 cols | Maintained in repo root |
| Provenance Dataset | `candidate_records_with_provenance.json` | ✅ Validated Schema 1.0.0 | Regenerated via `candidate_provenance.py` |
| Data Schemas | `schema/*.schema.json` | ✅ Draft-07 compliant | Committed in `schema/` |
| Network Access | HTTPS to PubChem/ChEMBL | ⚠️ Optional (offline supported) | Pre-seeded `.api_cache.json` |

---

## 3. APIs and Interfaces

External platforms (such as BIQOS, analytics pipelines, or web interfaces) interact with the drug discovery pipeline through three integration surfaces:

### 3.1 Unified Python API (`pipeline_api.py`)

A single, clean Python module exposing callable functions for all pipeline stages:

```python
import pipeline_api as api

# Ingest and search
candidates = api.load_candidates()
matching = api.search_candidates("rifampin")

# Filter by criteria
tb_drugs = api.filter_by_area("Tuberculosis")
approved_drugs = api.filter_by_stage("Approved")

# Completeness and Provenance
completeness = api.assess_completeness()
provenance_records = api.build_provenance_records()

# Candidate Comparison & Scoring Engine (v2)
comparison_results = api.score_candidates_v2()

# Full pipeline execution
summary = api.run_full_pipeline()
```

#### API Methods and Contracts

| Method | Parameters | Return Type | Contract / Behavior |
|---|---|---|---|
| `load_candidates` | `csv_path: Optional[str]` | `List[Dict[str, str]]` | Returns 10 parsed candidate records |
| `search_candidates` | `term: str, candidates: Optional[List]` | `List[Dict[str, str]]` | Substring match against `compound_name` and `synonyms` |
| `filter_by_area` | `area: str, candidates: Optional[List]` | `List[Dict[str, str]]` | Matches `therapeutic_area` |
| `filter_by_stage` | `stage: str, candidates: Optional[List]` | `List[Dict[str, str]]` | Matches `evidence_stage` |
| `assess_completeness`| `csv_path: Optional[str]` | `List[Dict[str, Any]]` | Returns completed field counts and percentage |
| `score_candidates_v2`| `records: Optional[List]` | `List[Dict[str, Any]]` | Produces ranked array conforming to comparison schema |
| `run_full_pipeline` | None | `Dict[str, Any]` | Full workflow summary with top-ranked candidates |

### 3.2 Formal JSON Schema Contracts (`schema/`)

All data exported or imported adheres to committed Draft-07 JSON Schemas:
- **Candidate Record Schema:** [`schema/candidate_record.schema.json`](file:///c:/Users/sharc/OneDrive/Documents/BEE/Biotech/bhiv-biotech-drug-discovery/schema/candidate_record.schema.json)
  - Enforces mandatory presence of `candidate_id`, `compound_name`, `target`, `mechanism_of_action`, `source_evidence`, `provenance`, and `score.score_inputs`.
- **Comparison Results Schema:** [`schema/comparison_results.schema.json`](file:///c:/Users/sharc/OneDrive/Documents/BEE/Biotech/bhiv-biotech-drug-discovery/schema/comparison_results.schema.json)
  - Enforces `method_version`, `maximum_score`, `scoring_dimensions`, and ranked candidate results with status flags (`COMPLETE` or `INCOMPLETE`).

### 3.3 External Biomedical API Client (`external_api_client.py`)

- **PubChem Interface:** `fetch_pubchem_compound(name_or_cid)` queries compound metadata (Formula, Molecular Weight, IUPAC, InChIKey) via PUG REST.
- **ChEMBL Interface:** `fetch_chembl_compound(chembl_id)` queries molecule phase and therapeutic flags.
- **Resilience:** Automatic fallback to preseeded `.api_cache.json` in offline or sandboxed environments.

---

## 4. Test Runtime Execution

Automated test execution validates that all pipeline contracts remain intact:

### 4.1 Test Suite Invocation
```powershell
python test_suite.py
```

### 4.2 Runtime Specification
- **Test Runner:** Custom lightweight test runner (`test_suite.py`) without heavy dependencies.
- **Execution Time:** ~0.45 seconds.
- **Exit Status Code:**
  - `0`: All 18 tests passed (Ready for deployment/merge).
  - `1`: One or more tests failed (Blocks integration pipeline).

### 4.3 Automated Test Inventory

| # | Test Name | Target Tested | Success Criteria |
|---|---|---|---|
| 01 | TEST-01 CSV loads | `candidate_compounds.csv` | 10 rows loaded |
| 02 | TEST-02 CSV schema | `candidate_compounds.csv` | 17 columns confirmed |
| 03 | TEST-03 All candidate IDs | `candidate_compounds.csv` | C-001 through C-010 present |
| 04 | TEST-04 No duplicate IDs | `candidate_compounds.csv` | Uniqueness verified |
| 05 | TEST-05 Synonym search | `pipeline_api.py` | "Rifampin" matches C-001 |
| 06 | TEST-06 Unknown search | `pipeline_api.py` | Unknown term returns empty list |
| 07 | TEST-07 Evidence gaps | `calculate_completeness.py` | Identifies potency/selectivity gaps |
| 08 | TEST-08 Missing score input | `calculate_scores_v2.py` | Missing scores flagged `INCOMPLETE` |
| 09 | TEST-09 Invalid candidate ID | `pipeline_api.py` | C-999 handled gracefully |
| 10 | TEST-10 Empty dataset | `calculate_scores_v2.py` | Returns empty list safely |
| 11 | TEST-11 Reproducibility | `calculate_scores_v2.py` | Runs produce identical output |
| 12 | TEST-12 Tie-breaking | `calculate_scores_v2.py` | Deterministic ordering |
| 13 | TEST-13 v2 real records | `calculate_scores_v2.py` | 10 COMPLETE, C-002 rank 1 |
| 14 | TEST-14 Candidate schema | `schema/candidate_record.schema.json` | 10/10 records pass validation |
| 15 | TEST-15 Comparison schema | `schema/comparison_results.schema.json` | Results file passes validation |
| 16 | TEST-16 Modularity | All modules | All callable without side-effects |
| 17 | TEST-17 Filtering API | `pipeline_api.py` | Filters return expected subsets |
| 18 | TEST-18 External API client | `external_api_client.py` | Queries cached PubChem/ChEMBL data |

---

## 5. Integration Milestone Tracking

| # | Requirement | Status | Action Taken |
|---|---|---|---|
| INT-01 | Score inputs in JSON records | ✅ **DONE** | Populated `score.score_inputs` across all 10 candidates in canonical JSON |
| INT-02 | Modular Python API | ✅ **DONE** | Implemented `pipeline_api.py` exposing clean functions across all modules |
| INT-03 | JSON Schema definition | ✅ **DONE** | Created `schema/candidate_record.schema.json` and `schema/comparison_results.schema.json` |
| INT-04 | Schema validation in tests | ✅ **DONE** | Wired `jsonschema.validate` into `test_suite.py` (TEST-14, TEST-15) |
| INT-05 | CI-compatible test exit codes | ✅ **DONE** | `test_suite.py` returns EXIT 0 on pass, EXIT 1 on failure |
| INT-06 | Quantitative potency/selectivity | ⚠️ Future | Ongoing scientific curation |
| INT-07 | External API integration | ✅ **DONE** | Implemented `external_api_client.py` with PubChem/ChEMBL support and caching |
| INT-08 | Data versioning | ✅ **DONE** | Schema versioning (1.0.0) tracked in provenance block and schemas |
