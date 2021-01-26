# InternetMonitorData10
#

##01/20/2021 InternetMonitorData10
##  x Finish Function-izing
##  Add Comments
##  x Add Ping_Bad_Limit, Sleep_per_Loop, and Start Time to Output file
##  x Put output files in some directory
##01/15/2021 InternetMonitorData9
##  Convert to structured programming.
##      Function for writing to file.  Write to file normal and write to file error.
##      Function for Duplicate actions for Internet and Router Pings
##      Fix Plot to not have if and/or convert to function
##01/14/2021 InternetMonitorData8
##  If current event on CTRL-C, write to file before end time and closing.
##  Write current even at end of loop, fixes 01/12 comment
##01/13/2021 InternetMonitorData7
##  Add time classification:  Day (8-5), Evening (5-12), Night (12-8)
##  Add file Overwrite protection
##  Add end time to exit in CTRL-C
##01/12/2021 InternetMonitorData6
##  Add start/stop to saved data file
##  Write file after each Bad Event 
##  Print info if bad pings go over 60
##  ** Won't write last event if last ping in loop is bad **
##01/11/2021 InternetMonitorData5
##  Save Outage Data
##  Exit Gracefully:  Close data file on ineterupt.
##01/11/2021 InternetMonitorData4
##  Added duration of Bad events
##11/23/2020 InternetMonitorData2
##  Checks for time out (= -10) and unreachable (= -20)
##  Forms list of internet and router ping times
##  Continuously plots last NPlot of internet ping times
##11/20/2020 InternetMonitorData
##  Pings internet and router

import subprocess
import matplotlib.pylab as plt
import time
import datetime
import csv
import math
import signal
import sys 
import os
import os.path

# User Set up values, these are global defined outside the functions.
NN = 60     # Number of pings
NPlot = 30  # Number of most recent pings to plot
Ping_Bad_Limit = 200    # in milliseconds (ms)
Ping_Event_Files = 'C:\\DaveL\\Technical\\MyPyScripts\\Ping_Event_Files\\'
Outage_File_Name = 'Outage0126_Temp06.csv'
Sleep_per_Loop = 0.1    # Seconds.  Script uses little/no CPU with 2 seconds
Show_Continuous_Ping_Plot = True
G_IP =  '8.8.4.4'           # Google IP Address
##G_IP = '157.157.157.157'  # Times out Test Address
##G_IP = '192.168.1.5'      # Unreachable Test Address
R_IP = '192.168.1.1'        # Router IP Address
##R_IP = '192.168.254.254'  # Alex Router IP Address
##R_IP = '192.168.1.6'      # PC IP Address



# Initialize Output File and Start Time
def Initilize_Output_File():
    # Single needed input variable is global use input:  Outage_File_Name
    if not os.path.isfile(Ping_Event_Files + Outage_File_Name):
        with open(Ping_Event_Files + Outage_File_Name, mode='w', newline='') as Outage_file:
            Outage_writer = csv.writer(Outage_file)
            Outage_writer.writerow(['Type', 'Date', 'Time', 'TOD', 'Duration', 'Ping Count', \
                'Worst Code', 'Max Ping', 'Down Time', 'Up Time', 'Monitor Time', \
                'Ping Bad Limit', 'Sleep per Loop', 'Start Time'])
            # File closes at end of WITH
    else:
        print('File ' + Ping_Event_Files + Outage_File_Name + ' exists.  Use different file name.')
        sys.exit(0)

    Outage_file = open(Ping_Event_Files + Outage_File_Name, mode='a', newline='')  # Re-open for append in loop.
    Outage_CSV = csv.writer(Outage_file)

    dtc = datetime.datetime.now()
    print('Start Time ' + dtc.strftime("%Y-%m-%d %H:%M:%S"))

    Outage_Row = ['Start', dtc.strftime("%Y-%m-%d"), dtc.strftime("%H:%M:%S"), '', '', \
        '', '', '',  str(0), str(0), str(0), \
        '', '', '']
    Outage_CSV.writerow(Outage_Row)
    # Write buffered lines to file
    Outage_file.flush()
    os.fsync(Outage_file.fileno())
    return(Outage_file, Outage_CSV)

