#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=2GB
#SBATCH --time=08:00:00
#SBATCH --mail-user=cb2610@nyu.edu
#SBATCH --mail-type=END
#SBATCH --job-name=vocab-grep-srun
#
#SBATCH --array=0-74

FILES=(/scratch/cb2610/Common_Crawl/WET_Files_Test75-5/*)

srun ./search_vocab_grep_file.sh ${FILES[$SLURM_ARRAY_TASK_ID]}
