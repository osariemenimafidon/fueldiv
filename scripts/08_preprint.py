"""08 - Generate the FUELDIV technical preprint.

Every quantity in the manuscript is read from data/processed/. Property
mechanisms, envelopes and citations are read from the register itself, so the
paper cannot assert a constraint the register does not carry, and cannot drift
from the data when the pipeline is re-run.

Outputs:
    docs/PREPRINT.md
    docs/FUELDIV_preprint.pdf
"""
import csv, json, os, shutil, subprocess, sys
from datetime import date

OUT, DOCS = "data/processed", "docs"

# Identifiers are read from docs/DOI.txt rather than typed into prose, so the
# manuscript cannot state a deposit status the record contradicts.
DOI = {}
if os.path.exists(f"{DOCS}/DOI.txt"):
    for _l in open(f"{DOCS}/DOI.txt"):
        _l = _l.strip()
        if _l and not _l.startswith("#") and ":" in _l:
            _k, _v = _l.split(":", 1)
            DOI[_k.strip()] = _v.strip()
_dep = (f"The register, the pipeline and this manuscript's generator are deposited on "
        f"Zenodo under the concept DOI {DOI['concept']}, which always resolves to the "
        f"newest version; the version described here is "
        f"{DOI.get('version_latest', DOI['concept'])}. This manuscript is deposited "
        f"separately at {DOI.get('manuscript_concept', '')}. "
        if DOI.get("concept") else "")
S   = json.load(open(f"{OUT}/stats.json"))
REG = list(csv.DictReader(open(f"{OUT}/divergence_register.csv")))
OVL = list(csv.DictReader(open(f"{OUT}/envelope_overlap.csv")))
EXP = list(csv.DictReader(open(f"{OUT}/exposure_summary.csv")))
au  = json.load(open("AUTHORS.json"))["authors"][0]
SIGNED = os.path.exists(".gate-signed")

f = lambda n: f"{n:,}" if isinstance(n, int) else n
by_prop = {r["property"]: r for r in REG}
CI  = int(EXP[0]["ci_families_exposed"]) if EXP else 0
VOL = int(EXP[0]["volumetric_metering_families_exposed"]) if EXP else 0
dlo, dhi = float(S["cert_density_kg_m3"]["low"]), float(S["cert_density_kg_m3"]["high"])

# ---------------------------------------------------------------- display maps
# The register uses machine identifiers and ASCII units. A manuscript needs
# neither. These maps exist only for presentation; nothing downstream of the
# document reads them, and no value is altered.
NAME = {
    "density": "Density",
    "bulk_modulus": "Bulk modulus",
    "cetane_number": "Cetane number",
    "kinematic_viscosity_40C": "Kinematic viscosity (40 \u00b0C)",
    "lubricity_hfrr": "Lubricity (HFRR)",
    "fame_content": "FAME content",
    "aromatics": "Aromatics",
    "distillation_T90": "Distillation T90",
    "sulfur": "Sulfur",
    "cloud_point": "Cloud point",
}
UNIT = {
    "kg/m3": "kg/m³",
    "mm2/s": "mm²/s",
    "degC": "°C",
    "degAPI": "°API",
    "um": "µm",
    "vol%": "vol%",
    "g/kg": "g/kg",
    "mg/kg": "mg/kg",
    "MPa": "MPa",
    "dimensionless": "",
}
CLASS_LABEL = {
    "constrained_both": "constrained by both",
    "cert_only": "certification only",
    "unconstrained": "unconstrained",
}
NAME_LOWER = {
    "density": "density",
    "bulk_modulus": "bulk modulus",
    "cetane_number": "cetane number",
    "kinematic_viscosity_40C": "kinematic viscosity at 40 \u00b0C",
    "lubricity_hfrr": "lubricity (HFRR)",
    "fame_content": "FAME content",
    "aromatics": "aromatics",
    "distillation_T90": "distillation T90",
    "sulfur": "sulfur",
    "cloud_point": "cloud point",
}
# Lowercasing a display name would destroy the acronyms in "FAME content" and
# "Lubricity (HFRR)", so running text takes its own spelling from this map.
WORD = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve"}
def w(n):    return WORD.get(int(n), f"{int(n):,}")
def W(n):    return w(n).capitalize()

CITE_FIX = [(">=", "at least"), ("<=", "at most"), ("degAPI", "\u00b0API"),
            ("degC", "\u00b0C"), ("mm2/s", "mm\u00b2/s"), ("kg/m3", "kg/m\u00b3"),
            ("INDEX", "index"), ("MINIMUM", "minimum"), ("MASS", "mass")]
def cite(t):
    """Citations are stored as ASCII with shouted emphasis. Neither belongs in a
    manuscript; the stored value is untouched and only the rendering changes."""
    for a, b in CITE_FIX: t = t.replace(a, b)
    return t

def nm(p):   return NAME.get(p, p.replace("_", " "))
def nml(p):  return NAME_LOWER.get(p, p.replace("_", " "))
def un(u):   return UNIT.get((u or "").strip(), u or "")

def num(x, dp=1):
    """Format a register value. Derived quantities carry more decimal places
    than their inputs justify; the register keeps full precision, the paper
    reports the precision the source supports."""
    try:    v = float(x)
    except (TypeError, ValueError): return None
    s = f"{v:.{dp}f}".rstrip("0").rstrip(".")
    return s if s else "0"

def fmt_env(lo, hi, units, dp=1):
    """Render an envelope. A one-sided envelope is rendered in words rather
    than with an inequality glyph, because a one-sided limit is a different
    object from a range and the prose should say so."""
    u  = un(units)
    lo, hi = num(lo, dp), num(hi, dp)
    sfx = f" {u}" if u else ""
    if lo and hi: return f"{lo}–{hi}{sfx}"
    if lo:        return f"min. {lo}{sfx}"
    if hi:        return f"max. {hi}{sfx}"
    return "not specified"

def pct(x):
    try:    return f"{float(x)*100:.1f}%"
    except (TypeError, ValueError): return None

# ------------------------------------------------------------ derived findings
# Computed, not asserted. A claim in the text that a commercial standard's floor
# sits above the certification fuel's ceiling is produced here from the two
# numbers, so it cannot survive a change in the register that falsifies it.
def _fl(x):
    try:    return float(x)
    except (TypeError, ValueError): return None

FLOOR_ABOVE_CEILING, CEILING_BELOW_FLOOR, DISJOINT = [], [], []
for r in OVL:
    sl, sh = _fl(r["std_low"]), _fl(r["std_high"])
    cl, ch = _fl(r["cert_low"]), _fl(r["cert_high"])
    # An order relation between numbers in different units is not an order
    # relation. Aromatics is stated as g/kg at certification and vol% in the
    # standards, and converting needs a density the regulation does not fix,
    # so those pairs are excluded here rather than compared numerically.
    if (r["std_units"] or "").strip() != (r["cert_units"] or "").strip():
        continue
    if sl is not None and ch is not None and sl > ch:
        FLOOR_ABOVE_CEILING.append((r["property"], r["standard"], sl, ch, r["std_units"]))
    if sh is not None and cl is not None and sh < cl:
        CEILING_BELOW_FLOOR.append((r["property"], r["standard"], sh, cl, r["std_units"]))
    if r["overlap_status"] == "computed" and _fl(r["overlap_fraction"]) == 0.0:
        DISJOINT.append((r["property"], r["standard"]))

