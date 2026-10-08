---
doc_id: DK-SOP-001
title: System Management SOP
version: "1.0"
orientation: portrait
approvers:
  - [Author, System Owner / Lead Developer]
  - [Reviewer, Quality Assurance]
  - [Approver, Head of Data Management]
---

# 1. Purpose

This standard operating procedure (SOP) defines how the DataKollecta system is operated and
maintained so that it stays in a validated state throughout its life. It covers:

- change control and release;
- user access;
- audit-trail review;
- backup and recovery;
- incidents and support;
- security;
- the release of study configurations;
- periodic review;
- training;
- retention and decommissioning.

One SOP covers all of these so that the procedures stay consistent with each other. The forms
needed to record each activity are in the appendices.

# 2. Scope

This SOP applies to every component of the DataKollecta system listed in the Validation Plan
(DK-VAL-001), in production, and to everyone who develops, administers or uses it.
Study-specific procedures, such as data management plans and data query processes, are
outside its scope. This SOP refers to them where they connect.

# 3. Responsibilities

| Role | Responsibilities under this SOP |
|:-------------------------|:-------------------------------------------------------------------|
| **System Owner** | Accountable for the system and its validated state. Approves changes and releases; ensures that reviews, backups and restore tests happen; keeps the validation package current. |
| **Developer** | Makes changes under change control, runs the automated tests, prepares releases, documents changes. |
| **Quality Assurance (QA)** | Independently reviews changes, test evidence and periodic reviews; approves Major changes; follows up CAPAs. |
| **System Administrator** | Administers the hosting accounts; runs backups and restore tests; applies platform and security settings. Must not take part in entering or changing study data. |
| **Project Owner** (portal role) | Manages a project's members and field credentials; locks and unlocks data; carries out access and audit-trail reviews for the project. |
| **Data Manager** | Completes the Study Build Validation Record; reviews data and audit trails; runs exports. |
| **All users** | Use their own accounts only; keep passwords confidential; report incidents and defects without delay. |

# 4. Change control and release

## 4.1 What is a change

A change is anything that alters the system's software, configuration or environment. That
includes:

- application, portal or server-function code;
- database migrations;
- authentication or hosting settings;
- the survey and backup tools;
- the hosting plan or provider;
- the procedures in this SOP.

Study configurations (survey packages) are controlled separately under section 10.

## 4.2 Classification

| Class | Examples | Required |
|:-------------|:------------------------------------------|:--------------------------------------------------|
| **Minor** | Wording, layout or help-text changes with no effect on data; documentation | Change log entry; review by a second person; automated suites relevant to the component |
| **Standard** | New or changed functions; bug fixes; dependency upgrades | Change Request (Appendix A) with impact assessment; all automated suites (AT-01 to AT-10) for the affected components; the manual OQ test cases for the affected requirements; QA review |
| **Major** | Changes to the audit trail, access control, authentication, synchronisation, data storage, export or backup; database schema changes affecting collected data; a new platform or provider | As Standard, plus a written test plan approved by QA before testing, re-execution of all High-risk test cases for the affected area, an update to DK-VAL-002 and DK-VAL-003, and a Validation Summary Report addendum approved before release |
| **Emergency** | A fix needed at once to stop data loss, a security breach or an outage | May be released after the Developer's own testing and the System Owner's approval. The full change record, testing and QA review must follow within 5 working days. |

## 4.3 Procedure

1. **Request.** Record the change on a Change Request (Appendix A): what, why, the
   components affected, and the classification.
2. **Impact assessment.** Assess the effect on:
   - the requirements (DK-VAL-002), including their risk ratings;
   - data already collected (for example, whether a schema change preserves existing
     records);
   - studies in progress;
   - documentation and training.
3. **Develop.** Make the change on a branch in the component's repository. Every change is
   committed with a description; nothing is changed directly in production except as part
   of a release (section 4.4).
4. **Test.**
   - Run the automated suites required by the classification on the commit to be released.
     Keep their logs.
   - Execute the manual test cases required, using the forms in DK-VAL-004.
   - Record failures as deviations.
5. **Review and approve.** A person other than the developer reviews the change and its
   test evidence. The System Owner approves release (and QA, for Major changes).
6. **Release** (section 4.4), then update the validation documents and training material as
   identified in step 2.
7. **Notify** the Project Owners and data managers of active studies of any change that
   affects how they use the system, before or at release.

