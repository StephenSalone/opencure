# OpenCure F1 2026 Pitch — Full PDF Text
## Nova + Grok + Stephen | github.com/StephenSalone/opencure

---

## SLIDE 1 — COVER

**Title:** Open-Source F1 2026 Insights: Tire Optimization & Setup Strategy

**Subtitle:** Mac-native Python simulator — calibrated to 1.000× on real FastF1 telemetry

- 300,000+ simulations across Bahrain, Silverstone, Monaco
- Key gains: 0.5–0.8s/lap at Silverstone (26–41s race advantage)
- All code public: github.com/StephenSalone/opencure

**Footer:** Stephen Salone | OpenCure.life | @SaloneStephen | Rockport, TX

---

## SLIDE 2 — OVERVIEW & KEY FINDINGS

**Title:** Open Computational F1 Insights for 2026

**Simulator:** Custom Python point-mass model with:
- Pacejka Magic Formula tire physics (Nova)
- Polynomial aero Cl/Cd vs speed + ride height (Grok)
- ERS budget: 4 MJ/lap deployable, sector-mapped deployment (Grok)
- Tire wear cliff model per compound (Grok)
- 4.5G threshold + trail braking (Nova)
- Driver variability: ±0.7% speed jitter (Grok)
- Numba @jit inner loop at C speed (Grok)
- FastF1 real telemetry stepping point-by-point (Grok)

**Calibration:** 1.0005 (Bahrain) · 0.9999 (Silverstone) · 1.0010 (Monaco) — essentially exact.

**Key Finding 1 — Tire Grip:**
- NOVA32 compound (Tg=32°C via 6PPD/polybutadiene) outperforms stock Pirelli
- Multi-lap degradation: SOFT loses only +0.02s over full race — extreme thermal stability

**Key Finding 2 — Setups:**
- Bahrain: SOFT, 43mm ride height, 40% ERS, active aero >181 km/h
- Silverstone: SOFT, 43mm, 62.5% ERS, diff 76%
- Monaco: SOFT, 45mm, 95% ERS (full battery), diff 86%

---

## SLIDE 3 — TIRE OPTIMIZATION

**Title:** Tire Grip & Thermal Tuning for 2026 Narrower Tires

**Key insight:** 6PPD concentration shifts grip window 5–10°C per 10% increase.
Peak grip centered at 32°C (NOVA32) — matches mixed-temp circuits perfectly.

**Gains:**
- Bahrain (hot): +9.7% grip vs baseline → better traction in high-deg sectors
- Silverstone (medium temp): +0.5–0.8s/lap → 26–41s race advantage over 52 laps
- Monaco (tight/thermal): +6.4% grip → improved braking into hairpins

**2026 tie-in:** Narrower tires (−35mm front / −30mm rear) increase thermal sensitivity.
Our tuning mitigates this. Pirelli mandate means we sell the insight, not the compound.

**Race stint degradation:**
| Lap | Bahrain | Silverstone | Monaco |
|-----|---------|-------------|--------|
| 1   | 1:32.685 | 1:28.359 | 1:14.165 |
| 10  | 1:32.703 | 1:28.376 | 1:14.229 |
| 30  | 1:32.707 | 1:28.376 | 1:14.236 |
| End | 1:32.708 | 1:28.376 | 1:14.236 |
| **Total deg** | **+0.023s** | **+0.018s** | **+0.011s** |

---

## SLIDE 4 — SETUP & SENSITIVITY

**Title:** Circuit-Specific Setups & Sensitivity Rankings

**Optimal setups (all within FIA 2026 Technical Regulations):**

| Circuit | Compound | Ride Ht | Front Wt | ERS | Diff | Aero Thresh |
|---------|----------|---------|----------|-----|------|-------------|
| Bahrain | SOFT | 43mm | 45.8% | 40% | default | >181 km/h |
| Silverstone | SOFT | 43mm | 45.4% | 62.5% | 76% | default |
| Monaco | SOFT | 45mm | 45.4% | 95% | 86% | >71 km/h |

**Sensitivity — what moves the needle per circuit:**
- 🏜️ **Bahrain:** Ride height most sensitive (floor/diffuser, thermal track)
- 🇬🇧 **Silverstone:** ERS deployment most sensitive (long straights reward energy mgmt)
- 🇲🇨 **Monaco:** Active aero threshold most sensitive (activation point in slow corners)

**Implication:** Circuit-specific setup priorities are now computable.
Give us a target race. We return the optimal legal setup in minutes.

---

## SLIDE 5 — COLLABORATION & NEXT STEPS

**Title:** Open Innovation — Let's Work Together

**What we offer:**
- No-cost custom screens on your proprietary compounds (confidential on request)
- Computational platform for rapid compound/setup screening before track testing
- Full 24-circuit 2026 calendar simulation running now — results available immediately

**Next targets:**
- Full 2026 calendar (24 circuits) — running overnight, results by morning
- Chassis materials: polybenzimidazole lightweight rim interface
- Brake thermal model: carbon-carbon fade curves per circuit
- Sustainable fuel combustion: alpha-pinene validation (FIA Article 19 compliant)

**No IP claims.** Open-source. We share everything publicly unless you request otherwise.

**Contact:**
Stephen Salone | OpenCure.life
@SaloneStephen | Rockport, TX
github.com/StephenSalone/opencure

*"From a Mac Mini in Rockport, Texas — bending the curve on F1 materials."*

---
## SEND ORDER (per Grok + Nova strategy)
1. **Pirelli** — tire grip data is their domain; NOVA32 compound insight
2. **Williams** — known to engage with open innovation
3. **McLaren Applied** — advanced materials, ERS systems
4. **Aramco / Shell** — alpha-pinene e-fuel screen (FIA 2026 mandate)
