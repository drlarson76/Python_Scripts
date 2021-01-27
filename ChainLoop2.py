# ChainLoop2
# 2/2/2020 drl

import scipy as sp
import matplotlib.pylab as plt
import numpy as np
# import math
import time
start = time.time()

# DeltaM* G = T*cos(theta) 
# DeltaM = x*M   x: (1,0)  = (1-y)/L
# x*M*G = T*cos(theta)
# x = (T/MG)*cos(theta)
# theta = arccos(x*MG/T) = arccos(x/TMG)
# Catenary y = a*cosh(x/a).  Wikipedia
#   x measured from lowest point
#   a = Th/(Lambda*H)
#   Th = horizontal force
#   Lambda mass per unit length
#   H = Seperation of supports

L = 600 # Length of chain/2, intial L
SuspHt = 180 # Height of suspension
MinTarg = 20 # Target of loop minimum
ErrTarg = 0.01 # Maximum Error to MinTarg
TMG = 1.5 # Tension on chain/(mass*gravity)
N = 100 # Number of Increments
NErrTarg = 0.01 # Max Error Due to Number of intervals
DelL = L/N # Delta in Step 

# Determine L given T ------------------------------------
print(' ')
print(' ')
print('Start Step 1 ------------------------')
LGuess = L
MaxLoop = 100
ML = 0
ErrEst = ErrTarg*1.1
while np.abs(ErrEst) > ErrTarg:
    ML = ML+1
    DelL = LGuess/N
    x = sp.linspace(1, 0, N+1)
    # theta = np.arccos(x/TMG)
    theta = 1/np.arctan(x/TMG)
    CosTheta = x/TMG 
    SinTheta = np.sin(theta)
    # print(theta)
    # print(theta*(180/np.pi))
    # print(CosTheta)
    # print(SinTheta)

    XSum = SinTheta[0]*DelL
    YSum = CosTheta[0]*DelL
    XPos = XSum
    YPos = YSum
    for t in range(1, N+1):
        XSum = XSum + SinTheta[t]*DelL
        YSum = YSum - CosTheta[t]*DelL
        XPos = np.append(XPos,XSum)
        YPos = np.append(YPos,YSum)

    XPos = np.append(0, XPos)
    YPos = np.append(2*CosTheta[0]*DelL, YPos)

    YMax = np.max(YPos)
    YPos2 = SuspHt+YPos-YMax
    Y2Min = np.min(YPos2)
    print(Y2Min)
    ErrEst = Y2Min - MinTarg 
    LGuess = LGuess + ErrEst
    if ML > MaxLoop:
        break

print(ML)
# print('Position')
# print(XPos)
# print(YPos)

plt.plot(XPos, YPos2)
plt.figure()
# print(time.time() - start)

# Determine N for necessary resolution ---------------------------
print(' ')
print(' ')
print('Start Step 2 ------------------------')
# LGuess = L
NGuess = 2*N
MaxLoop = 100
ML = 0
ErrEst = NErrTarg*1.1
while np.abs(ErrEst) > NErrTarg:
    CurY2Min = Y2Min
    ML = ML+1
    DelL = LGuess/NGuess
    x = sp.linspace(1, 0, NGuess+1)
    theta = np.arccos(x/TMG)
    CosTheta = x/TMG 
    SinTheta = np.sin(theta)
    # print(theta)
    # print(theta*(180/np.pi))
    # print(CosTheta)
    # print(SinTheta)

    XSum = SinTheta[0]*DelL
    YSum = CosTheta[0]*DelL
    XPos = XSum
    YPos = YSum
    for t in range(1, NGuess+1):
        XSum = XSum + SinTheta[t]*DelL
        YSum = YSum - CosTheta[t]*DelL
        XPos = np.append(XPos,XSum)
        YPos = np.append(YPos,YSum)

    XPos = np.append(0, XPos)
    YPos = np.append(2*CosTheta[0]*DelL, YPos)

    YMax = np.max(YPos)
    YPos2 = SuspHt+YPos-YMax
    Y2Min = np.min(YPos2)
    print('NGuess, ErrEst, NFactor')
    print(NGuess)
    ErrEst = Y2Min - CurY2Min 
    print(ErrEst)
    NFactor = np.abs(ErrEst/NErrTarg)
    if NFactor > 2:
        NFactor = 2
    print(NFactor)
    NGuess = np.int(np.floor(NGuess*NFactor))
    if NGuess > 100000:
        print('Loop Over 100,000')
        print(NGuess)
        break
    if ML > MaxLoop:
        break

print('ML, Y2Min')    
print(ML)
print(Y2Min)
print(time.time() - start)
# print('Position')
# print(XPos)
# print(YPos)

# plt.plot(XPos, YPos2)
# plt.figure()

# Determine L given T with Intervals Small enough to guarentee max error
print(' ')
print(' ')
print('Start Step 3 ------------------------')
LGuess = L
MaxLoop = 100
ML = 0
ErrEst = ErrTarg*1.1
N = NGuess
print('Y2Min')
while np.abs(ErrEst) > ErrTarg:
    ML = ML+1
    DelL = LGuess/N
    x = sp.linspace(1, 0, N+1)
    theta = np.arccos(x/TMG)
    CosTheta = x/TMG 
    SinTheta = np.sin(theta)
    # print(theta)
    # print(theta*(180/np.pi))
    # print(CosTheta)
    # print(SinTheta)

    XSum = SinTheta[0]*DelL
    YSum = CosTheta[0]*DelL
    XPos = XSum
    YPos = YSum
    for t in range(1, N+1):
        XSum = XSum + SinTheta[t]*DelL
        YSum = YSum - CosTheta[t]*DelL
        XPos = np.append(XPos,XSum)
        YPos = np.append(YPos,YSum)

    XPos = np.append(0, XPos)
    YPos = np.append(2*CosTheta[0]*DelL, YPos)

    YMax = np.max(YPos)
    YPos2 = SuspHt+YPos-YMax
    Y2Min = np.min(YPos2)
    print(Y2Min)
    ErrEst = Y2Min - MinTarg 
    LGuess = LGuess + ErrEst
    if ML > MaxLoop:
        break

print('ML, Y2Min')    
print(ML)
print(Y2Min)
print('Distance Between Supports')
print(2*XSum)
print('T/MG, LGuess, DelL')
print(TMG)
print(LGuess)
print(DelL)
print('NGuess')
print(NGuess)
# print('Position')
# print(XPos)
# print(YPos)
# print('Elapsed Time')
# print(time.time() - start)

# plt.plot(XPos, YPos2)
# plt.figure()

# Theoretical Fit ---------------------------------------------
print(' ')
print(' ')
print('Start Step 4 ------------------------')
# Catenary y = a*cosh(x/a).  Wikipedia
#   a = TMG

CFac = 0.9
yc = CFac*TMG*LGuess*np.cosh(XPos/(CFac*TMG*LGuess))
yc2 = yc[::-1]
MaxYC2 = np.max(yc2)
yc3 = 180+yc2-MaxYC2 

plt.plot(XPos, yc3, 'r')
plt.plot(XPos, YPos2, 'k')
plt.show()







