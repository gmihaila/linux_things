#!/usr/bin/env
""" Change yaml paths for mlflow
	This will help users see artifacts logs
"""

import os


absolute_path = os.path.abspath(".")
mlrun_path = absolute_path + "/mlruns/"

if os.path.exists(mlrun_path):
	mlrun_path += "0"
	runs = os.listdir(mlrun_path)
	

def change_file(yaml_path):	
	with open(yaml_path+ "/meta.yaml", "r") as f:
		lines = f.read()
		lines = lines.split("\n")
		if "artifact_location: " in lines[0]:
			lines = ["artifact_location: //%s"%(yaml_path)] + lines[1:]
		if "artifact_uri: " in lines[0]:
			lines = ["artifact_uri: //%s"%(yaml_path) + "/artifacts"] + lines[1:]
	with open(yaml_path + "/meta.yaml", "w") as f:
		f.write("\n".join(lines))
	return "\n".join(lines)


## change main yaml file
change_file(mlrun_path)

## change each run yaml path
for run in runs:
	if len(run) == 32:
		print(run)
		change_file(mlrun_path + "/" + run)

print("Finsihed!")