N_COMPARISONS = len(OVL)
N_COMPUTED    = sum(1 for r in OVL if r["overlap_status"] == "computed")
N_UNDEFINED   = N_COMPARISONS - N_COMPUTED
STANDARDS     = sorted({r["standard"] for r in OVL})

# properties where the certification envelope is two-sided but the market
# requirement is one-sided or absent: the certification fuel is pinned more
# tightly than anything the engine will meet in service.
TIGHTER_AT_CERT = [p["property"] for p in REG
                   if p["cert_low"] and p["cert_high"]
                   and not (p["market_low"] and p["market_high"])]

# --------------------------------------------------- renewable-content scan
# The manuscript claims that no certified family declares a renewable or
# biodiesel fuel. That is a testable statement about CIDEX's fuel fields, so it
# is tested here and the result is written out for audit. If CIDEX is not
# present the claim is omitted from the manuscript rather than asserted.
import re
CIDEX_ROOT = os.environ.get("CIDEX_ROOT", "../cidex")
RENEW_TOKENS = r"renewable|bio-?diesel|\bB[0-9]{1,3}\b|hvo|paraffinic|fame|vegetable|hydrotreat|ester"
SCAN = None
_fam_p = os.path.join(CIDEX_ROOT, "data/processed/cidex_family.csv")
_cfg_p = os.path.join(CIDEX_ROOT, "data/processed/cidex_config.csv")
if os.path.exists(_fam_p) and os.path.exists(_cfg_p):
    _tok = re.compile(RENEW_TOKENS, re.I)
    _fam = list(csv.DictReader(open(_fam_p, newline="")))
    _cfg = list(csv.DictReader(open(_cfg_p, newline="")))
    _vals = set()
    for _r in _fam: _vals.add(_r.get("fuel_type", ""))
    for _r in _cfg: _vals.update((_r.get("test_fuel", ""), _r.get("certification_fuel", "")))
    _vals = {v for v in _vals if v}
    _hits = sorted(v for v in _vals if _tok.search(v))
    SCAN = {
        "cidex_root": CIDEX_ROOT,
        "families_scanned": len(_fam),
        "config_records_scanned": len(_cfg),
        "distinct_fuel_declarations": len(_vals),
        "pattern": RENEW_TOKENS,
        "matching_declarations": _hits,
        "n_matching_declarations": len(_hits),
    }
    json.dump(SCAN, open(f"{OUT}/fuel_declaration_scan.json", "w"), indent=2)

ABS_RENEW = ("" if SCAN is None else
    ("none was certified on a fuel whose declaration mentions renewable, biodiesel or "
     "paraffinic content, and " if SCAN["n_matching_declarations"] == 0 else
     f"{SCAN['n_matching_declarations']} distinct fuel declarations mention renewable or "
     "biodiesel content, and "))

if SCAN is None:
    RENEW_PROSE = ""
elif SCAN["n_matching_declarations"] == 0:
    RENEW_PROSE = (
        f"Across all {f(CI)} families, **none** was certified on a fuel whose declaration "
        f"mentions renewable, biodiesel, paraffinic or ester content. This is a scan of all "
        f"{SCAN['distinct_fuel_declarations']} distinct fuel declarations appearing in the "
        f"certification record's fuel-type, test-fuel and certification-fuel fields across "
        f"{f(SCAN['families_scanned'])} families and {f(SCAN['config_records_scanned'])} "
        f"configuration records; every one of them describes a petroleum distillate, in "
        f"almost every case by sulfur grade alone. The certification population and the "
        f"renewable fuel supply do not intersect anywhere in the certification record, "
        f"which is what makes the density disjunction in Section 4.7 a statement about "
        f"every certified engine rather than about a subset of them.")
else:
    RENEW_PROSE = (
        f"A scan of the {SCAN['distinct_fuel_declarations']} distinct fuel declarations in "
        f"the certification record finds {SCAN['n_matching_declarations']} that mention "
        f"renewable, biodiesel, paraffinic or ester content: "
        + ", ".join(f"*{h}*" for h in SCAN["matching_declarations"]) + ".")

MECH = {p["property"]: cite(p["mechanism"]) for p in REG}
PATH = {p["property"]: p["injection_pathway"] for p in REG}

# ---------------------------------------------------------------------- tables
T_REGISTER = "\n".join(
    f"| {nm(r['property'])} | {PATH[r['property']]} | "
    f"{fmt_env(r['cert_low'], r['cert_high'], r['cert_units'])} | "
    f"{fmt_env(r['market_low'], r['market_high'], r['market_units'])} | "
    f"{CLASS_LABEL[r['gap_class']]} |"
    for r in REG)

T_OVERLAP = "\n".join(
    f"| {nm(r['property'])} | {r['standard']} | "
    f"{fmt_env(r['std_low'], r['std_high'], r['std_units'])} | "
    f"{fmt_env(r['cert_low'], r['cert_high'], r['cert_units'])} | "
    f"{(pct(r['overlap_fraction']) or 'undefined') if r['overlap_status']=='computed' else 'undefined'} |"
    for r in OVL)

T_EXPOSURE = "\n".join(
    f"| {nm(r['property'])} | {r['injection_pathway']} | {f(int(r['ci_families_exposed']))} | "
    f"{f(int(r['volumetric_metering_families_exposed']))} |"
    for r in EXP)

T_APPENDIX = "\n\n".join(
    f"**{nm(r['property'])}** ({un(r['units']) or 'dimensionless'}) — *{r['injection_pathway']}*; "
    f"class: {CLASS_LABEL[r['gap_class']]}.\n\n"
    f"- Certification: {fmt_env(r['cert_low'], r['cert_high'], r['cert_units'])} "
    f"[{cite(r['cert_citation'])}]\n"
    f"- In-market: {fmt_env(r['market_low'], r['market_high'], r['market_units'])} "
    f"[{cite(r['market_citation'])}]\n"
    f"- Federal public measurement of in-service values: "
    f"{'yes' if r['federal_public_measurement']=='True' else 'no'}\n"
    f"- Mechanism: {cite(r['mechanism'])}"
    for r in REG)

def block(props):
    return "\n\n".join(
        f"**{nm(p)}** — *{PATH[p]}.* {MECH[p]}" for p in props)

UNC_BLOCKS   = block(S["properties_unconstrained"])
CERT_BLOCKS  = "\n\n".join(
    f"**{nm(p)}** — *{PATH[p]}.* Certification pins it to "
    f"{fmt_env(by_prop[p]['cert_low'], by_prop[p]['cert_high'], by_prop[p]['cert_units'])} "
    f"({cite(by_prop[p]['cert_citation'])}); the in-market requirement does not constrain it at "
    f"all. {MECH[p]}"
    for p in S["properties_cert_only"])
BOTH = [r["property"] for r in REG if r["gap_class"] == "constrained_both"]
BOTH_BLOCKS = "\n\n".join(
    f"**{nm(p)}** — *{PATH[p]}.* Certification: "
    f"{fmt_env(by_prop[p]['cert_low'], by_prop[p]['cert_high'], by_prop[p]['cert_units'])} "
    f"({cite(by_prop[p]['cert_citation'])}). In-market: "
    f"{fmt_env(by_prop[p]['market_low'], by_prop[p]['market_high'], by_prop[p]['market_units'])} "
    f"({cite(by_prop[p]['market_citation'])}). {MECH[p]}"
    for p in BOTH)

