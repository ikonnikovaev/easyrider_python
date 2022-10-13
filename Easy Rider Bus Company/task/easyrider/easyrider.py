import json

fields = ["bus_id", "stop_id", "stop_name", "next_stop", "stop_type", "a_time"]

def check(field, obj_field):
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


data_str = input()
data = json.loads(data_str)
error_count = {field: 0 for field in fields}
for obj in data:
    for field in fields:
        if field not in obj.keys() and field != "stop_type":
            error_count[field] += 1
        elif not check(field, obj[field]):
            error_count[field] += 1


print(f"Type and required field validation: {sum(error_count.values())} errors")
for field in fields:
    print(f"{field}: {error_count[field]}")


