from Emission_Func import calculate_fuel_and_emissions
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('/home/akkumar03/Air_Transport_Research/openap/Simulated Southwest Data.csv')

# Initialize total values
total_mass_used = 0
total_CO2_released = 0

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    ac = row['ac']  # Assuming there is a column 'ac' for aircraft type
    duration_minutes = int(row['duration_minutes'])  # Convert to integer
    alt_to = int(row['alt_to_ft'])  # Convert to integer
    alt_ld = int(row['alt_ld_ft'])  # Convert to integer
    mass_to = int(row['mass_to_kg'])  # Convert to integer

    # Calculate fuel and emissions for the current row
    mass_used, CO2_released = calculate_fuel_and_emissions(ac=ac, duration_minutes=duration_minutes, alt_to=alt_to, alt_ld=alt_ld, mass_to=mass_to)

    # Add to total values
    total_mass_used += mass_used
    total_CO2_released += CO2_released

    print(f'Fuel Used: {mass_used:.2f} kg')
    print(f'CO2 released: {CO2_released:.2f} kg')

    # Print the total results
print(f'Total fuel used: {total_mass_used:.2f} kg')
print(f'Total CO2 released: {total_CO2_released:.2f} kg')
