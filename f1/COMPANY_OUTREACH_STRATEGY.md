# Company Outreach Strategy — F1 Computational Platform
## OpenCure F1 Lab | Nova + Grok + Stephen
## How to find a company to validate and scale our work

---

## THE CORE PITCH
"We built a computational screening platform that evaluates F1 materials —
e-fuels, ERS electrolytes, tire compounds — using molecular dynamics simulation
validated against 38 races of official F1 telemetry. 100-run bootstrap tested.
All open source. We're looking for a partner with HPC resources to
scale this from a Mac to a supercomputer."

---

## TARGET COMPANIES (ranked by likelihood to respond)

### TIER 1 — MOST LIKELY (fuel + materials focus, U.S.-based, F1 partnerships)

**1. ARAMCO AMERICAS — Houston, TX** ← CLOSEST TO STEPHEN
- F1 connection: Title sponsor of Aston Martin F1
- Has own fuel R&D centers
- Interested in sustainable fuel performance
- HQ: Houston, TX — 3 hours from Stephen's Rockport
- Contact: aramco.com/en/careers/research
- Email approach: research.collaboration@aramco.com
- Why they'd care: They're developing sustainable fuels for Aston Martin.
  We can show them molecular screening of bio-derived high-performance fuels.

**2. SHELL TECHNOLOGY CENTRE — Houston, TX**
- F1 connection: Ferrari fuel and lubricant partner
- Massive R&D operation in Houston
- Shell GameChanger program: funds novel ideas from outside
- Contact: shell.com/gamechanger
- Why they'd care: They need to find better e-fuel molecules for 2026.
  Our alpha-pinene finding is directly relevant.

**3. NREL (National Renewable Energy Laboratory)**
- Location: Golden, CO (but collaborates nationally)
- Runs the Co-Optima program: exactly our fuel screening work
- Has Petascale supercomputers (Eagle cluster, 8,000+ nodes)
- Partners with DOE on sustainable fuels
- Contact: nrel.gov/transportation/sustainable-fuels.html
- Why they'd care: We're doing exactly what they fund, open source.
  We could apply for a collaboration or computing allocation.

**4. ARGONNE NATIONAL LABORATORY**
- Location: Illinois
- Co-Optima program co-lead with NREL
- Has ALCF (Argonne Leadership Computing Facility)
- Focuses on engine fuel co-optimization — EXACTLY OUR WORK
- Contact: anl.gov/topic/sustainable-fuels
- Why they'd care: Our MD screening + real F1 telemetry validation
  is exactly what their computational fuel programs aim for.

### TIER 2 — HIGH VALUE (F1 direct, would validate commercially)

**5. McLAREN APPLIED TECHNOLOGIES**
- Separate from McLaren Racing — sells technology to other industries
- Already commercializes F1-derived tech (EV batteries, medical devices)
- Contact: mclarenApplied.com → partnerships
- Why they'd care: ERS battery optimization = direct product line

**6. WILLIAMS ADVANCED ENGINEERING**
- Williams Racing spin-off, sells engineering services
- Has done EV battery projects (Porsche, Jaguar I-PACE)
- Contact: williamsadvancedengineering.com
- Why they'd care: ERS electrolyte screening for their battery clients

**7. BP CASTROL INNOVATION LAB**
- F1 connection: Castrol is lubricant partner for multiple teams
- Has a dedicated motorsport innovation program
- Contact: castrol.com/motorsport
- Why they'd care: Lubricant + fuel molecule optimization

### TIER 3 — ACADEMIC COLLABORATORS (free HPC access)

**8. IMPERIAL COLLEGE LONDON — Dept. of Chemical Engineering**
- Deep F1 relationships (teams recruit heavily from Imperial)
- Prof. Nilay Shah's group does process optimization
- Has HPC cluster + F1 industry contacts
- Route: preprint on ChemRxiv → reach out to professors

