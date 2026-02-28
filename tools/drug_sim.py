"""
Protein-Ligand MD Simulation Pipeline
Nova x Grok — Open Source Drug Discovery
Uses: OpenMM 8.4 + OpenFF + RDKit on Apple Silicon
"""

from openmm import *
from openmm.app import *
from openmm.unit import *
from openff.toolkit.topology import Molecule
from openmmforcefields.generators import SystemGenerator
import urllib.request
import sys, os

# === 1. Fetch a real drug target from PDB ===
# Using 1HSG: HIV-1 Protease with bound inhibitor (Indinavir)
PDB_ID = "1HSG"
pdb_file = f"{PDB_ID}_protein.pdb"
ligand_file = f"{PDB_ID}_ligand.sdf"

if not os.path.exists(pdb_file):
    print(f"Fetching {PDB_ID} from RCSB PDB...")
    url = f"https://files.rcsb.org/download/{PDB_ID}.pdb"
    urllib.request.urlretrieve(url, f"{PDB_ID}_raw.pdb")
    print("Downloaded.")

# === 2. Use Aspirin as our test ligand (SMILES — no file needed) ===
print("Loading ligand: Aspirin")
ligand_mol = Molecule.from_smiles("CC(=O)Oc1ccccc1C(=O)O", name="aspirin")
ligand_mol.generate_conformers(n_conformers=1)
print(f"Ligand atoms: {ligand_mol.n_atoms}")

# === 3. Build a minimal protein-free system (ligand in water) for quick test ===
print("\nBuilding ligand-in-water system...")

system_generator = SystemGenerator(
    forcefields=['amber/ff14SB.xml', 'amber/tip3p_standard.xml'],
    small_molecule_forcefield='openff-2.0.0',
    forcefield_kwargs={'constraints': HBonds, 'rigidWater': True},
    periodic_forcefield_kwargs={'nonbondedMethod': PME, 'nonbondedCutoff': 1.0 * nanometer},
    cache='openmm_systems.db'
)
system_generator.add_molecules([ligand_mol])

# Create ligand topology + positions
from openff.toolkit.topology import Topology as OFFTopology
off_topology = ligand_mol.to_topology()
omm_topology = off_topology.to_openmm()

import numpy as np
positions = ligand_mol.conformers[0].to_openmm()

# Solvate
modeller = Modeller(omm_topology, positions)
modeller.addSolvent(
    system_generator.forcefield,
    model='tip3p',
    padding=1.2 * nanometer,
    ionicStrength=0.15 * molar
)
print(f"System atoms after solvation: {modeller.topology.getNumAtoms()}")

# === 4. Create system ===
system = system_generator.create_system(modeller.topology)

# === 5. Integrator + simulation ===
integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 2*femtoseconds)
platform = Platform.getPlatformByName('OpenCL')  # Apple Silicon GPU
print(f"\nUsing platform: OpenCL (Apple Silicon)")

simulation = Simulation(modeller.topology, system, integrator, platform=platform)
simulation.context.setPositions(modeller.positions)

# === 6. Minimize ===
print("Minimizing energy...")
simulation.minimizeEnergy(maxIterations=500)
print("Minimization complete!")

# === 7. Short production run ===
simulation.reporters.append(StateDataReporter(
    sys.stdout, 500,
    step=True, potentialEnergy=True,
    temperature=True, density=True, separator='\t'
))
simulation.reporters.append(DCDReporter('aspirin_in_water.dcd', 1000))

print("\nRunning 2000 steps (~4 ps) of MD...")
print("Step\tPotEnergy(kJ/mol)\tTemp(K)\tDensity(g/mL)")
simulation.step(2000)

print("\n✅ Simulation complete! Trajectory saved: aspirin_in_water.dcd")
print("Nova + Grok just ran drug molecule simulation on Apple Silicon. 🔬")
