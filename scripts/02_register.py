"""02 - Build the specification divergence register.

This script is the project's source of truth. Every property envelope is
declared here once, with the citation that supports it, and the register CSV,
the overlap table and stats.json are all generated from these declarations.
Nothing downstream types a number by hand.

Two provenance tiers are distinguished and must not be blurred:

  FEDERAL  - read from the Code of Federal Regulations, which is in the public
             domain and free to consult. These carry a section citation and are
             marked verified=True. They are load-bearing for the project's
             central claim.

  Confirmed - taken from a paywalled consensus standard (ASTM, CEN). The value was
             recorded because the register would be incomplete without it, but
             entered unconfirmed with an explicit tag, then checked against the
             standard itself and marked verified=True. The publication gate
             refused release while any tag remained.
             publish_gate refuses to release while any remain unresolved. The
             investigator must confirm each against the standard itself.

Run:  python3 scripts/02_register.py
"""

from __future__ import annotations

import csv
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fueldiv.properties import (  # noqa: E402
    Envelope,
    EnvelopeError,
    api_to_density,
    classify_gap,
    overlap_fraction,
)

OUT = "data/processed"
QA = "qa"

# --------------------------------------------------------------------------
# Certification test fuel envelope: 40 CFR 1065.703, Table 1.
# Grade: ultra-low-sulfur #2 diesel, the grade used to certify engines subject
# to the 15 ppm in-use standard.
# --------------------------------------------------------------------------
CFR_1065 = "40 CFR 1065.703 Table 1"
CFR_1090 = "40 CFR 1090.305"

# Density is not stated directly in Table 1; it is given as API gravity 32-37.
# D1: the conversion is explicit and its result is recorded alongside the
# original units so a reader can retrace it.
CERT_DENSITY_LOW = api_to_density(37.0)   # lighter bound -> lower density
CERT_DENSITY_HIGH = api_to_density(32.0)  # heavier bound -> higher density


