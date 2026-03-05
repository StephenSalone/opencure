"""
F1 Fuel Additive Screening
OpenCure F1 Performance Lab - Nova + Grok + Stephen

F1 fuel is ~99 octane hydrocarbon blend. We screen known
performance additives for combustion efficiency properties.
Using molecular descriptors as proxies for:
- Octane rating contribution
- Combustion energy density
- Thermal stability
"""
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
import json

print("=" * 55)
print("  F1 FUEL ADDITIVE MOLECULAR SCREEN")  
print("  OpenCure F1 Lab | Nova + Grok + Stephen")
print("=" * 55)

# Known and candidate F1 fuel additives
additives = {
    # Current F1 allowed additives
    'toluene':           'Cc1ccccc1',
    'ethanol':           'CCO',
    'MTBE':              'COC(C)(C)C',
    'MMT_antiknock':     '[Mn](=O)(=O)=O',
    
    # High performance additives (research compounds)
    'nitromethane':      'C[N+](=O)[O-]',
    'diethyl_ether':     'CCOCC',
    'methyl_cyclohexane':'CC1CCCCC1',
    'naphthalene':       'c1ccc2ccccc2c1',
    'trimethylbenzene':  'Cc1cc(C)cc(C)c1',
    'cyclopentadiene':   'C1=CC=C1',
    
    # Novel candidates (Nova + Grok suggestion)
    'dimethyl_carbonate':'COC(=O)OC',
    'gamma_butyrolactone':'O=C1CCCO1',
    'tetralin':          'C1CCc2ccccc2C1',
}

results = []
for name, smiles in additives.items():
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            continue
        mol_h = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol_h, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol_h)
        
        # Calculate molecular descriptors relevant to combustion performance
        mw = Descriptors.MolWt(mol)
        log_p = Descriptors.MolLogP(mol)  # lipophilicity/energy density proxy
        tpsa = Descriptors.TPSA(mol)      # polarity
        hbd = rdMolDescriptors.CalcNumHBD(mol)
        hba = rdMolDescriptors.CalcNumHBA(mol)
        rot_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
        rings = rdMolDescriptors.CalcNumRings(mol)
        aromatic = rdMolDescriptors.CalcNumAromaticRings(mol)
        
        # Carbon/hydrogen ratio - combustion energy indicator
        formula = rdMolDescriptors.CalcMolFormula(mol)
        
        # Combustion energy proxy: LogP correlates with energy density for hydrocarbons
        # Higher LogP = more hydrocarbon character = more energy per molecule
        # Aromatic rings contribute to octane rating
        octane_score = (aromatic * 15) + (rings * 8) + (log_p * 5) - (tpsa * 0.5)
        
        result = {
            'name': name,
            'smiles': smiles,
            'formula': formula,
            'MW': round(mw, 2),
            'LogP': round(log_p, 3),
            'octane_proxy': round(octane_score, 1),
            'aromatic_rings': aromatic,
            'TPSA': round(tpsa, 2),
        }
        results.append(result)
        print(f"\n{name} ({formula}): LogP={log_p:.2f}, Octane_proxy={octane_score:.1f}, Aromatic={aromatic}")
        
    except Exception as e:
        print(f"{name}: ERR {e}")

# Sort by octane proxy score
results.sort(key=lambda x: x['octane_proxy'], reverse=True)

print("\n\n=== TOP F1 FUEL ADDITIVE CANDIDATES (by octane proxy) ===")
for i, r in enumerate(results[:8]):
    print(f"{i+1}. {r['name']}: {r['octane_proxy']:.1f} | {r['formula']} | LogP={r['LogP']}")

with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/fuel_additive_results.json','w') as f:
    json.dump(results, f, indent=2)
print("\nResults saved.")