## 4.4 Release and version identification

Each release is identified by a unique version (DK-VAL-003, section 9):

- **Field application.**
  1. Rename the `[UNRELEASED]` heading in `ChangeLog.md` to the version and date.
  2. Bump the build number.
  3. Build every product and flavor from the same commit, without a further bump.
  4. Commit the version files, and tag `vX.Y.Z+B`.
  5. Record the SHA-256 checksum of each distributed package file on the Change Request.
- **Portal, server functions and database.**
  1. Rename `[Unreleased]` in `CHANGELOG.md` to the version and date, and record the
     migration head.
  2. Set the version in `package.json`.
  3. Commit, and tag `web-vX.Y.Z`.
  4. Apply database migrations (`supabase db push`) **before** pushing to the main branch,
     because the portal deploys automatically from that branch.
  5. Deploy any changed server functions.
  6. Push the main branch and the tag.
  7. Check the sidebar version and commit in production.
- **Survey tools and backup tools.** Record the commit in use on the Change Request, and on
  any Study Build Validation Record or Restore Test Record made with them.

The **version history** of every component (repository history, tags and change logs) is
kept for the life of the system and for the retention period in section 13.

## 4.5 Configuration changes

Authentication and other server settings are kept in the committed file
`supabase/config.toml`. They are changed only by editing that file under this procedure, then
applying it.

Before applying, compare the file with the live settings and record the differences on the
Change Request. After applying, check the live settings again. This control was introduced
after the 4 September 2026 incident (DK-VAL-002, R-20).

Hosting-account settings that are not in a file (plan, backups, administrators) are recorded
on the Change Request when changed.

## 4.6 Distributing the field application

Install packages only from the release build recorded on the Change Request. Record the
version installed on each device in the device register (section 9.3). A device must be
upgraded before the old version is withdrawn, and only after the device's pending records
have been synchronised.

# 5. User access management

## 5.1 Portal accounts

- **Individual accounts.** Every person has their own account, registered with their own
  e-mail address. Shared or generic accounts are not allowed.
- **Granting access.** A Project Owner adds a person to a project only when:
  - the person is authorised to work on the study (for example, on the delegation log);
  - they have been trained (section 12);
  - the study's approvals are in place.
- **Least privilege.** Give each person the lowest role that lets them do their work: Viewer
  for monitors, statisticians and data reviewers; Editor for survey designers and field
  coordinators; Owner for the principal investigator or study manager. Each project should
  have at least two Owners. Every role can export all data (DK-VAL-002, R-18), so only add
  people who are allowed to see the study's data.
- **Changes and removal.** When someone's role changes or they leave, the Project Owner
  changes or removes their access within **2 working days**, and the same day for a
  dismissal or a suspected compromise.

## 5.2 Field credentials

- **One credential per person.** Each interviewer has their own field credential; the
  username identifies the person. Credentials are not shared. If a device is shared between
  interviewers, each signs in with their own credential; the handover is recorded in the
  device register.
- **Passwords.** Field passwords are given to the interviewer in person or through a
  separate channel, not written on the device.
- **Leavers and lost devices.** When an interviewer leaves, or a device is lost or stolen,
  the credential is **reset or disabled the same day**. Resetting signs out every device
  using it immediately.

## 5.3 Administrator access

- **Who.** Administrative access to the hosting accounts (Supabase, Vercel, GitHub) is limited
  to named System Administrators and Developers, listed on the Periodic Review record.
- **MFA.** Multi-factor authentication is mandatory on all of them.
- **Separation from study data.** Administrators must not use administrative access to view
  or change study data, except to investigate an incident, which is then recorded on an
  Incident Record. Direct database changes to study data are forbidden. A correction to
  collected data is made on the device and travels through synchronisation, so that it is
  audited.

## 5.4 Access review

**Each Project Owner, every 3 months for active projects:**

1. Compare the Members list and the Field team list with the study's delegation log.
2. Remove or disable anything not justified.
3. Record the review on an Access Review Record (Appendix B).

**The System Owner, at the periodic review (section 11):** review the administrator accounts.

# 6. Audit-trail review

1. **When.** The Data Manager reviews each active project's audit trail every month during
   data collection, and once more before the data is locked for analysis. Review is
   risk-based: it concentrates on changes to critical data (eligibility, consent, primary
   endpoints, safety data, identifiers).
