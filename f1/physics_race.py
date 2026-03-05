"""
NOVA vs GROK PHYSICS RACE
F1 2026 Lap Time Simulator
OpenCure F1 Lab — Stephen Salone

Running BOTH physics models.
Winner = whichever gets closer to real 2024 lap times.
Then we take the winner and run 100,000 simulations on Mac Mini.
"""
import numpy as np
import json

from physics_nova import nova_sim_lap
from physics_grok import grok_sim_lap

print("=" * 70)
print("  NOVA vs GROK PHYSICS MODELS — HEAD TO HEAD")
print("  F1 2026 | Nova + Grok + Stephen")
print("=" * 70)

CIRCUITS = {
    'Bahrain': {
        'laps':57,'track_temp':23.7,
        'real_sec':92.608,'real_driver':'VER',
        'corners':[
            {'es':55,'as':28,'xs':50,'l':120,'r':35,'st':400},
            {'es':82,'as':65,'xs':78,'l':80,'r':90,'st':200},
            {'es':72,'as':55,'xs':68,'l':100,'r':60,'st':850},
            {'es':85,'as':70,'xs':82,'l':90,'r':110,'st':150},
            {'es':65,'as':45,'xs':60,'l':130,'r':45,'st':300},
            {'es':78,'as':60,'xs':74,'l':110,'r':75,'st':650},
            {'es':88,'as':72,'xs':85,'l':85,'r':120,'st':300},
            {'es':50,'as':32,'xs':48,'l':140,'r':30,'st':1000},
        ]},
    'British': {
        'laps':52,'track_temp':27.7,
        'real_sec':88.293,'real_driver':'SAI',
        'corners':[
            {'es':80,'as':72,'xs':78,'l':90,'r':160,'st':800},
            {'es':85,'as':70,'xs':82,'l':200,'r':100,'st':100},
            {'es':75,'as':62,'xs':72,'l':150,'r':80,'st':600},
            {'es':70,'as':52,'xs':65,'l':120,'r':55,'st':200},
            {'es':55,'as':38,'xs':52,'l':130,'r':35,'st':500},
            {'es':78,'as':65,'xs':75,'l':100,'r':95,'st':400},
            {'es':45,'as':30,'xs':42,'l':150,'r':28,'st':900},
            {'es':82,'as':75,'xs':80,'l':80,'r':180,'st':500},
        ]},
    'Monaco': {
        'laps':78,'track_temp':46.3,
        'real_sec':74.165,'real_driver':'LEC',
        'corners':[
            {'es':45,'as':22,'xs':38,'l':100,'r':18,'st':200},
            {'es':62,'as':48,'xs':58,'l':120,'r':50,'st':500},
            {'es':38,'as':18,'xs':32,'l':80,'r':12,'st':150},
            {'es':30,'as':15,'xs':28,'l':70,'r':10,'st':100},
            {'es':55,'as':40,'xs':52,'l':110,'r':40,'st':300},
            {'es':75,'as':68,'xs':72,'l':200,'r':200,'st':100},
            {'es':55,'as':35,'xs':50,'l':100,'r':30,'st':400},
            {'es':48,'as':28,'xs':42,'l':90,'r':22,'st':350},
        ]},
}

# Best setup from prior optimisation
BEST_SETUP = {
    'wd':0.478,'rhf':0.033,'rhr':0.075,'cb':0.609,
    'ers':0.457,'aat':98.2,'fuel':100.0,'dif':0.985
}

# Calibration: from our prior run we know what scale factor each model needs
# We'll let the data speak — compute raw, then calibrate against real lap times

compounds = ['SOFT','MEDIUM','HARD','NOVA32']
results_nova = {}
results_grok = {}

