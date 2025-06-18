#!/bin/bash

#SBATCH --job-name=SigKernel
#SBATCH --time=48:00:00
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=3700
#SBATCH --gres=gpu:quadro_rtx_6000:1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=Archer.Dodson@warwick.ac.uk

module purge
module load GCC/12.3.0
module load OpenMPI/4.1.5
module load PyTorch/2.1.2-CUDA-12.1.1
module load SciPy-bundle  

source ~/ArcherDissEnv3/bin/activate  #Change environment

srun python ScoreCardWeather.py

deactivate