2. **How.** Export the project's data (DK-VAL-003, section 6.9) and review `formchanges.csv`
   and `project_audit.csv`. Look for:
   - edits to records after they were first uploaded, especially to critical fields;
   - edits made long after the interview, or by an interviewer other than the original one;
   - unusual patterns, such as one user making many changes, or changes at unusual times;
   - reclassifications, purges, data locks and unlocks, and their reasons;
   - access changes (members, roles, field credentials) and data-feed key activity.
3. **Device edits** carry no reason for change (DK-VAL-002, R-01). Until that is corrected:
   - every correction to data that has already been uploaded must be requested through the
     study's data query process, which records the reason;
   - the reviewer reconciles each post-upload device edit against a resolved query.
4. **Findings.** An edit with no corresponding query is followed up with the interviewer and
   documented. A suspected falsification, or an unexplained or unauthorised change, is an
   incident (section 8).
5. **Record.** Record the review (date, period covered, reviewer, findings, actions) in the
   study's data management file.

# 7. Backup, restore and disaster recovery

## 7.1 Backups

| Backup | Tool | Frequency | Kept |
|:-----------------|:------------------------------|:-----------------------------|:---------------------------|
| Platform database backup | Hosting provider | As provided by the plan (recorded at IQ-07) | Per plan |
| Scheduled CSV export of every project | `export_data.py` (DataBackup) | Daily | At least 90 days of dailies, plus the last of each month for the life of the system |
| Encrypted full snapshot (database and files) | `backup_snapshot.py create` | Weekly; before every release; at every database lock | The last 8 weeklies; every pre-release and database-lock snapshot for the retention period |

**Storage.**

- Backups are stored on organisation-controlled storage that is independent of the hosting
  provider, with access limited to the System Administrators.
- Snapshots are encrypted with the organisation's approved backup key. The private key is
  held by two named people and stored securely, separately from the backups.
- The scheduled export e-mails a summary after every run. A **failed backup** is
  investigated on the same working day and recorded as an incident if it cannot be fixed at
  once.

## 7.2 Restore testing

At least **every 6 months**, and after any change to the backup tools or hosting plan, a
System Administrator restores the latest snapshot locally (`backup_snapshot.py
restore-local`). They reconcile record counts with production, test the restore of the
latest CSV export, and record it all on a Restore Test Record (Appendix E).

## 7.3 Disaster recovery

If the production service is lost or its data is damaged:

1. Declare an incident (section 8), stop data collection uploads if needed (pause the
   affected projects), and notify the Project Owners.
2. Field devices keep all unsynchronised data safely. Instruct interviewers to keep
   collecting and **not** to remove surveys or the application.
3. Recover through the hosting provider's backup or point-in-time recovery. If that is not
   possible, recover from the latest snapshot into a new production project, apply
   configuration from the repository, and redeploy the portal and server functions.
4. Verify the recovered system with IQ-03 to IQ-05, and reconcile record counts against the
   last export.
5. Resume synchronisation. Devices upload anything received after the recovery point. The
   upload is idempotent, so records are neither duplicated nor lost.
6. Record the recovery on the Incident Record and a Restore Test Record.

# 8. Incidents, defects and user support

1. **Reporting.** Users report problems, suspected defects and security concerns to the
   support contact published in the portal help (*Support*) or to the System Owner. Field
   staff report through their supervisor.
2. **Recording.** Every report is recorded on an Incident / Defect Record (Appendix C), or
   in the issue tracker of the affected repository with the same information, and given a
   number.
3. **Classification.**

| Class | Meaning | Target response |
|:----------|:-----------------------------------------------------------|:---------------------------|
| Critical | Possible data loss or corruption; security breach or suspected unauthorised access; failure of the audit trail; total outage | Start the same day; System Owner and QA informed at once |
| Major | A function not working, with a workaround | Start within 2 working days |
| Minor | Cosmetic or documentation | Next planned release |

4. **Investigation.** Investigate the cause. Assess the effect on data already collected
   and on studies in progress. Agree corrective and preventive actions (CAPA). Fixes are
   made under change control (section 4).
5. **Security incidents and personal data breaches.** A suspected breach, including a lost or
   stolen device holding unsynchronised data, is reported at once to the System Owner and
   the organisation's data protection officer. It is also reported to the study sponsors
   affected, in time for them to meet their own reporting obligations (normally within 24
   hours). The credential of a lost device is reset at once (section 5.2).
