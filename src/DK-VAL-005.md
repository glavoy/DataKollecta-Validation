---
doc_id: DK-VAL-005
title: Validation Summary Report
version: "1.0"
orientation: landscape
status: "Interim: automated testing complete; manual testing (IQ/OQ/PQ) to be executed and recorded, then this report is finalised and signed."
approvers:
  - [Author, System Owner / Lead Developer]
  - [Reviewer, Quality Assurance (independent of development)]
  - [Approver, Head of Data Management]
---

# 1. Purpose and how to read this report

This report summarises the validation of the DataKollecta system carried out under the
Validation Plan (DK-VAL-001). It records:

- what was tested, on which versions, by whom, and with what result;
- how every requirement is traced to its verification;
- the deviations found and how they were resolved;
- the known limitations accepted for use;
- the conclusion on whether the system is fit for its intended use.

**For an auditor, this is the first document to read.** Section 9 indexes the whole
validation package and where its evidence is kept.

**Status of this version.** The automated regression testing (section 4) has been
executed on the baseline versions, and its results are final. The manual installation,
operational and performance qualification (IQ, OQ, PQ) in DK-VAL-004 is to be executed by an
independent tester after the protocol is approved. Section 5 and the *Manual result* column
of the traceability matrix are then completed, and the release statement (section 10) is
signed. Until then, this report is an interim report and the release statement is not in
force.

# 2. System and versions validated

| Component | Version | Source identifier | Repository |
|:--------------------|:-------------------|:------------------------------------------|:-------------------|
| Field application (DataKollecta product) | 1.4.1+19 | Tag v1.4.1+19, commit 8dc4302ef9b81dd3de1d66cfe87b3422cfa75ec4 | DataKollecta |
| Web portal, server functions, database schema | 1.2.0, migration head 20261008150000 | Tag web-v1.2.0, commit ea1f2990cdd88f27a1cfae2f017d22ad7e9370ae | DataKollecta-Web |
| SurveyGen | — | Commit 005a7f97e2a98fd032c91866354fe15d6e7e3270 | DataKollecta-SurveyGen |
| SurveyTest | — | Commit d38cb50ea3a85e3d39cfaafef5c6448102770917 | DataKollecta-SurveyTest |
| DataBackup | — | Commit dafe783b53ab478b33aba81ff9fa97f634082f82 | DataKollecta-DataBackup |

**Validation type.** Retrospective for these baseline versions (DK-VAL-001, section 4.3).
The system was in production use before this validation.

**Audit-trail baseline.** Server-side audit events exist from 5 October 2026 (migration
20261005090000) onwards (DK-VAL-002, R-11). Studies with data collected before that date
should note it in their data management documentation.

# 3. Summary of validation activities

| Activity | Document | Status |
|:-----------------------------------------|:--------------|:--------------------------------------------------|
| Validation planning | DK-VAL-001 | Written; for approval |
| User requirements and risk assessment (62 requirements, 20 residual risks) | DK-VAL-002 | Written; for approval |
| Functional and design specification | DK-VAL-003 | Written; for approval |
| Test protocol (8 IQ, 39 OQ, 1 PQ, 10 AT) | DK-VAL-004 | Written; to be approved **before** manual execution |
| Automated regression testing (AT-01 to AT-10) | Section 4 | **Executed 8 October 2026: all suites pass**; 6 deviations, all minor (section 7) |
| Manual IQ / OQ / PQ | Section 5 | To be executed |
| Traceability | Section 6 | Complete. Checked by `tools/traceability.py`: every requirement is verified by at least one test or procedure, and every reference resolves. |
| Procedures for the validated state | DK-SOP-001 | Written; for approval |
| Study configuration validation | DK-TPL-001 | Template written; completed per study |

# 4. Automated test results

## 4.1 Execution

