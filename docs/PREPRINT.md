% What the fuel regulation guarantees an engine designer: a specification divergence register for United States compression-ignition certification
% Osariemen Imafidon
% 2026-09-15

Independent Researcher. ORCID [0009-0006-3069-4674](https://orcid.org/0009-0006-3069-4674).
Correspondence: odimafid@gmail.com.

**Preprint.** Not peer reviewed. Part of the
[FACET](https://osariemenimafidon.github.io/facet/) research program.

---

## Abstract

A compression-ignition engine sold in the United States is certified once, on a test fuel
whose properties are fixed by **40 CFR 1065.703**. It is then operated, for a useful life
measured in thousands of hours, on fuel that need only satisfy **40 CFR 1090** — a
materially shorter list of requirements. The two regulations are written for different
purposes, and neither references the other's property set.

This paper reads both, property by property, and records where they fail to overlap. Of
**10 fuel properties** selected because a mechanism connects each to the
injection event or its immediate consequences,
3 are constrained at certification *and* in the market,
3 are constrained at certification only, and
**4 are constrained by neither**. The federal government publishes measurements of
in-service values for **none of the
ten**, so the size of the realised divergence is not a quantity anyone
outside the fuel supply chain can currently estimate from public data.

The four unconstrained properties are not peripheral to injection. They
are bulk modulus, cloud point, FAME content, lubricity (HFRR). Bulk modulus sets
the speed of sound in the fuel and therefore the propagation of the pressure wave from
pump to nozzle, and therefore the actual start of injection relative to the commanded one.
Lubricity sets the wear margin at the hardware performing the injection. Neither has a
numeric limit in either regulation.

Comparing the certification envelope against three commercial consensus standards across
24 property-standard pairs, we find that renewable diesel meeting
**EN 15940 lies wholly outside** the certification fuel's density envelope —
838.9–864.6 kg/m³ against
765–800 kg/m³,
an overlap of exactly zero. Its cetane floor sits above the certification fuel's cetane
ceiling. Across **8,354 certified compression-ignition engine families**, none was certified on a fuel whose declaration mentions renewable, biodiesel or paraffinic content, and **7,928 of them (94.9%)** meter fuel volumetrically, the configuration in
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

1. A **divergence register**: 10 injection-relevant fuel properties, each
   carrying its certification envelope, its in-market envelope, a section-level citation
   for both, a stated physical mechanism, and a gap class.
2. **Envelope overlap arithmetic** against 3 commercial consensus
   standards across 24 property-standard pairs, distinguishing computed
   overlap from the case in which overlap is mathematically undefined, and including
   1 case of exactly zero overlap.
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

It does not claim that the 4 unconstrained properties vary widely in
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

Of the 10 properties in the register, 5 carry a two-sided certification band while carrying no two-sided in-market band: density, cetane number, kinematic viscosity at 40 °C, distillation T90, sulfur.

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


## 3 Method

### 3.1 Property selection

Properties were selected on a single criterion: a documented physical mechanism by which
the property alters the injection event or its immediate consequences. Each property is
recorded in the register with that mechanism stated explicitly in a text field, so the
selection is auditable rather than asserted. A reader who disagrees that a property
belongs can read the stated mechanism and say why it is wrong.

Ten properties met the criterion.
Nine act on the injection event or its immediate consequences
directly; the remainder is carried as a control case and is discussed below.

Sulfur is the control. It is not an injection parameter in the direct sense the other
properties are, but it is the one fuel property that is federally specified, federally
enforced and federally measured, and it is the property whose reduction removed the
lubricity margin that injection hardware had previously relied on. Its presence in the
register makes visible what a fully constrained property looks like in every column, which
is the comparison the rest of the table needs.

We make no claim that these 10 are exhaustive. They are the properties
for which a mechanism could be stated plainly enough to defend. A property omitted here
because no crisp mechanism could be written is a candidate for a later revision of the
register, not a refutation of it.

### 3.2 Sources and the transcription problem

Both primary sources are regulatory text, not datasets. There is no bulk download, no API
and no machine-readable specification table. Values were read from the Code of Federal
Regulations and transcribed into the register, each carrying a section-level citation on
the individual value rather than on the document as a whole:

- **40 CFR 1065.703 Table 1** — the certification test fuel specification.
- **40 CFR 1090.305** — the in-market diesel requirement.

Manual transcription is the obvious failure mode of a project of this shape, and asserting
that it was done carefully is not a control. It is addressed instead by a verification
point in the project's checklist: named register rows are opened in the CFR by a person
and compared against the cell, and the result is recorded. The publication gate refuses to
remove the draft stamp until that attestation exists.

A third class of source — the commercial consensus standards ASTM D975, EN 590 and
EN 15940 — is **paywalled**. Every value taken from them entered the register tagged
as unconfirmed and blocked publication until the investigator opened the standard and
confirmed the figure against the published text.
0 remain unconfirmed at the time of writing.

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

- `constrained_both` — both regulations state a numeric limit.
- `cert_only` — the certification specification states a limit; the in-market
  requirement does not.
- `unconstrained` — neither states a limit.

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
\mathrm{overlap} = \frac{\max\left(0,\ \min(c_{hi}, s_{hi}) - \max(c_{lo}, s_{lo})\right)}{s_{hi} - s_{lo}}
$$

where $c$ denotes the certification envelope and $s$ the standard's. The quantity answers
the question an engine designer would ask: if a fuel merely meets this commercial
standard, what fraction of the permitted specification space would also have been
acceptable as a certification fuel?

Where either envelope is unbounded on either side, the overlap is **undefined** and is
recorded as such, not as zero. The distinction is substantive rather than pedantic:
ASTM D975 sets no density limit at all, which is a different statement from setting one
that fails to overlap. Of 24 property-standard pairs,
6 yield a computed overlap and 18 are undefined because at least one
envelope is open on at least one side. That ratio is itself a result: most of the
comparisons a designer would want to make cannot be made, because most of the limits
involved are one-sided.

We additionally compute two order relations that do not require both envelopes to be
closed, because a one-sided limit can still be decisive:

- a standard's **floor above** the certification **ceiling**
  ($s_{lo} > c_{hi}$): every fuel meeting the standard exceeds the certification band;
- a standard's **ceiling below** the certification **floor**
  ($s_{hi} < c_{lo}$): every fuel meeting the standard falls short of it.

### 3.6 Unit reconciliation

Two unit reconciliations were required, and both are recorded in the register rather than
performed silently in the text.

**Density.** The certification specification states API gravity
(API gravity 32-37 °API), while every comparison standard states
density in kg/m³. API gravity is converted by the standard definition

$$
\rho = \frac{141.5}{\mathrm{API} + 131.5} \times \rho_{w},
\qquad \rho_{w} = 999.016\ \mathrm{kg/m^3}
$$

giving a certification envelope of **838.9–864.6 kg/m³**. The
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

One discriminating count is reported. Families using volumetric metering — direct or
indirect injection, as opposed to metering schemes that infer or measure mass — are
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
describes. Prose claims that depend on an order relation between two numbers — for
example that a standard's floor exceeds the certification ceiling — are likewise
generated from the comparison rather than written as text, so they cannot outlive the
condition that made them true.

---


## 4 Results

### 4.1 The divergence register

Table 1 is the register in summary form. Appendix A reproduces it in full, with the
mechanism text and the citation attached to every cell.

Table 1. Injection-relevant fuel properties, their certification and in-market envelopes,
and the resulting gap class.

| Property | Injection pathway | Certification | In-market | Gap class |
|:-----------------|:----------------------------|:-------------------|:------------------|:-----------------|
| Density | fuelling quantity | 838.9–864.6 kg/m³ | not specified | certification only |
| Bulk modulus | injection timing | not specified | not specified | unconstrained |
| Cetane number | combustion phasing | 40–50 | min. 40 | constrained by both |
| Kinematic viscosity (40 °C) | spray formation and fuelling quantity | 2–3.2 mm²/s | not specified | certification only |
| Lubricity (HFRR) | injection hardware durability | not specified | not specified | unconstrained |
| FAME content | post-injection / oil dilution | not specified | not specified | unconstrained |
| Aromatics | soot formation and seal compatibility | min. 100 g/kg | max. 35 vol% | constrained by both |
| Distillation T90 | spray evaporation | 293–332 °C | not specified | certification only |
| Sulfur | control case | 7–15 mg/kg | max. 15 mg/kg | constrained by both |
| Cloud point | fuel delivery to the pump | not specified | not specified | unconstrained |

### 4.2 Distribution of gap classes

Of 10 properties:
**3** are constrained by both regulations,
**3** by the certification specification only, and
**4** by neither. The federal government
publishes measurements of in-service values for
**none** of them.

The last figure is the one that determines what can be said next. With no federal
measurement programme covering these properties in the fuel actually sold, the magnitude of
any realised divergence is not estimable from public data by anyone outside the fuel supply
chain. This paper can therefore establish the *structure* of the gap and cannot establish
its *size*, and it does not attempt to.

### 4.3 The properties constrained by neither regulation

These four properties have no numeric limit in 40 CFR 1065.703 and
no numeric limit in 40 CFR 1090. Each entry below gives the injection pathway and the
mechanism exactly as recorded in the register.

**Bulk modulus** — *injection timing.* Sets the speed of sound in the fuel, therefore the propagation of the pressure wave from pump to nozzle, therefore the actual start of injection relative to the commanded one.

**Cloud point** — *fuel delivery to the pump.* Wax onset temperature. Filter and low-pressure-side plugging change the fuel supply pressure the high-pressure pump sees.

**FAME content** — *post-injection / oil dilution.* FAME raises boiling range and reduces volatility of the heavy tail; post-injection events used for aftertreatment regeneration can then reach the cylinder wall and dilute the lubricating oil.

**Lubricity (HFRR)** — *injection hardware durability.* Wear scar diameter at the high-pressure pump and injector needle. Desulfurisation and paraffinic processing both remove the polar species that provide boundary lubrication.

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

For these three properties the certification test fuel is pinned and the
in-market fuel is not constrained at all. This is the asymmetry that most directly
undermines the substitution on which certification rests: the tighter specification applies
to the fuel burned once in a laboratory, and no specification applies to the fuel burned
for the rest of the engine's life.

**Density** — *fuelling quantity.* Certification pins it to 838.9–864.6 kg/m³ (40 CFR 1065.703 Table 1 (derived from API gravity 32-37 °API)); the in-market requirement does not constrain it at all. Injection systems meter volume at a commanded rail pressure and duration; delivered fuel mass scales directly with density. A density shift is a fuelling error before any other effect.

**Distillation T90** — *spray evaporation.* Certification pins it to 293–332 °C (40 CFR 1065.703 Table 1 T90 (ASTM D86)); the in-market requirement does not constrain it at all. The heavy tail of the distillation curve sets how completely the spray evaporates before the diffusion burn, and therefore soot.

**Kinematic viscosity (40 °C)** — *spray formation and fuelling quantity.* Certification pins it to 2–3.2 mm²/s (40 CFR 1065.703 Table 1 (ASTM D445)); the in-market requirement does not constrain it at all. Governs nozzle discharge coefficient, internal leakage and spray penetration; also sets high-pressure pump lubrication margin.

### 4.5 The properties constrained by both — and what that does not mean

Three properties carry a numeric limit in both regulations. The class
label is the weakest of the three findings and needs qualifying, because "constrained by
both" does not imply "constrained consistently".

**Cetane number** — *combustion phasing.* Certification: 40–50 (40 CFR 1065.703 Table 1 (ASTM D613)). In-market: min. 40 (40 CFR 1090.305(c)(1) cetane index at least 40, alternative to aromatics cap). Sets ignition delay, therefore the split between premixed and diffusion burn, therefore the NOx/PM trade-off the calibration was tuned against.

**Aromatics** — *soot formation and seal compatibility.* Certification: min. 100 g/kg (40 CFR 1065.703 Table 1 minimum 100 g/kg (ASTM D5186)). In-market: max. 35 vol% (40 CFR 1090.305(c)(2) aromatics at most 35 vol%, alternative to cetane index). Aromatics drive soot formation and also swell elastomer seals in the injection system. The certification fuel specifies a minimum aromatic content; a near-zero-aromatic fuel sits below it.

**Sulfur** — *control case.* Certification: 7–15 mg/kg (40 CFR 1065.703 Table 1 ultra-low-sulfur grade). In-market: max. 15 mg/kg (40 CFR 1090.305(b) ULSD maximum 15 ppm). Not an injection parameter directly, but the regulated property whose reduction removed the lubricity that injection hardware previously relied on. Included as the control case: this is what a fully constrained and federally enforced property looks like.

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
means that of the three properties in this class, only sulfur is
unconditionally constrained in the market.

Stated plainly: the number of injection-relevant properties that 40 CFR 1090
unconditionally binds, for every diesel fuel sold, is one — and it is the control case
rather than an injection parameter.

### 4.6 Overlap with commercial consensus standards

Table 2 gives every property-standard comparison. Overlap is the fraction of the standard's
permitted envelope that lies inside the certification envelope, computed only where both
envelopes are closed on both sides.

Table 2. Envelope overlap, all 24 property-standard pairs.

| Property | Standard | Standard envelope | Certification envelope | Overlap |
|:-----------------|:--------------------|:--------------------|:--------------------|--------:|
| Density | ASTM D975 2-D S15 | not specified | 838.9–864.6 kg/m³ | undefined |
| Density | EN 590 | 820–845 kg/m³ | 838.9–864.6 kg/m³ | 24.2% |
| Density | EN 15940 | 765–800 kg/m³ | 838.9–864.6 kg/m³ | 0.0% |
| Bulk modulus | ASTM D975 2-D S15 | not specified | not specified | undefined |
| Bulk modulus | EN 590 | not specified | not specified | undefined |
| Bulk modulus | EN 15940 | not specified | not specified | undefined |
| Cetane number | ASTM D975 2-D S15 | min. 40 | 40–50 | undefined |
| Cetane number | EN 590 | min. 51 | 40–50 | undefined |
| Cetane number | EN 15940 | min. 70 | 40–50 | undefined |
| Kinematic viscosity (40 °C) | ASTM D975 2-D S15 | 1.9–4.1 mm²/s | 2–3.2 mm²/s | 54.5% |
| Kinematic viscosity (40 °C) | EN 590 | 2–4.5 mm²/s | 2–3.2 mm²/s | 48.0% |
| Kinematic viscosity (40 °C) | EN 15940 | 2–4.5 mm²/s | 2–3.2 mm²/s | 48.0% |
| Lubricity (HFRR) | ASTM D975 2-D S15 | max. 520 µm | not specified | undefined |
| Lubricity (HFRR) | EN 590 | max. 460 µm | not specified | undefined |
| Lubricity (HFRR) | EN 15940 | max. 460 µm | not specified | undefined |
| FAME content | ASTM D975 2-D S15 | max. 5 vol% | not specified | undefined |
| FAME content | EN 590 | max. 7 vol% | not specified | undefined |
| FAME content | EN 15940 | max. 7 vol% | not specified | undefined |
| Aromatics | EN 590 | max. 8 vol% | min. 100 g/kg | undefined |
| Aromatics | EN 15940 | max. 1.1 vol% | min. 100 g/kg | undefined |
| Distillation T90 | ASTM D975 2-D S15 | 282–338 °C | 293–332 °C | 69.6% |
| Sulfur | ASTM D975 2-D S15 | max. 15 mg/kg | 7–15 mg/kg | undefined |
| Sulfur | EN 590 | max. 10 mg/kg | 7–15 mg/kg | undefined |
| Cloud point | ASTM D975 2-D S15 | not specified | not specified | undefined |

Six of the 24 pairs yield a computed overlap; 18
are undefined because at least one envelope is open on at least one side. Even where overlap is
computable it is rarely large: a fuel meeting a commercial standard has a substantial
probability of sitting outside the certification band on any given property, and those
probabilities are not independent across properties, because they are driven by the same
underlying refinery streams.

Two order relations survive the one-sided cases:

- **Standard floor above certification ceiling:** **EN 590** requires at least 51 cetane where certification permits at most 50; **EN 15940** requires at least 70 cetane where certification permits at most 50.
- **Standard ceiling below certification floor:** **EN 15940** permits at most 800 kg/m³ of density where certification requires at least 838.9.
- **Exactly zero computed overlap:** density against **EN 15940**.

### 4.7 The density disjunction

The single most decisive result is density against EN 15940. The certification envelope is
838.9–864.6 kg/m³. Paraffinic diesel to EN 15940 class A is
765–800 kg/m³.
The envelopes do not overlap. Not marginally, not at a tail: the standard's entire
permitted range lies below the certification specification's lower bound, by roughly
39 kg/m³ at the closest approach.

EN 590 conventional diesel fares better but not well: an overlap of
24.2%
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
| Bulk modulus | injection timing | 8,354 | 7,928 |
| Lubricity (HFRR) | injection hardware durability | 8,354 | 7,928 |
| FAME content | post-injection / oil dilution | 8,354 | 7,928 |
| Cloud point | fuel delivery to the pump | 8,354 | 7,928 |

The exposure count is 8,354 families for every unconstrained property, because
40 CFR 1065.703 governs the certification of the entire compression-ignition population;
the number is a magnitude rather than a rate, and it is reported to fix the scale of the
structural finding rather than to discriminate between engines.

Of those, **7,928 (94.9%)** meter fuel volumetrically. For this subset the
mechanism from a density shift to a fuelling error is immediate and requires no intervening
assumption about control strategy, closed-loop correction or adaptive learning.

Across all 8,354 families, **none** was certified on a fuel whose declaration mentions renewable, biodiesel, paraffinic or ester content. This is a scan of all 36 distinct fuel declarations appearing in the certification record's fuel-type, test-fuel and certification-fuel fields across 8,627 families and 9,794 configuration records; every one of them describes a petroleum distillate, in almost every case by sulfur grade alone. The certification population and the renewable fuel supply do not intersect anywhere in the certification record, which is what makes the density disjunction in Section 4.7 a statement about every certified engine rather than about a subset of them.

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


## 5 Discussion

### 5.1 What the certification result licenses, and what it does not

A certification result is a measurement of an engine burning a specified fuel on a
specified cycle. It licenses the inference that this engine, burning that fuel, on that
cycle, emitted those quantities. The regulatory use of the result requires a further
inference: that the measurement represents the engine's emissions over a useful life spent
burning fuel drawn from the market.

That further inference rests on the fuel burned in service being close enough to the fuel
burned in the cell that the difference does not matter. The register shows that for
7 of 10 injection-relevant
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
three the class count suggests. Counting conditionality correctly, one
property is unconditionally bound, and that property is sulfur — which the register
carries as the control case precisely because it is not an injection parameter.

We report the class counts as computed from the presence of limits, and report this
qualification separately rather than folding it into the count, because the folding
requires a judgement about what "constrained" means and we prefer to leave that judgement
visible.

### 5.3 The binding constraint is measurement, not analysis

The federal government publishes measurements of in-service values for
none of the ten
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
properties covering the 4 unconstrained properties at minimum.

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
at least the 4 unconstrained properties. This is the intervention that
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

**Property selection.** The 10 properties are those for which a defensible
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

All processed data are in the repository under `data/processed/`: the divergence register,
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

**Density** (kg/m³) — *fuelling quantity*; class: certification only.

- Certification: 838.9–864.6 kg/m³ [40 CFR 1065.703 Table 1 (derived from API gravity 32-37 °API)]
- In-market: not specified [40 CFR 1090.305 (not regulated)]
- Federal public measurement of in-service values: no
- Mechanism: Injection systems meter volume at a commanded rail pressure and duration; delivered fuel mass scales directly with density. A density shift is a fuelling error before any other effect.

**Bulk modulus** (MPa) — *injection timing*; class: unconstrained.

- Certification: not specified [40 CFR 1065.703 Table 1 (not specified)]
- In-market: not specified [40 CFR 1090.305 (not regulated)]
- Federal public measurement of in-service values: no
- Mechanism: Sets the speed of sound in the fuel, therefore the propagation of the pressure wave from pump to nozzle, therefore the actual start of injection relative to the commanded one.

**Cetane number** (dimensionless) — *combustion phasing*; class: constrained by both.

- Certification: 40–50 [40 CFR 1065.703 Table 1 (ASTM D613)]
- In-market: min. 40 [40 CFR 1090.305(c)(1) cetane index at least 40, alternative to aromatics cap]
- Federal public measurement of in-service values: no
- Mechanism: Sets ignition delay, therefore the split between premixed and diffusion burn, therefore the NOx/PM trade-off the calibration was tuned against.

**Kinematic viscosity (40 °C)** (mm²/s) — *spray formation and fuelling quantity*; class: certification only.

- Certification: 2–3.2 mm²/s [40 CFR 1065.703 Table 1 (ASTM D445)]
- In-market: not specified [40 CFR 1090.305 (not regulated)]
- Federal public measurement of in-service values: no
- Mechanism: Governs nozzle discharge coefficient, internal leakage and spray penetration; also sets high-pressure pump lubrication margin.

**Lubricity (HFRR)** (µm) — *injection hardware durability*; class: unconstrained.

- Certification: not specified [40 CFR 1065.703 Table 1 (not specified)]
- In-market: not specified [40 CFR 1090.305 (not regulated)]
- Federal public measurement of in-service values: no
- Mechanism: Wear scar diameter at the high-pressure pump and injector needle. Desulfurisation and paraffinic processing both remove the polar species that provide boundary lubrication.

**FAME content** (vol%) — *post-injection / oil dilution*; class: unconstrained.

- Certification: not specified [40 CFR 1065.703 Table 1 (not specified; neat petroleum distillate implied)]
- In-market: not specified [40 CFR 1090.305 (not regulated)]
- Federal public measurement of in-service values: no
- Mechanism: FAME raises boiling range and reduces volatility of the heavy tail; post-injection events used for aftertreatment regeneration can then reach the cylinder wall and dilute the lubricating oil.

**Aromatics** (vol%) — *soot formation and seal compatibility*; class: constrained by both.

- Certification: min. 100 g/kg [40 CFR 1065.703 Table 1 minimum 100 g/kg (ASTM D5186)]
- In-market: max. 35 vol% [40 CFR 1090.305(c)(2) aromatics at most 35 vol%, alternative to cetane index]
- Federal public measurement of in-service values: no
- Mechanism: Aromatics drive soot formation and also swell elastomer seals in the injection system. The certification fuel specifies a minimum aromatic content; a near-zero-aromatic fuel sits below it.

**Distillation T90** (°C) — *spray evaporation*; class: certification only.

- Certification: 293–332 °C [40 CFR 1065.703 Table 1 T90 (ASTM D86)]
- In-market: not specified [40 CFR 1090.305 (not regulated)]
- Federal public measurement of in-service values: no
- Mechanism: The heavy tail of the distillation curve sets how completely the spray evaporates before the diffusion burn, and therefore soot.

**Sulfur** (mg/kg) — *control case*; class: constrained by both.

- Certification: 7–15 mg/kg [40 CFR 1065.703 Table 1 ultra-low-sulfur grade]
- In-market: max. 15 mg/kg [40 CFR 1090.305(b) ULSD maximum 15 ppm]
- Federal public measurement of in-service values: no
- Mechanism: Not an injection parameter directly, but the regulated property whose reduction removed the lubricity that injection hardware previously relied on. Included as the control case: this is what a fully constrained and federally enforced property looks like.

**Cloud point** (°C) — *fuel delivery to the pump*; class: unconstrained.

- Certification: not specified [40 CFR 1065.703 Table 1 (qualitative only: 'adequate for proper engine operation')]
- In-market: not specified [40 CFR 1090.305 (not regulated)]
- Federal public measurement of in-service values: no
- Mechanism: Wax onset temperature. Filter and low-pressure-side plugging change the fuel supply pressure the high-pressure pump sees.

---

## Appendix B: overlap comparisons in full

Table 2 in Section 4.6 reproduces every comparison; this appendix records the citation
supporting each standard envelope.

- **Density** vs **ASTM D975 2-D S15**: not specified — ASTM D975 Table 1 - D975 sets no density limit
- **Density** vs **EN 590**: 820–845 kg/m³ — EN 590 Table 1, temperate grades
- **Density** vs **EN 15940**: 765–800 kg/m³ — EN 15940 Table 1, paraffinic diesel class A
- **Bulk modulus** vs **ASTM D975 2-D S15**: not specified — ASTM D975 - no bulk modulus limit
- **Bulk modulus** vs **EN 590**: not specified — EN 590 - no bulk modulus limit
- **Bulk modulus** vs **EN 15940**: not specified — EN 15940 - no bulk modulus limit
- **Cetane number** vs **ASTM D975 2-D S15**: min. 40 — ASTM D975 Table 1 cetane number min 40
- **Cetane number** vs **EN 590**: min. 51 — EN 590 cetane number min 51
- **Cetane number** vs **EN 15940**: min. 70 — EN 15940 class A cetane number min 70
- **Kinematic viscosity (40 °C)** vs **ASTM D975 2-D S15**: 1.9–4.1 mm²/s — ASTM D975 Table 1
- **Kinematic viscosity (40 °C)** vs **EN 590**: 2–4.5 mm²/s — EN 590 Table 1
- **Kinematic viscosity (40 °C)** vs **EN 15940**: 2–4.5 mm²/s — EN 15940 Table 1
- **Lubricity (HFRR)** vs **ASTM D975 2-D S15**: max. 520 µm — ASTM D975 Table 1, HFRR at 60 °C
- **Lubricity (HFRR)** vs **EN 590**: max. 460 µm — EN 590 Table 1, HFRR at 60 °C
- **Lubricity (HFRR)** vs **EN 15940**: max. 460 µm — EN 15940 Table 1
- **FAME content** vs **ASTM D975 2-D S15**: max. 5 vol% — ASTM D975 permits up to 5 vol% FAME within the D975 grade
- **FAME content** vs **EN 590**: max. 7 vol% — EN 590 FAME max 7 vol%
- **FAME content** vs **EN 15940**: max. 7 vol% — EN 15940 FAME limit
- **Aromatics** vs **EN 590**: max. 8 vol% — EN 590 polycyclic aromatics max 8 vol%
- **Aromatics** vs **EN 15940**: max. 1.1 vol% — EN 15940 total aromatics max 1.1 vol%
- **Distillation T90** vs **ASTM D975 2-D S15**: 282–338 °C — ASTM D975 Table 1 T90
- **Sulfur** vs **ASTM D975 2-D S15**: max. 15 mg/kg — ASTM D975 grade 2-D S15
- **Sulfur** vs **EN 590**: max. 10 mg/kg — EN 590 sulfur max 10 mg/kg
- **Cloud point** vs **ASTM D975 2-D S15**: not specified — ASTM D975 - cloud point reported by season/region, not limited

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
