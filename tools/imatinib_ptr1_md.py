"""
Imatinib vs PTR1 (Leishmania) MD Simulation - OpenCure.life
"""
from openmm.app import *
from openmm import *
from openmm.unit import *
from openff.toolkit import Molecule
from openmmforcefields.generators import SystemGenerator

print("=== Imatinib-PTR1 MD Simulation ===")
print("Target: PTR1 (2BFA) - Leishmania major")
print("Ligand: Imatinib (docking: -8.273 kcal/mol)")

pdb = PDBFile('2BFA_fixed.pdb')

imatinib_smiles = "Cc1ccc(cc1Nc2nccc(n2)c3cccnc3)NC(=O)c4ccc(cc4)CN5CCN(CC5)C"
mol = Molecule.from_smiles(imatinib_smiles)
mol.generate_conformers(n_conformers=1)
print("Imatinib conformer generated")

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
    'imatinib_ptr1_md.log', 100, step=True,
    potentialEnergy=True, temperature=True, density=True))
simulation.reporters.append(DCDReporter('imatinib_ptr1.dcd', 100))
simulation.step(2000)

state = simulation.context.getState(getEnergy=True)
pe = state.getPotentialEnergy().value_in_unit(kilocalories_per_mole)
print(f"\nFinal potential energy: {pe:.2f} kcal/mol")
print("DONE - imatinib_ptr1.dcd saved")
