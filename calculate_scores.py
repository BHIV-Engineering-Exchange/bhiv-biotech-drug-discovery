import csv
import os

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "candidate_compounds.csv")

CRITERIA = [
    "Target relevance",
    "Mechanism evidence",
    "Potency evidence",
    "Selectivity evidence",
    "ADME evidence",
    "Safety evidence",
    "Research/development evidence",
    "Evidence completeness"
]

# Scores are based on the strength of documented evidence.
# This is NOT a clinical recommendation.
SCORES = {
    "C-001": [5, 5, 1, 1, 5, 4, 5, 4],
    "C-002": [5, 5, 4, 2, 5, 3, 5, 5],
    "C-003": [5, 4, 1, 1, 5, 3, 5, 4],
    "C-004": [5, 5, 1, 1, 5, 3, 5, 4],
    "C-005": [5, 5, 3, 2, 5, 3, 5, 4],
    "C-006": [5, 4, 2, 2, 4, 3, 5, 4],
    "C-007": [5, 4, 2, 2, 4, 3, 5, 4],
    "C-008": [4, 5, 2, 2, 5, 3, 5, 4],
    "C-009": [4, 3, 2, 2, 3, 2, 5, 4],
    "C-010": [4, 4, 2, 2, 3, 2, 3, 4]
}


def calculate_candidate_scores(candidate_id):
    """Retrieve scoring breakdown and total for a specific candidate ID."""
    scores = SCORES.get(candidate_id)
    if scores is None:
        return None

    breakdown = dict(zip(CRITERIA, scores))
    return {
        "candidate_id": candidate_id,
        "criteria_scores": breakdown,
        "scores_list": scores,
        "total_score": sum(scores),
        "max_score": len(CRITERIA) * 5
    }


def calculate_all_scores(csv_file=None):
    """Score all candidates present in the candidate CSV."""
    if csv_file is None:
        csv_file = CSV_FILE

    with open(csv_file, newline="", encoding="utf-8-sig") as file:
        candidates = list(csv.DictReader(file))

    results = []
    for candidate in candidates:
        cid = candidate["candidate_id"]
        scored = calculate_candidate_scores(cid)
        if scored:
            scored["compound_name"] = candidate.get("compound_name", "")
            results.append(scored)

    return results


def main():
    """Print score breakdown for all candidates."""
    results = calculate_all_scores()

    print("\nTB Candidate Evidence Scoring")
    print("=" * 70)

    for item in results:
        print(f"\n{item['candidate_id']} - {item['compound_name']}")
        print("-" * 50)
        for criterion, score in item["criteria_scores"].items():
            print(f"{criterion}: {score}/5")
        print(f"TOTAL SCORE: {item['total_score']}/{item['max_score']}")


if __name__ == "__main__":
    main()
