import numpy as np 
import matplotlib.pyplot as plt

"""
Let's start from the second_try_ele_VS_fuel.py script, separating electrified VS non electrified energy consumption
We suppose that : 
- For electrified processes : Final emission (= considering the efficacy)
    - best case scenario : 50 gCO2/ kWh <=> 50 / 3.6 gCO2 / MJ (Fully renewable E + nuclear E)
    - worst case scenario : 1000 g CO2 / kWh (300 g par E primaire + 30 % efficacy rate, fully coal) <=> 1000 / 3.6 g CO2 / MJ
"""

#Electricity cases 
best_case_scenario = 50 / 3.6
worst_case_scenario =  1000 / 3.6

"""
first part : separate the parameters used in first_try.py
1. Mining processes
"""

#Electricity 
E_y_C = 3.6 #CED of crushing in MJ-eq per ton ore (1 kWh / ton ore for UG & OP)
E_y_V = 72 # CED of ventilation in MJ-eq per ton ore, for UG mines only, 20 kWh 

#Diesel 
E_y_Ld = 7.3 #CED of loading in MJ-eq per ton ore, for OP mines only
E_y_H_L = 5.7# CED of loading and hauling in MJ-eq per ton ore, for UG mines only
#drilling and blasting, and transportation too 

#Other 
d_y = 500 #depth of the path (m)
road_gradient = 0.1 #angle of the road, 10 % is the maximum 
C_y = 0.007 #The ore grade
R_y_P = 0.7 #recovery rate of processing 
R_y_Me = 0.9 #recovery rate of metallurgy


def g_CO2_mine_elec_calcul (type_of_mine,SR_y_OP,energy_case_scenario): 
    """
    Final emission (= considering the efficacy)
    - best case scenario : 50 / 3.6 gCO2 / MJ (Fully renewable E + nuclear E)
    - worst case scenario : 1000 / 3.6 g CO2 / MJ
    """

    if type_of_mine == "OP": 
        SR_y = SR_y_OP #stripping ratio, 10 is the maximal, 2.5 used in the article        
        E_y_mine = (E_y_C) * (1 + SR_y) / (C_y * R_y_P * R_y_Me) #cumulative energy demand for the mine

    if type_of_mine == "UG": 
        SR_y = 0.1 
        E_y_mine = ((E_y_C) * (1 + SR_y) + E_y_V) / (C_y * R_y_P * R_y_Me) #cumulative energy demand for the mine
    
    g_CO2 = E_y_mine * energy_case_scenario
    return(g_CO2)

def g_CO2_mine_fuel_calcul (type_of_mine,SR_y_OP): 
    """
    Primary emission (= not considering the efficacy)
    Here, all the processes are guessed to use fuel
    """
    fuel_CO2_per_MJ = 300 / 3.6 #g CO2 / MJ 

    if type_of_mine == "OP": 
        E_y_D_B = 2 #CED of drilling and blasting in MJ-eq per ton ore, 2 for OP
        e_y_T = 0.0005 #CED of transportation in MJ-eq per ton ore and m, 0.0005 for OP
        SR_y = SR_y_OP #stripping ratio, 10 is the maximal, 2.5 used in the article   
        distance = (d_y / np.sin(road_gradient)) * 2  
        E_y_mine = (E_y_D_B + E_y_Ld + e_y_T*distance) * (1 + SR_y) / (C_y * R_y_P * R_y_Me) #cumulative energy demand for the mine

    if type_of_mine == "UG": 
        E_y_D_B = 11.5 #CED of drilling and blasting in MJ-eq per ton ore, 11.5 for UG
        e_y_T = 0.029 #CED of transportation in MJ-eq per ton ore and m, 0.029 for UG
        SR_y = 0.1 
        E_y_mine = ((E_y_D_B + E_y_H_L + e_y_T*d_y) * (1 + SR_y)) / (C_y * R_y_P * R_y_Me) #cumulative energy demand for the mine
    
    g_CO2 = E_y_mine * fuel_CO2_per_MJ
    return(g_CO2)


"""
2. Process before metallurgy : fully electrifyable
"""
#Electricity 
E_y_C_G = 43.2 #CED of crushing and grinding in MJ-eq per ton ore
E_y_F = 14.4 #CED of flotation in MJ-eq per ton ore
E_y_L = 10.8 #CED of leaching in MJ-eq per ton ore

