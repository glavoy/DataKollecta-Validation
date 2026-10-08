---
doc_id: DK-VAL-004
title: Test Protocol
version: "1.0"
orientation: landscape
approvers:
  - [Author, System Owner / Lead Developer]
  - [Reviewer, Quality Assurance (independent of development)]
  - [Approver, Head of Data Management]
---

# 1. Purpose and instructions

This protocol contains the pre-approved test cases that verify the DataKollecta system
against its user requirements (DK-VAL-002), following the strategy in the Validation Plan
(DK-VAL-001). It is **signed before execution**. The executed copy, with results, initials
and evidence, is the record of testing and is retained with the validation package.

**Instructions to testers**

1. **Before you start.** Complete the Version Record (section 2) and the Tester Log
   (section 3).
2. **Steps.** Carry out each step exactly as written. Record what you actually observe in
   *Actual result*. "As expected" is acceptable only when the result matches the expected
   result in every detail.
3. **Each step.** Mark it **P** (pass) or **F** (fail), and write your initials and the date.
4. **Evidence.** Where a step says *Evidence*, take a screenshot or keep the file. Name it
   `<test ID>-<step>` (for example `OQ-08-3.png`) and write the name in the Actual result.
5. **Failures.** If a step fails, do not stop. Record what happened, raise a deviation
   (DK-VAL-005, deviation log) and write its number in the Actual result. Continue if the
   remaining steps are still meaningful; otherwise stop the test case and record why.
6. **Records.** Use permanent ink on paper, or tracked entries in an electronic copy. Correct
   an entry with a single line through it, the new entry, your initials, the date and the
   reason. Never erase, overwrite or use correction fluid.
7. **Independence.** You must not execute a test case you wrote.
8. **Closing a test case.** Complete the result table at the end of each test case. The
   reviewer checks each executed test case and signs it.

**Test data.** All test data is synthetic. Never enter real participant data in a test.

# 2. Version record (completed at the start of execution)

| Item | Version or identifier recorded | Recorded by, date |
|:----------------------------------------------|:------------------------------------------|:--------------------|
| Field application build (Settings screen) | | |
| Field application package file and SHA-256 | | |
| Portal version and commit (sidebar) | | |
| Database migration head | | |
| Server functions deployed (version or deploy date) | | |
| SurveyGen commit | | |
| SurveyTest commit | | |
| DataBackup commit | | |
| Test device A: model, Android version | | |
| Test device B: model, Android version | | |
| Workstation: operating system, browser and version | | |

# 3. Tester log

Everyone who executes or reviews a test case signs here once, so that their initials can be
identified.

| Name | Role | Initials | Signature | Date |
|:------------------------|:----------------------|:---------|:--------------------|:-----------|
| | | | | |
| | | | | |
| | | | | |
| | | | | |

# 4. Common prerequisites

| ID | Prerequisite |
|:-----|:-----------------------------------------------------------------------------------|
| P-1 | A project named **VALIDATION-TEST** exists in the production portal and is used for nothing else. |
| P-2 | Portal accounts with individual e-mail addresses: **OWN** (Owner of VALIDATION-TEST), **EDT** (Editor), **VWR** (Viewer), **NM** (not a member of VALIDATION-TEST). |
| P-3 | Field credentials in VALIDATION-TEST: **FC1** (interviewer 1) and **FC2** (interviewer 2). |
| P-4 | Two Android test devices, **A** and **B**, with the field application at the version under test and automatic date and time switched on. |
| P-5 | A workstation with SurveyGen at the version under test, the validation test assets from the validation package's `test-assets` folder, and a SHA-256 tool (for example `sha256sum`, or `Get-FileHash` in PowerShell). |
| P-6 | The validation test survey built with SurveyGen: run `python3 make_test_survey.py` in `test-assets`, then build `valtest_config.json` and `valtest_config_v2.json` with SurveyGen. This produces packages **valtest_v1.zip** and **valtest_v2.zip**. Then run `python3 make_unsafe_package.py` to produce **valtest_unsafe.zip**. |

The validation test survey has two forms: **Household** (base form, ID "VT" + site +
3-digit counter) and **Household member** (repeating child form, linked on hhid). The
`Comments` column of the dictionary names the test case that uses each question.

# 5. Installation Qualification (IQ)

## IQ-01 Source baseline

| Verifies | URS-901, URS-902 | Prerequisites | Read access to the five source repositories |
|:----------|:------------------|:--------------|:---------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | In each repository, look up the release tag or commit listed in DK-VAL-001 section 2.1. | The tag or commit exists and is on the main branch (or, before merge, on the branch named in the Summary Report). | | | |
| 2 | Open the field application's ChangeLog and the portal's CHANGELOG at those versions. | Each has a heading for the release version, with a dated list of changes. The portal entry names the migration head 20261008150000. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## IQ-02 Field application installation

