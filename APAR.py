import pandas
import datetime

data = pandas.read_csv('C:\Users\Morgan\AnacondaProjects\APAR\APAR Test Data - Rule 15.csv')

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

dt_obj = []
for a in date:
    dt_obj.append(datetime.datetime.strptime(a, "%m/%d/%y %H:%M"))

length = len(hcv)
dt_sf = 2
dt_rf = 2
dt_min = 3
changeover_temp = 80
min_OAF = 0.3
minimum_OAD = 20
DAT_SP = 74
eps_t = 3
eps_f = 0.2
eps_hc = 12
eps_cc = 12
eps_d = 7

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

for a in range(0,length):
    OAF = (mat[a] - rat[a])/(oat[a] - rat[a])
    if abs(dat[a] - DAT_SP) > eps_t:
        Rule_25.append(1)
        print"At",date[a],"Rule 25 was broken. Persistent DAT error exists."
    else:
        Rule_25.append(0)
    if mat[a] < (min(rat[a],oat[a]) - eps_t):
        Rule_26.append(1)
        print "At",date[a],"Rule 26 was broken. MAT should be between RAT and OAT - MAT too low."
    else:
        Rule_26.append(0)
    if mat[a] > (max(rat[a],oat[a]) + eps_t):
        Rule_27.append(1)
        print "At",date[a],"Rule 27 was broken. MAT should be between RAT and OAT - MAT too high."
    else:
        Rule_27.append(0)
    #if MT_h > MT_max: 
     #   Rule_28.append(1)
      #  print "At",date[a],"Rule 28 was broken. Too many mode switches per hour."
    #else:
     #   Rule_28.append(0)
      #  """ HAVE TO DEVELOP THIS RULE """

    if hcv[a] != 0 and oad[a] == minimum_OAD and ccv[a] == 0:
        if dat[a] < (mat[a] + dt_sf - eps_t):
            Rule_1.append(1)
            print "At",date[a],"Rule 1 was broken. In heating mode, DAT should be greater than MAT."
        else:
            Rule_1.append(0)         
        if abs(rat[a] - oat[a]) >= dt_min and abs(OAF - min_OAF) > eps_f:
            Rule_2.append(1)
            print "At",date[a],"Rule 2 was broken. OAF is too low or too high."
        else:
            Rule_2.append(0)
        if abs(hcv[a] - 100) <= eps_hc and abs(DAT_SP - dat[a]) >= eps_t:
            Rule_3.append(1)
            print "At",date[a],"Rule 3 was broken. Heating coil valve command is fully open and DAT error exists."
        else:
            Rule_3.append(0)
        if abs(hcv[a] - 100) <= eps_hc:
            Rule_4.append(1)
            print "At",date[a],"Rule 4 was broken. Heating coil valve command is fully open. If heating load increases, DAT will drift from SP."
        else:
            Rule_4.append(0)
    elif oad[a] > minimum_OAD and oad[a] <= 100 and hcv[a] == 0 and ccv[a] == 0:      
        if oat[a] > (DAT_SP - dt_sf + eps_t):
            Rule_5.append(1)
            print "At",date[a],"Rule 5 was broken. OAT is too warm for cooling with outdoor air (economizing)."
        else:
            Rule_5.append(0)
        if dat[a] > (rat[a] - dt_rf + eps_t):
            Rule_6.append(1)
            print "At",date[a],"Rule 6 was broken. DAT should be less than RAT."
        else:
            Rule_6.append(0)
        if abs(dat[a] - dt_sf - mat[a]) > eps_t:
            Rule_7.append(1)
            print "At",date[a],"Rule 7 was broken. DAT and MAT should be nearly the same."
        else:
            Rule_7.append(0)
    elif oad[a] == 100 and hcv[a] == 0 and ccv[a] != 0:
        if oat[a] < (DAT_SP - dt_sf - eps_t):
            Rule_8.append(1)
            print "At",date[a],"Rule 8 was broken. OAT is too cool for mechanical cooling w/100% outside air"
        else:
            Rule_8.append(0)
        if oat[a] > (changeover_temp + eps_t):
            Rule_9.append(1)
            print "At",date[a],"Rule 9 was broken. Outdoor air enthalpy is too great for mechanical cooling w/100% outside air"
        else:
            Rule_9.append(0)
        if abs(oat[a] - mat[a]) > eps_t:
            Rule_10.append(1)
            print "At",date[a],"Rule 10 was broken. OAT and MAT should be nearly the same"
        else:
            Rule_10.append(0)
        if dat[a] > (mat[a] + dt_sf + eps_t):
            Rule_11.append(1)
            print "At",date[a],"Rule 11 was broken. DAT should be less than MAT."
        else:
            Rule_11.append(0)
        if dat[a] > (rat[a] - dt_rf + eps_t):
            Rule_12.append(1)
            print"At",date[a],"Rule 12 was broken. DAT should be less than RAT."
        else:
            Rule_12.append(0)
        if abs(ccv[a] - 100) <= eps_cc and abs(DAT_SP - dat[a]) >= eps_t:
            Rule_13.append(1)
            print"At",date[a],"Rule 13 was broken. Cooling coil valve command is fully open and DAT error exists."
        else:
            Rule_13.append(0)
        if abs(ccv[a] - 100) <= eps_cc:
            Rule_14.append(1)
            print"At",date[a],"Rule 14 was broken. Cooling coil valve command is fully open. If cooling load increases, DAT will drift from SP."
        else:
            Rule_14.append(0)
    elif oad[a] == minimum_OAD and ccv[a] != 0 and hcv[a] == 0:
        if oat[a] < (changeover_temp - eps_t):
            Rule_15.append(1)
            print"At",date[a],"Rule 15 was broken. Outdoor air enthalpy is too low for mechanical cooling w/minimum outside air."
        else:
            Rule_15.append(0)
        if dat[a] > (mat[a] + dt_sf + eps_t):
            Rule_16.append(1)
            print"At",date[a],"Rule 16 was broken. DAT should be less than MAT."
        else:
            Rule_16.append(0)
        if dat[a] > (rat[a] - dt_rf + eps_t):
            Rule_17.append(1)
            print"At",date[a],"Rule 17 was broken. DAT should be less than RAT."
        else:
            Rule_17.append(0)
        if abs(rat[a] - oat[a]) >= dt_min and abs(OAF - min_OAF) > eps_f:
            Rule_18.append(1)
            print"At",date[a],"Rule 18 was broken. OAF is too low or too high."
        else:
            Rule_18.append(0)
        if abs(ccv[a] - 100) <= eps_cc and abs(DAT_SP - dat[a]) >= eps_t:
            Rule_19.append(1)
            print"At",date[a],"Rule 19 was broken. Cooling coil valve command is fully open and DAT error exists."
        else:
            Rule_19.append(0)
        if abs(ccv[a] - 100) <= eps_cc:
            Rule_20.append(1)
            print"At",date[a],"Rule 20 was broken. Cooling coil valve command is fully open. If cooling load increases, DAT will drift from SP."
        else:
            Rule_20.append(0)
    elif ccv[a] != 0 and hcv[a] != 0:
        if ccv[a] >= eps_cc and hcv[a] >= eps_hc and eps_d <= oad[a] <= (100 - eps_d):
            Rule_21.append(1)
            print "At",date[a],"Rule 21 was broken. Cooling coil valve, heating coil valve, and outside air dampers are modulating simultaneously."
        else:
            Rule_21.append(0)
        if hcv[a] >= eps_hc and ccv[a] >= eps_cc:
            Rule_22.append(1)
            print "At",date[a],"Rule 22 was broken. Heating coil valve and cooling coil valve are modulating simultaneously."
        else:
            Rule_22.append(0)
        if hcv[a] >= eps_hc and oad[a] >= eps_d:
            Rule_23.append(1)
            print "At",date[a],"Rule 23 was broken. Heating coil valve and outside air damper are modulating simultaneously."
        else:
            Rule_23.append(0)
        if eps_d <= oad[a] <= (100 - eps_d) and ccv[a] >= eps_cc:
            Rule_24.append(1)
            print "At",date[a],"Rule 24 was broken. Outside air damper and cooling coil valve are modulating simultaneously."
        else:
            Rule_24.append(0)