from pathlib import Path

import openmm
from openmm import app, unit


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

input_pdb = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_solvated.pdb"
)

input_system = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_system.xml"
)

output_pdb = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_minimized.pdb"
)


# ============================================================
# Load structure
# ============================================================

print("=" * 60)
print("LIVE_PROTEIN - ENERGY MINIMIZATION")
print("=" * 60)

print("\nLoading solvated structure...")

pdb = app.PDBFile(str(input_pdb))

print(f"Atoms: {pdb.topology.getNumAtoms()}")
print(f"Residues: {pdb.topology.getNumResidues()}")


# ============================================================
# Load OpenMM system
# ============================================================

print("\nLoading OpenMM system...")

with open(input_system, "r") as file:
    system = openmm.XmlSerializer.deserialize(file.read())

print("System loaded.")


# ============================================================
# Create integrator
# ============================================================

temperature = 300 * unit.kelvin

integrator = openmm.LangevinMiddleIntegrator(
    temperature,
    1.0 / unit.picosecond,
    0.002 * unit.picoseconds
)


# ============================================================
# Select platform
# ============================================================

print("\nSelecting OpenMM platform...")

platform = openmm.Platform.getPlatformByName("CPU")

print(f"Platform: {platform.getName()}")


# ============================================================
# Create simulation
# ============================================================

simulation = app.Simulation(
    pdb.topology,
    system,
    integrator,
    platform
)


# ============================================================
# Set initial positions
# ============================================================

simulation.context.setPositions(pdb.positions)


# ============================================================
# Initial energy
# ============================================================

state = simulation.context.getState(
    getEnergy=True
)

initial_energy = state.getPotentialEnergy()

print("\nInitial potential energy:")
print(initial_energy)


# ============================================================
# Energy minimization
# ============================================================

print("\nRunning energy minimization...")

simulation.minimizeEnergy(
    tolerance=10 * unit.kilojoule_per_mole / unit.nanometer,
    maxIterations=5000
)


# ============================================================
# Final energy
# ============================================================

state = simulation.context.getState(
    getEnergy=True,
    getPositions=True
)

final_energy = state.getPotentialEnergy()

print("\nFinal potential energy:")
print(final_energy)


# ============================================================
# Save minimized structure
# ============================================================

print("\nSaving minimized structure...")

with open(output_pdb, "w") as file:

    app.PDBFile.writeFile(
        simulation.topology,
        state.getPositions(),
        file
    )


# ============================================================
# Final report
# ============================================================

print("\n" + "=" * 60)
print("ENERGY MINIMIZATION COMPLETE")
print("=" * 60)

print(f"\nOutput:")
print(output_pdb)

print("\nInitial energy:")
print(initial_energy)

print("\nFinal energy:")
print(final_energy)