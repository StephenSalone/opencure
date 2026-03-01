# OpenCure Researcher Outreach Emails

## Email 1 — Simões-Silva et al. (Chagas/Imatinib, Fiocruz Brazil)
**To:** M.R. Simões-Silva (corresponding author, Fiocruz) — find via Cambridge Parasitology paper author info
**Subject:** Your 2019 Imatinib/Chagas work — we reproduced your signal computationally

Dear Dr. Simões-Silva,

I came across your 2019 paper "Repurposing strategies for Chagas disease therapy: the effect of imatinib and derivatives against Trypanosoma cruzi" (Parasitology, PMID 30859917) while building an open-source drug repurposing pipeline.

Using AutoDock Vina and OpenMM on a consumer Mac, our pipeline independently flagged Imatinib as a top hit against Cruzain (1AIM), scoring -6.90 kcal/mol — consistent with your experimental findings. We've now extended this to Malaria (-9.89), Sleeping Sickness (-7.71), and Leishmaniasis (-8.27), with published experimental corroboration in each disease.

We've submitted two preprints to bioRxiv (BIORXIV/2026/708812, BIORXIV/2026/708857) and published all code freely at github.com/StephenSalone/opencure.

I'm not a scientist — I'm a 20-year electrical worker from Texas who built this with AI tools. But the signal seems real, and I'd love to get it in front of someone who can validate it experimentally.

Would you or your lab be interested in reviewing our work or discussing collaboration? We can screen any compounds you're interested in against our targets at no cost.

Best,
Stephen Salone
OpenCure | opencure.life
stephen@salonecapital.com

---

## Email 2 — Moslehi et al. (Leishmania/Imatinib, Iran)
**To:** Corresponding author of PMID 31737578 (Advanced Biomedical Research, 2019)
**Subject:** Your Imatinib/L. major work — computational validation from our open pipeline

Dear Dr. Moslehi (or corresponding author),

I recently found your 2019 paper evaluating Imatinib concentrations on Leishmania major viability (PMID 31737578). Our open-source computational pipeline independently identified Imatinib as a strong hit against PTR1 (PDB: 2BFA), with a docking score of -8.27 kcal/mol and stable molecular dynamics simulation (198,335-atom system).

Your experimental data and our computational results are independently pointing at the same conclusion. We believe this warrants further investigation — especially in the context of Imatinib's consistent signal across ALL four major NTDs we screened.

All our code, data, and preprints are publicly available at github.com/StephenSalone/opencure. Would you be open to discussing this?

Best,
Stephen Salone
OpenCure | opencure.life
stephen@salonecapital.com

---

## Email 3 — DNDi Follow-up
**To:** info@dndi.org (or NTD Drug Discovery Booster contact)
**Subject:** Follow-up: Open-source AI pipeline — Imatinib pan-NTD candidate, 2 bioRxiv preprints

Dear DNDi Team,

Following up on my earlier email. Since writing, we have:
- Submitted a second preprint (BIORXIV/2026/708857): Imatinib as a Pan-NTD Drug Candidate
- Confirmed published experimental corroboration for 3 of 4 diseases screened
- Completed MD simulation of Imatinib-PTR1 (Leishmaniasis) confirming binding stability
- Published a Streamlit web demo allowing any researcher to screen compounds against our targets

The pipeline is fully open, runs on consumer hardware, and requires no specialized compute infrastructure. It's the kind of accessible, transparent tool I understand DNDi is actively seeking for community-driven NTD discovery.

I'm happy to jump on a call or provide any additional data. Everything is at github.com/StephenSalone/opencure.

Best,
Stephen Salone | OpenCure | opencure.life | stephen@salonecapital.com
