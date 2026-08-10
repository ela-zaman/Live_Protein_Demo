from openmm.app import PDBFile

pdb = PDBFile("../data/raw/1OVA.pdb")

print("Number of atoms:", pdb.topology.getNumAtoms())
print("Number of residues:", pdb.topology.getNumResidues())
print("Number of chains:", pdb.topology.getNumChains())

for chain in pdb.topology.chains():
    residues = list(chain.residues())

    print(
        f"Chain {chain.id}: "
        f"{len(residues)} residues"
    )