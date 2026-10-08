---
doc_id: DK-VAL-003
title: Functional and Design Specification
version: "1.0"
orientation: portrait
---

# 1. Purpose and scope

This document describes how DataKollecta meets the user requirements in DK-VAL-002: its
components, how data moves between them, and the design of the controls that protect data
integrity. It describes the versions listed in the Validation Plan (DK-VAL-001, section 2).
The section numbers are referenced from the traceability matrix in the Validation Summary
Report (DK-VAL-005).

The source code of each component, with its version history, is the detailed design. This
document summarises it at the level an auditor or a new developer needs, and names the code
locations where a control is implemented so it can be inspected.

# 2. System overview

## 2.1 Components

| Component | What it is | Technology | Repository |
|:--------------|:---------------------------------------------------|:-------------------|:-----------------------|
| Field application | Collects data on Android devices and Windows computers, offline, and synchronises with the server | Flutter/Dart, SQLite | DataKollecta |
| Web portal | Project, people, survey and data management for study staff, in a web browser | React/TypeScript, static web application | DataKollecta-Web |
| Server | Database, authentication, file storage and three server functions (app-login, app-sync, project-data-feed) | Supabase: PostgreSQL 17, Supabase Auth, Storage, Deno edge functions | DataKollecta-Web (supabase/) |
| SurveyGen | Builds a survey package from an Excel data dictionary | Python | DataKollecta-SurveyGen |
| SurveyTest | Tests a survey package by running simulated interviews with the field application's own engine | Flutter/Dart (desktop) | DataKollecta-SurveyTest |
| DataBackup | Scheduled CSV backup; encrypted full snapshot; verified local restore | Python, PostgreSQL client tools, GnuPG | DataKollecta-DataBackup |

The same field-application code base also builds a separate product (GiSTX) that
synchronises by FTP. That product is a different application with its own identity and
is outside the scope of this document. The DataKollecta build excludes all FTP code at
compile time (`AppConfig.isDataKollecta`, `lib/config/app_config.dart`).

## 2.2 Data flow

1. **Design.** A study's questionnaire is written as an Excel data dictionary and built with
   SurveyGen, or designed in the portal's survey designer. The result is a survey package
   (section 3).
2. **Test.** The package is tested with SurveyTest and by hand (DK-TPL-001), then uploaded to
   the project in the portal and moved to the *Test* stage, then *Deployed*.
3. **Download.** An interviewer signs in on the field application with a field credential. The
   application lists the project's surveys and downloads the package through a time-limited
   link (section 5.4).
4. **Capture.** Interviews are recorded offline into a SQLite database on the device, one per
   survey (section 4).
5. **Synchronise.** When a connection is available, new and changed records and the
   device's change history are uploaded over HTTPS to the app-sync function. It writes them
   to PostgreSQL (section 5.3).
6. **Review and export.** Study staff view records and their histories in the portal and
   export them as CSV with an integrity manifest (sections 6.5 and 6.9). Authorised systems
   can read the data through the read-only data feed (section 6.10).
7. **Protect.** Every server change is written to the audit trail (section 7). Data is backed
   up by the platform and by the organisation's own tools (section 8).

# 3. Survey definition and packaging

## 3.1 Data dictionary and SurveyGen

The data dictionary is an Excel workbook. Each worksheet ending in `_dd` defines one form
(questionnaire), one row per question. A `crfs` worksheet lists the forms, their order,
their parent–child links and their ID configuration. SurveyGen (`main.py --config`) reads
the workbook and a configuration file giving the survey name, survey identifier and
database name.

Before writing anything, SurveyGen validates the dictionary (`dd_validators.py`,
`skip_parser.py`, `skip_graph.py`, `calculation_parser.py`, `response_parser.py`). It checks:

- field names: their syntax, that they are unique, and that none duplicates a reserved
  system variable;
- question type against field type, and that required attributes (such as maximum length)
  are present;
- numeric and date ranges, and mask lengths;
- that every selection question has responses;
- that logic checks use known fields, valid operators and real response codes;
- that skip targets exist and skip values are real codes, with no self-referencing preskips;
- that calculations refer only to fields that exist and precede them, and that query
  calculations are a single read-only SELECT;
- that the Comments field is optional, and that every CSV file the definition refers to
  exists.

Any **error** stops the build. The generated files are deleted, no package is produced,
and the program exits with status 1. Errors and warnings are written to the build log
`gistlogfile.txt` and summarised on screen. Only a clean run produces a package and
reports SUCCESS.

