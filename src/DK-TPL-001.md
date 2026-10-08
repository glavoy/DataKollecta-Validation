---
doc_id: DK-TPL-001
title: Study Build Validation Record
version: "1.0"
orientation: portrait
status: Approved template. Complete one copy for each study build and each amendment.
approvers:
  - [Author, System Owner / Lead Developer]
  - [Reviewer, Quality Assurance]
  - [Approver, Head of Data Management]
---

# How to use this record

This record shows that a study's DataKollecta configuration (its survey package) was:

- specified from the protocol;
- built and tested;
- accepted by its users before real data was collected with it.

It is the study-level part of the system's validation (DK-VAL-001, section 4.2; DK-SOP-001,
section 10). The system's general functions are validated separately and need not be
re-tested here.

Instructions:

- Complete a **new copy** for the first release of a study's survey and for **every
  amendment** that changes it. File the signed copy in the study's data management file.
- Write "N/A", with a reason, for anything that does not apply.
- Follow good documentation practice: no blank required fields; corrections with a single
  line, initials, date and reason.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 1. Study and build identification

| Field | Entry |
|:-------------------------------------------|:------------------------------------------------|
| Study title | |
| Protocol number and version / date | |
| Data management plan version / date | |
| CRF or questionnaire version (source for the dictionary) | |
| DataKollecta project (name / code) | |
| This record is for | ☐ Initial release  ☐ Amendment no. ___ (previous record ref.: ___________) |
| Reason for the amendment, and the protocol amendment it implements | |
| Survey name (surveyName) | |
| Survey identifier (surveyId), new for every version | |
| Database name (databaseName), unchanged since the first version | |
| Data dictionary file name, version and SHA-256 checksum | |
| DataKollecta field application version in use for the study | |
| Portal version at the time of release | |

# Part 2. Specification review

The dictionary is reviewed against the protocol and CRF by someone other than its author.

| # | Check | Done (initials, date) | Comments |
|:--|:--------------------------------------------------------------|:-----------|:-----------------|
| 2.1 | Every data item required by the protocol and CRF is in the dictionary, and nothing that is not required (data minimisation) | | |
| 2.2 | Question wording and response options match the approved questionnaire, including translations if used | | |
| 2.3 | Eligibility and consent questions, and their skip rules, are correct and prevent enrolment of an ineligible participant | | |
| 2.4 | Ranges and logic checks are defined for all critical numeric and date fields | | |
| 2.5 | Identifier configuration (idconfig) produces the ID format in the protocol or DMP | | |
| 2.6 | Form hierarchy (crfs sheet): parent and child forms, linking fields, repeat counts | | |
| 2.7 | For an amendment: changes are limited to those in the protocol amendment; the databaseName is unchanged; existing fields are not renamed or re-typed | | |

| Specification reviewed by: name, signature, date | |
|:------------------------------------------------|:--|

# Part 3. Build

| Field | Entry |
|:-------------------------------------------|:------------------------------------------------|
| Built with | ☐ SurveyGen, commit: __________  ☐ Portal survey designer, portal version: ______ |
| Build date and by whom | |
| Build result | ☐ SUCCESS, no errors |
| Warnings (list each, with justification or action) | |
| Build log kept (file name) | |
| Package file name and SHA-256 checksum | |

# Part 4. Automated testing (SurveyTest)

| Field | Entry |
|:-------------------------------------------|:------------------------------------------------|
| SurveyTest commit and run date | |
| Seed and number of interviews | |
| Report file name (HTML), kept with this record | |
| Lint result | ☐ No problems ☐ Problems found (list below) |

| Finding (type, form, field) | Seed | Resolution (fixed in dictionary, or justification) | Initials, date |
|:---------------------------------|:--------|:------------------------------------------|:--------------|
| | | | |
| | | | |
| | | | |

| # | Check | Done (initials, date) | Comments |
|:--|:--------------------------------------------------------------|:-----------|:-----------------|
| 4.1 | Every skip rule was exercised in both directions, or the report shows why one could not be | | |
| 4.2 | Every question was reached, and every form was entered | | |
| 4.3 | The skip decision tables in the report were compared with the paper questionnaire and match it | | |

# Part 5. User acceptance test (on a device)

**Prerequisites.**

1. Upload the package to the project and promote it to **Test**.
2. Install it on a test device with a field credential of the project.
3. Use only fictitious data. Records created now are labelled *test*.

**Testing.** Carry out the standard checks (5.1–5.8). Then add one row for each
study-specific critical check: at least every eligibility rule, every consent check, every
range or logic check on a primary endpoint or safety field, and the ID format.

| # | Test (action) | Expected result | Actual result | P/F | Initials, date |
|:--|:----------------------------------|:-----------------------------|:-------------------|:----|:-----------|
| 5.1 | Download the survey on the device and open each form | All forms open; the survey name and version are correct | | | |
| 5.2 | Complete one full interview following the most common path | All questions appear in the right order with correct wording | | | |
| 5.3 | Complete an interview for an **ineligible** participant | The interview ends or blocks as the protocol requires | | | |
| 5.4 | Create two base records; check the generated IDs | IDs follow the specified format and are unique | | | |
| 5.5 | Create the child or repeat forms for one parent | Children link to the parent; numbering is correct | | | |
| 5.6 | Edit a saved record and synchronise | The edit appears in the portal with its edit history | | | |
| 5.7 | Synchronise and export from the portal | Exported values match what was entered | | | |
| 5.8 | For an amendment: open a record collected under the previous version | Old data is intact; new fields are empty | | | |
| 5.9 | *(study-specific)* | | | | |
| 5.10 | *(study-specific)* | | | | |
| 5.11 | *(study-specific)* | | | | |
| 5.12 | *(study-specific)* | | | | |
| 5.13 | *(study-specific)* | | | | |
| 5.14 | *(study-specific)* | | | | |

Attach screenshots or other evidence for failed steps and for critical checks.

# Part 6. Deviations

| No. | Step | Description | Impact | Action (fix, rebuild, retest) | Closed (initials, date) |
|:----|:-----|:------------------------|:---------------|:--------------------|:------------|
| | | | | | |
| | | | | | |

If the package is changed to fix a deviation, Parts 3 to 5 are repeated for the new
package, or the record states which tests were repeated and why the others were not.

# Part 7. Release

| # | Step | Done (initials, date) |
|:--|:--------------------------------------------------------------------|:------------------|
| 7.1 | All deviations closed; no open problem affects critical data | |
| 7.2 | Ethics and regulatory approvals for this version are in place (for an amendment: the amendment is approved) | |
| 7.3 | Field staff trained on this version | |
| 7.4 | Survey promoted to **Deployed** in the portal (date and time) | |
| 7.5 | Test records purged with a reason, or confirmed to be excluded from analysis by their *test* label | |
| 7.6 | Previous version (for an amendment): status set as agreed, and field teams told the date from which the new version must be used | |

# Part 8. Approval

By signing, the approvers confirm that the study configuration has been specified, built and
tested as recorded above, and is fit for collecting the study's data.

| Role | Name | Signature | Date |
|:-------------------------------------------|:-------------------|:-------------------|:-----------|
| Data Manager (prepared and built) | | | |
| Tester (executed Part 5; not the builder) | | | |
| Principal Investigator or delegate (approves for use) | | | |
