# PHASE 8 — TEST STATUS REPORT

## 1. Project
**Project:** BHIV Biotech — TB Drug-Discovery Candidate Intelligence

**Phase:** Phase 8 — Version 2 Scoring and Integration Verification

## 2. Execution Summary

The Version 2 scoring pipeline was updated to support the existing candidate record structure and reuse the documented eight-dimensional scoring inputs.

The integration maps existing candidate IDs and compound names into the expected Version 2 structure.

## 3. Test Results

| Test | Result |
|---|---|
| Score normalization | PASS |
| Complete score calculation | PASS |
| Missing score handling | PASS |
| Deterministic scoring | PASS |
| Deterministic tie handling | PASS |

**Unit tests:** 5 passed, 0 failed.

## 4. Integration Results

- Total candidate records: 10
- Complete scores: 10
- Incomplete scores: 0
- Rankings generated: 10
- Maximum score: 40
- Method version: 1.0.0

## 5. Final Candidate Ranking

| Rank | Candidate ID | Compound | Score |
|---|---|---|---|
| 1 | C-002 | Isoniazid | 34/40 |
| 2 | C-005 | Bedaquiline | 32/40 |
| 3 | C-001 | Rifampicin | 30/40 |
| 4 | C-008 | Linezolid | 30/40 |
| 5 | C-004 | Ethambutol | 29/40 |
| 6 | C-006 | Delamanid | 29/40 |
| 7 | C-007 | Pretomanid | 29/40 |
| 8 | C-003 | Pyrazinamide | 28/40 |
| 9 | C-009 | Clofazimine | 25/40 |
| 10 | C-010 | Sutezolid | 24/40 |

## 6. Output Verification

The generated `candidate_comparison_results_v2.json` was independently inspected.

Verified:
- 10 records present
- 10 complete scores
- 0 incomplete scores
- All rankings assigned
- First-ranked candidate: Isoniazid
- First-ranked score: 34/40

## 7. Files

- `calculate_scores_v2.py`
- `candidate_records_with_provenance.json`
- `candidate_comparison_results_v2.json`
- `calculate_scores_v2_backup.py`
- `candidate_comparison_results_v2_backup.json`

The original evidence records were preserved.

## 8. Limitations

The scoring values are existing manually assigned evidence-documentation scores. Successful software testing does not independently validate their scientific accuracy or establish clinical recommendations.

The historical claim of 12/12 tests was not independently reproduced. The current independently executed test result is 5/5 unit tests plus successful integration verification.

## 9. Conclusion

The Version 2 scoring integration was successfully executed and verified against all 10 candidate records.

All five built-in tests passed, all 10 candidate scores were complete, and all 10 rankings were generated and saved.

**Status: Version 2 integration verification completed.**