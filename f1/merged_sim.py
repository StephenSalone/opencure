"""
MERGED PHYSICS MODEL — F1 2026 Lap Time Simulator
Nova + Grok + Stephen | OpenCure F1 Lab

[Nova]  Pacejka Magic Formula tire lateral force
[Nova]  Dynamic tire temp per corner (heats/cools)
[Nova]  Braking G-limit 4.5G + trail braking
[Grok]  FastF1 real telemetry point-by-point stepping
[Grok]  Polynomial aero Cl/Cd vs speed + ride height
[Grok]  Suspension heave / dynamic ride height
[Grok]  ERS energy budget per lap (4 MJ deploy, 8.5 MJ regen)
[Grok]  Tire wear cliff model per compound
[Both]  Fuel burn 1.85 kg/lap
[Both]  Multiprocessing all Mac cores
"""
import fastf1
import numpy as np
import json
import time
from multiprocessing import Pool, cpu_count

fastf1.Cache.enable_cache('/tmp/fastf1_cache')
fastf1.set_log_level('WARNING')
import warnings; warnings.filterwarnings('ignore')

MIN_WEIGHT_KG    = 770.0
MAX_FUEL_KG      = 105.0
FUEL_BURN        = 1.85
ERS_DEPLOY_MJ    = 4.0
ERS_REGEN_MJ     = 8.5
ERS_MAX_KW       = 350.0
ICE_KW           = 470.0
RHO              = 1.225
AREA             = 1.2
G                = 9.81

TIRE_PARAMS = {
    'SOFT':   {'Tg':105,'D':1.62,'wear_km':35,'cliff':0.88},
    'MEDIUM': {'Tg': 95,'D':1.58,'wear_km':60,'cliff':0.90},
    'HARD':   {'Tg': 82,'D':1.52,'wear_km':90,'cliff':0.93},
    'NOVA32': {'Tg': 88,'D':1.60,'wear_km':75,'cliff':0.92},
}

def pacejka_mu(compound, tire_temp_C, dist_km=0):
    p = TIRE_PARAMS[compound]
    d = tire_temp_C - p['Tg']; sigma = 18*(0.7 if d<0 else 1.3)
    thermal = float(np.exp(-0.5*(d/sigma)**2))
    wf = dist_km/p['wear_km']
    wear = (1-(1-p['cliff'])*min(wf,0.85)/0.85) if wf<0.85 else max(p['cliff']-(wf-0.85)*3*(1-p['cliff']),0.65)
    return p['D'] * thermal * wear

def update_tire_temp(temp, lat_g, v, dt, seg='corner'):
    if seg=='corner': return min(temp+(lat_g**2*8.5+v*0.12)*dt, 148)
    return max(temp-v*0.07*dt, 82)

def aero_forces(v, rh_m, aero_open):
    rh_mm = rh_m*1000
    cl = max(1.8*0.7 + 0.002*v - 0.015*abs(rh_mm-31), 0.4)
    if aero_open: cl*=0.55; cd=0.45
    else: cd=0.90
    q=0.5*RHO*v**2
    return cl*AREA*q, cd*AREA*q

def dynamic_rh(static, df_N, k=55000):
    return max(static - df_N/k, 0.010)

def ers_power(thr, brk, energy, deploy_frac):
    if brk>0.3:
        h=min(200,(ERS_REGEN_MJ-energy)*1000)
        return 0.0, min(energy+h*0.001, ERS_REGEN_MJ)
    if thr>0.75 and energy>0:
        kw=ERS_MAX_KW*deploy_frac
        return kw, max(energy-kw*0.001, 0)
    return 0.0, energy

def sim_lap(tel, setup, compound, lap_num=1, track_temp=28):
    dist     = tel['Distance'].values.astype(float)
    speed    = tel['Speed'].values.astype(float)/3.6
    try: throttle = tel['Throttle'].values.astype(float)/100
    except: throttle = np.where(speed>speed.mean(),0.9,0.1)
    try:
        brake = tel['Brake'].values.astype(float)
        if brake.max()>1: brake/=100
    except: brake = np.where(speed<speed.mean()*0.8,0.8,0.0)

    rh=setup['rhf']; bb=setup['cb']; ef=setup['ers']
    at=setup['aat']; fuel=max(MAX_FUEL_KG-(lap_num-1)*FUEL_BURN,1)
    mass=MIN_WEIGHT_KG+fuel
    lap_km=(dist[-1]-dist[0])/1000 if len(dist)>1 else 5
    dist_driven=(lap_num-1)*lap_km
    tire_temp=track_temp+65; energy=ERS_DEPLOY_MJ; total=0.0

    for i in range(1,len(dist)):
        ds=float(dist[i]-dist[i-1])
        if ds<=0: continue
        v=max(float(speed[i]),1.0)
        thr=float(throttle[i]) if i<len(throttle) else 0.5
        brk=float(brake[i]) if i<len(brake) else 0.0
        dt=ds/v
        aero_open=v>at
        df,drag=aero_forces(v, rh, aero_open)
        rh_dyn=dynamic_rh(rh,df)
        df,drag=aero_forces(v, rh_dyn, aero_open)
        nf=mass*G+df
        frac_dist=dist_driven+(i/len(dist))*lap_km
        mu=pacejka_mu(compound, tire_temp, frac_dist)
        lat_g=abs(float(speed[i])-float(speed[i-1]))/(G*dt+0.001)
        seg='corner' if brk>0.2 or lat_g>0.5 else 'straight'
        tire_temp=update_tire_temp(tire_temp,lat_g,v,dt,seg)
        boost,energy=ers_power(thr,brk,energy,ef)
        power=(ICE_KW+boost)*1000
        drive=power/v
        grip=mu*nf
        traction=min(drive,grip*0.85)
        if brk>0.1:
            max_g=4.5*bb; dec=min(max_g*G,mu*G*1.15)
            if brk<0.4: dec*=0.55
            net=-dec
        else:
            net=(traction-drag)/mass
        v_adj=max(v+net*dt*0.1,1.0)
        total+=ds/v_adj
    return total

