---
doc_id: DK-VAL-001
title: Validation Plan
version: "1.0"
orientation: portrait
---

# 1. Purpose

This plan defines how the DataKollecta system is validated: what is in scope, how risk
decides the depth of testing, who does what, which documents are produced, and the criteria
for declaring the system fit for its intended use.

Validation here means establishing, with documented evidence, that the system consistently
does what it is required to do. That includes protecting the integrity, confidentiality and
availability of the data it holds. The approach follows generally accepted practice for
computerised systems used in clinical research and other regulated studies: a risk-based
life-cycle approach, with documented requirements and approved test cases, traceability
between them, controlled change, and periodic review. It is written to satisfy any sponsor,
auditor, ethics committee or regulatory inspector who asks how the system was validated.

DataKollecta is developed and operated by IDRC. IDRC is therefore both the supplier of the
system and the organisation responsible for its validation, and no external certification
is relied on.

# 2. Scope

## 2.1 In scope

The validation covers the DataKollecta system at the following baseline versions:

| Component | Baseline version | Source identifier |
|:--------------------|:--------------------------|:-----------------------------------------------|
| Field application (DataKollecta product, Android and Windows) | 1.4.1+19 | Tag v1.4.1+19, commit 8dc4302ef9b8 |
| Web portal, server functions and database schema | 1.2.0; migration head 20261008150000 | Tag web-v1.2.0, commit ea1f2990cdd8 |
| SurveyGen | Commit 005a7f97e2a9 | DataKollecta-SurveyGen |
| SurveyTest | Commit d38cb50ea3a8 | DataKollecta-SurveyTest |
| DataBackup | Commit dafe783b53ab | DataKollecta-DataBackup |

It also covers the procedures that keep the system in a validated state (DK-SOP-001), and the
validation of each study's configuration (DK-TPL-001).

## 2.2 Out of scope

- **GiSTX**, the separate product built from the same field-application code base that
  synchronises by FTP. Its code is excluded from the DataKollecta build at compile time.
- **The internal software of the hosting platforms** (Supabase, Vercel, GitHub). These are
  assessed as service providers (DK-VAL-002, section 6), not tested as software.
- **Operating systems, browsers and devices.** These are infrastructure, controlled through
  the device and workstation requirements in DK-SOP-001, section 9.
- **iOS, macOS and Linux builds of the field application.** These are not approved for
  production data collection.
- **Statistical analysis software** used on exported data.

# 3. System description and intended use

The intended use is described in DK-VAL-002, section 2, and the system design in DK-VAL-003.
In short, DataKollecta captures research data offline on field devices and synchronises it
to a central server. Study staff manage projects, surveys and users there, and review and
export the data. Data may be source data or case report form data in clinical and
public-health studies, so the system is treated as having a direct impact on data integrity
and, potentially, on participant safety.

**Software category.** The field application, portal and tools are custom software developed
by IDRC, and are validated in full. The hosting platforms are configured infrastructure and
services, and are covered by the service-provider assessment and installation qualification.

# 4. Validation strategy

## 4.1 Risk-based approach

Every requirement in the User Requirements Specification is rated for its impact on
participant safety and data integrity, the probability of failure, and how easily a failure
would be detected (DK-VAL-002, section 3). The resulting risk class sets the test depth:

- **High:** pre-approved manual tests with negative cases and objective evidence, plus
  automated regression tests.
- **Medium:** a manual test or an automated test.
- **Low:** an automated test, inspection or a procedural control.

Requirements that the system does not yet fully meet are kept in the specification, marked
as gaps, and assessed in a residual risk register with compensating controls and planned
corrections. Known limitations are disclosed, not hidden.

## 4.2 Two levels of validation

1. **Platform validation** (this plan, DK-VAL-002 to DK-VAL-005). This covers the system's
   general functions: data capture engine, edit checks, synchronisation, audit trail, access
   control, export, backup and restore. It is done for the baseline and repeated, in
   proportion to the change, for each new release (DK-SOP-001, section 4).
2. **Study configuration validation** (DK-TPL-001, one record per study and per protocol
   amendment). This covers the study's own forms, edit checks, skips and identifiers,
   verified against the protocol and data management plan before the study's survey is
   deployed.

