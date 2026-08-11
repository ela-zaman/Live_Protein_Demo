from pathlib import Path

from openmm import app, unit
from openmm.app import PDBFile, Modeller, ForceField


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

input_pdb = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_fixed.pdb"
)

output_pdb = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_solvated.pdb"
)


# ============================================================
# Load fixed protein
# ============================================================

print("=" * 60)
print("LIVE_PROTEIN - OPENMM SYSTEM PREPARATION")
print("=" * 60)

print("\nLoading fixed protein:")
print(input_pdb)

pdb = PDBFile(str(input_pdb))

print(f"\nAtoms: {pdb.topology.getNumAtoms()}")
print(f"Residues: {pdb.topology.getNumResidues()}")


# ============================================================
# Create Modeller
# ============================================================

modeller = Modeller(
    pdb.topology,
    pdb.positions
)


# ============================================================
# Force field
# ============================================================

print("\nLoading force field...")

forcefield = ForceField(
    "amber14-all.xml",
    "amber14/tip3p.xml"
)

print("Force field loaded.")


# ============================================================
# Add hydrogens
# ============================================================

print("\nAdding hydrogens...")

modeller.addHydrogens(
    forcefield,
    pH=7.0
)

print(
    f"Atoms after hydrogen addition: "
    f"{modeller.topology.getNumAtoms()}"
)


# ============================================================
# Add explicit water
# ============================================================




# ============================================================
# Add ions
# ============================================================


print("\nAdding water and ions...")

modeller.addSolvent(
    forcefield,
    model="tip3p",
    padding=1.0 * unit.nanometer,
    ionicStrength=0.15 * unit.molar,
    positiveIon="Na+",
    negativeIon="Cl-"
)

print(
    f"Atoms after solvation and ion addition: "
    f"{modeller.topology.getNumAtoms()}"
)


# ============================================================
# Save solvated structure
# ============================================================

print("\nSaving solvated structure...")

with open(output_pdb, "w") as file:

    PDBFile.writeFile(
        modeller.topology,
        modeller.positions,
        file
    )


print("\n" + "=" * 60)
print("SOLVATED SYSTEM CREATED")
print("=" * 60)

print(f"\nOutput:")
print(output_pdb)