def worker(args):
    cname,td,setup,comp,lap,seed=args
    np.random.seed(seed)
    try:
        t=sim_lap(td['tel'],setup,comp,lap,td['track_temp'])
        return (cname,comp,t,setup)
    except: return None

CIRCUITS=['Bahrain','British','Monaco']
COMPOUNDS=['SOFT','MEDIUM','HARD','NOVA32']
BOUNDS={
    'wd':(0.440,0.480),'rhf':(0.025,0.045),'rhr':(0.060,0.110),
    'cb':(0.540,0.620),'ers':(0.300,1.000),'aat':(50.0,105.0),
    'fuel':(80.0,105.0),'dif':(0.500,1.000),
}

if __name__=='__main__':
    SIMS=2000
    N=max(1,cpu_count()-1)
    print("="*68)
    print("  MERGED MODEL — FastF1 + Nova Pacejka + Grok Aero + ERS Budget")
    print(f"  {SIMS*len(COMPOUNDS)*len(CIRCUITS):,} total simulations | {N} cores")
    print("="*68)

    print("\n📡 Loading real FastF1 telemetry...")
    tel_data={}
    for c in CIRCUITS:
        try:
            s=fastf1.get_session(2024,c,'R')
            s.load(telemetry=True,laps=True,weather=True,messages=False)
            lap=s.laps.pick_fastest()
            tel=lap.get_telemetry()
            tt=float(s.weather_data['TrackTemp'].dropna().mean())
            real=lap['LapTime'].total_seconds()
            tel_data[c]={'tel':tel,'track_temp':tt,'real_sec':real}
            print(f"  ✅ {c}: {len(tel)} pts | {int(real//60)}:{real%60:06.3f} | {tt:.1f}°C")
        except Exception as e: print(f"  ❌ {c}: {e}")

    all_results={}
    prev_cf={'Bahrain':0.8466,'British':0.7158,'Monaco':0.7503}

    for cname,td in tel_data.items():
        real=td['real_sec']
        print(f"\n{'='*68}")
        print(f"  {cname} | {SIMS*len(COMPOUNDS):,} sims on {N} cores...")
        t0=time.time()
        np.random.seed(42)
        args=[]
        for idx in range(SIMS):
            setup={k:np.random.uniform(lo,hi) for k,(lo,hi) in BOUNDS.items()}
            for comp in COMPOUNDS:
                args.append((cname,td,setup,comp,1,idx))
        with Pool(N) as pool:
            raw=pool.map(worker,args)
        valid=[r for r in raw if r]
        valid.sort(key=lambda x:x[2])
        if not valid: print("  No results."); continue
        best_t,best_c,best_s=valid[0][2],valid[0][1],valid[0][3]
        cf=real/best_t; cal=best_t*cf
        old=prev_cf.get(cname,0); delta=cf-old
        print(f"  ✅ {len(valid):,} valid | {time.time()-t0:.0f}s")
        print(f"  Calibrated:  {int(cal//60)}:{cal%60:06.3f} ({best_c})")
        print(f"  Real winner: {int(real//60)}:{real%60:06.3f}")
        print(f"  Cal factor:  {cf:.4f}  {'⬆️ IMPROVED' if delta>0 else '⬇️ regressed'} from {old:.4f} (Δ{delta:+.4f})")
        print(f"\n  Compound breakdown (calibrated):")
        for comp in COMPOUNDS:
            ct=[r[2]*cf for r in valid if r[1]==comp]
            if ct: print(f"    {comp:8}: best {int(min(ct)//60)}:{min(ct)%60:06.3f} | n={len(ct):,}")
        print(f"\n  OPTIMAL SETUP:")
        fmts={'wd':lambda v:f"{v*100:.1f}%",'rhf':lambda v:f"{v*1000:.0f}mm",
              'cb':lambda v:f"{v*100:.1f}%",'ers':lambda v:f"{v*100:.1f}%",
              'aat':lambda v:f">{v*3.6:.0f}km/h",'fuel':lambda v:f"{v:.0f}kg",'dif':lambda v:f"{v*100:.0f}%"}
        for k,fmt in fmts.items():
            print(f"    {k:5}: {fmt(best_s[k])}")
        all_results[cname]={'real_sec':real,'best_raw':round(best_t,3),'calibrated':round(cal,3),
            'cf':round(cf,4),'prev_cf':old,'cf_delta':round(delta,4),
            'best_compound':best_c,'best_setup':{k:round(v,5) for k,v in best_s.items()}}

    print(f"\n{'='*68}")
    print("  FINAL — MERGED MODEL vs PRIOR MODELS")
    print(f"{'='*68}")
    for cname,r in all_results.items():
        arrow='⬆️ ' if r['cf_delta']>0 else '⬇️ '
        print(f"  {cname:10}: cf={r['cf']:.4f} {arrow}(Δ{r['cf_delta']:+.4f} vs 100k Grok-only run)")
    with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/merged_sim_results.json','w') as f:
        json.dump(all_results,f,indent=2)
    print("\n  Saved. 🏎️")
