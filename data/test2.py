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
    

###########################################################

# tram_stops = build_tram_stops(STOP_FILE)
tram_lines, time_transition = build_tram_lines(LINE_FILE)
# print(tram_lines)



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

line_dict = {'1': ['Östra Sjukhuset', 'Tingvallsvägen', 'Kaggeledstorget', 'Ättehögsgatan', 'Munkebäckstorget', 'Lana'], 
            '2': ['Östra Sjukhuset', 'Mölndals sjukhus', 'Lackarebäck', 'Krokslätts Fabriker', 'Krokslätts torg', 'Lana']}

print(lines_between_stops(line_dict, 'Ättehögsgatan', 'Östra Sjukhuset'))

