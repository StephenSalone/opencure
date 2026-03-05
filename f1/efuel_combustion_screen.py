"""
F1 2026: E-FUEL MOLECULE SCREENING
OpenCure F1 Lab - Nova + Grok + Stephen

2026 F1 mandates 100% sustainable fuels.
Teams and fuel suppliers (Shell, Petronas, Castrol, BP) are racing
to find the best performing e-fuel within FIA rules.

We screen sustainable fuel molecules for:
1. Energy density (more energy per kg = more power)
2. Octane equivalence (resistance to knock = higher compression ratio)
3. Flame speed (faster burn = more efficient combustion)
4. Hydrogen content (cleaner combustion, less soot on intercooler)

Rules: FIA Article 19 limits to specific compound classes.
Allowed: alcohols, ethers, aromatics, cyclic compounds, esters.
NOT allowed: nitrogen-containing fuel additives.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors, rdMolTransforms
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
import numpy as np
import json, re

print("=" * 65)
print("  F1 2026 E-FUEL MOLECULE SCREENING")
print("  100% sustainable fuel required by 2026 regs")
print("  OpenCure F1 Lab | Nova + Grok + Stephen")
print("=" * 65)

# Candidate sustainable fuel molecules
# All within FIA Article 19 allowed compound classes
fuels = {
    # Current F1 fuel base components
    'toluene':              ('Cc1ccccc1',           'Aromatic - base octane'),
    'isooctane':            ('CC(C)CC(C)(C)C',      '100 octane reference'),
    'ethanol_E10':          ('CCO',                  'Alcohol - current bio addition'),
    
    # High-performance sustainable candidates
    'cyclopentanone':       ('O=C1CCCC1',            'Bio-derived, high octane'),
    'methylfuran_2MF':      ('Cc1ccco1',             'High energy density bio-fuel'),
    'dimethylfuran_DMF':    ('Cc1ccc(C)o1',          'DMF - exceptional octane'),
    'ethyl_levulinate':     ('CCOC(=O)CCC(C)=O',     'Bio-ester, sustainable'),
    'GVL_valerolactone':    ('CC1CCC(=O)O1',         'Green solvent/fuel candidate'),
    'furfuryl_alcohol':     ('OCc1ccco1',             'Biomass-derived'),
    'MTHF_methylTHF':       ('CC1CCCO1',             'Renewable ether'),
    'limonene':             ('CC1=CCC(=C)CC1',       'Terpene - citrus bio-fuel'),
    'pinene_alpha':         ('CC1=CCC2CC1C2(C)C',    'Terpene aviation research'),
    
    # Novel high-octane sustainable compounds (Nova+Grok candidates)
    'methylcyclopentane':   ('CC1CCCC1',             'Cyclic - high density'),
    'bicyclo_hexane':       ('C1CCC2CCCC2C1',        'Bicyclic - novel candidate'),
    'cumene_isopropylbenz': ('CC(C)c1ccccc1',        'Aromatic - high density'),
    'mesitylene':           ('Cc1cc(C)cc(C)c1',      '1,3,5-trimethylbenzene'),
    'cyclopentane':         ('C1CCCC1',              'Pure cyclic'),
    'methylnaphthalene':    ('Cc1ccc2ccccc2c1',      'Heavy aromatic, very high octane'),
}

def parse_formula(formula):
    c = int(re.search(r'C(\d+)', formula).group(1)) if re.search(r'C(\d+)', formula) else (1 if 'C' in formula else 0)
    h_match = re.search(r'H(\d+)', formula)
    h = int(h_match.group(1)) if h_match else (1 if 'H' in formula else 0)
    o_match = re.search(r'O(\d+)', formula)
    o = int(o_match.group(1)) if o_match else (1 if 'O' in formula else 0)
    return c, h, o

results = []
for name, (smiles, desc) in fuels.items():
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            continue
        
        mol_h = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol_h, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol_h)
        
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        formula = CalcMolFormula(mol)
        rings = rdMolDescriptors.CalcNumRings(mol)
        aromatic = rdMolDescriptors.CalcNumAromaticRings(mol)
        rot_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
        
        try:
            c, h, o = parse_formula(formula)
        except:
            c, h, o = 0, 0, 0
        
        # Energy density proxy (kcal/g)
        # C-H bonds release ~4.8 kcal/g; oxygen content reduces energy density
        # Higher C/O ratio = more energy
        co_ratio = c / max(o, 0.1)
        hc_ratio = h / max(c, 1)
        energy_proxy = logp * 8 + co_ratio * 3 + hc_ratio * 2
        
        # Octane proxy
        # Aromatics: highest octane (toluene RON 120)
        # Branching: isomers have higher octane than straight chains
        # Cyclic: good octane
        # Rings resist autoignition = high octane
        octane_proxy = (aromatic * 25) + (rings * 12) + (logp * 4) - (rot_bonds * 3)
        
        # Flame speed proxy (laminar burning velocity)
        # Lighter molecules, more H/C ratio = faster flame
        # Furans and alcohols = fast burning
        furan = 'o1' in smiles or 'O1' in smiles
        alcohol = 'O' in formula and not smiles.startswith('O=')
        flame_proxy = hc_ratio * 10 + (15 if furan else 0) + (8 if alcohol else 0) - mw * 0.05
        
        # Sustainable F1 composite score
        # F1 needs: energy density + octane + flame speed + sustainable source
        f1_fuel_score = energy_proxy * 0.35 + octane_proxy * 0.40 + flame_proxy * 0.25
        
        r = {
            'name': name, 'description': desc, 'formula': formula,
            'MW': round(mw,1), 'LogP': round(logp,2),
            'C_O_ratio': round(co_ratio,2), 'H_C_ratio': round(hc_ratio,2),
            'energy_proxy': round(energy_proxy,1),
            'octane_proxy': round(octane_proxy,1),
            'flame_proxy': round(flame_proxy,1),
            'f1_fuel_score': round(f1_fuel_score,1)
        }
        results.append(r)
        
    except Exception as e:
        print(f"  {name}: {e}")

results.sort(key=lambda x: x['f1_fuel_score'], reverse=True)

print("\n--- E-FUEL RANKINGS FOR F1 2026 ---")
print(f"{'Rank':>4} | {'Molecule':22} | {'F1 Score':>8} | {'Energy':>6} | {'Octane':>6} | {'Flame':>5} | Description")
print("-" * 95)
for i, r in enumerate(results):
    flag = "🔥" if i < 3 else ("✅" if i < 7 else "")
    print(f"  {i+1:>2} | {r['name']:22} | {r['f1_fuel_score']:>8.1f} | {r['energy_proxy']:>6.1f} | {r['octane_proxy']:>6.1f} | {r['flame_proxy']:>5.1f} | {r['description'][:35]} {flag}")

top = results[0]
print(f"\n🏆 TOP E-FUEL CANDIDATE: {top['name']} ({top['formula']})")
print(f"   F1 Score: {top['f1_fuel_score']} | Energy:{top['energy_proxy']} | Octane:{top['octane_proxy']} | Flame:{top['flame_proxy']}")
print(f"   {top['description']}")
print(f"\n   2026 relevance: Higher octane = higher compression ratio in 1.6L V6")
print(f"   = more thermal efficiency beyond current 52% record")
print(f"   = more power from same fuel allowance (105kg per race)")

with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/efuel_screen_results.json','w') as f:
    json.dump(results, f, indent=2)
print("\nResults saved.")