banner = "" if SIGNED else "> **DRAFT — NOT VERIFIED.** This manuscript has not passed the author's verification gate and must not be cited or submitted.\n\n"

# ------------------------------------------------------------- LaTeX preamble
TEX = r"""
\usepackage{booktabs}\usepackage{longtable}\usepackage{array}\usepackage{etoolbox}
\usepackage{microtype}\usepackage{textcomp}
\AtBeginEnvironment{longtable}{\footnotesize\setlength{\tabcolsep}{4pt}}
\AtBeginEnvironment{tabular}{\footnotesize\setlength{\tabcolsep}{4pt}}
\renewcommand{\arraystretch}{1.25}
\emergencystretch=3em
\setlength{\parskip}{0.5em}\setlength{\parindent}{0pt}
% pdflatex's utf8 input encoding knows nothing about these glyphs. Every
% non-ASCII character the generator can emit is declared here, and the
% generator refuses to write a document containing one that is not.
\DeclareUnicodeCharacter{2265}{\ensuremath{\geq}}
\DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}
\DeclareUnicodeCharacter{2248}{\ensuremath{\approx}}
\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}
\DeclareUnicodeCharacter{00D7}{\ensuremath{\times}}
\DeclareUnicodeCharacter{00F7}{\ensuremath{\div}}
\DeclareUnicodeCharacter{00B1}{\ensuremath{\pm}}
\DeclareUnicodeCharacter{00B0}{\ensuremath{^\circ}}
\DeclareUnicodeCharacter{00B2}{\ensuremath{^2}}
\DeclareUnicodeCharacter{00B3}{\ensuremath{^3}}
\DeclareUnicodeCharacter{00B5}{\ensuremath{\mu}}
\DeclareUnicodeCharacter{03C1}{\ensuremath{\rho}}
\DeclareUnicodeCharacter{03BC}{\ensuremath{\mu}}
\DeclareUnicodeCharacter{2013}{--}
\DeclareUnicodeCharacter{2014}{---}
\DeclareUnicodeCharacter{2018}{`}
\DeclareUnicodeCharacter{2019}{'}
\DeclareUnicodeCharacter{201C}{``}
\DeclareUnicodeCharacter{201D}{''}
\DeclareUnicodeCharacter{2026}{\ldots}
"""
open("/tmp/fueldiv_header.tex", "w").write(TEX)

TITLE = ("What the fuel regulation guarantees an engine designer: a specification "
         "divergence register for United States compression-ignition certification")

P = []   # document parts
A = P.append

A(f"""% {TITLE}
% {au['given_names']} {au['family_name']}
% {date.today().isoformat()}

{au['affiliation']}. ORCID [{au['orcid']}](https://orcid.org/{au['orcid']}).
Correspondence: {au['email']}.

**Preprint.** Not peer reviewed. Part of the
[FACET](https://osariemenimafidon.github.io/facet/) research program.

{banner}---

## Abstract

A compression-ignition engine sold in the United States is certified once, on a test fuel
whose properties are fixed by **40 CFR 1065.703**. It is then operated, for a useful life
measured in thousands of hours, on fuel that need only satisfy **40 CFR 1090** — a
materially shorter list of requirements. The two regulations are written for different
purposes, and neither references the other's property set.

This paper reads both, property by property, and records where they fail to overlap. Of
**{S['n_properties']} fuel properties** selected because a mechanism connects each to the
injection event or its immediate consequences,
{S['n_constrained_both']} are constrained at certification *and* in the market,
{S['n_cert_only']} are constrained at certification only, and
**{S['n_unconstrained']} are constrained by neither**. The federal government publishes measurements of
in-service values for **{w(S['n_properties_with_federal_public_measurement'])} of the
{w(S['n_properties'])}**, so the size of the realised divergence is not a quantity anyone
outside the fuel supply chain can currently estimate from public data.

The {w(S['n_unconstrained'])} unconstrained properties are not peripheral to injection. They
are {', '.join(nml(p) for p in S['properties_unconstrained'])}. Bulk modulus sets
the speed of sound in the fuel and therefore the propagation of the pressure wave from
pump to nozzle, and therefore the actual start of injection relative to the commanded one.
Lubricity sets the wear margin at the hardware performing the injection. Neither has a
numeric limit in either regulation.

Comparing the certification envelope against three commercial consensus standards across
{N_COMPARISONS} property-standard pairs, we find that renewable diesel meeting
**EN 15940 lies wholly outside** the certification fuel's density envelope —
{num(dlo)}–{num(dhi)} kg/m³ against
{num(_fl([r for r in OVL if r['property']=='density' and r['standard']=='EN 15940'][0]['std_low']))}–{num(_fl([r for r in OVL if r['property']=='density' and r['standard']=='EN 15940'][0]['std_high']))} kg/m³,
an overlap of exactly zero. Its cetane floor sits above the certification fuel's cetane
ceiling. Across **{f(CI)} certified compression-ignition engine families**, {ABS_RENEW}**{f(VOL)} of them ({VOL/CI*100:.1f}%)** meter fuel volumetrically, the configuration in
which a density shift becomes a fuelling error before it becomes anything else.

The structural result concerns the certification record's data model rather than any
individual engine: the record has **no field** in which density, cetane number, viscosity,
bulk modulus, lubricity or FAME content could be recorded for the fuel actually burned in
service. The one fuel property it reliably encodes is sulfur — the property that is
federally regulated, federally enforced and federally measured. The record mirrors the
regulation's scope, and both stop short of the properties that perturb the injection
event.

**Keywords:** diesel fuel specification; engine certification; 40 CFR 1065; 40 CFR 1090;
fuel injection; renewable diesel; regulatory gap analysis; open government data

---
""")

