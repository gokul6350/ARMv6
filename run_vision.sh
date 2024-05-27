#!/bin/bash

echo "
██╗░░░██╗██╗░██████╗██╗░█████╗░███╗░░██╗  ░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░
██║░░░██║██║██╔════╝██║██╔══██╗████╗░██║  ██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗
╚██╗░██╔╝██║╚█████╗░██║██║░░██║██╔██╗██║  ╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝
░╚████╔╝░██║░╚═══██╗██║██║░░██║██║╚████║  ░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗
░░╚██╔╝░░██║██████╔╝██║╚█████╔╝██║░╚███║  ██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║
░░░╚═╝░░░╚═╝╚═════╝░╚═╝░╚════╝░╚═╝░░╚══╝  ╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
"

cd ./vision_server

# Source the conda.sh script
source ~/miniconda3/etc/profile.d/conda.sh  # Adjust this path if necessary

# Activate the conda environment
conda activate vision

# Run the Python scripts
python detech_config.py
python app.py

# Deactivate the conda environment
conda deactivate

