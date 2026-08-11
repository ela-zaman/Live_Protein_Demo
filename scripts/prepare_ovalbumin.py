from pathlib import Path

from pdbfixer import PDBFixer
from openmm.app import PDBFile


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

input_pdb = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_protein.pdb"
)

output_pdb = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_fixed.pdb"
)


# --------------------------------------------------
# Load structure
# --------------------------------------------------

print("=" * 60)
print("LIVE_PROTEIN - OVALBUMIN PREPARATION")
print("=" * 60)

print(f"\nInput structure:")
print(input_pdb)

fixer = PDBFixer(filename=str(input_pdb))


# --------------------------------------------------
# Report missing structural components
# --------------------------------------------------

print("\nChecking structure...")

fixer.findMissingResidues()

if fixer.missingResidues:
    print(
        f"Missing residues detected: "
        f"{len(fixer.missingResidues)}"
    )
else:
    print("Missing residues: None")


fixer.findNonstandardResidues()

if fixer.nonstandardResidues:
    print(
        f"Non-standard residues detected: "
        f"{len(fixer.nonstandardResidues)}"
    )
else:
    print("Non-standard residues: None")


fixer.findMissingAtoms()

print(
    f"Residues with missing atoms: "
    f"{len(fixer.missingAtoms)}"
)

print(
    f"Residues with missing terminals: "
    f"{len(fixer.missingTerminals)}"
)


# --------------------------------------------------
# Replace non-standard residues
# --------------------------------------------------

if fixer.nonstandardResidues:

    print("\nReplacing non-standard residues...")

    fixer.replaceNonstandardResidues()

else:

    print("\nNo non-standard residues to replace.")


# --------------------------------------------------
# Add missing atoms
# --------------------------------------------------

print("\nAdding missing atoms...")

fixer.findMissingAtoms()
fixer.addMissingAtoms()


# --------------------------------------------------
# Save fixed structure
# --------------------------------------------------

print("\nSaving fixed structure...")

with open(output_pdb, "w") as file:

    PDBFile.writeFile(
        fixer.topology,
        fixer.positions,
        file
    )


print("\n" + "=" * 60)
print("PREPARATION COMPLETE")
print("=" * 60)

print(f"\nOutput:")
print(output_pdb)

print("\nNext stage:")
print("Hydrogen addition → Solvation → Ions → OpenMM system")