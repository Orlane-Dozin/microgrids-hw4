from pyomo.core.base import Var, Constraint, Objective, NonNegativeReals, Reals, Binary, Integers, maximize, Param
import pyomo.environ as pyo
from pyomo.core.kernel import value
from pyomo.opt import SolverStatus, TerminationCondition
from pyomo.core.base import ConcreteModel, RangeSet, Set
import utils
from utils import extract_EV_data
SCENARIO =  1                                                                   # TODO: Change from 1 to 4 to see results for each representative day

# WARNING: when running this you should have SIZING variable in parameters.py set to False 

from parameters import *
import Plot

# Load data
data = utils.SizingData(START_DATE, scen=SCENARIO)

if USE_EV:    # create t_init array, t_target and soc_init
    EV_initial_SOC, t_arr, t_dep = extract_EV_data(data) 
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
model.periods = RangeSet(N_PERIODS)                                             # Goes from 1 to N_PERIODS
if USE_EV: model.connections = Set(initialize=range(n_EV_con))                  # Goes from 0 to (number of connections-1)

# Create variables

# Operation variables
model.soc = Var(model.periods, within=NonNegativeReals)                         # Storage state of charge [Wh]
model.charge_storage_sp = Var(model.periods, within=NonNegativeReals)           # Storage charge setpoint [W]
model.discharge_storage_sp = Var(model.periods, within=NonNegativeReals)        # Storage discharge setpoint [W]

model.EV_soc = Var(model.periods, within=NonNegativeReals)                      # EV state of charge [Wh]
model.charge_EV_sp = Var(model.periods, within=NonNegativeReals)                # EV charge setpoint [W]
model.discharge_EV_sp = Var(model.periods, within=NonNegativeReals)             # EV discharge setpoint [W]

model.gen_PV_sp = Var(model.periods, within=NonNegativeReals)                   # PV generation [W]
model.imp_grid = Var(model.periods, within=NonNegativeReals)                    # [W]
model.exp_grid = Var(model.periods, within=NonNegativeReals)                    # [W]
model.steer_genset_sp = Var(model.periods, within=NonNegativeReals)             # genset setpoint [W]

# Sizing PARAMETERS
model.storage_energy_capacity_units = Param(default=41)                         # Battery capacity is 45 kWh
model.storage_inverter_capacity_units = Param(default=10)                       # Pnom of the inverter is 10 * unit_capacity (1kW) 
model.EV_capacity_units = Param(default=54.5)                                   # EV battery capacity is 60 kWh
model.EV_inverter_capacity_units = Param(default=10)                            # Pnom of the inverter is 10 * unit_capacity (1kW)
model.PV_capacity = Param(default=1e4)                                          # PV system capacity is 10 kWp
model.PV_inverter_capacity_units = Param(default=10)                            # Pnom of the inverter is 10 * unit_capacity (1kW)
model.grid_capacity = Param(default=16)                                         # Not used when GRID_CONNECTED is set to False
model.genset_capacity = Param(default=1e4)                                      # Genset Pnom is 10 kW


# Create constraints:                                   
#           use data.consumption(p) to get consumption for timestep p
#               data.PV_generation(p) to get Pmax [pu] for timestep p
#               data.EV_connected(p) to get connection status of the EV (0 or 1)
#           p should go from 1 to N_PERIODS

def power_balance_rule(m, p): #TODO
    prod_expression = 0
    cons_expression = 0
    return prod_expression >= cons_expression                                   # You should ensure that this constraint is close to tight


def storage_level_rule(m, p): #TODO
    return 


def storage_max_capacity_rule(m, p): #TODO
    return
def storage_min_capacity_rule(m, p): #TODO
    return 


def storage_charge_power_rule1(m, p): #TODO
    return 


def storage_discharge_power_rule1(m, p):
    return  #TODO


def storage_charge_power_rule2(m, p):
    return  #TODO


def storage_discharge_power_rule2(m, p):
    return #TODO



def EV_level_rule(m, p):
    return  #TODO

def EV_target_rule(m,c):
    return #TODO

def EV_max_capacity_rule(m, p):
    return  #TODO

def EV_min_capacity_rule(m, p):
    return  #TODO

def EV_charge_power_rule(m, p):
    return #TODO

def EV_discharge_power_rule(m, p):
    return #TODO

def EV_charge_power_rule2(m, p):                                                # Used when no EV
    return m.charge_EV_sp <=0

def EV_discharge_power_rule2(m, p):                                             # Used when no EV
    return m.discharge_EV_sp[p] <= 0


def PV_generation_rule1(m, p):
    return #TODO


def PV_generation_rule2(m, p):
    return #TODO

def import_limit_rule(m, p):
    return #TODO


def export_limit_rule(m, p):
    return #TODO


def import_limit_rule2(m, p):                                                   # Used when no grid connection
    return m.imp_grid[p] <= 0


def export_limit_rule2(m, p):                                                   # Used when no grid connection
    return m.exp_grid[p] <= 0


def genset_generation_rule(m, p):
    return #TODO


model.power_balance_cstr = Constraint(model.periods, rule=power_balance_rule)

model.storage_level_cstr = Constraint(model.periods, rule=storage_level_rule)
model.storage_min_capacity_cstr = Constraint(model.periods, rule=storage_min_capacity_rule)
model.storage_max_capacity_cstr = Constraint(model.periods, rule=storage_max_capacity_rule)
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
else:
    model.import_limit_cstr = Constraint(model.periods, rule=import_limit_rule2)
    model.export_limit_cstr = Constraint(model.periods, rule=export_limit_rule2)
    

model.genset_generation_cstr = Constraint(model.periods, rule=genset_generation_rule)


# Create objective
def total_cost(m):
    opex = 0 
    return opex

model.obj = Objective(rule=total_cost, sense=pyo.minimize)

# Solve the model
opt = utils.configure_solver(model)
if EXPORT_MODEL:
    print("Exporting model...")
    utils.export_model(model)
print("Solving model...")
results = opt.solve(model, tee=False, keepfiles=False)

# Check is the problem is feasible
status = results.solver.status
termination_condition = results.solver.termination_condition

print("\nSolver status:", status, termination_condition)
if status == 'ok' : utils.plot_and_print(model,data, plot_soc=True) # You can change plot_soc to False to improve readability
# You should do additionnal data processing, do nicer plots, compute other indicators for your system results