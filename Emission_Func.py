from openap import FuelFlow, Emission

def calculate_fuel_and_emissions(duration_minutes, alt_to, alt_ld, mass_to, ac, eng=None):
    # Initialize fuel flow and emission objects
    fuelflow = FuelFlow(ac=ac, eng=eng)
    emission = Emission(ac=ac, eng=eng)
    
    # Takeoff
    TAS_TO = 150  # kt
    ALT_TO = alt_to  # ft
    MASS_TO = mass_to  # kg
    DUR_TO = 40  # s
    
    FF_TO = fuelflow.takeoff(tas=TAS_TO, alt=ALT_TO)  # kg/s
    MASS_USED_TO = FF_TO * DUR_TO
    CO2_TO = (emission.co2(FF_TO) / 1000) * DUR_TO
    
    # Climb
    TAS_CL = (460 - 150) / 2  # kt
    ALT_CL = (36000 - ALT_TO) / 2  # ft
    MASS_CL = MASS_TO - MASS_USED_TO  # kg 
    DUR_CL = 20 * 60  # s
    VS_CL = (36000 - ALT_TO) / (DUR_CL / 60)  # ft/min
    ACC_CL = ((460 - 150) * 0.514444) / DUR_CL  # m/s^2
    
    FF_CL = fuelflow.enroute(mass=MASS_CL, tas=TAS_CL, alt=ALT_CL, vs=VS_CL, acc=ACC_CL)
    MASS_USED_CL = FF_CL * DUR_CL
    CO2_CL = (emission.co2(FF_CL) / 1000) * DUR_CL
    
    # Cruise
    TAS_CR = 460  # kt
    ALT_CR = 36000  # ft
    MASS_CR = MASS_CL - MASS_USED_CL  # kg
    DUR_CR = (duration_minutes * 60) - (DUR_TO + DUR_CL + (20 * 60))  # s
    
    FF_CR = fuelflow.enroute(mass=MASS_CR, tas=TAS_CR, alt=ALT_CR)
    MASS_USED_CR = FF_CR * DUR_CR
    CO2_CR = (emission.co2(FF_CR) / 1000) * DUR_CR
    
    # Descent
    TAS_DE = (460 - 120) / 2  # kt
    ALT_DE = (36000 - alt_ld) / 2  # ft
    MASS_DE = MASS_CR - MASS_USED_CR  # kg
    DUR_DE = 20 * 60  # s
    VS_DE = (alt_ld - 36000) / (DUR_DE / 60)  # ft/min
    ACC_DE = ((120 - 460) * 0.514444) / DUR_DE  # m/s^2
    
    FF_DE = fuelflow.enroute(mass=MASS_DE, tas=TAS_DE, alt=ALT_DE, vs=VS_DE, acc=ACC_DE)
    MASS_USED_DE = FF_DE * DUR_DE
    CO2_DE = (emission.co2(FF_DE) / 1000) * DUR_DE
    
    # Total fuel and emissions
    total_mass_used = MASS_USED_TO + MASS_USED_CL + MASS_USED_CR + MASS_USED_DE
    total_CO2_released = CO2_TO + CO2_CL + CO2_CR + CO2_DE
    
    return total_mass_used, total_CO2_released
