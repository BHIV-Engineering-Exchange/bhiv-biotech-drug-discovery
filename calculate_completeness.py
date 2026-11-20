import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "candidate_compounds.csv")

EVIDENCE_FIELDS = [
    "source_database",
    "molecular_identifier",
    "target",
    "mechanism_of_action",
    "evidence_stage",
    "potency",
    "selectivity",
    "adme",
    "safety_toxicity",
    "supporting_publications"
]


def is_complete(value):
    """Check if an evidence field contains substantive value."""
    if not value:
        return False

    value = value.strip()

    if value.upper() in [
        "UNKNOWN",
        "UNKNOWN / NOT FOUND",
        "NOT FOUND",
        "N/A"
    ]:
        return False

    return True


def calculate_candidate_completeness(candidate, fields=None):
    """Calculate completeness metrics for a single candidate."""
    if fields is None:
        fields = EVIDENCE_FIELDS

    completed = sum(1 for field in fields if is_complete(candidate.get(field, "")))
    total = len(fields)
    percentage = (completed / total) * 100 if total > 0 else 0.0

    return {
        "candidate_id": candidate.get("candidate_id", ""),
        "compound_name": candidate.get("compound_name", ""),
        "completed_fields": completed,
        "total_fields": total,
        "completeness_percentage": percentage
    }


def calculate_all_completeness(csv_file=None):
    """Calculate completeness for all candidates in the CSV file."""
    if csv_file is None:
        csv_file = CSV_FILE

    with open(csv_file, newline="", encoding="utf-8-sig") as file:
        candidates = list(csv.DictReader(file))

    return [calculate_candidate_completeness(c) for c in candidates]


def main():
    """Print completeness summary for TB candidates."""
    results = calculate_all_completeness()

    print("\nTB Candidate Evidence Completeness")
    print("=" * 50)

    for item in results:
        print(
            f"{item['candidate_id']} - "
            f"{item['compound_name']}: "
            f"{item['completed_fields']}/{item['total_fields']} fields = "
            f"{item['completeness_percentage']:.0f}%"
        )


if __name__ == "__main__":
    main()
