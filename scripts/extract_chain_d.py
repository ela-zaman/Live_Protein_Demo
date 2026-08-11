from pathlib import Path
from Bio.PDB import MMCIFParser, MMCIFIO, Select

PROJECT_ROOT = Path(__file__).resolve().parent.parent

input_file = PROJECT_ROOT / "data" / "raw" / "1OVA.cif"
output_file = PROJECT_ROOT / "data" / "prepared" / "1OVA_chain_D.cif"


class ChainDSelect(Select):
    def accept_chain(self, chain):
        return chain.id == "D"


parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("1OVA", str(input_file))

io = MMCIFIO()
io.set_structure(structure)
io.save(str(output_file), select=ChainDSelect())

print("Extracted Chain D")
print(f"Input : {input_file}")
print(f"Output: {output_file}")