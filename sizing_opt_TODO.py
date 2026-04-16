from pyomo.core.base import Var, Constraint, Objective, NonNegativeReals, Reals, Binary, Integers, maximize
import pyomo.environ as pyo
from pyomo.core.kernel import value
from pyomo.opt import SolverStatus, TerminationCondition
from pyomo.core.base import ConcreteModel, RangeSet, Set
import utils
ANNUAL_CONSUMPTION = 4e6                                                        # TODO: add your yearly electricity consumption [Wh]
YEARLY_KM = 5e3                                                                 # TODO: add your car usage [kM]
                                                                                # Energy efficiency of 20kWh/100 km is considered
                                                                                # Should not be more than 40k km a year
# WARNING: when running this you should have SIZING variable in parameters.py set to True 
from parameters import *

import Plot

# Load data
data = utils.SizingData(START_DATE, yearly_cons=ANNUAL_CONSUMPTION)

if USE_EV:
    # create t_init array, t_target and soc_init
    EV_initial_SOC, t_arr, t_dep = utils.extract_EV_data(data, yearly_km=YEARLY_KM) 
    n_EV_con = len(t_arr)                                                       # Number of EV_connections
    
    # EV_initial_SOC: list of states of charge when the EV arrives [Wh] indices go from 0 to n_EV_con-1
    # t_arr: list of time indices for EV arrival. Numbers in this list can go from 1 to N_PERIODS, indices of this list go from 0 to n_EV_con-1
    #       you should ensure that at the begining of each timestep in this list, the EV_soc variable is equal to the corresponding EV_initial_SOC
    # t_dep: list of time indices for EV departure. Numbers in this list can go from 1 to N_PERIODS, indices of this list go from 0 to n_EV_con-1
    #       you should ensure that at the end of each timestep in this list, the EV_soc variable is equal to EV_TARGET_SOC

# Create the pyomo model
model = ConcreteModel()

# Create sets
# Time periods of length RESOLUTION_IN_MINUTES
model.periods = RangeSet(N_PERIODS)
if USE_EV: model.connections = Set(initialize=range(n_EV_con))
model.grid_capacity_options = Set(initialize=GRID_CAPACITY_PRICE.keys())        # Indices for grid connection capacities
model.genset_capacity_options = Set(initialize=GENSET_CAPACITY_PRICE.keys())    # Indices for genset investment capacities

# Create variables

# Operation variables
model.soc = Var(model.periods, within=NonNegativeReals)                         # Storage state of charge [Wh]
model.charge_storage_sp = Var(model.periods, within=NonNegativeReals)           # Storage charge setpoint [W]
model.discharge_storage_sp = Var(model.periods, within=NonNegativeReals)        # Storage discharge setpoint [W]

model.EV_soc = Var(model.periods, within=NonNegativeReals)                      # EV state of charge [Wh]
model.charge_EV_sp = Var(model.periods, within=NonNegativeReals)                # EV charge setpoint [W]
model.discharge_EV_sp = Var(model.periods, within=NonNegativeReals)             # EV discharge setpoint [W]

model.gen_PV_sp = Var(model.periods, within=NonNegativeReals)                   # PV generation [W]
model.imp_grid = Var(model.periods, within=NonNegativeReals)                    # Power import from the grid connection [W]
model.exp_grid = Var(model.periods, within=NonNegativeReals)                    # Power export to the grid connection [W]
model.steer_genset_sp = Var(model.periods, within=NonNegativeReals)             # genset setpoint [W]



# Sizing variables
model.storage_energy_capacity_units = Var(within=Integers)
model.storage_inverter_capacity_units = Var(within=Integers)
model.PV_capacity = Var(within=NonNegativeReals)
model.PV_inverter_capacity_units = Var(within=Integers)
model.grid_capacity = Var(model.grid_capacity_options, within=Binary)
model.genset_capacity = Var(model.genset_capacity_options, within=Binary)

# Create constraints:                                   
#           use data.consumption(p) to get consumption for timestep p
#               data.PV_generation(p) to get Pmax [pu] for timestep p
#               data.EV_connected(p) to get connection status of the EV (0 or 1)
#           p should go from 1 to N_PERIODS

def power_balance_rule(m, p):
    prod_expression = 0
    cons_expression = 0
    return prod_expression >= cons_expression                                   # You should ensure that this constraint is close to tight


def storage_level_rule(m, p):
    return 0==0 # TODO

def storage_capacity_rule(m, p):
    return 0==0 # TODO

def storage_charge_power_rule1(m, p):
    return 0==0 # TODO

def storage_discharge_power_rule1(m, p):
    return  0==0 # TODO

