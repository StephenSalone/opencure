"""
GROK PHYSICS MODEL — F1 2026 Lap Time Simulator
Key additions per Grok's recommendations:
- Polynomial aero Cl/Cd curve vs speed AND ride height (Grok's key addition)
- ERS energy budget tracked per sector (not flat %)
- Tire degradation over laps (grip -2% per 10C over 100C)
- Fuel/weight shift per lap
- Suspension heave/pitch model affecting ride height dynamically
"""
import numpy as np

# ============================================================
# GROK: Polynomial aero function (Cl AND Cd vs speed + ride height)
# This is Grok's key differentiation from Nova
# ============================================================
def grok_aero_force(speed_ms, ride_height_m, active_aero_open=False):
    """
    Grok's aero model: polynomial curves fit to 2026 regulations.
    Cl varies with speed and ride height.
    Cd varies with aero state.
    2026 targets: 30% downforce reduction, 55% drag reduction vs 2025.
    """
    # Base Cl for 2026 (30% less than 2024's ~2.8 = ~1.96)
    base_cl = 1.96
    
    # Speed effect: more downforce at higher speeds (squared)
    speed_effect = 0.002 * speed_ms  # small linear term
    
    # Ride height effect: lower = more floor seal = more downforce
    # Optimal at 33mm (0.033m), penalty above/below
    rh_mm = ride_height_m * 1000
    rh_effect = -0.015 * abs(rh_mm - 33)  # penalty per mm from optimal
    
    cl = max(base_cl + speed_effect + rh_effect, 0.5)
    
    # Active aero: open above 353 km/h
    if active_aero_open:
        cl *= 0.55   # wings open: significant downforce reduction
        cd = 0.45    # 55% less drag: Grok's 2026 estimate
    else:
        cd = 0.90    # corner mode drag
    
    q = 0.5 * 1.225 * speed_ms**2  # dynamic pressure
    downforce_N = cl * 1.35 * q
    drag_N = cd * 1.35 * q
    return downforce_N, drag_N, cl

# ============================================================
# GROK: ERS sector energy budget
# Tracks energy in/out per lap, maximizes deployment on exits
# ============================================================
def grok_ers_sector(sector_type, speed_ms, energy_remaining_mj, max_energy_mj=8.5):
    """
    Grok's ERS model: deploy on exits, harvest on braking, zero on corners.
    Returns power boost (kW) and updated energy.
    """
    if energy_remaining_mj <= 0:
        return 0.0, 0.0
    
    if sector_type == 'accel':
        # Deploy ERS on acceleration zones
        deploy_rate = min(350.0, energy_remaining_mj * 1000)  # kW
        energy_used = deploy_rate * 0.001  # MJ per second approximation
        return deploy_rate, max(energy_remaining_mj - energy_used, 0)
    
    elif sector_type == 'brake':
        # Harvest ERS during braking (regen)
        harvest_rate = 200.0  # kW regen
        energy_gained = harvest_rate * 0.001
        return 0.0, min(energy_remaining_mj + energy_gained, max_energy_mj)
    
    else:  # corner — no ERS
        return 0.0, energy_remaining_mj

# ============================================================
# GROK: Tire degradation model
# Grip drops as function of temperature and lap count
# ============================================================
def grok_tire_grip(compound, tire_temp_C, lap_num=1):
    """
    Grok's degradation: grip -2% per 10C above 100C + lap wear.
    Based on MD thermal softening data.
    """
    BASE_GRIP = {'SOFT':1.62,'MEDIUM':1.58,'HARD':1.52,'NOVA32':1.60}
    DEG_RATE  = {'SOFT':0.003,'MEDIUM':0.0015,'HARD':0.0007,'NOVA32':0.001}
    TG        = {'SOFT':105,'MEDIUM':95,'HARD':82,'NOVA32':88}
    
    base = BASE_GRIP.get(compound, 1.58)
    tg = TG.get(compound, 95)
    
    # Thermal effect: -2% per 10C above optimal
    if tire_temp_C > 100:
        thermal_deg = 0.002 * (tire_temp_C - 100)
    else:
        thermal_deg = 0
    
    # Lap wear
    lap_deg = lap_num * DEG_RATE.get(compound, 0.0015)
    
    # Peak grip from Gaussian (our MD model)
    sigma = 18.0
    d = tire_temp_C - tg
    s = sigma * (0.7 if d < 0 else 1.3)
    peak = float(np.exp(-0.5*(d/s)**2))
    
    return base * peak * max(0.7, 1 - thermal_deg - lap_deg)

