# DataKollecta validation package

This repository is the computerised-system validation package for the DataKollecta system
(field application, web portal and server, SurveyGen, SurveyTest, DataBackup). It is what you
show an auditor, sponsor or inspector who asks whether the system is validated.

No outside body certifies software of this kind. What is expected is that the organisation
responsible for the system validates it itself, and keeps the documented evidence: this
package.

## The documents

The Word files in [`docs/`](docs/) are the controlled documents. Print or e-sign them.

| ID | Document | Sign when |
|---|---|---|
| DK-VAL-001 | Validation Plan | Now |
| DK-VAL-002 | User Requirements Specification and Risk Assessment | Now |
| DK-VAL-003 | Functional and Design Specification | Now |
| DK-VAL-004 | Test Protocol (IQ / OQ / PQ / automated) | **Before** the manual tests are run |
| DK-VAL-005 | Validation Summary Report (results, traceability, deviations, release statement) | After the manual tests are run and recorded |
| DK-SOP-001 | System Management SOP (change control, access, audit-trail review, backup and restore, incidents, security, periodic review, training, retention), with forms | Now |
| DK-TPL-001 | Study Build Validation Record (template) | One copy per study build and per amendment |

Show an auditor **DK-VAL-005** first: it summarises everything and indexes the rest.

## What is still to do

1. Fill in the names on the approval pages, review, and sign DK-VAL-001 to DK-VAL-004 and
   DK-SOP-001.
2. Set up the test project and accounts (DK-VAL-004 section 4). An independent tester (not
   the developer) then executes the IQ, OQ and PQ test cases on real devices and the
   production portal, recording results and evidence.
3. Record the hosting facts (Supabase region, plan, backups and point-in-time recovery;
   provider attestations) at IQ-07, and update DK-VAL-002 section 6.
4. Complete sections 5 and 10 of DK-VAL-005, and sign it.
5. For every study, complete DK-TPL-001 before deploying its survey.
6. Work through the planned corrections in the residual risk register (DK-VAL-002 section 5)
   under change control.

## Layout

```
src/            Text sources of the documents (edit these, never the .docx directly)
docs/           Built Word documents
tools/          build_docs.py (builds docs/), traceability.py (checks and builds the matrix)
test-assets/    The validation test survey used by the Test Protocol, and the scripts that make it
evidence/       Test evidence: automated logs (with SHA256SUMS), and later the manual test evidence
```

## Rebuilding the documents

Requires pandoc (2.19 or later), Python 3 with `python-docx`, `openpyxl` and `pyyaml`.

```bash
python3 tools/traceability.py     # check traceability; exits non-zero on any problem
python3 tools/build_docs.py       # rebuild every document in docs/
python3 tools/build_docs.py DK-VAL-004   # rebuild one
```

Changing a document is itself a change under DK-SOP-001 section 4. Raise the `version` in the
document's front matter and add a line to its `history`.

## Re-running the automated tests

The commands and acceptance criteria are in DK-VAL-004 section 8. Put each run in a new
folder under `evidence/`, named by date and versions, with the full log of every suite and a
`SHA256SUMS` file (`sha256sum *.log > SHA256SUMS`). Then record the counts in DK-VAL-005
section 4.
