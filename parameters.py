# This file contains parameters you may want to play with.

from datetime import datetime
# Parameters

# SOLVER_CONFIGURATION
EXPORT_MODEL = False


## General simulation parameters
# Connection to the grid
GRID_CONNECTED = False           # TODO: Change depending on the current case
USE_EV = True                    # TODO: Decide wether to model EV 
SIZING = False                   # TODO: Change to True for part 2 when using sizing.opt

if SIZING:
    N_DAYS = 31                                                                 # Number of days to simulate, from start_date [day] #TODO: Change to 365 to finalize
else:
    N_DAYS = 1                                                                  # Number of days to simulate, fixed to 1 to model the same scenario as HW3

# Time
START_DATE = datetime(2021, 1, 1, 0, 0, 0)                                      #TODO: You can change that to model other seasons, but there is only data for 2021
# Start date of the sizing run. No error handling if out of the data range.

RESOLUTION_IN_MINUTES = 15                                                      # Time step duration [min]
N_PERIODS = int(N_DAYS * 24 * 60 / RESOLUTION_IN_MINUTES)                       # Number of operation time steps
INVESTMENT_HORIZON = 20                                                         # [Years] Investment horizon

# Storage device sizing parameters
STORAGE_UNIT_CAPACITY = 1100  # [Wh]
STORAGE_UNIT_PRICE = 320  # [EUR]
STORAGE_MAX_P_RATE = 1800 # [W]
# Storage device operational parameters
INITIAL_SOC = 0  # [/] * Battery capacity  
CHARGE_EFFICIENCY = 0.95  # [/]
DISCHARGE_EFFICIENCY = 0.95  # [/]
#OTHER PRICE TO PENALIZE UNWANTED BEHAVIOR                                      # You can penalize some of the powers in your storage and EV to avoid big discharging peak.
                                                                                # This should not change much the final price in a visible way, it should only push your solution away from unrealistic.
                                                                                # Just smooth the soc curves and avoid unecessary discharging.

# Inverter capacity
INVERTER_UNIT_CAPACITY = 1000  # [VA]
INVERTER_UNIT_PRICE = 150  # [EUR]
PROSUMER_TARIF = 0.070 # [EUR/VA.year]

# PV
PV_CAPACITY_PRICE = 0.5                                                         # [EUR/Wp]
PV_MAX_CAPACITY = 0                                                             # TODO: Depending on your roofsize, you can relax afterwards and see effects

# Grid connection cost
# Key: [A], value: [EUR/year]
GRID_CAPACITY_PRICE = {16: 5, 32: 12.5, 64: 50}
GRID_VOLTAGE = 230  # [V]
GRID_IMPORT_PRICE = 0.4  # [EUR/kWh]
GRID_EXPORT_PRICE = 0.04  # [EUR/kWh]
# Genset
GENSET_CAPACITY_PRICE = {3100: 450, 5500: 750,
                         8000: 1880}  # Key: [VA], value: [EUR]


FUEL_PRICE_COEFF = 2/(10.74*0.4)  # [EUR/kWh] cost/(energy_density*efficiency)
#OTHER PRICE TO PENALIZE UNWANTED BEHAVIOR                                      # You should penalize some of the powers in your genset to have coherent genset behaviors.
                                                                                # This should not change the total final price in a visible way, it should only push your solution away from unrealistic.


# EV
EV_CAPACITY = 60e3          # [Wh]
EV_TARGET_SOC = 0.8*EV_CAPACITY         # [/]
EV_INVERTER_CAPACITY = 10e3 # [W]

## CO2
# Variable emission
FUEL_CO2 = 0.300 #g/Wh
# You can add a CO2 emission for grid import and test the model in non islanded mode

# Fixed emission
PV_CO2 = 1.8e3 # g/Wp
STORAGE_CO2 = 150 #g/Wh
GENSET_CO2 = {3100: 40e3, 5500: 60e3, 8000: 80e3} #g/device
INVERTER_CO2 = 60 #g/VA
