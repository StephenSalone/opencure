#!/bin/bash
# Run remaining 30 races when FastF1 rate limit resets (1hr after 22:20 CST)
sleep 3600
cd /Users/stephensalone/.openclaw/workspace-science-bot/f1
/opt/homebrew/bin/conda run -n drugdiscovery python3 mass_simulation.py >> mass_sim_run2.log 2>&1
echo "Done" >> mass_sim_run2.log
