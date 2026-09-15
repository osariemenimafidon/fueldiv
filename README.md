# FUELDIV — Fuel Divergence Atlas

**Specification divergence between the diesel certification test fuel, the
federal in-market fuel requirement, and the fuels actually sold into the tank.**

Part of [FACET](https://osariemenimafidon.github.io/facet/) — Fuel-Adaptive
Control Evidence & Transferability.

Osariemen Imafidon · ORCID [0009-0006-3069-4674](https://orcid.org/0009-0006-3069-4674) · Independent Researcher

> **Status: verified. Not yet deposited.**
> The 24 values taken from paywalled consensus standards have been confirmed
> against the standards themselves, and the verification checklist is signed.
> No DOI has been minted yet. See `docs/VERIFICATION_CHECKLIST.md`.

---

## What this is

A compression-ignition engine is certified on a test fuel whose properties are
fixed by **40 CFR 1065.703**. It is then operated, for a useful life measured in
thousands of hours, on fuel that need only satisfy **40 CFR 1090** — a much
shorter list of requirements.

This project reads both, property by property, and records where they fail to
overlap. It then joins the result to the certified engine population from
[CIDEX](https://github.com/osariemenimafidon/cidex) so the structural finding
carries a population count rather than an adjective.

## Principal findings (draft)

Of ten injection-relevant fuel properties examined:

| | Count |
|---|---|
| Constrained at certification **and** in the market | 3 |
| Constrained at certification only | 3 |
| Constrained in neither | **4** |
| With published federal measurement of in-service values | **0** |

The four constrained in neither — **bulk modulus, lubricity, FAME content and
cloud point** — are not peripheral. Bulk modulus sets the propagation of the
pressure wave from pump to nozzle, and therefore the actual start of injection
relative to the commanded one. Lubricity sets the wear margin at the very
hardware that performs the injection.

Two further results:

- **Renewable diesel to EN 15940 lies wholly outside the certification fuel's
  density envelope.** The certification fuel is 838.9–864.6 kg/m³ (derived from
  API gravity 32–37 °API). EN 15940 paraffinic diesel is 765–800 kg/m³. The
  overlap is zero. Injection systems meter volume, so delivered mass tracks
  density directly.
- **No engine in the certified population was certified on a fuel containing any
  renewable or biodiesel content.** Across 8,354 compression-ignition engine
  families (MY2011–2027), the `certification_fuel` field takes four distinct
  values, three of which are sulfur grades of petroleum distillate. 99.2 % of
  families describe their certification fuel by sulfur grade alone.

That last point is the structural one. **The certification record has no field in
which density, cetane number, viscosity, bulk modulus, lubricity or FAME content
could be recorded.** The one fuel property the record reliably encodes — sulfur —
is the one property that is federally regulated, federally enforced and
federally measured. The record's data model mirrors the regulation's scope, and
both stop short of the properties that perturb the injection event.

**7,928 of the 8,354 families (94.9 %) use direct or indirect diesel injection** —
volumetric metering, where a density shift becomes a fuelling error before
anything else happens.

## Repository layout

```
data/reference/      declared inputs (none yet; v2.0 EIA volumes land here)
data/processed/      generated — register, overlap table, exposure, stats.json
docs/                build spec, codebook, limitations, verification checklist
logs/provenance.jsonl  every source retrieval, with citation
qa/                  machine-readable QA report per script
scripts/             numbered, run in order
src/fueldiv/         property conversions and envelope arithmetic
```

## Reproducing

Python 3.10+. The register and exposure steps use only the standard library;
`matplotlib` is needed for figures.

```bash
git clone https://github.com/osariemenimafidon/fueldiv
cd fueldiv
pip install -r requirements.txt

# CIDEX must be built first — it supplies the engine population.
# See https://github.com/osariemenimafidon/cidex
python3 scripts/01_provenance.py
python3 scripts/02_register.py
python3 scripts/03_exposure.py --cidex ../cidex
```

Expected output of step 2: 10 properties, 24 overlap rows, 4 unconstrained
properties, 1 disjoint envelope. Step 3: 8,354 CI families, 0 certified on
renewable or biodiesel fuel. If your numbers differ, CIDEX has been rebuilt from
a newer EPA file drop — which is a finding, not a failure. Record it.

## Getting the source data

**There is no bulk download for this project's primary sources.** The
certification fuel envelope and the in-market requirement are regulatory text,
read from the Code of Federal Regulations and transcribed into
`scripts/02_register.py` with a section citation on every value:

- 40 CFR 1065.703 Table 1 — <https://www.ecfr.gov/current/title-40/part-1065/section-1065.703>
- 40 CFR 1090.305 — <https://www.ecfr.gov/current/title-40/part-1090/section-1090.305>

Both are US Government works in the public domain. A rebuilder should open them
and check the transcription; that is verification point **V5**.

The engine population comes from CIDEX, which itself requires two EPA
certification workbooks downloaded by hand — `epa.gov` is unreachable from this
project's build environments under the operating organisation's egress policy.
CIDEX's README documents that procedure.

## What this project does not claim

It does not estimate what fuel any particular engine actually burned. It
establishes what the regulatory system constrains and measures, and what it does
not. The in-service distribution — the Atlas proper — is **v2.0**, and requires
EIA biofuel volume data not yet in hand. See `docs/BUILD_SPEC.md` §2.

It does not assert that an unconstrained property is out of specification in
practice. Refiners and blenders hold to consensus standards that constrain more
than federal law requires. The finding is about what is *guaranteed* to an engine
designer, not what is typical.

## Licence

Code: MIT (`LICENSE`). Data and documentation: CC BY 4.0 (`LICENSE-DATA`).
Regulatory text quoted from the CFR is a US Government work, not subject to
copyright.

## Citation

See `CITATION.cff`. A DOI will be minted on first Zenodo deposit, which will not
happen before the verification gate is passed.
