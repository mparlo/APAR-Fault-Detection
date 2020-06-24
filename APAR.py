import pandas

#lines 8-44 take data from a csv file, find the columns for the variables listed, 
#and create separate arrays for them.
#Variable names have to be the same as the labels specified by the code. 
#A haystack agent of some sort may be necessary for renaming variables so the code can find them.

def read_data(csv_filename):
    data = pandas.read_csv(csv_filename)
    
read_data('Filepath')    

OAD = data.loc[:,'OAD']
MAT = data.loc[:,'MAT']
DAT = data.loc[:,'DAT']
RAT = data.loc[:,'RAT']
OAT = data.loc[:,'OAT']
CCV = data.loc[:,'CCV']
HCV = data.loc[:,'HCV']
date = data.loc[:,'Time']

oad = []
for line in OAD:
    oad.append(line)
mat = []
for line in MAT:
    mat.append(line)
dat = []
for line in DAT:
    dat.append(line)
rat = []
for line in RAT:
    rat.append(line)
oat = []
for line in OAT:
    oat.append(line)
ccv = []
for line in CCV:
    ccv.append(line)
hcv = []
for line in HCV:
    hcv.append(line)
length = len(hcv)

#lines 24-51 create empty arrays for each rule. The fault detection section of code
#will append boolean values to these arrays at each time step - 0 if a rule is broken
#and 0 if a rule is not broken

Rule_1 = []
Rule_2 = []
Rule_3 = []
Rule_4 = []
Rule_5 = []
Rule_6 = []
Rule_7 = []
Rule_8 = []
Rule_9 = []
Rule_10 = []
Rule_11 = []
Rule_12 = []
Rule_13 = []
Rule_14 = []
Rule_15 = []
Rule_16 = []
Rule_17 = []
Rule_18 = []
Rule_19 = []
Rule_20 = []
Rule_21 = []
Rule_22 = []
Rule_23 = []
Rule_24 = []
Rule_25 = []
Rule_26 = []
Rule_27 = []
Rule_28 = []

#lines 56-70 set values that will remain constant. some values will be set in the code, but
#for now the threshold values will be input before any fault detection is performed.

minimum_OAD = 20
eps_t = int(raw_input("What is the temperature threshold?")) 
eps_f = int(raw_input("What is the OAF threshold?"))
eps_hc = int(raw_input("What is the heating coil threshold?"))
eps_cc = int(raw_input("What is the cooling coil threshold?"))
eps_d = int(raw_input("What is the outside air damper threshold?"))
DAT_SP = int(raw_input("What is the DAT set point?"))
"""
min_OAF = minimum OAF threshold?
dt_sf = delta t over supply fan
dt_rf = delta t over return fan
dt_min = threshold on the minimum temperature difference between RAT and OAT
changeover_temp = changeover temperature between modes 3 & 4
MT_max = maximum number of mode changes per hour
"""

#lines 77-89 are a function that will determine the operating mode of the AHU of interest
#(heating, economizing, mechanical cooling with 100% outside air,
#mechanical cooling with minimum outside air, and undetermined)
#and direct the program to a set of rules for each mode. every mode will run all_modes

def determine_mode(hcv,ccv,oad):
    for i in range(0,length):
            return all_modes(oat,mat,dat,rat)
            if hcv[i] != 0 and oad[i] == minimum_OAD and ccv[i] == 0:
                return mode_1(dat,mat,rat,oat,hcv)
            elif oad[i] > minimum_OAD and oad[i] < 100 and hcv[i] == 0 and ccv[i] == 0:
                return mode_2(oat,dat,rat,mat)
            elif oad[i] == 100 and hcv[i] == 0 and ccv[i] != 0:
                return mode_3(oad,dat,mat,rat)
            elif oad[i] == minimum_OAD and ccv[i] != 0:
                return mode_4(oat,mat,dat,rat)
            elif ccv[i] != 0 and hcv[i] != 0:
                return mode_5(ccv,hcv,oad)

determine_mode(hcv,ccv,oad)
        
