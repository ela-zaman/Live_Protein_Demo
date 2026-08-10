from pathlib import Path
from Bio.PDB import MMCIFParser

PROJECT_ROOT = Path(__file__).resolve().parent.parent
cif_path = PROJECT_ROOT / "data" / "raw" / "1OVA.cif"

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("1OVA", str(cif_path))

model = structure[0]

standard_amino_acids = {
    "ALA", "ARG", "ASN", "ASP", "CYS",
    "GLN", "GLU", "GLY", "HIS", "ILE",
    "LEU", "LYS", "MET", "PHE", "PRO",
    "SER", "THR", "TRP", "TYR", "VAL"
}

print("=" * 60)
print("1OVA PROTEIN CHAIN ANALYSIS")
print("=" * 60)

for chain in model:

    residues = list(chain.get_residues())

    protein_residues = [
        residue
        for residue in residues
        if residue.get_resname().strip() in standard_amino_acids
    ]

    other_residues = [
        residue
        for residue in residues
        if residue.get_resname().strip() not in standard_amino_acids
    ]

    print(f"\nCHAIN {chain.id}")
    print("-" * 60)

    print(f"Total residues:        {len(residues)}")
    print(f"Protein residues:      {len(protein_residues)}")
    print(f"Other residues:        {len(other_residues)}")

    if protein_residues:
        first = protein_residues[0]
        last = protein_residues[-1]

        print(
            f"Protein starts:        "
            f"{first.get_resname()} {first.id[1]}"
        )

        print(
            f"Protein ends:          "
            f"{last.get_resname()} {last.id[1]}"
        )

    if other_residues:

        other_types = sorted(
            set(
                residue.get_resname().strip()
                for residue in other_residues
            )
        )

        print(
            f"Other residue types:   "
            f"{other_types}"
        )

    print(
        f"Protein atom count:    "
        f"{sum(len(list(r.get_atoms())) for r in protein_residues)}"
    )

print("\n" + "=" * 60)
for chain in model:
    protein_residues = [
        residue
        for residue in chain.get_residues()
        if residue.get_resname().strip() in standard_amino_acids
    ]

    print(
        f"Chain {chain.id}: "
        f"{len(protein_residues)} protein residues, "
        f"{sum(len(list(r.get_atoms())) for r in protein_residues)} protein atoms"
    )