"""
FULL 2026 CALENDAR SIMULATION
24 circuits | Nova + Grok physics | Numba JIT
OpenCure F1 Lab — Nova + Grok + Stephen

FastF1 circuit name map for 2024 data (proxy for 2026 layout)
Track temps estimated from historical race data.
"""
import fastf1
import numpy as np
import json, time
from multiprocessing import Pool, cpu_count
from numba import jit
import warnings
warnings.filterwarnings('ignore')
fastf1.Cache.enable_cache('/tmp/fastf1_cache')
fastf1.set_log_level('WARNING')

MIN_WEIGHT=770.0; MAX_FUEL=105.0; FUEL_BURN=1.85
ERS_DEPLOY=4.0; ERS_REGEN=8.5; ERS_KW=350.0; ICE_KW=470.0
RHO=1.225; AREA=1.2; G=9.81

@jit(nopython=True)
def _inner(dist,speed,throttle,brake,rh,bb,ef,at,fuel,tt,Tg,D,wkm,cliff,dkm,n,lkm):
    mass=MIN_WEIGHT+fuel; tire_temp=tt+65.0; energy=ERS_DEPLOY; total=0.0
    for i in range(1,n):
        ds=dist[i]-dist[i-1]
        if ds<=0.0: continue
        v=max(speed[i],1.0); thr=throttle[i]; brk=brake[i]; dt=ds/v
        rh_mm=rh*1000.0; aopen=v>at
        bcl=max(1.8*0.7+0.002*v-0.015*abs(rh_mm-31.0),0.4)
        cl=bcl*0.55 if aopen else bcl; cd=0.45 if aopen else 0.90
        q=0.5*RHO*v*v; df=cl*AREA*q; drag=cd*AREA*q
        rh2=max(rh-df/55000.0,0.010); rh2mm=rh2*1000.0
        cl2=max(1.8*0.7+0.002*v-0.015*abs(rh2mm-31.0),0.4)
        cl2=cl2*0.55 if aopen else cl2; cd2=0.45 if aopen else 0.90
        df=cl2*AREA*q; drag=cd2*AREA*q; nf=mass*G+df
        d2=tire_temp-Tg; sig=18.0*(0.7 if d2<0.0 else 1.3)
        thermal=2.71828**(-0.5*(d2/sig)*(d2/sig))
        wf=dkm/wkm
        wear=(1-(1-cliff)*min(wf,0.85)/0.85) if wf<0.85 else max(cliff-(wf-0.85)*3.0*(1-cliff),0.65)
        mu=D*thermal*wear
        lat_g=abs(speed[i]-speed[i-1])/(G*dt+0.001)
        if brk>0.2 or lat_g>0.5:
            dT=(lat_g*lat_g*8.5+v*0.12)*dt; tire_temp=min(tire_temp+dT,148.0)
        else:
            tire_temp=max(tire_temp-v*0.07*dt,82.0)
        if brk>0.3:
            h=min(200.0,(ERS_REGEN-energy)*1000.0); energy=min(energy+h*0.001,ERS_REGEN); boost=0.0
        elif thr>0.75 and energy>0.0:
            boost=ERS_KW*ef; energy=max(energy-boost*0.001,0.0)
        else: boost=0.0
        power=(ICE_KW+boost)*1000.0; drive=power/v; grip=mu*nf
        traction=min(drive,grip*0.85)
        if brk>0.1:
            dec=min(4.5*bb*G,mu*G*1.15)
            if brk<0.4: dec*=0.55
            net=-dec
        else: net=(traction-drag)/mass
        v2=max(v+net*dt*0.1,1.0); total+=ds/v2
    return total

TIRE_DATA={'SOFT':(105.0,1.62,35.0,0.88),'MEDIUM':(95.0,1.58,60.0,0.90),
           'HARD':(82.0,1.52,90.0,0.93),'NOVA32':(88.0,1.60,75.0,0.92)}