| Verifies | URS-901 | Prerequisites | P-4; release package file datakollecta-1.4.1-build19.apk |
|:----------|:---------|:--------------|:--------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Compute the SHA-256 checksum of the package file. Record it in the Version Record. | A 64-character checksum is recorded. | | | |
| 2 | Record the package's signing certificate fingerprint (for example `apksigner verify --print-certs`). | The certificate is the organisation's DataKollecta key, not a debug key. Record the SHA-256 fingerprint. | | | |
| 3 | Install the package on devices A and B, and open **Settings**. *Evidence.* | The application opens, named DataKollecta. Settings shows version 1.4.1+19. | | | |
| 4 | In the device's application settings, check the application ID. | `com.datakollecta.datakollecta`. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## IQ-03 Portal deployment

| Verifies | URS-901 | Prerequisites | P-2 |
|:----------|:---------|:--------------|:-----|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Sign in to the portal as OWN, and read the version and commit in the sidebar. *Evidence.* | Version 1.2.0. The commit matches the tag web-v1.2.0 (ea1f2990cdd8, or a later commit recorded in the Summary Report). | | | |
| 2 | In the hosting provider's dashboard (Vercel), check the production deployment's source. | Production is deployed from the DataKollecta-Web main branch, at the commit seen in step 1. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## IQ-04 Database migration level

| Verifies | URS-901, URS-902 | Prerequisites | Administrator access to the Supabase project; Supabase CLI linked to production |
|:----------|:------------------|:--------------|:------------------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Run `supabase migration list` against production. *Evidence: save the output.* | Every migration in the repository at web-v1.2.0 is applied, the last being 20261008150000. No migration is applied that is not in the repository. | | | |
| 2 | In the database, list the triggers on `system_audit_events`, `formchanges` and `submissions` (query in DK-SOP-001 Appendix G). | The protective triggers (row-level and TRUNCATE) are present and enabled. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## IQ-05 Server functions

| Verifies | URS-901 | Prerequisites | Administrator access to the Supabase project |
|:----------|:---------|:--------------|:----------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | List the deployed server functions (dashboard or `supabase functions list`). *Evidence.* | Exactly app-login, app-sync and project-data-feed are deployed. Record each function's version and last deploy date. | | | |
| 2 | Compare each function's deploy date with the date of tag web-v1.2.0, and with the CHANGELOG entries for later function changes. | Each function was deployed on or after the last change to its code at the release version. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## IQ-06 Authentication configuration

| Verifies | URS-401, URS-406, URS-407, URS-412 | Prerequisites | Administrator access to the Supabase project |
|:----------|:-----------------------------------|:--------------|:----------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | In the production authentication settings, record: e-mail confirmation, minimum password length, secure password change, sign-up enabled, MFA (TOTP) enabled, session time limit and inactivity timeout, and rate limits. *Evidence.* | The values match `supabase/config.toml` at web-v1.2.0: confirmation on; length 10; secure change on; sign-up on; TOTP on; no inactivity timeout (known gap R-03); rate limits as committed. | | | |
| 2 | Confirm that every administrator account on the Supabase, Vercel and GitHub organisations has MFA enabled. | All administrator accounts have MFA. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## IQ-07 Hosting and service providers

| Verifies | URS-903, URS-405 | Prerequisites | Administrator access to the provider accounts |
|:----------|:------------------|:--------------|:-----------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | From the Supabase account, record: organisation and project, region, plan, backup frequency and retention, and whether point-in-time recovery is enabled. *Evidence.* | All values recorded. Backups are enabled. | | | |
| 2 | Obtain the current security attestation of each provider (for example a SOC 2 report or summary) and record its date. | Attestations are current (issued within the last 18 months). | | | |
| 3 | Record the production portal domain, and check its TLS certificate in a browser. | The certificate is valid and issued for the domain. | | | |
| 4 | Update DK-VAL-002 section 6 with the facts recorded, through change control. | Facts recorded; conclusion unchanged, or a deviation is raised. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## IQ-08 Survey and backup tools

| Verifies | URS-901 | Prerequisites | P-5 |
|:----------|:---------|:--------------|:-----|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | On the workstation, run `git rev-parse HEAD` in the SurveyGen, SurveyTest and DataBackup folders. | Each matches the commit in DK-VAL-001 section 2.1, or a later approved commit. | | | |
| 2 | Record the Python and Flutter versions installed. | Recorded. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

# 6. Operational Qualification (OQ)

## OQ-01 Survey build refuses a dictionary with errors

| Verifies | URS-102 | Prerequisites | P-5, P-6 (valtest_errors.xlsx and valtest_config_errors.json) |
|:----------|:---------|:--------------|:---------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Run SurveyGen with `valtest_config_errors.json`. | The program reports "ERRORS FOUND" and that no package was created. | | | |
| 2 | List the output folder `build/errors`. | It contains only `gistlogfile.txt`: no XML files, manifest or ZIP. | | | |
| 3 | Open `gistlogfile.txt`. *Evidence: keep the file.* | It reports each of the five deliberate errors: field name 'Respondent Name'; radio 'sex' with no responses; skip to nonexistent field 'no_such_field'; logic check using nonexistent field 'visit_dte'; 'age' with only one end of its range. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-02 Survey build from a valid dictionary

