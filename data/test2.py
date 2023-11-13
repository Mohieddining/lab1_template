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


def lines_via_stop(linedict, stop):

    lines_v_stops = []
    for key, value in linedict.items():
        for station in value:
            if station == stop:
                lines_v_stops.append(key)

    sorted_lines = sorted(lines_v_stops, key=lambda x: int(x))
    return sorted_lines

###########################################################

tram_stops = build_tram_stops(STOP_FILE)
tram_lines, time_transition = build_tram_lines(LINE_FILE)
# print(tram_lines)

def dialogue(tramfile=TRAM_FILE):

    tram_stops = build_tram_stops(STOP_FILE)
    tram_lines, time_transition = build_tram_lines(LINE_FILE)

    with open(TRAM_FILE, 'r', encoding='utf-8'):
        stop = input('What lines go via ')
        result = lines_via_stop(tram_lines, stop)
        if result:
            print('The lines that go via', stop, 'are: ', result)
        else:
            print('No lines goes via', stop)

# line_dict = {'1': ['Östra Sjukhuset', 'Tingvallsvägen', 'Kaggeledstorget', 'Ättehögsgatan', 'Munkebäckstorget', 'Lana'], 
#             '2': ['Östra Sjukhuset', 'Mölndals sjukhus', 'Lackarebäck', 'Krokslätts Fabriker', 'Krokslätts torg', 'Lana']}

# print(lines_via_stop(line_dict, 'Östra Sjukhuset'))

if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        dialogue()


