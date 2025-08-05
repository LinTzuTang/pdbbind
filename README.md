# PDBbind RNA-Ligand Data Processing Pipeline

This repository provides scripts and utilities for downloading, preprocessing, and parsing RNA-ligand complexes from the PDBbind NL dataset [(PDBbind)](https://www.pdbbind-plus.org.cn/). 

---
## Pipeline Overview
### 1. Download Complex Structures
Download all relevant PDBbind complexes (CIF format) as listed in the label CSV.

```bash
python download_pdbbind.py --csv pdbbind_NL_labels.csv --output pdbbind_dataset/complex_database
```

### 2. Extract and Process RNA Chains
Parse each complex and extract the RNA chain, outputting both `.cif` and `.pdb` files.
```bash
python process_rna.py --complexes_dir pdbbind_dataset/complex_database \
                      --output_dir_cif pdbbind_dataset/parsed_rna3db_rnas_whole \
                      --output_dir_pdb pdbbind_dataset/parsed_rna3db_rnas_whole_pdb
```

### 3. Extract and Process Ligands
Extract ligand structures from each complex file based on ligand ID.
```bash
python process_ligand.py --complexes_dir pdbbind_dataset/complex_database \
                         --output_dir_cif pdbbind_dataset/parsed_ligand \
                         --output_dir_pdb pdbbind_dataset/parsed_ligand_pdb
```

---

## Other Functions

### 1. Convert CIF to PDB
Use `convert_cif2pdb.py` to fix naming and convert all CIFs to PDB format.
```bash
python convert_cif2pdb.py --input_dir pdbbind_dataset/parsed_rna3db_rnas_whole \
                          --output_dir pdbbind_dataset/parsed_rna3db_rnas_whole_pdb
```
### 2. Extract RNA Sequences
Batch extract RNA sequences from all parsed CIF files:
```bash
python get_sequences.py --input_dir pdbbind_dataset/parsed_rna3db_rnas_whole \
                        --output pdbbind_NL2020_rna.fasta
```

There are more functions I used to process RNA; see [my GitHub repository](github link) for details.