Platform validation makes it unnecessary to re-test the engine for every study. Study
validation makes sure each study's configuration does what that study's protocol requires.

## 4.3 Retrospective validation

DataKollecta was in use before this validation package was produced. The validation is
therefore **retrospective** for the baseline versions in section 2.1. This is stated openly.

- The baseline versions are validated as they are, against requirements that describe both
  what the system does and what it should do.
- The automated test suites that existed during development are used as validation evidence.
  They were run on the baseline commits and their results retained (DK-VAL-005, section 4).
- Development records (version history, change log, release tags) are used as evidence of
  change control before this package.
- Limitations found during the retrospective assessment are recorded as residual risks
  (DK-VAL-002, section 5) and in the Validation Summary Report.
- Studies that collected data before the validation was approved should note this in their
  data management documentation. They can rely on this validation for the baseline
  versions, and for earlier versions only where the change log shows the relevant functions
  were unchanged.

From the approval of this package onwards, validation is **prospective**: every release is
validated before it is put into production (DK-SOP-001, section 4).

# 5. Deliverables

The validation package is deliberately small. Each document combines related content so
that an auditor can see the whole validation in a few documents.

| Document ID | Title | Content |
|:-------------|:-------------------------------|:---------------------------------------------------|
| DK-VAL-001 | Validation Plan (this document) | Scope, strategy, roles, acceptance criteria |
| DK-VAL-002 | User Requirements Specification and Risk Assessment | Requirements, risk ratings, residual risk register, service-provider assessment |
| DK-VAL-003 | Functional and Design Specification | How each requirement is met |
| DK-VAL-004 | Test Protocol | Pre-approved installation (IQ), operational (OQ), performance (PQ) and automated (AT) test cases, with spaces for results |
| DK-VAL-005 | Validation Summary Report | Results, traceability matrix, deviation log, known issues, release statement, package index |
| DK-SOP-001 | System Management SOP | Procedures that keep the system validated (change control, access, audit-trail review, backup and restore, incidents, security, periodic review, training, retention), with forms |
| DK-TPL-001 | Study Build Validation Record | Template completed for each study's configuration |

Supporting evidence is kept with the package: automated test logs with their checksums,
screenshots and other attachments from manual testing, and signed copies of all documents.

# 6. Roles and responsibilities

| Role | Responsibilities in validation |
|:-----------------------|:------------------------------------------------------------------|
| **System Owner** (Lead Developer) | Owns the system and this package. Writes the specifications and test protocol. Runs the automated tests. Fixes defects. Maintains the system under DK-SOP-001. |
| **Quality Assurance** (independent reviewer) | Reviews and approves the plan, specifications and protocol before testing. Reviews executed tests and deviations. Approves the Summary Report. Must not have written the code under review. |
| **Tester** | Executes the manual test cases exactly as written. Records actual results and evidence. Raises deviations. Must not be the author of the test case being executed, and should be a person who will use the system in practice (for example a data manager or field supervisor). |
| **Head of Data Management** (Approver) | Approves the plan and protocol. Decides on the acceptability of residual risks. Signs the release statement in the Summary Report. |
| **Study teams** | Complete the Study Build Validation Record (DK-TPL-001) for each study before deployment. |

One person may hold more than one role, except that nobody reviews or tests their own work.
Where the team is too small to keep these roles apart, the reason is recorded in the
Summary Report and an external reviewer is used for the independent review.

# 7. Testing approach

## 7.1 Test types

| Type | Purpose | Where it is run |
|:-----|:----------------------------------------------------|:-----------------------------------------------|
| **IQ**: Installation Qualification | The correct versions are installed and configured as specified in production. | Production |
| **OQ**: Operational Qualification | Each function works as specified, including refusals of invalid or unauthorised actions. | A test project in production, or a non-production environment where the test would affect real data |
| **PQ**: Performance Qualification | The system supports the real end-to-end workflow, with real devices and users. | A test project in production |
| **AT**: Automated tests | Regression suites covering the code of every component. | Development or test environment, on the release commit |

## 7.2 Test environments

Manual OQ and PQ tests use a dedicated **test project** in the production system. This
means they run on the same platform, configuration and code as studies. All records created
are labelled *test* (DK-VAL-003, section 6.6), and are purged or reclassified after testing.
Tests that would affect production configuration (for example authentication settings) are
not run in production; they are verified by inspection of the configuration (IQ).