SurveyGen also writes the reserved system variables into every form, in fixed positions
(section 4.6). It drops any row the dictionary declares for them, so a dictionary cannot
misplace them.

## 3.2 Portal survey designer

The portal includes a survey designer that produces the same package format. Its
validation and XML generation are covered by the portal's automated tests
(`src/lib/**/__tests__`).

## 3.3 Package format

A survey package is a ZIP file containing:

- one XML file per form;
- the CSV files the forms use for response lists, and no others;
- a manifest, `survey_manifest.gistx` (JSON), with `surveyId`, `surveyName` and
  `databaseName`, and the form list and configuration from the `crfs` sheet.

## 3.4 Versions and the dataset

Every version of a survey must have a new `surveyId`. The `databaseName` must stay the same
for the life of the study: it names the SQLite database on the device and so ties every
version to one dataset. Record-ID counters are derived from the records already in that
database, so changing the database name would restart them and produce duplicate IDs. On the
server, "New Version" in the portal keeps the dataset; "Duplicate" starts a new one.

## 3.5 SurveyTest

SurveyTest installs a package in a sandbox, using the field application's own parsing and
navigation code, compiled in from the DataKollecta repository rather than copied. It runs in
four stages:

1. Static checks of the package.
2. **Steered interviews**: for every skip rule, one interview that tries to make it fire and
   one that tries to stop it, plus an attempt to reach any question not yet reached.
3. **Random interviews**, with several answering strategies.
4. **Integrity checks** on the saved records.

It reports findings by type: a question never reached, a form that cannot be completed, a
skip rule that never fires, a logic check that can never fail, an empty cascading list, and
others. It also produces a decision table per form showing what each skip rule does, for a
person to compare with the paper questionnaire. Every finding carries a seed that replays
it exactly. The report is a single HTML file.

SurveyTest does not judge whether the form matches the protocol; that is the purpose of
the study build review and user acceptance test (DK-TPL-001).

# 4. Field application

## 4.1 Platforms and identity

The DataKollecta build has application ID `com.datakollecta.datakollecta` and its own signing
key. It stores its files in a folder named `DataKollecta`. Android is the primary platform;
Windows is also supported. Each installation has a stable device identifier
(`lib/services/sync/device_identity.dart`), which is sent with every upload.

## 4.2 Installing a survey package

Downloaded packages are extracted once into the survey folder
(`lib/services/survey_config_service.dart`). Each survey's definition is read and checked
when it is opened (`lib/services/survey_loader.dart`). Every table and field name that comes
from the dictionary is checked against a strict identifier rule
(`SurveyTableSchema.validateIdentifier`) at the points where it enters the application:

- question field names;
- the table and column of database-sourced response lists;
- every identifier in the forms list;
- the table name derived from each form's file name.

A query calculation is accepted only if it is a single SELECT statement with no comments
(`SurveyTableSchema.validateQuerySql`). A package that breaks either rule is refused with an
error. Each survey is opened independently, so one bad package does not stop other surveys
on the device from working.

Removing a survey from the device (Settings) deletes its definition and package only. The
message shown says that collected data is not deleted, and it is not.

## 4.3 Questionnaire rendering and question types

The survey screen (`lib/screens/survey_screen.dart`) shows one question at a time, and keeps
one map of answers for the record as its single source of truth. The question types are:

- text, including numeric and decimal entry with masks;
- date and date-time;
- single choice (radio) and multiple choice (checkbox);
- drop-down (combobox);
- information screens;
- automatic fields, which have no user interface.

Response options come from the XML, from a CSV file in the package
(`csv_data_service.dart`), or from records already on the device
(`database_response_service.dart`), filtered by earlier answers where defined. "Don't know"
and "Refused" are offered where the definition includes them.

## 4.4 Edit checks

