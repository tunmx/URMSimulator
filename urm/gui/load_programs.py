import json
import os
def load_programs(path):
    json_files = [f for f in os.listdir(path) if f.endswith(".json")]
    programs = []
    for json_file in json_files:
        with open(os.path.join(path, json_file), "r") as f:
            data = json.load(f)
            data['name'] = json_file.split('.')[0]
            programs.append(data)
    return programs

if __name__ == "__main__":
    programs = load_programs("./programs")
    for program in programs:
        print(program)