#the function 'mode_1' applies the rules for fault detection in heating mode to the dataset. 
#at every time step all the rules are evaluated, and boolean variables are stored to indicate  
#faulty/not faulty conditions. This time-series fault data will be used by diagnostics and 
#analytics agents. The functions below also have outputs that tell the user when a broken rule  
#is detected, and which rule it was. This output is for testing the program, and won't necessarily
#be in the final agent.

def mode_1(dat,mat,rat,oat,hcv):
    OAF = (mat[i] - rat[i])/(oat[i] - rat[i])
    if dat[i] < (mat[i] + dt_sf - eps_t):
        Rule_1.append(1)
        print "At",date[i],"Rule 1 was broken. In heating mode, DAT should be greater than MAT."
    else:
        Rule_1.append(0)         
    if abs(rat[a] - oat[i]) >= dt_min and abs(OAF - min_OAF) > eps_f:
        Rule_2.append(1)
        print "At",date[i],"Rule 2 was broken. OAF is too low or too high."
    else:
        Rule_2.append(0)
    if abs(hcv[i] - 100) <= eps_hc and (DAT_SP - dat[i]) >= eps_t:
        Rule_3.append(1)
        print "At",date[i],"Rule 3 was broken. Heating coil valve command is fully open and DAT error exists."
    else:
        Rule_3.append(0)
    if abs(hcv[i] - 100) <= eps_hc:
        Rule_4.append(1)
        print "At",date[i],"Rule 4 was broken. Heating coil valve command is fully open. If heating load increases, DAT will drift from SP."
    else:
        Rule_4.append(0)

#the function 'mode_2' applies the rules for fault detection in economizing mode to the dataset.

def mode_2(oat,dat,rat,mat):
    if oat[i] > (DAT_SP - dt_sf + eps_t):
        Rule_5.append(1)
        print "At",date[i],"Rule 5 was broken. OAT is too warm for cooling with outdoor air (economizing)."
    else:
        Rule_5.append(0)
    if dat[i] > (rat[i] - dt_rf + eps_t):
        Rule_6.append(1)
        print "At",date[i],"Rule 6 was broken. DAT should be less than RAT."
    else:
        Rule_6.append(0)
    if abs(dat[i] - dt_sf - mat[i]) > eps_t:
        Rule_7.append(1)
        print "At",date[i],"Rule 7 was broken. DAT and MAT should be nearly the same."
    else:
        Rule_7.append(0)
        
#the function 'mode_3' applies the rules for fault detection during mechanical cooling with 
#100% outside air to the dataset.

def mode_3(oat,dat,mat,rat):
    if oat[i] < (DAT_SP - dt_sf - eps_t):
        Rule_8.append(1)
        print "At",date[i],"Rule 8 was broken. OAT is too cool for mechanical cooling w/100% outside air"
    else:
        Rule_8.append(0)
    if oat[i] > (changeover_temp + eps_t):
        Rule_9.append(1)
        print "At",date[i],"Rule 9 was broken. Outdoor air enthalpy is too great for mechanical cooling w/100% outside air"
    else:
        Rule_9.append(0)
    if abs(oat[i] - mat[i]) > eps_t:
        Rule_10.append(1)
        print "At",date[i],"Rule 10 was broken. OAT and MAT should be nearly the same"
    else:
        Rule_10.append(0)
    if dat[i] > (mat[i] + dt_sf + eps_t):
        Rule_11.append(1)
        print "At",date[i],"Rule 11 was broken. DAT should be less than MAT."
    else:
        Rule_11.append(0)
    if dat[i] > (rat[i] - dt_rf + eps_t):
        Rule_12.append(1)
        print"At",date[i],"Rule 12 was broken. DAT should be less than RAT."
    else:
        Rule_12.append(0)
    if abs(ccv[i] - 1) <= eps_cc and (DAT_SP - dat[i]) >= eps_t:
        Rule_13.append(1)
        print"At",date[i],"Rule 13 was broken. Cooling coil valve command is fully open and DAT error exists."
    else:
        Rule_13.append(0)
    if abs(ccv[i] - 1) <= eps_cc:
        Rule_14.append(1)
        print"At",date[i],"Rule 14 was broken. Cooling coil valve command is fully open. If cooling load increases, DAT will drift from SP."
    else:
        Rule_14.append(0)

#the function 'mode_4' applies the rules for fault detection during mechanical cooling with 
#minimum outside air to the dataset.
            