| Check | Behaviour | Implementation |
|:---------------|:-----------------------------------------------------------|:----------------------------|
| Answer required | The Next button stays disabled until the question is answered, unless the definition marks it optional. | `AnswerValidationService.isAnswered`, `canProceed` |
| Range and format | Numeric ranges, decimal places, maximum length and date ranges; an invalid entry shows a message and blocks moving on. | `numeric_validation_service.dart`, `answer_validation_service.dart`, `widgets/input_formatters.dart` |
| Logic check | Cross-field conditions with AND/OR and parentheses, comparing answers with each other or with constants; a failed check shows its message and blocks moving on. | `logic_service.dart`, `field_comparator.dart` |
| Skip logic | Preskip before a question and postskip after it; jumps to the target field. On save, answers to questions not visited on the final path are cleared, except key fields and automatic fields. | `skip_service.dart`, `answer_storage_service.dart` (`clearSkippedAnswers`) |
| Unique value | A field declared unique is checked against existing records. | `survey_loader.dart` (`unique_check`), `db_service.dart` |
| Duplicate record | A new record whose key fields match an existing record is refused. | `duplicate_key_service.dart` |

## 4.5 Identifier generation

Participant and record identifiers are built from the form's ID configuration in the forms
list. The configuration combines fixed text, values of earlier fields, and a zero-padded
counter taken from the highest value already in that form's table
(`lib/services/id_generator.dart`). Child records in repeating groups are numbered by
`child_increment_service.dart` and linked to their parent through the configured linking
field.

## 4.6 System variables

Automatic fields are computed when navigation reaches them (`lib/services/auto_fields.dart`).
SurveyGen places them so that each one records the right moment:

| Variable | Content | When computed |
|:------------|:-----------------------------------------------|:-------------------------------------|
| starttime, startdate | Interview start | Before the first question |
| uniqueid | Globally unique record identifier (UUID) | After the last question |
| swver | Product and version, e.g. "DataKollecta 1.4.1+19" | After the last question |
| survey_id | The package's survey identifier | After the last question |
| stoptime | Interview end | After the last question |
| lastmod | Time of last modification | After the last question, and refreshed whenever the record is saved again |

## 4.7 Local storage and schema

Each survey has one SQLite database, named by its `databaseName`, with one table per form.
Its columns are the form's field names. When a survey is opened, the table schema is
reconciled with the definition (`DbService._syncSurveyTable`). Missing tables are created,
and new fields are added as columns. Existing columns and data are never removed.

When a record is updated, only the fields that changed are written. A field cleared on
purpose is written as an explicit empty value, so a cleared answer cannot reappear.

## 4.8 Edit mode and the device audit trail

A saved record can be reopened and edited. On save, each changed field is compared with its
original value (`change_summary_service.dart`, `answer_equality.dart`), and one row per
changed field is written to the survey's `formchanges` table. Each row contains:

