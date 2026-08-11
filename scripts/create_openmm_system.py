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

output_system = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_system.xml"
)


# ============================================================
# Load solvated structure
# ============================================================

print("=" * 60)
print("LIVE_PROTEIN - OPENMM SYSTEM CREATION")
print("=" * 60)

print("\nLoading solvated structure:")
print(input_pdb)

pdb = app.PDBFile(str(input_pdb))

print(f"Atoms: {pdb.topology.getNumAtoms()}")
print(f"Residues: {pdb.topology.getNumResidues()}")


# ============================================================
# Force field
# ============================================================

print("\nLoading force field...")

forcefield = app.ForceField(
    "amber14-all.xml",
    "amber14/tip3p.xml"
)

print("Force field loaded.")


# ============================================================
# Create OpenMM System
# ============================================================

print("\nCreating OpenMM system...")

system = forcefield.createSystem(
    pdb.topology,

    nonbondedMethod=app.PME,

    nonbondedCutoff=1.0 * unit.nanometer,

    constraints=app.HBonds,

    rigidWater=True,

    ewaldErrorTolerance=0.0005
)

print("OpenMM system created.")


# ============================================================
# Save system
# ============================================================

print("\nSaving system XML...")

with open(output_system, "w") as file:
    file.write(openmm.XmlSerializer.serialize(system))


print("\n" + "=" * 60)
print("OPENMM SYSTEM CREATED")
print("=" * 60)

print(f"\nOutput:")
print(output_system)

print("\nSystem configuration:")
print("  Force field : AMBER14")
print("  Water       : TIP3P")
print("  Electrostatics: PME")
print("  Cutoff      : 1.0 nm")
print("  Constraints : HBonds")