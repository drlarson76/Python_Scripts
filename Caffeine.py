# Caffeine
#
#   Calculates caffiene in a person's system based on caffiene half life of 5 hours.
#
#   22 Jan 2021 Dave Larson


import matplotlib.pylab as plt
import numpy as np

# Half Life Formula
# N = N0 * (1/2) ^ (t/half_life)
Half_Life = float(5) # Caffeine Half Life in Hours

# Case A:  2 100 mg pills------------------
Case_Label = '2 Pills'
Dose1 = 100
First_Dose = 7 # am
Dose1_Label = 'Pill ' + str(Dose1) + ' mg'
Dose2 = 100
Dose_2_Delay = 7
Dose2_Label = 'Pill ' + str(Dose2) + ' mg'
Dose3 = 0
Dose_3_Delay = 13
Dose3_Label = 'No 3rd Intake ' + str(Dose3) + ' mg'
Remaining01 = []
Remaining02 = []
Remaining03 = []
Remaining = []
Time_List = []
Ticks_List = []

for jj in range(0, 24):
    Elasped_Time = float(jj)
    # Time_List.append(jj+First_Dose)
    Time_List.append(jj)
    if jj < 24-First_Dose:
        Ticks_List.append(jj+First_Dose)
    else:
        Ticks_List.append(jj+First_Dose - 24)
    Remaining01.append(Dose1 * (1/2) ** (Elasped_Time/Half_Life))
    if Elasped_Time < Dose_2_Delay:
        Remaining02.append(0)
    else:
        Remaining02.append(Dose2 * (1/2) ** ((Elasped_Time-Dose_2_Delay)/Half_Life))
    if Elasped_Time < Dose_3_Delay:
        Remaining03.append(0)
    else:
        Remaining03.append(Dose3 * (1/2) ** ((Elasped_Time-Dose_3_Delay)/Half_Life))

Remaining = np.add(Remaining01, Remaining02)
Remaining = np.add(Remaining, Remaining03)
Remain_10pm = round(Remaining[20-First_Dose],1)

Remaining_A = Remaining
Remain_10pm_A= Remain_10pm
Case_Label_A = Case_Label

plt.plot(Time_List, Remaining01, label = Dose1_Label)
plt.plot(Time_List, Remaining02, label = Dose2_Label)
plt.plot(Time_List, Remaining03, label = Dose3_Label)
plt.plot(Time_List, Remaining, label = 'Total')
plt.xticks(Time_List, Ticks_List)
plt.xlim(0,24)
plt.legend()
plt.xlabel('Time of Day')
plt.ylabel('mg of Caffeine in System')
TString = 'Caffeine in System. Intake = ' + Case_Label + '.\n' + str(Remain_10pm) + ' mg remains at 10 pm'
plt.title(TString)
plt.figure()



# Case B:  1 Pill, 2 tea ------------------
Case_Label = '1 Pill, 2 tea'
Dose1 = 100
First_Dose = 7 # am
Dose1_Label = 'Pill ' + str(Dose1) + ' mg'
Dose2 = 35
Dose_2_Delay = 4
Dose2_Label = 'Green Tea ' + str(Dose2) + ' mg'
Dose3 = 35
Dose_3_Delay = 7
Dose3_Label = 'Greem Tea ' + str(Dose3) + ' mg'
Remaining01 = []
Remaining02 = []
Remaining03 = []
Remaining = []
Time_List = []
Ticks_List = []

for jj in range(0, 24):
    Elasped_Time = float(jj)
    # Time_List.append(jj+First_Dose)
    Time_List.append(jj)
    if jj < 24-First_Dose:
        Ticks_List.append(jj+First_Dose)
    else:
        Ticks_List.append(jj+First_Dose - 24)
    Remaining01.append(Dose1 * (1/2) ** (Elasped_Time/Half_Life))
    if Elasped_Time < Dose_2_Delay:
        Remaining02.append(0)
    else:
        Remaining02.append(Dose2 * (1/2) ** ((Elasped_Time-Dose_2_Delay)/Half_Life))
    if Elasped_Time < Dose_3_Delay:
        Remaining03.append(0)
    else:
        Remaining03.append(Dose3 * (1/2) ** ((Elasped_Time-Dose_3_Delay)/Half_Life))

Remaining = np.add(Remaining01, Remaining02)
Remaining = np.add(Remaining, Remaining03)
Remain_10pm = round(Remaining[20-First_Dose],1)

Remaining_B = Remaining
Remain_10pm_B = Remain_10pm
Case_Label_B = Case_Label

plt.plot(Time_List, Remaining01, label = Dose1_Label)
plt.plot(Time_List, Remaining02, label = Dose2_Label)
plt.plot(Time_List, Remaining03, label = Dose3_Label)
plt.plot(Time_List, Remaining, label = 'Total')
plt.xticks(Time_List, Ticks_List)
# plt.xlim(0,24)
plt.legend()
plt.xlabel('Time of Day')
plt.ylabel('mg of Caffeine in System')
TString = 'Caffeine in System. Intake = ' + Case_Label + '.\n' + str(Remain_10pm) + ' mg remains at 10 pm'
plt.title(TString)
plt.figure()
    
