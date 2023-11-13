import sys
import json


# test data
linedict = {}
linedict['1'] = ['Mölndals Innerstad', 'Mölndals sjukhus', 'Lackarebäck','test station']
timedict = {}
timedict['Mölndals Innerstad'] = {'Mölndals sjukhus' : 1}
timedict['Mölndals sjukhus'] = {'Lackarebäck' : 7}
timedict['Lackarebäck'] = {'test station' : 9}

stop1 = 'Mölndals Innerstad'
stop2 = 'test station'
line = '1'
def time_between_stops(linedict, timedict, line, stop1, stop2):
    time = 0
    if stop1 and stop2  in linedict[line]:
        stops_on_line = linedict[line]
        start_index = stops_on_line.index(stop1)
        end_index = stops_on_line.index(stop2)
        if start_index == end_index:
            return(time)
        
        elif start_index < end_index:
            stops_between_values = stops_on_line[start_index: end_index + 1]
        else:
            stops_between_values = stops_on_line[end_index: start_index + 1]
            
            
        for indx in range(len(stops_between_values)- 1):
            if stops_between_values[indx] in timedict and stops_between_values[indx + 1] in timedict[stops_between_values[indx]]:
           
                time += timedict[stops_between_values[indx]][stops_between_values[indx + 1]]
            else:
                time += timedict[stops_between_values[indx + 1]
                                 ][stops_between_values[indx]]
        return(time)
    else:
        print("Stops are not on the same line") #maybe do some error handling here
        
        
        
print(time_between_stops(linedict, timedict, line, stop1, stop2))