6. **Closure.** An incident is closed when its CAPAs are complete and their effectiveness
   has been checked. Incidents are reviewed at each periodic review for trends.

# 9. Security and platform management

## 9.1 Passwords and authentication

- **Portal passwords** must be at least 10 characters, unique to DataKollecta, and kept in a
  password manager. They must never be shared or written down.
- **Shared browsers.** Users must not let a browser save their portal password on a shared
  or personal computer they do not control.
- **Administrators** use MFA on all hosting accounts (section 5.3). Until MFA enrolment is
  available in the portal (DK-VAL-002, R-02), Project Owners must use a password manager
  with a unique generated password.

## 9.2 Workstations

Computers used to access the portal or run the survey and backup tools must:

- run a supported operating system with security updates applied;
- run current anti-virus software;
- lock the screen after at most **10 minutes** of inactivity (DK-VAL-002, R-03).

Users must sign out of the portal when they finish on a shared computer. USB drives used to
move survey packages or exports must be organisation-owned and scanned for malware.

## 9.3 Field devices

Devices used for data collection must:

- run a supported Android version (or Windows with full-disk encryption) and receive
  security updates;
- have a screen lock with PIN or password. This also activates the operating system's storage
  encryption (DK-VAL-002, R-06 and R-07);
- have automatic network date, time and time zone switched on (R-17);
- not be rooted or jail-broken;
- have the DataKollecta application installed only from the release build (section 4.6).

The System Administrator keeps a **device register**: device, serial number, assigned
interviewer, application version installed, and dates of issue, handover and return.

Interviewers synchronise **at least daily** when a connection is available, so that as
little data as possible is held only on the device.

macOS, Linux and iOS builds of the field application are not used for production data
collection.

## 9.4 Platform and provider management

The System Owner:

- monitors the hosting providers' status pages and change notices;
- assesses any platform change that could affect the system, and handles it as a change or
  an incident;
- keeps provider terms, data-processing agreements and security attestations on file, and
  reviews them at each periodic review;
- applies dependency and platform updates through change control.

Security updates rated critical by the vendor are assessed within 5 working days.

# 10. Study configuration: build, validation and release

Each study's survey is validated before it is used to collect real data, and again for each
protocol amendment that changes it:

1. **Specification.** The Data Manager prepares the data dictionary from the protocol and
   the case report forms, and has it reviewed by a second person against them.
2. **Build.** Build the package with SurveyGen (or the portal designer). The build must
   complete with no errors; every warning is assessed.
3. **Test.**
   - Run SurveyTest on the package and resolve or justify every finding.
   - Upload the package to the project and promote it to **Test**.
   - Carry out the user acceptance test on a device, following the checklist in DK-TPL-001.
   - Involve at least one future user (for example a field supervisor).
4. **Record.** Complete the Study Build Validation Record (DK-TPL-001) and have it signed.
5. **Release.** Only then promote the survey to **Deployed**. Records collected during
   testing remain labelled *test* and can be purged by the Owner (with a reason) before
   deployment.
6. **Amendments.**
   - Make each change as a **New Version** of the survey, keeping the same database name
     (DK-VAL-003, section 3.4).
   - Validate it with a new DK-TPL-001 record that refers to the previous one.
   - Deploy it only once the amendment has the necessary approvals.
   - Inform the investigators and field teams of the change and its effective date.

# 11. Periodic review

Every **12 months**, and after any Major incident, the System Owner and QA review whether the
system is still in a validated state. They record the result on a Periodic Review Record
(Appendix D). The review covers:

- changes made since the last review, including the hosting platforms, and their
  documentation;
- deviations, incidents and CAPAs, and any recurrence;
- the residual risk register (DK-VAL-002, section 5): progress of corrections, and any new
  risk;
- security: administrator accounts and MFA, security incidents, provider attestations;
- access reviews done during the period;
- backups and restore tests done during the period;
- the audit-trail protection check: run the query in Appendix G and confirm the result;
- whether the requirements still describe how the system is used, including new uses or new
  regulations;
- training records.

The review concludes either that the system remains validated, or what revalidation is
needed.

# 12. Training

Before anyone is given access, they are trained in the parts of the system and of this SOP
relevant to their role:

