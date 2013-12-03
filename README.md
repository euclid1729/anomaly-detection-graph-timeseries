The program has been tested on a Windows machine as well as a Linux machine running Python 2.7. It can be downloaded and installed from http://www.python.org/download/
To successfully run the program, the following Python libraries need to installed:
1.) collections
2.) operator
3.) sys
4.) os
5.) Numpy

b. Environment variable settings (if any) and OS it should/could run on.
OS: Windows, Linux

c. Instructions on how to run the program.
1] First run the script format_convertor.py to convert the actual graph to the input type required for the algorithm to run.
To run the script use the following command

>> python format_convertor.py

Enter the necessary feature you want to use for anomaly detection and the output directory name. This will create a series of files from 0_<filename> to <t>_<filename> in the output directory specified by you, (output directory will be in your present working directory).

The anomaly detection algorithm can be run by using the following command:
>> python time_series_zscores.py

The program will ask the user for the directory name of the input graph. Please specify the name of the directory which contains files from the output of the format_convertor script (please keep time_series_zscores.py and the output directory of format_convertor.py
in same working directory) . Please specify the path of the output file at the appropriate prompt.

d. Instructions on how to interpret the results.
The first line of output file contains min threshold and max threshold for z scores. The following lines contain (start_day,end_day) of anomalous week along with the z score. 

e. Sample input and output files.
Sample files are included in the zip along with the README
