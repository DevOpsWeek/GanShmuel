import json

json_str='{"ref":"val/val/val"}'
print(type(json_str))
dict_str=json.loads(json_str)
current_branch=list(dict_str['ref'].split("/"))
print(current_branch[2])