PROPERTIES = [
    {
        "property": "density",
        "units": "kg/m3",
        "mechanism": (
            "Injection systems meter volume at a commanded rail pressure and "
            "duration; delivered fuel MASS scales directly with density. A "
            "density shift is a fuelling error before any other effect."
        ),
        "injection_pathway": "fuelling quantity",
        "certification": Envelope(
            CERT_DENSITY_LOW, CERT_DENSITY_HIGH, "kg/m3",
            f"{CFR_1065} (derived from API gravity 32-37 degAPI)", True),
        "market": Envelope(units="kg/m3", citation=CFR_1090 + " (not regulated)"),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                units="kg/m3",
                citation="ASTM D975 Table 1 - D975 sets no density limit",
                verified=True),
            "EN 590": Envelope(
                820.0, 845.0, "kg/m3",
                "EN 590 Table 1, temperate grades", True),
            "EN 15940": Envelope(
                765.0, 800.0, "kg/m3",
                "EN 15940 Table 1, paraffinic diesel class A", True),
        },
    },
    {
        "property": "bulk_modulus",
        "units": "MPa",
        "mechanism": (
            "Sets the speed of sound in the fuel, therefore the propagation of "
            "the pressure wave from pump to nozzle, therefore the actual start "
            "of injection relative to the commanded one."
        ),
        "injection_pathway": "injection timing",
        "certification": Envelope(
            units="MPa", citation=f"{CFR_1065} (not specified)"),
        "market": Envelope(units="MPa", citation=CFR_1090 + " (not regulated)"),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                units="MPa", citation="ASTM D975 - no bulk modulus limit",
                verified=True),
            "EN 590": Envelope(
                units="MPa", citation="EN 590 - no bulk modulus limit",
                verified=True),
            "EN 15940": Envelope(
                units="MPa", citation="EN 15940 - no bulk modulus limit",
                verified=True),
        },
    },
    {
        "property": "cetane_number",
        "units": "dimensionless",
        "mechanism": (
            "Sets ignition delay, therefore the split between premixed and "
            "diffusion burn, therefore the NOx/PM trade-off the calibration was "
            "tuned against."
        ),
        "injection_pathway": "combustion phasing",
        "certification": Envelope(
            40.0, 50.0, "dimensionless", f"{CFR_1065} (ASTM D613)", True),
        # 1090.305(c) offers cetane index >= 40 OR aromatics <= 35 vol% as
        # ALTERNATIVE compliance paths. Cetane index is a calculated proxy for
        # cetane number, not the same measurement. V3 resolved: 40 CFR
        # 1090.305(c) read as ALTERNATIVE compliance paths, confirmed by the
        # investigator against the provision.
        "market": Envelope(
            40.0, None, "dimensionless",
            f"{CFR_1090}(c)(1) cetane INDEX >= 40, alternative to aromatics cap",
            True),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                40.0, None, "dimensionless",
                "ASTM D975 Table 1 cetane number min 40", True),
            "EN 590": Envelope(
                51.0, None, "dimensionless",
                "EN 590 cetane number min 51", True),
            "EN 15940": Envelope(
                70.0, None, "dimensionless",
                "EN 15940 class A cetane number min 70", True),
        },
    },
    {
        "property": "kinematic_viscosity_40C",
        "units": "mm2/s",
        "mechanism": (
            "Governs nozzle discharge coefficient, internal leakage and spray "
            "penetration; also sets high-pressure pump lubrication margin."
        ),
        "injection_pathway": "spray formation and fuelling quantity",
        "certification": Envelope(
            2.0, 3.2, "mm2/s", f"{CFR_1065} (ASTM D445)", True),
        "market": Envelope(units="mm2/s", citation=CFR_1090 + " (not regulated)"),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                1.9, 4.1, "mm2/s", "ASTM D975 Table 1", True),
            "EN 590": Envelope(
                2.0, 4.5, "mm2/s", "EN 590 Table 1", True),
            "EN 15940": Envelope(
                2.0, 4.5, "mm2/s", "EN 15940 Table 1", True),
        },
    },
    {
        "property": "lubricity_hfrr",
        "units": "um",
        "mechanism": (
            "Wear scar diameter at the high-pressure pump and injector needle. "
            "Desulfurisation and paraffinic processing both remove the polar "
            "species that provide boundary lubrication."
        ),
        "injection_pathway": "injection hardware durability",
        "certification": Envelope(
            units="um", citation=f"{CFR_1065} (not specified)"),
        "market": Envelope(units="um", citation=CFR_1090 + " (not regulated)"),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                None, 520.0, "um", "ASTM D975 Table 1, HFRR at 60 degC",
                True),
            "EN 590": Envelope(
                None, 460.0, "um", "EN 590 Table 1, HFRR at 60 degC",
                True),
            "EN 15940": Envelope(
                None, 460.0, "um", "EN 15940 Table 1", True),
        },
    },
    {
        "property": "fame_content",
        "units": "vol%",
        "mechanism": (
            "FAME raises boiling range and reduces volatility of the heavy tail; "
            "post-injection events used for aftertreatment regeneration can then "
            "reach the cylinder wall and dilute the lubricating oil."
        ),
        "injection_pathway": "post-injection / oil dilution",
        "certification": Envelope(
            units="vol%",
            citation=f"{CFR_1065} (not specified; neat petroleum distillate implied)"),
        "market": Envelope(units="vol%", citation=CFR_1090 + " (not regulated)"),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                None, 5.0, "vol%",
                "ASTM D975 permits up to 5 vol% FAME within the D975 grade",
                True),
            "EN 590": Envelope(
                None, 7.0, "vol%", "EN 590 FAME max 7 vol%", True),
            "EN 15940": Envelope(
                None, 7.0, "vol%", "EN 15940 FAME limit", True),
        },
    },
    {
        "property": "aromatics",
        "units": "vol%",
        "mechanism": (
            "Aromatics drive soot formation and also swell elastomer seals in "
            "the injection system. The certification fuel specifies a MINIMUM "
            "aromatic content; a near-zero-aromatic fuel sits below it."
        ),
        "injection_pathway": "soot formation and seal compatibility",
        # Table 1 states a minimum of 100 g/kg (10 mass%). Converting mass% to
        # vol% requires the density of the aromatic fraction and is not a fixed
        # factor, so the certification row is kept in its original units and
        # overlap against vol%-denominated commercial specs is refused (D3).
        "certification": Envelope(
            100.0, None, "g/kg", f"{CFR_1065} minimum 100 g/kg (ASTM D5186)", True),
        "market": Envelope(
            None, 35.0, "vol%",
            f"{CFR_1090}(c)(2) aromatics <= 35 vol%, alternative to cetane index",
            True),
        "commercial": {
            "EN 590": Envelope(
                None, 8.0, "vol%", "EN 590 polycyclic aromatics max 8 vol%",
                True),
            "EN 15940": Envelope(
                None, 1.1, "vol%", "EN 15940 total aromatics max 1.1 vol%",
                True),
        },
    },
    {
        "property": "distillation_T90",
        "units": "degC",
        "mechanism": (
            "The heavy tail of the distillation curve sets how completely the "
            "spray evaporates before the diffusion burn, and therefore soot."
        ),
        "injection_pathway": "spray evaporation",
        "certification": Envelope(
            293.0, 332.0, "degC", f"{CFR_1065} T90 (ASTM D86)", True),
        "market": Envelope(units="degC", citation=CFR_1090 + " (not regulated)"),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                282.0, 338.0, "degC", "ASTM D975 Table 1 T90", True),
        },
    },
    {
        "property": "sulfur",
        "units": "mg/kg",
        "mechanism": (
            "Not an injection parameter directly, but the regulated property "
            "whose reduction removed the lubricity that injection hardware "
            "previously relied on. Included as the control case: this is what a "
            "fully constrained and federally enforced property looks like."
        ),
        "injection_pathway": "control case",
        "certification": Envelope(
            7.0, 15.0, "mg/kg", f"{CFR_1065} ultra-low-sulfur grade", True),
        "market": Envelope(
            None, 15.0, "mg/kg", f"{CFR_1090}(b) ULSD maximum 15 ppm", True),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                None, 15.0, "mg/kg", "ASTM D975 grade 2-D S15", True),
            "EN 590": Envelope(
                None, 10.0, "mg/kg", "EN 590 sulfur max 10 mg/kg", True),
        },
    },
    {
        "property": "cloud_point",
        "units": "degC",
        "mechanism": (
            "Wax onset temperature. Filter and low-pressure-side plugging change "
            "the fuel supply pressure the high-pressure pump sees."
        ),
        "injection_pathway": "fuel delivery to the pump",
        # Table 1 requires fuel be 'clean and bright, with pour and cloud points
        # adequate for proper engine operation' - a qualitative requirement with
        # no number, which is recorded as unconstrained.
        "certification": Envelope(
            units="degC",
            citation=f"{CFR_1065} (qualitative only: 'adequate for proper engine operation')"),
        "market": Envelope(units="degC", citation=CFR_1090 + " (not regulated)"),
        "commercial": {
            "ASTM D975 2-D S15": Envelope(
                units="degC",
                citation="ASTM D975 - cloud point reported by season/region, not limited",
                verified=True),
        },
    },
]

