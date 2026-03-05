# F1 2026 Rules — What We Can and Cannot Change
## OpenCure F1 Lab | Studied before building simulator

---

## WHAT WE CAN OPTIMIZE (legal setup variables)

### AERODYNAMICS
- Front wing angle: Corner Mode (high DF) ↔ Straight Mode (low drag)
  - Active aero: front + rear wings adjust simultaneously
  - Activation zone: driver-controlled on straights
  - Overtake Mode: available within 1s of car ahead
- Rear wing angle: 3-element rear wing (beam wing removed vs 2025)
- Front wing width: 100mm narrower than 2025 — fixed by regs
- Floor: flat floor + larger diffuser (no Venturi tunnels)
- Bargeboard position: teams have some freedom here
- Ride height: adjustable (affects floor seal and diffuser efficiency)

### POWER UNIT / ERS
- Total power: ~50% ICE + ~50% MGU-K electric (350kW each approx)
- ERS deployment: driver-controlled "Boost" button — when and how much
- ERS harvesting: regenerative braking strategy (when to harvest vs deploy)
- Engine modes: teams can map fuel/ignition within FIA limits
- Fuel load: up to 105kg per race — less fuel = lighter = faster early laps

### SUSPENSION / CHASSIS
- Minimum weight: 770kg (with driver) — we target this exactly
- Wheelbase: fixed at ~3400mm (200mm shorter than 2025) — set by regs
- Ride height: adjustable front and rear (affects aero platform)
- Camber: front and rear — affects tire contact patch
- Toe: front and rear — affects stability vs responsiveness
- Caster angle: affects steering feel and self-centering
- Spring rates: adjustable — affects bump handling
- Anti-roll bar stiffness: front and rear
- Ballast position: within car, affects weight distribution %

### TIRES
- Compound choice: SOFT/MEDIUM/HARD (Pirelli designated per circuit)
- Tire pressure: within Pirelli-specified minimum (typically 21-26 psi front, 19-23 psi rear)
- Camber at tire: affects operating temp and wear
- Blankets: BANNED from 2024 — cold tire warm-up strategy matters

### BRAKES
- Brake bias: % front/rear — driver adjustable on steering wheel
- Brake duct size: adjustable for cooling vs drag
- Brake material: carbon-carbon (fixed by convention but compound density can vary)

### GEARBOX
- Gear ratios: teams select from FIA-homologated set per season
- Differential settings: entry/mid/exit — affects corner traction

---

## WHAT IS FIXED / CANNOT CHANGE

- V6 1.6L turbo ICE — same displacement (fixed)
- MGU-H: REMOVED in 2026 (gone)
- Tire construction: Pirelli only, teams cannot modify
- Fuel: must be FIA-approved 100% sustainable fuel
- Safety structures: halo, rollhoop, impact structures (safety fixed)
- Maximum overall width: 2000mm
- Minimum weight: 770kg — cannot go below
- Track limits: must stay within white lines (FIA Sporting Regs Art. 33)

---

## KEY 2026 CHANGES THAT AFFECT OUR SIMULATOR

1. **Active aero = new optimization variable**: when to activate Straight Mode?
   - Early activation = max straight speed but entering corner in wrong config
   - Optimal activation point = circuit-specific, lap-time-dependent
   
2. **50/50 power split**: ERS deployment timing is now as important as throttle
   - 350kW electric available — but battery has finite energy per lap
   - Where you deploy ERS per lap is the biggest single setup variable

3. **30% less downforce**: corner speeds lower than 2025
   - More emphasis on mechanical grip (tires, suspension) vs aero grip

4. **30kg lighter**: 770kg minimum — ballast position matters more
   - Weight distribution front/rear affects both corner entry and exit

5. **Narrower tires**: less contact patch, Tg model adjustments needed

---

## TRACK LIMITS (FIA Sporting Regulations Article 33)
- Must keep at least two wheels within white lines at all times
- Exceeding track limits = lap time deleted in qualifying
- In race: repeated violations = 5-second penalty
- Our simulator: hard constraint — any config violating track limits = invalid lap