| Role | Training content |
|:--------------------|:-------------------------------------------------------------------------|
| Interviewer | The field application: data entry, edit checks, editing, synchronising; device security; reporting problems |
| Field supervisor | As interviewer, plus the device register and credential handover |
| Data Manager | Portal data pages, export and manifest checking, audit-trail review, study build (section 10) |
| Project Owner | Members, roles and field credentials; data lock, reclassification and purge; access review |
| Developer, Administrator | This whole SOP and the validation package |

Training uses the portal's built-in help (*Documentation*) and the study's own materials.
Training is recorded on a Training Record (Appendix F) or the organisation's training
system, and repeated when a release changes how a role works.

# 13. Record retention, archiving and decommissioning

1. **Retention.** Study data, its audit trails, exports with their manifests, and the
   validation records of every system version used for a study are kept for at least as long
   as that study's essential records must be kept. That period is set by the sponsor,
   protocol and applicable law. It must not be shorter than the longest such period of any
   study whose data the system holds.
2. **At the end of each study:**
   1. Lock the project's data with a reason.
   2. Make a final export and verify its manifest checksums.
   3. Take a final encrypted snapshot.
   4. Archive the project in the portal.
   5. Keep the export, manifest and snapshot receipt in the study file.
3. **Readability.** Archived exports are kept in open formats (CSV and JSON) so that they
   stay readable without the system. Snapshots are tested as part of restore testing.
4. **Decommissioning the system** (or moving to another one):
   1. Make a final export and snapshot of every project, and verify them by a restore.
   2. Keep them, the validation package and the source code repositories for the retention
      period.
   3. Remove all user access.
   4. Close the hosting accounts only when the data and documentation are safely retained
      elsewhere.
   5. Record the decommissioning as a Major change.
5. **Validation documentation** of current and previous versions is kept with the source
   code (the validation repository) and as signed copies in the quality records.

# 14. Records

Records made under this SOP are kept as signed paper originals or as signed electronic
documents. Each is filed under its form number and date, in the quality records for the
system, and kept for the retention period in section 13.

| Record | Form | Kept by |
|:------------------------------------|:-------------|:-------------------|
| Change Request and Release Record | Appendix A | System Owner |
| Access Review Record | Appendix B | Project Owner (project file) |
| Incident / Defect Record | Appendix C | System Owner |
| Periodic Review Record | Appendix D | System Owner / QA |
| Restore Test Record | Appendix E | System Administrator |
| Training Record | Appendix F | Line manager / training system |
| Study Build Validation Record | DK-TPL-001 | Data Manager (study file) |
| Audit-trail review | Data management file | Data Manager |
| Device register | Section 9.3 | System Administrator |

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Appendix A. Change Request and Release Record

| Field | Entry |
|:--------------------------------------|:-----------------------------------------------|
| Change number | CR- |
| Requested by, date | |
| Component(s) affected | ☐ Field application ☐ Portal ☐ Server functions ☐ Database ☐ Auth or hosting configuration ☐ SurveyGen ☐ SurveyTest ☐ DataBackup ☐ Procedure |
| Description of the change and reason | |
| Classification (section 4.2) | ☐ Minor ☐ Standard ☐ Major ☐ Emergency |
| Impact assessment: requirements (URS IDs) and risk ratings affected | |
| Impact on data already collected and on studies in progress | |
| Documents and training to update | |
| Testing required (AT, OQ and PQ IDs) | |
| Approved to proceed (System Owner; QA if Major): name, signature, date | |
| Repository, branch and commit released | |
| Automated test results (suites, counts, log file names) | |
| Manual test results (test IDs, Pass/Fail, deviation IDs) | |
| Configuration differences checked before and after applying (section 4.5) | |
| Version released and tag | |
| Package checksums (field application) | |
| Released to production: date and by whom | |
| Users notified (who, date) | |
| Reviewed (independent reviewer): name, signature, date | |
| Approved for release (System Owner; QA if Major): name, signature, date | |

# Appendix B. Access Review Record

| Field | Entry |
|:------------------------------|:-------------------------------------------------------|
| Project | |
| Review period | |
| Members reviewed (total) | |
| Field credentials reviewed (total, active and disabled) | |
| Compared against (delegation log or staff list, version or date) | |

| Account or credential | Role or status found | Justified? (Y/N) | Action taken | Date of action |
|:---------------------------|:------------------|:-------------|:-----------------------|:------------|
| | | | | |
| | | | | |
| | | | | |