- the form and field;
- the record's `uniqueid`;
- the old and new values;
- the time of the change (`changed_at`, the device's local time);
- the user identifier;
- a unique `changeuniqueid`.

When a key field changes, child records are updated through database triggers
(`survey_table_schema.dart`). The triggers also write `formchanges` rows, so cascaded changes
are recorded too.

Any edit clears the record's synchronised flag, so the record is uploaded again with the
change rows.

*Known limitation (DK-VAL-002, R-01): the application does not ask for a reason for change,
and does not record the time zone or UTC time of the change.*

## 4.9 Local backup log

Every insert and update is also appended, as a SQL statement, to a plain-text log for each
table (`lib/services/db_backup.dart`, folder `DataKollecta/backups/<surveyId>/`). It is for
manual recovery if a device database is damaged. The application never reads it, and a
failure to write it does not stop the save.

## 4.10 Security on the device

- **Sync passwords and tokens** are held in the platform's secure storage: Keystore-backed
  encrypted storage on Android, and operating-system data protection on Windows. On macOS and Linux they are held in application preferences
  instead (DK-VAL-002, R-07); those platforms are not approved for data collection.
- **Survey databases** are not encrypted by the application. They rely on the operating
  system's storage encryption (R-07).
- **No in-app login.** The application has no login of its own (R-06). The user identifier
  recorded on server-side data comes from the field credential used to synchronise.

# 5. Synchronisation

## 5.1 Device authentication (app-login)

Field credentials (project code, username, password) are created by project Owners or
Editors in the portal. Passwords are stored as bcrypt hashes with cost 12. Older hashes are
upgraded at the next successful login.

`app-login` checks the credential through a database function callable only by the server
(`verify_app_credential`). That function always performs exactly one bcrypt comparison, so a
response does not reveal whether the username exists. Every failure returns the same HTTP
401 response.

Lockout: after 10 failed attempts for a username, or 50 from one network address, within 15
minutes, further attempts are refused until the window passes.

On success, the function issues a random session token valid for 30 days, and returns the
project's surveys.

## 5.2 Sessions and revocation

On every call, `app-sync` checks that:

- the token exists and has not expired;
- its credential is still active;
- the project is active (not paused or archived).

If any check fails, the response is 401. The ways to revoke a device are:

- disabling the credential;
- resetting its password, which deletes all of that credential's sessions;
- pausing or archiving the project.

When a token is refused, the application signs in again with the stored credential. If the
password has been reset, the application shows that the credential must be updated in
Settings. The stored credential is replaced only after the server accepts the new one
(release 1.4.1). Unsynchronised data stays on the device throughout.

## 5.3 Upload (app-sync)

`lib/services/sync/record_uploader.dart` uploads unsynchronised records in batches, walking
each table in a strictly increasing row order. It then uploads change-history rows.

- **Marking as synchronised.** A row is marked synchronised only after the server lists it as
  saved; failed rows stay pending.
- **Stopping.** The uploader stops after a set number of consecutive failures, or when the
  server asks it to slow down, and resumes at the next sync.
- **Batch size.** The server accepts at most 500 rows per request.

On the server, records are stored with an upsert on the project, form and local unique ID.
Re-sending a record therefore updates it rather than duplicating it. Change rows are stored
by `formchanges_uuid`:

- an exact re-send is accepted and changes nothing;
- a re-send with any value altered is refused.

The server sets the uploader's identity (`surveyor_id`) from the authenticated session and
ignores any value the device sends. It also records the device identifier.

Each record's data status (*test* or *deployed*) is set on first receipt from the survey's
stage at that moment, and later re-sends do not change it (section 6.6). If the project's
data is locked, records and change rows are refused and stay on the device (section 6.7).

## 5.4 Survey download

The survey list returned at login contains only the project's Test and Deployed surveys. Each
package is downloaded through a signed storage URL that expires after 24 hours.

## 5.5 Project binding

A device can hold surveys from several projects. `lib/services/sync/project_sessions.dart`
records which project each survey came from, and sends uploads with that project's session.
A survey whose identifier or database name is already bound to a different project is
refused (`ProjectAssociationConflict`), because both names are storage keys on the device,
and a collision would mix two projects' records in one database.

# 6. Web portal and server

## 6.1 Portal accounts

Portal users sign in with an e-mail address and password through Supabase Auth. The
authentication settings are committed in `supabase/config.toml` and applied with the
Supabase CLI:

| Setting | Value |
|:-------------------------------------|:-------------------------------------------|
| E-mail confirmation | Required |
| Minimum password length | 10 characters, with no composition rules (`src/lib/passwordPolicy.ts`) |
| Password change | Requires re-authentication (`secure_password_change`) |
| Access token lifetime | 1 hour; refresh tokens are rotated |
| Sign-in rate limits | Enabled |
| Open sign-up | Enabled; a new account has no project access (DK-VAL-002, R-04) |
| TOTP multi-factor authentication | Enabled on the server; no enrolment screen in the portal (R-02) |
| Session inactivity timeout | Not configured (R-03) |

## 6.2 Roles and row-level security

Access is per project. Each member has one role, Owner, Editor or Viewer, with the
permissions shown below (also published in the portal help, *Roles and permissions*).

| Action | Owner | Editor | Viewer |
|:-----------------------------------------------------|:-:|:-:|:-:|
| See the project, members, field team, surveys and records | ✓ | ✓ | ✓ |
| Export data | ✓ | ✓ | ✓ |
| Create, upload, version and deploy surveys | ✓ | ✓ | |
| Manage field credentials | ✓ | ✓ | |
| Manage members and roles | ✓ | | |
| Pause, archive, lock or unlock the project | ✓ | | |
| Reclassify or purge test records | ✓ | | |
| Manage data-feed keys | ✓ | | |

These permissions are enforced in the database by row-level security on every table, and by
security-definer functions for privileged actions. They are not just hidden in the user
interface. A user who is not a member of a project can read nothing of it.

**No editing of collected data.** No portal role has insert, update or delete rights on
collected records (`submissions`) or change history (`formchanges`). Those rights were
withdrawn in migration `20261005090000`. Data enters the server only through app-sync.

## 6.3 Projects

A project is *active*, *paused* or *archived*. Pausing or archiving stops all device
synchronisation (section 5.2). A project that holds records or audit history cannot be
deleted (`prevent_collected_data_destruction`); it can only be archived.

## 6.4 Survey lifecycle and storage

A survey moves through the stages Draft, Test, Deployed and Complete. Deployed and Complete
surveys cannot be edited.

Package files are kept in a storage bucket whose policies (migration `20261008120000`)
allow:

- reading only by members of the owning project;
- uploading only by Owners and Editors;
- no overwriting or deleting of a deployed survey's package.

## 6.5 Viewing data

The Data page lists records by form, showing deployed records by default. Each record shows:

- its values;
- its device edit history (from `formchanges`);
- its server history (from the audit trail, section 7.2).

## 6.6 Test and deployed records

Each record's `data_status` is set when the server first receives it: *test* if its survey was
then in the Test stage, *deployed* if it was Deployed (migration `20261006090000`). An
Owner can correct the label with a reason (`reclassify_submissions`), and the change is
audited.

## 6.7 Data lock

An Owner can lock a project's data with a reason (`set_project_data_lock`). While locked, the
database refuses inserts and updates to records and change history. A device's pending
uploads are refused and stay on the device until an Owner reopens the data, also with a
reason. Locks are recorded in `project_data_locks` and in the audit trail.

## 6.8 Purging test records

An Owner can permanently remove *test* records (migration `20261008150000`), subject to these
conditions:

- **Who and when.** It requires a reason and is refused while the data is locked.
- **Deployed records.** A deployed record must first be reclassified as test, with a reason.
- **What is kept.** The full content of each purged record is kept in the audit trail and in
  `purged_submissions`.
- **Re-sent records.** If a device later re-sends a purged record, it is discarded and
  logged (`DISCARD_PURGED`).

No other route can delete a record, including the server's own functions and direct
database sessions.

## 6.9 Export

The export (`src/components/project/ProjectData.tsx`, `src/lib/exportManifest.ts`) produces a
ZIP file containing:

- one CSV file per form;
- `formchanges.csv`: the device change history;
- `project_audit.csv`: the whole project's server audit trail;
- `manifest.json`.

The manifest gives:

- an export identifier, creation time, project and scope;
- the portal version and build commit;
- for every file, its size and SHA-256 checksum, computed over the exact bytes written.

The manifest is also written to the audit trail as an `EXPORT` event, so the existence and
content of every export can be proven later. A data manager can re-compute the checksums
with any standard tool.

## 6.10 Data feeds

Owners can create read-only API keys for one project (`project-data-feed`, migration
`20261008090000`). Key rules:

- **Storage.** Keys are shown once and stored only as a SHA-256 hash.
- **Limits.** A key can have an expiry date and can be revoked. At most 20 can be active per
  project.
- **Auditing.** Creation, revocation and every read are audited.

# 7. Audit trail

## 7.1 Device change history

This is described in section 4.8. On the server, change rows are stored in `formchanges` with
a unique `formchanges_uuid` and are protected by a trigger
(`protect_device_audit_history`) that refuses deletion and any rewrite. An exact re-send is
accepted.

## 7.2 Server audit trail

Database triggers write a row to `system_audit_events` for every insert, update and delete
on the audited tables:

- collected records;
- project members;
- field credentials;
- data locks;
- projects;
- survey packages;
- forms.

Each row holds:

| Column | Content |
|:--------------------|:-----------------------------------------------------------------|
| occurred_at | Server time of the change, with time zone (`clock_timestamp()`) |
| project_id, entity_type, entity_id | What was changed |
| operation | INSERT, UPDATE, DELETE, or a named action such as EXPORT, PURGE, DISCARD_PURGED |
| actor_user_id | The portal user, when the change was made by a signed-in user |
| actor_database_role | How the change arrived: portal user, server function (for example a device sync), or a direct database session |
| uploader_username | The field credential, for changes arriving from devices |
| old_values, new_values | The values before and after (password hashes and tokens excluded) |
| reason | The reason given, for actions that require one |

Changes that touch only internal bookkeeping timestamps are not recorded.

The server audit trail began with migration `20261005090000` (5 October 2026). Earlier
activity was not reconstructed (DK-VAL-002, R-11).

## 7.3 Protection of the audit trail

- **Update and delete.** Triggers refuse any update or delete on `system_audit_events`
  (`protect_system_audit_events`) and on `formchanges`.
- **Bulk empty.** Statement-level triggers refuse TRUNCATE on `system_audit_events`,
  `formchanges` and `submissions` (migration `20261005100000`).
- **Grants.** No role is granted update or delete on the audit table, and portal users can
  only read the events of projects they belong to.
- **Residual risk.** A database administrator could still disable a trigger; that is a
  schema change, visible in migration history and platform logs (DK-VAL-002, R-10).

## 7.4 Review

The audit trail is reviewed per record in the portal (section 6.5), and for a whole project
through `project_audit.csv` in the export (section 6.9). Periodic review of the audit trail is
a procedural control (DK-SOP-001, section 6).

## 7.5 Time

Server timestamps come from the database server's clock, which is synchronised by the
hosting provider, and are stored with time zone. Device timestamps (interview times,
`changed_at`) are the device's local wall-clock time and are stored as recorded. The server
also records its own receipt time, in UTC, for each record (`submitted_at`) and change row
(`synced_at`).

# 8. Backup and recovery

## 8.1 Platform backups

The hosting provider takes database backups according to the plan in use. The plan,
retention and point-in-time recovery setting are recorded at IQ-07 (DK-VAL-002, R-13).

## 8.2 Scheduled CSV backup

`export_data.py` (DataKollecta-DataBackup) runs on a schedule on an organisation computer.
For each project it writes each form's CSV and `formchanges.csv` into a timestamped folder.
It retries failures three times, logs to `backup.log`, e-mails a summary, and exits with
an error status on failure. It does not include the server audit trail (R-12).

## 8.3 Encrypted snapshot

`backup_snapshot.py create` takes a full database dump and every stored file. It writes a
SHA-256 manifest of every file (`snapshot_integrity.py`), packs everything into one archive,
and encrypts it with GnuPG. An approved key recipient is required for real data. It then
writes a receipt containing the archive's checksum.

## 8.4 Verified restore

`backup_snapshot.py restore-local` restores a snapshot only into an empty, explicitly named
database on the local machine. Before restoring, it checks:

- the archive against its receipt;
- every file against the manifest.

It refuses a tampered, missing or extra file, unsafe paths and links, and remote or system
databases. The restore runs in a single transaction. Recovery of the production platform
itself is done through the provider and recorded on the Restore Test Record (DK-SOP-001,
Appendix E).

# 9. Version identification and release

| Component | Version scheme | Where the version is visible |
|:--------------|:---------------------------|:------------------------------------------------------|
| Field application | X.Y.Z+B in `pubspec.yaml`; B is a build counter that is never reused; release tag vX.Y.Z+B | Settings screen; `swver` on every record; package file name `datakollecta-X.Y.Z-buildB.apk` |
| Portal, server functions and database | X.Y.Z in `package.json`, one version for all three; tag web-vX.Y.Z; the change log records the migration head | Portal sidebar (version and commit); every export manifest |
| SurveyGen, SurveyTest, DataBackup | Git commit identifier | Recorded on the Study Build Validation Record and backup receipts |

Releases follow the change-control procedure in DK-SOP-001, section 4.

# 10. Hosting

| Function | Provider | Notes |
|:-----------------|:------------|:---------------------------------------------------|
| Database, authentication, file storage, server functions | Supabase | One production project; details recorded at IQ-07 |
| Portal web files | Vercel | Built and deployed from the main branch of DataKollecta-Web; security headers deny framing and content-type sniffing |
| Source code and releases | GitHub | One repository per component |

All traffic uses HTTPS. The portal holds no data of its own; the browser talks directly to
Supabase, subject to row-level security.

# 11. Interfaces

| Interface | From → To | Protocol and format | Controls |
|:-------------------|:------------------|:--------------------------|:-------------------------------------------|
| Device login | Field app → app-login | HTTPS, JSON | Section 5.1 |
| Upload | Field app → app-sync | HTTPS, JSON, at most 500 rows per request | Sections 5.2, 5.3 |
| Survey download | Field app → Storage | HTTPS, signed URL, ZIP | Section 5.4 |
| Portal | Browser → Supabase | HTTPS, REST and Auth APIs | Sections 6.1, 6.2 |
| Export | Portal → user | ZIP of CSV and JSON manifest | Section 6.9 |
| Data feed | External system → project-data-feed | HTTPS, JSON, API key | Section 6.10 |
| Survey build | SurveyGen → portal | ZIP package, uploaded by a user | Sections 3.1, 6.4 |
| Backup | Supabase → organisation storage | PostgreSQL protocol over TLS; files | Section 8 |
