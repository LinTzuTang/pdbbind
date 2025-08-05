import pandas as pd
import os
import logging
from Bio import PDB
from convert_cif2pdb import convert_cif_to_pdb

# Initialize the logger
logging.basicConfig(filename='cif_processing.log', level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def extract_ligand_from_cif(cif_path, pdbid, ligand_id, output_dir):
    parsed_info = PDB.MMCIF2Dict.MMCIF2Dict(cif_path)

    # Columns for atom site data
    atom_site_columns = [
        "_atom_site.group_PDB",
        "_atom_site.id",
        "_atom_site.type_symbol",
        "_atom_site.label_atom_id",
        "_atom_site.label_alt_id",
        "_atom_site.label_comp_id",
        "_atom_site.label_asym_id",
        "_atom_site.label_entity_id",
        "_atom_site.label_seq_id",
        "_atom_site.pdbx_PDB_ins_code",
        "_atom_site.Cartn_x",
        "_atom_site.Cartn_y",
        "_atom_site.Cartn_z",
        "_atom_site.occupancy",
        "_atom_site.B_iso_or_equiv",
        "_atom_site.pdbx_formal_charge",
        "_atom_site.auth_seq_id",
        "_atom_site.auth_comp_id",
        "_atom_site.auth_asym_id",
        "_atom_site.auth_atom_id",
        "_atom_site.pdbx_PDB_model_num"
    ]

    # Group atom site data by ligand and chain
    ligands_data = {}
    num_entries = sum([i == '1' for i in parsed_info["_atom_site.pdbx_PDB_model_num"]])  # get model 1 only

    for i in range(num_entries):
        if (parsed_info["_atom_site.group_PDB"][i] == "HETATM" and
            parsed_info["_atom_site.label_comp_id"][i] == ligand_id):
            
            chain_id = parsed_info["_atom_site.label_asym_id"][i]
            key = f"{ligand_id}_{chain_id}"
            
            if key not in ligands_data:
                ligands_data[key] = []
            entry = [parsed_info[col][i] for col in atom_site_columns]
            ligands_data[key].append(entry)

    # Write each ligand-chain pair to separate CIF files
    if not ligands_data:
        error_message = f"No atom site data found for PDB ID: {pdbid}, Ligand ID: {ligand_id}"
        logging.error(error_message)
        print(error_message)
    else:
        for key, atom_site_data in ligands_data.items():
            ligand, chain = key.split("_")
            output_cif_path = os.path.join(output_dir, f"{pdbid}_{ligand}_{chain}.cif")

            with open(output_cif_path, 'w') as cif_file:
                cif_file.write(f"data_ligand_{pdbid}_{ligand}_{chain}\n")
                
                # Write atom site data
                cif_file.write("loop_\n")
                for col in atom_site_columns:
                    cif_file.write(f"{col}\n")
                for entry in atom_site_data:
                    cif_file.write(" ".join(map(str, entry)) + "\n")
            
            print(f"Processed and wrote data for {pdbid} - Ligand ID: {ligand}, Chain: {chain}")

def process_csv_and_extract_ligands(csv_path, cif_dir, output_dir):
    df = pd.read_csv(csv_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for index, row in df.iterrows():
        cif_path = os.path.join(cif_dir, f"{row['pdb']}.cif")
        try:
            extract_ligand_from_cif(
                cif_path=cif_path,
                pdbid=row['pdb'],
                ligand_id=row['ligand'],
                output_dir=output_dir
            )
        except ValueError as e:
            print(e)

def parse_cif_file(cif_file_path):
    parser = PDB.MMCIFParser()
    structure = parser.get_structure("structure", cif_file_path)
    
    # Print some details to verify the parsing
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    print(atom)

def main():
    # Directly set the paths
    csv_path = 'pdbbind_NL_cleaned.csv'
    cif_dir = 'pdbbind_dataset/complex_database'
    output_dir = 'pdbbind_dataset/parsed_ligand'
    output_pdb_dir = 'pdbbind_dataset/parsed_ligand_pdb'
    
    if not os.path.exists(output_pdb_dir):
        os.makedirs(output_pdb_dir)
    
    # Process the CSV and extract ligands to CIF files
    process_csv_and_extract_ligands(csv_path, cif_dir, output_dir)

    # Parse the generated CIF files to test
    for filename in os.listdir(output_dir):
        if filename.endswith('.cif'):
            cif_file_path = os.path.join(output_dir, filename)
            print(f"Parsing {cif_file_path}")
            pdb_file_path = os.path.join(output_pdb_dir, filename.replace('.cif', '.pdb'))
            convert_cif_to_pdb(cif_file_path, pdb_file_path)

if __name__ == "__main__":
    main()
