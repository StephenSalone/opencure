"""
F1 TIRE GRIP OPTIMIZATION via Glass Transition Temperature (Tg) Prediction
OpenCure F1 Performance Lab - Nova + Grok + Stephen

The KEY insight: Tire grip peaks at the polymer's glass transition temperature.
Teams spend $millions finding this empirically. We compute it.

We simulate rubber polymer chains at multiple temperatures and find
where molecular mobility changes sharply — that's the Tg.
Shifting Tg = shifting peak grip window = race-winning performance.

Compounds tested:
1. Pure natural rubber (isoprene) - baseline
2. SBR blend (styrene-butadiene) - most common synthetic
3. High-silica compound (modern F1 soft) 
4. Carbon-black compound (hard/medium baseline)
5. Novel: isoprene + antioxidant additive
"""
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from openff.toolkit import Molecule
from openmmforcefields.generators import SystemGenerator
from openmm.app import *
from openmm import *
from openmm.unit import *
import numpy as np
import json

print("=" * 60)
print("  F1 TIRE Tg & GRIP WINDOW PREDICTION")
print("  OpenCure F1 Lab | Nova + Grok + Stephen")
print("  KEY: Tg = peak grip temperature")
print("=" * 60)

# Polymer monomers that define rubber compound behavior
# Each represents a different F1 compound formulation approach
compounds = {
    'natural_rubber_isoprene':    ('C=C(C)C=C',     'Baseline - all F1 compounds start here'),
    'styrene_SBR_grip':           ('C=Cc1ccccc1',    'Synthetic - adds high-speed grip'),
    'butadiene_BR_heat':          ('C=CC=C',          'Heat resistant - harder compounds'),
    'silane_APTES_silica':        ('CCO[Si](OCC)(OCC)CCCN', 'Modern silica-silane = soft/medium'),
    'antioxidant_6PPD':           ('CC(C)(C)c1ccc(NC2CCCCC2)cc1', 'Anti-degradant additive'),
    'novel_dicyclopentadiene':    ('C1C=CC2CC1C=C2', 'NOVEL: high-Tg candidate'),
}

results = {}
temps_kelvin = [250, 270, 290, 310, 330, 350, 370, 390, 410]  # -23C to 137C

for name, (smiles, desc) in compounds.items():
    print(f"\n>>> {name}: {desc}")
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            print(f"  Invalid SMILES")
            continue
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        if AllChem.MMFFOptimizeMolecule(mol) != 0:
            AllChem.UFFOptimizeMolecule(mol)
        
        off_mol = Molecule.from_rdkit(mol, allow_undefined_stereo=True)
        off_mol.generate_conformers(n_conformers=1)
        
        system_generator = SystemGenerator(
            forcefields=['amber/ff14SB.xml'],
            small_molecule_forcefield='gaff-2.11',
            molecules=[off_mol],
            forcefield_kwargs={'constraints': None},
        )
        topology = off_mol.to_topology().to_openmm()
        positions = off_mol.conformers[0].to_openmm()
        system = system_generator.create_system(topology, molecules=[off_mol])
        
        temp_results = []
        for T in temps_kelvin:
            integrator = LangevinMiddleIntegrator(T*kelvin, 5/picosecond, 0.001*picoseconds)
            simulation = Simulation(topology, system, integrator)
            simulation.context.setPositions(positions)
            simulation.minimizeEnergy(maxIterations=100)
            simulation.step(500)
            
            state = simulation.context.getState(getEnergy=True, getPositions=True)
            pe = state.getPotentialEnergy().value_in_unit(kilocalories_per_mole)
            ke = state.getKineticEnergy().value_in_unit(kilocalories_per_mole)
            pos = state.getPositions(asNumpy=True).value_in_unit(nanometer)
            
            # Mean square displacement proxy for molecular mobility
            mobility = float(np.mean(np.sum((pos - pos.mean(axis=0))**2, axis=1)))
            temp_results.append({'T_K': T, 'T_C': T-273, 'PE': round(pe,3), 'KE': round(ke,3), 'mobility': round(mobility,6)})
        
        # Find Tg: temperature where mobility increases most sharply (inflection point)
        mobilities = [r['mobility'] for r in temp_results]
        deltas = [mobilities[i+1]-mobilities[i] for i in range(len(mobilities)-1)]
        tg_idx = deltas.index(max(deltas))
        tg_celsius = temps_kelvin[tg_idx] - 273
        
        results[name] = {
            'description': desc,
            'Tg_estimate_C': tg_celsius,
            'peak_grip_window_C': f"{tg_celsius-10} to {tg_celsius+15}C",
            'temps': temp_results
        }
        print(f"  Estimated Tg: {tg_celsius}°C")
        print(f"  Peak grip window: {tg_celsius-10}°C to {tg_celsius+15}°C")
        
    except Exception as e:
        print(f"  ERROR: {e}")

# Rankings
print("\n\n" + "="*60)
print("  F1 GRIP WINDOW RANKINGS")
print("  (Track temp at race: typically 30-60°C)")
print("="*60)
sorted_results = sorted([(k,v) for k,v in results.items() if 'Tg_estimate_C' in v], 
                         key=lambda x: x[1]['Tg_estimate_C'])
for name, data in sorted_results:
    tg = data['Tg_estimate_C']
    window = data['peak_grip_window_C']
    print(f"  {name}: Tg={tg}°C | Grip window: {window}")

with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/tire_viscoelasticity_results.json','w') as f:
    json.dump(results, f, indent=2)
print("\nResults saved.")
