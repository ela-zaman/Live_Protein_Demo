from pathlib import Path
from Bio.PDB import MMCIFParser

PROJECT_ROOT = Path(__file__).resolve().parent.parent

cif_path = PROJECT_ROOT / "data" / "prepared" / "1OVA_chain_D.cif"

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("1OVA_D", str(cif_path))

model = structure[0]
chain = model["D"]

print("=" * 60)
print("1OVA — CHAIN D")
print("=" * 60)

for residue in chain.get_residues():
    hetflag, resseq, icode = residue.id

    print(
        f"{residue.get_resname():>3} "
        f"{resseq:>4} "
        f"hetflag={hetflag!r}"
    )