def sim_lap(arrays,setup,compound,lap_num=1,track_temp=28.0,jitter=True):
    dist,spd,thr,brk=arrays
    lkm=(dist[-1]-dist[0])/1000.0 if len(dist)>1 else 5.0
    if jitter:
        spd=spd*np.random.uniform(0.993,1.007,len(spd))
    fuel=max(MAX_FUEL-(lap_num-1)*FUEL_BURN,1.0)
    dkm=(lap_num-1)*lkm
    Tg,D,wkm,cliff=TIRE_DATA[compound]
    return _inner(dist,spd,thr,brk,setup['rhf'],setup['cb'],setup['ers'],
                  setup['aat'],fuel,track_temp,Tg,D,wkm,cliff,dkm,len(dist),lkm)

def worker(args):
    arrays,setup,compound,tt,seed=args
    np.random.seed(seed)
    try:
        t=sim_lap(arrays,setup,compound,1,tt,True)
        return (compound,t,setup)
    except: return None

BOUNDS={'wd':(0.440,0.480),'rhf':(0.025,0.050),'rhr':(0.060,0.110),
        'cb':(0.540,0.620),'ers':(0.300,1.000),'aat':(13.9,29.2),
        'fuel':(80.0,105.0),'dif':(0.500,1.000)}
COMPOUNDS=['SOFT','MEDIUM','HARD','NOVA32']

# Full 2026 FIA calendar — FastF1 name + estimated track temp
CALENDAR_2026 = [
    ('Bahrain',    2024, 23.7, 57),
    ('Saudi Arabia', 2024, 28.0, 50),
    ('Australian', 2024, 22.5, 58),
    ('Japanese',   2024, 18.0, 53),
    ('Chinese',    2024, 20.0, 56),
    ('Miami',      2024, 40.0, 57),
    ('Emilia Romagna', 2024, 24.0, 63),
    ('Monaco',     2024, 46.3, 78),
    ('Canadian',   2024, 26.0, 70),
    ('Spanish',    2024, 42.0, 66),
    ('Austrian',   2024, 30.0, 71),
    ('British',    2024, 27.7, 52),
    ('Hungarian',  2024, 48.0, 70),
    ('Belgian',    2024, 20.0, 44),
    ('Dutch',      2024, 22.0, 72),
    ('Italian',    2024, 35.0, 53),
    ('Azerbaijan', 2024, 32.0, 51),
    ('Singapore',  2024, 48.0, 62),
    ('United States', 2024, 36.0, 56),
    ('Mexico City',2024, 20.0, 71),
    ('São Paulo',  2024, 38.0, 71),
    ('Las Vegas',  2024, 12.0, 50),
    ('Qatar',      2024, 38.0, 57),
    ('Abu Dhabi',  2024, 32.0, 58),
]

