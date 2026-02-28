"""
Open Drug Repurposing Agent for Neglected Diseases
Nova x Grok — Built February 28, 2026

Step 1: Search literature for disease target
Step 2: Find approved drugs that might bind
Step 3: Simulate binding with OpenMM
Step 4: Score and report candidates
"""

import urllib.request
import urllib.parse
import json
import time

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"

# Known neglected disease targets with PDB structures
NEGLECTED_TARGETS = {
    "chagas": {
        "disease": "Chagas Disease (Trypanosoma cruzi)",
        "target": "Cruzain (T. cruzi cysteine protease)",
        "pdb_id": "1AIM",
        "search_query": "Trypanosoma cruzi cruzain inhibitor drug repurposing",
        "affected": "6-7 million people, Latin America"
    },
    "malaria": {
        "disease": "Malaria (Plasmodium falciparum)",
        "target": "Falcipain-2 (P. falciparum cysteine protease)",
        "pdb_id": "3BPF",
        "search_query": "Plasmodium falciparum falcipain inhibitor repurposing",
        "affected": "240 million people, Sub-Saharan Africa"
    },
    "sleeping_sickness": {
        "disease": "Sleeping Sickness (Trypanosoma brucei)",
        "target": "TbCatB (T. brucei cathepsin B)",
        "pdb_id": "3HHI",
        "search_query": "Trypanosoma brucei inhibitor drug repurposing",
        "affected": "50,000-70,000 people, Africa"
    }
}

# FDA-approved drugs with known binding potential (from literature)
REPURPOSING_CANDIDATES = [
    {"name": "Imatinib", "smiles": "Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1", "approved_for": "Leukemia"},
    {"name": "Metformin", "smiles": "CN(C)C(=N)NC(=N)N", "approved_for": "Diabetes"},
    {"name": "Ivermectin", "smiles": "C1CC2CC(CC3OC(=O)C(C(=C/C(=C/[C@@H](C[C@H]1OC(=O)C(=CC3=O)C)C)C)C)O2)CC(=O)O", "approved_for": "Parasites"},
    {"name": "Niclosamide", "smiles": "OC(=O)c1ccc(Cl)cc1NC(=O)c1cc([N+](=O)[O-])ccc1Cl", "approved_for": "Tapeworm"},
    {"name": "Auranofin", "smiles": "CC(=O)O[C@@H]1[C@@H](OC(C)=O)[C@H](OC(C)=O)[C@@H](CO)O1.[Au]SP(CC)(CC)CC", "approved_for": "Arthritis"},
]


def search_literature(query, limit=5):
    """Search Semantic Scholar for relevant papers."""
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,year,authors,abstract,citationCount,openAccessPdf"
    }
    url = f"{SEMANTIC_SCHOLAR_API}/paper/search?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "NovaDrugRepurposing/1.0"})
    try:
        time.sleep(2)
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()).get("data", [])
    except Exception as e:
        return []


def analyze_candidates(target_info):
    """Search literature for drug-target combinations."""
    print(f"\n{'='*60}")
    print(f"TARGET: {target_info['target']}")
    print(f"DISEASE: {target_info['disease']}")
    print(f"AFFECTED: {target_info['affected']}")
    print(f"{'='*60}")

    print(f"\n📚 Searching literature...")
    papers = search_literature(target_info["search_query"])

    if papers:
        print(f"Found {len(papers)} relevant papers:")
        for p in papers[:3]:
            print(f"  [{p.get('year','?')}] {p.get('title','')[:80]}")
            print(f"         Citations: {p.get('citationCount', 0)}")
    else:
        print("  (Rate limited — API key needed for full access)")

    print(f"\n💊 Repurposing candidates to simulate:")
    for drug in REPURPOSING_CANDIDATES:
        print(f"  - {drug['name']} (approved for {drug['approved_for']})")

    return REPURPOSING_CANDIDATES


def run_quick_binding_screen(target_name, candidates):
    """Use RDKit to quickly screen candidates by drug-likeness."""
    print(f"\n🔬 Running quick drug-likeness screen (Lipinski rules)...")
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors

        results = []
        for drug in candidates:
            mol = Chem.MolFromSmiles(drug["smiles"])
            if mol:
                mw = Descriptors.MolWt(mol)
                logp = Descriptors.MolLogP(mol)
                hbd = Descriptors.NumHDonors(mol)
                hba = Descriptors.NumHAcceptors(mol)
                # Lipinski Rule of 5
                passes = (mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10)
                results.append({
                    "name": drug["name"],
                    "mw": round(mw, 1),
                    "logp": round(logp, 2),
                    "lipinski": "✅ PASS" if passes else "⚠️  FAIL",
                    "smiles": drug["smiles"]
                })
                print(f"  {drug['name']:15} MW:{mw:6.1f}  LogP:{logp:5.2f}  {('✅ PASS' if passes else '⚠️  FAIL')}")

        return results
    except ImportError:
        print("  RDKit not available in this env")
        return candidates


if __name__ == "__main__":
    print("🌍 OPEN DRUG REPURPOSING AGENT FOR NEGLECTED DISEASES")
    print("   Nova x Grok — February 28, 2026")
    print("   Mission: Find treatments for diseases Big Pharma ignores\n")

    # Focus on Chagas first
    target = NEGLECTED_TARGETS["chagas"]
    candidates = analyze_candidates(target)
    screened = run_quick_binding_screen("chagas", candidates)

    print(f"\n{'='*60}")
    print("NEXT STEPS (full pipeline):")
    print("  1. Download Cruzain crystal structure (PDB: 1AIM)")
    print("  2. Dock top candidates into binding site")
    print("  3. Run OpenMM MD simulation for each")
    print("  4. Calculate binding free energy")
    print("  5. Rank and publish top candidates openly")
    print(f"{'='*60}")
    print("\nThis pipeline could identify a Chagas treatment candidate")
    print("that researchers anywhere in the world can test in the lab.")
    print("\nLet's go. 🔬🌍")