for cname, circ in CIRCUITS.items():
    real = circ['real_sec']
    print(f"\n{'='*70}")
    print(f"  {cname} | Real: {int(real//60)}:{real%60:06.3f} ({circ['real_driver']})")
    print(f"  {'Compound':8} | {'Nova (raw)':>10} | {'Grok (raw)':>10} | {'Nova cal':>9} | {'Grok cal':>9}")
    print(f"  {'-'*55}")
    
    nova_best = 9999; grok_best = 9999
    nova_best_c = ''; grok_best_c = ''
    
    for comp in compounds:
        try:
            nt = nova_sim_lap(circ, BEST_SETUP, comp, 1)
        except Exception as e:
            nt = None
        try:
            gt = grok_sim_lap(circ, BEST_SETUP, comp, 1)
        except Exception as e:
            gt = None
        
        # Calibrate both to real lap scale
        # Use a fixed calibration: target real lap time at best compound
        nc = nt  # we'll calibrate after finding best
        gc = gt
        
        if nt and nt < nova_best: nova_best = nt; nova_best_c = comp
        if gt and gt < grok_best: grok_best = gt; grok_best_c = comp
        
        nt_str = f"{nt:.2f}" if nt else "ERR"
        gt_str = f"{gt:.2f}" if gt else "ERR"
        print(f"  {comp:8} | {nt_str:>10} | {gt_str:>10}")
    
    # Calibrate best times to real lap times
    nova_cal_factor = real / nova_best if nova_best < 9999 else 1.0
    grok_cal_factor = real / grok_best if grok_best < 9999 else 1.0
    
    nova_cal_best = nova_best * nova_cal_factor
    grok_cal_best = grok_best * grok_cal_factor
    
    nova_err = abs(nova_cal_best - real)
    grok_err = abs(grok_cal_best - real)
    
    print(f"\n  Calibrated best:")
    print(f"    Nova ({nova_best_c}): {int(nova_cal_best//60)}:{nova_cal_best%60:06.3f} | cal factor {nova_cal_factor:.4f}")
    print(f"    Grok ({grok_best_c}): {int(grok_cal_best//60)}:{grok_cal_best%60:06.3f} | cal factor {grok_cal_factor:.4f}")
    print(f"\n  Cal factor closer to 1.0 = more physically accurate model")
    
    nova_closer = abs(1 - nova_cal_factor) < abs(1 - grok_cal_factor)
    winner = "NOVA 🔵" if nova_closer else "GROK 🔴"
    print(f"  🏆 More accurate: {winner} (factor {min(nova_cal_factor,grok_cal_factor):.4f} vs {max(nova_cal_factor,grok_cal_factor):.4f})")
    
    results_nova[cname] = {'raw': nova_best, 'cal': nova_cal_best, 'factor': nova_cal_factor, 'compound': nova_best_c}
    results_grok[cname] = {'raw': grok_best, 'cal': grok_cal_best, 'factor': grok_cal_factor, 'compound': grok_best_c}

# ============================================================
# FINAL VERDICT
# ============================================================
print(f"\n\n{'='*70}")
print(f"  FINAL VERDICT — NOVA vs GROK PHYSICS")
print(f"{'='*70}")

nova_wins = 0; grok_wins = 0
for cname in CIRCUITS:
    real = CIRCUITS[cname]['real_sec']
    nf = results_nova[cname]['factor']
    gf = results_grok[cname]['factor']
    if abs(1-nf) < abs(1-gf):
        nova_wins += 1
        print(f"  {cname}: NOVA wins (factor {nf:.4f} vs {gf:.4f})")
    else:
        grok_wins += 1
        print(f"  {cname}: GROK wins (factor {gf:.4f} vs {nf:.4f})")

print(f"\n  Score: Nova {nova_wins} — Grok {grok_wins}")
if nova_wins > grok_wins:
    print(f"  🏆 NOVA physics model is more accurate")
    print(f"  → Pacejka tire model + braking G-limit = better physics")
    winner_model = 'nova'
elif grok_wins > nova_wins:
    print(f"  🏆 GROK physics model is more accurate")
    print(f"  → Polynomial aero + ride height dynamics = better physics")
    winner_model = 'grok'
else:
    print(f"  🤝 TIE — merge both models for 100,000 sim run")
    winner_model = 'merged'

print(f"\n  Next: Run {winner_model} model x 100,000 simulations on Mac Mini overnight")
print(f"  Command: python3 overnight_100k.py --model {winner_model}")

with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/physics_race_results.json','w') as f:
    json.dump({'nova':results_nova,'grok':results_grok,'winner':winner_model},f,indent=2)
print(f"\nResults saved.")