def g_CO2_process_elec_calcul (process,energy_case_scenario): 
    """
    Final emission (= considering the efficacy)
    - best case scenario : 50 / 3.6 gCO2 / MJ (Fully renewable E + nuclear E)
    - worst case scenario : 1000 / 3.6 g CO2 / MJ
    """
    if process == "CGF": 
        E_y_process = (E_y_C_G + E_y_F)/(C_y * R_y_P * R_y_Me)
    if process == "leaching": 
        E_y_process = (E_y_C_G + E_y_L)/(C_y * R_y_P * R_y_Me)
    g_CO2 = E_y_process * energy_case_scenario
    return(g_CO2)


"""
3. Metallurgy
- Smelting uses electricity and fuel oil : separation of the parameter in E_y_Sm_elec and E_y_Sm_oil
"""

#Electriity 
E_y_Sm_elec = 1800 #CED of smelting in MJ-eq per ton Cu (and not Ore)
E_y_Re = 1440 #CED of refining in MJ-eq per ton ore
E_y_SX = 3600 #CED of solvent extraction in MJ-eq per ton Cu
E_y_EW = 7200 #CED of electrowinning in MJ-eq per ton Cu

#Fuel
E_y_Sm_oil = 4175 #CED of smelting in MJ-eq per ton Cu (and not Ore)

#Other
R_y_Sm = 0.97 #recovery rate of smelting in % 
R_y_Re = 1 #recovery rate of refining in % 
R_y_SX = 0.9 #recovery rate of solvent extraction in % 
R_y_EW = 1 #recovery rate of electrowinning in %

def g_CO2_metallurgy_elec_calcul (metallurgy,energy_case_scenario): 
    """
    Final emission (= considering the efficacy)
    - best case scenario : 50 / 3.6 gCO2 / MJ (Fully renewable E + nuclear E)
    - worst case scenario : 1000 / 3.6 g CO2 / MJ
    """
    if metallurgy == "pyrometallurgy" : 
        E_y_metallurgy = (E_y_Sm_elec / (R_y_Sm * R_y_Re)) + (E_y_Re / R_y_Re)
    if metallurgy == "hydrometallurgy" : 
        E_y_metallurgy = (E_y_SX / (R_y_SX * R_y_EW)) + (E_y_EW / R_y_EW)
    g_CO2 = E_y_metallurgy * energy_case_scenario
    return(g_CO2)

def g_CO2_metallurgy_fuel_calcul (metallurgy): 
    """
    Primary emission (= not considering the efficacy)
    Here, all the pyrometallurgy process uses coke, 300 g CO2 / MWh <=> 300 / 3.6 g CO2 / MJ
    """
    coal_CO2_per_MJ = 300 / 3.6 #g CO2 / MJ 
    if metallurgy == "pyrometallurgy" : 
        E_y_metallurgy = (E_y_Sm_oil / (R_y_Sm * R_y_Re)) + (E_y_Re / R_y_Re)
    if metallurgy == "hydrometallurgy" : 
        E_y_metallurgy = 0
    g_CO2 = E_y_metallurgy * coal_CO2_per_MJ
    return(g_CO2)


"""
Combine all 
"""

def g_CO2_elec_total(mine,SR_y_OP_result,procss,mtallurgy,e_case_scenario): 
    g_CO2_mine = g_CO2_mine_elec_calcul(type_of_mine=mine,SR_y_OP=SR_y_OP_result,energy_case_scenario=e_case_scenario) 
    g_CO2_process = g_CO2_process_elec_calcul(process=procss,energy_case_scenario=e_case_scenario) 
    g_CO2_metallurgycalcul = g_CO2_metallurgy_elec_calcul(metallurgy=mtallurgy,energy_case_scenario=e_case_scenario)
    g_CO2_tot = g_CO2_mine + g_CO2_process + g_CO2_metallurgycalcul
    return(g_CO2_tot)

def g_CO2_carbonated_total(mine,SR_y_OP_result,mtallurgy): 
    g_CO2_mine = g_CO2_mine_fuel_calcul(type_of_mine=mine,SR_y_OP=SR_y_OP_result) 
    g_CO2_process = 0
    g_CO2_metallurgycalcul = g_CO2_metallurgy_fuel_calcul(metallurgy=mtallurgy)
    g_CO2_tot = g_CO2_mine + g_CO2_process + g_CO2_metallurgycalcul
    return(g_CO2_tot)


"""
Part 5 : Look at the shares between all the techniques
In 2010 : 
- Share OP / UG : 90 % - 10 % 
- Share pyro / hydro : 80 % - 20 % 
- Reminder : process --> metallurgy 
    - CGF --> Pyro 
    - Leaching --> hydro
"""