| Item | Detail |
|:-----------------------|:-------------------------------------------------------------------------|
| Date | 8 October 2026 |
| Executed by | Executed under the System Owner's direction by the development team's AI coding assistant (Claude Code), in an isolated cloud test environment. Logs are reviewed by QA. |
| Environment | Linux x86-64 container. Flutter 3.47.6 (Dart 3.13.5); Python 3.13.16; Node.js 22.22.0; PostgreSQL client 16.15; Supabase CLI 2.120.0 with a local stack built from the repository's migrations (PostgreSQL 17); Deno 2.9.6 |
| Code tested | The exact commits in section 2, from clean checkouts; no source file was modified for testing |
| Evidence | `evidence/2026-10-08-baseline/` in the validation repository: one full log per suite, with checksums in `SHA256SUMS`; the test-environment router and import map used for AT-08; the installation logs |
| Timing | This run took place before DK-VAL-004 was signed, as part of the retrospective baseline. The commands and acceptance criteria are those now set out in DK-VAL-004, section 8. QA may require it to be repeated after approval; any repeat is recorded in a later version of this report. |

## 4.2 Results

| ID | Suite | Tests run | Passed | Failed | Skipped | Result | Log file (SHA-256, first 16 characters) |
|:-----|:-----------------------------|:------|:------|:------|:------|:-----------|:-----------------------------------------------|
| AT-01 | Field application static analysis | n/a | — | 0 errors | — | Pass with deviation DEV-03 (1 warning) | AT-01_app_flutter_analyze.log (472945d96e95c8cc) |
| AT-02 | Field application tests (default build) | 592 | 589 | 0 | 3 | Pass | AT-02_app_flutter_test.log (2c82d196d4397783) |
| AT-03 | Field application tests (DataKollecta build) | 592 | 591 | 0 | 1 | Pass | AT-03_app_flutter_test_datakollecta.log (7d30c63318e58dcd) |
| AT-04 | SurveyGen tests | 371 | 370 | 0 | 1 | Pass | AT-04_surveygen_unittest.log (4ae3f386718a5cf7) |
| AT-05 | SurveyTest analysis and tests | 69 | 69 | 0 | 0 | Pass (no analysis issues) | AT-05a_surveytest_flutter_analyze.log (d31aa81bb57326af); AT-05b_surveytest_flutter_test.log (f2cac4c3b56c566a) |
| AT-06 | Portal lint, type check, build | n/a | — | 0 errors | — | Pass (5 lint warnings, all "fast refresh" developer-tooling hints with no effect on behaviour) | AT-06a_portal_lint.log (15b199e852ba7c4a); AT-06b_portal_typecheck.log (19eaf43821a7660e); AT-06c_portal_build.log (3fc01e71767f52ce) |
| AT-07 | Portal unit tests | 516 | 516 | 0 | 0 | Pass (after DEV-02) | AT-07_portal_vitest.log (230204f32fca7062) |
| AT-08 | Server function integration tests | 80 | 80 | 0 | 0 | Pass (test environment per DEV-04) | AT-08_server_functions_deno_test.log (48a0f6bd00ca164f) |
| AT-09 | Database control scripts | 2 scripts | 2 | 0 | 0 | Pass | AT-09a_sql_validation_controls.log (c33431a81e82fd8c); AT-09b_sql_audit_trail_hardening.log (28f12d8965e90155) |
| AT-10 | DataBackup tests | 8 | 8 | 0 | 0 | Pass | AT-10_databackup_unittest.log (f89b96ee3000c33e) |
| **Total** | | **2,228 test cases + 2 scripts** | **2,223 + 2** | **0** | **5** | **Pass** | |

AT-02 and AT-03 run the same test files under the two product builds, so most tests are
counted in both. The total counts each execution.

**Skipped tests explained.**

- **AT-02 (3) and AT-03 (1).** These tests apply to one product only and skip themselves in
  the other build. For example, "GiSTX allows two surveyIds on one database" runs only for
  GiSTX, and "a side-loaded zip with no known project is allowed through" is skipped in the
  DataKollecta build. This is by design.
- **AT-04 (1).** `test_test_kit.VariantBuildTests` needs a real study dictionary, which is
  deliberately not kept in the repository. Study dictionaries are verified per study under
  DK-TPL-001.

**Server-side tests by area (AT-08):**

| Area | Tests |
|:-----------------------------------------------|:------|
| Device sign-in | 16 |
| Synchronisation | 23 |
| Audit trail | 4 |
| Credential reset | 9 |
| Test and deployed status | 5 |
| Data feed | 7 |
| Purge | 7 |
| Storage policies | 6 |
| Data-lock and audit-retry controls | 3 |