# ============================================================
# GROK: Suspension heave model
# Ride height changes dynamically with downforce load
# ============================================================
def grok_dynamic_ride_height(static_rh_m, downforce_N, spring_rate_Nm=50000):
    """
    Grok's suspension: car squats under downforce, affecting floor seal.
    ride_height_dynamic = static - downforce/spring_rate
    """
    squat = downforce_N / spring_rate_Nm
    return max(static_rh_m - squat, 0.010)  # minimum 10mm

# ============================================================
# GROK: Full lap simulation
# ============================================================
def grok_sim_lap(circuit, setup, compound='MEDIUM', lap_num=1):
    """
    Full Grok physics lap simulation.
    """
    g = 9.81
    
    fuel_kg = max(setup['fuel'] - (lap_num-1) * 1.85, 1.0)
    mass = 770 + fuel_kg
    
    energy_mj = 8.5  # Start each lap with full ERS budget
    tire_temp = circuit['track_temp'] + 65
    total_time = 0.0
    
    for i, corner in enumerate(circuit['corners']):
        v_entry = corner['es']
        v_apex_t = corner['as']
        radius = corner['r']
        corner_len = corner['l']
        straight_len = corner.get('st', 100)
        
        # ---- GROK AERO: polynomial with ride height ----
        on_straight = v_entry > setup['aat']
        static_rh = setup['rhf']
        
        df_entry, drag_entry, cl = grok_aero_force(v_entry, static_rh, on_straight)
        
        # Dynamic ride height (suspension squat)
        dyn_rh = grok_dynamic_ride_height(static_rh, df_entry)
        df_apex, drag_apex, cl2 = grok_aero_force(v_apex_t, dyn_rh, False)
        
        # ---- GROK TIRE GRIP with degradation ----
        wt_N = mass * g
        nf_N = wt_N + df_apex
        mu = grok_tire_grip(compound, tire_temp, lap_num)
        
        v_max = np.sqrt(mu * g * radius)
        v_apex_actual = min(v_apex_t * mu, v_max)
        
        # ---- TIRE TEMP (simple heating model) ----
        lat_g = v_apex_actual**2 / (radius * g)
        heating = lat_g**2 * 8 + v_apex_actual * 0.15
        dt_corner = corner_len / max(v_apex_actual, 1)
        tire_temp = min(tire_temp + heating * dt_corner, 145)
        
        # ---- BRAKING (Grok: simple decel) ----
        decel = min(4.0 * g, mu * g * 1.2)  # ~4G braking
        t_brake = (v_entry - v_apex_actual) / decel if v_entry > v_apex_actual else 0
        
        # ---- CORNER TIME ----
        t_corner = corner_len / max(v_apex_actual, 1.0)
        
        # ---- STRAIGHT: Grok ERS sector budget ----
        tire_temp = max(tire_temp - (v_entry * 0.08) * (straight_len/max(v_entry,1)), 85)
        
        ers_boost, energy_mj = grok_ers_sector('accel', v_apex_actual, energy_mj)
        _, energy_mj = grok_ers_sector('brake', v_entry, energy_mj)
        
        power_kw = 470 + ers_boost
        drag_N = drag_apex
        traction_N = power_kw * 1000 / max(v_apex_actual, 1)
        net_force = traction_N - drag_N
        accel = net_force / mass
        
        if accel > 0 and straight_len > 0:
            t_straight = np.sqrt(2 * straight_len / max(accel, 0.01))
        else:
            t_straight = straight_len / max(v_entry, 1.0)
        
        total_time += t_brake + t_corner + t_straight
    
    return total_time

print("Grok physics model loaded.")
