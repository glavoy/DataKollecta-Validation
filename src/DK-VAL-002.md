---
doc_id: DK-VAL-002
title: User Requirements Specification and Risk Assessment
version: "1.0"
orientation: landscape
---

# 1. Purpose

This document states what the DataKollecta system must do to be fit for its intended use,
and how much each requirement matters. It has three parts:

- **User requirements (section 4).** Each requirement is numbered (URS-nnn), testable and
  owned by the organisation. Requirements are the basis of validation: every requirement is
  traced to at least one test case in the Test Protocol (DK-VAL-004) or, where it is met by a
  procedure, to a section of the System Management SOP (DK-SOP-001). The trace is recorded
  in the Validation Summary Report (DK-VAL-005).
- **Risk assessment (sections 3 and 4).** Each requirement carries a risk rating, which sets
  how deeply it is tested.
- **Residual risk register (section 5) and service-provider assessment (section 6).** These
  record known limitations of the current version and the controls that make each one
  acceptable, and the assessment of the external platforms the system runs on.

The requirements describe the system as it is actually built, at the versions listed in the
Validation Plan (DK-VAL-001). Where the organisation needs something the system does not yet
do, the requirement is still stated, marked **Gap**, and handled in the residual risk
register. This is so the gap stays visible rather than being dropped from the requirements.

# 2. Intended use

DataKollecta is used to collect, store, manage and export research data, including data
collected in clinical and public-health studies. Data is captured on Android tablets and
phones, and on Windows computers, by trained interviewers, often offline and in the field. It
is synchronised to a central server when a connection is available, and reviewed and
exported by study staff through a web portal. Exported data is used for analysis and
reporting.

Data captured in DataKollecta can be source data or case report form data. Errors or loss could
therefore affect the reliability of study results, and where data informs participant
follow-up, participant safety. That is why the requirements below concentrate on data
integrity: data must be attributable, legible, contemporaneous, original and accurate
(ALCOA), and complete, consistent, enduring and available.

# 3. Risk assessment method

Each requirement is assessed for what would happen if the system failed to meet it.

| Factor | High (H) | Medium (M) | Low (L) |
|:---------------|:----------------------------------------------|:--------------------------------------------|:-------------------------------------------|
| **Impact (I)** on participant safety, data integrity or regulatory compliance | Could cause loss, corruption or undetectable change of study data, unattributable data, or unauthorised access to personal data | Could cause incorrect data that is likely to be detected by normal data review, or delay or disruption to data collection | Inconvenience only; no effect on data or participants |
| **Probability (P)** of the failure occurring | Complex or new logic, many inputs, or relies on user behaviour | Moderately complex, established logic | Simple, stable, or provided by a mature platform |
| **Detectability (D)** of the failure if it occurs | Unlikely to be noticed before data is used | Would be noticed by routine review or a later check | Immediately obvious to the user |

The **risk class** combines them. Impact dominates: a High-impact requirement is never rated
below Medium risk.

| Impact | Probability or detectability is High | Otherwise |
|:-------|:-------------------------------------|:----------|
| High | **High** risk | **High** risk if either is Medium, else **Medium** |
| Medium | **Medium** risk | **Low** risk if both are Low, else **Medium** |
| Low | **Low** risk | **Low** risk |

Note: *detectability* is rated "High" when a failure would be **hard** to detect. A
higher score always means a higher risk.

**Test depth by risk class:**

| Risk class | Required verification |
|:-----------|:----------------------|
| **High** | A documented, pre-approved manual test case, including negative tests (attempting what must be refused), with objective evidence. It is also covered by an automated regression test wherever one exists. |
| **Medium** | A documented manual test case (positive path) **or** an automated regression test with retained results. |
| **Low** | An automated test, verification by inspection, or a procedural control. |

The risk assessment is reviewed at each periodic review and whenever a change affects a
requirement (DK-SOP-001, sections 4 and 11).

# 4. User requirements and risk assessment

Abbreviations: **I/P/D** = impact, probability, detectability; **Risk** = resulting risk
class. **Verified by** = the test cases in DK-VAL-004 (IQ, OQ, PQ = manual; AT = automated
regression suite) or SOP sections in DK-SOP-001. **Status** is "Met" unless marked
**Partly met** or **Gap**, which point to the residual risk register (section 5).