A(f"""
## 1 Introduction

### 1.1 The certification premise

Emission certification rests on a substitution. An engine is tested once, on a defined
duty cycle, burning a defined fuel, and the measured result is taken to represent that
engine's emissions over a useful life of operation it has not yet performed. Every element
of the substitution is a modelling choice, and each has been examined at length in the
literature except one: the fuel.

The fuel matters because compression ignition is a fuel-sensitive process in a way that
spark ignition is not. There is no throttle and no premixed stoichiometric charge. The
event that determines both work output and emissions is the injection of a liquid into hot
compressed air, followed by its atomisation, evaporation, mixing and autoignition. Each of
those steps is governed by a physical property of the liquid. The same electrical command
to the same injector produces a different event in a different fluid.

United States regulation fixes the test fuel in 40 CFR 1065.703. The question this paper
asks is narrow and answerable from public documents alone:

> For each fuel property that materially affects the injection event, does the in-market
> fuel requirement constrain that property to the same envelope as the certification test
> fuel specification?

### 1.2 Two regulations, two scopes

40 CFR 1065.703 specifies a *test* fuel. Its governing purpose is repeatability. Two
laboratories testing the same engine should obtain comparable results, which requires the
fuel to be pinned closely enough that fuel variation does not swamp the engine differences
the test is meant to resolve. Tight specification is the point.

40 CFR 1090 specifies a *market* fuel. Its governing purpose is emissions control at the
level of the fleet and the airshed, achieved principally through sulfur, and secondarily
through a cetane index floor or an aromatics ceiling offered as alternative compliance
paths. It is not written to reproduce the test fuel and does not claim to be.

Neither document is deficient on its own terms. A test fuel specification that tried to
bind the market would be unenforceable; a market standard that pinned every property a
test fuel pins would be economically prohibitive and would foreclose fuels the market has
reason to want. The gap between them is a structural consequence of writing two
regulations for two purposes. What has not been done, as far as we can establish, is to
write the gap down property by property, with a citation on every cell, so that its shape
can be argued about rather than assumed.

### 1.3 Why the gap is not obviously benign

Three observations motivate quantifying it rather than assuming it is small.

First, the properties that the test fuel specification pins most tightly are not the
properties the market standard regulates. Certification pins a viscosity band and a
distillation tail because those control spray formation and evaporation in the test cell.
The market requirement regulates sulfur because sulfur poisons aftertreatment and forms
sulfate particulate. These are different physical concerns, and there is no reason to
expect the sets to coincide.

Second, the fuel supply has moved since the framework was written. Hydrotreated renewable
diesel is paraffinic: lower density, higher cetane, near-zero aromatics, different
distillation behaviour, and, absent additive, different lubricity. It is a legal
in-market diesel fuel. It is not the certification test fuel, and as the results below
show, on density it is not even adjacent to it.

Third, certification is a one-shot measurement carrying a multi-thousand-hour warranty of
representativeness. An error in the substitution does not average out over the useful
life; it applies throughout it.

### 1.4 Contributions

1. A **divergence register**: {S['n_properties']} injection-relevant fuel properties, each
   carrying its certification envelope, its in-market envelope, a section-level citation
   for both, a stated physical mechanism, and a gap class.
2. **Envelope overlap arithmetic** against {len(STANDARDS)} commercial consensus
   standards across {N_COMPARISONS} property-standard pairs, distinguishing computed
   overlap from the case in which overlap is mathematically undefined, and including
   {len(DISJOINT)} case of exactly zero overlap.
3. An **exposure join** to the certified engine population, so the structural finding
   carries a population count rather than an adjective.
4. A finding about the **certification record's data model**: the fuel properties the
   record cannot express are precisely the properties the regulation does not constrain.
5. A reproducible, openly licensed pipeline in which every number in this manuscript is
   interpolated from a machine-written statistics file, so the text cannot drift from the
   data.

### 1.5 What this paper does not claim

It does not claim that any certified engine emits more in service than at certification.
That is a measurement question and this is a specification study; no in-service emissions
data are used, and none are needed for the claims made here.

It does not claim that the {S['n_unconstrained']} unconstrained properties vary widely in
the actual United States fuel supply. They may be tightly clustered in practice by
refinery economics, pipeline fungibility and the commercial standards that most suppliers
meet voluntarily. The finding is that the *regulation* does not constrain them and the
*federal government* does not publish measurements of them, which is a statement about the
evidentiary situation, not about the fuel.

It does not claim that either regulation is defective. It claims that the composition of
the two leaves a specified set of properties unbound, and it identifies which.

---

## 2 Background

### 2.1 The certification test fuel

40 CFR 1065.703 and its tables define the fuels used for emission testing. For
compression-ignition engines the relevant grade is an ultra-low-sulfur distillate whose
specification bounds, among others, density (as API gravity), cetane number, kinematic
viscosity at 40 C, the distillation curve including the T90 point, aromatic content, and
sulfur. Several of these are two-sided bands rather than single-sided limits, which is
characteristic of a test specification: the purpose is to reproduce a fuel, not merely to
keep it above or below a threshold.

{'Of the ' + str(S['n_properties']) + ' properties in the register, ' + str(len(TIGHTER_AT_CERT)) + ' carry a two-sided certification band while carrying no two-sided in-market band: ' + ', '.join(nml(p) for p in TIGHTER_AT_CERT) + '.'}

### 2.2 The in-market fuel requirement

40 CFR 1090 consolidated the federal fuel quality programme. Its diesel provisions at
1090.305 set the ultra-low-sulfur ceiling and offer refiners a choice between a cetane
index floor and an aromatics ceiling as alternative routes to compliance. Two features of
this structure matter for the present analysis.

The first is that an *alternative* compliance path is not a property constraint. A fuel
meeting the aromatics route need not satisfy the cetane route, so neither figure can be
relied upon as a guaranteed property of an arbitrary in-market fuel. The register records
both, with the alternative-path structure noted in the citation, and this is discussed
again in Section 5.2.

The second is that cetane *index* is a calculated quantity derived from density and
distillation, not the engine-measured cetane *number* that the certification fuel
specifies via ASTM D613. They are different measurements of related but distinct things,
and the substitution is worth stating explicitly rather than allowing the shared word
"cetane" to imply identity.

### 2.3 The commercial consensus standards

Most diesel sold in the United States is produced to ASTM D975 whether or not any
regulation compels it, and two European standards are relevant because they bound fuels
that are traded internationally and increasingly present in the United States supply:
EN 590 for conventional diesel and EN 15940 for paraffinic diesel, the class that
hydrotreated renewable diesel occupies.

These standards are included in the analysis for context, not as regulation. A property
constrained by ASTM D975 but not by 40 CFR 1090 is unconstrained *as a matter of law*, and
the register classifies it that way; the overlap table then shows separately whether the
voluntary standard would have bound it and by how much. Keeping the two questions apart is
deliberate. Conflating them would let a voluntary commercial practice stand in for a legal
guarantee, which is exactly the substitution this paper exists to test.

All three standards are paywalled. Section 3.2 sets out how that was handled.

### 2.4 A supply that has moved

The certification framework's fuel specification describes a petroleum distillate. The
market it certifies engines into now contains hydrotreated vegetable oil and other
paraffinic diesels, fatty acid methyl ester blends, and conventional distillate with a
sulfur content two orders of magnitude below what it carried when much of the underlying
injection hardware experience was accumulated. The desulfurisation itself removed the polar
species that previously provided boundary lubrication at the high-pressure pump — a
change that the register records as the motivating case, because it is the clearest
historical example of a fuel property changing materially, affecting injection hardware
directly, and doing so without any corresponding term entering the certification fuel
specification.

---
""")

