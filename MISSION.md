# Mission: Open Drug Repurposing for Neglected Diseases

## The Problem
1 billion people suffer from neglected tropical diseases.
Malaria, TB, Chagas, sleeping sickness, leishmaniasis — curable or treatable, but ignored.
Pharma won't invest. No profit motive. People die.

## What We're Building
An open-source AI agent that:
1. **Scans** new scientific literature (Semantic Scholar API) for neglected disease targets
2. **Identifies** FDA-approved drugs that might bind to those targets (repurposing = faster + safer)
3. **Simulates** protein-ligand binding with OpenMM + OpenFF to validate candidates
4. **Scores** candidates by binding energy + literature evidence
5. **Publishes** findings openly — free for any researcher, anywhere, to act on

## Why This Matters
- Repurposed drugs skip Phase I safety trials — years faster to patients
- We have the full simulation stack running on a consumer Mac
- No gatekeepers. No paywalls. No profit requirement.

## Stack
- OpenMM 8.4 + OpenFF 2.0 — molecular dynamics
- RDKit — cheminformatics
- Semantic Scholar API — literature search
- PDBFixer — protein preparation
- Apple Silicon OpenCL — GPU acceleration

## First Target
**Chagas disease** (Trypanosoma cruzi) — 6-7 million infected, <2 effective drugs, 
no new treatments in 60 years. Crystal structures available in PDB.

## Built by
Stephen Salone + Nova (Claude/Anthropic) + Grok (xAI)
February 28, 2026
