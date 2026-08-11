from pathlib import Path
from Bio.PDB import PDBParser


PROJECT_ROOT = Path(__file__).resolve().parent.parent

pdb_file = (
    PROJECT_ROOT
    / "data"
    / "prepared"
    / "1OVA_chain_D_protein.pdb"
)


parser = PDBParser(QUIET=True)
structure = parser.get_structure("1OVA_D", str(pdb_file))


model = structure[0]

chains = list(model.get_chains())
residues = list(model.get_residues())
atoms = list(model.get_atoms())


print("=" * 60)
print("CLEAN PROTEIN VERIFICATION")
print("=" * 60)

print(f"Chains : {len(chains)}")
print(f"Residues: {len(residues)}")
print(f"Atoms   : {len(atoms)}")

print("\nChains:")

for chain in chains:

    chain_residues = list(chain.get_residues())
    chain_atoms = list(chain.get_atoms())

    print(
        f"Chain {chain.id}: "
        f"{len(chain_residues)} residues, "
        f"{len(chain_atoms)} atoms"
    )


print("\nFirst residue:")
print(
    residues[0].get_resname(),
    residues[0].id
)

print("\nLast residue:")
print(
    residues[-1].get_resname(),
    residues[-1].id
)