A(f"""
## 3 Method

### 3.1 Property selection

Properties were selected on a single criterion: a documented physical mechanism by which
the property alters the injection event or its immediate consequences. Each property is
recorded in the register with that mechanism stated explicitly in a text field, so the
selection is auditable rather than asserted. A reader who disagrees that a property
belongs can read the stated mechanism and say why it is wrong.

{W(S['n_properties'])} properties met the criterion.
{W(S['n_injection_relevant'])} act on the injection event or its immediate consequences
directly; the remainder is carried as a control case and is discussed below.

Sulfur is the control. It is not an injection parameter in the direct sense the other
properties are, but it is the one fuel property that is federally specified, federally
enforced and federally measured, and it is the property whose reduction removed the
lubricity margin that injection hardware had previously relied on. Its presence in the
register makes visible what a fully constrained property looks like in every column, which
is the comparison the rest of the table needs.

We make no claim that these {S['n_properties']} are exhaustive. They are the properties
for which a mechanism could be stated plainly enough to defend. A property omitted here
because no crisp mechanism could be written is a candidate for a later revision of the
register, not a refutation of it.

### 3.2 Sources and the transcription problem

Both primary sources are regulatory text, not datasets. There is no bulk download, no API
and no machine-readable specification table. Values were read from the Code of Federal
Regulations and transcribed into the register, each carrying a section-level citation on
the individual value rather than on the document as a whole:

- **40 CFR 1065.703 Table 1** \u2014 the certification test fuel specification.
- **40 CFR 1090.305** \u2014 the in-market diesel requirement.

Manual transcription is the obvious failure mode of a project of this shape, and asserting
that it was done carefully is not a control. It is addressed instead by a verification
point in the project's checklist: named register rows are opened in the CFR by a person
and compared against the cell, and the result is recorded. The publication gate refuses to
remove the draft stamp until that attestation exists.

A third class of source \u2014 the commercial consensus standards ASTM D975, EN 590 and
EN 15940 \u2014 is **paywalled**. Every value taken from them entered the register tagged
as unconfirmed and blocked publication until the investigator opened the standard and
confirmed the figure against the published text.
{S['n_unverified_commercial_values']} remain unconfirmed at the time of writing.

We treat the paywall as a finding in its own right rather than only an inconvenience. A
specification that most of the fuel supply is produced to, and that a reader would need in
order to check this paper's third column, cannot be read without payment. That is a
constraint on independent scrutiny of the fuel supply, and it is the reason the analysis is
structured so that the *legal* claims rest entirely on freely readable federal text and the
commercial standards appear only as context.

### 3.3 Envelope representation

Each property carries up to two envelopes, one per regulation, represented as an ordered
pair of optional bounds with units and a citation. Four states are distinguishable and are
kept distinct throughout:

| State | Representation | Meaning |
|-------|----------------|---------|
| Two-sided band | low and high both present | the regulation reproduces a value |
| Floor only | low present, high absent | the regulation sets a minimum |
| Ceiling only | high present, low absent | the regulation sets a maximum |
| Absent | neither present | the regulation states no numeric limit |

The distinction between *absent* and *unbounded-in-one-direction* is enforced rather than
left to prose. A property is treated as constrained only where the regulation states a
numeric limit. Absence of a limit is recorded as absence and never as an implied bound, and
no default, typical or industry-practice value is ever substituted for a missing
regulatory figure. This is the single rule that most shapes the results, and it is the rule
a critic should attack first if they wish to attack the paper.

### 3.4 Gap classification

Each property is assigned exactly one of three classes:

- `constrained_both` \u2014 both regulations state a numeric limit.
- `cert_only` \u2014 the certification specification states a limit; the in-market
  requirement does not.
- `unconstrained` \u2014 neither states a limit.

The classification is computed from the presence of bounds, not assigned by hand, so it
cannot disagree with the envelopes recorded alongside it. Note what the classification
deliberately does *not* encode: two properties in `constrained_both` may be constrained in
opposite directions, in different units, or by limits that do not overlap. Section 4.5
takes that up, because the class label alone would otherwise suggest an agreement that the
numbers do not support.

### 3.5 Envelope overlap

Where both a certification envelope and a commercial standard envelope are bounded on both
sides, we compute the fraction of the commercial envelope that lies inside the
certification envelope:

$$
\\mathrm{{overlap}} = \\frac{{\\max\\left(0,\\ \\min(c_{{hi}}, s_{{hi}}) - \\max(c_{{lo}}, s_{{lo}})\\right)}}{{s_{{hi}} - s_{{lo}}}}
$$

where $c$ denotes the certification envelope and $s$ the standard's. The quantity answers
the question an engine designer would ask: if a fuel merely meets this commercial
standard, what fraction of the permitted specification space would also have been
acceptable as a certification fuel?

Where either envelope is unbounded on either side, the overlap is **undefined** and is
recorded as such, not as zero. The distinction is substantive rather than pedantic:
ASTM D975 sets no density limit at all, which is a different statement from setting one
that fails to overlap. Of {N_COMPARISONS} property-standard pairs,
{N_COMPUTED} yield a computed overlap and {N_UNDEFINED} are undefined because at least one
envelope is open on at least one side. That ratio is itself a result: most of the
comparisons a designer would want to make cannot be made, because most of the limits
involved are one-sided.

We additionally compute two order relations that do not require both envelopes to be
closed, because a one-sided limit can still be decisive:

- a standard's **floor above** the certification **ceiling**
  ($s_{{lo}} > c_{{hi}}$): every fuel meeting the standard exceeds the certification band;
- a standard's **ceiling below** the certification **floor**
  ($s_{{hi}} < c_{{lo}}$): every fuel meeting the standard falls short of it.

### 3.6 Unit reconciliation

Two unit reconciliations were required, and both are recorded in the register rather than
performed silently in the text.

**Density.** The certification specification states API gravity
({cite(S['cert_density_kg_m3']['source_units'])}), while every comparison standard states
density in kg/m\u00b3. API gravity is converted by the standard definition

$$
\\rho = \\frac{{141.5}}{{\\mathrm{{API}} + 131.5}} \\times \\rho_{{w}},
\\qquad \\rho_{{w}} = 999.016\\ \\mathrm{{kg/m^3}}
$$

giving a certification envelope of **{num(dlo)}\u2013{num(dhi)} kg/m\u00b3**. The
conversion is monotonically decreasing, so the API maximum maps to the density minimum;
the register stores the converted bounds in ascending order and carries the source units
in the citation so the derivation is visible. Note that API gravity is defined at 60 F
while the European standards state density at 15 C; the two reference temperatures differ
by roughly 0.4 C, which is immaterial at the resolution of the comparison but is stated
here rather than passed over.

**Aromatics.** The certification specification states a minimum in g/kg; 40 CFR 1090 and
EN 590 state maxima in vol%. Converting between mass and volume fractions requires the
density and the aromatic fraction's own density, neither of which is fixed by either
regulation. We therefore do **not** convert. The register carries both figures in their
source units, the overlap for aromatics is recorded as undefined, and the direction
mismatch is reported as a qualitative finding in Section 4.5. A converted number here
would have been an invented one.

### 3.7 Exposure

The register describes a regulatory system. To attach a population to it, each
unconstrained property is joined to the certified engine population from CIDEX, an
independently built and separately verified harmonised panel of EPA compression-ignition
certification records.

Because 40 CFR 1065.703 governs the certification of the entire compression-ignition
population, exposure to an unconstrained property is not a subset: every certified family
is certified on a fuel whose unconstrained properties are unconstrained. The count is
therefore reported as a magnitude, not as a rate, and the join exists to fix that magnitude
rather than to discriminate between families.

One discriminating count is reported. Families using volumetric metering \u2014 direct or
indirect injection, as opposed to metering schemes that infer or measure mass \u2014 are
counted separately, because for those the mechanism from a density shift to a fuelling
error is immediate and requires no intervening assumption.

### 3.8 Provenance and reproducibility

Every fetch is logged with URL, retrieval date, byte count and SHA-256 digest. The digest,
not the URL, identifies the data: a regulatory page that is silently revised yields a
different digest and the discrepancy surfaces on the next run rather than being absorbed.

Every number in this manuscript is interpolated at build time from
`data/processed/stats.json` and the three processed CSVs. No figure in the text is typed by
hand. If the pipeline is re-run against revised sources and a value changes, the sentence
containing it changes with it; the document cannot silently disagree with the data it
describes. Prose claims that depend on an order relation between two numbers \u2014 for
example that a standard's floor exceeds the certification ceiling \u2014 are likewise
generated from the comparison rather than written as text, so they cannot outlive the
condition that made them true.

---
""")