| Verifies | URS-101, URS-103 | Prerequisites | P-5, P-6 |
|:----------|:------------------|:--------------|:---------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Run SurveyGen with `valtest_config.json`. | "SUCCESS". No errors are reported. | | | |
| 2 | List the contents of `build/v1/valtest_v1.zip`. | household.xml, member.xml, survey_manifest.gistx and sites.csv. | | | |
| 3 | Open survey_manifest.gistx. | surveyId `valtest_v1`, databaseName `valtest.sqlite`, and two forms, household and member. | | | |
| 4 | Compute and record the SHA-256 checksum of valtest_v1.zip. | Recorded. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-03 Survey testing with SurveyTest

| Verifies | URS-105 | Prerequisites | SurveyTest installed (P-5); valtest_v1.zip |
|:----------|:---------|:--------------|:---------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Open valtest_v1.zip in SurveyTest and run a test with the default settings. | The run completes. A report is shown with the survey name, survey ID, number of interviews and findings. | | | |
| 2 | Save the HTML report. *Evidence.* | A single HTML file is saved. | | | |
| 3 | Review the findings and the skip decision tables for the Household form. | The skips on `pregnant` (shown only for females) and `fever_days` (shown only when Fever is ticked) appear, and were exercised in both directions. Record any findings and their explanation. | | | |
| 4 | Open valtest_unsafe.zip in SurveyTest. | The package is refused at installation, naming the unusable field name. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-04 Survey lifecycle and package protection

| Verifies | URS-106, URS-410 | Prerequisites | P-1, P-2; valtest_v1.zip |
|:----------|:------------------|:--------------|:--------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As EDT, upload valtest_v1.zip to VALIDATION-TEST. | The survey appears with status Draft. | | | |
| 2 | Promote the survey to **Test**. | The status is Test. | | | |
| 3 | Promote the survey to **Deployed**. *Evidence.* | The status is Deployed. | | | |
| 4 | Try to edit the deployed survey, and to replace or delete its package. | Editing is not offered or is refused. Replacing or deleting the package is refused. | | | |
| 5 | As VWR, try to upload a package or change the survey's status. | The options are not available or the action is refused. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-05 New survey version keeps one dataset

| Verifies | URS-103, URS-107 | Prerequisites | OQ-04 and OQ-18 completed (records exist in valtest v1); valtest_v2.zip |
|:----------|:------------------|:--------------|:-----------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Record the number of Household records on device A, and the highest Household ID. | Recorded. | | | |
| 2 | As EDT, create a **New Version** of the survey from valtest_v2.zip, and deploy it. | Version 2 is Deployed in the same dataset. | | | |
| 3 | On device A, download the new version and open it. | Version 2 opens. The question "Does the household own a bed net?" is present. | | | |
| 4 | Open the record list for Household. | All records from step 1 are still listed, with their values. | | | |
| 5 | Create one new Household record. | Its ID continues the counter from step 1 (the next number); the counter has not restarted. | | | |
| 6 | Synchronise. In the portal, view the Household data. | Old and new records are in one dataset. The new column `bednet` has a value only for the new record. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-06 Unsafe survey package is refused on the device

| Verifies | URS-104 | Prerequisites | Device A with valtest installed; valtest_unsafe.zip |
|:----------|:---------|:--------------|:-----------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Copy valtest_unsafe.zip into the application's `DataKollecta/zips` folder on device A (side-load), and restart the application. | The application starts. | | | |
| 2 | Select "Validation Test Survey UNSAFE" and try to open a form. *Evidence.* | The survey is refused with an error naming the unusable identifier (resp-ondent). No form opens. | | | |
| 3 | Select the validation survey (valtest) and open a Household record. | It works normally. | | | |
| 4 | Remove the unsafe survey in Settings. | It is removed; the valtest survey is unaffected. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-07 Question types and required answers

| Verifies | URS-201, URS-205 | Prerequisites | Device A signed in with FC1; valtest v1 downloaded |
|:----------|:------------------|:--------------|:----------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Start a new Household record. At "Select the study site" (drop-down), leave it unanswered. | Next is not available until a site is selected. | | | |
| 2 | Continue through the form, checking that each question type is shown correctly: date (visitdate), text (respondent), number (age), single choice (sex), decimal (weight), multiple choice (symptoms), time (arrival). | Each question shows the right input control and cannot be passed while blank. | | | |
| 3 | At "Does the respondent smoke?", check the options. | "Don't know" and "Refused" are offered as well as Yes and No. Choosing "Refused" allows Next. | | | |
| 4 | At "Notes (optional)", leave the field blank. | Next is available with the field blank. | | | |
| 5 | Finish and save the record. | The record is saved and appears in the Household record list. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-08 Range checks

| Verifies | URS-202 | Prerequisites | As OQ-07 |
|:----------|:---------|:--------------|:----------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | In a new Household record, enter age **17**. *Evidence.* | A range message is shown and Next is not available. | | | |
| 2 | Enter age **111**. | A range message is shown and Next is not available. | | | |
| 3 | Enter age **18**, then **110**. | Both are accepted. | | | |
| 4 | At visitdate, choose tomorrow's date. | Refused (the maximum is today). | | | |
| 5 | At visitdate, choose a date more than one year ago. | Refused (the minimum is one year ago). | | | |
| 6 | At weight, enter **1.9**, then **250.1**, then **72.5**. | 1.9 and 250.1 are refused; 72.5 is accepted. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-09 Logic checks

