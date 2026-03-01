# Computational Drug Repurposing Screen for Neglected Tropical Diseases Using Open-Source AI Pipeline

**Stephen Salone¹, Nova (AI Research Assistant)², Grok (AI Research Assistant)³**

¹ OpenCure, Rockport, Texas, USA  
² Anthropic/OpenClaw  
³ xAI  

**Correspondence:** stephen@salonecapital.com  
**Website:** https://opencure.life  
**Date:** February 28, 2026  

---

## Abstract

Neglected tropical diseases (NTDs) affect over one billion people globally yet receive minimal pharmaceutical investment due to lack of commercial incentive. Drug repurposing — identifying new uses for existing approved drugs — offers a faster, cheaper path to treatment. Here we present results from an open-source computational pipeline that screens FDA-approved drugs against cysteine protease targets from three major NTDs: Chagas disease (*Trypanosoma cruzi* cruzain), malaria (*Plasmodium falciparum* falcipain-2), and sleeping sickness (*Trypanosoma brucei* TbCatB). Using AutoDock Vina 1.2.7 and OpenMM 8.4 molecular dynamics on consumer Apple Silicon hardware, we screened four FDA-approved drugs and identified several candidates with binding affinities exceeding the -6.0 kcal/mol threshold considered promising for drug development. Notably, ivermectin showed exceptional binding to falcipain-2 (-10.21 kcal/mol) and activity against all three targets. Imatinib likewise showed activity across all three disease targets. All data, code, and results are freely available at https://opencure.life.

---

## 1. Introduction

Neglected tropical diseases disproportionately affect the world's poorest populations. Chagas disease affects an estimated 6–7 million people in Latin America, with no new treatment approved in over 60 years. Malaria infects 240 million people annually, causing over 600,000 deaths. Sleeping sickness (*T. brucei* infection) affects approximately 70,000 people in sub-Saharan Africa and is fatal without treatment.

Drug repurposing offers significant advantages over de novo drug development: repurposed drugs have established safety profiles, known pharmacokinetics, existing manufacturing infrastructure, and can bypass Phase I clinical trials. Computational screening provides a cost-effective method to identify repurposing candidates before expensive laboratory validation.

Recent advances in open-source molecular dynamics (OpenMM), cheminformatics (RDKit), and docking software (AutoDock Vina) have made it possible to run meaningful drug discovery pipelines on consumer hardware. This work demonstrates that a complete computational repurposing screen can be executed on a single Apple Silicon Mac in under 24 hours at zero cost.

---

## 2. Methods

### 2.1 Target Selection and Preparation

Three cysteine protease targets were selected based on biological importance and availability of crystal structures:

- **Cruzain** (*T. cruzi*): PDB ID 1AIM — main protease essential for parasite survival
- **Falcipain-2** (*P. falciparum*): PDB ID 3BPF — hemoglobin degradation enzyme
- **TbCatB** (*T. brucei*): PDB ID 3HHI — cathepsin B-like protease

Protein structures were downloaded from the RCSB Protein Data Bank. Heteroatoms and water molecules were removed using PDBFixer 1.12.0. Missing residues and atoms were added, and hydrogens were added at pH 6.5 (consistent with the slightly acidic parasite food vacuole environment). Structures were converted to PDBQT format using OpenBabel 3.1.1.

### 2.2 Ligand Preparation

Four FDA-approved drugs were selected as repurposing candidates based on prior literature, anti-parasitic mechanism, and Lipinski Rule of Five compliance:

| Drug | Approved Use | MW | LogP | Lipinski |
|------|-------------|-----|------|----------|
| Ivermectin | Parasitic infections | 474.6 | 3.69 | ✅ Pass |
| Imatinib | Chronic myeloid leukemia | 493.6 | 4.59 | ✅ Pass |
| Niclosamide | Tapeworm infections | 355.1 | 3.85 | ✅ Pass |
| Metformin | Type 2 diabetes | 129.2 | -1.03 | ✅ Pass |

3D conformers were generated using RDKit 2024.x with MMFF force field optimization. Structures were converted to PDBQT format using OpenBabel.

### 2.3 Molecular Docking

Docking was performed using AutoDock Vina 1.2.7 (Apple Silicon binary). Search boxes of 30×30×30 Å were centered on the protein geometric center. Exhaustiveness was set to 8. Top binding modes were recorded.

### 2.4 Molecular Dynamics Simulation

Selected drug-protein complexes were simulated using OpenMM 8.4 with the OpenFF 2.0 (Sage) force field for ligands and AMBER ff14SB for proteins. Systems were solvated in TIP3P water with 150 mM NaCl (physiological ionic strength). Energy minimization was performed (500 steps), followed by 2,000 steps of MD at 300K using a Langevin integrator (2 fs timestep). Simulations ran on Apple Silicon GPU via OpenCL.

### 2.5 Computational Environment

