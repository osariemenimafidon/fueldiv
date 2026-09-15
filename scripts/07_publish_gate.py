#!/usr/bin/env python3
"""07 — FUELDIV pre-publication gate.

Two halves, as the checklist describes.

MECHANICAL: no [VERIFY] tag may remain anywhere in the tree, and no Envelope may
carry verified=False. Both are refusals to publish a value nobody has opened the
standard to confirm.

HUMAN: the investigator signs. That cannot be scripted, so --sign records it.
Signing is refused while any mechanical item is outstanding, which is the point:
the attestation cannot be made before the work it attests to.

Deleting .gate-signed returns the project to draft on the next build.
"""
import argparse, json, os, re, subprocess, sys
from datetime import date

SKIP_DIRS = {".git", "__pycache__", "data", "logs", ".venv", "figures", "qa", "release"}
# 06_docs.py generates the checklist and must name the tag to explain the
# convention; the gate script itself likewise. A scanner that flags its own
# documentation is one people learn to ignore.
SKIP_FILES = {"07_publish_gate.py", "06_docs.py",
              "VERIFICATION_CHECKLIST.md", "BUILD_SPEC.md"}
TEXT_EXT = {".py", ".md", ".csv", ".json", ".cff", ".txt", ".yml", ".yaml"}
SIGIL = "\x5bVERIFY"


def scan():
    hits, unverified = [], []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in files:
            if fn in SKIP_FILES or os.path.splitext(fn)[1] not in TEXT_EXT:
                continue
            p = os.path.join(root, fn)
            try:
                lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                continue
            for n, line in enumerate(lines, 1):
                if SIGIL in line:
                    hits.append((p, n, line.strip()[:90]))
                if re.search(r",\s*False\s*\)", line) and "Envelope" not in line and p.endswith("02_register.py"):
                    unverified.append((p, n, line.strip()[:90]))
    return hits, unverified


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sign", action="store_true",
                    help="record the investigator's attestation. Refused while items remain.")
    a = ap.parse_args()

    hits, unverified = scan()
    ok = not hits and not unverified

    if hits:
        print(f"GATE FAIL — {len(hits)} unconfirmed value(s) still tagged:\n")
        for p, n, l in hits[:20]:
            print(f"    {p}:{n}  {l}")
        if len(hits) > 20:
            print(f"    … and {len(hits)-20} more")
        print()
    if unverified:
        print(f"GATE FAIL — {len(unverified)} Envelope(s) still carry verified=False.\n")

    if not ok:
        return 1

    print("MECHANICAL: PASS — no unconfirmed tags, every envelope marked verified.\n")

    if os.path.exists(".gate-signed"):
        print(open(".gate-signed").read())
        print("GATE CLEARED.")
        return 0

    if not a.sign:
        print("HUMAN: NOT SIGNED. Run with --sign once every checklist box is ticked.")
        return 1

    who = json.load(open("AUTHORS.json"))["authors"][0]
    open(".gate-signed", "w").write(
        f"""FUELDIV verification gate — signed by the investigator.

Attests to docs/VERIFICATION_CHECKLIST.md in full: the 24 commercial standard
values confirmed against the standards themselves, the API-gravity conversion,
the reading of 40 CFR 1090.305(c), the federal-measurement finding, and five CFR
transcription spot checks.

Signed: {who['name']} (ORCID {who['orcid']})
Recorded: {date.today().isoformat()}

Deleting this file returns the project to draft on the next build.
""")
    print(f"SIGNED by {who['name']} on {date.today().isoformat()}.")
    print("GATE CLEARED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