Automated tests that need a server run against a **local server stack** built from the same
migrations and server-function code as production. Any difference between this environment
and production (tool versions, how server functions are hosted, network restrictions) is
recorded with the results and its significance assessed in the Summary Report.

## 7.3 Test case requirements

Every test case in DK-VAL-004 states:

- its identifier and the requirements it verifies;
- the software version under test;
- its prerequisites;
- its numbered steps;
- the expected result of each step.

The protocol is approved **before** it is executed. During execution, the tester records:

- the actual result of each step;
- pass or fail;
- their initials and the date;
- a reference to any evidence (screenshot, file, log).

Results must be recorded as they are observed. Corrections follow good documentation
practice: a single line through the original, the correction, initials, date and reason.
Nothing may be erased or overwritten.

Evidence is kept in the evidence folder of the validation package, named by test case
identifier.

## 7.4 Automated tests as evidence

Automated suites are treated as test cases (AT-01 to AT-10). For each one the validation
records:

- the exact command;
- the commit tested;
- the tool versions;
- the full output log;
- the SHA-256 checksum of the log;
- the number of tests run, passed, failed and skipped.

A suite passes when its command exits successfully and no test fails. A skipped test must be
explained.

# 8. Deviation management

Any result that differs from the expected result is a **deviation**. Each deviation is
recorded in the deviation log in DK-VAL-005 with:

- an identifier;
- the test step;
- a description;
- its classification;
- an impact assessment;
- the action taken and any retest.

| Classification | Definition | Required before release |
|:---------------|:------------------------------------------------------|:-------------------------------------------|
| **Critical** | Data loss or corruption, unauthorised access, or failure of the audit trail, with no workaround | Must be fixed and retested |
| **Major** | A requirement is not met, but a documented workaround or procedural control exists | Fix, or an accepted residual risk with a correction plan, approved by the Approver |
| **Minor** | Cosmetic, documentation, test-script or test-environment problem with no effect on data | Recorded; corrected when convenient |

A deviation caused by an error in the test case itself is corrected in the test case, and the
step is re-executed. When a fix is made, the affected test cases are re-executed. Where
previously passed tests are not repeated, the reason is recorded.

# 9. Acceptance criteria

The system is declared fit for its intended use when all of the following hold:

1. All documents in section 5 are approved.
2. All IQ test cases pass.
3. All OQ and PQ test cases for High and Medium risk requirements pass, or their deviations
   are resolved under section 8.
4. All automated suites (AT) pass, or their deviations are resolved.
5. There is no open critical deviation.
6. Every requirement is traced to a passed test or an approved procedural control, or to an
   accepted residual risk.
7. The residual risk register has been reviewed and accepted by the Approver.
8. The procedures in DK-SOP-001 are approved and the people who operate the system are
   trained in them.

# 10. Service providers

Hosting providers are assessed in DK-VAL-002, section 6. Installation qualification (IQ-07)
records the facts of the production configuration from the provider accounts. The
assessment is renewed at each periodic review, and whenever a provider or plan changes.

# 11. Maintaining the validated state

After release, the validated state is maintained by DK-SOP-001:

- change control and release (section 4);
- access management (section 5);
- audit-trail review (section 6);
- backup and restore testing (section 7);
- incident management (section 8);
- security (section 9);
- periodic review (section 11);
- training (section 12);
- retention (section 13).

The validation documents of every version used in a study are retained for as long as that
study's records.

# 12. Glossary

| Term | Meaning |
|:---------------|:-------------------------------------------------------------------------|
| ALCOA+ | Data that is Attributable, Legible, Contemporaneous, Original, Accurate, Complete, Consistent, Enduring and Available |
| Audit trail | A secure, computer-generated, time-stamped record of who did what and when, with values before and after |
| CAPA | Corrective and preventive action |
| Deviation | A difference between the expected and the actual result of a test |
| Field credential | A project code, username and password used by the field application to synchronise |
| IQ, OQ, PQ | Installation, Operational and Performance Qualification |
| Migration | A version-controlled script that changes the database schema |
| Survey package | The ZIP file containing a study's form definitions and manifest |
| Traceability | The documented link between each requirement and the test or procedure that verifies it |
| URS | User Requirements Specification |