| Verifies | URS-203 | Prerequisites | As OQ-07 |
|:----------|:---------|:--------------|:----------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | In a new record, enter visitdate = today − 5 days. At consentdate, enter today − 2 days. *Evidence.* | The message "Consent cannot be signed after the visit date" is shown, and Next is not available. | | | |
| 2 | Change consentdate to today − 5 days. | The message disappears; Next is available. | | | |
| 3 | Change consentdate to today − 10 days. | Accepted. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-10 Skip logic and clearing of skipped answers

| Verifies | URS-204 | Prerequisites | As OQ-07; portal access as VWR to inspect the saved record |
|:----------|:---------|:--------------|:-----------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | New record: sex = **Male**. | "Is the respondent pregnant?" is not shown; the next question is weight. | | | |
| 2 | Go back, set sex = **Female**. | The pregnancy question is shown. Answer **Yes**. | | | |
| 3 | At symptoms, tick **Cough** only. | "For how many days has there been fever?" is not shown. | | | |
| 4 | Go back, tick **Fever** as well; answer fever days = **3**. | The fever-days question is shown and accepted. | | | |
| 5 | Go back to sex and change it to **Male**. Go back to symptoms and untick Fever. Complete and save the record. Note the respondent name used. | The record saves. | | | |
| 6 | Synchronise, and in the portal open the record. *Evidence.* | `pregnant` and `fever_days` are empty: the answers to questions skipped on the final path were cleared. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-11 Unique values and duplicate records

| Verifies | URS-206 | Prerequisites | As OQ-07 |
|:----------|:---------|:--------------|:----------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Create and save a Household record with phone **0700000001**. | Saved. | | | |
| 2 | Start another record, and enter the same phone number. *Evidence.* | The message "This phone number is already registered" is shown, and Next is not available. | | | |
| 3 | Enter **0700000002**. | Accepted. | | | |
| 4 | Enter a phone number of 9 digits. | Refused: the length must be exactly 10. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-12 Identifier generation

| Verifies | URS-207 | Prerequisites | As OQ-07 |
|:----------|:---------|:--------------|:----------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Create a Household record with site **Site One** (01). Note its Household ID. | The ID has the form VT01nnn, with a 3-digit counter. | | | |
| 2 | Create a second record for Site One. | The ID is the previous one plus one. | | | |
| 3 | Create a record for **Site Two** (02). | The ID is VT02nnn, with its own counter. | | | |
| 4 | List all Household IDs on the device. *Evidence.* | No two records share an ID. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-13 Automatic system variables

| Verifies | URS-208, URS-901 | Prerequisites | A record saved and synchronised (any earlier OQ) |
|:----------|:------------------|:--------------|:--------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Note the device clock when starting a new record and when saving it. Save, then synchronise. | Saved and uploaded. | | | |
| 2 | In the portal, open the record. *Evidence.* | `starttime` and `stoptime` match the times noted (within a minute). `startdate` is the date. `uniqueid` is a UUID. `swver` reads "DataKollecta 1.4.1+19". `survey_id` is valtest_v1. `lastmod` is the save time. | | | |
| 3 | On the device, open the record, change the respondent name, save, and synchronise. | In the portal, `lastmod` shows the later time. `starttime` is unchanged. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-14 Offline operation and persistence

| Verifies | URS-210, URS-213 | Prerequisites | Device B signed in with FC2; valtest v1 downloaded |
|:----------|:------------------|:--------------|:----------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Switch device B to flight mode (no network). | No connection. | | | |
| 2 | Create and save three Household records. | All three save without any network error. | | | |
| 3 | Force-close the application, restart the device, and open the application again. | All three records are listed with their values. | | | |
| 4 | Remove the survey in Settings and confirm. Note the message. | The message states that collected data will not be deleted. | | | |
| 5 | Download the survey again (switch off flight mode) and open the Household list. | The three records are still present. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-15 Editing a saved record: device audit trail and re-upload

| Verifies | URS-301, URS-302, URS-306, URS-502 | Prerequisites | A synchronised Household record on device A (created with FC1) |
|:----------|:-----------------------------------|:--------------|:-----------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Open the record on device A. Change age from its value to a new valid value, and weight to a new value. Save. | A summary of the changes is shown before saving, and the record saves. | | | |
| 2 | Check whether a reason for the change is requested. | **Known gap (R-01):** no reason is requested. Record what is shown. | | | |
| 3 | Synchronise. | The upload reports success. | | | |
| 4 | In the portal (VWR), open the record. *Evidence.* | The record shows the new values. The device edit history lists two changes (age, weight), each with old value, new value, time of change and user (FC1). | | | |
| 5 | Synchronise device A again without changing anything. | Nothing new is uploaded. The edit history in the portal still lists exactly two changes. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-16 Field-device sign-in and lockout

