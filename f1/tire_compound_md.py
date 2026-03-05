"""
F1 Tire Compound Molecular Dynamics
OpenCure F1 Performance Lab - Nova + Grok + Stephen

Comparing key polymer components used in F1 tire rubber:
- cis-1,4-Polyisoprene (natural rubber - base compound)
- Styrene monomer (SBR component - synthetic grip)  
- Butadiene (BR component - heat resistance)
- Silica coupling agent TESPT (modern F1 compound additive)

We measure thermal stability and molecular flexibility as proxies
for grip performance and heat degradation resistance.
"""
from openmm.app import *
from openmm import *
from openmm.unit import *
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

print("=" * 55)
print("  F1 TIRE COMPOUND MOLECULAR DYNAMICS")
print("  OpenCure F1 Lab | Nova + Grok + Stephen")
print("=" * 55)

# Key molecules in F1 tire compounds
compounds = {
    'isoprene_monomer':   'C=C(C)C=C',           # Natural rubber building block
    'styrene':            'C=Cc1ccccc1',           # SBR component (grip)
    'butadiene':          'C=CC=C',                # BR component (heat resist)
    'toluene_diisocyanate': 'O=C=Nc1ccc(C)c(N=C=O)c1',  # Crosslinker
    'silane_APTES':       'CCO[Si](OCC)(OCC)CCCN', # Silica coupling agent
}

results = {}
for name, smiles in compounds.items():
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        
        # Write to SDF for OpenMM
        writer = Chem.SDWriter(f'/tmp/{name}.sdf')
        writer.write(mol)
        writer.close()
        
        from openff.toolkit import Molecule
        from openmmforcefields.generators import SystemGenerator
        
        off_mol = Molecule.from_rdkit(mol)
        off_mol.generate_conformers(n_conformers=1)
        
        system_generator = SystemGenerator(
            forcefields=['amber/ff14SB.xml', 'amber/tip3p_standard.xml'],
            small_molecule_forcefield='gaff-2.11',
            molecules=[off_mol],
            forcefield_kwargs={'constraints': HBonds, 'rigidWater': True},
        )
        
        # Build solvated system
        modeller = Modeller(Topology(), [])
        modeller.add(off_mol.to_topology().to_openmm(), off_mol.conformers[0].to_openmm())
        
        from openmm.app import Modeller
        from openmm import Vec3
        import openmm.unit as unit

        # Simple vacuum simulation for thermal property estimation
        topology = off_mol.to_topology().to_openmm()
        positions = off_mol.conformers[0].to_openmm()
        
        system = system_generator.create_system(topology, molecules=[off_mol])
        
        # Run at 300K (ambient) and 373K (racing temp ~100C)
        temps = [(300, 'ambient_300K'), (373, 'racing_100C'), (423, 'extreme_150C')]
        mol_results = {}
        for temp_k, label in temps:
            integrator = LangevinMiddleIntegrator(temp_k*kelvin, 1/picosecond, 0.001*picoseconds)
            simulation = Simulation(topology, system, integrator)
            simulation.context.setPositions(positions)
            simulation.minimizeEnergy()
            simulation.step(1000)
            state = simulation.context.getState(getEnergy=True, getPositions=True)
            pe = state.getPotentialEnergy().value_in_unit(kilocalories_per_mole)
            ke = state.getKineticEnergy().value_in_unit(kilocalories_per_mole)
            mol_results[label] = {'PE': round(pe,3), 'KE': round(ke,3), 'Total': round(pe+ke,3)}
        
        results[name] = mol_results
        print(f"\n{name}:")
        for label, vals in mol_results.items():
            print(f"  {label}: PE={vals['PE']:.2f}, KE={vals['KE']:.2f} kcal/mol")
            
    except Exception as e:
        print(f"{name}: ERROR - {e}")

import json
with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/tire_compound_results.json','w') as f:
    json.dump(results, f, indent=2)
print("\n\nResults saved to f1/tire_compound_results.json")
print("DONE")
