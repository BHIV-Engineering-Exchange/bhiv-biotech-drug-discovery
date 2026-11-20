import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "candidate_compounds.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "candidate_comparison_results.csv")

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


def generate_comparison_data(csv_file=None):
    """Generate ranked comparison list from CSV candidate data and SCORES."""
    if csv_file is None:
        csv_file = CSV_FILE

    with open(csv_file, newline="", encoding="utf-8-sig") as file:
        candidates = list(csv.DictReader(file))

    results = []

    for candidate in candidates:
        candidate_id = candidate["candidate_id"]

        if candidate_id not in SCORES:
            continue

        scores = SCORES[candidate_id]

        row = {
            "candidate_id": candidate_id,
            "compound_name": candidate["compound_name"],
        }

        for criterion, score in zip(CRITERIA, scores):
            row[criterion] = score

        row["total_score"] = sum(scores)
        results.append(row)

    # Sort by highest score first, using Candidate ID as tie-breaker
    results.sort(key=lambda x: (-x["total_score"], x["candidate_id"]))

    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    return results


def save_comparison_csv(results, output_file=None):
    """Write comparison results into a CSV file."""
    if output_file is None:
        output_file = OUTPUT_FILE

    fieldnames = [
        "rank",
        "candidate_id",
        "compound_name"
    ] + CRITERIA + ["total_score"]

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    return output_file


def main():
    """Execute candidate comparison and save ranked results."""
    results = generate_comparison_data()
    saved_path = save_comparison_csv(results)

    print("\nFinal TB Candidate Ranking")
    print("=" * 55)

    for row in results:
        print(
            f"{row['rank']}. {row['candidate_id']} - "
            f"{row['compound_name']}: "
            f"{row['total_score']}/40"
        )

    print("\nComparison file created successfully:")
    print(saved_path)


if __name__ == "__main__":
    main()
