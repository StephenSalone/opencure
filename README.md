# OpenCure 🔬

**Open-source AI drug repurposing pipeline for neglected tropical diseases.**

Finding cures for diseases the world forgot about.

## 🤗 [Live Demo — Try It Now](https://huggingface.co/spaces/SciloanBort/opencure-ntd-screen)

🌐 [opencure.life](https://opencure.life) | 📄 [Preprint (bioRxiv)](https://biorxiv.org) | 📧 stephen@salonecapital.com

---

## What Is This?

Over a billion people suffer from neglected tropical diseases (NTDs) — Chagas, malaria, sleeping sickness, leishmaniasis. These diseases kill hundreds of thousands every year. Yet they receive a fraction of the research funding of diseases that affect wealthier populations.

OpenCure is an open-source pipeline that:
1. **Screens FDA-approved drugs** as repurposing candidates against NTD targets
2. **Runs molecular docking** (AutoDock Vina) to predict binding affinity
3. **Validates with molecular dynamics** (OpenMM) to confirm binding stability
4. **Publishes all findings freely** — no paywalls, no patents, no barriers

If a drug already approved for human use binds strongly to a disease target, it could be repurposed — potentially reaching patients in years instead of decades.

---

## Results So Far

Screened 4 FDA-approved drugs against 3 neglected disease targets. All scores in kcal/mol (more negative = stronger binding). Threshold for interest: **-6.0 kcal/mol**.

| Drug | Chagas (Cruzain) | Malaria (Falcipain-2) | Sleeping Sickness (TbCatB) |
|---|---|---|---|
| **Ivermectin** | -7.26 ✅ | **-10.21 🔥** | -7.41 ✅ |
| **Imatinib** | -6.90 ✅ | **-9.89 🔥** | -7.71 ✅ |
| **Niclosamide** | -6.36 ✅ | -7.82 ✅ | -6.56 ✅ |
| Metformin | -4.31 ❌ | -4.81 ❌ | -4.30 ❌ |

🔥 = Exceptional hit (≤ -9.0) | ✅ = Strong hit (≤ -6.0) | ❌ = Below threshold

**Top candidates:** Ivermectin and Imatinib show exceptional binding against Falcipain-2 (malaria). All three hit drugs exceed threshold across all three diseases.

> ⚠️ These are computational predictions — hypothesis-generating, not proof. Experimental validation required.

---

## Disease Targets

| Disease | Target Protein | PDB ID | People Affected |
|---|---|---|---|
| Chagas disease | Cruzain (cysteine protease) | 1AIM | ~6–7 million |
| Malaria | Falcipain-2 (cysteine protease) | 3BPF | ~250 million/year |
| Sleeping sickness | TbCatB (cathepsin B) | 3HHI | ~70,000/year |

---

## How to Run It

### Requirements

- macOS or Linux (Apple Silicon supported)
- [Miniforge](https://github.com/conda-forge/miniforge) (conda)
- AutoDock Vina 1.2.7 ([download for your platform](https://github.com/ccsb-scripps/AutoDock-Vina/releases))

### Setup

```bash
git clone https://github.com/StephenSalone/opencure.git
cd opencure

# Create conda environment
conda create -n drugdiscovery python=3.11
conda activate drugdiscovery
conda install -c conda-forge rdkit openmm openff-toolkit pdbfixer openbabel

# Place AutoDock Vina binary in tools/vina/
# Download from: https://github.com/ccsb-scripps/AutoDock-Vina/releases
```

### Screen a Drug

```bash
conda activate drugdiscovery
python tools/repurposing_agent.py
```

### Run Molecular Dynamics

```bash
python tools/drug_sim.py
```

---

## Repository Structure

```
opencure/
├── tools/
│   ├── repurposing_agent.py     # Main screening pipeline (Lipinski + docking)
│   ├── drug_sim.py              # OpenMM molecular dynamics simulations
│   ├── semantic_scholar.py      # Literature search wrapper
│   ├── *.pdb                    # Protein structures (fixed with PDBFixer)
│   ├── *.pdbqt                  # Receptor and ligand files for Vina
│   └── vina/                    # AutoDock Vina binary (add your own)
├── results/
│   ├── chagas_screen_2026-02-28.json    # Raw docking results
│   ├── opencure_preprint_v1.md          # Full preprint (Markdown)
│   └── opencure_preprint_v1.docx        # Full preprint (Word)
├── website/
│   └── index.html               # opencure.life source
└── MISSION.md                   # Why we're doing this
```

---

## The Stack

| Tool | Purpose |
|---|---|
| [RDKit](https://www.rdkit.org/) | Cheminformatics, Lipinski filtering, 3D conformer generation |
| [AutoDock Vina 1.2.7](https://vina.scripps.edu/) | Molecular docking |
| [OpenMM 8.4](https://openmm.org/) | Molecular dynamics simulations |
| [OpenFF Toolkit](https://github.com/openforcefield/openff-toolkit) | Force field parameterization |
| [PDBFixer](https://github.com/openmm/pdbfixer) | Protein structure preparation |
| [OpenBabel](https://openbabel.org/) | File format conversion |
| [Semantic Scholar API](https://api.semanticscholar.org/) | Literature search |

Everything is free and open-source. No GPU required (OpenCL via Metal on Apple Silicon).

---

## Limitations

This is early-stage computational work. Known limitations:
- Small drug library (4 drugs screened so far — expanding)
- Rigid receptor docking (no protein flexibility)
- Geometric center docking box (not active-site specific)
- Short MD simulations (validation only)
- No experimental validation yet

We document these openly so researchers can build on and improve the work.

---

## Contribute

This project is wide open. If you're a researcher, student, or developer:

- **Run it** on your own drug library
- **Add new disease targets** — open an issue with a PDB ID
- **Improve the pipeline** — PRs welcome
- **Validate experimentally** — contact us if you want to collaborate

---

## Cite This Work

Salone, S. (2026). *Computational Drug Repurposing Screen for Neglected Tropical Diseases Using Open-Source AI Pipeline.* bioRxiv. BIORXIV/2026/708812.

---

## License

MIT License — use it, build on it, save lives with it.

---

## Who Built This

**Stephen Salone** — Founder, OpenCure  
20-year electrical worker from Rockport, Texas. No PhD. Just a person who thinks the world can do better for the people it's forgotten about.

*"The best time to start was 60 years ago. The second best time is now."*

📧 stephen@salonecapital.com | 🌐 opencure.life