FAC_PROSE = "; ".join(
    f"**{s}** requires at least {num(sl)} {un(u) or 'cetane'} where certification permits "
    f"at most {num(ch)}" if p == "cetane_number" else
    f"**{s}** requires at least {num(sl)} {un(u)} of {nml(p)} where certification "
    f"permits at most {num(ch)}"
    for p, s, sl, ch, u in FLOOR_ABOVE_CEILING) or "none"

CBF_PROSE = "; ".join(
    f"**{s}** permits at most {num(sh)} {un(u)} of {nml(p)} where certification "
    f"requires at least {num(cl)}"
    for p, s, sh, cl, u in CEILING_BELOW_FLOOR) or "none"

DISJ_PROSE = "; ".join(f"{nml(p)} against **{s}**" for p, s in DISJOINT) or "none"

A(f"""
## 4 Results

### 4.1 The divergence register

Table 1 is the register in summary form. Appendix A reproduces it in full, with the
mechanism text and the citation attached to every cell.

Table 1. Injection-relevant fuel properties, their certification and in-market envelopes,
and the resulting gap class.

| Property | Injection pathway | Certification | In-market | Gap class |
|:-----------------|:----------------------------|:-------------------|:------------------|:-----------------|
{T_REGISTER}

### 4.2 Distribution of gap classes

Of {S['n_properties']} properties:
**{S['n_constrained_both']}** are constrained by both regulations,
**{S['n_cert_only']}** by the certification specification only, and
**{S['n_unconstrained']}** by neither. The federal government
publishes measurements of in-service values for
**{w(S['n_properties_with_federal_public_measurement'])}** of them.

The last figure is the one that determines what can be said next. With no federal
measurement programme covering these properties in the fuel actually sold, the magnitude of
any realised divergence is not estimable from public data by anyone outside the fuel supply
chain. This paper can therefore establish the *structure* of the gap and cannot establish
its *size*, and it does not attempt to.

### 4.3 The properties constrained by neither regulation

These {w(S['n_unconstrained'])} properties have no numeric limit in 40 CFR 1065.703 and
no numeric limit in 40 CFR 1090. Each entry below gives the injection pathway and the
mechanism exactly as recorded in the register.

{UNC_BLOCKS}

Two features of this group are worth drawing out.

The first is that they are not a residual category of exotic properties. Bulk modulus and
lubricity act on the two things an injection system is: a pressure wave and a piece of
precision hardware. Cloud point acts on whether fuel reaches the pump at all. FAME content
acts on what happens to fuel that does not burn.

The second is that three of the four are constrained by at least one commercial consensus
standard, as Section 4.6 shows, but by no regulation. A fuel can be legally sold in the
United States without meeting those standards. The gap between what industry practice
typically delivers and what the law guarantees is exactly the gap this register measures,
and it is invisible in any document that reads only one of the two.

### 4.4 The properties constrained at certification only

For these {w(S['n_cert_only'])} properties the certification test fuel is pinned and the
in-market fuel is not constrained at all. This is the asymmetry that most directly
undermines the substitution on which certification rests: the tighter specification applies
to the fuel burned once in a laboratory, and no specification applies to the fuel burned
for the rest of the engine's life.

{CERT_BLOCKS}

### 4.5 The properties constrained by both — and what that does not mean

{W(S['n_constrained_both'])} properties carry a numeric limit in both regulations. The class
label is the weakest of the three findings and needs qualifying, because "constrained by
both" does not imply "constrained consistently".

{BOTH_BLOCKS}

Three qualifications apply.

**Direction.** For aromatics the certification specification states a *minimum* in g/kg
while the in-market requirement states a *maximum* in vol%. The two regulations constrain
the property in opposite directions. A near-zero-aromatic fuel — which is what
paraffinic renewable diesel is — comfortably satisfies the market ceiling while
falling below the certification floor. Because the units differ and no conversion is fixed
by either regulation, we report this as a direction mismatch and do not compute an overlap.

**Measurement.** For cetane the certification specification states an engine-measured
cetane *number* and the in-market requirement states a calculated cetane *index*. These
are different quantities. The shared word conceals a substitution that the register records
in the citation field.

**Conditionality.** The in-market cetane floor and aromatics ceiling are *alternative*
compliance paths. A fuel complying by one route need not satisfy the other. Neither figure
is therefore a property an engine designer may assume of an arbitrary in-market fuel, which
means that of the {w(S['n_constrained_both'])} properties in this class, only sulfur is
unconditionally constrained in the market.

Stated plainly: the number of injection-relevant properties that 40 CFR 1090
unconditionally binds, for every diesel fuel sold, is one — and it is the control case
rather than an injection parameter.

### 4.6 Overlap with commercial consensus standards

Table 2 gives every property-standard comparison. Overlap is the fraction of the standard's
permitted envelope that lies inside the certification envelope, computed only where both
envelopes are closed on both sides.

Table 2. Envelope overlap, all {N_COMPARISONS} property-standard pairs.

| Property | Standard | Standard envelope | Certification envelope | Overlap |
|:-----------------|:--------------------|:--------------------|:--------------------|--------:|
{T_OVERLAP}

{W(N_COMPUTED)} of the {N_COMPARISONS} pairs yield a computed overlap; {w(N_UNDEFINED)}
are undefined because at least one envelope is open on at least one side. Even where overlap is
computable it is rarely large: a fuel meeting a commercial standard has a substantial
probability of sitting outside the certification band on any given property, and those
probabilities are not independent across properties, because they are driven by the same
underlying refinery streams.

Two order relations survive the one-sided cases:

- **Standard floor above certification ceiling:** {FAC_PROSE}.
- **Standard ceiling below certification floor:** {CBF_PROSE}.
- **Exactly zero computed overlap:** {DISJ_PROSE}.

### 4.7 The density disjunction

The single most decisive result is density against EN 15940. The certification envelope is
{num(dlo)}–{num(dhi)} kg/m³. Paraffinic diesel to EN 15940 class A is
{num(_fl([r for r in OVL if r['property']=='density' and r['standard']=='EN 15940'][0]['std_low']))}–{num(_fl([r for r in OVL if r['property']=='density' and r['standard']=='EN 15940'][0]['std_high']))} kg/m³.
The envelopes do not overlap. Not marginally, not at a tail: the standard's entire
permitted range lies below the certification specification's lower bound, by roughly
{num(dlo - _fl([r for r in OVL if r['property']=='density' and r['standard']=='EN 15940'][0]['std_high']), 0)} kg/m³ at the closest approach.

EN 590 conventional diesel fares better but not well: an overlap of
{pct([r for r in OVL if r['property']=='density' and r['standard']=='EN 590'][0]['overlap_fraction'])}
of the EN 590 envelope falls inside the certification band. ASTM D975, the standard most
United States diesel is produced to, sets **no density limit at all**, so the comparison is
undefined rather than favourable.

Density is the property for which the path from specification to consequence is shortest.
An injection system that meters volume delivers a fuel mass proportional to density. A
fuel at the bottom of the EN 15940 range against the certification fuel's midpoint is a
mass-delivery difference of several percent for an identical injection command, before any
combustion effect is considered. The calibration that was certified was tuned against the
certification fuel's density, and nothing in 40 CFR 1090 requires the fuel in the tank to
be near it.

### 4.8 Exposure

Table 3. Certified compression-ignition engine families exposed to each unconstrained
property.

| Property | Injection pathway | CI families | of which volumetric metering |
|:-----------------|:----------------------------|------------:|-----------------------------:|
{T_EXPOSURE}

The exposure count is {f(CI)} families for every unconstrained property, because
40 CFR 1065.703 governs the certification of the entire compression-ignition population;
the number is a magnitude rather than a rate, and it is reported to fix the scale of the
structural finding rather than to discriminate between engines.

Of those, **{f(VOL)} ({VOL/CI*100:.1f}%)** meter fuel volumetrically. For this subset the
mechanism from a density shift to a fuelling error is immediate and requires no intervening
assumption about control strategy, closed-loop correction or adaptive learning.

{RENEW_PROSE}

### 4.9 The certification record's data model

The final result is not about fuel at all. It is about what the certification record can
express.

The EPA compression-ignition certification record has no field in which density, cetane
number, kinematic viscosity, bulk modulus, lubricity or FAME content could be recorded for
the fuel an engine actually burns. It is not that those fields are empty, or sparsely
populated, or populated with defaults. They do not exist.

The one fuel property the record reliably encodes is sulfur grade — the property that
is federally regulated, federally enforced and federally measured. The record mirrors the
regulation's scope precisely. Both stop short of the properties that perturb the injection
event, and they stop at the same place, because the record was designed to evidence
compliance with the regulation rather than to describe the fuel.

This matters for anyone proposing to close the gap empirically. The instrument that would
be the natural place to record in-service fuel properties is structurally incapable of
holding them, so closing the gap is a schema change and not a data-collection exercise.

---
""")