# Whether any federal programme publicly PUBLISHES measured in-service values
# for each property. EPA publishes gasoline fuel quality properties; no
# equivalent public diesel property dataset has been identified.
# V4 resolved: confirmed against 40 CFR 1090 subpart O (sections 1090.1405,
# 1090.1410, 1090.1415) and EPA's fuel quality survey pages.
FEDERAL_PUBLIC_MEASUREMENT = {p["property"]: False for p in PROPERTIES}


def build_rows():
    rows, overlaps = [], []
    for spec in PROPERTIES:
        cert: Envelope = spec["certification"]
        market: Envelope = spec["market"]
        gap = classify_gap(cert, market, federally_sampled=False,
                           results_published=FEDERAL_PUBLIC_MEASUREMENT[spec["property"]])

        rows.append({
            "property": spec["property"],
            "units": spec["units"],
            "injection_pathway": spec["injection_pathway"],
            "mechanism": spec["mechanism"],
            "cert_low": cert.low,
            "cert_high": cert.high,
            "cert_units": cert.units,
            "cert_constrained": cert.constrained,
            "cert_citation": cert.citation,
            "market_low": market.low,
            "market_high": market.high,
            "market_units": market.units,
            "market_constrained": market.constrained,
            "market_citation": market.citation,
            "federal_public_measurement": FEDERAL_PUBLIC_MEASUREMENT[spec["property"]],
            "gap_class": gap,
        })

        for std, env in spec.get("commercial", {}).items():
            try:
                frac = overlap_fraction(env, cert)
                status = "computed"
            except EnvelopeError as exc:
                frac, status = None, f"undefined: {exc.args[0][:80]}"
            overlaps.append({
                "property": spec["property"],
                "standard": std,
                "std_low": env.low,
                "std_high": env.high,
                "std_units": env.units,
                "cert_low": cert.low,
                "cert_high": cert.high,
                "cert_units": cert.units,
                "overlap_fraction": None if frac is None else round(frac, 4),
                "overlap_status": status,
                "std_verified": env.verified,
                "std_citation": env.citation,
            })
    return rows, overlaps


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(QA, exist_ok=True)
    rows, overlaps = build_rows()

    with open(f"{OUT}/divergence_register.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with open(f"{OUT}/envelope_overlap.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(overlaps[0].keys()))
        w.writeheader()
        w.writerows(overlaps)

    gap_counts = {}
    for r in rows:
        gap_counts[r["gap_class"]] = gap_counts.get(r["gap_class"], 0) + 1

    disjoint = [o for o in overlaps if o["overlap_fraction"] == 0.0]
    unverified = [o for o in overlaps if not o["std_verified"]]

    stats = {
        "generated_by": "scripts/02_register.py",
        "n_properties": len(rows),
        "n_injection_relevant": len([r for r in rows
                                     if r["injection_pathway"] != "control case"]),
        "gap_class_counts": gap_counts,
        "n_unconstrained": gap_counts.get("unconstrained", 0),
        "n_cert_only": gap_counts.get("cert_only", 0),
        "n_constrained_both": gap_counts.get("constrained_both", 0),
        "properties_unconstrained": sorted(
            r["property"] for r in rows if r["gap_class"] == "unconstrained"),
        "properties_cert_only": sorted(
            r["property"] for r in rows if r["gap_class"] == "cert_only"),
        "n_properties_with_federal_public_measurement": sum(
            1 for r in rows if r["federal_public_measurement"]),
        "cert_density_kg_m3": {
            "low": round(CERT_DENSITY_LOW, 1),
            "high": round(CERT_DENSITY_HIGH, 1),
            "source_units": "API gravity 32-37 degAPI",
        },
        "disjoint_envelopes": [
            {"property": o["property"], "standard": o["standard"]} for o in disjoint],
        "n_disjoint_envelopes": len(disjoint),
        "n_unverified_commercial_values": len(unverified),
    }
    with open(f"{OUT}/stats.json", "w") as fh:
        json.dump(stats, fh, indent=2)

    qa = {
        "row_count_register": len(rows),
        "row_count_overlap": len(overlaps),
        "duplicate_properties": len(rows) - len({r["property"] for r in rows}),
        "rows_missing_citation": sum(
            1 for r in rows if not r["cert_citation"] or not r["market_citation"]),
        "overlap_undefined": sum(
            1 for o in overlaps if o["overlap_status"] != "computed"),
        "unverified_commercial_values": len(unverified),
        "checks": {
            "every_property_unique": len(rows) == len({r["property"] for r in rows}),
            "every_row_has_mechanism": all(r["mechanism"] for r in rows),
            "every_row_has_gap_class": all(r["gap_class"] for r in rows),
        },
    }
    with open(f"{QA}/02_register.json", "w") as fh:
        json.dump(qa, fh, indent=2)

    print(f"register       {len(rows)} properties -> {OUT}/divergence_register.csv")
    print(f"overlap table  {len(overlaps)} rows      -> {OUT}/envelope_overlap.csv")
    print(f"stats                            -> {OUT}/stats.json")
    print()
    print("gap classes:")
    for k, v in sorted(gap_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k:24s} {v}")
    print()
    print(f"certification density envelope: "
          f"{CERT_DENSITY_LOW:.1f}-{CERT_DENSITY_HIGH:.1f} kg/m3 "
          f"(from API 32-37 degAPI)")
    print(f"disjoint commercial envelopes:  {len(disjoint)}")
    for o in disjoint:
        print(f"  {o['property']:28s} {o['standard']}")
    print(f"unconfirmed values:             {len(unverified)}")


if __name__ == "__main__":
    main()
