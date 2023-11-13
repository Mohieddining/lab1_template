import sys
import json
from math import radians, sin, cos, sqrt, atan2, pi

# files given
STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'

# file to give
TRAM_FILE = './tramnetwork.json'

def build_tram_stops(jsonobject):
    tram_stops = {}
    with open(STOP_FILE, 'r') as file:
        stops = json.load(file)
        
    for stop_name, stop_info in stops.items():
        latitude, longitude = stop_info['position']
        tram_stops[stop_name] = {'lat': (float(latitude)), 'lon': float(longitude)}

    return tram_stops

def build_tram_lines(lines):
    train_lines_number_keys = []
    Stop_time = []
    Stop_name = []

    tram_lines = {}
    time_transition = {}
    with open(LINE_FILE, 'r', encoding='utf-8') as file:
        lines_raw = file.read()
        Lines_seperated = lines_raw.split("\n\n")
        Numberof_train_lines = len(Lines_seperated)

        for ind1 in range(Numberof_train_lines-1):
            Stops_seperated = Lines_seperated[ind1].split("\n")
            train_lines_number_keys.append(Stops_seperated[0].rstrip(':'))
            Stops_seperated.pop(0)
            Numberof_Stops = len(Stops_seperated)

            for ind2 in range(Numberof_Stops):
                Temp = Stops_seperated[ind2].split("  ")
                Stop_name.append(Temp[0])
                Temp = Stops_seperated[ind2].split(":")
                Stop_time.append(int(Temp[1]))

            tram_lines[train_lines_number_keys[ind1]] = []
            for ind3 in range(Numberof_Stops): # here we separate the list into stops
                parts = Stops_seperated[ind3].split("  ")
                Stops_seperated[ind3] = parts[0]
                tram_lines[train_lines_number_keys[ind1]].append(Stops_seperated[ind3])
            
            
        for n in range(len(Stop_name)-1):
            duration = Stop_time[n+1] - Stop_time[n]
            if Stop_time[n+1] == 0:
                n = n + 1
            else:
                if Stop_name[n] not in time_transition.keys():
                    time_transition[Stop_name[n]] = {Stop_name[n+1]: duration}
                else:
                    if Stop_name[n+1] not in time_transition[Stop_name[n]]:
                        time_transition[Stop_name[n]][Stop_name[n+1]] = duration

        return tram_lines, time_transition
    
        # print(tram_lines['13'], '\n')
        # print(time_transition, '\n')
        # print("Length of time_transition: ", len(time_transition))
        # print("Length of Stop_name: ", len(Stop_name))
        # print("Length of Stop_time: ", len(Stop_time))

def build_tram_network(stopfile, linefile):

    tram_stops = build_tram_stops(stopfile)
    tram_lines, time_transition = build_tram_lines(linefile)

    tram_network = {'stops': {}, 'lines': {}, 'times': {}}

    for key, value in tram_stops.items():
        tram_network['stops'][key] = value

    for key, value in tram_lines.items():
        tram_network['lines'][key] = value

    for key, value in time_transition.items():
        tram_network['times'][key] = value


    with open(TRAM_FILE, 'w', encoding='utf-8') as json_file:
        network = json.dump(tram_network, json_file)
        
    # return tram_network

def lines_via_stop(linedict, stop):

    lines_v_stops = []
    for key, value in linedict.items():
        for station in value:
            if station == stop:
                lines_v_stops.append(key)

    sorted_lines = sorted(lines_v_stops, key=lambda x: int(x))
    return sorted_lines

def lines_between_stops(linedict, stop1, stop2):

    start_index = 0
    end_index = 0
    stops_btw = []
    lines_btw_stops = []

    for key, value in linedict.items():
        for station in value:
            if stop1 == station:
                start_index = value.index(stop1)
            if stop2 == station:
                end_index = value.index(stop2)
        
        if end_index > start_index:
            stops_btw = value[start_index:end_index + 1]
        if start_index > end_index:
            stops_btw = value[end_index:start_index + 1]

        if stop1 in stops_btw and stop2 in stops_btw:
            lines_btw_stops.append(key)

    sorted_stops = sorted(lines_btw_stops, key=lambda x: int(x))
    return sorted_stops

def time_between_stops(linedict, timedict, line, stop1, stop2):
    time = 0
    if stop1 and stop2 in linedict[line]:
        stops_on_line = linedict[line]
        start_index = stops_on_line.index(stop1)
        end_index = stops_on_line.index(stop2)
        if start_index == end_index:
            return time

        elif start_index < end_index:
            stops_between_values = stops_on_line[start_index: end_index + 1]
        else:
            stops_between_values = stops_on_line[end_index: start_index + 1]

        for indx in range(len(stops_between_values) - 1):
            if stops_between_values[indx] in timedict and stops_between_values[indx + 1] in timedict[stops_between_values[indx]]:

                time += timedict[stops_between_values[indx]
                                 ][stops_between_values[indx + 1]]
            else:
                time += timedict[stops_between_values[indx + 1]
                                 ][stops_between_values[indx]]
                
        # return (print('The time between', stop1, 'and', stop2, 'is: ', time, 's'))
        return time
    else:
        # maybe do some error handling here
        print("Stops are not on the same line")

def distance_between_stops(stopdict, stop1, stop2):
    r = 6371009.0
    lat_1 = stopdict[stop1]['lat'] * pi/180
    lon_1 = stopdict[stop1]['lon'] * pi/180
    lat_2 = stopdict[stop2]['lat'] * pi/180
    lon_2 = stopdict[stop2]['lon'] * pi/180
    dlat = lat_2 - lat_1
    dlon = lon_2 - lon_1
    meanlat = (lat_1 + lat_2) / 2
    distance = int(r* sqrt(dlat **2 + (cos(meanlat) * dlon) **2 ))
    
    # return (print('The distance between', stop1, 'and', stop2, 'is: ', distance, 'm'))
    return distance

def answer_query(tramdict, query):
    ## YOUR CODE HERE
    pass

def dialogue(tramfile=TRAM_FILE):
    ## YOUR CODE HERE
    pass

if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        dialogue()


# print(build_tram_stops(STOP_FILE))

# print(build_tram_lines(LINE_FILE))

# print(build_tram_network(STOP_FILE, LINE_FILE))

# tram_lines, time_transition = build_tram_lines(LINE_FILE)
# print(time_between_stops(tram_lines, time_transition, '2', 'Mölndals Innerstad', 'Axel Dahlströms Torg'))

# tram_stops = build_tram_stops(STOP_FILE)
# print(distance_between_stops(tram_stops, 'Mölndals Innerstad', 'Axel Dahlströms Torg'))

# tram_lines, time_transition = build_tram_lines(LINE_FILE)
# print(lines_via_stop(tram_lines, 'Centralstationen'))

tram_lines, time_transition = build_tram_lines(LINE_FILE)
print(lines_between_stops(tram_lines, "Korsvägen", "Chalmers"))