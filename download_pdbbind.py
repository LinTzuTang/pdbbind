import argparse
import os
import pandas as pd
from tqdm import tqdm
from Bio.PDB import PDBList


class MmcifDownloader:
    def __init__(self, csv_file, output_dir, num_pdb=None, pdb_id_list=None):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.pdb_list = self._get_pdb_list_from_csv(csv_file, num_pdb, pdb_id_list)

    def _get_pdb_list_from_csv(self, csv_file, num_pdb=None, pdb_id_list=None):
        """
        Get a list of unique PDB IDs from a CSV file.
        """
        if num_pdb and pdb_id_list:
            raise ValueError("Cannot set both num_pdb and pdb_id_list. Please specify only one.")

        df = pd.read_csv(csv_file)
        if pdb_id_list:
            pdb_list = [pdb_id for pdb_id in df["pdb"].tolist() if pdb_id in pdb_id_list]
        else:
            pdb_list = df["pdb"].tolist()
            if num_pdb:
                pdb_list = pdb_list[:num_pdb]
        pdb_list = list(set(pdb_list))
        return pdb_list

    def download_mmcif(self):
        """
        Download mmCIF files from a list of PDB IDs and save them to a specified directory.
        """
        pdbl = PDBList()
        download_failed_log = os.path.join(self.output_dir, "download_failed.txt")

        dld_pdb_list = []
        for pdb_id in tqdm(self.pdb_list, desc="Fetching PDBs", unit="file"):
            cif_file_path = os.path.join(self.output_dir, f"{pdb_id}.cif")
            if os.path.exists(cif_file_path):
                print(f"{cif_file_path} already exists. Skipping download.")
                continue
            try:
                pdbl.retrieve_pdb_file(pdb_id, pdir=self.output_dir, file_format="mmCif")
                dld_pdb_list.append(pdb_id)
            except Exception as e:
                with open(download_failed_log, "a") as f:
                    f.write(f"{pdb_id}: {str(e)}\n")
                print(f"Failed to download {pdb_id}: {str(e)}")

        print(f"{len(dld_pdb_list)} PDBs downloaded successfully.")

    def clean_output_files(self):
        """
        Remove all files in the output directory.
        """
        for file in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Download mmCIF files for a list of PDB IDs from a CSV file.")
    parser.add_argument("--csv_file", type=str, required=True, help="Path to the CSV file containing PDB IDs.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the mmCIF files.")
    parser.add_argument("--num_pdb", type=int, help="Number of PDB IDs to download.")
    parser.add_argument("--pdb_id_list", nargs="+", help="Specific list of PDB IDs to download.")

    args = parser.parse_args()

    # Create an instance of MmcifDownloader
    mmcif_downloader = MmcifDownloader(args.csv_file, args.output_dir, args.num_pdb, args.pdb_id_list)

    # Download the mmCIF files
    mmcif_downloader.download_mmcif()


if __name__ == "__main__":
    main()