## 4.1 Survey definition, build and versioning

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-101 | A study's questionnaire can be defined in a structured data dictionary (Excel workbook) or in the portal's survey designer. The definition is turned into a survey package containing the form definitions and a manifest that identifies the survey. | M | M | M | Medium | OQ-02, AT-04, AT-07 | Met |
| URS-102 | The build refuses a definition that contains errors. Errors include invalid or duplicate field names, missing response lists, skip or logic rules that refer to unknown fields or codes, and calculations that refer to missing fields. Every error is reported to the person building it, and no package is produced. | H | M | M | High | OQ-01, AT-04, AT-07 | Met |
| URS-103 | Each version of a survey has its own survey identifier, while the name of its local database stays the same across versions, so data from all versions accumulates in one dataset. Record ID counters must not restart. | H | M | H | High | OQ-05, AT-02, AT-03, AT-04 | Met |
| URS-104 | The field application refuses to install a survey package whose table or field names are unsafe, or whose query calculations are anything other than a single read-only query. A refused package must not affect other surveys already on the device. | H | L | M | High | OQ-06, AT-02, AT-03, AT-05 | Met |
| URS-105 | A survey package can be tested before use. The test runs simulated interviews to find unreachable questions, skip rules that never fire, and forms that cannot be completed, and produces a report. | M | M | M | Medium | OQ-03, AT-05, TPL | Met |
| URS-106 | A survey moves through the stages Draft, Test, Deployed and Complete. Deployed and Complete surveys cannot be edited, and a deployed survey's package file cannot be replaced or deleted. | H | M | M | High | OQ-04, AT-08 | Met |
| URS-107 | When a new survey version adds fields, the local database gains the new fields. Existing records and columns are kept and never dropped. | H | M | M | High | OQ-05, AT-02, AT-03 | Met |

## 4.2 Data capture (field application)

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-201 | The application supports these question types: free text, numeric, date, date-time, single choice, multiple choice, drop-down list, information screens, and automatically computed fields. | M | L | L | Low | OQ-07, AT-02, AT-03 | Met |
| URS-202 | Numeric and date answers outside the defined range are refused with a message, and the interviewer cannot proceed until the answer is corrected. | H | M | M | High | OQ-08, AT-02, AT-03 | Met |
| URS-203 | Cross-field consistency checks defined for the study are evaluated as data is entered. A failed check shows its message and blocks moving on until resolved. | H | M | M | High | OQ-09, AT-02, AT-03 | Met |
| URS-204 | Skip logic shows only the questions that apply. Answers to questions skipped because of a later change are cleared when the record is saved, so the record holds no inconsistent answers. | H | M | H | High | OQ-10, AT-02, AT-03, AT-05 | Met |
| URS-205 | A question must be answered before the interviewer can move on, unless the study's definition marks it optional. "Don't know" and "Refused" are recorded as answers where the definition offers them. | H | L | M | Medium | OQ-07, AT-02, AT-03 | Met |
| URS-206 | A new record whose key fields duplicate an existing record is refused, as is a value defined as unique that is already in use. | H | M | M | High | OQ-11, AT-02, AT-03 | Met |
| URS-207 | Participant and record identifiers are generated according to the study's configuration. Generated identifiers are never duplicated within a device's dataset for a survey. | H | M | H | High | OQ-12, AT-02, AT-03 | Met |
| URS-208 | Each record automatically carries: interview start and stop times, a globally unique record identifier, the software name and version, the survey identifier, and the time of last modification. | H | L | M | Medium | OQ-13, AT-02, AT-03 | Met |
| URS-209 | Input formats (masks, fixed lengths, decimal places) defined for a field are enforced during entry. | L | L | L | Low | OQ-38, AT-02, AT-03 | Met |
| URS-210 | All data capture works without a network connection. Saved records stay on the device across application restarts and device reboots until they are synchronised. | H | M | M | High | OQ-14, PQ-01 | Met |
| URS-211 | Repeating groups and linked child forms (for example, household members) are linked to their parent record by the configured linking field. | H | M | M | High | OQ-36, AT-02, AT-03, AT-05 | Met |
| URS-212 | Response options can come from the definition itself, from a CSV file in the package, or from data already collected on the device. Options are filtered as defined. | M | M | L | Medium | OQ-37, AT-02, AT-03 | Met |
| URS-213 | Collected data is never deleted from the device by application functions. Removing a survey definition from the device leaves its collected data in place. | H | L | M | Medium | OQ-14 | Met |

