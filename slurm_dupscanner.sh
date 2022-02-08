#!/bin/bash
#SBATCH --ntasks=12                   # Number of processes
#SBATCH --partition=cpu
#SBATCH --job-name=dupscanner # Job name
#SBATCH --error=dupscan.err
#SBATCH --output=dupscan.out
#SBATCH --nodes=1                    # Run all processes on a single node	
#SBATCH --mem-per-cpu=5GB

module load imod
# probably load anaconda & the environment as well

python3 microduplicate_screener/microduplicate_screener.py --i MotionCorr/optics_group3/corrected_micrographs.star --bin 8 --scanrange 34 --imagespermove 16 --imagesperhole 4 --j 12 --csvout duplicate_group3.csv