if __name__=='__main__':
    SIMS=5000  # per circuit × 4 compounds = 20k each, 480k total
    N=max(1,cpu_count()-1)
    print("="*68)
    print("  FULL 2026 CALENDAR SIMULATION — 24 CIRCUITS")
    print(f"  {SIMS*4*24:,} total sims | Numba JIT | {N} cores")
    print("="*68)

    # Warm up numba
    print("\n⚡ Warming up Numba...")
    try:
        s=fastf1.get_session(2024,'Bahrain','R')
        s.load(telemetry=True,laps=True,weather=False,messages=False)
        lap=s.laps.pick_fastest(); tel=lap.get_telemetry()
        dist=tel['Distance'].values.astype(np.float64)
        spd=tel['Speed'].values.astype(np.float64)/3.6
        try: thr=tel['Throttle'].values.astype(np.float64)/100
        except: thr=np.where(spd>spd.mean(),0.9,0.1).astype(np.float64)
        try:
            brk=tel['Brake'].values.astype(np.float64)
            if brk.max()>1: brk/=100
        except: brk=np.where(spd<spd.mean()*0.8,0.8,0.0).astype(np.float64)
        warm_arr=(dist,spd,thr,brk)
        dummy={'rhf':0.033,'cb':0.58,'ers':0.65,'aat':20.0,'fuel':100,'wd':0.46,'rhr':0.075,'dif':0.75}
        _=sim_lap(warm_arr,dummy,'MEDIUM',1,28,False)
        print("  ✅ Numba ready")
    except Exception as e:
        print(f"  ⚠️  Warm-up issue: {e}")
        warm_arr=None

    all_results={}
    total_start=time.time()
    failed=[]

    for circuit_name, year, est_temp, race_laps in CALENDAR_2026:
        print(f"\n[{circuit_name}] Loading...", end='', flush=True)
        try:
            s=fastf1.get_session(year,circuit_name,'R')
            s.load(telemetry=True,laps=True,weather=True,messages=False)
            lap=s.laps.pick_fastest()
            tel=lap.get_telemetry()
            try: tt=float(s.weather_data['TrackTemp'].dropna().mean())
            except: tt=est_temp
            real_sec=lap['LapTime'].total_seconds()
            dist=tel['Distance'].values.astype(np.float64)
            spd=tel['Speed'].values.astype(np.float64)/3.6
            try: thr=tel['Throttle'].values.astype(np.float64)/100
            except: thr=np.where(spd>spd.mean(),0.9,0.1).astype(np.float64)
            try:
                brk=tel['Brake'].values.astype(np.float64)
                if brk.max()>1: brk/=100
            except: brk=np.where(spd<spd.mean()*0.8,0.8,0.0).astype(np.float64)
            arrays=(dist,spd,thr,brk)
        except Exception as e:
            print(f" ❌ {e}")
            failed.append(circuit_name)
            continue

        print(f" ✅ {int(real_sec//60)}:{real_sec%60:06.3f} | {tt:.1f}°C | {len(dist)} pts")
        t0=time.time()
        np.random.seed(42)
        args=[]
        for idx in range(SIMS):
            setup={k:np.random.uniform(lo,hi) for k,(lo,hi) in BOUNDS.items()}
            for comp in COMPOUNDS:
                args.append((arrays,setup,comp,tt,idx))
        with Pool(N) as pool:
            raw=pool.map(worker,args)
        valid=[r for r in raw if r]
        valid.sort(key=lambda x:x[1])
        if not valid: failed.append(circuit_name); continue
        best_c,best_t,best_s=valid[0]
        cf=real_sec/best_t; cal=best_t*cf
        elapsed=time.time()-t0

        # Top compound per circuit
        comp_best={}
        for comp in COMPOUNDS:
            ct=[r[1]*cf for r in valid if r[0]==comp]
            if ct: comp_best[comp]=round(min(ct),3)

        all_results[circuit_name]={
            'real_sec':real_sec,'calibrated':round(cal,3),'cf':round(cf,6),
            'best_compound':best_c,'track_temp':round(tt,1),'race_laps':race_laps,
            'compound_best':comp_best,
            'best_setup':{k:round(v,5) for k,v in best_s.items()},
            'elapsed':round(elapsed,1)
        }
        print(f"  → {int(cal//60)}:{cal%60:06.3f} ({best_c}) | cf={cf:.4f} | {elapsed:.0f}s")

        # Save incrementally
        with open('/Users/stephensalone/.openclaw/workspace-science-bot/f1/calendar_2026_results.json','w') as f:
            json.dump(all_results,f,indent=2)

    total_elapsed=time.time()-total_start
    print(f"\n\n{'='*68}")
    print(f"  2026 FULL CALENDAR COMPLETE")
    print(f"  {len(all_results)}/24 circuits | {total_elapsed/60:.1f} min")
    print(f"  Failed: {failed if failed else 'none'}")
    print(f"{'='*68}\n")

    # Summary table
    print(f"  {'Circuit':20} {'Temp':5} {'Real':8} {'Our Best':8} {'Compound':8} {'CF':8}")
    print(f"  {'-'*65}")
    for cname,r in all_results.items():
        real=r['real_sec']; cal=r['calibrated']
        print(f"  {cname:20} {r['track_temp']:4.0f}C  {int(real//60)}:{real%60:06.3f}  {int(cal//60)}:{cal%60:06.3f}  {r['best_compound']:8} {r['cf']:.4f}")

    # NOVA32 circuits (cool track temps where our compound wins)
    nova32_circuits=[c for c,r in all_results.items() if r['best_compound']=='NOVA32']
    print(f"\n  NOVA32 wins at: {nova32_circuits if nova32_circuits else 'none (at this temp)'}")
    print(f"\n  Saved to f1/calendar_2026_results.json 🏎️")
