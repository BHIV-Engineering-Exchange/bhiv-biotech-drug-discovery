"""
TB Drug Discovery Pipeline — Automated Test Suite
Covers Phase 8 requirements: 12 test cases across CSV integrity,
search, filtering, scoring, completeness, and edge-case handling.
Run with: python test_suite.py
"""

import csv
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "candidate_compounds.csv")
JSON_PROVENANCE = os.path.join(BASE_DIR, "candidate_records_with_provenance.json")
JSON_V1 = os.path.join(BASE_DIR, "candidate_records_v1.json")

EXPECTED_COLUMNS = 17
EXPECTED_CANDIDATES = 10
EXPECTED_CANDIDATE_IDS = {
    "C-001", "C-002", "C-003", "C-004", "C-005",
    "C-006", "C-007", "C-008", "C-009", "C-010"
}
SCORE_FIELDS = [
    "target_relevance", "mechanism_evidence", "potency_evidence",
    "selectivity_evidence", "adme_evidence", "safety_evidence",
    "research_development_evidence", "evidence_completeness"
]

PASSED = []
FAILED = []


def result(name, passed, detail=""):
    if passed:
        PASSED.append(name)
        print(f"  PASS  {name}")
    else:
        FAILED.append(name)
        print(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# TEST-01  Valid candidate CSV loads and contains expected record count
# ---------------------------------------------------------------------------
def test_01_csv_loads():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        result("TEST-01 CSV loads with 10 candidates", len(rows) == EXPECTED_CANDIDATES,
               f"got {len(rows)}")
    except FileNotFoundError:
        result("TEST-01 CSV loads with 10 candidates", False, "CSV file missing")


# ---------------------------------------------------------------------------
# TEST-02  CSV schema has exactly 17 columns
# ---------------------------------------------------------------------------
def test_02_csv_schema():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cols = reader.fieldnames or []
        result("TEST-02 CSV schema has 17 columns", len(cols) == EXPECTED_COLUMNS,
               f"got {len(cols)}")
    except FileNotFoundError:
        result("TEST-02 CSV schema has 17 columns", False, "CSV file missing")


# ---------------------------------------------------------------------------
# TEST-03  All expected candidate IDs are present
# ---------------------------------------------------------------------------
def test_03_candidate_ids():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        ids = {r["candidate_id"] for r in rows}
        missing = EXPECTED_CANDIDATE_IDS - ids
        result("TEST-03 All candidate IDs present", not missing,
               f"missing: {missing}")
    except FileNotFoundError:
        result("TEST-03 All candidate IDs present", False, "CSV file missing")


# ---------------------------------------------------------------------------
# TEST-04  No duplicate candidate IDs in CSV
# ---------------------------------------------------------------------------
def test_04_no_duplicate_ids():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        ids = [r["candidate_id"] for r in rows]
        duplicates = {i for i in ids if ids.count(i) > 1}
        result("TEST-04 No duplicate candidate IDs", not duplicates,
               f"duplicates: {duplicates}")
    except FileNotFoundError:
        result("TEST-04 No duplicate candidate IDs", False, "CSV file missing")


# ---------------------------------------------------------------------------
# TEST-05  Synonym search — Rifampin resolves to C-001
# ---------------------------------------------------------------------------
def test_05_synonym_search():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        term = "rifampin"
        matches = [r for r in rows
                   if term in r["compound_name"].lower()
                   or term in r["synonyms"].lower()]
        found = any(r["candidate_id"] == "C-001" for r in matches)
        result("TEST-05 Synonym 'Rifampin' resolves to C-001", found,
               f"matches: {[r['candidate_id'] for r in matches]}")
    except FileNotFoundError:
        result("TEST-05 Synonym search", False, "CSV file missing")


# ---------------------------------------------------------------------------
# TEST-06  Unknown search term returns no candidates (not an error)
# ---------------------------------------------------------------------------
def test_06_unknown_search():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        term = "tubercorin"
        matches = [r for r in rows
                   if term in r["compound_name"].lower()
                   or term in r["synonyms"].lower()]
        result("TEST-06 Unknown term returns empty result", len(matches) == 0,
               f"unexpected matches: {len(matches)}")
    except FileNotFoundError:
        result("TEST-06 Unknown search term", False, "CSV file missing")


# ---------------------------------------------------------------------------
# TEST-07  Incomplete evidence fields detected (potency / selectivity gaps)
# ---------------------------------------------------------------------------
def test_07_incomplete_evidence():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        gap_markers = {"UNKNOWN / NOT FOUND", "UNKNOWN", "NOT FOUND", ""}
        incomplete = [r["candidate_id"] for r in rows
                      if r.get("potency", "").strip().upper() in gap_markers
                      or r.get("selectivity", "").strip().upper() in gap_markers]
        # At least 8 candidates are known to have potency/selectivity gaps
        result("TEST-07 Evidence gaps detected (≥8 candidates)", len(incomplete) >= 8,
               f"incomplete count: {len(incomplete)}")
    except FileNotFoundError:
        result("TEST-07 Incomplete evidence detection", False, "CSV file missing")


# ---------------------------------------------------------------------------
# TEST-08  Missing score input is flagged (not silently zero'd)
# ---------------------------------------------------------------------------
def test_08_missing_score_input():
    # Simulate a record with no score.score_inputs — expect INCOMPLETE status
    sys.path.insert(0, BASE_DIR)
    try:
        import calculate_scores_v2 as sv2
        record_no_score = {"candidate_id": "X-001", "compound": {"name": "Test"}}
        scored = sv2.calculate_score(record_no_score)
        result("TEST-08 Missing score input flagged as INCOMPLETE",
               scored["score_status"] == "INCOMPLETE",
               f"got: {scored['score_status']}")
    except Exception as exc:
        result("TEST-08 Missing score input flagged as INCOMPLETE", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-09  Invalid / non-existent candidate ID handled gracefully
# ---------------------------------------------------------------------------
def test_09_invalid_candidate_id():
    try:
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        ids = {r["candidate_id"] for r in rows}
        result("TEST-09 C-999 not in dataset", "C-999" not in ids)
    except FileNotFoundError:
        result("TEST-09 Invalid candidate ID", False, "CSV file missing")


# ---------------------------------------------------------------------------
# TEST-10  Empty dataset handled gracefully by scoring engine
# ---------------------------------------------------------------------------
def test_10_empty_dataset():
    sys.path.insert(0, BASE_DIR)
    try:
        import calculate_scores_v2 as sv2
        results = sv2.create_comparison_results([])
        result("TEST-10 Empty dataset returns empty results list",
               isinstance(results, list) and len(results) == 0,
               f"got: {results}")
    except Exception as exc:
        result("TEST-10 Empty dataset handled gracefully", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-11  Comparison reproducibility — same input produces same ranking
# ---------------------------------------------------------------------------
def test_11_comparison_reproducibility():
    sys.path.insert(0, BASE_DIR)
    try:
        import calculate_scores_v2 as sv2
        # Build two identical synthetic records with full scores
        def make_record(cid, name):
            return {
                "candidate_id": cid,
                "compound": {"name": name},
                "score": {"score_inputs": {f: 3 for f in SCORE_FIELDS}}
            }
        records = [make_record("C-002", "B"), make_record("C-001", "A")]
        run1 = sv2.create_comparison_results(records)
        run2 = sv2.create_comparison_results(records)
        result("TEST-11 Comparison reproducibility",
               [r["candidate_id"] for r in run1] == [r["candidate_id"] for r in run2])
    except Exception as exc:
        result("TEST-11 Comparison reproducibility", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-12  Deterministic tie-breaking — C-001 ranks before C-002 on equal score
# ---------------------------------------------------------------------------
def test_12_deterministic_tie_handling():
    sys.path.insert(0, BASE_DIR)
    try:
        import calculate_scores_v2 as sv2
        def make_record(cid, name):
            return {
                "candidate_id": cid,
                "compound": {"name": name},
                "score": {"score_inputs": {f: 4 for f in SCORE_FIELDS}}
            }
        records = [make_record("C-002", "B"), make_record("C-001", "A")]
        results = sv2.create_comparison_results(records)
        result("TEST-12 Deterministic tie-breaking (C-001 before C-002)",
               results[0]["candidate_id"] == "C-001" and results[1]["candidate_id"] == "C-002",
               f"order: {[r['candidate_id'] for r in results]}")
    except Exception as exc:
        result("TEST-12 Deterministic tie-breaking", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-13  v2 scoring produces 10 COMPLETE candidates with full rankings
# ---------------------------------------------------------------------------
def test_13_v2_scores_real_records():
    sys.path.insert(0, BASE_DIR)
    try:
        import calculate_scores_v2 as sv2
        records = sv2.load_records()
        results = sv2.create_comparison_results(records)
        complete_count = sum(1 for r in results if r["score"]["score_status"] == "COMPLETE")
        top_cand = results[0]["candidate_id"] if results else ""
        passed = (len(results) == EXPECTED_CANDIDATES and complete_count == EXPECTED_CANDIDATES and top_cand == "C-002")
        result("TEST-13 v2 scoring produces 10 COMPLETE ranked candidates", passed,
               f"complete: {complete_count}, top: {top_cand}")
    except Exception as exc:
        result("TEST-13 v2 scoring produces 10 COMPLETE ranked candidates", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-14  JSON Schema validation for candidate records with provenance
# ---------------------------------------------------------------------------
def test_14_schema_candidate_records():
    schema_path = os.path.join(BASE_DIR, "schema", "candidate_record.schema.json")
    try:
        import jsonschema
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        with open(JSON_PROVENANCE, "r", encoding="utf-8") as f:
            records = json.load(f)
        for r in records:
            jsonschema.validate(instance=r, schema=schema)
        result("TEST-14 JSON Schema validates candidate records", True)
    except Exception as exc:
        result("TEST-14 JSON Schema validates candidate records", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-15  JSON Schema validation for comparison results
# ---------------------------------------------------------------------------
def test_15_schema_comparison_results():
    schema_path = os.path.join(BASE_DIR, "schema", "comparison_results.schema.json")
    results_path = os.path.join(BASE_DIR, "candidate_comparison_results_v2.json")
    try:
        import jsonschema
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        with open(results_path, "r", encoding="utf-8") as f:
            comp_data = json.load(f)
        jsonschema.validate(instance=comp_data, schema=schema)
        result("TEST-15 JSON Schema validates comparison results v2", True)
    except Exception as exc:
        result("TEST-15 JSON Schema validates comparison results v2", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-16  Modularity: all modules expose importable callable functions
# ---------------------------------------------------------------------------
def test_16_module_modularity():
    sys.path.insert(0, BASE_DIR)
    try:
        import calculate_completeness as c_comp
        import calculate_scores as c_scores
        import generate_comparison as c_gen
        import drug_discovery_pipeline as c_pipe
        import pipeline_api as c_api
        import external_api_client as c_ext

        checks = [
            callable(getattr(c_comp, "calculate_candidate_completeness", None)),
            callable(getattr(c_scores, "calculate_candidate_scores", None)),
            callable(getattr(c_gen, "generate_comparison_data", None)),
            callable(getattr(c_pipe, "search_by_name", None)),
            callable(getattr(c_api, "run_full_pipeline", None)),
            callable(getattr(c_ext, "fetch_pubchem_compound", None))
        ]
        result("TEST-16 All modules expose callable importable functions", all(checks))
    except Exception as exc:
        result("TEST-16 All modules expose callable importable functions", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-17  Pipeline API search and filtering return expected candidates
# ---------------------------------------------------------------------------
def test_17_pipeline_api_functions():
    sys.path.insert(0, BASE_DIR)
    try:
        import pipeline_api as api
        tb_cands = api.filter_by_area("Tuberculosis")
        app_cands = api.filter_by_stage("Approved")
        rif = api.search_candidates("Rifampicin")
        passed = (len(tb_cands) == 10 and len(app_cands) >= 7 and len(rif) >= 1)
        result("TEST-17 Pipeline API filtering and search functional", passed)
    except Exception as exc:
        result("TEST-17 Pipeline API filtering and search functional", False, str(exc))


# ---------------------------------------------------------------------------
# TEST-18  External API client resolves cached compound properties
# ---------------------------------------------------------------------------
def test_18_external_api_client():
    sys.path.insert(0, BASE_DIR)
    try:
        import external_api_client as ext
        rif = ext.fetch_pubchem_compound("Rifampicin")
        inh = ext.fetch_chembl_compound("CHEMBL64")
        passed = (rif.get("cid") == 135398735 and inh.get("pref_name") == "ISONIAZID")
        result("TEST-18 External API client queries cached data", passed)
    except Exception as exc:
        result("TEST-18 External API client queries cached data", False, str(exc))


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print()
    print("TB Drug Discovery Pipeline — Automated Test Suite")
    print("=" * 60)
    print()

    test_01_csv_loads()
    test_02_csv_schema()
    test_03_candidate_ids()
    test_04_no_duplicate_ids()
    test_05_synonym_search()
    test_06_unknown_search()
    test_07_incomplete_evidence()
    test_08_missing_score_input()
    test_09_invalid_candidate_id()
    test_10_empty_dataset()
    test_11_comparison_reproducibility()
    test_12_deterministic_tie_handling()
    test_13_v2_scores_real_records()
    test_14_schema_candidate_records()
    test_15_schema_comparison_results()
    test_16_module_modularity()
    test_17_pipeline_api_functions()
    test_18_external_api_client()

    print()
    print("=" * 60)
    total = len(PASSED) + len(FAILED)
    print(f"Results: {len(PASSED)}/{total} tests passed")
    if FAILED:
        print("Failed tests:")
        for name in FAILED:
            print(f"  - {name}")
    else:
        print("All tests passed.")
    print()

    sys.exit(0 if not FAILED else 1)


if __name__ == "__main__":
    main()