## 4.3 Development checks of the validation test assets

The validation test survey (DK-VAL-004, P-6) was built with SurveyGen at the baseline commit
while this package was prepared. These checks are not a substitute for executing OQ-01,
OQ-02 and OQ-06, but they confirm the test assets are fit for use:

- The clean dictionary built successfully.
- The error dictionary was refused with all five deliberate errors reported, plus one
  consequential error.
- The field application's survey loader, at the baseline commit, loaded the clean package
  and refused the unsafe package with "Unusable SQL identifier "resp-ondent"".

# 5. Manual test results (IQ, OQ, PQ)

*To be completed after execution of DK-VAL-004.*

| Test case | Result (Pass / Fail) | Deviation IDs | Executed by, date | Reviewed by, date |
|:-------------|:------------|:--------------|:---------------------|:---------------------|
| IQ-01 to IQ-08 | | | | |
| OQ-01 to OQ-10 | | | | |
| OQ-11 to OQ-20 | | | | |
| OQ-21 to OQ-30 | | | | |
| OQ-31 to OQ-39 | | | | |
| PQ-01 | | | | |

Executed test cases with failures are listed individually in the deviation log (section 7).

**Environment differences.** Manual tests run in the production system, in the dedicated
test project VALIDATION-TEST (DK-VAL-001, section 7.2). Record here any difference from that
plan:

# 6. Traceability matrix

Each requirement (DK-VAL-002) is mapped below to the section of the Functional and Design
Specification (DK-VAL-003) that implements it, the manual tests and procedures (DK-VAL-004,
DK-SOP-001) that verify it, and the automated suites that cover it. The *Manual result*
column is completed when section 5 is complete. The *Status* column gives the requirement's
status from DK-VAL-002; for any requirement not fully met, it points to the residual risk
register.

This matrix is generated from DK-VAL-002 and DK-VAL-004 by `tools/traceability.py`, which
also checks that every reference resolves. It must not be edited by hand.

{{TRACEABILITY_MATRIX}}

# 7. Deviation log

| ID | Found in | Description | Class | Impact assessment | Resolution | Status |
|:-------|:---------|:--------------------------------------------|:-------|:------------------------------------------|:------------------------------------------|:---------|
| DEV-01 | AT-06/AT-07 set-up | `npm ci` (clean install from the lockfile) failed because the web project's `package-lock.json` is out of step with `package.json`: esbuild 0.28.2 and its platform packages are missing from the lockfile. | Minor | The build cannot be reproduced from the lockfile alone. Production builds are made by the hosting platform from the committed sources. No effect on data. | Tests run after `npm install`, with the lockfile restored afterwards (log kept). Correction: regenerate and commit the lockfile (DK-VAL-002, R-15). | Open: correction planned |
| DEV-02 | AT-07 | On the first run, 1 of 35 test files (`surveyErrors.test.ts`) failed to load because the module it imports requires the Supabase URL and key environment variables. No test assertion failed. | Minor | A test-environment set-up issue; not a defect in the portal, which always runs with these variables set. | Re-run with placeholder values (the tests make no network calls): 516 of 516 passed. First-run log kept. Correction: give the test set-up its own values. | Closed (test environment); improvement planned |
| DEV-03 | AT-01 | `flutter analyze` reported 1 warning, `unawaited_return_in_try_block`, at `lib/services/ftp_service.dart:423`. The rule is new in Flutter 3.47.6, newer than the SDK used in development. | Minor | The file is the FTP transport of the GiSTX product, which the DataKollecta build excludes at compile time. No effect on DataKollecta. | Accepted for this baseline. Correction: add the missing `await` in the next field-application release. | Open: correction planned |
| DEV-04 | AT-08 | The test environment's network policy blocks esm.sh and deno.land, so the server functions could not run in Supabase's own edge runtime. | Minor | The same function code and library versions were run on Deno 2.9.6 on the host, with an import map pointing to the same libraries from npm and jsr (`@supabase/supabase-js@2.115.0`, `@std/assert@0.224.0`). A small router supplied the gateway's `x-forwarded-for` header. The database, authentication and storage were the real local Supabase services. The difference concerns only module loading, not function logic. Production behaviour is confirmed by the manual OQ tests run against production. | First (blocked) run log kept; the router and import map are kept with the evidence. | Closed |
| DEV-05 | AT-02, AT-03, AT-05 | The test environment used Flutter 3.47.6. Running `flutter pub get` with it resolved four SDK-pinned packages (matcher, meta, test_api, vector_math) to newer versions than the committed `pubspec.lock`. Flutter 3.47.6 also updated `analysis_options.yaml` automatically. | Minor | Test-only packages and analysis settings, with no effect on application behaviour. Both files were restored after testing; the analysis ran with the committed settings. | Recorded. The development SDK version is to be recorded in future change requests. | Closed |
| DEV-06 | AT-04 | One test skipped (needs a real study dictionary). | Minor | Covered per study by DK-TPL-001. | Accepted. | Closed |

