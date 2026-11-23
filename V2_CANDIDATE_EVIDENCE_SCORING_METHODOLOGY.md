# V2 Candidate Evidence Scoring Methodology

## 1. Purpose

The scoring framework is intended to support structured comparison of tuberculosis drug-discovery candidates based on documented evidence.

It is a research evidence-intelligence tool and is not a clinical recommendation, treatment guideline, or independent assessment of drug efficacy.

## 2. Scoring Dimensions

Each candidate is evaluated across eight dimensions:

1. Target relevance
2. Mechanism evidence
3. Potency evidence
4. Selectivity evidence
5. ADME evidence
6. Safety evidence
7. Research and development evidence
8. Evidence completeness

Each dimension has a maximum of 5 points.

Maximum possible total: 40 points.

## 3. Existing Score Origin

The initial score assignments were manually defined in the original `calculate_scores.py` file.

The V2 implementation inherited these values through a hardcoded `SCORES` dictionary.

These values are classified as legacy manually assigned evidence-documentation scores.

They have not been independently reproduced from a complete, dimension-level evidence mapping.

## 4. Arithmetic Verification of Legacy Scores

The original `calculate_scores.py` file contains eight manually assigned dimension-level scores for each of the 10 TB candidates.

The sum of the eight dimension-level scores was checked against the historical candidate totals.

All 10 candidate totals matched the original score lists.

This confirms arithmetic reproducibility of the historical totals from the original manually assigned scores.

It does not independently reproduce or validate the scientific rationale for each individual dimension score.

## 5. Scoring Scale

Each scoring dimension has a maximum value of 5 points.

The original dimension-level values are manually assigned legacy evidence-documentation scores.

The current methodology does not define a complete, independently verified interpretation for every score from 0 to 5.

Therefore, the existing scores are preserved as legacy values. No new score definitions or candidate scores are inferred during this documentation update.

A formal scoring rubric should be established before assigning or revising scores based on evidence.

## 6. Evidence Requirements

Each score should be supported by:

- Candidate identifier
- Scoring dimension
- Score value
- Evidence source
- Source identifier or publication reference
- Brief scoring rationale
- Verification status

Where evidence is unavailable or insufficient, the scoring input must remain explicitly incomplete.

Missing evidence must not be automatically converted into a score of zero.

## 7. Reproducibility Limitation

The historical totals can be reproduced by summing the original manually assigned dimension-level scores.

However, the existing hardcoded score assignments do not independently demonstrate how each score was derived from the candidate evidence records.

The scoring input contract and evidence mapping must be completed before the results can be described as independently evidence-reproducible.

## 8. Intended V2 Behavior

The corrected V2 implementation is intended to:

- Read scoring inputs from a versioned input file
- Validate candidate identifiers and scoring dimensions
- Preserve missing values
- Identify incomplete candidates
- Calculate totals only for candidates meeting the documented completeness requirements
- Generate comparison results from the committed input
- Preserve source provenance and scoring rationale

## 9. Limitations

The existing rankings are historical outputs from manually assigned scores.

They should not be interpreted as validated scientific rankings, clinical recommendations, or proof of therapeutic superiority.

## 10. Legacy Score Mapping Validation

The file `legacy_score_evidence_mapping_v2.csv` contains 80 mapping rows, representing 8 scoring dimensions for each of the 10 TB candidates.

A structural and arithmetic validation was completed.

Validation results:

- Total data rows: 80
- Rows per candidate: 8
- Unique scoring dimensions per candidate: PASS
- Scores within the permitted 0–5 range: PASS
- Verification status consistency (`NOT_VERIFIED`): PASS
- Historical candidate totals matched: PASS
- Overall CSV validation: PASS

The validation confirms the structure of the mapping file and the arithmetic consistency of the historical scores.

**Evidence verification remains incomplete.** Source documents, publication identifiers, and evidence-based scoring rationales have not yet been independently mapped and verified for each scoring dimension.

The legacy scores must not be represented as scientifically validated rankings or clinical recommendations.