"""
NOVA PHYSICS MODEL — F1 2026 Lap Time Simulator
Key additions vs baseline:
- Pacejka-inspired lateral tire force (real slip angle physics)
- Dynamic tire temp per corner (heats/cools each segment)
- Braking G-limit at 4.5G threshold braking + trail braking
- Fuel burn per lap (1.85 kg/lap weight drop)
- Sector ERS deployment map (exits only, harvest on braking)
- Drag properly as 0.5 * rho * Cd * A * v^2
"""
import numpy as np

# ============================================================
# NOVA: Pacejka "Magic Formula" tire model (simplified)
# Fy = D * sin(C * arctan(B*alpha - E*(B*alpha - arctan(B*alpha))))
# where alpha = slip angle
# ============================================================
def pacejka_grip(slip_angle_deg, Fz_N, compound='MEDIUM', tire_temp_C=95):
    """
    Returns lateral force (N) for given slip angle and load.
    Coefficients tuned for F1 compounds.
    """
    PARAMS = {
        'SOFT':   {'B':12.0, 'C':1.65, 'D':1.62, 'E':-0.5},
        'MEDIUM': {'B':11.5, 'C':1.60, 'D':1.58, 'E':-0.4},
        'HARD':   {'B':11.0, 'C':1.55, 'D':1.52, 'E':-0.3},
        'NOVA32': {'B':11.8, 'C':1.62, 'D':1.60, 'E':-0.45},
    }
    p = PARAMS.get(compound, PARAMS['MEDIUM'])
    
    # Temperature effect on peak grip (D parameter)
    # Gaussian from our MD model — peak at compound Tg
    TG = {'SOFT':105,'MEDIUM':95,'HARD':82,'NOVA32':88}
    tg = TG.get(compound, 95)
    d_temp = p['D'] * np.exp(-0.5*((tire_temp_C - tg)/18.0)**2)
    
    a = np.radians(slip_angle_deg)
    Fy = Fz_N * d_temp * np.sin(
        p['C'] * np.arctan(p['B']*a - p['E']*(p['B']*a - np.arctan(p['B']*a)))
    )
    return abs(float(Fy))

# ============================================================
# NOVA: Dynamic tire temperature model
# Temp rises in corners, falls on straights
# ============================================================
def update_tire_temp(temp_C, lateral_g, speed_ms, segment_type='corner', dt=1.0):
    """Tire temperature evolves dynamically each segment."""
    if segment_type == 'corner':
        heating_rate = lateral_g**2 * 8.0 + speed_ms * 0.15  # friction heating
        return min(temp_C + heating_rate * dt, 145)  # max temp 145C
    else:  # straight
        cooling_rate = speed_ms * 0.08   # convective cooling
        ambient = 85.0  # baseline running temp
        return max(temp_C - cooling_rate * dt, ambient)

# ============================================================
# NOVA: Braking model with G-limit and trail braking
# ============================================================
def calc_braking_time(v_entry, v_apex, normal_force_N, brake_bias, mass_kg):
    """
    Threshold braking at max 4.5G, trailing off near apex.
    Returns braking time and distance.
    """
    g = 9.81
    max_brake_g = 4.5  # F1 threshold braking
    mu_brake = brake_bias * 1.8  # brake force coefficient
    
    decel_g = min(max_brake_g, mu_brake * normal_force_N / (mass_kg * g))
    decel = decel_g * g
    
    # Trail braking: last 30% of braking zone is reduced
    v_trail_start = v_apex + (v_entry - v_apex) * 0.3
    
    # Phase 1: full braking
    if v_entry > v_trail_start:
        t1 = (v_entry - v_trail_start) / decel
        d1 = (v_entry**2 - v_trail_start**2) / (2 * decel)
    else:
        t1, d1 = 0, 0
    
    # Phase 2: trail braking (50% braking + cornering)
    trail_decel = decel * 0.5
    t2 = (v_trail_start - v_apex) / max(trail_decel, 0.1)
    d2 = (v_trail_start**2 - v_apex**2) / max(2 * trail_decel, 0.1)
    
    return t1 + t2, d1 + d2

