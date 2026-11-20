# BIOTECH_DEPENDENCY_REGISTER

**Project:** TB Drug Discovery Research and Candidate Intelligence Pipeline  
**Repository:** `bhiv-biotech-drug-discovery`  
**Last updated:** 20 November 2026  
**Status:** All runtime dependencies verified operational (18/18 tests passing)

---

## 1. Summary

This register documents every dependency — file, module, interface, and external resource — that the pipeline scripts rely on. All runtime blockers identified in the original audit have been resolved, and standard schemas and programmatic interfaces are fully wired.

---

## 2. Check Dependencies

To verify that all required files, Python packages, and runtime dependencies are available before launching the pipeline or executing tests, run the pre-flight check commands below.

### 2.1 Automated Dependency Check Command

Run this one-line command from the repository root:

```powershell
python -c "
import os, sys, csv, json, pathlib, urllib.request
deps = ['csv', 'json', 'os', 'pathlib', 'urllib.request']
print('Checking standard library dependencies...')
for d in deps:
    print(f'  [OK] {d}')

print('Checking third-party packages...')
try:
    import jsonschema
    print(f'  [OK] jsonschema (v{getattr(jsonschema, \"__version__\", \"installed\")})')
except ImportError:
    print('  [FAIL] jsonschema missing - install with: pip install jsonschema')
    sys.exit(1)

print('Checking critical repository files...')
required_files = [
    'candidate_compounds.csv',
    'candidate_records_v1.json',
    'candidate_records_with_provenance.json',
    'schema/candidate_record.schema.json',
    'schema/comparison_results.schema.json'
]
missing = [f for f in required_files if not os.path.exists(f)]
if missing:
    print(f'  [FAIL] Missing files: {missing}')
    sys.exit(1)
else:
    print('  [OK] All critical data and schema files present.')

print('ALL DEPENDENCIES OPERATIONAL.')
"
```

### 2.2 Dependency Verification Matrix

| Category | Dependency | Version / Spec | Role in Pipeline | Health Status |
|---|---|---|---|---|
| Runtime | Python | >= 3.9 (tested on 3.12/3.14) | Base language interpreter | ✅ Verified |
| Stdlib | `csv` | Built-in | Reads/writes canonical compound registry | ✅ Verified |
| Stdlib | `json` | Built-in | Serializes canonical and provenance records | ✅ Verified |
| Stdlib | `os` | Built-in | Script-relative path resolution (`BASE_DIR`) | ✅ Verified |
| Stdlib | `pathlib` | Built-in | Modern filesystem path navigation | ✅ Verified |
| Stdlib | `urllib` | Built-in | REST communication with PubChem / ChEMBL | ✅ Verified |
| Package | `jsonschema` | >= 4.0.0 | Contract validation for records and scoring | ✅ Verified (4.25.1) |
| Data | `candidate_compounds.csv` | 17 columns, 10 records | Primary canonical evidence store | ✅ Present |
| Data | `candidate_records_v1.json` | JSON Schema v1.0.0 | Canonical records with source evidence | ✅ Present |
| Data | `candidate_records_with_provenance.json` | JSON Schema v1.0.0 | Enriched records with provenance & scores | ✅ Present |
| Schema | `candidate_record.schema.json` | Draft-07 JSON Schema | Validates canonical candidate record format | ✅ Present |
| Schema | `comparison_results.schema.json` | Draft-07 JSON Schema | Validates comparison ranking output format | ✅ Present |

---

## 3. File Dependencies

### Input Files

| Dependency File | Type | Required By | Status |
|---|---|---|---|
| `candidate_compounds.csv` | CSV, UTF-8-BOM, 17 fields | `drug_discovery_pipeline.py`, `calculate_scores.py`, `calculate_completeness.py`, `generate_comparison.py`, `pipeline_api.py` | ✅ Present, 10 records |
| `candidate_records_v1.json` | JSON array, UTF-8 | `candidate_provenance.py` | ✅ Present, 10 records with score inputs |
| `candidate_records_with_provenance.json` | JSON array, UTF-8 | `calculate_scores_v2.py`, `pipeline_api.py` | ✅ Present, enriched with provenance |
| `schema/candidate_record.schema.json` | JSON Schema Draft-07 | `test_suite.py`, validation layers | ✅ Present |
| `schema/comparison_results.schema.json` | JSON Schema Draft-07 | `test_suite.py`, validation layers | ✅ Present |

