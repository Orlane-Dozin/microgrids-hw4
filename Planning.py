from param import delta_t
from param import SOC_min_bss, SOC_max_bss, eff_bss
from param import C_ev, P_nom_ev, eff_ev, SOC_min_ev, SOC_max_ev, SOC_target_ev
from param import PI_gen, PI_imp, PI_exp
from param import P_max_hp, COP_hp, delta_T_max, C_hp

from pyomo.environ import ConcreteModel, Param, Var, Objective, Constraint, NonNegativeReals, minimize
from datetime import datetime
import utils

def create_model(res,C_pv,C_bss,P_nom_bss, P_nom_pv, P_max_gen):
    # Create a concrete model
    model = ConcreteModel()
    
    model.periods = range(res.t_s)
    # model.connections = range(len(res.t_arr)) # A set is created with length equal to the number of EV connections

    # Access all parameters present in the res object.
    # These exists for each t in model.t:
    #  - model.P_load[t] = Load power at time t
    #  - model.P_pv_max[t] = Max available PV power at time t
    #  - model.EV_connected[t] = EV connected at time t
    #  - model.t_arr[t] = Bollean connexion of the EV
    #  - model.t_dep[t] = Boolean disconnexion of the EV
    #  - model.SOC_i_ev[t] = Initial SOC of the EV connected at time t (only non zero if t_arr[t] is true)
    model.P_load = Param(model.periods, initialize=[res.P_load[t] for t in model.periods], mutable=True)
    model.P_pv_max = Param(model.periods, initialize=[res.P_pv_max[t] for t in  model.periods], mutable=True)
    model.EV_connected = Param(model.periods, initialize=[res.EV_connected[t] for t in  model.periods], mutable=True)
    model.t_arr = Param(model.periods, initialize=[res.t_arr[t] for t in model.periods], mutable=True)
    model.t_dep = Param(model.periods, initialize=[res.t_dep[t] for t in model.periods], mutable=True)
    model.SOC_i_ev = Param(model.periods, initialize=[res.SOC_i_ev[t] for t in model.periods], mutable=True)
    model.T_set = Param(model.periods, initialize=[res.T_set[t] for t in model.periods], mutable=True)
    model.P_loss = Param(model.periods, initialize=[res.P_loss[t] for t in model.periods], mutable=True)
    model.SOC_0_bss = Param(initialize=0.5*C_bss, mutable=True)
    model.SOC_0_ev = Param(initialize=0.5*C_ev, mutable=True)
    model.T_0_hp = Param(initialize=res.T_set[0], mutable=True)

    # Operation planning asset sizes
    model.P_nom_pv = Param(initialize=P_nom_pv)                            # Nominal power for PV inverter
    model.C_bss = Param(initialize=C_bss)                                  # Battery capacity
    model.C_pv = Param(initialize=C_pv)                                    # PV system size
    model.P_nom_bss = Param(initialize=P_nom_bss)                          # Battery inverter nominal power
    model.P_nom_ev = Param(initialize=P_nom_ev)                            # EV inverter nominal power
    model.C_ev = Param(initialize=C_ev)                                    # EV capacity
    model.P_max_gen = Param(initialize=P_max_gen)                          # Maximum generator power

    # Variables
    model.P_imp = Var(model.periods, within=NonNegativeReals)              # Imported power
    model.P_exp = Var(model.periods, within=NonNegativeReals)              # Exported power
    model.P_pv = Var(model.periods, within=NonNegativeReals)               # PV power output 
    model.P_gen = Var(model.periods, within=NonNegativeReals)              # Generator power output 
    model.P_charge_bss = Var(model.periods, within=NonNegativeReals)       # Battery charging power 
    model.P_discharge_bss = Var(model.periods, within=NonNegativeReals)    # Battery discharging power 
    model.P_charge_ev = Var(model.periods, within=NonNegativeReals)        # EV charging power 
    model.P_discharge_ev = Var(model.periods, within=NonNegativeReals)     # EV discharging power 
    model.P_hp_hot = Var(model.periods, within=NonNegativeReals) 
    model.P_hp_cold = Var(model.periods, within=NonNegativeReals) 
    model.T_hp = Var(model.periods, within=NonNegativeReals)


    # Energy storage variables for battery and EV
    model.SOC_bss = Var(model.periods, within=NonNegativeReals)            # Bss state of charge [kWh]
    model.SOC_ev = Var(model.periods, within=NonNegativeReals)             # EV state of charge [kWh]
    
    # Define the objective function ----------------------------------------------------------------------------
    model.objective = Objective(sense=minimize,
                                expr= 0)
    
    #Constraints ---------------------------------------------------------------------------------------------------------------------------
    
    return model

def run(model, results):
    model, results = utils.solve_model(model, results)
    if model and results:
        utils.check_res(results)
        utils.print_res(results)
        utils.plot_res(results)  
    return results


if __name__ == "__main__":
    start_time = datetime(2021, 1, 1, 0, 0, 0)                                  # Start time of the simulation [YYYY, MM, DD, HH, MM, SS]
    n_days = 365                                                                 # Number of days to simulate

    # Given quantities for the system sizes
    C_pv = 10                            # PV system size [kWp]
    C_bss = 40                           # Battery capacity [kWh]	
    P_nom_bss = 10                       # Battery inverter nominal power [kW]
    P_nom_pv = 10                        # PV inverter nominal power [kW]
    P_max_gen = 10                       # Maximum generator power [kW]


    results = utils.Results(start_time, n_days, yearly_kwh=0, yearly_km=0)      # Initialize results object with start time and number of days, yearly consumption and km driven
    model = create_model(results,C_pv,C_bss,P_nom_bss, P_nom_pv, P_max_gen)
    run(model, results)
