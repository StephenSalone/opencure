"""
F1 CHASSIS: Carbon Fiber Resin Interface Binding Energy
OpenCure F1 Performance Lab - Nova + Grok + Stephen

The F1 chassis is carbon fiber + epoxy resin. 
The interface between fiber and matrix determines:
- Stiffness (lap time through aerodynamic load handling)
- Weight (every 10kg = ~0.3s per lap)
- Impact resistance

We screen different epoxy/resin molecules for binding
affinity to carbon fiber surface models.
Stronger binding = lighter chassis = faster car.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
import json

print("=" * 60)
print("  F1 CARBON FIBER RESIN INTERFACE SCREEN")
print("  OpenCure F1 Lab | Nova + Grok + Stephen")
print("=" * 60)

resins = {
    'bisphenol_A_epoxy':     ('c1ccc(C(C)(C)c2ccc(OCC3CO3)cc2)cc1OCC1CO1', 'Standard aerospace epoxy'),
    'TGDDM_epoxy':           ('C(N(CC1CO1)c1ccc(-c2ccc(N(CC3CO3)CC4CO4)cc2)cc1)C1CO1', 'High-temp F1 epoxy'),
    'cyanate_ester':         ('CC(C)(c1ccc(OC#N)cc1)c1ccc(OC#N)cc1', 'Ultra-high temp'),
    'bismaleimide':          ('O=C1C=CC(=O)N1c1ccc(Cc2ccc(N3C(=O)C=CC3=O)cc2)cc1', 'BMI - premium F1'),
    'polyimide_monomer':     ('O=C1OC(=O)c2cc3ccc(=O)oc3cc21', 'Extreme temp resistant'),
    'novel_polybenzimidazole': ('c1ccc2nc3ccccc3nc2c1', 'NOVEL: ultra-rigid candidate'),
}

results = []
for name, (smiles, desc) in resins.items():
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            print(f"{name}: invalid SMILES")
            continue
        
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        tpsa = Descriptors.TPSA(mol)
        rings = rdMolDescriptors.CalcNumRings(mol)
        aromatic = rdMolDescriptors.CalcNumAromaticRings(mol)
        hba = rdMolDescriptors.CalcNumHBA(mol)
        hbd = rdMolDescriptors.CalcNumHBD(mol)
        
        # Interface strength proxy:
        # - Aromatic rings: pi-pi stacking with carbon fiber surface
        # - HBD: hydrogen bonding with sizing agents
        # - Low MW: better penetration and wetting
        # - LogP: hydrophobicity controls cure behavior
        interface_score = (aromatic * 20) + (hbd * 8) + (hba * 5) - (mw * 0.05) + (rings * 10)
        
        r = {
            'name': name,
            'description': desc,
            'MW': round(mw,1),
            'LogP': round(logp,2),
            'aromatic_rings': aromatic,
            'HBD': hbd,
            'interface_score': round(interface_score, 1)
        }
        results.append(r)
        print(f"{name}: score={interface_score:.1f} | MW={mw:.0f} | Ar={aromatic} | {desc}")
    except Exception as e:
        print(f"{name}: ERR {e}")

results.sort(key=lambda x: x['interface_score'], reverse=True)
print("\n\n=== TOP CARBON FIBER RESINS FOR F1 CHASSIS ===")
for i,r in enumerate(results):
    print(f"{i+1}. {r['name']}: {r['interface_score']} | {r['description']}")

with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/carbon_fiber_results.json','w') as f:
    json.dump(results, f, indent=2)
print("\nResults saved.")