def g_CO2_elec_result_with_shares(share_OP_UG, share_pyro_hydro,SR_y_OP_result,e_case_scenario):
    result_y_mine_with_share = share_OP_UG * g_CO2_mine_elec_calcul(type_of_mine="OP",SR_y_OP=SR_y_OP_result,energy_case_scenario=e_case_scenario) + (1 - share_OP_UG) * g_CO2_mine_elec_calcul(type_of_mine="UG",SR_y_OP=SR_y_OP_result,energy_case_scenario=e_case_scenario)
    result_y_process_with_share = share_pyro_hydro * g_CO2_process_elec_calcul(process="CGF",energy_case_scenario=e_case_scenario) + (1 - share_pyro_hydro) * g_CO2_process_elec_calcul(process="leaching",energy_case_scenario=e_case_scenario) 
    result_y_metallurgy_with_share = share_pyro_hydro * g_CO2_metallurgy_elec_calcul(metallurgy="pyrometallurgy",energy_case_scenario=e_case_scenario) + (1 - share_pyro_hydro) * g_CO2_metallurgy_elec_calcul(metallurgy="hydrometallurgy",energy_case_scenario=e_case_scenario)
    result_with_share = result_y_mine_with_share + result_y_process_with_share + result_y_metallurgy_with_share
    return(result_with_share)

def g_CO2_fuel_result_with_shares(share_OP_UG, share_pyro_hydro,SR_y_OP_result):
    result_y_mine_with_share = share_OP_UG * g_CO2_mine_fuel_calcul(type_of_mine="OP",SR_y_OP=SR_y_OP_result) + (1 - share_OP_UG) * g_CO2_mine_fuel_calcul(type_of_mine="UG",SR_y_OP=SR_y_OP_result)
    result_y_process_with_share = 0
    result_y_metallurgy_with_share = share_pyro_hydro * g_CO2_metallurgy_fuel_calcul(metallurgy="pyrometallurgy") + (1 - share_pyro_hydro) * g_CO2_metallurgy_fuel_calcul(metallurgy="hydrometallurgy")
    result_with_share = result_y_mine_with_share + result_y_process_with_share + result_y_metallurgy_with_share
    return(result_with_share)


##best_case_scenario
#print("best case scenario")
#print("g_CO2_elec = " + str(g_CO2_elec_result_with_shares(share_OP_UG=0.9, share_pyro_hydro=0.8,SR_y_OP_result=2,e_case_scenario=best_case_scenario)) + " g CO2 / t Cu")
#print("g_CO2_carbonated = " + str(g_CO2_fuel_result_with_shares(share_OP_UG=0.9, share_pyro_hydro=0.8,SR_y_OP_result=2)) + " #g CO2 / t Cu")

##worst_case_scenario
print("worst case scenario")
print("g_CO2_elec = " + str(g_CO2_elec_result_with_shares(share_OP_UG=0.9, share_pyro_hydro=0.8,SR_y_OP_result=2,e_case_scenario=worst_case_scenario)) + " g CO2 / t Cu")
print("g_CO2_carbonated = " + str(g_CO2_fuel_result_with_shares(share_OP_UG=0.9, share_pyro_hydro=0.8,SR_y_OP_result=2)) + " #g CO2 / t Cu")


"""
Graph 1 : share OP and UG and Energy consumption evolvment 
- ore_grade = 0.007
- depth = 500 m
- SR_y_OP_result = 2 
- share_pyro = 0.8, share_hydro = 0.2, share_pyro_hydro = 0.8
"""
ore_grade = 0.007
share_OP = np.linspace(0.1, 0.9, 100)  
share_pyro = 0.8
SR_y_OP_result_ = 2 
g_mean_elec_worst = [g_CO2_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=0.8,SR_y_OP_result=2,e_case_scenario=worst_case_scenario) + g_CO2_fuel_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=2) for x in share_OP]
g_mean_elec_best = [g_CO2_elec_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=2,e_case_scenario=best_case_scenario) + g_CO2_fuel_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=2) for x in share_OP]

plt.plot(share_OP, g_mean_elec_worst, label = "Cas limite, électricité la plus carbonée")
plt.plot(share_OP, g_mean_elec_best, label = "Cas limite, électricité la moins carbonée")
plt.xlim(0, 1)
plt.ylim(100000, 12000000)
plt.xlabel('OP (%)')
plt.ylabel('g CO2 émis / t Cu')
plt.title('Stérile / Minerai = 2')
legend=plt.legend()
legend.set_title("Electricité")
plt.show()

