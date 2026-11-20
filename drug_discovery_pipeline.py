import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "candidate_compounds.csv")


def load_candidates(csv_file=None):
    """Load candidate compounds from CSV."""
    if csv_file is None:
        csv_file = CSV_FILE

    try:
        with open(csv_file, newline="", encoding="utf-8-sig") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"\nERROR: {csv_file} not found.")
        return []


def search_by_name(candidates, search_term):
    """Search candidates by compound name or synonym."""
    search_term = search_term.lower().strip()
    results = []

    for candidate in candidates:
        name = candidate.get("compound_name", "").lower()
        synonyms = candidate.get("synonyms", "").lower()

        if search_term in name or search_term in synonyms:
            results.append(candidate)

    return results


def filter_by_therapeutic_area(candidates, area):
    """Filter candidates by therapeutic area."""
    area = area.lower().strip()
    return [
        candidate
        for candidate in candidates
        if area in candidate.get("therapeutic_area", "").lower()
    ]


def filter_by_evidence_stage(candidates, stage):
    """Filter candidates by evidence stage."""
    stage = stage.lower().strip()
    return [
        candidate
        for candidate in candidates
        if stage in candidate.get("evidence_stage", "").lower()
    ]


def display_candidates(candidates):
    """Display candidate IDs and names."""
    if not candidates:
        print("\nNo candidates found.")
        return

    print("\nCandidates")
    print("=" * 50)

    for candidate in candidates:
        print(
            f"{candidate['candidate_id']} - "
            f"{candidate['compound_name']}"
        )


def display_candidate_details(candidate):
    """Display detailed research information for one candidate."""
    print("\nCandidate Details")
    print("=" * 60)
    print(f"Candidate ID: {candidate.get('candidate_id', '')}")
    print(f"Compound Name: {candidate.get('compound_name', '')}")
    print(f"Synonyms: {candidate.get('synonyms', '')}")
    print(f"Source Database: {candidate.get('source_database', '')}")
    print(f"Molecular Identifier: {candidate.get('molecular_identifier', '')}")
    print(f"Target: {candidate.get('target', '')}")
    print(f"Mechanism of Action: {candidate.get('mechanism_of_action', '')}")
    print(f"Therapeutic Area: {candidate.get('therapeutic_area', '')}")
    print(f"Evidence Stage: {candidate.get('evidence_stage', '')}")
    print(f"Potency: {candidate.get('potency', '')}")
    print(f"Selectivity: {candidate.get('selectivity', '')}")
    print(f"ADME: {candidate.get('adme', '')}")
    print(f"Safety/Toxicity: {candidate.get('safety_toxicity', '')}")
    print(f"Supporting Publications: {candidate.get('supporting_publications', '')}")
    print(f"Known Limitations: {candidate.get('known_limitations', '')}")
    print(f"Evidence Confidence: {candidate.get('evidence_confidence', '')}")
    print(f"Missing Information: {candidate.get('missing_information', '')}")


def main():
    candidates = load_candidates()

    if not candidates:
        return

    print("\nTB Drug Discovery Research Pipeline")
    print("=" * 50)
    print(f"Loaded candidates: {len(candidates)}")

    while True:
        print("\nMenu")
        print("1. Search by compound name")
        print("2. Filter by therapeutic area")
        print("3. Filter by evidence stage")
        print("4. Show all candidates")
        print("5. View candidate details")
        print("6. View all candidate details")
        print("7. Exit")

        try:
            choice = input("\nEnter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting pipeline.")
            break

        if choice == "1":
            try:
                term = input("Enter compound name or synonym: ")
            except (EOFError, KeyboardInterrupt):
                break
            results = search_by_name(candidates, term)
            display_candidates(results)

        elif choice == "2":
            try:
                area = input("Enter therapeutic area: ")
            except (EOFError, KeyboardInterrupt):
                break
            results = filter_by_therapeutic_area(candidates, area)
            display_candidates(results)

        elif choice == "3":
            try:
                stage = input("Enter evidence stage: ")
            except (EOFError, KeyboardInterrupt):
                break
            results = filter_by_evidence_stage(candidates, stage)
            display_candidates(results)

        elif choice == "4":
            display_candidates(candidates)

        elif choice == "5":
            try:
                candidate_id = input(
                    "Enter candidate ID (example: C-001): "
                ).strip().upper()
            except (EOFError, KeyboardInterrupt):
                break

            found = False
            for candidate in candidates:
                if candidate["candidate_id"].strip().upper() == candidate_id:
                    display_candidate_details(candidate)
                    found = True
                    break

            if not found:
                print("\nCandidate ID not found.")

        elif choice == "6":
            print("\nAll Candidate Details")
            print("=" * 60)
            for candidate in candidates:
                display_candidate_details(candidate)

        elif choice == "7":
            print("\nExiting pipeline.")
            break

        else:
            print("\nInvalid choice. Please select 1-7.")


if __name__ == "__main__":
    main()