| Reviewed by (Project Owner): name, signature, date | |
|:---------------------------------------------------|:--|

# Appendix C. Incident / Defect Record

| Field | Entry |
|:--------------------------------------|:-----------------------------------------------|
| Incident number | INC- |
| Reported by, date and time | |
| Component and version | |
| Description (what happened, when, who was affected) | |
| Classification (section 8) | ☐ Critical ☐ Major ☐ Minor  ☐ Security / personal data breach |
| Immediate action taken | |
| Notifications (data protection officer, sponsors, others): who, when | |
| Investigation and root cause | |
| Impact on data already collected | |
| Corrective and preventive actions (CAPA), with change numbers | |
| Effectiveness check | |
| Closed by (System Owner): name, signature, date | |
| Reviewed by (QA, for Critical): name, signature, date | |

# Appendix D. Periodic Review Record

| Review item (section 11) | Findings | Action required |
|:------------------------------------------|:--------------------------------|:----------------------|
| Period covered and versions in use | | |
| Changes made (list of change numbers), including platform changes | | |
| Deviations, incidents and CAPAs | | |
| Residual risk register (DK-VAL-002 section 5) | | |
| Administrator accounts and MFA | | |
| Provider attestations and agreements | | |
| Access reviews done | | |
| Backups and restore tests done | | |
| Audit-trail protection check (Appendix G), result | | |
| Requirements still current; new uses or regulations | | |
| Training records | | |
| **Conclusion:** ☐ remains validated ☐ revalidation needed (describe) | | |

| Reviewed by (System Owner): name, signature, date | Approved by (QA): name, signature, date |
|:--------------------------------------------------|:-----------------------------------------|
| | |

# Appendix E. Restore Test Record

| Field | Entry |
|:--------------------------------------|:-----------------------------------------------|
| Date and performed by | |
| Reason | ☐ Scheduled (6-monthly) ☐ After change CR- ☐ Recovery after incident INC- |
| Snapshot used (file name, receipt checksum, date taken) | |
| DataBackup commit used | |
| Integrity check result | |
| Target database (local, empty) | |
| Row counts: submissions / formchanges / system_audit_events (restored vs production at snapshot time) | |
| Latest CSV export opened and checked (date, project) | |
| Tamper test (altered copy refused)? | ☐ Yes ☐ Not performed (reason) |
| Problems found and actions | |
| Restored copy disposed of securely (how, when) | |
| Performed by: name, signature, date | |
| Reviewed by: name, signature, date | |

# Appendix F. Training Record

| Name | Role | Training content (section 12) and material version | Trainer | Date | Trainee signature | Trainer signature |
|:-----------------|:-------------|:------------------------------|:-----------|:---------|:------------|:------------|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

# Appendix G. Audit-trail protection check

Run this query against the production database (read-only; for example in the hosting
provider's SQL editor) at installation qualification (IQ-04) and at every periodic review.

```sql
select c.relname as table_name, t.tgname as trigger_name, t.tgenabled as enabled
from pg_trigger t
join pg_class c on c.oid = t.tgrelid
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relname in ('system_audit_events', 'formchanges', 'submissions', 'projects',
                    'project_members', 'app_credentials', 'survey_packages', 'crfs',
                    'project_data_locks')
  and not t.tgisinternal
order by 1, 2;
```

**Expected result.** At version 1.2.0 the query returns these protective and auditing
triggers, each with enabled = `O`. Other triggers may also be listed.

| Table | Triggers that must be present and enabled |
|:--------------------|:--------------------------------------------------------------------|
| system_audit_events | protect_system_audit_events, refuse_truncate |
| formchanges | protect_device_audit_history, enforce_formchanges_lock, refuse_truncate |
| submissions | audit_submission_state, enforce_submission_lock, discard_purged_submission, stamp_submission_data_status, refuse_truncate |
| projects | audit_projects, protect_project_data |
| project_members | audit_project_members |
| app_credentials | audit_app_credentials |
| survey_packages | audit_survey_packages, protect_survey_data, trg_survey_packages_delete_guard, trg_survey_packages_lifecycle |
| crfs | audit_crfs |
| project_data_locks | audit_project_lock |

Any missing or disabled trigger is a **Critical incident** (section 8). A release that
changes this list updates this appendix through change control.
