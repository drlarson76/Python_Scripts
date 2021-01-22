# Concentration
##  Calculates and plots the concentration of an additive in a container over time
##  with equal input and output flow based on initial concentration
##  and input concentration.
##  22 Nov 2020 drl

import matplotlib.pylab as plt
import numpy as np

# Used in all cases
a = 0.1         # Flow rate as fraction of container capacity
NN = 50         # Number of iterations of fixed delta t

# Case 1.  Input is plain water.  Container has initial concentraion.
CInput = 0      # Input flow additive concentration
COutput = 1     # Intial additive concentration in container
Concentration = [COutput]   # Initialize list, container Concentration

for jj in range(0, NN):
    COutput = COutput*(1-a) + CInput*(a)
    Concentration.append(COutput)

plt.plot(Concentration)
plt.title('Case 1.  Plain water in.  Container starts with additive.') 
plt.figure()

# Case 2.  Input has constant concentration, container initially has
#            plain water.
CInput = 1      # Input flow additive concentration
COutput = 0     # Intial additive concentration in container
Concentration2 = [COutput]   # Initialize list, container Concentration

for jj in range(0, NN):
    COutput = COutput*(1-a) + CInput*(a)
    Concentration2.append(COutput)

plt.plot(Concentration2)
plt.title('Case 2.  Constant additive in.  Container starts with plain water.') 
plt.figure()

# Compare Case 1 and Case 2
MOnes = -1*np.ones(NN+1)
Concentration3 = np.array(Concentration) + np.array(Concentration2) + MOnes # Numpy arrays add element by element.
# Alternatively np.add will add lists element by element, but only 2 lists
# Concentration3 = np.add(Concentration, Concentration2)
# Concentration3 = np.add(Concentration3, MOnes)
plt.plot(Concentration3)
plt.title('Compare Case 1 and Case 2 Curve Shape') 
plt.figure()

# Case 3.  Input toggles between constant concentration as input and plain water,
#            container initially has plain water.

CInput = 1      # Input flow additive concentration
COutput = 0     # Intial additive concentration in container
Concentration = [COutput]   # Initialize list, container Concentration

for jj in range(0, NN):
    # CLast = CLast*(1-a)
    if jj % 2 == 0:
        COutput = COutput*(1-a) + CInput*(a)
    else:
        COutput = COutput*(1-a)
    Concentration.append(COutput)

plt.plot(Concentration)
plt.title('Case 3.  Input toggles between additive and no additive. \n Container starts with plain water.') 
plt.show()