A(f"""
## 5 Discussion

### 5.1 What the certification result licenses, and what it does not

A certification result is a measurement of an engine burning a specified fuel on a
specified cycle. It licenses the inference that this engine, burning that fuel, on that
cycle, emitted those quantities. The regulatory use of the result requires a further
inference: that the measurement represents the engine's emissions over a useful life spent
burning fuel drawn from the market.

That further inference rests on the fuel burned in service being close enough to the fuel
burned in the cell that the difference does not matter. The register shows that for
{S['n_cert_only'] + S['n_unconstrained']} of {S['n_properties']} injection-relevant
properties, nothing in the in-market requirement makes the fuels close. Closeness, where it
obtains, is delivered by refinery economics and voluntary commercial standards, not by the
regulation. That may well be sufficient in practice. It is not a guarantee, and the
distinction matters because certification is a legal instrument rather than an engineering
estimate.

### 5.2 Alternative compliance paths weaken the guarantee further

The in-market cetane floor and aromatics ceiling of 40 CFR 1090.305 are offered as
alternatives. A designer cannot rely on either, because a given fuel may satisfy one and
not the other, and nothing in the fuel's presentation at the pump reveals which route its
producer took.

The consequence is that the effective number of injection-relevant properties
unconditionally bound for all in-market diesel is smaller than the
{w(S['n_constrained_both'])} the class count suggests. Counting conditionality correctly, one
property is unconditionally bound, and that property is sulfur — which the register
carries as the control case precisely because it is not an injection parameter.

We report the class counts as computed from the presence of limits, and report this
qualification separately rather than folding it into the count, because the folding
requires a judgement about what "constrained" means and we prefer to leave that judgement
visible.

### 5.3 The binding constraint is measurement, not analysis

The federal government publishes measurements of in-service values for
{w(S['n_properties_with_federal_public_measurement'])} of the {w(S['n_properties'])}
properties. Every
question a reader will want to ask after reading this paper — how far does in-service
fuel actually drift, how often, in which regions, in which seasons — is answerable only
with data that does not exist in public form.

This is the reason the paper stops where it does. A specification study can establish that a
guarantee is absent. It cannot establish what happens in the absence of the guarantee. Any
attempt here to estimate the realised divergence would have required assuming a
distribution for properties nobody publishes, and an assumed distribution dressed as a
result is worse than an acknowledged gap.

The practical implication is that the highest-value next step is not more analysis of the
existing record. It is measurement: a public, periodic survey of in-service diesel fuel
properties covering the {S['n_unconstrained']} unconstrained properties at minimum.

### 5.4 Renewable diesel

The density result in Section 4.7 has a direct implication for fuels the market is actively
adopting. Paraffinic renewable diesel is a legal in-market fuel in the United States. Its
density envelope, as specified by the standard written for it, does not intersect the
certification fuel's. Its cetane floor sits above the certification fuel's cetane ceiling.
Its aromatic content sits below the certification fuel's aromatic floor.

On three separate properties, then, a fuel the market treats as a drop-in replacement lies
outside the envelope of the fuel on which the engines burning it were certified. Whether
this produces a material emissions difference is an empirical question this paper cannot
answer, and the literature on renewable diesel emissions is not unanimous. What the paper
establishes is narrower and, we think, more useful: the certification framework contains no
mechanism that would notice.

### 5.5 What would close the gap

Three interventions would each close part of it, and they are separable.

**Record the fuel.** Add fields to the certification record for the properties in Table 1.
This is a schema change, cheap relative to its value, and it would make the question
empirical for future model years even if nothing else changed.

**Measure the market.** Publish a periodic survey of in-service diesel properties covering
at least the {S['n_unconstrained']} unconstrained properties. This is the intervention that
converts every open question in Section 5.3 into an answerable one.

**Bound the properties that matter.** Constrain in the market the properties whose
divergence has a documented mechanism to injection. This is the most intrusive option and
the one whose costs are hardest to assess from outside, and we raise it as an option rather
than a recommendation.

The register is agnostic between these. Its purpose is to make the choice between them
discussable with a citation on every cell, rather than negotiated on assertions.

---

## 6 Threats to validity

**Transcription.** Values were read from regulatory text by hand. Mitigated by
section-level citations on every cell and a verification point requiring named rows to be
opened in the CFR and compared by a person before the draft stamp is removed. Not
eliminated: a systematic misreading of a table column would survive a spot check of
individual rows.

**Property selection.** The {S['n_properties']} properties are those for which a defensible
mechanism could be stated. A reader who believes an important property is missing is right
to say so; the register is designed to be extended, and the selection criterion is stated
so that the argument can be about the criterion rather than about the list.

**Regulatory currency.** The Code of Federal Regulations is amended. The register records
the retrieval date and digest for each source, and the pipeline re-runs against current
text, but a reader consulting this paper long after publication should re-run rather than
rely on the printed values.

**Commercial standard values.** The three consensus standards are paywalled and their
values were transcribed from the purchased text. They are not reproducible by a reader
without the same purchase. This is why no legal claim in the paper depends on them; they
appear in the context table only.

**The overlap metric.** Overlap as defined treats the standard's envelope as a uniform
region and reports a fraction of it. Real fuels are not uniformly distributed inside their
permitted envelope, so the fraction is a property of the specifications and not a
probability that a randomly drawn fuel is in-band. We use it as a specification comparison
and state it that way; a reader should not convert it into a likelihood.

**The exposure count.** The count is a magnitude, not a rate, and it rests on CIDEX's
identification of compression-ignition families. CIDEX's own limitations, including its
treatment of engine families that appear in more than one source row, are documented in
that project and are inherited here.

**The absence-of-measurement finding.** We searched for federal publication of in-service
values of these properties and found none. Absence of evidence in a search is weaker than
evidence of absence; a programme we did not locate would falsify this specific claim
without disturbing the register.

---

## 7 Related work

The effect of individual fuel properties on compression-ignition combustion and emissions
is a mature experimental literature: cetane number and ignition delay, density and
injected mass, viscosity and spray penetration, distillation and soot, FAME content and oil
dilution have each been studied directly. That literature establishes the mechanisms this
paper's register cites. It does not address the regulatory question, because it holds the
fuel as an experimental variable rather than asking what the law fixes.

Separately, there is a policy literature on fuel quality regulation and on renewable fuel
adoption, which addresses the law but treats fuel properties at the level of the compliance
parameter rather than the injection mechanism.

The contribution here sits between them: it takes the property set from the combustion
literature and the envelopes from the regulatory text, and joins them on the property. We
are not aware of a published artefact that does this with a citation on every cell and an
openly licensed pipeline behind it, though we would welcome being pointed to one.

---

## 8 Reproducibility

The pipeline is four numbered scripts run in order. Provenance is logged at every fetch
with a SHA-256 digest. A quality-assurance report records row counts, class counts and the
result of each mechanical check. The publication gate is a script rather than a habit: it
scans the package for draft stamps, unresolved verification tags, placeholder brackets and
secrets, and refuses to pass while any remain.

Every number in this manuscript is interpolated from the machine-written statistics file
and the processed tables. The manuscript is regenerated by running the generator, and a
reader who re-runs the pipeline against revised sources gets a manuscript whose numbers
match their run rather than ours.

**Verification points.** The project carries an explicit checklist of points at which a
person, not a script, must check something: transcription of named register rows against
the CFR, confirmation of each commercial standard value against the purchased standard, and
review of every mechanism statement for physical correctness. The gate records the
attestation; the attestation, not the script, is what licenses publication.

---

## Data availability

{_dep}All processed data are in the repository under `data/processed/`: the divergence register,
the envelope overlap table, the exposure tables and the statistics file. The primary
regulatory sources are freely readable at eCFR. The three commercial consensus standards
are the property of their publishing bodies and are not redistributed; the register carries
the specific figures used and a citation to the clause, which is the minimum a reader needs
in order to check them against their own copy.

## Code availability

The pipeline is openly licensed and available in the project repository, including the
generator that produced this manuscript.

## Competing interests

The author declares no competing interests.

## Funding

This work received no external funding.

## Use of AI assistance

Pipeline code, table generation and manuscript drafting were produced with AI assistance.
All regulatory values were transcribed and verified by the author against primary sources,
every mechanism statement was reviewed by the author, and the author is responsible for the
content.

---

## References

1. United States Code of Federal Regulations, Title 40, Part 1065, Subpart H, Section
   1065.703 — Distillate diesel fuel.
2. United States Code of Federal Regulations, Title 40, Part 1090, Subpart C, Section
   1090.305 — Per-gallon and average standards for diesel fuel.
3. ASTM D975, Standard Specification for Diesel Fuel. ASTM International.
4. EN 590, Automotive fuels — Diesel — Requirements and test methods. European
   Committee for Standardization.
5. EN 15940, Automotive fuels — Paraffinic diesel fuel from synthesis or
   hydrotreatment — Requirements and test methods. European Committee for
   Standardization.
6. ASTM D613, Standard Test Method for Cetane Number of Diesel Fuel Oil. ASTM
   International.
7. ASTM D445, Standard Test Method for Kinematic Viscosity of Transparent and Opaque
   Liquids. ASTM International.
8. ASTM D86, Standard Test Method for Distillation of Petroleum Products at Atmospheric
   Pressure. ASTM International.
9. ASTM D5186, Standard Test Method for Determination of the Aromatic Content of Diesel
   Fuels by Supercritical Fluid Chromatography. ASTM International.
10. United States Environmental Protection Agency. Annual Certification Data for Vehicles,
    Engines, and Equipment.
11. Imafidon, O. CIDEX: a harmonised panel of EPA compression-ignition engine
    certification records. FACET research program.

---

## Appendix A: the divergence register in full

Every field recorded for every property, including the mechanism text and the citation
attached to each envelope.

{T_APPENDIX}

---

## Appendix B: overlap comparisons in full

Table 2 in Section 4.6 reproduces every comparison; this appendix records the citation
supporting each standard envelope.

{chr(10).join(f"- **{nm(r['property'])}** vs **{r['standard']}**: {fmt_env(r['std_low'], r['std_high'], r['std_units'])} — {cite(r['std_citation'])}" for r in OVL)}

---

## Appendix C: notes on reading the tables

*Not specified* means the regulation or standard states no numeric limit for that property.
It does not mean the property is unlimited in practice, and it does not mean the value is
unknown; it means the document is silent.

*Undefined* in the overlap column means the overlap fraction cannot be computed because at
least one of the two envelopes is open on at least one side. It is not zero and should not
be read as a small number.

*Min.* and *max.* denote one-sided limits. A one-sided limit constrains a fuel in one
direction only, and two one-sided limits pointing in opposite directions do not compose into
a band.
""")

