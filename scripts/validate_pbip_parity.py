#!/usr/bin/env python3
"""Validate the public PBIP structure and optionally compare a local private PBIR.

The baseline contains hashes and counts for public structure only. Private paths,
visual IDs, data, and DAX formulas are never written to the parity report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "PowerBI/ProjectVortex.Public.Report"
DEFAULT_MODEL = ROOT / "PowerBI/ProjectVortex.SemanticModel"
DEFAULT_BASELINE = ROOT / "docs/pbip-structure-baseline.json"
DEFAULT_PARITY = ROOT / "docs/pbip-parity-report.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_report_root(path: Path) -> Path:
    path = path.resolve()
    if (path / "definition/pages/pages.json").exists():
        return path
    if path.name == "pages" and (path / "pages.json").exists():
        return path.parent.parent
    raise FileNotFoundError(f"PBIR report root not found: {path}")


def report_structure(report_arg: Path, model_arg: Path) -> tuple[dict, dict]:
    report = normalize_report_root(report_arg)
    model = model_arg.resolve()
    pages_root = report / "definition/pages"
    order = load_json(pages_root / "pages.json").get("pageOrder", [])
    page_rows = []
    all_visuals = []
    for page_id in order:
        folder = pages_root / page_id
        page_file = folder / "page.json"
        if not page_file.exists():
            raise FileNotFoundError(f"Missing page definition for ordered page: {page_id}")
        page = load_json(page_file)
        visuals = sorted(folder.glob("visuals/*/visual.json"))
        types = Counter()
        for visual_path in visuals:
            visual = load_json(visual_path).get("visual", {})
            types[visual.get("visualType", "UNKNOWN")] += 1
            all_visuals.append(visual_path)
        page_rows.append({
            "pageId": page_id,
            "displayName": page.get("displayName", page_id),
            "visualCount": len(visuals),
            "visualTypes": dict(sorted(types.items())),
        })

    theme_name = load_json(report / "definition/report.json").get("themeCollection", {}).get("customTheme", {}).get("name")
    theme_file = report / "StaticResources/RegisteredResources" / f"{theme_name}.json" if theme_name else None
    if not theme_file or not theme_file.exists():
        raise FileNotFoundError(f"Declared custom theme resource is missing: {theme_name or 'unnamed'}")

    relationships_file = model / "definition/relationships.tmdl"
    if not relationships_file.exists():
        raise FileNotFoundError(f"Missing semantic-model relationships: {relationships_file.name}")
    relationship_text = relationships_file.read_text(encoding="utf-8-sig")
    relationship_count = len(re.findall(r"(?m)^relationship\s+", relationship_text))

    table_files = [p for p in (model / "definition/tables").glob("*.tmdl")
                   if not p.name.startswith(("LocalDateTable_", "DateTableTemplate_"))]
    measures = []
    for table_file in sorted(table_files):
        lines = table_file.read_text(encoding="utf-8-sig").splitlines()
        i = 0
        while i < len(lines):
            match = re.match(r"^(\s*)measure\s+(.+?)\s*=\s*(.*?)\s*$", lines[i])
            if not match:
                i += 1
                continue
            indent, measure_name, expression = match.groups()
            expression_lines = [expression]
            i += 1
            while i < len(lines):
                line = lines[i]
                if not line.strip():
                    i += 1
                    continue
                line_indent = len(line) - len(line.lstrip())
                if line_indent <= len(indent) or re.match(r"^\s+(formatString|lineageTag|annotation|displayFolder|description)\s*:", line):
                    break
                expression_lines.append(line.strip())
                i += 1
            measures.append(f"{table_file.name}:{measure_name}=" + " ".join(expression_lines))

    visual_hashes = []
    for path in all_visuals:
        rel = path.relative_to(report).as_posix()
        visual_hashes.append((rel, sha(path.read_bytes())))
    page_order_hash = sha(json.dumps(page_rows, sort_keys=True, separators=(",", ":")).encode())
    visual_definition_hash = sha(json.dumps(visual_hashes, separators=(",", ":")).encode())
    structure = {
        "pageCount": len(page_rows),
        "visualCount": sum(row["visualCount"] for row in page_rows),
        "pageOrderAndTypesSha256": page_order_hash,
        "visualDefinitionsSha256": visual_definition_hash,
        "customThemeName": theme_name,
        "customThemeSha256": sha(theme_file.read_bytes()),
        "relationshipCount": relationship_count,
        "relationshipsSha256": sha(relationship_text.encode()),
        "authoredTableCount": len(table_files),
        "measureCount": len(measures),
        "daxDeclarationsSha256": sha("\n".join(sorted(measures)).encode()),
    }
    details = {"pages": page_rows, "themeHash": structure["customThemeSha256"]}
    return structure, details


def compare_private(private_report_arg: Path, private_model_arg: Path,
                    public_structure: dict, public_details: dict,
                    reported_private_visuals: int) -> dict:
    private_report = normalize_report_root(private_report_arg)
    private_structure, private_details = report_structure(
        private_report, private_model_arg
    )
    private_pages = {row["displayName"]: row for row in private_details["pages"]}
    public_pages = {row["displayName"]: row for row in public_details["pages"]}
    page_differences = []
    for name in list(dict.fromkeys([*private_pages, *public_pages])):
        priv = private_pages.get(name)
        pub = public_pages.get(name)
        if priv is None or pub is None:
            page_differences.append({"page": name, "privatePresent": priv is not None, "publicPresent": pub is not None})
            continue
        type_names = sorted(set(priv["visualTypes"]) | set(pub["visualTypes"]))
        type_delta = {kind: {"private": priv["visualTypes"].get(kind, 0), "public": pub["visualTypes"].get(kind, 0)}
                      for kind in type_names if priv["visualTypes"].get(kind, 0) != pub["visualTypes"].get(kind, 0)}
        if priv["visualCount"] != pub["visualCount"] or type_delta:
            page_differences.append({
                "page": name,
                "privateVisualCount": priv["visualCount"],
                "publicVisualCount": pub["visualCount"],
                "visualTypeCounts": type_delta,
            })
    return {
        "reference": "active locally supplied private PBIR snapshot; source path intentionally omitted",
        "privatePageCount": private_structure["pageCount"],
        "privateVisualCountReproduced": private_structure["visualCount"],
        "operatorReportedPrivateVisualCount": reported_private_visuals,
        "unreconciledReportedVisualDifference": reported_private_visuals - private_structure["visualCount"],
        "publicPageCount": len(public_pages),
        "publicVisualCount": sum(row["visualCount"] for row in public_details["pages"]),
        "samePageNamesAndOrder": [row["displayName"] for row in private_details["pages"]] == [row["displayName"] for row in public_details["pages"]],
        "pageVisualDifferences": page_differences,
        "themeNameMatches": private_structure["customThemeName"] == load_json(DEFAULT_REPORT / "definition/report.json").get("themeCollection", {}).get("customTheme", {}).get("name"),
        "themeContentMatches": private_structure["customThemeSha256"] == public_details["themeHash"],
        "semanticModelComparison": "Public aggregate-only relationships and DAX intentionally differ from private trade-level semantics; counts only, private definitions omitted.",
        "privateAuthoredTableCount": private_structure["authoredTableCount"],
        "publicAuthoredTableCount": public_structure["authoredTableCount"],
        "privateRelationshipCount": private_structure["relationshipCount"],
        "publicRelationshipCount": public_structure["relationshipCount"],
        "privateMeasureCount": private_structure["measureCount"],
        "publicMeasureCount": public_structure["measureCount"],
        "privateModelFormulasOrDataWritten": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-root", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--model-root", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--write-baseline", action="store_true", help="Explicitly refresh the public structural baseline")
    parser.add_argument("--private-report-root", type=Path)
    parser.add_argument("--private-model-root", type=Path)
    parser.add_argument("--reported-private-visuals", type=int, default=88)
    parser.add_argument("--parity-output", type=Path, default=DEFAULT_PARITY)
    args = parser.parse_args()

    current, details = report_structure(args.report_root, args.model_root)
    issues = []
    if current["pageCount"] != 14:
        issues.append(f"Public page count must remain 14, found {current['pageCount']}")
    if current["visualCount"] != 83:
        issues.append(f"Public visual count must remain 83, found {current['visualCount']}")
    if args.write_baseline:
        args.baseline.parent.mkdir(parents=True, exist_ok=True)
        args.baseline.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    elif args.baseline.exists():
        approved = load_json(args.baseline)
        for key, value in current.items():
            if approved.get(key) != value:
                issues.append(f"Public structure drift detected: {key}")
    else:
        issues.append(f"Missing approved structure baseline: {args.baseline.name}")

    parity = None
    if args.private_report_root:
        if not args.private_model_root:
            parser.error("--private-model-root is required with --private-report-root")
        parity = compare_private(args.private_report_root, args.private_model_root, current, details,
                                 args.reported_private_visuals)
        args.parity_output.parent.mkdir(parents=True, exist_ok=True)
        args.parity_output.write_text(json.dumps(parity, indent=2) + "\n", encoding="utf-8")

    result = {"publicStructure": current, "issues": issues, "privateParity": parity}
    print(json.dumps(result, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
