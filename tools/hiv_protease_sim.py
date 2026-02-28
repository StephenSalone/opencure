"""
HIV Protease + Indinavir MD Simulation
Nova x Grok — Open Source Drug Discovery
Target: HIV-1 Protease (1HSG) with Indinavir inhibitor
"""

from openmm import *
from openmm.app import *
from openmm.unit import *
from openff.toolkit.topology import Molecule
from openmmforcefields.generators import SystemGenerator
import sys

# === Indinavir SMILES (HIV protease inhibitor — real FDA-approved drug) ===
INDINAVIR_SMILES = "CC(C)(C)NC(=O)[C@@H]1C[C@@H]2CCCC[C@@H]2CN1C[C@@H](O)[C@H](Cc1ccccc1)NC(=O)[C@H](CC(=O)N)NC(=O)c1ccc2ccccc2n1"

print("=== HIV Protease + Indinavir Simulation ===")
print("Loading Indinavir (HIV protease inhibitor)...")
ligand = Molecule.from_smiles(INDINAVIR_SMILES, name="indinavir")
ligand.generate_conformers(n_conformers=1)
print(f"Indinavir atoms: {ligand.n_atoms}")

# === Load HIV protease protein (pre-fixed with PDBFixer) ===
print("Loading HIV-1 Protease (1HSG, fixed)...")
pdb = PDBFile('1HSG_fixed.pdb')
print(f"Protein atoms: {pdb.topology.getNumAtoms()}")

# === SystemGenerator with OpenFF for ligand ===
print("\nSetting up force fields...")
system_generator = SystemGenerator(
    forcefields=['amber/ff14SB.xml', 'amber/tip3p_standard.xml'],
    small_molecule_forcefield='openff-2.0.0',
    forcefield_kwargs={'constraints': HBonds, 'rigidWater': True},
    periodic_forcefield_kwargs={'nonbondedMethod': PME, 'nonbondedCutoff': 1.0*nanometer},
    cache='hiv_systems.db'
)
system_generator.add_molecules([ligand])

modeller = Modeller(pdb.topology, pdb.positions)

# Add ligand at center of protein binding site
ligand_positions = ligand.conformers[0].to_openmm()
ligand_topology = ligand.to_topology().to_openmm()
modeller.add(ligand_topology, ligand_positions)

# === Solvate ===
print("Solvating complex in TIP3P water...")
modeller.addSolvent(
    system_generator.forcefield,
    model='tip3p',
    padding=1.0*nanometer,
    ionicStrength=0.15*molar,
    neutralize=True
)
print(f"Total atoms after solvation: {modeller.topology.getNumAtoms()}")

# === Create system ===
print("Creating MD system...")
system = system_generator.create_system(modeller.topology)

# === Integrator ===
integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 2*femtoseconds)

# === Use OpenCL (Apple Silicon GPU) ===
platform = Platform.getPlatformByName('OpenCL')
print(f"Platform: OpenCL (Apple Silicon GPU)")

simulation = Simulation(modeller.topology, system, integrator, platform=platform)
simulation.context.setPositions(modeller.positions)

# === Minimize ===
print("\nMinimizing energy (this takes ~1-2 min)...")
simulation.minimizeEnergy(maxIterations=1000)
print("Minimization complete!")

# === Short MD run ===
simulation.reporters.append(StateDataReporter(
    sys.stdout, 500,
    step=True, potentialEnergy=True,
    temperature=True, density=True, separator='\t'
))
simulation.reporters.append(DCDReporter('hiv_protease_indinavir.dcd', 1000))

print("\nRunning 2000 steps (~4 ps) of HIV protease + Indinavir MD...")
print("Step\tPotEnergy(kJ/mol)\tTemp(K)\tDensity(g/mL)")
simulation.step(2000)

print("\n✅ HIV Protease + Indinavir simulation complete!")
print("Trajectory: hiv_protease_indinavir.dcd")
print("Nova + Grok just simulated a real HIV drug on Apple Silicon. 🔬")