| Verifies | URS-403 | Prerequisites | Device B; field credential FC2; a further credential FC-LOCK created for this test |
|:----------|:---------|:--------------|:----------------------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | On device B, try to sign in with a username that does not exist. | Refused with a general message that does not say whether the username exists. | | | |
| 2 | Try to sign in as FC-LOCK with a wrong password. | Refused with the same message as step 1. | | | |
| 3 | Repeat step 2 until 10 failed attempts have been made, then try the **correct** password for FC-LOCK. *Evidence.* | Refused while the lockout lasts (15 minutes). | | | |
| 4 | After 15 minutes, sign in as FC-LOCK with the correct password. | Accepted. | | | |
| 5 | In the portal (OWN), view FC-LOCK. | The credential is shown; its password is never displayed. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-17 Revoking a device's access

| Verifies | URS-404 | Prerequisites | Device B signed in with FC2, with at least one unsynchronised record |
|:----------|:---------|:--------------|:-------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As OWN, **reset the password** of FC2 in the portal. | Confirmed. | | | |
| 2 | On device B, synchronise. *Evidence.* | The upload is refused. The application says the credential must be updated. The unsynchronised record is still on the device. | | | |
| 3 | In Settings on device B, enter the new password and synchronise. | Accepted. The pending record is uploaded. | | | |
| 4 | As OWN, **disable** FC2. On device B, create a record and synchronise. | Refused; the record stays on the device. | | | |
| 5 | Re-enable FC2. As OWN, **pause** the project. Synchronise device B. | Refused. | | | |
| 6 | Set the project back to **active**. Synchronise device B. | Accepted. The pending record is uploaded. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-18 Upload completeness, interruption and attribution

| Verifies | URS-501, URS-503 | Prerequisites | Device A signed in with FC1 |
|:----------|:------------------|:--------------|:-----------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | In flight mode, create **20** Household records. Note the count of unsynchronised records shown. | The count includes the 20 records. | | | |
| 2 | Switch off flight mode, start synchronising, and switch flight mode on again before it completes. | The application reports the interruption. No error message suggests data loss. | | | |
| 3 | Switch off flight mode and synchronise again until the application reports nothing pending. | Nothing pending. | | | |
| 4 | In the portal, count the Household records from device A. *Evidence.* | Every record created is present exactly once: no duplicates and none missing. | | | |
| 5 | Open any one of these records in the portal. | It is attributed to FC1 (uploader), with device A's identifier. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-19 A survey cannot be claimed by two projects on one device

| Verifies | URS-505 | Prerequisites | A second project **VALIDATION-TEST-2** with its own credential FC3, into which valtest_v1.zip is uploaded and deployed |
|:----------|:---------|:--------------|:--------------------------------------------------------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | On device A (which already holds valtest from VALIDATION-TEST), add the project VALIDATION-TEST-2 with FC3 and check for surveys. *Evidence.* | The valtest survey from VALIDATION-TEST-2 is refused, with a message that it belongs to another project. | | | |
| 2 | Synchronise device A. | Records go only to VALIDATION-TEST. VALIDATION-TEST-2 receives none. | | | |
| 3 | Archive VALIDATION-TEST-2 after the test. | Archived. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-20 Portal accounts and passwords

| Verifies | URS-401 | Prerequisites | A new e-mail address not yet registered |
|:----------|:---------|:--------------|:----------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Sign up with the new address and a 9-character password. | Refused: at least 10 characters are required. | | | |
| 2 | Sign up with a 10-character password. Before confirming the e-mail, try to sign in. | Sign-in is refused until the address is confirmed. | | | |
| 3 | Confirm the address from the e-mail and sign in. | Signed in. No projects are visible. | | | |
| 4 | Change the password from the account page. *Evidence.* | Re-authentication is required before the change is accepted. | | | |
| 5 | Sign in with a wrong password several times. | Each attempt is refused. Record whether a rate-limit message appears (lockout is a known gap, R-05). | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-21 Role-based access

| Verifies | URS-402, URS-410 | Prerequisites | P-2 |
|:----------|:------------------|:--------------|:-----|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Sign in as **NM**. Search for VALIDATION-TEST. Try to open its address, copied from OWN's browser. | The project is not listed and cannot be opened. No data is shown. | | | |
| 2 | Sign in as **VWR**. | The project, surveys, records and members are visible. There is no option to upload surveys, manage the field team, manage members, lock data, or reclassify or purge records. | | | |
| 3 | Sign in as **EDT**. | EDT can upload surveys and manage field credentials. EDT cannot manage members, lock data, or reclassify or purge records. | | | |
| 4 | Sign in as **OWN**. | All the actions in the role matrix (DK-VAL-003 §6.2) are available. | | | |
| 5 | As VWR, try a forbidden change directly against the server: use the browser's developer tools to repeat a request EDT made (for example, creating a field credential) using VWR's session. *Evidence.* | Refused by the server (permission error); nothing is changed. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-22 Portal users cannot change collected data