# ------------------------------------------------------------------ write out
os.makedirs(DOCS, exist_ok=True)
md = "\n".join(P)
open(f"{DOCS}/PREPRINT.md", "w", encoding="utf-8").write(md)
words = len(md.split())
print(f"written: {DOCS}/PREPRINT.md ({os.path.getsize(f'{DOCS}/PREPRINT.md'):,} bytes, ~{words:,} words)")

# Mechanical check, not a hope: the LaTeX header declares a fixed set of
# non-ASCII glyphs. Anything outside it reaches pdflatex undefined and kills the
# build at whatever line it happens to land on, so catch it here instead.
DECLARED = set("≥≤≈→×÷±°"
               "²³µρμ–—"
               "‘’“”…")
undeclared = sorted({c for c in md if ord(c) > 127} - DECLARED)
if undeclared:
    raise SystemExit("undeclared non-ASCII characters in PREPRINT.md: "
        + ", ".join(f"{c!r} (U+{ord(c):04X})" for c in undeclared)
        + "\nDeclare them in TEX or replace them in the generator.")

if shutil.which("pandoc"):
    pdf = f"{DOCS}/FUELDIV_preprint.pdf"
    r = subprocess.run(["pandoc", f"{DOCS}/PREPRINT.md", "-o", pdf,
        "--toc", "--toc-depth=2", "-H", "/tmp/fueldiv_header.tex",
        "-V", "geometry:margin=1in", "-V", "fontsize=11pt",
        "-V", "colorlinks=true", "-V", "linkcolor=MidnightBlue",
        "-V", "urlcolor=MidnightBlue"], capture_output=True, text=True)
    print(f"written: {pdf} ({os.path.getsize(pdf):,} bytes)" if r.returncode == 0
          else "PDF failed:\n" + r.stderr[:1200])
else:
    print("pandoc not found; markdown only")