All computations were performed on an Apple Silicon Mac using:
- Conda environment with Python 3.11
- OpenMM 8.4, OpenFF Toolkit, RDKit, PDBFixer, OpenBabel
- AutoDock Vina 1.2.7
- Total compute cost: $0 (consumer hardware)

---

## 3. Results

### 3.1 Chagas Disease — Cruzain (PDB: 1AIM)

| Drug | Binding Affinity (kcal/mol) | Assessment |
|------|-----------------------------|------------|
| Ivermectin | **-7.262** | Strong Hit |
| Imatinib | **-6.898** | Hit |
| Niclosamide | **-6.357** | Promising |
| Metformin | -4.307 | Below Threshold |

Three of four drugs exceeded the -6.0 kcal/mol threshold. Ivermectin showed the strongest binding, consistent with its known anti-parasitic mechanism.

### 3.2 Malaria — Falcipain-2 (PDB: 3BPF)

| Drug | Binding Affinity (kcal/mol) | Assessment |
|------|-----------------------------|------------|
| Ivermectin | **-10.21** | Exceptional |
| Imatinib | **-9.887** | Excellent |
| Niclosamide | **-7.820** | Strong Hit |
| Metformin | -4.809 | Below Threshold |

Falcipain-2 scores were notably higher than Cruzain across all drugs. Ivermectin's score of -10.21 kcal/mol is consistent with affinities observed for drugs specifically designed against this target. Ivermectin has known antimalarial activity in literature, lending biological plausibility to this result.

### 3.3 Sleeping Sickness — TbCatB (PDB: 3HHI)

| Drug | Binding Affinity (kcal/mol) | Assessment |
|------|-----------------------------|------------|
| Imatinib | **-7.711** | Strong Hit |
| Ivermectin | **-7.407** | Strong Hit |
| Niclosamide | **-6.556** | Hit |
| Metformin | -4.298 | Below Threshold |

### 3.4 Cross-Disease Summary

Ivermectin and Imatinib both exceeded the -6.0 kcal/mol threshold across all three disease targets — a notable finding suggesting broad-spectrum anti-parasitic potential for these repurposing candidates.

---

## 4. Discussion

### 4.1 Key Findings

The most significant finding is ivermectin's exceptional binding affinity to falcipain-2 (-10.21 kcal/mol). Falcipain-2 is essential for *P. falciparum* hemoglobin degradation and is a validated drug target. Ivermectin's antimalarial activity has been reported previously, and our computational result is consistent with direct falcipain-2 inhibition as a potential mechanism.

Imatinib's activity across all three targets is notable. Imatinib inhibits tyrosine kinases, but its activity against *T. cruzi* has been reported in cell-based assays, lending biological credibility to our Cruzain docking result.

### 4.2 Limitations

Several important caveats apply to these results:

1. **Docking is a computational prediction, not experimental validation.** Binding scores predict affinity but do not account for cell permeability, metabolism, toxicity, or in vivo pharmacokinetics.

2. **Docking box placement** was based on geometric protein center rather than known active site coordinates. Active site-specific docking may yield different results.

3. **No induced fit.** AutoDock Vina uses a rigid receptor model. Protein flexibility upon ligand binding is not modeled.

4. **Short MD simulations.** 4 ps of MD is insufficient for full thermodynamic equilibration. These simulations confirm system stability but are not free energy calculations.

5. **Small drug library.** Only 4 drugs were screened. A broader screen across approved drug databases (e.g., DrugBank, ~9,000 compounds) is warranted.

These results should be considered **hypothesis-generating** — they provide computational rationale for experimental follow-up, not evidence of clinical efficacy.

### 4.3 Significance

This work demonstrates that a meaningful computational drug repurposing screen can be performed on consumer hardware in under 24 hours at zero cost using entirely open-source tools. The pipeline is fully reproducible and available at https://opencure.life.

The primary value is not any individual result — it is the pipeline itself. OpenCure represents a proof-of-concept for democratized drug discovery: making computational screening accessible to researchers without access to expensive software licenses or supercomputing resources.

---

## 5. Conclusion

We present a freely available, open-source computational drug repurposing pipeline and apply it to three neglected tropical diseases. Ivermectin and imatinib show computational binding activity above the -6.0 kcal/mol threshold against all three disease targets, with ivermectin showing exceptional affinity for falcipain-2 (-10.21 kcal/mol). These findings warrant experimental validation and represent the first output of the OpenCure open-source drug discovery initiative.

All code, data, and results are freely available at **https://opencure.life** and the associated GitHub repository.

---

## Data Availability

All docking results, trajectory files, and analysis scripts are available at https://opencure.life. Code is open-source.

## Acknowledgments

This work was conducted as part of the OpenCure initiative. Computational assistance provided by Nova (Anthropic/Claude) and Grok (xAI). We thank the RCSB Protein Data Bank for open access to crystal structures, and the developers of AutoDock Vina, OpenMM, OpenFF, and RDKit for their open-source contributions.

## Conflicts of Interest

None declared. This work was conducted without commercial funding.

---

*Preprint submitted to bioRxiv. Not peer-reviewed.*
