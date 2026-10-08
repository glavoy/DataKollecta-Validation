#!/usr/bin/env python3
"""Traceability: build the matrix for the Validation Summary Report, and check it.

Reads the requirement tables in src/DK-VAL-002.md and the test cases in
src/DK-VAL-004.md, and:

  * checks that every test case a requirement names exists in the protocol;
  * checks that every IQ/OQ/PQ test case in the protocol names requirements that exist;
  * checks that every requirement is verified by at least one test or procedure;
  * produces the traceability matrix (Markdown) that build_docs.py inserts into
    DK-VAL-005 in place of the line {{TRACEABILITY_MATRIX}}.

    python3 tools/traceability.py          # run the checks; exit status 1 on any problem
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URS_SRC = ROOT / "src" / "DK-VAL-002.md"
TP_SRC = ROOT / "src" / "DK-VAL-004.md"

# Section of the Functional and Design Specification (DK-VAL-003) that implements each
# requirement. "SOP" means it is met by procedure rather than by a system function.
FS = {
    "URS-101": "3.1–3.3", "URS-102": "3.1", "URS-103": "3.4", "URS-104": "4.2",
    "URS-105": "3.5", "URS-106": "6.4", "URS-107": "4.7",
    "URS-201": "4.3", "URS-202": "4.4", "URS-203": "4.4", "URS-204": "4.4",
    "URS-205": "4.4", "URS-206": "4.4", "URS-207": "4.5", "URS-208": "4.6",
    "URS-209": "4.3, 4.4", "URS-210": "4.7", "URS-211": "4.5", "URS-212": "4.3",
    "URS-213": "4.2",
    "URS-301": "4.8", "URS-302": "5.3, 7.1", "URS-303": "7.2", "URS-304": "7.3",
    "URS-305": "6.5, 6.9, 7.4", "URS-306": "4.8, 6.6–6.8", "URS-307": "7.5",
    "URS-308": "6.2",
    "URS-401": "6.1", "URS-402": "6.2", "URS-403": "5.1", "URS-404": "5.2",
    "URS-405": "10, 11", "URS-406": "6.1", "URS-407": "6.1", "URS-408": "6.2, 7.2",
    "URS-409": "6.10", "URS-410": "6.4", "URS-411": "4.10", "URS-412": "6.1",
    "URS-501": "5.3", "URS-502": "4.8, 5.3", "URS-503": "5.3", "URS-504": "5.4",
    "URS-505": "5.5",
    "URS-601": "6.6", "URS-602": "6.7", "URS-603": "6.8", "URS-604": "6.3",
    "URS-701": "6.9", "URS-702": "6.9", "URS-703": "6.10",
    "URS-801": "8.1, 8.2", "URS-802": "8.3", "URS-803": "8.4", "URS-804": "4.9",
    "URS-805": "SOP",
    "URS-901": "9", "URS-902": "9; SOP", "URS-903": "10", "URS-904": "SOP",
    "URS-905": "SOP",
}

# Result of each automated suite in the baseline run (DK-VAL-005 section 4).
AT_RESULT = {f"AT-{i:02d}": "Pass" for i in range(1, 11)}
AT_RESULT["AT-01"] = "Pass with deviation DEV-03"


def parse_urs() -> list[dict]:
    rows = []
    for line in URS_SRC.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (URS-\d{3}) \| (.+?) \| ([HML]) \| ([HML]) \| ([HML]) \| "
                     r"(High|Medium|Low) \| (.+?) \| (.+?) \|$", line)
        if m:
            rows.append({"id": m.group(1), "text": m.group(2), "risk": m.group(6),
                         "verified": m.group(7), "status": m.group(8)})
    return rows


def expand_refs(text: str) -> list[str]:
    """'IQ-01–IQ-05, OQ-13, AT-02' -> ['IQ-01', ..., 'IQ-05', 'OQ-13', 'AT-02']."""
    out = []
    for a, b in re.findall(r"\b((?:IQ|OQ|PQ|AT)-\d{2})(?:\s*[–-]\s*((?:IQ|OQ|PQ|AT)-\d{2}))?",
                           text):
        if b:
            prefix = a[:3]
            for n in range(int(a[3:]), int(b[3:]) + 1):
                out.append(f"{prefix}{n:02d}")
        else:
            out.append(a)
    return out


def parse_protocol() -> dict[str, list[str]]:
    """Test ID -> URS IDs it verifies (from each test case's 'Verifies' row)."""
    tests: dict[str, list[str]] = {}
    current = None
    text = TP_SRC.read_text(encoding="utf-8")
    for line in text.splitlines():
        h = re.match(r"^## ((?:IQ|OQ|PQ)-\d{2}) ", line)
        if h:
            current = h.group(1)
            tests[current] = []
            continue
        if current and line.startswith("| Verifies |"):
            tests[current] = re.findall(r"URS-\d{3}", line)
            current = None
        a = re.match(r"^\| (AT-\d{2}) \|", line)
        if a:
            tests[a.group(1)] = re.findall(r"URS-\d{3}", line)
    return tests


def check(urs: list[dict], tests: dict[str, list[str]]) -> list[str]:
    problems = []
    ids = {r["id"] for r in urs}
    for r in urs:
        refs = expand_refs(r["verified"])
        sop = "SOP" in r["verified"] or "section 6" in r["verified"] or "TPL" in r["verified"]
        if not refs and not sop:
            problems.append(f"{r['id']} is verified by nothing")
        for t in refs:
            if t not in tests:
                problems.append(f"{r['id']} names {t}, which is not in the protocol")
    referenced = {t for r in urs for t in expand_refs(r["verified"])}
    for t, reqs in tests.items():
        if t.startswith(("IQ", "OQ", "PQ")):
            if not reqs:
                problems.append(f"{t} names no requirement")
            for q in reqs:
                if q not in ids:
                    problems.append(f"{t} names {q}, which is not in the URS")
            if t not in referenced:
                problems.append(f"{t} is not named by any requirement's 'Verified by'")
    for r in urs:
        if r["id"] not in FS:
            problems.append(f"{r['id']} has no Functional Specification section mapped")
    return problems


def matrix_markdown() -> str:
    urs = parse_urs()
    lines = [
        "| Requirement | Risk | FS section (DK-VAL-003) | Manual tests (DK-VAL-004) | "
        "Automated tests: baseline result | Manual result | Status |",
        "|:------------|:-------|:-----------|:----------------------|:----------------------|"
        ":-----------|:--------------------------|",
    ]
    for r in urs:
        refs = expand_refs(r["verified"])
        manual = [t for t in refs if not t.startswith("AT")]
        auto = [t for t in refs if t.startswith("AT")]
        extra = []
        if "SOP" in r["verified"]:
            extra.append(re.sub(r".*?(DK-SOP-001 §\d+).*", r"\1", r["verified"]))
        if "section 6" in r["verified"]:
            extra.append("DK-VAL-002 §6")
        if "TPL" in r["verified"]:
            extra.append("DK-TPL-001")
        auto_txt = ", ".join(f"{a}: {AT_RESULT[a]}" for a in auto) or "—"
        manual_txt = ", ".join(manual + extra) or "—"
        status = r["status"].replace("**", "")
        if status.startswith("Met") and "procedural" not in status and not manual:
            status = "Met"
        lines.append(f"| {r['id']} | {r['risk']} | {FS[r['id']]} | {manual_txt} | {auto_txt} | "
                     f"{'To be recorded' if manual else 'N/A'} | {status} |")
    return "\n".join(lines)


def main() -> int:
    urs = parse_urs()
    tests = parse_protocol()
    problems = check(urs, tests)
    print(f"{len(urs)} requirements, "
          f"{sum(1 for t in tests if not t.startswith('AT'))} manual test cases, "
          f"{sum(1 for t in tests if t.startswith('AT'))} automated suites")
    for p in problems:
        print("PROBLEM:", p)
    if not problems:
        print("Traceability complete: every requirement is verified, every reference resolves.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
