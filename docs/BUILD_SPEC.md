# FUELDIV — Build specification

**Project:** Fuel Divergence Atlas — Specification Divergence Register (v1.0)
**Program:** FACET (Fuel-Adaptive Control Evidence & Transferability)
**Investigator:** Osariemen Imafidon · ORCID 0009-0006-3069-4674 · Independent Researcher
**Spec written:** 2026-09-15
**Status:** Verified 2026-09-15 — checklist signed, not yet deposited

---

## 1. The question this project answers

For a compression-ignition engine certified under 40 CFR part 1065 and operated on
fuel sold under 40 CFR part 1090, **which injection-relevant fuel properties are
constrained at certification, which are constrained in the market, which are
measured and published by the federal government — and where do those three sets
fail to overlap?**

The program's §1 premise is that the certified-to-in-service fuel gap is widening.
That premise is currently supported in PROGRAM.md by property ranges drawn from
commercial fuel standards. This project establishes the part of the premise that
can be shown from **primary federal law alone**, which is the part no reviewer can
dispute and no paywall obstructs.

The finding this project tests is deliberately falsifiable:

> **H0:** Every fuel property that materially perturbs the injection event is
> either constrained at certification, constrained in the market, or measured in
> published federal data.

If H0 holds, the program's §1 premise weakens and FACET should say so. Initial
reading of 40 CFR 1065.703 and 40 CFR 1090 subpart D indicates H0 fails, but the
register is built to record the result either way.

## 2. Scope

- **Engine population:** heavy-duty highway (MY2017–2026) and nonroad
  compression-ignition (MY2012–2026), as delimited by CIDEX's usable ranges.
  Off-highway is in scope because its fuel-quality exposure is least constrained.
- **Fuel:** distillate diesel and its commercial substitutes and blends sold into
  the same tank — petroleum ULSD, FAME biodiesel blends, and paraffinic renewable
  diesel.
- **Out of scope for v1.0:** state-level in-service property estimates. Those
  require EIA volume data, which is not reachable from either build environment
  (see §7) and is deferred to v2.0.

## 3. Sources

| # | Source | What it supplies | Access | Vintage |
|---|---|---|---|---|
| S1 | 40 CFR 1065.703 + Table 1 | Certification test fuel property envelope | eCFR, free, public domain | current |
| S2 | 40 CFR 1090 subpart D (§1090.305, §1090.310) | Federal in-market diesel requirements | eCFR, free, public domain | current |
| S3 | CIDEX v1.0 processed panel | Certified engine family population to join against | local, CC BY 4.0 | v1.0.0 |
| S4 | ASTM D975, D7467; EN 590, EN 15940 | Commercial fuel spec envelopes | **paywalled** — see §6 | current |
| S5 | EPA fuel quality survey program | Whether diesel properties are sampled and whether results are published | EPA web, free | current |

Only S1–S3 are load-bearing for v1.0's central claim. S4 entered the register as
cited-but-unverified rows, since those standards are paywalled; the investigator
has since confirmed all 24 against the standards themselves and they are now
marked `verified=True` (§6).

## 4. Unit of analysis and measures

**Unit of analysis:** one *fuel property* × one *constraint regime*.

Regimes: `certification` (S1), `market` (S2), `commercial_spec` (S4),
`federal_measurement` (S5).

For each property the register records: mechanism of action on the injection
event; whether each regime constrains it; the numeric range where constrained;
the citation; and a derived **gap class**:

| Gap class | Meaning |
|---|---|
| `constrained_both` | Bounded at certification and in the market |
| `cert_only` | Bounded at certification, unbounded in market |
| `market_only` | Bounded in market, unbounded at certification |
| `unconstrained` | Bounded in neither |
| `sampled_unpublished` | Federally sampled but results not publicly released |

Derived measures:

- **Envelope overlap** — for a property bounded in more than one regime, the
  fraction of the commercial range lying inside the certification range.
  A value of 0 means a legally-sold fuel is wholly outside the certified envelope.
- **Exposed family count** — from CIDEX, the number of certified engine families
  whose certification did not constrain a given property, by panel and model year.

## 5. Outputs

| Output | File |
|---|---|
| Property register (machine-readable) | `data/processed/divergence_register.csv` |
| Envelope overlap table | `data/processed/envelope_overlap.csv` |
| Exposed-family counts joined to CIDEX | `data/processed/exposure_by_family.csv` |
| Statistics file (every number in every document) | `data/processed/stats.json` |
| QA report | `qa/*.json` |
| Figures | `figures/` |
| Codebook, limitations, verification checklist | `docs/` |
| Technical report | `docs/TECHNICAL_REPORT.md` → PDF |

## 6. Verification points — investigator must personally check

These are the points where the build cannot verify itself. Each is tagged
`[VERIFY]` in the register and will block `publish_gate` until resolved.

1. **V1 — Commercial spec values (S4).** ASTM D975, D7467, EN 590 and EN 15940 are
   paywalled. Every value taken from them is entered as `[VERIFY]` with the exact
   table and clause to check. **This includes the EN 590 (820–845 kg/m³) and
   EN 15940 (765–800 kg/m³) figures already asserted in PROGRAM.md**, which
   currently carry no citation in the program repository.
2. **V2 — API gravity to density conversion.** The certification envelope is
   stated in °API; density is derived as ρ = 999.016 × 141.5/(°API + 131.5).
   Confirm the conversion and the reference temperature convention (60 °F).
3. **V3 — The either/or reading of §1090.305(c).** The register treats cetane
   index ≥ 40 and aromatics ≤ 35 vol% as alternative compliance paths, not joint
   requirements. Confirm against the regulatory text.
4. **V4 — Fuel survey publication status (S5).** Confirm whether EPA's fuel
   quality survey program samples diesel properties and whether any diesel result
   is published, at what resolution. The `sampled_unpublished` gap class depends
   on this.
5. **V5 — Five spot checks.** Five register rows chosen by the investigator,
   traced by hand from the CFR text to the register cell.

## 7. Known environment constraint

`epa.gov`, `eia.gov`, `ecfr.gov`, `federalregister.gov` and `zenodo.org` are all
blocked by egress policy from **both** the cloud container and the device shell;
only `github.com` is reachable. Consequences:

- Regulatory text was read through a retrieval tool, not fetched to disk. Every
  CFR citation in the register therefore carries section and paragraph so the
  investigator can confirm it directly in a browser.
- v2.0's EIA volume data must be downloaded manually, as CIDEX's raw EPA files
  were.
- The Zenodo deposit cannot be executed from either environment. It will be
  prepared as a guided procedure in `docs/PUBLISH_GUIDE.md`.

## 8. Licence

Data and documentation: CC BY 4.0. Code: MIT. Consistent with CIDEX and FACET.

## 9. Target venues

1. Zenodo deposit with DOI — the citable home for the register.
2. Open preprint (engrXiv, or arXiv eess.SY) for the descriptor.
3. Future EPA docket comment when the next heavy-duty or nonroad fuel or
   certification rule opens for comment. The register is the evidence base for
   the comment that the certification fuel envelope no longer brackets the
   in-service fuel population.
