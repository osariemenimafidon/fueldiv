"""03 - Join the divergence register to the certified engine population.

The register (02) establishes which fuel properties are constrained at
certification and in the market. This script answers the question that makes
that structural finding concrete: HOW MANY real certified engine families were
certified under a test fuel that left a given property unconstrained, and what
does the certification record actually say about the fuel they were certified
on?

Input is CIDEX v1.0's processed panel, which must be built first. CIDEX is a
sibling project in the same programme; this script reads it read-only and never
writes into it.

Run:  python3 scripts/03_exposure.py --cidex ../cidex
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import re
import sys

OUT = "data/processed"
QA = "qa"

# Compression-ignition families. CIDEX carries two spellings of the cycle for
# the same thing because EPA's two source workbooks spell it differently; both
# are compression ignition and both belong in scope.
CI_CYCLES = {"4 Stroke Compression Ignition", "Diesel"}

# A metering system is volumetric when the quantity delivered is set by a
# commanded duration at a commanded pressure. Density error then becomes
# fuelling error directly, which is the pathway the register's density row
# describes.
VOLUMETRIC_DIESEL_METERING = re.compile(
    r"(direct|indirect)\s+diesel\s+injection|electronic direct injection",
    re.IGNORECASE,
)

# Every property the certification fuel descriptor is capable of expressing.
# Determined empirically from the distinct values in CIDEX, not assumed.
SULFUR_GRADE = re.compile(r"(\d+\s*-\s*\d+\s*ppm|\d+\s*ppm)", re.IGNORECASE)

# Markers that a certification fuel contained renewable or biodiesel content.
# If the certified population contains none of these, the certification fuel
# population is wholly petroleum distillate.
RENEWABLE_MARKERS = re.compile(
    r"\b(b\d{1,3}|biodiesel|fame|renewable|paraffinic|hvo|paraffin|ester)\b",
    re.IGNORECASE,
)


def read_csv(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cidex", default="../cidex",
                    help="path to the CIDEX project root")
    args = ap.parse_args()

    fam_path = os.path.join(args.cidex, "data/processed/cidex_family.csv")
    cfg_path = os.path.join(args.cidex, "data/processed/cidex_config.csv")
    for p in (fam_path, cfg_path):
        if not os.path.exists(p):
            raise SystemExit(
                f"MISSING: {p}\nBuild CIDEX first (its scripts 01-05), then rerun."
            )

    fam = read_csv(fam_path)
    cfg = read_csv(cfg_path)

    ci = [r for r in fam if r["engine_cycle"] in CI_CYCLES]
    volumetric = [r for r in ci
                  if VOLUMETRIC_DIESEL_METERING.search(r["fuel_metering_system"] or "")]

    # ---- what does the certification record say about the fuel? ----------
    fuel_descriptors = collections.Counter(
        r["fuel_type"] for r in ci if r["fuel_type"])
    cert_fuels = collections.Counter(
        r["certification_fuel"] for r in cfg if r["certification_fuel"])

    sulfur_only = sum(n for d, n in fuel_descriptors.items() if SULFUR_GRADE.search(d))
    renewable = {d: n for d, n in fuel_descriptors.items() if RENEWABLE_MARKERS.search(d)}
    renewable_cert = {d: n for d, n in cert_fuels.items() if RENEWABLE_MARKERS.search(d)}

    # ---- exposure -------------------------------------------------------
    # The certification test fuel specification in 40 CFR 1065.703 is universal:
    # it applies to every engine certified under part 1065. So a property the
    # spec leaves unconstrained is unconstrained for the ENTIRE certified
    # population. The exposure count is therefore the population count, and the
    # value of computing it is that it converts a structural claim into a
    # number a reader can check.
    register = read_csv(f"{OUT}/divergence_register.csv")
    exposure = []
    for row in register:
        if row["cert_constrained"] == "True":
            continue
        exposure.append({
            "property": row["property"],
            "injection_pathway": row["injection_pathway"],
            "gap_class": row["gap_class"],
            "ci_families_exposed": len(ci),
            "volumetric_metering_families_exposed": len(volumetric),
            "basis": "40 CFR 1065.703 applies to the whole certified population",
        })

    by_year = collections.Counter((r["panel"], r["model_year"]) for r in ci)
    with open(f"{OUT}/exposure_by_family.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["panel", "model_year", "ci_families",
                    "volumetric_metering_families"])
        vol_by_year = collections.Counter(
            (r["panel"], r["model_year"]) for r in volumetric)
        for (panel, my) in sorted(by_year):
            w.writerow([panel, my, by_year[(panel, my)], vol_by_year[(panel, my)]])

    with open(f"{OUT}/exposure_summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(exposure[0].keys()))
        w.writeheader()
        w.writerows(exposure)

    # ---- merge into stats.json -----------------------------------------
    with open(f"{OUT}/stats.json") as fh:
        stats = json.load(fh)

    stats["population"] = {
        "cidex_families_total": len(fam),
        "ci_families": len(ci),
        "volumetric_diesel_metering_families": len(volumetric),
        "volumetric_share_of_ci": round(len(volumetric) / len(ci), 4) if ci else None,
        "panels": sorted({r["panel"] for r in ci}),
        "model_year_range": [min(r["model_year"] for r in ci),
                             max(r["model_year"] for r in ci)],
    }
    stats["certification_fuel_record"] = {
        "distinct_fuel_type_descriptors": len(fuel_descriptors),
        "families_whose_descriptor_states_only_a_sulfur_grade": sulfur_only,
        "share_stating_only_sulfur_grade": round(sulfur_only / len(ci), 4) if ci else None,
        "families_certified_on_renewable_or_biodiesel_fuel": sum(renewable.values()),
        "config_records_certified_on_renewable_or_biodiesel_fuel": sum(renewable_cert.values()),
        "distinct_certification_fuel_values": sorted(cert_fuels),
        "note": (
            "The certification record's fuel field encodes sulfur grade. It has "
            "no field for density, cetane number, viscosity, bulk modulus, "
            "lubricity or FAME content."
        ),
    }
    stats["exposure"] = {
        e["property"]: e["ci_families_exposed"] for e in exposure}

    with open(f"{OUT}/stats.json", "w") as fh:
        json.dump(stats, fh, indent=2)

    qa = {
        "cidex_families_read": len(fam),
        "cidex_config_records_read": len(cfg),
        "ci_families": len(ci),
        "volumetric_metering_families": len(volumetric),
        "families_dropped_non_ci": len(fam) - len(ci),
        "distinct_fuel_type_descriptors": len(fuel_descriptors),
        "top_fuel_descriptors": fuel_descriptors.most_common(8),
        "distinct_certification_fuel_values": sorted(cert_fuels),
        "checks": {
            "ci_population_non_empty": len(ci) > 0,
            "every_ci_family_has_model_year": all(r["model_year"] for r in ci),
            "no_renewable_certification_fuel_found": sum(renewable_cert.values()) == 0,
        },
    }
    with open(f"{QA}/03_exposure.json", "w") as fh:
        json.dump(qa, fh, indent=2)

    print(f"CI families                      {len(ci):,} of {len(fam):,} CIDEX families")
    print(f"  volumetric diesel metering     {len(volumetric):,}")
    print(f"  model years                    {stats['population']['model_year_range'][0]}"
          f"-{stats['population']['model_year_range'][1]}")
    print()
    print(f"distinct fuel_type descriptors   {len(fuel_descriptors)}")
    print(f"  stating only a sulfur grade    {sulfur_only:,} "
          f"({sulfur_only / len(ci):.1%} of CI families)")
    print(f"  stating renewable/biodiesel    {sum(renewable.values())}")
    print()
    print("distinct certification_fuel values in the whole certified population:")
    for v in sorted(cert_fuels):
        print(f"  {cert_fuels[v]:6,d}  {v}")
    print()
    print("exposed population, by unconstrained property:")
    for e in exposure:
        print(f"  {e['property']:26s} {e['ci_families_exposed']:,} CI families "
              f"({e['gap_class']})")


if __name__ == "__main__":
    sys.exit(main())