# ============================================================
# NOVA: Full lap simulation
# ============================================================
def nova_sim_lap(circuit, setup, compound='MEDIUM', lap_num=1):
    """
    Full Nova physics lap simulation.
    Returns lap time in seconds.
    """
    # Constants
    g = 9.81
    rho = 1.225
    frontal_area = 1.35
    
    # Car state
    fuel_kg = max(setup['fuel'] - (lap_num-1) * 1.85, 1.0)
    mass = 770 + fuel_kg
    
    # Aero (v2 drag)
    cl = 2.8 if True else 1.4  # corner mode default
    cd_corner = 0.95
    cd_straight = 0.57  # 40% less drag open wing (2026)
    
    # Start tire temp
    tire_temp = circuit['track_temp'] + 65
    
    total_time = 0.0
    
    for i, corner in enumerate(circuit['corners']):
        v_entry = corner['es']
        v_apex_target = corner['as']
        v_exit = corner['xs']
        radius = corner['r']
        corner_len = corner['l']
        straight_len = corner.get('st', 100)
        
        # ---- ACTIVE AERO ----
        on_straight = v_entry > setup['aat']
        cl_use = 1.4 if on_straight else cl
        cd_use = cd_straight if on_straight else cd_corner
        
        # ---- DOWNFORCE at apex speed ----
        df_N = 0.5 * rho * cl_use * frontal_area * v_apex_target**2
        wt_N = mass * g
        nf_N = wt_N + df_N  # total normal force
        
        # ---- PACEJKA TIRE GRIP ----
        # Optimal slip angle for F1 ~8-12 degrees
        optimal_slip = 10.0
        Fy = pacejka_grip(optimal_slip, nf_N / 4, compound, tire_temp)
        mu_lat = (Fy * 4) / nf_N  # effective lateral friction coeff
        
        # Max corner speed from centripetal limit
        v_max = np.sqrt(mu_lat * g * radius)
        v_apex_actual = min(v_apex_target * mu_lat, v_max)
        
        # ---- DYNAMIC TIRE TEMP (corner) ----
        lat_g = v_apex_actual**2 / (radius * g)
        tire_temp = update_tire_temp(tire_temp, lat_g, v_apex_actual, 'corner', corner_len/v_apex_actual if v_apex_actual > 0 else 1)
        
        # ---- BRAKING ----
        t_brake, d_brake = calc_braking_time(v_entry, v_apex_actual, nf_N, setup['cb'], mass)
        
        # ---- CORNER TIME ----
        t_corner = corner_len / max(v_apex_actual, 1.0)
        
        # ---- TIRE TEMP (straight - cooling) ----
        tire_temp = update_tire_temp(tire_temp, 0, v_entry, 'straight', straight_len/max(v_entry,1))
        
        # ---- ACCELERATION (ERS-boosted) ----
        # ERS deployed on corner exits
        ers_fraction = setup['ers'] * 1.3  # heavier deployment on exits
        ers_fraction = min(ers_fraction, 1.0)
        power_kw = 470 + 350 * ers_fraction
        
        drag_N = 0.5 * rho * cd_straight * frontal_area * v_apex_actual**2
        traction_N = min(power_kw*1000/max(v_apex_actual,1), nf_N * setup['dif'] * 1.5)
        net_force = traction_N - drag_N
        accel = net_force / mass
        
        if accel > 0 and straight_len > 0:
            t_straight = np.sqrt(2 * straight_len / max(accel, 0.01))
        else:
            t_straight = straight_len / max(v_exit, 1.0)
        
        total_time += t_brake + t_corner + t_straight
    
    return total_time

print("Nova physics model loaded.")