## 4.3 Data changes and audit trail

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-301 | Any change to a saved record on the device is recorded in an audit trail on the device. Each entry gives the form, field, record identifier, old value, new value, date and time of the change, the user identifier, and a unique change identifier. | H | M | H | High | OQ-15, AT-02, AT-03 | Met |
| URS-302 | Device audit-trail entries are uploaded to the server and kept there unchanged. Uploading the same entry again changes nothing, and an attempt to upload an altered version of an existing entry is refused. | H | M | H | High | OQ-15, AT-08, AT-09 | Met |
| URS-303 | The server records an audit event for every creation, change and deletion of study data and of study configuration (projects, members, field credentials, surveys, forms, data locks). The event records who did it, when (server time), the role or channel used, and the values before and after. | H | M | H | High | OQ-23, AT-08, AT-09 | Met |
| URS-304 | No user of the system, including project owners and the server's own functions, can change or delete audit-trail records, by single or bulk operations. | H | L | H | High | OQ-24, AT-08, AT-09 | Met |
| URS-305 | The audit trail can be reviewed for each record in the portal, and exported for a whole project in a human-readable format. | H | L | M | Medium | OQ-23, OQ-29 | Met |
| URS-306 | A reason is recorded for every change to data that has already been saved. | H | H | H | High | OQ-15, OQ-25, OQ-26, OQ-27 | **Partly met**: recorded for portal actions (reclassification, data lock, purge, key revocation), not yet for edits made on the device. See R-01. |
| URS-307 | Server timestamps come from the server clock and include the time zone. Device timestamps record the local wall-clock time of the event. | H | L | M | Medium | OQ-23, AT-08 | Met; device time zone not uploaded, see R-17 |
| URS-308 | Portal users cannot create, change or delete collected records. Data originates only from field devices. | H | L | H | High | OQ-22, AT-08, AT-09 | Met |

## 4.4 Access control and security

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-401 | Each portal user has an individual account identified by a verified e-mail address. Passwords are at least 10 characters, and changing a password requires re-authentication. | H | M | M | High | OQ-20, IQ-06, AT-07 | Met |
| URS-402 | Access to each project is role-based (Owner, Editor, Viewer). Permissions are enforced by the server, not only hidden in the user interface. A user who is not a member of a project can see nothing of it. | H | M | H | High | OQ-21, AT-08 | Met |
| URS-403 | Field devices authenticate with a project code, username and password. Passwords are stored only as salted hashes. Failed logins return one uniform message, and repeated failures lock the username and the source address for a period. | H | M | M | High | OQ-16, AT-08 | Met |
| URS-404 | Device sessions expire, and are refused immediately when the credential is disabled or reset, or when the project is paused or archived. Data already on the device is kept. | H | M | M | High | OQ-17, AT-08 | Met |
| URS-405 | All communication between devices, browsers and the server is encrypted (HTTPS/TLS). | H | L | M | Medium | OQ-34, IQ-07 | Met |
| URS-406 | Portal users are able to use, and privileged users are required to use, multi-factor authentication. | H | M | H | High | IQ-06 | **Gap**, see R-02 |
| URS-407 | Inactive portal sessions end automatically after a defined period and require re-authentication. | M | M | M | Medium | IQ-06 | **Gap**, see R-03 |
| URS-408 | Lists of current project members, their roles and field credentials (including disabled ones) are available, and every change to access is in the audit trail. | H | L | M | Medium | OQ-35, OQ-23 | Met |
| URS-409 | Read-only API keys for data feeds are limited to one project, stored only as hashes, and can expire or be revoked. Their creation, use and revocation are audited. | H | M | M | High | OQ-30, AT-08 | Met |
| URS-410 | Survey package files are readable only by members of the project they belong to. Only Owners and Editors can upload them. | M | M | M | Medium | OQ-21, AT-08 | Met |
| URS-411 | Study data stored on field devices is protected against access by unauthorised persons if a device is lost or stolen. | H | M | H | High | DK-SOP-001 §9 | **Partly met**: relies on device encryption and screen lock, see R-06 and R-07 |
| URS-412 | Portal accounts are protected against repeated password guessing. | H | M | M | High | IQ-06 | **Partly met**: rate limiting only, see R-05 |

