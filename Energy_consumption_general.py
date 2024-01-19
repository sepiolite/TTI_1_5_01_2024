import numpy as np 
import matplotlib.pyplot as plt

"""
Let's start from the first_try script, separating electrified VS non electrified energy consumption
"""

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


def E_y_mine_elec_calcul (type_of_mine,SR_y_OP): 
    if type_of_mine == "OP": 
        SR_y = SR_y_OP #stripping ratio, 10 is the maximal, 2.5 used in the article        
        E_y_mine = (E_y_C) * (1 + SR_y) / (C_y * R_y_P * R_y_Me) #cumulative energy demand for the mine

    if type_of_mine == "UG": 
        SR_y = 0.1 
        E_y_mine = ((E_y_C) * (1 + SR_y) + E_y_V) / (C_y * R_y_P * R_y_Me) #cumulative energy demand for the mine
    return(E_y_mine)

def E_y_mine_fuel_calcul (type_of_mine,SR_y_OP): 
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
    return(E_y_mine)


"""
2. Process before metallurgy : fully electrifyable
"""
#Electricity 
E_y_C_G = 43.2 #CED of crushing and grinding in MJ-eq per ton ore
E_y_F = 14.4 #CED of flotation in MJ-eq per ton ore
E_y_L = 10.8 #CED of leaching in MJ-eq per ton ore

def E_y_process_elec_calcul (process): 
    if process == "CGF": 
        E_y_process = (E_y_C_G + E_y_F)/(C_y * R_y_P * R_y_Me)
    if process == "leaching": 
        E_y_process = (E_y_C_G + E_y_L)/(C_y * R_y_P * R_y_Me)
    return(E_y_process)


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

def E_y_metallurgy_elec_calcul (metallurgy): 
    if metallurgy == "pyrometallurgy" : 
        E_y_metallurgy = (E_y_Sm_elec / (R_y_Sm * R_y_Re)) + (E_y_Re / R_y_Re)
    if metallurgy == "hydrometallurgy" : 
        E_y_metallurgy = (E_y_SX / (R_y_SX * R_y_EW)) + (E_y_EW / R_y_EW)
    return(E_y_metallurgy)

def E_y_metallurgy_fuel_calcul (metallurgy): 
    if metallurgy == "pyrometallurgy" : 
        E_y_metallurgy = (E_y_Sm_oil / (R_y_Sm * R_y_Re)) + (E_y_Re / R_y_Re)
    if metallurgy == "hydrometallurgy" : 
        E_y_metallurgy = 0
    return(E_y_metallurgy)


"""
Combine all 
"""

def E_elec_total(mine,SR_y_OP_result,procss,mtallurgy): 
    E_y_mine = E_y_mine_elec_calcul(type_of_mine=mine,SR_y_OP=SR_y_OP_result) 
    E_y_process = E_y_process_elec_calcul(process=procss) 
    E_y_metallurgycalcul = E_y_metallurgy_elec_calcul(metallurgy=mtallurgy)
    E_tot = E_y_mine + E_y_process + E_y_metallurgycalcul
    return(E_tot)

def E_fuel_total(mine,SR_y_OP_result,mtallurgy): 
    E_y_mine = E_y_mine_fuel_calcul(type_of_mine=mine,SR_y_OP=SR_y_OP_result) 
    E_y_process = 0
    E_y_metallurgycalcul = E_y_metallurgy_fuel_calcul(metallurgy=mtallurgy)
    E_tot = E_y_mine + E_y_process + E_y_metallurgycalcul
    return(E_tot)


"""
Part 5 : Look at the shares between all the techniques
In 2010 : 
- Share OP / UG : 90 % - 10 % 
- Share pyro / hydro : 80 % - 20 % 
- Reminder : process --> metallurgy 
    - CGF --> Pyro 
    - Leaching --> hydro
"""


def E_mean_elec_result_with_shares(share_OP_UG, share_pyro_hydro,SR_y_OP_result):
    result_y_mine_with_share = share_OP_UG * E_y_mine_elec_calcul(type_of_mine="OP",SR_y_OP=SR_y_OP_result) + (1 - share_OP_UG) * E_y_mine_elec_calcul(type_of_mine="UG",SR_y_OP=SR_y_OP_result)
    result_y_process_with_share = share_pyro_hydro * E_y_process_elec_calcul(process="CGF") + (1 - share_pyro_hydro) * E_y_process_elec_calcul(process="leaching") 
    result_y_metallurgy_with_share = share_pyro_hydro * E_y_metallurgy_elec_calcul(metallurgy="pyrometallurgy") + (1 - share_pyro_hydro) * E_y_metallurgy_elec_calcul(metallurgy="hydrometallurgy")
    result_with_share = result_y_mine_with_share + result_y_process_with_share + result_y_metallurgy_with_share
    return(result_with_share)

