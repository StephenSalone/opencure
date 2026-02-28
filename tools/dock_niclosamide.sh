#!/bin/bash
# Dock Niclosamide into Cruzain active site (Chagas disease target)
# OpenCure.life — First published binding score

cd ~/.openclaw/workspace-science-bot/tools

echo "=== OpenCure Drug Docking Pipeline ==="
echo "Drug: Niclosamide (FDA-approved anti-parasitic)"
echo "Target: Cruzain (Trypanosoma cruzi - Chagas disease)"
echo ""

# Convert protein to PDBQT (Vina format) using conda env
/opt/homebrew/bin/conda run -n drugdiscovery python -c "
import subprocess, os

# Use obabel to convert if available, otherwise use prepare_receptor
try:
    result = subprocess.run(['obabel', '1AIM_fixed.pdb', '-O', 'cruzain.pdbqt', '-xr'], 
                          capture_output=True, text=True)
    print('Receptor converted:', result.returncode)
except:
    print('obabel not found - installing...')
    os.system('conda install -c conda-forge openbabel -y -q')
"

# Install openbabel if needed
/opt/homebrew/bin/conda install -n drugdiscovery -c conda-forge openbabel -y -q 2>/dev/null

# Convert files
/opt/homebrew/bin/conda run -n drugdiscovery bash -c "
obabel 1AIM_fixed.pdb -O cruzain.pdbqt -xr 2>&1 | tail -2
obabel niclosamide_3d.pdb -O niclosamide.pdbqt 2>&1 | tail -2
echo 'Files converted to PDBQT'
"

# Run docking
echo ""
echo "Running AutoDock Vina docking..."
./vina \
  --receptor cruzain.pdbqt \
  --ligand niclosamide.pdbqt \
  --center_x 103.3 \
  --center_y 8.4 \
  --center_z -11.9 \
  --size_x 30 \
  --size_y 30 \
  --size_z 30 \
  --exhaustiveness 8 \
  --num_modes 5 \
  --out niclosamide_docked.pdbqt \
  --log docking_results.txt

echo ""
echo "=== DOCKING RESULTS ==="
cat docking_results.txt
echo ""
echo "Negative kcal/mol = binding affinity (more negative = better binding)"
echo "Anything below -6 kcal/mol is considered promising for drug development"