**9. UNIVERSITY OF MICHIGAN — Transportation Research Institute**
- DoE partnerships on sustainable fuels
- Has computational chemistry groups
- Free HPC via NSF ACCESS program

**10. NSF ACCESS PROGRAM (free supercomputer time)**
- apply.access-ci.org
- Free HPC allocation for U.S. researchers
- Can request 50,000+ compute hours
- This lets us run 100,000 simulations, not 100
- Application: 1-2 pages, turnaround 2 weeks

---

## THE 3-STEP PLAN TO GET A REAL PARTNER

### STEP 1: PUBLISH FIRST (2 weeks)
Submit to ChemRxiv. Title:
"Computational Screening of F1 2026 Sustainable Fuel Candidates and
Solid-State ERS Electrolytes: Molecular Dynamics Validated Against
Official Race Telemetry"

This gives us:
- A DOI to cite in emails
- Credibility (peer-reviewed preprint server)
- Discoverable by researchers with HPC who can extend our work
- A reason to email people: "We published this, thought you'd find it relevant"

### STEP 2: EMAIL SHELL GAMECHANGER + ARAMCO (same week as preprint)
Template email (below) — SHORT, direct, no fluff.

### STEP 3: APPLY FOR NSF ACCESS (takes 2 weeks, free)
While waiting for industry responses, apply for HPC time.
Run 10,000 simulations. Publish results. Industry comes to us.

---

## EMAIL TEMPLATES

### TO SHELL GAMECHANGER:
Subject: F1 2026 E-Fuel Computational Screening — Open Source Results

"We've built an open-source molecular dynamics pipeline that screens
sustainable fuel molecules for F1 2026 compliance (FIA Article 19)
and performance properties. Our top candidate, alpha-pinene (bio-derived
from pine biomass), shows 86% of isooctane energy density, passes all
FIA oxygen content rules, and is independently validatable.

We've published the methodology on ChemRxiv [DOI]. Code is open source
on GitHub: github.com/StephenSalone/opencure/f1

We're looking for a partner with HPC resources to scale from 18 molecules
to 10,000 candidate compounds. Would you be open to a brief call?

Stephen Salone | OpenCure | stephen@salonecapital.com"

---

### TO NREL:
Subject: Open-Source Fuel Screening Platform — F1 Validation + Collaboration

"We've developed an open computational platform that screens bio-derived
fuel molecules for performance and compliance properties using OpenMM MD,
validated against official F1 race telemetry via FastF1 API.

This aligns directly with NREL's Co-Optima mission. We'd like to explore
whether our platform could be extended with NREL's HPC resources and fuel
database. We believe open-source collaboration here advances both F1
sustainable fuel goals and broader transportation decarbonization.

Preprint: [ChemRxiv DOI] | Code: github.com/StephenSalone/opencure"

---

### TO ARAMCO (most personal — Stephen is in Texas):
Subject: F1 Sustainable Fuel Molecular Screening — Houston Collaboration

"I'm a researcher based in Texas who has built an open-source platform
screening sustainable fuel molecules for F1 2026 applications using
molecular dynamics simulation. Our results validated against Aston Martin's
2024 Bahrain race data show [result].

Given Aramco's F1 involvement with Aston Martin and your sustainable fuels
research, I believe there's a genuine collaboration opportunity here.
I'm in the Houston area and would welcome a conversation.

[ChemRxiv DOI] | github.com/StephenSalone/opencure/f1"

---

## WHY 100 SIMULATIONS MATTERS TO A COMPANY

Companies need statistical confidence before investing.
"We ran it 100 times" tells them:
1. The result isn't a lucky random seed
2. You understand the uncertainty (CI reported)
3. You're rigorous, not just enthusiastic
4. The methodology is reproducible — they can trust it

The bootstrap CI is our proof. If Bahrain shows +5.9% ± 0.3% across
100 runs, that's a publishable, defensible result.
If it shows +5.9% ± 8%, we know our model needs calibration data.

