# MachineLearningCookieData
# 
# C:\DaveL\Technical\MyPyScripts\MachineLearningCookieData
#
# Classifies Cookies at good or bad in well known Cookie Dataset.
#   Reads data in CookieData2.txt which resides in same folder as Python script
#
# 2/19/2020 David Larson

import scipy as sp
import matplotlib.pylab as plt
import numpy as np
import time

start = time.time()
# Read Data to be Classified -----------------------------

# Open file
f = open('CookieData2.txt', 'r')

# Read and ignore header lines
header1 = f.readline() # Read and ignore single header line

# Loop over lines and extract variables of interest
InFileData = [] # List with all input data, [Radius, Chips, Goodness]
GR = []         # Radius values with good=1
GC = []         # Chip values with good=0
BR = []         # Radius values with good=1
BC = []         # Chip values with good=0
AR = []         # All Radius Values
AC = []         # All Chip Values
for line in f:
    line = line.strip()         # Remove leading and trailing spaces
    columns = line.split()      # Spilt into strings at white space (with no argument)
    Radius = float(columns[0])  # Columns var has 3 strings, convert to floating point numbers
    Chips = float(columns[1])
    Goodness = float(columns[2])
    InFileData.append([Radius, Chips, Goodness])  # Make list of input data
    AR.append(Radius)           # Radius value list
    AC.append(Chips)            # Chips value list
    if Goodness == 1:           # Make lists of Good and Bad Radius/Chips
        GR.append(Radius)
        GC.append(Chips)
    else:
        BR.append(Radius)
        BC.append(Chips)
    # print(Radius, Chips, Goodness)

f.close()
print('Actual Defined Good Cookies:  ' + str(len(GR)))
print('Actual Defined Bad Cookies:   ' + str(len(BR)))

# Define Search Grid ---------------------------------------
# T1 = Classification Value (Mean Radius Squared of all Data)
# T2 = Cookie Radius Elipse Factor
# T3 = Chip Count Elipse Factor
# RadMean = Mean of Radius Data    
# ChipMean = Mean of Chip Count Data 

T1 = 7 # sp.linspace(7.0, 7.2, 10) # Fixed Classification Value at 7
T2 = sp.linspace(0.058, 0.2, 10)
T3 = sp.linspace(0.44, 0.6, 10)

# Calculate Learning Paramenters, Minimize Cost Function --------------------------
# Initialize some Variables
h = []                              # Initial list for default append
# h =np.empty([0, 6])               # Used with Numpy Append
# h =np.empty([10*10*10*2*58, 6])   # Used with pre-allocated Numpy Array
II = range(0,len(InFileData))       # Iterative for input data
Cost = []                           # List of Cost for Each Trial
MinCost = 50000                     # Arbitary Initial Min Cost Comparison
RadMean = np.mean(AR)               # Mean of Radius Values
ChipMean = np.mean(AC)              # Mean of Chip Values
kk=0                                # Counter for pre-allocated Numpy Array
# Minimization Loop
# print(time.time() - start)
print('Loop Start Time:  ' + str(time.time() - start))
# for t1 in T1:                     # Used when Trials Varied T1
#    print(time.time() - start)     #   Must change indent to vary T1
t1 = T1                             # Constant t1 value
for t2 in T2:
    for t3 in T3:
        SubCost = []
        for ii in II:
            # z is predicting feature.  z = Average "radius" - (distance from feature
            #   to average feature value)
            z = t1 - np.sqrt(((InFileData[ii][0]-RadMean)/t2)**2 \
                + ((InFileData[ii][1]-ChipMean)/t3)**2 )
            # temp is prediction.  Near Zero = bad cookie, Near One = Good Cookie.
            temp = 1/(1+np.exp(-z))
            if InFileData[ii][2] == 1:
                tempcost = -np.log(temp)
                SubCost.append(tempcost)
            else:
                tempcost = -np.log(1-temp)
                SubCost.append(tempcost)
            # Default append (fastest)
            h.append([t1, t2, t3, temp, InFileData[ii][2], tempcost])
            # Numpy append (slow)
            # h = np.append(h, [[t1, t2, t3, temp, InFileData[ii][2], tempcost]], axis=0)
            # Numpy pre-allocated array (close second for speed)
            # h[kk, :] = [t1, t2, t3, temp, InFileData[ii][2], tempcost]
            kk = kk+1       # Counter for pre-allocated Numpy Array
        CurCost = sum(SubCost)  # Cost value for current trial
        Cost.append([t1, t2, t3, InFileData[ii][2], CurCost])
        if CurCost < MinCost:
            MinCost = CurCost
            MinIndex = [t1, t2, t3] ;

