#!/bin/bash
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=5
#SBATCH --time=90:00:00
#SBATCH --partition=cmb
#SBATCH --mem=10G
cd /home/pmd-01/zhuliu/project/ye/selection
source env/bin/activate
date
python3 m1.py 0.6 0.5 0.7
date