## 4.5 Synchronisation and data transfer

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-501 | Records are uploaded in batches. A record is marked as synchronised only after the server confirms it. A failed or interrupted upload is retried later, without losing or duplicating records. | H | M | H | High | OQ-18, PQ-01, AT-02, AT-03, AT-08 | Met |
| URS-502 | A record edited after upload is uploaded again, and the server holds the latest version. | H | M | H | High | OQ-15, AT-02, AT-03, AT-08 | Met |
| URS-503 | The server attributes every uploaded record and change to the field credential that authenticated the upload, not to a value supplied by the device. It also records the device identifier. | H | L | H | High | OQ-18, AT-08 | Met |
| URS-504 | Devices can download only surveys of projects they are authenticated to, through links that expire. | M | L | M | Medium | OQ-39, AT-08 | Met |
| URS-505 | Each survey on a device is bound to the project it came from. A survey or database name already bound to another project is refused, so that two projects' data can never be mixed in one database. | H | L | H | High | OQ-19, AT-02, AT-03 | Met |

## 4.6 Data management controls

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-601 | Each record is labelled as *test* or *deployed* when the server first receives it, according to the survey's stage at that time. The label can be changed only by a project Owner, with a reason, and the change is audited. | H | M | M | High | OQ-25, AT-08 | Met |
| URS-602 | A project Owner can lock a project's data, giving a reason. While locked, the server refuses new and changed records and change-history entries, which stay on the device until the lock is lifted. Locking and unlocking are audited. | H | M | M | High | OQ-26, AT-08, AT-09 | Met |
| URS-603 | Test records can be permanently removed ("purged") only by a project Owner, only with a reason, and never while the data is locked. The full content of each purged record is preserved in the audit trail, and a purged record that a device uploads again is discarded and logged. | H | M | M | High | OQ-27, AT-08 | Met |
| URS-604 | A project or survey that holds collected data or audit history cannot be deleted, only archived or completed. | H | L | M | Medium | OQ-28, AT-08, AT-09 | Met |

## 4.7 Export and reporting

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-701 | A project's data can be exported to CSV, one file per form, together with the device change history and the project's server audit trail. | H | M | M | High | OQ-29, PQ-01, AT-07 | Met |
| URS-702 | Every export includes a manifest listing each file with its SHA-256 checksum and size, and the portal version and build that produced it. Every export is recorded in the audit trail. | H | L | M | Medium | OQ-29, AT-07 | Met |
| URS-703 | Authorised systems can read a project's data through a read-only API (data feed). | M | L | M | Medium | OQ-30, AT-08 | Met |

## 4.8 Backup, recovery and retention

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-801 | Project data is backed up automatically, at a defined frequency, to storage independent of the hosting platform. Backup failures are reported to a responsible person. | H | M | M | High | OQ-31, DK-SOP-001 §7 | **Partly met**: the scheduled CSV backup excludes the server audit trail, see R-12 |
| URS-802 | A complete, encrypted snapshot of the database and stored files can be taken. Each snapshot has an integrity manifest and a receipt with its checksum. | H | M | M | High | OQ-32, AT-10 | Met |
| URS-803 | A snapshot can be restored and verified. Restoration checks integrity first, refuses a tampered or incomplete snapshot, and restores in a single transaction to an empty target database only. | H | M | H | High | OQ-32, AT-10 | Met |
| URS-804 | The field application keeps a local, append-only log of every record it saves, for recovery if the database is damaged. | M | L | M | Low | OQ-33 | Met |
| URS-805 | Study data, audit trails, exports and validation records are retained, readable, for the required retention period, including after the study or the system is closed. | H | M | M | High | DK-SOP-001 §13 | Met (procedural) |

## 4.9 Versioning, operation and infrastructure

| ID | Requirement | I | P | D | Risk | Verified by | Status |
|:-------|:----------------------------------------------------------------------------|:--|:--|:--|:-------|:-------------------|:----------|
| URS-901 | The version of each component in use can be identified: the application version on its Settings screen and in every record; the portal version and build on screen and in every export; the database migration level; and the version of each survey tool. | H | L | M | Medium | IQ-01–IQ-05, IQ-08, OQ-13 | Met |
| URS-902 | Every change to the system is controlled. It is assessed for impact, tested, approved, released under a recorded version, and noted in the change log. | H | M | M | High | DK-SOP-001 §4, IQ-01 | Met (procedural) |
| URS-903 | The hosting platforms provide an adequate level of security, availability, physical protection and backup, and give the organisation access to its data at all times. | H | L | M | Medium | IQ-07, section 6 | Met; to be confirmed at IQ-07, see R-13 |
| URS-904 | Defects, incidents and user problems can be reported, recorded and resolved through a defined route. | M | M | M | Medium | DK-SOP-001 §8 | Met (procedural) |
| URS-905 | Users are trained in the functions they use before they are given access. | H | M | M | High | DK-SOP-001 §12 | Met (procedural) |