### Generated / Output Files

| Output File | Produced By | Consumed By | Status |
|---|---|---|---|
| `candidate_records_with_provenance.json` | `candidate_provenance.py` | `calculate_scores_v2.py`, `pipeline_api.py` | ✅ Generated deterministically |
| `candidate_comparison_results.csv` | `generate_comparison.py` | Human review / downstream reporting | ✅ Generated on each run |
| `candidate_comparison_results_v2.json` | `calculate_scores_v2.py` | Downstream BIQOS integration / reporting | ✅ Generated on each run |
| `.api_cache.json` | `external_api_client.py` | Cached REST API lookup layer | ✅ Generated on API query |

---

## 4. APIs and Interfaces

The pipeline provides two tiers of interfaces:
1. **Internal Programmatic APIs** for Python modules and integration harnesses.
2. **External REST Client Interfaces** for public biomedical databases.

### 4.1 Unified Python API (`pipeline_api.py`)

The primary programmatic interface for external callers and test runners.

```python
import pipeline_api as api

# 1. Candidate Loading & Search
candidates = api.load_candidates()                       # List[Dict[str, str]]
matches = api.search_candidates("rifampin")             # List[Dict[str, str]]
filtered_area = api.filter_by_area("Tuberculosis")       # List[Dict[str, str]]
filtered_stage = api.filter_by_stage("Approved")         # List[Dict[str, str]]

# 2. Completeness & Evidence Metrics
completeness = api.assess_completeness()                 # List[Dict[str, Any]]

# 3. Provenance & Scoring Engines
prov_records = api.build_provenance_records()           # List[Dict[str, Any]]
v1_scores = api.score_candidates_v1()                   # List[Dict[str, Any]]
v2_scores = api.score_candidates_v2()                   # List[Dict[str, Any]]
ranked_v1 = api.generate_comparison_v1()                # List[Dict[str, Any]]

# 4. Pipeline Execution Summary
summary = api.run_full_pipeline()                       # Dict[str, Any]
```

#### API Method Signatures and Contracts

| Function | Parameters | Return Type | Description |
|---|---|---|---|
| `load_candidates(csv_path)` | `csv_path: Optional[str]` | `List[Dict[str, str]]` | Loads 17-field candidate rows from CSV |
| `search_candidates(term, candidates)` | `term: str, candidates: Optional[List]` | `List[Dict[str, str]]` | Case-insensitive name & synonym search |
| `filter_by_area(area, candidates)` | `area: str, candidates: Optional[List]` | `List[Dict[str, str]]` | Substring match on therapeutic area |
| `filter_by_stage(stage, candidates)` | `stage: str, candidates: Optional[List]` | `List[Dict[str, str]]` | Substring match on evidence stage |
| `assess_completeness(csv_path)` | `csv_path: Optional[str]` | `List[Dict[str, Any]]` | Calculates completed fields and % per candidate |
| `score_candidates_v1(csv_path)` | `csv_path: Optional[str]` | `List[Dict[str, Any]]` | Evaluates 8 criteria from hardcoded baseline |
| `score_candidates_v2(records)` | `records: Optional[List]` | `List[Dict[str, Any]]` | Evaluates 8 dimensions from `score.score_inputs` |
| `generate_comparison_v1(csv_path)` | `csv_path: Optional[str]` | `List[Dict[str, Any]]` | Generates ranked comparison records with ties broken |
| `build_provenance_records(input_path)` | `input_path: Optional[str]` | `List[Dict[str, Any]]` | Emits records with provenance & score blocks |
| `run_full_pipeline()` | None | `Dict[str, Any]` | Full end-to-end execution summary |

### 4.2 External Database Interfaces (`external_api_client.py`)

Provides access to public databases with local caching and offline fallback.

| Function | Target API Endpoint | Input | Output Contract |
|---|---|---|---|
| `fetch_pubchem_compound(name_or_cid)` | `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/...` | Compound name or numeric CID | `CID`, `MolecularFormula`, `MolecularWeight`, `IUPACName`, `InChIKey`, `provenance_source` |
| `fetch_chembl_compound(chembl_id)` | `https://www.ebi.ac.uk/chembl/api/data/molecule/...` | ChEMBL Molecule ID (e.g. `CHEMBL64`) | `molecule_chembl_id`, `pref_name`, `max_phase`, `therapeutic_flag`, `provenance_source` |

