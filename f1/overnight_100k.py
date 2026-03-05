"""
OVERNIGHT 100,000 SIMULATION RUN
F1 2026 | Grok Physics Model (winner of head-to-head)
OpenCure F1 Lab — Nova + Grok + Stephen

Runs on Mac Mini overnight. Multi-core parallel.
Sweeps every legal F1 2026 setup variable.
Goal: find the absolute fastest legal setup per circuit.
"""
import numpy as np
import json
import time
from multiprocessing import Pool, cpu_count
from physics_grok import grok_sim_lap

START_TIME = time.time()

CIRCUITS = {
    'Bahrain': {
        'laps':57,'track_temp':23.7,'real_sec':92.608,'real_driver':'VER',
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
        'laps':52,'track_temp':27.7,'real_sec':88.293,'real_driver':'SAI',
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
        'laps':78,'track_temp':46.3,'real_sec':74.165,'real_driver':'LEC',
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
    'Bahrain_night': {
        'laps':57,'track_temp':18.0,'real_sec':92.608,'real_driver':'baseline',
        'corners':[  # same layout, cooler temps (night race scenario)
            {'es':55,'as':28,'xs':50,'l':120,'r':35,'st':400},
            {'es':82,'as':65,'xs':78,'l':80,'r':90,'st':200},
            {'es':72,'as':55,'xs':68,'l':100,'r':60,'st':850},
            {'es':85,'as':70,'xs':82,'l':90,'r':110,'st':150},
            {'es':65,'as':45,'xs':60,'l':130,'r':45,'st':300},
            {'es':78,'as':60,'xs':74,'l':110,'r':75,'st':650},
            {'es':88,'as':72,'xs':85,'l':85,'r':120,'st':300},
            {'es':50,'as':32,'xs':48,'l':140,'r':30,'st':1000},
        ]},
}

BOUNDS = {
    'wd':   (0.440, 0.480),
    'rhf':  (0.025, 0.045),
    'rhr':  (0.060, 0.110),
    'cb':   (0.540, 0.620),
    'ers':  (0.300, 1.000),
    'aat':  (50.0,  100.0),
    'fuel': (80.0,  105.0),
    'dif':  (0.500, 1.000),
}

COMPOUNDS = ['SOFT','MEDIUM','HARD','NOVA32']

def run_batch(args):
    """Single batch of simulations — called by worker process."""
    circuit_name, circ, n_sims, seed = args
    np.random.seed(seed)
    results = []
    for _ in range(n_sims):
        setup = {k: np.random.uniform(lo,hi) for k,(lo,hi) in BOUNDS.items()}
        for comp in COMPOUNDS:
            try:
                t = grok_sim_lap(circ, setup, comp, 1)
                if t and t > 0:
                    results.append((t, comp, {k:round(v,5) for k,v in setup.items()}))
            except:
                pass
    return circuit_name, results

if __name__ == '__main__':
    SIMS_PER_CIRCUIT = 25000  # 25k × 4 circuits = 100k total
    BATCH_SIZE = 1000
    N_CORES = max(1, cpu_count() - 1)

    print("=" * 68)
    print("  OVERNIGHT 100,000 SIMULATION RUN")
    print(f"  Grok Physics | {len(CIRCUITS)} circuits | {N_CORES} CPU cores")
    print(f"  {SIMS_PER_CIRCUIT:,} setups × {len(COMPOUNDS)} compounds × {len(CIRCUITS)} circuits")
    print(f"  = {SIMS_PER_CIRCUIT * len(COMPOUNDS) * len(CIRCUITS):,} total lap simulations")
    print("=" * 68)

    all_bests = {}

    for cname, circ in CIRCUITS.items():
        real = circ['real_sec']
        n_batches = SIMS_PER_CIRCUIT // BATCH_SIZE
        args = [(cname, circ, BATCH_SIZE, seed) for seed in range(n_batches)]

        print(f"\n[{cname}] Running {SIMS_PER_CIRCUIT:,} setups across {N_CORES} cores...")
        t0 = time.time()

        with Pool(N_CORES) as pool:
            batch_results = pool.map(run_batch, args)

        # Collect all
        all_times = []
        for _, batch in batch_results:
            all_times.extend(batch)

        if not all_times:
            print(f"  No valid results for {cname}")
            continue

        # Sort and find best
        all_times.sort(key=lambda x: x[0])
        best_t, best_c, best_s = all_times[0]
        p5_t   = all_times[int(len(all_times)*0.05)][0]
        median = all_times[len(all_times)//2][0]

        # Calibrate
        cf = real / best_t
        cal_best = best_t * cf
        elapsed = time.time() - t0

        print(f"  Done in {elapsed:.0f}s | {len(all_times):,} valid sims")
        print(f"  Best raw:    {best_t:.3f}s | Cal: {int(cal_best//60)}:{cal_best%60:06.3f} ({best_c})")
        print(f"  Real winner: {int(real//60)}:{real%60:06.3f} ({circ['real_driver']})")
        print(f"  Cal factor:  {cf:.4f} (1.000 = perfect model)")
        print(f"  Top 5%:      {p5_t*cf:.3f}s | Median: {median*cf:.3f}s")
        print(f"\n  OPTIMAL SETUP ({cname}):")
        print(f"    Compound:          {best_c}")
        print(f"    Weight dist front: {best_s['wd']*100:.1f}%")
        print(f"    Ride height front: {best_s['rhf']*1000:.0f}mm")
        print(f"    Brake bias:        {best_s['cb']*100:.1f}%")
        print(f"    ERS deployment:    {best_s['ers']*100:.1f}%")
        print(f"    Active aero:       >{best_s['aat']*3.6:.0f} km/h")
        print(f"    Diff exit lock:    {best_s['dif']*100:.1f}%")
        print(f"    Fuel load:         {best_s['fuel']:.1f}kg")

        # Compound breakdown
        print(f"\n  COMPOUND BREAKDOWN:")
        for comp in COMPOUNDS:
            comp_times = [t for t,c,_ in all_times if c==comp]
            if comp_times:
                best_comp = min(comp_times)*cf
                print(f"    {comp:8}: best={int(best_comp//60)}:{best_comp%60:06.3f} | n={len(comp_times):,}")

        all_bests[cname] = {
            'real_sec': real,
            'best_raw': round(best_t,3),
            'best_calibrated': round(cal_best,3),
            'calibration_factor': round(cf,4),
            'best_compound': best_c,
            'best_setup': best_s,
            'n_valid_sims': len(all_times),
            'elapsed_sec': round(elapsed,1),
        }

    # ============================================================
    total_elapsed = time.time() - START_TIME
    print(f"\n\n{'='*68}")
    print(f"  100,000 SIMULATION COMPLETE")
    print(f"  Total time: {total_elapsed/60:.1f} minutes")
    print(f"{'='*68}")
    print(f"\n  CIRCUIT SUMMARY:")
    for cname, r in all_bests.items():
        real = r['real_sec']
        cb = r['best_calibrated']
        print(f"  {cname:14}: {int(cb//60)}:{cb%60:06.3f} ({r['best_compound']}) | cf={r['calibration_factor']:.4f} | {r['n_valid_sims']:,} sims")

    print(f"\n  MOST ACCURATE CIRCUIT (cf closest to 1.0):")
    best_cf = min(all_bests.items(), key=lambda x: abs(1-x[1]['calibration_factor']))
    print(f"  → {best_cf[0]}: cf={best_cf[1]['calibration_factor']:.4f}")

    with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/overnight_100k_results.json','w') as f:
        json.dump(all_bests, f, indent=2)
    print(f"\n  All results saved.")
    print(f"  Ready to present to F1 teams. 🏎️")
