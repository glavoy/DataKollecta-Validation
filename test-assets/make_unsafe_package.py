#!/usr/bin/env python3
"""Make the deliberately unsafe survey package used by OQ-06.

Takes the version-1 validation package built by SurveyGen and writes
build/unsafe/valtest_unsafe.zip, in which:

  - the field name `respondent` is changed to `resp-ondent` (not a valid identifier), and
  - the manifest's surveyId, surveyName and databaseName are changed, so the package
    cannot collide with the real validation survey on the device.

The field application must refuse to open this survey and must keep working
normally for the other surveys on the device.

    python3 make_unsafe_package.py build/v1/valtest_v1.zip
"""
import json
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main(src: str) -> None:
    out_dir = HERE / "build" / "unsafe"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "valtest_unsafe.zip"
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "household.xml":
                text = data.decode("utf-8")
                assert "fieldname = 'respondent'" in text
                data = text.replace("fieldname = 'respondent'",
                                    "fieldname = 'resp-ondent'").encode("utf-8")
            elif item.filename == "survey_manifest.gistx":
                manifest = json.loads(data.decode("utf-8-sig"))
                manifest["surveyId"] = "valtest_unsafe"
                manifest["surveyName"] = "Validation Test Survey UNSAFE"
                manifest["databaseName"] = "valtest_unsafe.sqlite"
                data = json.dumps(manifest, indent=2).encode("utf-8")
            zout.writestr(item.filename, data)
    print("written", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "build" / "v1" / "valtest_v1.zip"))