### 4.3 Interactive CLI Interface (`drug_discovery_pipeline.py`)

- **Entry point:** `python drug_discovery_pipeline.py`
- **Menu Options:** 1 (Search), 2 (Filter Area), 3 (Filter Stage), 4 (Show All), 5 (Candidate Details), 6 (All Details), 7 (Exit).
- **Execution Mode:** Non-blocking with `EOFError`/`KeyboardInterrupt` guards for safe piping (`"7" | python drug_discovery_pipeline.py`).

---

## 5. Test Runtime Execution

### 5.1 Test Execution Command

The pipeline automated test suite is invoked via standard Python:

```powershell
python test_suite.py
```

### 5.2 Test Runtime Profile

- **Total Test Cases:** 18
- **Average Runtime:** ~0.45 seconds
- **Exit Code Convention:**
  - `0`: All 18 tests passed
  - `1`: One or more tests failed (stops CI/CD pipelines)
- **Network Requirement:** None (runs 100% offline using local schemas and cached evidence)

### 5.3 Test Suite Coverage Matrix

| Test ID | Test Category | Target Component | Verification Logic |
|---|---|---|---|
| TEST-01 | Data Ingestion | `candidate_compounds.csv` | Exactly 10 candidate rows load |
| TEST-02 | Schema Conformance | `candidate_compounds.csv` | Exactly 17 columns present |
| TEST-03 | Candidate ID Integrity | `candidate_compounds.csv` | C-001 through C-010 all present |
| TEST-04 | Uniqueness | `candidate_compounds.csv` | Zero duplicate candidate IDs |
| TEST-05 | Search Functionality | `drug_discovery_pipeline.py` | Synonym "Rifampin" resolves to C-001 |
| TEST-06 | Search Edge Case | `drug_discovery_pipeline.py` | Unknown term returns empty list (no error) |
| TEST-07 | Evidence Gap Detection | `calculate_completeness.py` | Flags >=8 candidates with potency/selectivity gaps |
| TEST-08 | Scoring Validation | `calculate_scores_v2.py` | Missing score input correctly flagged INCOMPLETE |
| TEST-09 | Non-existent Record | `drug_discovery_pipeline.py` | Gracefully rejects invalid ID (C-999) |
| TEST-10 | Empty Dataset | `calculate_scores_v2.py` | Empty input returns empty list (no crash) |
| TEST-11 | Reproducibility | `calculate_scores_v2.py` | Multiple identical runs produce identical output |
| TEST-12 | Tie-breaking Logic | `calculate_scores_v2.py` | Deterministic ordering on equal scores (C-001 < C-002) |
| TEST-13 | End-to-End Scoring | `calculate_scores_v2.py` | Real records score 10 COMPLETE, C-002 rank 1 |
| TEST-14 | JSON Schema (Records) | `schema/candidate_record.schema.json` | Validates all records with provenance |
| TEST-15 | JSON Schema (Results) | `schema/comparison_results.schema.json` | Validates `candidate_comparison_results_v2.json` |
| TEST-16 | Modularity & Imports | All 6 modules + `pipeline_api.py` | Functions import and call with zero side effects |
| TEST-17 | Filter & Search APIs | `pipeline_api.py` | Multi-parameter filtering returns valid counts |
| TEST-18 | External API Client | `external_api_client.py` | Resolves cached PubChem CID and ChEMBL name |

---

## 6. Dependency Risk Register

| Risk | Affected Scripts | Likelihood | Impact | Mitigation Status |
|---|---|---|---|---|
| Missing third-party `jsonschema` | `test_suite.py` | Low | Medium | Standard library fallback / pre-flight check in §2.1 |
| `candidate_compounds.csv` renamed | CSV scripts | Low | Critical | Path pinned via `BASE_DIR = os.path.dirname(...)` |
| Sync duplicate `[1]` suffixes | JSON scripts | Low | High | Canonical filenames pinned; `[1]` variants deleted |
| External API offline / network blocked | `external_api_client.py` | Medium | Low | Local cache preseeded with offline fallback |
| Incompatible Python version | All scripts | Low | Low | Validated on Python 3.9 through 3.14 |