# Case C: 1 Pill, 1 Tea, 1 Mt Dew ------------------
Case_Label = '1 Pill, 1 tea, 1 Mt Dew'
Dose1 = 100
First_Dose = 7 # am
Dose1_Label = 'Pill ' + str(Dose1) + ' mg'
Dose2 = 35
Dose_2_Delay = 7
Dose2_Label = 'Green Tea ' + str(Dose2) + ' mg'
Dose3 = 55
Dose_3_Delay = 11
Dose3_Label = 'Mt Dew ' + str(Dose3) + ' mg'
Remaining01 = []
Remaining02 = []
Remaining03 = []
Remaining = []
Time_List = []
Ticks_List = []

for jj in range(0, 24):
    Elasped_Time = float(jj)
    # Time_List.append(jj+First_Dose)
    Time_List.append(jj)
    if jj < 24-First_Dose:
        Ticks_List.append(jj+First_Dose)
    else:
        Ticks_List.append(jj+First_Dose - 24)
    Remaining01.append(Dose1 * (1/2) ** (Elasped_Time/Half_Life))
    if Elasped_Time < Dose_2_Delay:
        Remaining02.append(0)
    else:
        Remaining02.append(Dose2 * (1/2) ** ((Elasped_Time-Dose_2_Delay)/Half_Life))
    if Elasped_Time < Dose_3_Delay:
        Remaining03.append(0)
    else:
        Remaining03.append(Dose3 * (1/2) ** ((Elasped_Time-Dose_3_Delay)/Half_Life))

Remaining = np.add(Remaining01, Remaining02)
Remaining = np.add(Remaining, Remaining03)
Remain_10pm = round(Remaining[20-First_Dose],1)

Remaining_C = Remaining
Remain_10pm_C = Remain_10pm
Case_Label_C = Case_Label

plt.plot(Time_List, Remaining01, label = Dose1_Label)
plt.plot(Time_List, Remaining02, label = Dose2_Label)
plt.plot(Time_List, Remaining03, label = Dose3_Label)
plt.plot(Time_List, Remaining, label = 'Total')
plt.xticks(Time_List, Ticks_List)
# plt.xlim(0,24)
plt.legend()
plt.xlabel('Time of Day')
plt.ylabel('mg of Caffeine in System')
TString = 'Caffeine in System. Intake = ' + Case_Label + '.\n' + str(Remain_10pm) + ' mg remains at 10 pm'
plt.title(TString)
plt.figure()
    
    
# Case D: 1 Tea, 1 Tea, 1 Tea ------------------
Case_Label = '1 Tea, 1 Tea, 1 Tea'
Dose1 = 35
First_Dose = 7 # am
Dose1_Label = 'Green Tea ' + str(Dose1) + ' mg'
Dose2 = 35
Dose_2_Delay = 7
Dose2_Label = 'Green Tea ' + str(Dose2) + ' mg'
Dose3 = 35
Dose_3_Delay = 9
Dose3_Label = 'Green Tea ' + str(Dose3) + ' mg'
Remaining01 = []
Remaining02 = []
Remaining03 = []
Remaining = []
Time_List = []
Ticks_List = []

for jj in range(0, 24):
    Elasped_Time = float(jj)
    # Time_List.append(jj+First_Dose)
    Time_List.append(jj)
    if jj < 24-First_Dose:
        Ticks_List.append(jj+First_Dose)
    else:
        Ticks_List.append(jj+First_Dose - 24)
    Remaining01.append(Dose1 * (1/2) ** (Elasped_Time/Half_Life))
    if Elasped_Time < Dose_2_Delay:
        Remaining02.append(0)
    else:
        Remaining02.append(Dose2 * (1/2) ** ((Elasped_Time-Dose_2_Delay)/Half_Life))
    if Elasped_Time < Dose_3_Delay:
        Remaining03.append(0)
    else:
        Remaining03.append(Dose3 * (1/2) ** ((Elasped_Time-Dose_3_Delay)/Half_Life))

Remaining = np.add(Remaining01, Remaining02)
Remaining = np.add(Remaining, Remaining03)
Remain_10pm = round(Remaining[20-First_Dose],1)

Remaining_D = Remaining
Remain_10pm_D = Remain_10pm
Case_Label_D = Case_Label

plt.plot(Time_List, Remaining01, label = Dose1_Label)
plt.plot(Time_List, Remaining02, label = Dose2_Label)
plt.plot(Time_List, Remaining03, label = Dose3_Label)
plt.plot(Time_List, Remaining, label = 'Total')
plt.xticks(Time_List, Ticks_List)
# plt.xlim(0,24)
plt.legend()
plt.xlabel('Time of Day')
plt.ylabel('mg of Caffeine in System')
TString = 'Caffeine in System. Intake = ' + Case_Label + '.\n' + str(Remain_10pm) + ' mg remains at 10 pm'
plt.title(TString)
plt.figure()

# Plot Case Results    
plt.plot(Time_List, Remaining_A, label = Case_Label_A)
plt.plot(Time_List, Remaining_B, label = Case_Label_B)
plt.plot(Time_List, Remaining_C, label = Case_Label_C)
plt.plot(Time_List, Remaining_D, label = Case_Label_D)
plt.xticks(Time_List, Ticks_List)
# plt.xlim(0,24)
plt.legend()
plt.xlabel('Time of Day')
plt.ylabel('mg of Caffeine in System')
TString = 'Caffeine in System. Four Cases.\nmg remaining at 10 pm ' \
    + ' A = ' + str(Remain_10pm_A) \
    + ' B = ' + str(Remain_10pm_B) \
    + ' C = ' + str(Remain_10pm_C) \
    + ' D = ' + str(Remain_10pm_D)
plt.title(TString)
plt.show()
