from pathlib import Path
from Bio.PDB import MMCIFParser, PDBIO, Select


PROJECT_ROOT = Path(__file__).resolve().parent.parent

input_file = PROJECT_ROOT / "data" / "raw" / "1OVA.cif"
output_file = PROJECT_ROOT / "data" / "prepared" / "1OVA_chain_D_protein.pdb"


class ProteinChainDSelect(Select):

    standard_amino_acids = {
        "ALA", "ARG", "ASN", "ASP", "CYS",
        "GLN", "GLU", "GLY", "HIS", "ILE",
        "LEU", "LYS", "MET", "PHE", "PRO",
        "SER", "THR", "TRP", "TYR", "VAL"
    }

    def accept_chain(self, chain):
        # Keep only Chain D
        return chain.id == "D"

    def accept_residue(self, residue):

        residue_name = residue.get_resname().strip()

        # Keep only standard amino acids
        return residue_name in self.standard_amino_acids


# Make sure output directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)


# Read mmCIF
parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("1OVA", str(input_file))


# Save filtered structure
io = PDBIO()
io.set_structure(structure)
io.save(str(output_file), ProteinChainDSelect())


print("=" * 60)
print("CLEAN OVALBUMIN STRUCTURE CREATED")
print("=" * 60)

print(f"Input : {input_file}")
print(f"Output: {output_file}")

print("\nSelected:")
print("  Chain D")
print("  Standard amino acids only")

print("\nRemoved:")
print("  NAG")
print("  HOH")
print("  Other non-protein components")