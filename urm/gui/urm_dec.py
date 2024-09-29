import json
from urm import C, J, Z, S
import urm

data = {
  "instructions": [
    {
      "operator": "C",
      "params": [
        2,
        0
      ]
    },
    {
      "operator": "Z",
      "params": [
        2
      ]
    },
    {
      "operator": "J",
      "params": [
        1,
        2,
        0
      ]
    },
    {
      "operator": "S",
      "params": [
        0
      ]
    },
    {
      "operator": "S",
      "params": [
        2
      ]
    },
    {
      "operator": "J",
      "params": [
        3,
        3,
        3
      ]
    }
  ],
  "safetyLimit": 10000
}


def build_urm_program_from_data(data):
    import urm
    from urm import C, J, Z, S

    instructions = []
    for instruction in data['instructions']:
        operator = instruction['operator']
        params = instruction['params']
        
        if operator == 'C':
            instructions.append(C(*params))
        elif operator == 'Z':
            instructions.append(Z(*params))
        elif operator == 'J':
            instructions.append(J(*params))
        elif operator == 'S':
            instructions.append(S(*params))
    
    urm_program = urm.Instructions(*instructions)
    safety_count = data.get("safetyLimit", 1000)
    return urm_program, safety_count

def serialize_urm_program(urm_program, safety_count):
    serialized_program = {
        "instructions": [],
        "safetyLimit": safety_count
    }
    
    for instruction in urm_program:
        print(instruction)
        operator = instruction[0]
        params = instruction[1:]
        
        serialized_instruction = {
            "operator": operator,
            "params": list(params)
        }
        
        serialized_program["instructions"].append(serialized_instruction)
    
    return serialized_program

def pipeline_urm_program(urm_program, safety_count):
    num_of_registers = urm.haddr(urm_program) + 1
    registers = urm.allocate(num_of_registers)
    input_nodes = {1: 2, 2: 4}
    result = urm.forward(input_nodes, registers, urm_program, safety_count=safety_count)
    return result


if __name__ == "__main__":
    urm_program, safety_count = build_urm_program_from_data(data)
    serialized_program = serialize_urm_program(urm_program, safety_count)
    print(serialized_program)
    num_of_registers = urm.haddr(urm_program) + 1
    registers = urm.allocate(num_of_registers)
    input_nodes = {1: 2, 2: 4}
    result = urm.forward(input_nodes, registers, urm_program, safety_count=safety_count)
    print(result.last_registers)