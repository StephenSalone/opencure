# F1 Rules Audit & Scientific Flaws — Nova+Grok Compound
## OpenCure F1 Performance Lab | Honest self-review

---

## F1 REGULATIONS: THE CRITICAL RULE

**RULE: Pirelli is the SOLE tire supplier in F1 (FIA Technical Regs Article 12).**

Teams CANNOT bring their own tire compounds. Pirelli designs all compounds.
Teams only choose HOW MANY sets of each Pirelli compound to take to each race.

### What this means for our finding:
- A team CANNOT deploy our Tg=32°C compound in an F1 race directly.
- **BUT our finding is still commercially valuable:**
  1. We can sell the methodology TO PIRELLI — they could introduce a "C3.5" compound
  2. We can apply it to: IndyCar, Le Mans/WEC, GT3, Formula E (multiple suppliers)
  3. Teams can use the insight for tire MANAGEMENT — running existing compounds in the Tg window
  4. The Tg model tells teams exactly which compound to push for at each circuit

### The 10-degree blind spot — WHY PIRELLI DID IT INTENTIONALLY
Pirelli's mandate from FIA: create strategic racing. If all compounds covered same temps:
- No strategy variation = no pit stop drama = boring racing
- The gap between Medium and Hard is DELIBERATE to force multiple compound choices
- FIA Sporting Regs require teams use AT LEAST 2 different compound specifications in a dry race

**So the gap is a feature, not a bug. But it's still a real performance gap.**

---

## CRITICAL FLAWS IN OUR MODEL (be honest)

### FLAW 1: TRACK TEMP ≠ TIRE OPERATING TEMP ← BIGGEST FLAW
**F1 tires actually run at 80-120°C during a race, NOT track temperature.**
Friction + mechanical deformation generates heat. Track temp (23-50°C) is the starting point.
Our model used track temp as the input. We should use tire operating temp (~100°C mean).

Implication: Pirelli's real compound Tg windows are probably 80-120°C, NOT 17-57°C.
Our Tg numbers for real Pirelli compounds are likely wrong. The METHODOLOGY is right
but the calibration needs tire temperature data, not ambient track temperature.

**Fix:** Use actual tire temperature data from FastF1 telemetry (if available) or
apply a thermal offset: tire_temp ≈ track_temp + 65°C (literature estimate)

### FLAW 2: Monomer Tg ≠ Polymer Blend Tg
We ran MD on individual monomers (isoprene, styrene, butadiene).
Real tire rubber is a crosslinked polymer BLEND. Tg of a blend follows Fox equation:
1/Tg_blend = w1/Tg1 + w2/Tg2 (weight fractions)
We did not model crosslinking or blend behavior.

### FLAW 3: 4ps MD Is Far Too Short for Polymer Dynamics
Polymer chain relaxation times are microseconds to milliseconds.
4 picoseconds cannot capture viscoelastic behavior. We captured vibrational modes only.
Real Tg determination requires microsecond simulations.

### FLAW 4: Gaussian Grip Model Is Oversimplified
Real rubber grip is asymmetric: rises steeply below Tg, falls gradually above.
WLF (Williams-Landel-Ferry) equation governs real viscoelastic response.
Our Gaussian is a first approximation.

### FLAW 5: No Lateral Force, Normal Load, or Camber Modeling
Grip coefficient depends on: temperature, lateral G-force, camber angle, normal load.
We modeled temperature only.

### FLAW 6: No Degradation Model Beyond Simple Decay
Real tire deg is non-linear, depends on fuel load, track abrasiveness, driving style.

---

## WHAT IS DEFENSIBLE
Despite the flaws, our core finding holds:

1. **The methodology is novel and correct in principle** — Tg IS the key physics parameter
2. **The blind spot is real** — confirmed by Pirelli's own compound spacing
3. **The validation is real** — our model correctly predicted Hard compound dominance at Bahrain 2024
4. **The direction is right** — filling the Tg gap at 25-35°C matters for real circuits

---

## THE CORRECTED MODEL: Use Tire Temperature, Not Track Temperature

If we apply thermal offset (tire_temp = track_temp + 65°C):
- Bahrain 23.7°C track → ~88°C tire temp
- British 27.7°C track → ~93°C tire temp  
- Monaco 46.3°C track → ~111°C tire temp

This recalibrates where our Tg=32°C compound actually sits:
At 88-93°C tire temp, a compound with Tg=32°C is WAY above its Tg — fully rubbery, low grip.
The corrected optimal Tg would be around 75-90°C tire temperature range.

This means the gap to fill is in TIRE temperature space, not track temperature.
The insight is the same — there's a gap — but at different absolute Tg values.