# Output Some Things    
print('Mean Cookie Radius:  ' + str(round(RadMean,2)))
print('Mean Chip Count:     ' + str(round(ChipMean,2)))
print('Minimum Cost:        ' + str(round(MinCost,2)))
print('Minimum Cost Index:')
print('  Classifying Value, Radius Elipse Factor, Chip Count Elipse Factor')
print('  ' + str(MinIndex))

plotvar = [h[ki][5] for ki in range(0, len(h))]
plt.plot(plotvar)
plt.title('All Error Values')
plt.figure()

# print('Cost Value for First 19 Cookies, No Sort')
# print(Cost[0:19])
YVar = [Cost[ki][4] for ki in range(0, len(Cost))]  # Cost for Trial
plt.plot(YVar, 'k+')
plt.title('Cost by Trial No Sort') 
plt.figure()

Cost.sort(key=lambda x: x[1]) # ----- Sort by Radius
# print('Cost Value for First 19 Cookies after Sort by Radius Elipse Factor')
# print(Cost[0:19])
XVar = [Cost[ki][1] for ki in range(0, len(Cost))]  # Radius Elipse Value
YVar = [Cost[ki][4] for ki in range(0, len(Cost))]  # Cost for Trial
plt.plot(XVar, YVar, 'b+')
plt.title('Cost by Trial Sort by Radius') 
plt.figure()

Cost.sort(key=lambda x: x[2]) # ----- Sort by Chip Count
# print('Cost Value for First 19 Cookies after Sort by Chip Count Elipse Factor')
# print(Cost[0:19])
XVar = [Cost[ki][2] for ki in range(0, len(Cost))]  # Chip Count Elipse Value
YVar = [Cost[ki][4] for ki in range(0, len(Cost))]  # Cost for Trial
plt.plot(XVar, YVar, 'r+')
plt.title('Cost by Trial Sort by Chip Count') 
plt.figure()

# Calculate Predicted Value for Input Data --------------------------------
Pred = []
PGR = []
PGC = []
PBR = []
PBC = []    
for ii in II:
    z = MinIndex[0] - np.sqrt(((InFileData[ii][0]-RadMean)/MinIndex[1])**2 \
        + ((InFileData[ii][1]-ChipMean)/MinIndex[2])**2 )
    # temp is prediction.  Near Zero = bad cookie, Near One = Good Cookie.
    temp = 1/(1+np.exp(-z))
    Pred.append(temp)
    if temp > 0.5:  # Radius and Chip count for Good Cookie Prediction > 0.5, Bad <= 0.5
        PGR.append(InFileData[ii][0])
        PGC.append(InFileData[ii][1])
    else:
        PBR.append(InFileData[ii][0])
        PBC.append(InFileData[ii][1])

# Print and plot some things    
print('Predicted Good Cookies:  ' + str(len(PGR)))
print('Predicted Bad Cookies:   ' + str(len(PBR)))
# print('List of Radius Values')
# print(AR)
# print('List of Number of Chip Values')
# print(AC)
# print('List of Predicted Scores for Each Point in Fit Model')
# print(Pred)
print('Total Run Time:  ' + str(time.time() - start))

# Plot Results ----------------------------------------------------------------

# TString = (SState + ' FitSlope=' + str(FitSlope) + ' MaxCases=' 
#            + str(MaxCases) + ' Lag=' + str(Lag) )
# plt.title(TString)

plt.plot(PGR, PGC, 'yo', label = 'Good')
plt.plot(PBR, PBC, 'ko', label = 'Bad')
plt.title('Cookie Quality Prediction')
plt.legend()
plt.figure()
plt.plot(GR, GC, 'b+', label = 'Good')
plt.plot(BR, BC, 'r+', label = 'Bad')
plt.title('Cookie Actual Defined Quality')
plt.legend()
plt.figure()
# plt.show()

plt.plot(PGR, PGC, 'yo', label = 'Good Pred')
plt.plot(PBR, PBC, 'ko', label = 'Bad Pred')
plt.plot(GR, GC, 'b+', label = 'Good Act')
plt.plot(BR, BC, 'r+', label = 'Bad Act')
plt.title('Cookie Quality')
plt.legend()
plt.show()

