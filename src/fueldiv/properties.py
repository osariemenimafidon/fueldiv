"""Fuel property conversions and envelope arithmetic for FUELDIV.

Design commitments, carried over from CIDEX's unit discipline:

D1  No silent conversion. Density is stored in kg/m3 and API gravity in degAPI;
    converting between them is an explicit call, because the certification
    envelope is written in degAPI and every commercial fuel standard is written
    in kg/m3, and a register that mixed them would be quietly wrong.

D2  An unconstrained property is None, never a sentinel number. A property that
    no regime bounds is the central finding of this project; encoding it as 0,
    -1 or NaN would let it be averaged into a summary statistic and disappear.

D3  Envelope overlap is undefined, not zero, when either envelope is absent.
    "We do not know" and "they do not overlap" are different findings and the
    register must never conflate them.
"""

from __future__ import annotations

from dataclasses import dataclass


# Density of water at 60 degF (15.56 degC), kg/m3. The API gravity definition is
# anchored at 60 degF, so this is the correct reference density for the
# conversion below -- not the 999.972 kg/m3 maximum at 4 degC.
WATER_DENSITY_60F = 999.016


class EnvelopeError(ValueError):
    """Raised when envelope arithmetic is asked for something undefined."""


def api_to_density(api_gravity: float) -> float:
    """Convert API gravity (degAPI) to density (kg/m3) at 60 degF.

    Uses the standard definition degAPI = 141.5 / SG - 131.5, inverted.
    Higher API gravity means a LIGHTER fuel, so the conversion is decreasing.

    >>> round(api_to_density(32.0), 1)
    864.6
    >>> round(api_to_density(37.0), 1)
    838.9
    """
    if api_gravity <= -131.5:
        raise ValueError(f"API gravity {api_gravity} is below the physical limit")
    specific_gravity = 141.5 / (api_gravity + 131.5)
    return specific_gravity * WATER_DENSITY_60F


def density_to_api(density_kg_m3: float) -> float:
    """Convert density (kg/m3 at 60 degF) to API gravity (degAPI).

    >>> round(density_to_api(864.6), 1)
    32.0
    """
    if density_kg_m3 <= 0:
        raise ValueError("density must be positive")
    specific_gravity = density_kg_m3 / WATER_DENSITY_60F
    return 141.5 / specific_gravity - 131.5


@dataclass(frozen=True)
class Envelope:
    """A closed, open, or absent numeric range for one property in one regime.

    An Envelope with both bounds None means the regime does not constrain the
    property at all. That is a finding, not missing data, and `constrained`
    reports it explicitly so downstream code cannot treat it as a gap in
    coverage.
    """

    low: float | None = None
    high: float | None = None
    units: str = ""
    citation: str = ""
    verified: bool = True

    @property
    def constrained(self) -> bool:
        return self.low is not None or self.high is not None

    @property
    def bounded_both_sides(self) -> bool:
        return self.low is not None and self.high is not None

    @property
    def width(self) -> float | None:
        if not self.bounded_both_sides:
            return None
        return self.high - self.low

    def contains(self, value: float) -> bool:
        if self.low is not None and value < self.low:
            return False
        if self.high is not None and value > self.high:
            return False
        return True


def overlap_fraction(commercial: Envelope, certification: Envelope) -> float:
    """Fraction of the commercial envelope that lies inside the certification one.

    Returns 0.0 when the two ranges are disjoint -- a legally sold fuel wholly
    outside the envelope the engine was certified on, which is the sharpest form
    of the divergence this project measures.

    Raises EnvelopeError when either envelope is unbounded on a side that
    matters, because an unconstrained regime has no overlap to compute. D3: the
    caller must record 'undefined', not silently receive 0.0.

    >>> cert = Envelope(838.9, 864.6, "kg/m3")
    >>> en590 = Envelope(820.0, 845.0, "kg/m3")
    >>> round(overlap_fraction(en590, cert), 3)
    0.244
    >>> en15940 = Envelope(765.0, 800.0, "kg/m3")
    >>> overlap_fraction(en15940, cert)
    0.0
    """
    if not (commercial.bounded_both_sides and certification.bounded_both_sides):
        raise EnvelopeError(
            "overlap is undefined unless both envelopes are bounded on both "
            f"sides; got commercial={commercial}, certification={certification}"
        )
    if commercial.units != certification.units:
        raise EnvelopeError(
            f"refusing to compare {commercial.units!r} against "
            f"{certification.units!r} -- convert first"
        )
    span = commercial.width
    if span == 0:
        return 1.0 if certification.contains(commercial.low) else 0.0

    lo = max(commercial.low, certification.low)
    hi = min(commercial.high, certification.high)
    return max(0.0, hi - lo) / span


def classify_gap(
    certification: Envelope,
    market: Envelope,
    federally_sampled: bool = False,
    results_published: bool = False,
) -> str:
    """Assign the gap class used throughout the register.

    `sampled_unpublished` outranks the structural classes: a property that the
    federal government measures but does not release is a different -- and more
    tractable -- problem than one nobody measures, and the register should say
    which it is.

    >>> classify_gap(Envelope(40, 50), Envelope(low=40))
    'constrained_both'
    >>> classify_gap(Envelope(839.8, 865.4), Envelope())
    'cert_only'
    >>> classify_gap(Envelope(), Envelope())
    'unconstrained'
    >>> classify_gap(Envelope(), Envelope(high=15), True, False)
    'sampled_unpublished'
    """
    if federally_sampled and not results_published:
        return "sampled_unpublished"
    if certification.constrained and market.constrained:
        return "constrained_both"
    if certification.constrained:
        return "cert_only"
    if market.constrained:
        return "market_only"
    return "unconstrained"


if __name__ == "__main__":
    import doctest

    failures, tests = doctest.testmod()
    print(f"{tests - failures}/{tests} doctests passed")
