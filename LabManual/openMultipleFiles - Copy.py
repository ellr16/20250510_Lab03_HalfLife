'''
Python script to read .tsv files from USX multi-run, 
and extract spectrum data
T. Hutton, tanya.hutton@uct.ac.za
Dept Physics, University of Cape Town
April 2018
Updated March 2023 
'''


import numpy as np
from matplotlib import pyplot as plt

# What file prefix did you choose on USX multi-run?(string)
filePrefix = 'AlActivation_run1'

# How many runs? (integer)
nRuns = 400

# what are your lower and upper limits for integration in channels? (integers)
lowerLimit = 0
upperLimit = 2048

# Initialise time array, will contain the integrated 
# number of counts between lowerLimit and upperLimit
# for each run
timeArray = np.zeros(nRuns)

# Placeholder
headerLen = 1000


# Loop through each run file
for i in range(1, nRuns+1):

#   open file 
    fileName = filePrefix +'_'+ str(i) + '.tsv'
    fileObject = open(fileName, 'r')    
 
#   loop through file line-by-line    
    for l, line in enumerate(fileObject):

        if "Conversion Gain" in line: 
            # Extract parameters from header and initialise arrays
            nChannels = int(line.split(':')[1])
            if nChannels < upperLimit: upperLimit = nChannels
            if i == 1: sumArray = np.zeros(nChannels)
            countArray = np.zeros(nChannels) 

        if "Channel Data" in line: headerLen = l+2

        if l >= headerLen:
#           split line and convert number of counts per channel to float
#           populate countArray channel-by-channel            
            part = line.split()
            if (len(part)) > 2: countArray[l - headerLen] = float(part[2])
            else: countArray[l - headerLen] = float(part[1])

#   close run file to release memory
    fileObject.close()    
    
#   sum counts between lowerLimit and upperLimit
#   populate timeArray run-by-run    
    timeArray[i-1] = sum(countArray[lowerLimit:upperLimit])

#   add run spectrum to sumArray
    sumArray += countArray
    
    print('fileName: %s\t integrated counts = %.0f' % (fileName, timeArray[i-1]))
        
            
plt.figure()    
plt.plot(timeArray)
plt.yscale('log')
plt.figure()
plt.plot(sumArray)
plt.yscale('log')
plt.show()    