| Verifies | URS-308 | Prerequisites | Records exist in VALIDATION-TEST |
|:----------|:---------|:--------------|:----------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As OWN, open a record in the portal. | There is no option to edit or delete the record's values. | | | |
| 2 | As OWN, use the browser's developer tools to send an update to the record and a delete of the record directly to the database API. *Evidence.* | Both are refused; the record is unchanged. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-23 Server audit trail content

| Verifies | URS-303, URS-305, URS-307, URS-408 | Prerequisites | OQ-15 and OQ-17 completed |
|:----------|:-----------------------------------|:--------------|:---------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As OWN, add a member (a test account) as Viewer, then change their role to Editor, then remove them. | Each action succeeds. | | | |
| 2 | Export the project's data (as in OQ-29) and open `project_audit.csv`. *Evidence.* | There are events for: the member added, the role changed and the member removed (OWN as actor, with time and before/after values); the FC2 password reset and disable from OQ-17; the survey status changes from OQ-04; the record inserts and updates from the devices (uploader shown). | | | |
| 3 | Check the times of the events from step 1. | The times match the time of the actions (with time zone) to within a minute. | | | |
| 4 | Open the record edited in OQ-15, and view its server history in the portal. | The server history shows the original insert and the update, with before and after values. | | | |
| 5 | Check that no event contains a password, password hash or session token. | None found. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-24 The audit trail cannot be changed or deleted

| Verifies | URS-304 | Prerequisites | OWN session; browser developer tools |
|:----------|:---------|:--------------|:-------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As OWN, send an update to one row of `system_audit_events` directly to the database API. *Evidence.* | Refused. | | | |
| 2 | As OWN, send a delete of one row of `system_audit_events`. | Refused. | | | |
| 3 | As OWN, send an update and a delete of one row of `formchanges`. | Both refused. | | | |
| 4 | Export again and compare the audit rows with the earlier export. | Unchanged. | | | |

Note: protection against the server's own functions and direct database sessions, including
bulk deletion (TRUNCATE), is verified by the automated tests AT-08 and AT-09.

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-25 Test and deployed records

| Verifies | URS-601, URS-306 | Prerequisites | A survey in **Test** stage and a survey in **Deployed** stage in VALIDATION-TEST |
|:----------|:------------------|:--------------|:------------------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Collect and upload one record in the Test-stage survey and one in the Deployed survey. | Both uploaded. | | | |
| 2 | In the portal Data page, check each record's status. | The first is *test*, the second *deployed*. The default view shows deployed records only. | | | |
| 3 | Edit the test record on the device and upload it again, after promoting its survey to Deployed. | The record is still labelled *test*. | | | |
| 4 | As OWN, reclassify the test record as deployed **without** a reason. | Refused: a reason is required. | | | |
| 5 | Reclassify it with a reason. *Evidence.* | Done. The audit trail shows the change with the reason and OWN as actor. | | | |
| 6 | As EDT, try to reclassify a record. | Not available or refused. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-26 Data lock

| Verifies | URS-602, URS-306 | Prerequisites | Device A with one new unsynchronised record |
|:----------|:------------------|:--------------|:---------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As OWN, try to lock the data without a reason. | Refused. | | | |
| 2 | Lock the data with the reason "Validation test OQ-26". | Locked. | | | |
| 3 | Synchronise device A. *Evidence.* | The upload is refused; the record remains pending on the device. | | | |
| 4 | Export the data. | Export works while locked. | | | |
| 5 | As OWN, unlock with a reason. Synchronise device A. | The pending record is uploaded. | | | |
| 6 | Check the audit trail. | Lock and unlock events are present with reasons, actor and time. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-27 Purging test records

| Verifies | URS-603, URS-306 | Prerequisites | At least two *test* records in VALIDATION-TEST |
|:----------|:------------------|:--------------|:----------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As EDT, look for the purge function. | Not available. | | | |
| 2 | As OWN, lock the data, then try to purge test records. | Refused while locked. Unlock afterwards (with a reason). | | | |
| 3 | As OWN, purge test records without a reason. | Refused. | | | |
| 4 | Purge with a reason. *Evidence.* | The test records no longer appear in the data. Deployed records are untouched. | | | |
| 5 | Export and check `project_audit.csv`. | A purge event exists for each purged record, containing its full content and the reason. | | | |
| 6 | On a device that still holds one of the purged records, edit it and synchronise. | The upload completes, but the record does not reappear in the data. A DISCARD_PURGED event is in the audit trail. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-28 Projects with data cannot be deleted

| Verifies | URS-604 | Prerequisites | VALIDATION-TEST holds records |
|:----------|:---------|:--------------|:-------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As OWN, try to delete VALIDATION-TEST. *Evidence.* | Refused, with a message that a project holding data can only be archived. | | | |
| 2 | Try to delete the deployed survey. | Refused. | | | |
| 3 | Archive VALIDATION-TEST-2 (from OQ-19). | Archived; its data remains viewable and exportable. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-29 Export and integrity manifest