"""
Graph 1.2 : share OP and UG and Energy consumption evolvment 
- ore_grade = 0.007
- depth = 500 m
- SR_y_OP_result = 5 
- share_pyro = 0.8, share_hydro = 0.2, share_pyro_hydro = 0.8
"""
ore_grade = 0.007
share_OP = np.linspace(0.1, 0.9, 100)  
share_pyro = 0.8
SR_y_OP_result_ = 5 
g_mean_elec_worst = [g_CO2_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=0.8,SR_y_OP_result=5,e_case_scenario=worst_case_scenario) + g_CO2_fuel_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=5) for x in share_OP]
g_mean_elec_best = [g_CO2_elec_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=5,e_case_scenario=best_case_scenario) + g_CO2_fuel_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=5) for x in share_OP]

plt.plot(share_OP, g_mean_elec_worst, label = "Cas limite, électricité la plus carbonée")
plt.plot(share_OP, g_mean_elec_best, label = "Cas limite, électricité la moins carbonée")
plt.xlim(0, 1)
plt.ylim(100000, 12000000)
plt.xlabel('OP (%)')
plt.ylabel('g CO2 émis / t Cu')
plt.title('Stérile / Minerai = 5')
#plt.title('Emission de GES en fonction de la répartition OP-UG (with depth = 500 m)')
legend=plt.legend()
legend.set_title("Electricité")
plt.show()


"""
Graph 1.3 : share OP and UG and Energy consumption evolvment 
- ore_grade = 0.007
- depth = 500 m
- SR_y_OP_result = 10 
- share_pyro = 0.8, share_hydro = 0.2, share_pyro_hydro = 0.8
"""
ore_grade = 0.007
share_OP = np.linspace(0.1, 0.9, 100)  
share_pyro = 0.8
SR_y_OP_result_ = 10 
g_mean_elec_worst = [g_CO2_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=0.8,SR_y_OP_result=10,e_case_scenario=worst_case_scenario) + g_CO2_fuel_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=10) for x in share_OP]
g_mean_elec_best = [g_CO2_elec_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=10,e_case_scenario=best_case_scenario) + g_CO2_fuel_result_with_shares(share_OP_UG=x, share_pyro_hydro=0.8,SR_y_OP_result=10) for x in share_OP]

plt.plot(share_OP, g_mean_elec_worst, label = "Cas limite, électricité la plus carbonée")
plt.plot(share_OP, g_mean_elec_best, label = "Cas limite, électricité la moins carbonée")
plt.xlim(0, 1)
plt.ylim(100000, 12000000)
plt.xlabel('OP (%)')
plt.ylabel('g CO2 émis / t Cu')
plt.title('Stérile / Minerai = 10')
#plt.title('Emission de GES en fonction de la répartition OP-UG (with depth = 500 m)')
legend=plt.legend()
legend.set_title("Electricité")
plt.show()




"""
Graph 2 : share hydro and pyro and CO2
- ore_grade = 0.007
- depth = 500 m
- SR_y_OP_result = 2 
- share_OP_UG = 0.9 (0.9 OP, 0.1 UG)
"""
ore_grade = 0.007
share_pyro = np.linspace(0.1, 0.9, 100)  
share_OP = 0.9
SR_y_OP_result_ = 2 
g_mean_elec_worst = [g_CO2_elec_result_with_shares(share_OP_UG=share_OP,share_pyro_hydro=x,SR_y_OP_result=2,e_case_scenario=worst_case_scenario) + g_CO2_fuel_result_with_shares(share_OP_UG=share_OP, share_pyro_hydro=x,SR_y_OP_result=2) for x in share_pyro]
g_mean_elec_best = [g_CO2_elec_result_with_shares(share_OP_UG=share_OP, share_pyro_hydro=x,SR_y_OP_result=2,e_case_scenario=best_case_scenario) + g_CO2_fuel_result_with_shares(share_OP_UG=share_OP, share_pyro_hydro=x,SR_y_OP_result=2) for x in share_pyro]

plt.plot(share_pyro, g_mean_elec_worst, label = "Cas limite, électricité la plus carbonée")
plt.plot(share_pyro, g_mean_elec_best, label = "Cas limite, électricité la moins carbonée")
plt.xlim(0, 1)
plt.ylim(100000, 10000000)
plt.xlabel('pyrométallurgie (%)')
plt.ylabel('g CO2 émis / t Cu')
#plt.title('Emission de GES en fonction de la répartition OP-UG (with depth = 500 m)')
legend=plt.legend()
legend.set_title("Electricité")
plt.show()