def mode_4(oat,mat,dat,rat):
    OAF = (mat[i] - rat[i])/(oat[i] - rat[i])
    if oat[i] < (changeover_temp - eps_t):
        Rule_15.append(1)
        print"At",date[i],"Rule 15 was broken. Outdoor air enthalpy is too low for mechanical cooling w/minimum outside air."
    else:
        Rule_15.append(0)
    if dat[i] > (mat[i] + dt_sf + eps_t):
        Rule_16.append(1)
        print"At",date[i],"Rule 16 was broken. DAT should be less than MAT."
    else:
        Rule_16.append(0)
    if dat[i] > (rat[i] - dt_rf + eps_t):
        Rule_17.append(1)
        print"At",date[i],"Rule 17 was broken. DAT should be less than RAT."
    else:
        Rule_17.append(0)
    if abs(rat[i] - oat[i]) >= dt_min and abs(OAF - min_OAF) > eps_f:
        Rule_18.append(1)
        print"At",date[i],"Rule 18 was broken. OAF is too low or too high."
    else:
        Rule_18.append(0)
    if abs(ccv[i] - 1) <= eps_cc and (DAT_SP - dat[i]) >= eps_t:
        Rule_19.append(1)
        print"At",date[i],"Rule 19 was broken. Cooling coil valve command is fully open and DAT error exists."
    else:
        Rule_19.append(0)
    if abs(ccv[i] - 1) <= eps_cc:
        Rule_20.append(1)
        print"At",date[i],"Rule 20 was broken. Cooling coil valve command is fully open. If cooling load increases, DAT will drift from SP."
    else:
        Rule_20.append(0)
        
#the function 'mode_5' applies the rules for fault detection when the mode is undetermined. 
#undetermined modes are often modes of simultaneous heating and cooling, or economizing and heating,
#or economizing and cooling.

def mode_5(ccv,hcv,oad):
    if ccv[i] > eps_cc and hcv[i] > eps_hc and eps_d < oad[i] < (1 - eps_d):
        Rule_21.append(1)
        print "At",date[i],"Rule 21 was broken. Cooling coil valve, heating coil valve, and outside air dampers are modulating simultaneously."
    else:
        Rule_21.append(0)
    if hcv[i] > eps_hc and ccv[i] > eps_cc:
        Rule_22.append(1)
        print "At",date[i],"Rule 22 was broken. Heating coil valve and cooling coil valve are modulating simultaneously."
    else:
        Rule_22.append(0)
    if hcv[i] > eps_hc and oad[i] > eps_d:
        Rule_23.append(1)
        print "At",date[i],"Rule 23 was broken. Heating coil valve and outside air damper are modulating simultaneously."
    else:
        Rule_23.append(0)
    if eps_d < oad[i] < (1 - eps_d) and ccv[i] > eps_cc:
        Rule_24.append(1)
        print "At",date[i],"Rule 24 was broken. Outside air damper and cooling coil valve are modulating simultaneously."
    else:
        Rule_24.append(0)
        
#the function 'all_modes' will be apply a set of rules to every dataset, regardless of mode.
#these rules are for detecting faults in the design of the AHU and in the temperature sensors.
        
def all_modes(oat,mat,dat,rat):
    if abs(dat[i] - DAT_SP) > eps_t:
        Rule_25.append(1)
        print"At",date[i],"Rule 25 was broken. Persistent DAT error exists."
    else:
        Rule_25.append(0)
    if mat[i] < (min(rat[i],oat[i]) - eps_t):
        Rule_26.append(1)
        print "At",date[i],"Rule 26 was broken. MAT should be between RAT and OAT - MAT too great."
    else:
        Rule_26.append(0)
    if mat[i] > (max(rat[i],oat[i]) - eps_t):
        Rule_27.append(1)
        print "At",date[i],"Rule 27 was broken. MAT should be between RAT and OAT - MAT too low."
    else:
        Rule_27.append(0)
    if MT_h > MT_max: 
        Rule_28.append(1)
        print "At",date[i],"Rule 28 was broken. Too many mode switches per hour."
    else:
        Rule_28.append(0)
        """ HAVE TO DEVELOP THIS RULE """