*Deviations found during manual testing are added below:*

| ID | Found in | Description | Class | Impact assessment | Resolution | Status |
|:-------|:---------|:--------------------------------------------|:-------|:------------------------------------------|:------------------------------------------|:---------|
| | | | | | | |
| | | | | | | |

# 8. Known limitations and residual risks

The current versions have known limitations. These are recorded with their controls and
planned corrections in the residual risk register (DK-VAL-002, section 5). Those an auditor is
most likely to ask about are:

- **No reason for change on device edits (R-01).** Device edits are fully audited (who, what,
  old and new value, when) but carry no reason. Controlled by the data query process and
  audit-trail review (DK-SOP-001 §6).
- **No multi-factor authentication for portal users (R-02)**, and **no automatic inactivity
  logout (R-03).** Controlled by password policy, workstation screen locks, MFA on all
  administrator accounts, and quarterly access reviews.
- **Device-side controls (R-06, R-07, R-08).** No in-app login; no application-level
  encryption of on-device data; records remain editable after upload. Controlled by personal
  credentials, device screen lock and storage encryption, the device register, daily
  synchronisation, and the project data lock.
- **Scheduled CSV backup excludes the server audit trail (R-12).** Controlled by the weekly
  encrypted full snapshot, which includes it.
- **Hosting facts to be confirmed at IQ-07 (R-13).**

The Approver's acceptance of these residual risks is given by signing DK-VAL-002 and the
release statement below.

# 9. Validation package index

| Item | Location |
|:-------------------------------------------|:------------------------------------------------------------|
| Signed documents DK-VAL-001 to DK-VAL-005, DK-SOP-001, DK-TPL-001 | Quality records (signed PDF or paper); editable sources in the DataKollecta-Validation repository, `docs/` (Word) and `src/` (text sources) |
| Automated test evidence | DataKollecta-Validation repository, `evidence/2026-10-08-baseline/` |
| Manual test evidence (screenshots, files, executed protocol) | DataKollecta-Validation repository, `evidence/<date>-manual/`, and the signed executed protocol in the quality records |
| Validation test survey and tools | DataKollecta-Validation repository, `test-assets/` |
| Traceability check | `tools/traceability.py` |
| Source code, change history and release tags | Repositories listed in section 2 |
| Change log | `ChangeLog.md` (field application), `CHANGELOG.md` (portal) |
| Change requests, incidents, access reviews, periodic reviews, restore tests, training | Quality records (DK-SOP-001, section 14) |
| Study build validation records | Each study's data management file |

# 10. Conclusion and release statement

*To be completed and signed when section 5 is complete.*

Based on the results recorded in this report:

☐ All acceptance criteria in DK-VAL-001, section 9, are met. The DataKollecta system, at the
versions in section 2, is **validated and fit for its intended use**, subject to the residual
risks in section 8 and their controls.

☐ The acceptance criteria are not met. The system must not be released for the following
reasons:

| Role | Name | Signature | Date |
|:-------------------------------------------|:-------------------|:-------------------|:-----------|
| System Owner | | | |
| Quality Assurance | | | |
| Head of Data Management (release approval) | | | |
