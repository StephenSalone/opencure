"""
Niclosamide vs SIRT1 MD Simulation - OpenCure Phase 2: Longevity
Docking score: -10.52 kcal/mol (strongest in entire dataset)
"""
from openmm.app import *
from openmm import *
from openmm.unit import *
from openff.toolkit import Molecule
from openmmforcefields.generators import SystemGenerator

print("=== Niclosamide-SIRT1 MD Simulation ===")
print("Target: SIRT1 (4ZZJ) - Longevity/NAD+ deacetylase")
print("Ligand: Niclosamide (docking: -10.52 kcal/mol — strongest score in dataset)")

pdb = PDBFile('4ZZJ_fixed.pdb')

niclosamide_smiles = "OC(=O)c1ccc(Cl)cc1NC(=O)c1cc([N+](=O)[O-])ccc1Cl"
mol = Molecule.from_smiles(niclosamide_smiles)
mol.generate_conformers(n_conformers=1)
print("Niclosamide conformer generated")

system_generator = SystemGenerator(
    forcefields=['amber/ff14SB.xml', 'amber/tip3p_standard.xml'],
    small_molecule_forcefield='gaff-2.11',
    molecules=[mol],
    forcefield_kwargs={'constraints': HBonds, 'rigidWater': True},
)

modeller = Modeller(pdb.topology, pdb.positions)
modeller.addSolvent(system_generator.forcefield, model='tip3p', padding=1.0*nanometer)
print(f"System built: {modeller.topology.getNumAtoms()} atoms")

system = system_generator.create_system(modeller.topology)
integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
platform = Platform.getPlatformByName('OpenCL')

simulation = Simulation(modeller.topology, system, integrator, platform)
simulation.context.setPositions(modeller.positions)

print("Minimizing...")
simulation.minimizeEnergy(maxIterations=500)
print("Equilibrating (500 steps)...")
simulation.step(500)

print("Production MD (2000 steps = 4 ps)...")
simulation.reporters.append(StateDataReporter(
    'niclosamide_sirt1_md.log', 100, step=True,
    potentialEnergy=True, temperature=True, density=True))
simulation.reporters.append(DCDReporter('niclosamide_sirt1.dcd', 100))
simulation.step(2000)

state = simulation.context.getState(getEnergy=True)
pe = state.getPotentialEnergy().value_in_unit(kilocalories_per_mole)
print(f"\nFinal potential energy: {pe:.2f} kcal/mol")
print("DONE - niclosamide_sirt1.dcd saved")
