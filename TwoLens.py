# TwoLens
# Find image positions and magnifications of 2 Lens SystemError
#
# C:\DaveL\Technical\MyPyScripts\TwoLens
#
#
# 8/1/2020 David Larson

# Set Up Variables
O1 = 3000     # Object Distance Lens 1
F1 = 52   # Focal Length Lens 1
# I1        # Image Distance Lens 1
# M1        # Magnification Lens 1
d = 3      # Distance between Lens 1 and Lens 2
# O2        # Object Distance Lens 2
F2 = 1000000   # Focal Length Lens 2
# I2        # Image Distance Lens 2
# M2        # Magnification Lens 2
# ITotal    # Image Position Relative to Lens 1
# MTotal    # Total Magnification
OSize = 1800    # Object Size
# ISize         # Image Size

# Lens 1 Calculations
I1 = (O1*F1)/(O1 - F1)
M1 = -I1/O1

# Lens 2 Calculations
O2 = d - I1  # I1 - d
I2 = (O2*F2)/(O2 - F2)
M2 = -I2/O2

# Final Position and Magnfication
ITotal = d + I2
MTotal = M1*M2
ISize = MTotal*OSize

# Print Some Things
print('O1:  ' + str(round(O1,2)))
print('F1:  ' + str(round(F1,2)))
print('I1:  ' + str(round(I1,2)))
print('M1:  ' + str(round(M1,5)))
print(' ')
print('d:   ' + str(round(d,2)))
print('O2:  ' + str(round(O2,2)))
print('F2:  ' + str(round(F2,2)))
print('I2:  ' + str(round(I2,2)))
print('M2:  ' + str(round(M2,5)))
print(' ')
print('ITotal:        ' + str(round(ITotal,2)))
print('MTotal:        ' + str(round(MTotal,5)))
print('OSize:         ' + str(round(OSize,5)))
print('ISize:         ' + str(round(ISize,5)))


