# Concentration
##Finds the concentration of an additive in a container
##with equal input and output flow based on initial concentration
##and input concentration.
##22 Nov 2020 drl

import matplotlib.pylab as plt
import numpy as np

# Case 1.  Input is plain water.  Container has initial concentraion.
CInput = 0      # Input flow concentration
COutput = 1     # Intial concentration in container
C = [COutput]   # Initialize list
a = 0.1         # Flow rate as fraction of container capacity
NN = 50         # Number of iterations of fixed delta t

for jj in range(0, NN):
    COutput = COutput*(1-a) + CInput*(a)
    C.append(COutput)


plt.plot(C)
plt.title('Case 1.  Plain water in.  Container starts with additive.') 
plt.figure()

# Case 2.  Input has constant concentration, container initially has
#            plain water.
CInput = 1
COutput = 0
C2 = [COutput]
# a = 0.1

for jj in range(0, NN):
    # CLast = CLast*(1-a)
    COutput = COutput*(1-a) + CInput*(a)
    C2.append(COutput)

plt.plot(C2)
plt.title('Case 2.  Constant additive in.  Container starts with plain water.') 
plt.figure()

# Compare Case 1 and Case 2
MOnes = -1*np.ones(NN+1)
C3 = np.array(C) + np.array(C2) + MOnes # Numpy arrays add element by element.
# Alternatively np.add will add lists element by element, but only 2 lists
# C3 = np.add(C, C2)
# C3 = np.add(C3, MOnes)
plt.plot(C3)
plt.title('Compare Case 1 and Case 2 Curve Shape') 
plt.figure()



CInput = 1
COutput = 0
C = [COutput]
# a = 0.1

# Case 3.  Input toggles between constant concentration and plain water,
#            container initially has plain water.
for jj in range(0, NN):
    # CLast = CLast*(1-a)
    if jj % 2 == 0:
        COutput = COutput*(1-a) + CInput*(a)
    else:
        COutput = COutput*(1-a)
    C.append(COutput)

plt.plot(C)
plt.title('Case 3.  Input toggles between additive and no additive. \n Container starts with plain water.') 
plt.show()
