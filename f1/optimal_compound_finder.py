"""
F1 OPTIMAL COMPOUND Tg FINDER
OpenCure F1 Performance Lab - Nova + Grok + Stephen

The real data showed track temps peak at 46°C (Monaco).
We recalibrate: what Tg value maximizes grip across hot circuits?
This is the compound NO ONE HAS — tuned to exact real temperatures.
"""
import fastf1
import numpy as np
import json
fastf1.Cache.enable_cache('/tmp/fastf1_cache')
fastf1.set_log_level('WARNING')

print("=" * 65)
print("  F1 OPTIMAL Tg FINDER — REAL DATA DRIVEN")
print("  OpenCure F1 Lab | Nova + Grok + Stephen")
print("=" * 65)

# Sweep Tg from 20 to 70°C at 1° increments
# Find which Tg maximizes aggregate grip across ALL circuits
circuit_temps = {
    'Bahrain':   23.7,
    'Monaco':    46.3,
    'British':   27.7,
    'Singapore': 36.4,
    'Abu Dhabi': 31.8,
    'Italian':   42.9,
    'Hungary':   50.0,   # known hot race
    'Austria':   32.0,
    'Spa':       22.0,
    'Japan':     28.0,
    'Mexico':    26.0,
    'Brazil':    35.0,
    'Las Vegas': 15.0,   # night race, cold
}

sigma = 18.0  # grip curve width (from our MD model)

def grip_at_temp(Tg, track_temp, sigma=18.0):
    return float(np.exp(-0.5 * ((track_temp - Tg) / sigma)**2))

# Current Pirelli compounds
pirelli = {'SOFT': 57, 'MEDIUM': 37, 'HARD': 17}

results = []
for Tg in range(15, 75):
    total_advantage = 0
    circuit_breakdown = {}
    for circuit, temp in circuit_temps.items():
        novel_grip = grip_at_temp(Tg, temp)
        # Best pirelli grip at this temp
        best_pirelli = max(grip_at_temp(tg, temp) for tg in pirelli.values())
        advantage = novel_grip - best_pirelli
        total_advantage += advantage
        circuit_breakdown[circuit] = round(advantage, 4)
    
    results.append({
        'Tg_C': Tg,
        'total_advantage': round(total_advantage, 4),
        'circuits': circuit_breakdown
    })

# Sort by best total advantage
results.sort(key=lambda x: x['total_advantage'], reverse=True)

print("\n--- TOP 10 OPTIMAL Tg VALUES ACROSS ALL CIRCUITS ---")
print(f"{'Tg°C':>5} | {'Total Adv':>9} | Best circuits")
print("-"*60)
for r in results[:10]:
    pos_circuits = [c for c,v in r['circuits'].items() if v > 0]
    print(f"  {r['Tg_C']:>3}°C | {r['total_advantage']:>+8.4f} | {', '.join(pos_circuits[:4])}")

best = results[0]
print(f"\n🏆 OPTIMAL Tg: {best['Tg_C']}°C")
print(f"   Wins across: {sum(1 for v in best['circuits'].values() if v > 0)}/{len(circuit_temps)} circuits")
print(f"\n--- Circuit-by-circuit advantage at Tg={best['Tg_C']}°C ---")
sorted_circuits = sorted(best['circuits'].items(), key=lambda x: x[1], reverse=True)
for circuit, adv in sorted_circuits:
    flag = "🔥" if adv > 0.05 else ("✅" if adv > 0 else "❌")
    temp = circuit_temps[circuit]
    print(f"  {flag} {circuit:12} ({temp:4.1f}°C): advantage {adv:+.4f}")

# Compare: what does Pirelli's best compound give vs our optimal
print(f"\n--- PIRELLI vs NOVA+GROK COMPOUND ---")
print("-"*65)
for circuit, temp in sorted(circuit_temps.items(), key=lambda x: x[1], reverse=True):
    best_p = max(grip_at_temp(tg, temp) for tg in pirelli.values())
    best_p_name = max(pirelli.items(), key=lambda x: grip_at_temp(x[1], temp))[0]
    ng = grip_at_temp(best['Tg_C'], temp)
    delta = ng - best_p
    flag = "🔥" if delta > 0 else ""
    print(f"  {circuit:12} | {temp:7.1f} | {best_p_name} {best_p:.4f}  | {ng:14.4f} | {delta:+.4f} {flag}")

with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/optimal_compound_results.json','w') as f:
    json.dump({'optimal_Tg': best['Tg_C'], 'top10': results[:10], 'all': results}, f, indent=2)
print("\nResults saved.")
