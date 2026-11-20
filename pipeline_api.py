"""
TB Drug Discovery Pipeline — Unified Python API
Provides programmatic access to all pipeline functions:
loading, search, filtering, completeness calculation, scoring, comparison,
provenance generation, and schema validation.
Addresses INT-02 / GAP-12.
"""

import os
from typing import Dict, List, Optional, Any

import calculate_completeness as comp
import calculate_scores as score_v1
import calculate_scores_v2 as score_v2
import candidate_provenance as prov
import drug_discovery_pipeline as pipeline
import generate_comparison as comp_gen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "candidate_compounds.csv")
CANONICAL_JSON = os.path.join(BASE_DIR, "candidate_records_v1.json")
PROVENANCE_JSON = os.path.join(BASE_DIR, "candidate_records_with_provenance.json")
COMPARISON_JSON = os.path.join(BASE_DIR, "candidate_comparison_results_v2.json")


def load_candidates(csv_path: Optional[str] = None) -> List[Dict[str, str]]:
    """Load candidate compound records from CSV."""
    return pipeline.load_candidates(csv_path or CSV_FILE)


def search_candidates(term: str, candidates: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
    """Search candidates by compound name or synonym."""
    if candidates is None:
        candidates = load_candidates()
    return pipeline.search_by_name(candidates, term)


def filter_by_area(area: str, candidates: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
    """Filter candidates by therapeutic area."""
    if candidates is None:
        candidates = load_candidates()
    return pipeline.filter_by_therapeutic_area(candidates, area)


def filter_by_stage(stage: str, candidates: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
    """Filter candidates by evidence stage."""
    if candidates is None:
        candidates = load_candidates()
    return pipeline.filter_by_evidence_stage(candidates, stage)


def assess_completeness(csv_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Assess evidence completeness across all candidate records."""
    return comp.calculate_all_completeness(csv_path or CSV_FILE)


def score_candidates_v1(csv_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Execute v1 criteria scoring across candidates."""
    return score_v1.calculate_all_scores(csv_path or CSV_FILE)


def generate_comparison_v1(csv_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Generate ranked candidate comparison using v1 scoring logic."""
    return comp_gen.generate_comparison_data(csv_path or CSV_FILE)


def build_provenance_records(input_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Process canonical records and build provenance-enriched candidate records."""
    records = prov.load_records()
    return prov.build_provenance_records(records)


def score_candidates_v2(records: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Score candidate records using the 8-dimension v2 scoring engine."""
    if records is None:
        records = score_v2.load_records()
    return score_v2.create_comparison_results(records)


def run_full_pipeline() -> Dict[str, Any]:
    """Run full pipeline lifecycle and return comprehensive execution summary."""
    candidates = load_candidates()
    completeness = assess_completeness()
    provenance_records = build_provenance_records()
    v2_results = score_candidates_v2(provenance_records)

    return {
        "candidate_count": len(candidates),
        "completeness_summary": [
            f"{c['candidate_id']}: {c['completeness_percentage']:.0f}%" for c in completeness
        ],
        "top_ranked_v2": [
            {
                "rank": r["rank"],
                "candidate_id": r["candidate_id"],
                "compound_name": r["compound_name"],
                "total_score": r["score"]["total"]
            }
            for r in v2_results if r.get("rank") is not None
        ][:3]
    }


if __name__ == "__main__":
    summary = run_full_pipeline()
    print("TB Pipeline API Summary:")
    print(f"Total candidates: {summary['candidate_count']}")
    print("Top 3 ranked candidates (v2):")
    for r in summary["top_ranked_v2"]:
        print(f"  Rank {r['rank']}: {r['candidate_id']} {r['compound_name']} ({r['total_score']}/40)")