def E_mean_fuel_result_with_shares(share_OP_UG, share_pyro_hydro,SR_y_OP_result):
    result_y_mine_with_share = share_OP_UG * E_y_mine_fuel_calcul(type_of_mine="OP",SR_y_OP=SR_y_OP_result) + (1 - share_OP_UG) * E_y_mine_fuel_calcul(type_of_mine="UG",SR_y_OP=SR_y_OP_result)
    result_y_process_with_share = 0
    result_y_metallurgy_with_share = share_pyro_hydro * E_y_metallurgy_fuel_calcul(metallurgy="pyrometallurgy") + (1 - share_pyro_hydro) * E_y_metallurgy_fuel_calcul(metallurgy="hydrometallurgy")
    result_with_share = result_y_mine_with_share + result_y_process_with_share + result_y_metallurgy_with_share
    return(result_with_share)


#print(E_mean_elec_result_with_shares())
#print(E_mean_fuel_result_with_shares())
    

"""
Graph 1.1 : share OP and UG and Energy consumption evolvment 
- ore_grade = 0.007
- depth = 500 m
- SR_y_OP_result = 2 
- share_pyro = 0.8, share_hydro = 0.2, share_pyro_hydro = 0.8
"""
ore_grade = 0.007
share_OP = np.linspace(0.1, 0.9, 100)  
share_pyro = 0.8
SR_y_OP_result_ = 2 
E_mean_elec = [E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]
E_mean_fuel = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]
E_mean_tot = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) + E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]

plt.plot(share_OP, E_mean_elec, label = "Consommation d'énergie électrique")
plt.plot(share_OP, E_mean_fuel, label = "Consommation d'énergie non-électrique")
plt.plot(share_OP, E_mean_tot, label = "Consommation d'énergie totale")
plt.xlim(0, 1)
plt.ylim(10000, 60000)
plt.xlabel('OP (%)')
plt.ylabel('Consommation énergétique (MJ/t Cu)')
plt.title('Stérile / minerai = 2')
#plt.title('Energy consumption in function of OP-UG repartition (with depth = 500 m)')
legend=plt.legend()
legend.set_title("Energie")
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
E_mean_elec = [E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]
E_mean_fuel = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]
E_mean_tot = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) + E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]

plt.plot(share_OP, E_mean_elec, label = "Consommation d'énergie électrique")
plt.plot(share_OP, E_mean_fuel, label = "Consommation d'énergie non-électrique")
plt.plot(share_OP, E_mean_tot, label = "Consommation d'énergie totale")
plt.xlim(0, 1)
plt.ylim(10000, 60000)
plt.xlabel('OP (%)')
plt.ylabel('Consommation énergétique (MJ/t Cu)')
plt.title('Stérile / minerai = 5')
#plt.title('Energy consumption in function of OP-UG repartition (with depth = 500 m)')
legend=plt.legend()
legend.set_title("Energie")
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
E_mean_elec = [E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]
E_mean_fuel = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]
E_mean_tot = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) + E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_) for x in share_OP]

plt.plot(share_OP, E_mean_elec, label = "Consommation d'énergie électrique")
plt.plot(share_OP, E_mean_fuel, label = "Consommation d'énergie non-électrique")
plt.plot(share_OP, E_mean_tot, label = "Consommation d'énergie totale")
plt.xlim(0, 1)
plt.ylim(10000, 60000)
plt.xlabel('OP (%)')
plt.ylabel('Consommation énergétique (MJ/t Cu)')
plt.title('Stérile / minerai = 10')
#plt.title('Energy consumption in function of OP-UG repartition (with depth = 500 m)')
legend=plt.legend()
legend.set_title("Energie")
plt.show()

"""
Graph 2 : share hydro and pyro and Energy consumption evolvment 
- ore_grade = 0.007
- depth = 500 m
- SR_y_OP_result = 2 
- share_OP_UG = 0.9 (0.9 OP, 0.1 UG)
"""
ore_grade = 0.007
share_pyro = np.linspace(0.1, 0.9, 100)  
share_OP = 0.9
SR_y_OP_result_ = 2 
E_mean_elec = [E_mean_elec_result_with_shares(share_OP_UG=share_OP,share_pyro_hydro=x,SR_y_OP_result=SR_y_OP_result_) for x in share_pyro]
E_mean_fuel = [E_mean_fuel_result_with_shares(share_OP_UG=share_OP,share_pyro_hydro=x,SR_y_OP_result=SR_y_OP_result_) for x in share_pyro]
E_mean_tot = [E_mean_fuel_result_with_shares(share_OP_UG=share_OP,share_pyro_hydro=x,SR_y_OP_result=SR_y_OP_result_) + E_mean_elec_result_with_shares(share_OP_UG=share_OP,share_pyro_hydro=x,SR_y_OP_result=SR_y_OP_result_) for x in share_pyro]

plt.plot(share_pyro, E_mean_elec, label = "Consommation d'énergie électrique")
plt.plot(share_pyro, E_mean_fuel, label = "Consommation d'énergie non électrique")
plt.plot(share_pyro, E_mean_tot, label = "Consommation d'énergie totale")
plt.xlim(0, 1)
plt.ylim(10000, 60000)
plt.xlabel('pyrométallurgie (%)')
plt.ylabel('Consommation énergétique (MJ/t Cu)', labelpad=1)
plt.title('Energy consumption in function of pyro-hydro repartition (with depth = 500 m)')
legend=plt.legend()
legend.set_title("Energie")
plt.show()


