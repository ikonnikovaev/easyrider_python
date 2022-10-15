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



data_str = input()
data = json.loads(data_str)
type_error_count = {field: 0 for field in fields}
for obj in data:
    for field in fields:
        if field not in obj.keys() and field != "stop_type":
            type_error_count[field] += 1
        elif not check_type(field, obj[field]):
            type_error_count[field] += 1


# print(f"Type and required field validation: {sum(type_error_count.values())} errors")
# for field in fields:
#    print(f"{field}: {type_error_count[field]}")


formatted_fields = ["stop_name", "stop_type", "a_time"]
format_error_count = {field: 0 for field in formatted_fields}
for obj in data:
    for field in obj.keys():
        if not check_format(field, obj[field]):
            # print(obj[field])
            format_error_count[field] += 1

# print(f"Format validation: {sum(format_error_count.values())} errors")
# for field in formatted_fields:
#     print(f"{field}: {format_error_count[field]}")

bus_lines = {}
print("Line names and number of stops:")
for obj in data:
    if obj["bus_id"] not in bus_lines:
        bus_lines[obj["bus_id"]] = 0
    bus_lines[obj["bus_id"]] += 1
for bus_id in bus_lines:
    print(f"bus_id: {bus_id}, stops: {bus_lines[bus_id]}")