| Verifies | URS-701, URS-702, URS-305 | Prerequisites | Records and edits from earlier OQs |
|:----------|:---------------------------|:--------------|:------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As VWR, export the valtest survey's data (all records). | A ZIP file downloads. | | | |
| 2 | Unzip it and list the files. | household.csv, member.csv, formchanges.csv, project_audit.csv and manifest.json. | | | |
| 3 | Open manifest.json. | It lists every file with its size and SHA-256 checksum, the portal version (1.2.0) and the commit. | | | |
| 4 | Compute the SHA-256 checksum of each CSV file yourself. *Evidence.* | Every checksum matches the manifest. | | | |
| 5 | Change one character in household.csv and compute its checksum again. | It no longer matches the manifest: a change to an exported file is detectable. | | | |
| 6 | Compare three records in household.csv with the same records on the device (record by record). | All values match. | | | |
| 7 | Check the audit trail for the export. | An EXPORT event by VWR exists, containing the manifest. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-30 Data feed keys

| Verifies | URS-703, URS-409 | Prerequisites | OWN session; a tool to make HTTPS requests (for example curl) |
|:----------|:------------------|:--------------|:-------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As OWN, create a data feed key. | The key is shown once. | | | |
| 2 | Read the project's data with the key, as described in the portal help (Data feeds, API reference). | Data is returned for this project only. | | | |
| 3 | Revoke the key, giving a reason, and repeat step 2. *Evidence.* | Refused. | | | |
| 4 | As EDT, look for data feed keys. | Not visible. | | | |
| 5 | Check the audit trail. | Key creation, use and revocation are recorded. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-31 Scheduled backup

| Verifies | URS-801 | Prerequisites | DataBackup configured on the backup computer as described in its README |
|:----------|:---------|:--------------|:------------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Run `export_data.py` (or wait for the scheduled run). | It completes and exits successfully. A summary e-mail is received. | | | |
| 2 | Open the newest backup folder for VALIDATION-TEST. | It has one CSV per form, and formchanges.csv, with today's records. | | | |
| 3 | Make the backup fail (for example by temporarily giving a wrong server address), and run it. *Evidence.* | It retries, then exits with an error and sends a failure e-mail. Restore the correct setting. | | | |
| 4 | Record the schedule in use (for example the Task Scheduler or cron entry). | Daily, or as set in DK-SOP-001 §7. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-32 Encrypted snapshot and verified restore

| Verifies | URS-802, URS-803 | Prerequisites | DataBackup; PostgreSQL client tools; GnuPG with the approved backup key; a local PostgreSQL server for the restore |
|:----------|:------------------|:--------------|:------------------------------------------------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Run `backup_snapshot.py create` against production. | An encrypted archive and a receipt containing the archive's SHA-256 checksum are written. | | | |
| 2 | Create an empty local database and run `backup_snapshot.py restore-local` into it. *Evidence.* | The integrity check passes and the restore completes. | | | |
| 3 | Count rows in submissions, formchanges and system_audit_events, in the restored database and in production (for VALIDATION-TEST). | The counts match, allowing for activity after the snapshot time. | | | |
| 4 | Make a copy of the archive and change one byte. Try to restore it. | Refused before any data is written. | | | |
| 5 | Try to restore into a database that is not empty. | Refused. | | | |
| 6 | Complete a Restore Test Record (DK-SOP-001 Appendix E). | Completed and signed. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-33 Device backup log

| Verifies | URS-804 | Prerequisites | Device A; a way to browse its files (USB file transfer) |
|:----------|:---------|:--------------|:-------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Save a new Household record on device A. | Saved. | | | |
| 2 | Open `DataKollecta/backups/valtest_v1/household_bak` on the device storage. | The file ends with an entry for the record just saved, containing its values. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-34 Encrypted communication

| Verifies | URS-405 | Prerequisites | Browser |
|:----------|:---------|:--------------|:--------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Open the portal address using `http://` instead of `https://`. | The browser is redirected to HTTPS, or the connection is refused. | | | |
| 2 | In the browser's developer tools, check the server API address the portal uses. | It uses HTTPS. | | | |
| 3 | Record the server API address configured in the field application's build. | It uses HTTPS. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-35 Access lists

| Verifies | URS-408 | Prerequisites | OQ-16, OQ-17 and OQ-23 completed |
|:----------|:---------|:--------------|:----------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | As OWN, open the Members page. *Evidence.* | Every member is listed with their role. | | | |
| 2 | Open the Field team page. | Every field credential is listed, including disabled ones, with their status. | | | |
| 3 | Find the history of access changes in the exported audit trail. | Every addition, role change, removal, credential creation, reset and disable made during testing is listed. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-36 Repeating child forms

| Verifies | URS-211 | Prerequisites | As OQ-07 |
|:----------|:---------|:--------------|:----------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Create a Household record with number of members = **3**, and save. | The application offers to start entering household members. | | | |
| 2 | Enter the three members. | Each member form is pre-filled with the household's ID and numbered 1, 2 and 3. | | | |
| 3 | Synchronise, and view the member data in the portal. *Evidence.* | Three member records, each with the parent's hhid and linenum 1, 2 and 3. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-37 Response options from a file

