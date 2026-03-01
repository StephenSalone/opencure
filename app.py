"""
OpenCure.life — NTD Drug Screening Web Demo
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="OpenCure - NTD Drug Screen", page_icon="🔬", layout="wide")

st.title("🔬 OpenCure — NTD Drug Repurposing Screen")
st.markdown("**Finding cures for diseases the world forgot about.**")
st.markdown("Free. Open source. Built by an electrician from Texas + two AIs.")
st.markdown("[GitHub](https://github.com/StephenSalone/opencure) | [opencure.life](https://opencure.life) | [bioRxiv Preprint](https://www.biorxiv.org/search/opencure)")

st.divider()

st.subheader("📊 Our Results — 4 Drugs × 4 Diseases")
st.markdown("Screened using AutoDock Vina 1.2.7 on Apple Silicon Mac. Threshold: **-6.0 kcal/mol**")

data = {
    "Drug": ["Imatinib (Gleevec)", "Ivermectin", "Niclosamide", "Metformin"],
    "FDA Approved For": ["Leukemia", "Parasitic infections", "Tapeworm", "Diabetes"],
    "Chagas": ["-6.90 ✅", "-7.26 ✅", "-6.36 ✅", "-4.31 ❌"],
    "Malaria": ["-9.89 🔥", "-10.21 🔥", "-7.82 ✅", "-4.81 ❌"],
    "Sleeping Sickness": ["-7.71 ✅", "-7.41 ✅", "-6.56 ✅", "-4.30 ❌"],
    "Leishmaniasis": ["-8.27 🔥", "-6.72 ✅", "-7.20 ✅", "-4.96 ❌"],
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)
st.caption("🔥 Strong hit (≤ -9.0) | ✅ Hit (≤ -6.0) | ❌ Below threshold | All scores in kcal/mol")

st.divider()

st.subheader("🧪 Imatinib — Published Experimental Validation")
col1, col2, col3 = st.columns(3)
with col1:
    st.success("**Leishmaniasis** ✅\nPMID 31737578 (2019)\nMatched Amphotericin B in vitro against L. major")
with col2:
    st.success("**Chagas Disease** ✅\nCambridge Parasitology (2019)\nDerivatives outperformed Benznidazole")
with col3:
    st.success("**Malaria** ✅\nPLOS ONE 2016 + 2025 Review\nPrevents P. falciparum egress via TK inhibition")

st.divider()

st.subheader("🛠️ Run Your Own Screen")
st.markdown("""
The full pipeline runs on any Mac in under 10 minutes:
```bash
git clone https://github.com/StephenSalone/opencure.git
cd opencure
conda create -n drugdiscovery python=3.11
conda activate drugdiscovery
conda install -c conda-forge rdkit openmm openff-toolkit pdbfixer openbabel
python tools/repurposing_agent.py
```
""")

st.divider()

st.subheader("🤝 Collaborate")
st.markdown("""
We're looking for wet-lab collaborators to validate these findings experimentally.

- **Email:** stephen@salonecapital.com  
- **GitHub:** [github.com/StephenSalone/opencure](https://github.com/StephenSalone/opencure)  
- **Website:** [opencure.life](https://opencure.life)

All data, code, and results are free forever. MIT licensed.
""")

st.caption("Built by Stephen Salone + Nova (Anthropic/Claude) + Grok (xAI) | March 2026")