def Classify_Ping_Response(Ping_String, Ping_Source, Bad_Limit, Loop_Count):
    if Ping_String.find('out') > 0:     # Timed Out = -10
        Ping_Time = -10
        Last_Was_Bad = True
        Bad_Code = 1 # 'Timed Out'
    elif Ping_String.find('unreachable') > 0:   # Unreachable = -20
        Ping_Time = -20
        Last_Was_Bad = True
        Bad_Code = 2
    elif Ping_String.find('General failure') > 0:   # General failure = -30
        Ping_Time = -30
        Last_Was_Bad = True
        Bad_Code = 3
    elif Ping_String.find('time=') > 0:     # Ping time returned
        Istart = Ping_String.find('time', 50, 150) + 5
        Iend = Ping_String.find('ms', 50, 150)
        Ping_Time = int(Ping_String[Istart:Iend]) # Internet ping time in ms
        Bad_Code = 0
        if Ping_Time >= Bad_Limit:
            Last_Was_Bad = True
        else:
            Last_Was_Bad = False
    else:
        print(Ping_Source + ':  Some funky error in ' + Ping_Source + ' string.  Loop = ', str(Loop_Count))
        print(Ping_String)
        Ping_Time = -40       # Unknown Failure
        Last_Was_Bad = True
        Bad_Code = 4
    return(Ping_Time, Last_Was_Bad, Bad_Code)

def Continuous_Plot(YMax, ITime, RTime, Ims, Rms, NN, jj):
        # YMax = max(YMax, Ims, Rms)
        # YMax = min(YMax, 500)
        plt.plot(ITime[max(0,(jj-NPlot)): jj], label= 'Google')
        plt.ylim([-35,YMax])
        plt.xticks(range(0, NPlot, 2))
        plt.draw()

        # plt.plot(RTime[(jj-NPlot): jj], label = 'Router')
        plt.plot(RTime[max(0,(jj-NPlot)): jj], label = 'Router')
        plt.ylim([-35,YMax])
        plt.xticks(range(0, NPlot, 2))
        TString = 'Loop ' + str(jj) + ' of ' + str(NN) \
            + '\nLast Values Google = ' + str(Ims) + ' Router = ' + str(Rms)
        plt.title(TString)
        plt.legend()
        # Supposed to put it into the upper left corner for example:
        plt.draw()
        mngr = plt.get_current_fig_manager()
        mngr.window.wm_geometry('640x514+500+100')
        plt.pause(0.0001)
        plt.clf()

def Exit_gracefully(signal, frame):     # Called by signal.signal() on CTRL-C
    Write_Last_Entries_And_Close('Interupt')
    sys.exit(0)

def Write_Last_Entries_And_Close(Called_By):
    dtc = datetime.datetime.now()
    # Only input method to this function for CTRL-C through Exit_gracefully()
    #   using signal.signal() is using global variables.
    Outage_file     = Global_Var_List[0] # Output file FID.  Global in user input.
    Outage_CSV      = Global_Var_List[1] # CSV handle
    TOD_Labels      = Global_Var_List[2] #
    TOD             = Global_Var_List[3] #
    Bad_Duration    = Global_Var_List[4] #
    Bad_Count       = Global_Var_List[5] #
    Code_Labels     = Global_Var_List[6] #
    Last_Bad_Code   = Global_Var_List[7] #
    Last_Bad_Ping   = Global_Var_List[8] #
    Cum_Down_Time   = Global_Var_List[9] #
    Module_Start    = Global_Var_List[10] #
    Bad_Start       = Global_Var_List[11] #
    Bad_End         = Global_Var_List[12] #
    Last_Minus_2_Was_Bad = Global_Var_List[13] #
    Ping_Bad_Limit  = Global_Var_List[14] # 
    Sleep_per_Loop  = Global_Var_List[15] #
    Start_Time      = Global_Var_List[16] #

    if Last_Minus_2_Was_Bad:    # In the middle of a bad event when CTRL-C or end of Loop
                                #   Update down time, write event to output file.
        print('Bad at end of Loop')
        Bad_Duration = round(Bad_End - Bad_Start, 1)
        Cum_Down_Time_Exit = round(Cum_Down_Time + Bad_Duration, 1) # Local Variable
        Bad_Tot_Counts = Bad_Count
        Event_End = round(time.time() - Module_Start, 1)
        Up_Time = round(Event_End - Cum_Down_Time_Exit, 1)
        Outage_Row = ['Bad', dtc.strftime("%Y-%m-%d"), dtc.strftime("%H:%M:%S"), TOD_Labels[TOD], str(Bad_Duration), \
            str(Bad_Tot_Counts), Code_Labels[Last_Bad_Code], str(Last_Bad_Ping), \
            str(Cum_Down_Time_Exit), str(Up_Time), str(Event_End), \
            str(Ping_Bad_Limit), str(Sleep_per_Loop), Start_Time]
        Outage_CSV.writerow(Outage_Row)
    else:
        Cum_Down_Time_Exit = Cum_Down_Time  # No addition to down time.
    
    # Write End Time and duration information to file
    Module_Duration =  round(time.time() - Module_Start, 1)
    Up_Time = round(Module_Duration - Cum_Down_Time_Exit, 1)
    Outage_Row = ['End', dtc.strftime("%Y-%m-%d"), dtc.strftime("%H:%M:%S"), '', '', \
        '', '', '', \
        str(Cum_Down_Time_Exit), str(Up_Time), str(Module_Duration), \
        '', '', '']
    Outage_CSV.writerow(Outage_Row)

    # Close file
    Outage_file.close()
    
    # Print End Time
    dtc = datetime.datetime.now()
    print('End Time ' + dtc.strftime("%Y-%m-%d %H:%M:%S"))

    # Leave plot open for several seconds
    if Called_By == 'Normal':
        time.sleep(5)
    elif Called_By == 'Interupt':
        print('Ended by CTRL-C')


