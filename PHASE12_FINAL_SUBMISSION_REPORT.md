\# PHASE 12 — FINAL SUBMISSION REPORT



\## 1. Project Details



\*\*Project:\*\* BHIV Biotech — TB Drug-Discovery Candidate Intelligence  

\*\*Task ID:\*\* BIOTECH-T3-SHAMIT-TB-DRUG-DISCOVERY  

\*\*Phase:\*\* Phase 12 — Final Submission Preparation



\## 2. Project Overview



This project demonstrates an educational Python-based workflow for organizing tuberculosis (TB) drug-discovery candidate information, documenting evidence and provenance, identifying evidence gaps, comparing candidates, and validating structured research data.



The project is intended for educational research and evidence organization.



\## 3. Candidate Registry



The project contains 10 candidate compounds:



| Candidate ID | Compound |

|---|---|

| C-001 | Rifampicin |

| C-002 | Isoniazid |

| C-003 | Pyrazinamide |

| C-004 | Ethambutol |

| C-005 | Bedaquiline |

| C-006 | Delamanid |

| C-007 | Pretomanid |

| C-008 | Linezolid |

| C-009 | Clofazimine |

| C-010 | Sutezolid |



\## 4. Project Workflow



The implemented workflow includes:



1\. Candidate record organization.

2\. Canonical candidate schema validation.

3\. Candidate identity resolution.

4\. Evidence source and provenance documentation.

5\. Evidence completeness and gap analysis.

6\. Candidate comparison.

7\. Version 2 scoring and ranking.

8\. Software testing and validation.

9\. Final documentation and handover preparation.



\## 5. Version 2 Scoring Results



The documented V2 scoring configuration uses:



\- 8 scoring dimensions.

\- Each dimension scored from 0 to 5.

\- Maximum score: 40.

\- 10 candidates processed.

\- 10 complete scores.

\- 0 incomplete scores.



\### Recorded ranking



| Rank | Candidate ID | Compound | Score |

|---:|---|---|---:|

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



These are documented research-comparison scores, not clinical efficacy or safety measurements.



\## 6. Testing and Validation



\### Phase 8 — V2 scoring tests



\- Tests passed: 5

\- Tests failed: 0



\### Phase 9 — Final validation



\- Validation checks passed: 7/7

\- Candidate records: 10

\- Scoring results: 10

\- Valid scoring inputs: 80/80

\- Incorrect score totals: 0

\- Missing or duplicate ranks: 0



\### Phase 11 — Repository test discovery



Command: `python -m unittest discover -v`



\- Candidate schema tests: 5 passed.

\- Identity resolution tests: 8 passed.

\- Total: 13 passed.

\- Failed: 0.



The Phase 8 and Phase 11 results are separate test executions and are not presented as one combined test suite.



\## 7. Key Project Files



Important project files include:



\- `README.md`

\- `candidate\_records\_v1.json`

\- `candidate\_records\_with\_provenance.json`

\- `candidate\_comparison\_results\_v2.json`

\- `PHASE8\_TEST\_STATUS.md`

\- `PHASE9\_FINAL\_VALIDATION\_REPORT.md`

\- `PHASE10\_FINAL\_HANDOVER\_REPORT.md`

\- `PHASE11\_REPOSITORY\_TEST\_RESULTS.md`

\- `test\_candidate\_schema.py`

\- `test\_identity\_resolution.py`



\## 8. Limitations



\- Scores are manually assigned research-documentation values.

\- Software tests verify selected implementation behaviors, not scientific correctness.

\- The project does not establish clinical efficacy or human safety.

\- Expert scientific review is required before interpreting research findings.

\- Production BIQOS integration has not been demonstrated.

\- A historical 12/12 test claim was not independently reproduced.

\- Local repository verification does not establish external submission or acceptance.



\## 9. Final Status



The documented project workflow, V2 scoring results, validation reports, repository tests, and handover materials have been prepared.



\*\*Local verification status:\*\* PASS for the checks documented in the project reports.



\*\*External submission status:\*\* Pending confirmation.



\*\*BIQOS production integration status:\*\* Not demonstrated.



\*\*Final conclusion:\*\* The project is prepared as an educational TB drug-discovery candidate intelligence prototype, with documented software validation and clearly stated limitations.