"""
Graph 3 : Share OP / UG and Electrical energy consumption evolvment (with different stripping ratio)
- ore_grade = 0.007
- depth = 500 m 
- SR_y_OP_result = 2 - 5 - 10 - 20
"""
d_y = 500 #depth of the path (m)
ore_grade = 0.007
share_pyro = 0.8
share_OP = np.linspace(0.1, 0.9, 100)  
SR_y_OP_result_1 = 2 
SR_y_OP_result_2 = 5 
SR_y_OP_result_3 = 20
SR_y_OP_result_4 = 50 
E_mean_1 = [E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_1) for x in share_OP]
E_mean_2 = [E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_2) for x in share_OP]
E_mean_3 = [E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_3) for x in share_OP]
E_mean_4 = [E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_4) for x in share_OP]
plt.plot(share_OP, E_mean_1, label=SR_y_OP_result_1)
plt.plot(share_OP, E_mean_2, label=SR_y_OP_result_2)
plt.plot(share_OP, E_mean_3, label=SR_y_OP_result_3)
plt.plot(share_OP, E_mean_4, label=SR_y_OP_result_4)
plt.xlim(0.1, 0.9)
plt.ylim(0, 100000)
plt.xlabel(' OP %')
plt.ylabel('Consommation d énergie électrique (MJ/t Cu)', labelpad=1)
legend=plt.legend()
legend.set_title("ratio stérile / minerai des OP")
plt.title('Electrical energy consumption in function of the share OP - UG')
plt.show()


"""
Graph 4 : Share OP / UG and Carbon-based energy consumption evolvment (with different stripping ratio)
- ore_grade = 0.007
- depth = 500 m 
- SR_y_OP_result = 2 - 5 - 10 - 20
"""
d_y = 500 #depth of the path (m)
ore_grade = 0.007
share_pyro = 0.8
share_OP = np.linspace(0.1, 0.9, 100)  
SR_y_OP_result_1 = 2 
SR_y_OP_result_2 = 5 
SR_y_OP_result_3 = 20
SR_y_OP_result_4 = 50 
SR_y_OP_result_5 = 0.1
E_mean_1 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_1) for x in share_OP]
E_mean_2 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_2) for x in share_OP]
E_mean_3 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_3) for x in share_OP]
E_mean_4 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_4) for x in share_OP]
E_mean_5 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_5) for x in share_OP]
plt.plot(share_OP, E_mean_1, label=SR_y_OP_result_1)
plt.plot(share_OP, E_mean_2, label=SR_y_OP_result_2)
plt.plot(share_OP, E_mean_3, label=SR_y_OP_result_3)
plt.plot(share_OP, E_mean_4, label=SR_y_OP_result_4)
plt.plot(share_OP, E_mean_5, label=SR_y_OP_result_5)
plt.xlim(0.1, 0.9)
plt.ylim(0, 100000)
plt.xlabel('OP %')
plt.ylabel('Consommation d énergie non électrique (MJ/t Cu)', labelpad=1)
legend=plt.legend()
legend.set_title("ratio stérile / minerai des OP")
plt.title('Carbon-based energy consumption in function of the share OP - UG')
plt.show()


"""
Graph 5 : Share OP / UG and total energy consumption evolvment (with different stripping ratio)
- ore_grade = 0.007
- depth = 500 m 
- SR_y_OP_result = 2 - 5 - 10 - 20
"""
d_y = 500 #depth of the path (m)
ore_grade = 0.007
share_pyro = 0.8
share_OP = np.linspace(0.1, 0.9, 100)  
SR_y_OP_result_1 = 2 
SR_y_OP_result_2 = 5 
SR_y_OP_result_3 = 20
SR_y_OP_result_4 = 50 
SR_y_OP_result_5 = 0.1
E_mean_1 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_1) + E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_1) for x in share_OP]
E_mean_2 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_2) + E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_2) for x in share_OP]
E_mean_3 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_3) + E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_3) for x in share_OP]
E_mean_4 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_4) + E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_4) for x in share_OP]
E_mean_5 = [E_mean_fuel_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_5) + E_mean_elec_result_with_shares(share_OP_UG=x,share_pyro_hydro=share_pyro,SR_y_OP_result=SR_y_OP_result_5) for x in share_OP]
plt.plot(share_OP, E_mean_5, label=SR_y_OP_result_5)
plt.plot(share_OP, E_mean_1, label=SR_y_OP_result_1)
plt.plot(share_OP, E_mean_2, label=SR_y_OP_result_2)
plt.plot(share_OP, E_mean_3, label=SR_y_OP_result_3)
plt.plot(share_OP, E_mean_4, label=SR_y_OP_result_4)
plt.xlim(0.1, 0.9)
plt.ylim(0, 100000)
plt.xlabel('OP %')
plt.ylabel('Consomation d énergie (MJ/t Cu)', labelpad=1)
legend=plt.legend()
legend.set_title("ratio stérile / minerai des OP")
plt.title('total energy consumption in function of the share OP - UG')
plt.show()

