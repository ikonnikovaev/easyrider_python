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

def describe_lines(data):
    lines = {}
    for obj in data:
        bus_id = obj["bus_id"]
        stop_type = obj["stop_type"]
        if stop_type not in ['S', 'O', 'F']:
            stop_type = 'O'
        stop_name = obj["stop_name"]
        if bus_id not in lines:
            lines[bus_id] = {'S': set(), 'F': set(), 'O': set()}
        lines[bus_id][stop_type].add(stop_name)
    return lines

def check_lines(lines):
    for bus_id in lines:
        if len(lines[bus_id]['S']) < 1 or len(lines[bus_id]['F']) < 1:
            print(f"There is no start or end stop for the line: {bus_id}.")
            return False
    return True

def find_start_stops(lines):
    start_stops = set()
    for bus_id in lines:
        start_stops.update(lines[bus_id]['S'])
    return start_stops

def find_finish_stops(lines):
    finish_stops = set()
    for bus_id in lines:
        finish_stops.update(lines[bus_id]['F'])
    return finish_stops

def find_transfer_stops(lines):
    transfer_stops = set()
    for (bus_id_1, bus_id_2) in itertools.combinations(lines.keys(), 2):
        stops_1 = lines[bus_id_1]['S'] | lines[bus_id_1]['F'] | lines[bus_id_1]['O']
        stops_2 = lines[bus_id_2]['S'] | lines[bus_id_2]['F'] | lines[bus_id_2]['O']
        transfer_stops.update(stops_1 & stops_2)
    return transfer_stops

data_str = input()
data = json.loads(data_str)
lines = describe_lines(data)
if check_lines(lines):
    start_stops = sorted(list(find_start_stops(lines)))
    transfer_stops = sorted(list(find_transfer_stops(lines)))
    finish_stops = sorted(list(find_finish_stops(lines)))
    print(f"Start stops: {len(start_stops)} {start_stops}")
    print(f"Transfer stops: {len(transfer_stops)} {transfer_stops}")
    print(f"Finish stops: {len(finish_stops)} {finish_stops}")



# type_error_count = {field: 0 for field in fields}
# for obj in data:
#     for field in fields:
#         if field not in obj.keys() and field != "stop_type":
#             type_error_count[field] += 1
#         elif not check_type(field, obj[field]):
#             type_error_count[field] += 1


# print(f"Type and required field validation: {sum(type_error_count.values())} errors")
# for field in fields:
#    print(f"{field}: {type_error_count[field]}")


# formatted_fields = ["stop_name", "stop_type", "a_time"]
# format_error_count = {field: 0 for field in formatted_fields}
# for obj in data:
#     for field in obj.keys():
#         if not check_format(field, obj[field]):
#             # print(obj[field])
#             format_error_count[field] += 1

# print(f"Format validation: {sum(format_error_count.values())} errors")
# for field in formatted_fields:
#     print(f"{field}: {format_error_count[field]}")

# bus_lines = {}
# print("Line names and number of stops:")
# for obj in data:
#     if obj["bus_id"] not in bus_lines:
#         bus_lines[obj["bus_id"]] = 0
#     bus_lines[obj["bus_id"]] += 1
# for bus_id in bus_lines:
#     print(f"bus_id: {bus_id}, stops: {bus_lines[bus_id]}")