| Verifies | URS-212 | Prerequisites | As OQ-07 |
|:----------|:---------|:--------------|:----------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | Open the site question in a new Household record. | Exactly three options: Site One, Site Two and Site Three, from sites.csv. | | | |
| 2 | Select Site Three and save the record; check the stored value in the portal. | The stored value is the code 03. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-38 Input formats

| Verifies | URS-209 | Prerequisites | As OQ-07 |
|:----------|:---------|:--------------|:----------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | At weight, try to type letters, and two decimal points. | Not accepted. | | | |
| 2 | At arrival time, type 0930. | It is shown and stored as 09:30. | | | |
| 3 | At arrival time, type 2560. | Refused as an invalid time. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

## OQ-39 Survey download

| Verifies | URS-504 | Prerequisites | VALIDATION-TEST with a Draft survey, a Test survey and a Deployed survey |
|:----------|:---------|:--------------|:-----------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | On device B, check for surveys to download. | The Test and Deployed surveys are offered. The Draft survey is not. | | | |
| 2 | Download a survey. | It installs and opens. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

# 7. Performance Qualification (PQ)

## PQ-01 End-to-end study simulation

| Verifies | URS-210, URS-501, URS-701 and the end-to-end workflow | Prerequisites | All IQ passed. Devices A (FC1) and B (FC2) with valtest deployed. Two testers acting as interviewers, plus a data manager. A paper source sheet for 10 fictitious households. |
|:----------|:---------------------------|:--------------|:--------------------------------------------------------------------------------------|

| Step | Action | Expected result | Actual result | P/F | Initials, date |
|:----|:-----------------------------------|:-----------------------------------|:-----------------------|:----|:-------------|
| 1 | The data manager prepares a paper source sheet with values for 10 households (5 per device), including members. | Prepared, signed and dated. | | | |
| 2 | Each interviewer enters 5 households from the sheet on their device, **in flight mode**, over at least two separate sessions. | All saved without error. | | | |
| 3 | Each interviewer corrects one value they entered, as directed by the data manager on the sheet. | Saved. | | | |
| 4 | Both devices synchronise. | Nothing pending on either device. | | | |
| 5 | The data manager locks the data with a reason, then exports. | Export completed. The manifest checksums verify (as in OQ-29). | | | |
| 6 | The data manager compares every exported value with the source sheet. *Evidence: annotated comparison.* | Every value matches the sheet after its directed correction. The two corrections appear in formchanges.csv with old and new values and the correct interviewer. | | | |
| 7 | Take an encrypted snapshot and restore it locally (as in OQ-32). Compare record counts with the export. | The counts match. | | | |
| 8 | Unlock the data with a reason. Purge or reclassify the test data as required, and archive the test project if testing is complete. | Done and audited. | | | |

| Overall result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |

# 8. Automated regression tests (AT)

Automated suites are executed on the release commits. For each suite the tester keeps the
full output log in the evidence folder, records its SHA-256 checksum, and records the counts
in DK-VAL-005 section 4.

A suite **passes** when its command exits with status 0 and no test fails. Every skipped
test must be explained.

| ID | Component | Command (run from the repository root) | Verifies | Acceptance criterion |
|:-----|:--------------|:------------------------------------------------|:-----------------|:-------------------------|
| AT-01 | Field application | `flutter analyze` | Code quality of all field-application code | No errors. Any warning is assessed as a deviation. |
| AT-02 | Field application | `flutter test` | URS-103, 104, 107, 2xx, 301, 501, 502, 505 | All tests pass. Skips must be product-specific tests only. |
| AT-03 | Field application, DataKollecta build | `flutter test --dart-define=APP_PRODUCT=datakollecta` | As AT-02, as built for DataKollecta | All tests pass. Skips must be product-specific tests only. |
| AT-04 | SurveyGen | `python -m unittest discover -s tests -v` | URS-101–103 | All tests pass. Skips need a stated reason. |
| AT-05 | SurveyTest | `flutter analyze && flutter test` | URS-104, 105, 204, 211 | No analysis issues; all tests pass. |
| AT-06 | Portal | `npm run lint`, `npx tsc --noEmit -p tsconfig.app.json`, `npm run build` | Build integrity of the portal | No lint errors, no type errors, build succeeds. |
| AT-07 | Portal | `npx vitest run` | URS-101, 102, 401, 701, 702 | All tests pass. |
| AT-08 | Server functions and database | Local stack: `supabase start`, `supabase db reset`, functions served; then `npm run test:functions` | URS-106, 302–304, 307, 308, 402–404, 409, 410, 501–504, 601–604, 703 | All tests pass. |
| AT-09 | Database controls | `psql "$SUPABASE_DB_URL" -f supabase/tests/validation_controls.sql` and `.../audit_trail_hardening.sql` | URS-302–304, 308, 602, 604 | Each script reports that its checks passed. |
| AT-10 | DataBackup | `python -m unittest discover -s tests -v` | URS-802, 803 | All tests pass. |

| Overall AT result (Pass/Fail) | Deviation IDs | Tester signature, date | Reviewer signature, date |
|:----------------------|:----------------|:-----------------------|:-----------------------|
| | | | |
