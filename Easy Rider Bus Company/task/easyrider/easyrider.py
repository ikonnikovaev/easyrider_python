import itertools
import json
import re

fields = ["bus_id", "stop_id", "stop_name", "next_stop", "stop_type", "a_time"]

def check_type(field, obj_field):
    if field in ["bus_id", "stop_id", "next_stop"]:
        if not isinstance(obj_field, int):
            return False
    if field in ["stop_name", "a_time"]:
        if not isinstance(obj_field, str) or not obj_field:
            return False
    if field == "stop_type":
        if not isinstance(obj_field, str) or len(obj_field) > 1:
            return False
    return True

def check_format(field, obj_field):
    if field == "stop_name":
        stop_name_pattern = r"([A-Z][\w ]*) (Road|Avenue|Boulevard|Street)$"
        return re.match(stop_name_pattern, obj_field) is not None
    if field == "stop_type" and obj_field:
        if len(obj_field) != 1:
            return False
        return re.match("S|O|F$", obj_field) is not None
    if field == "a_time":
        time_pattern = r"([01]\d|2[0-3]):([0-5]\d)$"
        return re.match(time_pattern, obj_field) is not None
    return True

class Stop:
    stop_names = {}
    def __init__(self, stop_id, stop_name, next_stop, stop_type, a_time):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.next_stop = next_stop
        if stop_type not in ['S', 'O', 'F']:
            self.stop_type = 'O'
        else:
            self.stop_type = stop_type
        self.a_time = a_time
        Stop.stop_names[stop_id] = stop_name

    def get_stop_name(stop_id):
        return Stop.stop_names[stop_id]



class BusLine:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.stops = []
        self.start = None
        self.finish = None

    def add_stop(self, stop):
        self.stops.append(stop)
        if stop.stop_type == 'S':
            self.start = stop
        if stop.stop_type == 'F':
            self.finish = stop

    def get_stop_names(self):
        stop_names = set()
        for stop in self.stops:
            stop_names.add(stop.stop_name)
        return stop_names



def describe_lines(data):
    lines = {}
    for obj in data:
        bus_id = obj["bus_id"]
        stop_id = obj["stop_id"]
        stop_type = obj["stop_type"]
        stop_name = obj["stop_name"]
        next_stop = obj["next_stop"]
        stop_type = obj["stop_type"]
        a_time = obj["a_time"]
        stop = Stop(stop_id, stop_name, next_stop, stop_type, a_time)
        if bus_id not in lines:
            lines[bus_id] = BusLine(bus_id)
        lines[bus_id].add_stop(stop)
    return lines

def check_lines_ends(lines):
    for bus_id in lines:
        if lines[bus_id].start is None or lines[bus_id].finish is None:
            print(f"There is no start or end stop for the line: {bus_id}.")
            return False
    return True

def find_start_stops(lines):
    start_stops = set()
    for bus_id in lines:
        start_stops.add(lines[bus_id].start.stop_name)
    return start_stops

def find_finish_stops(lines):
    finish_stops = set()
    for bus_id in lines:
        finish_stops.add(lines[bus_id].finish.stop_name)
    return finish_stops

def find_transfer_stops(lines):
    transfer_stops = set()
    for (bus_id_1, bus_id_2) in itertools.combinations(lines.keys(), 2):
        transfer_stops.update(lines[bus_id_1].get_stop_names() & lines[bus_id_2].get_stop_names())
    return transfer_stops

data_str = input()
data = json.loads(data_str)
lines = describe_lines(data)
if check_lines_ends(lines):
    start_stops = sorted(list(find_start_stops(lines)))
    transfer_stops = sorted(list(find_transfer_stops(lines)))
    finish_stops = sorted(list(find_finish_stops(lines)))
    print(f"Start stops: {len(start_stops)} {start_stops}")
    print(f"Transfer stops: {len(transfer_stops)} {transfer_stops}")
    print(f"Finish stops: {len(finish_stops)} {finish_stops}")