def storage_charge_power_rule2(m, p):
    return  0==0 # TODO

def storage_discharge_power_rule2(m, p):
    return  0==0 # TODO


def EV_level_rule(m, p):
    return  0==0 # TODO

def EV_target_rule(m,c):
    return 0==0 # TODO

def EV_max_capacity_rule(m, p):
    return 0==0 # TODO

def EV_min_capacity_rule(m, p):
    return 0==0 # TODO

def EV_charge_power_rule(m, p):
    return 0==0 # TODO

def EV_discharge_power_rule(m, p):
    return 0==0 # TODO

def EV_charge_power_rule2(m, p):                                                # Used when no EV
    return m.charge_EV_sp[p] <= 0

def EV_discharge_power_rule2(m, p):                                             # Used when no EV
    return m.discharge_EV_sp[p] <= 0


def PV_generation_rule1(m, p):
    return 0==0 # TODO

def PV_generation_rule2(m, p):
    return 0==0 # TODO


def import_limit_rule(m, p):
    return 0==0 # TODO

def export_limit_rule(m, p):
    return 0==0 # TODO

def grid_connection_choice_rule(m):
    return 0==0 # TODO

def import_limit_rule2(m, p):                                                   # Used when no grid connection
    return m.imp_grid[p] <= 0

def export_limit_rule2(m, p):                                                   # Used when no grid connection
    return m.exp_grid[p] <= 0


def genset_generation_rule(m, p):
    return 0==0 # TODO


model.power_balance_cstr = Constraint(model.periods, rule=power_balance_rule)

model.storage_level_cstr = Constraint(model.periods, rule=storage_level_rule)
model.storage_capacity_cstr = Constraint(model.periods, rule=storage_capacity_rule)
model.storage_charge_power_cstr1 = Constraint(model.periods, rule=storage_charge_power_rule1)
model.storage_discharge_power_cstr1 = Constraint(model.periods, rule=storage_discharge_power_rule1)
model.storage_charge_power_cstr2 = Constraint(model.periods, rule=storage_charge_power_rule2)
model.storage_discharge_power_cstr2 = Constraint(model.periods, rule=storage_discharge_power_rule2)

if USE_EV:
    model.EV_level_cstr = Constraint(model.periods, rule=EV_level_rule)
    model.EV_min_capacity_cstr = Constraint(model.periods, rule=EV_min_capacity_rule)
    model.EV_max_capacity_cstr = Constraint(model.periods, rule=EV_max_capacity_rule)
    model.EV_charge_power_cstr = Constraint(model.periods, rule=EV_charge_power_rule)
    model.EV_discharge_power_cstr = Constraint(model.periods, rule=EV_discharge_power_rule)
    model.EV_target_cstr = Constraint(model.connections, rule=EV_target_rule)
else:
    model.EV_charge_power_cstr = Constraint(model.periods, rule=EV_charge_power_rule2)
    model.EV_discharge_power_cstr = Constraint(model.periods, rule=EV_discharge_power_rule2)
    
model.PV_generation_cstr1 = Constraint(model.periods, rule=PV_generation_rule1)
model.PV_generation_cstr2 = Constraint(model.periods, rule=PV_generation_rule2)

if GRID_CONNECTED:
    model.import_limit_cstr = Constraint(model.periods, rule=import_limit_rule)
    model.export_limit_cstr = Constraint(model.periods, rule=export_limit_rule)
    model.grid_connection_choice_cstr = Constraint(rule=grid_connection_choice_rule)
else:
    model.import_limit_cstr = Constraint(model.periods, rule=import_limit_rule2)
    model.export_limit_cstr = Constraint(model.periods, rule=export_limit_rule2)

model.genset_generation_cstr = Constraint(model.periods, rule=genset_generation_rule)

# Create objective
def total_cost(m):
    opex = 0 
    capex = 0
    return capex + opex # TODO: and do not forget to weight those two terms

model.obj = Objective(rule=total_cost, sense=pyo.minimize)

# Solve the model
opt = utils.configure_solver(model)
if EXPORT_MODEL:
    print("Exporting model...")
    utils.export_model(model)
print("Solving model...")
results = opt.solve(model, tee=True, keepfiles=False)                          
# Change tee to True if you want to see solving status printed

# Check is the problem is feasible
status = results.solver.status
termination_condition = results.solver.termination_condition
print("\nSolver status:", status, termination_condition)

if status == "ok": utils.plot_and_print(model, data, sizing=True, plot_soc=True) # You can change plot_soc to False to improve readability

# You should do additionnal data processing, do nicer plots, compute other indicators for your system results