# 5. Residual risk register

These are the known limitations of the validated versions, with the controls that make each
one acceptable for use and the planned correction. The register is reviewed at each periodic
review (DK-SOP-001 §11) and updated after every release. A risk is closed only when its
correction has been released and verified.

| Risk ID | Description | I | Risk | Controls in place (mitigation) | Planned correction (CAPA) |
|:-------|:-----------------------------------------------------------|:--|:------------|:-----------------------------------------------------------|:------------------------------------|
| R-01 | Edits made on the device to a saved record do not capture a reason for change, nor the device's time zone and UTC time, although the server is ready to accept them (URS-306, URS-307). | H | High | Every edit is still recorded with old and new values, time and user (URS-301), and uploaded and protected (URS-302). DK-SOP-001 §6 requires corrections after upload to go through the study's data query process. The query form records the reason and is filed with the study documents, and the audit-trail review reconciles device edits against resolved queries. | Add a mandatory reason-for-change prompt and send UTC time and time zone with each change, in the next application release. |
| R-02 | Multi-factor authentication is enabled on the server but the portal offers no way to enrol, so portal users sign in with a password only (URS-406). | H | High | Unique passwords of at least 10 characters, stored in a password manager (DK-SOP-001 §9). Few Owners. Quarterly access reviews. All server administration (hosting dashboards, code hosting) is done through provider accounts that require MFA. | Add MFA enrolment to the portal and require it for Owners. |
| R-03 | The portal does not end an inactive session. Sign-in tokens refresh automatically (URS-407). | M | Medium | Workstation screen lock after at most 10 minutes of inactivity is required (DK-SOP-001 §9). Users must sign out of shared computers. | Configure an inactivity timeout and session time limit. |
| R-04 | Anyone can create a portal account. | L | Low | A new account has no access to any project until an Owner adds it. Membership changes are audited and reviewed. | Consider disabling open sign-up and using invitations. |
| R-05 | Portal sign-in is rate-limited but does not lock an account after repeated failures (URS-412). | H | Medium | Rate limits on sign-in attempts. Minimum password length. Password manager. R-02 controls. | Account lockout or MFA (with R-02). |
| R-06 | The field application has no user login of its own. Anyone holding an unlocked device can enter or edit data. | H | Medium | Each interviewer has a personal field credential, and devices are not shared without a recorded handover. Device screen lock with PIN is required (DK-SOP-001 §9). Edits are audited with the credential's user identifier. | Consider an application PIN. |
| R-07 | The survey databases and local backup log on the device are not encrypted by the application. On macOS and Linux, stored sync passwords are not held in the operating system's secure store. | H | Medium | Only Android (which encrypts storage by default when a screen lock is set) and Windows with full-disk encryption are approved for data collection (DK-SOP-001 §9). Regular synchronisation limits what is on a device. A lost or stolen device is an incident: its credential is reset at once (DK-SOP-001 §8). | Evaluate application-level database encryption. |
| R-08 | Records stay editable on the device after upload. There is no per-record lock or sign-off. | M | Medium | Every edit is audited and re-uploaded (URS-301, URS-502). The project data lock (URS-602) freezes the server dataset at database lock. Audit-trail review (DK-SOP-001 §6). | Consider per-record finalisation. |
| R-09 | Device session tokens are stored on the server unhashed and are valid for 30 days. | M | Medium | The token table is accessible only to server functions. Tokens are revoked by credential reset or disable and by pausing the project. | Store only a hash of each token; consider a shorter lifetime. |
| R-10 | A database administrator (the owner of the database objects) could disable the triggers that protect the audit trail. | H | Medium | Administrative access to the database is limited to named administrators, using MFA-protected provider accounts. Every schema change is a version-controlled migration. The periodic review runs a check that all protective triggers are present and enabled (DK-SOP-001 §11). The hosting platform keeps its own logs. | None planned beyond the controls; this is inherent to any database. |
| R-11 | Server audit events exist only from the audit-trail release (5 October 2026) onwards and were not reconstructed for earlier activity. Records uploaded before that date have no server-side history before it. | M | Medium | Device change history (URS-301) existed before that date and was uploaded. The baseline date is stated in the Validation Summary Report. Studies whose data predates it record this in their data management file. | None; historical. |
| R-12 | The scheduled CSV backup does not include the server audit trail and writes no checksum manifest (URS-801). | H | Medium | The encrypted full snapshot (URS-802) includes all tables, including the audit trail. It is taken weekly, before each release, and at each database lock (DK-SOP-001 §7). The platform's own backups also apply. | Add the audit trail and a manifest to the scheduled backup. |
| R-13 | Hosting region, backup retention and point-in-time recovery of the database platform are not recorded in the system documentation (URS-903). | M | Medium | Recorded at IQ-07 from the provider account and reviewed annually. | Not applicable once recorded. |
| R-14 | Automated tests are run by hand; there is no continuous integration. | M | Medium | DK-SOP-001 §4 requires every automated suite to be run on the release commit, with logs retained, before any release. | Set up continuous integration for all components. |
| R-15 | The web project's dependency lockfile is out of step with its package list, so a clean, locked install (`npm ci`) fails. See deviation DEV-01. | L | Low | Production builds are made by the hosting platform from the committed sources. The tests were run on a fresh install. | Regenerate and commit the lockfile. |
| R-16 | The development and validation team is small: the same people design, build and administer the system (segregation of duties). | M | Medium | Validation testing and the review of every change are done by someone other than the author (DK-VAL-001 §6). Administrator access is limited and reviewed. Administrators have no role in a study's data entry. | Review when the team grows. |
| R-17 | Device times are the device's own clock. A device with a wrong date or time records wrong interview times. | M | Medium | Devices must use automatic network time (DK-SOP-001 §9). The server records its own receipt time for every record. Field supervisors check device time at each sync. | With R-01, upload the time zone and UTC time. |
| R-18 | Every project role, including Viewer, can export all of a project's data, including personal data. | H | Medium | Membership is granted only to people authorised to see the study data, and reviewed quarterly. Every export is audited (URS-702). | Consider an export permission separate from viewing. |
| R-19 | The hosting providers can update their platforms without notice. | M | Medium | Provider status and change notices are monitored. A platform change that affects the system is handled as an incident or change (DK-SOP-001 §4 and §8). The periodic review covers provider changes. | Not applicable. |
| R-20 | On 4 September 2026, a configuration update to the authentication service turned off e-mail verification in production for about 10 minutes. It was found and reversed. | M | Low | Authentication configuration is now under change control: each configuration push is reviewed against the committed file before and after it is applied (DK-SOP-001 §4.5). IQ-06 verifies the production configuration. | Closed. |

