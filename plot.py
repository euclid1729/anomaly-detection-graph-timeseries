import matplotlib.pyplot as plt
import numpy as np
import sys
if len(sys.argv) != 3:
 print "enter file name and threshold as command line argument"
def plotScatter(normalpoints,threshold):
    #threshold=1.53476663145
    plt.axhline(y=threshold)
    plt.plot(normalpoints,color='r')
    plt.show()


threshold=sys.argv[2]  
data_full=[line.strip().split(' ')[1] for line in file(sys.argv[1])]
plotScatter(data_full,threshold)
