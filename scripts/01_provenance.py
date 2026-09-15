"""01 - Record provenance for every source this project reads.

FUELDIV's primary sources are regulatory text, not files. There is nothing to
hash. What a rebuilder needs instead is the exact citation, the retrieval date,
and the URL, so they can open the same provision and check the transcription
themselves. That is verification point V5.

The one hashable input is CIDEX's processed panel, which IS a file, and is
hashed so a reader can tell whether the exposure counts came from the same
CIDEX build the documents describe.
"""
import argparse, datetime, hashlib, json, os

LOG = "logs/provenance.jsonl"

TEXT_SOURCES = [
    {
        "kind": "regulatory_text",
        "citation": "40 CFR 1065.703 and Table 1 of 1065.703",
        "supplies": "certification test fuel property envelope",
        "url": "https://www.ecfr.gov/current/title-40/part-1065/section-1065.703",
        "publisher": "US Government Publishing Office / eCFR",
        "rights": "US Government work, public domain",
        "transcribed_into": "scripts/02_register.py",
    },
    {
        "kind": "regulatory_text",
        "citation": "40 CFR 1090.305, 40 CFR 1090.310, 40 CFR 1090 subpart D",
        "supplies": "federal in-market diesel fuel requirements",
        "url": "https://www.ecfr.gov/current/title-40/part-1090/section-1090.305",
        "publisher": "US Government Publishing Office / eCFR",
        "rights": "US Government work, public domain",
        "transcribed_into": "scripts/02_register.py",
    },
    {
        "kind": "regulatory_text",
        "citation": "40 CFR 1090 subpart O, sections 1090.1405, 1090.1410, 1090.1415",
        "supplies": "national fuels survey programme scope; basis for the "
                    "federal_public_measurement column",
        "url": "https://www.ecfr.gov/current/title-40/part-1090/subpart-O",
        "publisher": "US Government Publishing Office / eCFR",
        "rights": "US Government work, public domain",
        "transcribed_into": "scripts/02_register.py",
        "status": "confirmed V4 - diesel scope and publication status checked",
    },
    {
        "kind": "paywalled_standard",
        "citation": "ASTM D975, ASTM D7467, EN 590, EN 15940",
        "supplies": "commercial fuel envelopes",
        "url": "not freely available",
        "publisher": "ASTM International; CEN",
        "rights": "copyrighted; values transcribed as cited facts, text not reproduced",
        "transcribed_into": "scripts/02_register.py",
        "status": "confirmed V1 - every value checked against its standard",
    },
]


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cidex", default="../cidex")
    args = ap.parse_args()
    os.makedirs("logs", exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records = [dict(recorded_utc=now, **s) for s in TEXT_SOURCES]

    for rel in ("data/processed/cidex_family.csv", "data/processed/cidex_config.csv"):
        p = os.path.join(args.cidex, rel)
        if os.path.exists(p):
            st = os.stat(p)
            records.append({
                "recorded_utc": now, "kind": "derived_dataset",
                "citation": "CIDEX v1.0 (Imafidon 2026)", "file": rel,
                "bytes": st.st_size, "sha256": sha256(p),
                "url": "https://github.com/osariemenimafidon/cidex",
                "rights": "CC BY 4.0", "supplies": "certified engine population",
            })
        else:
            records.append({"recorded_utc": now, "kind": "derived_dataset",
                            "file": rel, "status": "MISSING - build CIDEX first"})

    with open(LOG, "a") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")
    for r in records:
        print(f"{r['kind']:20s} {r.get('citation', r.get('file'))}")
    print(f"\n{len(records)} records appended to {LOG}")


if __name__ == "__main__":
    main()