# 6. Service-provider assessment

The system runs on external platforms. For each one, the organisation remains responsible for
its data. The assessment records what each provider does, the risk, and how the organisation
satisfies itself. The facts marked *to be recorded* are confirmed from the provider accounts
at installation qualification (IQ-07) and reviewed at each periodic review.

| Provider | Service used | Data held | Basis of assessment | Facts to be recorded at IQ-07 | Conclusion |
|:---------|:-------------|:----------|:--------------------|:---------------------|:-----------|
| **Supabase** (managed PostgreSQL, authentication, file storage and server functions) | Production database, user authentication, survey package storage, server functions app-login, app-sync and project-data-feed | All collected study data, audit trails, user accounts | Published security documentation and independent security attestation (for example a SOC 2 report). Encryption at rest and in transit. Database access governed by row-level security defined in the organisation's own migrations. Data export at any time with the organisation's own backup tools (URS-801–803). | Organisation and project; region; plan; backup frequency, retention, and whether point-in-time recovery is enabled; administrators and MFA status; current attestation report date | Acceptable, subject to IQ-07 confirmation and the organisation's own backups |
| **Vercel** (static web hosting) | Hosts the portal's web application files | None. The portal is a static application; data goes directly between the browser and Supabase. | Published security documentation. Deployment only from the organisation's code repository. | Project; production domain; deployment source branch; administrators and MFA status | Acceptable; low risk because no study data is stored |
| **GitHub** (code hosting) | Source code, change history, release tags | None (no study data) | Version control is the evidence of change control (DK-SOP-001 §4) | Repository list; administrators and MFA status; branch protection | Acceptable |
| **Application distribution** (Android package files, Windows installer) | Installation of the field application | None | Packages are built from tagged sources and signed with the organisation's own keys; checksums are recorded at IQ-02 | Signing certificate fingerprint; distribution channel | Acceptable |

Agreements: the organisation keeps the provider terms of service and data-processing terms in
force for the life of the system, and makes sure study data can be made available to auditors
and inspectors through the organisation's own export and backup tools, independently of the
providers.
