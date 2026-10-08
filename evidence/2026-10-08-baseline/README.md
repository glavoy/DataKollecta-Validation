# Automated test evidence: baseline run, 8 October 2026

The execution record, results and deviations are in DK-VAL-005, sections 4 and 7.
`SHA256SUMS` holds the checksum of every file in this folder; verify it with
`sha256sum -c SHA256SUMS`.

| File | Test |
|---|---|
| AT-01_* … AT-10_* | One log per automated suite (DK-VAL-004 section 8) |
| DEV-0n_* | Logs of the first runs that raised deviations DEV-01, DEV-02 and DEV-04 |
| setup/ | Dependency installation logs and the Flutter toolchain version |
| test-environment/ | Router, import map and launcher used to run the server functions for AT-08 (DEV-04) |

Code tested: DataKollecta 8dc4302ef9b8 (v1.4.1+19), DataKollecta-Web ea1f2990cdd8 (web-v1.2.0),
DataKollecta-SurveyGen 005a7f97e2a9, DataKollecta-SurveyTest d38cb50ea3a8,
DataKollecta-DataBackup dafe783b53ab.
