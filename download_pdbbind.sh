#!/bin/bash
#SBATCH --job-name=download_pdbbind    # Job name
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --cpus-per-task=64
#SBATCH --mem=96gb                   # Job memory request
#SBATCH --partition=bigmem
#SBATCH --time=96:00:00             # Time limit hrs:min:sec
#SBATCH --output=download_pdbbind.log   # Standard output and error log
pwd; hostname; date

module load conda
conda activate hariboss

python download_pdbbind.py --csv_file pdbbind_NL_cleaned.csv --output_dir pdbbind_data/complex_database

date