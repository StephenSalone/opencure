"""
OpenCure.life — NTD Drug Screening Web Demo
Screen any FDA-approved drug against neglected tropical disease targets
"""
import streamlit as st
import subprocess
import os
import tempfile

st.set_page_config(page_title="OpenCure - NTD Drug Screen", page_icon="🔬", layout="wide")

st.title("🔬 OpenCure — NTD Drug Repurposing Screen")
st.markdown("**Screen any drug against neglected tropical disease targets in minutes.**")
st.markdown("Free. Open source. Runs on a Mac. [GitHub](https://github.com/StephenSalone/opencure) | [opencure.life](https://opencure.life)")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Drug")
    drug_name = st.text_input("Drug name", placeholder="e.g. Imatinib")
    smiles = st.text_input("SMILES string", placeholder="e.g. Cc1ccc(cc1Nc2nccc...")
    st.caption("Get SMILES from [PubChem](https://pubchem.ncbi.nlm.nih.gov/) or [DrugBank](https://www.drugbank.ca/)")

with col2:
    st.subheader("Target Disease")
    disease = st.selectbox("Disease target", [
        "Chagas disease (Cruzain / 1AIM)",
        "Malaria (Falcipain-2 / 3BPF)",
        "Sleeping Sickness (TbCatB / 3HHI)",
        "Leishmaniasis (PTR1 / 2BFA)",
    ])

st.divider()

if st.button("🚀 Run Screen", type="primary", disabled=not (drug_name and smiles)):
    st.info(f"Screening {drug_name} against {disease}...")
    st.warning("⚠️ Full pipeline requires local setup. See GitHub for instructions.")
    st.markdown("""
    **What the pipeline does:**
    1. Converts SMILES → 3D conformer (RDKit)
    2. Converts to PDBQT format (OpenBabel)
    3. Docks against target protein (AutoDock Vina 1.2.7)
    4. Reports binding score (kcal/mol)
    
    **Threshold:** -6.0 kcal/mol = potential hit
    """)

st.divider()
st.subheader("📊 Published Results")

import pandas as pd

data = {
    "Drug": ["Imatinib", "Ivermectin", "Niclosamide", "Metformin"],
    "Chagas (kcal/mol)": ["-6.90 ✅", "-7.26 ✅", "-6.36 ✅", "-4.31 ❌"],
    "Malaria (kcal/mol)": ["-9.89 🔥", "-10.21 🔥", "-7.82 ✅", "-4.81 ❌"],
    "Sleeping Sickness (kcal/mol)": ["-7.71 ✅", "-7.41 ✅", "-6.56 ✅", "-4.30 ❌"],
    "Leishmaniasis (kcal/mol)": ["-8.27 🔥", "-6.72 ✅", "-7.20 ✅", "-4.96 ❌"],
}
st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
st.caption("Threshold: -6.0 kcal/mol | ✅ Hit | 🔥 Strong Hit | ❌ Below threshold")

st.divider()
st.markdown("Built by [Stephen Salone](mailto:stephen@salonecapital.com) + Nova (AI) + Grok (AI) | [opencure.life](https://opencure.life) | MIT License")