### Main Routine -------------------------
        ## Determine Duration of Bad Event and Write Event to File, use internet ping only
        ## This section is a switch statement determined by whether the event was bad
        ##      and whether there was at leat 2 bad events consecutively.
        ##      Ignores good pings.  Ignores a single bad ping response.
        ##      Accumulates duration and information on bad events of 2 or more ping
        ##      duration.  Treats any string of consecutive bad pings as a single event.
        ##      I.E., until the first occurrence of a good ping after a string of bad pings.
def Main_Program():
    # Initialize some things
    Module_Start = time.time()
    ITime = []  # Internet ping times list
    RTime = []  # Router ping times list
    plt.ion()   # MatPlotLib interactive 'on' for continuous ping time plotting
    YMax = 200  # Default plot Y maximum
    Ims = 0
    Rms = 0
    Last_Was_Bad = False
    Last_Minus_2_Was_Bad = False 
    Bad_Count = 0
    Bad_Code = 0
    Last_Bad_Code = 0
    Last_Bad_Ping = 0
    Cum_Down_Time = 0
    Code_Labels = ['None', 'Timed Out', 'Unreachable', 'General Failure', 'Unknown Failure']
    TOD_Labels = ['Night', 'Day', 'Evening']
    dtc = datetime.datetime.now()
    Start_Time = dtc.strftime("%Y-%m-%d %H:%M:%S")
    
    # Initialize Output File.  Get FID and CSV Handle.
    Outage_file, Outage_CSV = Initilize_Output_File()

    global Global_Var_List
    # # Global Vars needed for Exit_gracefully
    # Outage_file   # Output file FID.  Global in user input.
    # Outage_CSV    # CSV handle
    # TOD_Labels:   Already defined.
    TOD = 0
    Bad_Duration = 0
    # Bad_Count:    Already defined.
    # Code_Labels:  Already defined.
    # Last_Bad_Code:  Already defined.
    # Last_Bad_Ping:  Already defined.
    # Cum_Down_Time:  Already defined.
    # Module_Start:  Already defined.
    Bad_Start = 0
    Bad_End = 0
    # Last_Minus_2_Was_Bad
    # Global_Var_List =  [Outage_file,        Outage_CSV,     TOD_Labels,     TOD, \
                        # Bad_Duration,       Bad_Count,      Code_Labels,    Last_Bad_Code, \
                        # Last_Bad_Ping,      Cum_Down_Time,  Module_Start,   Bad_Start, \
                        # Bad_End,            Last_Minus_2_Was_Bad ]
    
    # This is the Main routine, doing pings, parsing and classifying responses, making
    #   ping time lists, making bad event duration items.
    for jj in range(0, NN):
        time.sleep(Sleep_per_Loop)
        time.sleep(0.05)    # Minimum Ping Seperation
        dtc = datetime.datetime.now()
        if dtc.hour < 8:  # Night
            TOD = 0
        elif dtc.hour <= 17:  # Day
            TOD = 1
        else:
            TOD = 2  # Evening
        if jj/450 == math.floor(jj/450):
            print('Loop Count = ' + str(jj) + ' of ' + str(NN) + '  ' + dtc.strftime("%Y-%m-%d %H:%M:%S"))
        # Ping Internet and Router
        Iout = subprocess.Popen('ping ' + G_IP + ' -n 1', stdout=subprocess.PIPE, shell=True)
        (internetout, Ierr) = Iout.communicate()
        time.sleep(0.05)    # Seperate Pings
        Rout = subprocess.Popen('ping ' + R_IP + ' -n 1', stdout=subprocess.PIPE, shell=True)
        (routerout, Rerr) = Rout.communicate()

        # Strip ping Information line from subprocess output
        Istring = internetout.decode('utf8')
        Rstring = routerout.decode('utf8')

        # Parse strings, classify ping response
        # Internet ping time 
        Last_Was_Bad = False 
        Ims, Last_Was_Bad, Bad_Code = Classify_Ping_Response(Istring, 'Internet', Ping_Bad_Limit, jj)
        ITime.append(Ims)
        # Router ping time
        Rms, Not_Used01, Not_Used02 = Classify_Ping_Response(Rstring, 'Router', Ping_Bad_Limit, jj)
        RTime.append(Rms)

        ## Determine Duration of Bad Event and Write Event to File, use internet ping only
        ## This section is a switch statement determined by whether the event was bad
        ##      and whether there was at leat 2 bad events consecutively.
        ##      Ignores good pings.  Ignores a single bad ping response.
        ##      Accumulates duration and information on bad events of 2 or more ping
        ##      duration.  Treats any string of consecutive bad pings as a single event.
        ##      I.E., until the first occurrence of a good ping after a string of bad pings.
        if Last_Was_Bad and not Last_Minus_2_Was_Bad:  # First Bad Ping
            Bad_Start = time.time()
            Bad_Count = Bad_Count + 1 
            Last_Bad_Code = max(Last_Bad_Code, Bad_Code)
            Last_Bad_Ping = max(Ims, Last_Bad_Ping)
            Last_Minus_2_Was_Bad = True

        elif Last_Was_Bad and Last_Minus_2_Was_Bad:  # Consecutive Bad Pings
            Bad_End = time.time()
            Bad_Count = Bad_Count + 1 
            Last_Bad_Code = max(Last_Bad_Code, Bad_Code)
            Last_Bad_Ping = max(Ims, Last_Bad_Ping)
            Last_Minus_2_Was_Bad = True
            
            # Print some information if bad pings are running on and on
            if Bad_Count/60 == math.floor(Bad_Count/60):
                 print('Ongoing Bad Pings = ' + str(Bad_Count) + '  ' \
                 + ' Worst Code = ' + Code_Labels[Last_Bad_Code] \
                 + ' Worst Ping = ' + str(Last_Bad_Ping) )

        elif not Last_Was_Bad and Last_Minus_2_Was_Bad and Bad_Count == 1 :  # only 1 bad ping, ignore
            Last_Minus_2_Was_Bad = False
            Last_Bad_Code = 0
            Bad_Code = 0
            Last_Bad_Ping = 0
            Bad_Count = 0

        elif not Last_Was_Bad and Last_Minus_2_Was_Bad:  # First good ping after bad ping(s)
            # Determine and print bad ping sequence information  
            Bad_Duration = round(Bad_End - Bad_Start, 1)
            Bad_Tot_Counts = Bad_Count
            Cum_Down_Time = round(Cum_Down_Time + Bad_Duration, 1)
            Event_End = round(time.time() - Module_Start, 1)
            Up_Time = round(Event_End - Cum_Down_Time, 1)

            # Print Events and Write Evemts to file
            print(dtc.strftime("%Y-%m-%d %H:%M:%S") + ' Duration = ' + str(Bad_Duration) \
                + ' Ping Count = ' + str(Bad_Tot_Counts) )
            print('     Worst Code = ' + Code_Labels[Last_Bad_Code] \
                + ' Worst Ping = ' + str(Last_Bad_Ping) )
            Outage_Row = ['Bad', dtc.strftime("%Y-%m-%d"), dtc.strftime("%H:%M:%S"), TOD_Labels[TOD], str(Bad_Duration), \
                str(Bad_Tot_Counts), Code_Labels[Last_Bad_Code], str(Last_Bad_Ping), \
                str(Cum_Down_Time), str(Up_Time), str(Event_End), \
                str(Ping_Bad_Limit), str(Sleep_per_Loop), Start_Time]
            Outage_CSV.writerow(Outage_Row)

            # Write buffered lines to file
            Outage_file.flush()
            os.fsync(Outage_file.fileno())
            
            # Reset counter and codes
            Last_Bad_Code = 0
            Bad_Code = 0
            Last_Bad_Ping = 0
            Bad_Count = 0
            Last_Minus_2_Was_Bad = False

        else:  # Consecutive Good Pings
            Last_Bad_Code = 0
            Last_Bad_Ping = 0
            Bad_Count = 0
            Last_Minus_2_Was_Bad = False
        
        # Update global variable values after each loop to be ready for any interupt.
        Global_Var_List =  [Outage_file,        Outage_CSV,     TOD_Labels,     TOD, \
                            Bad_Duration,       Bad_Count,      Code_Labels,    Last_Bad_Code, \
                            Last_Bad_Ping,      Cum_Down_Time,  Module_Start,   Bad_Start, \
                            Bad_End,            Last_Minus_2_Was_Bad, \
                            Ping_Bad_Limit,      Sleep_per_Loop, Start_Time]
        
        # Show plot if requested.
        if Show_Continuous_Ping_Plot:
            Continuous_Plot(YMax, ITime, RTime, Ims, Rms, NN, jj)
    
    # If in a bad event loop, write event.  Write End information, close file.
    Write_Last_Entries_And_Close('Normal')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, Exit_gracefully)
    Main_Program()


