import random

import urm
from urm import C, J, Z, S

# Define the sequence of instructions for the subtraction operation.
sub_instruct = urm.Instructions(
    C(1, 4),
    J(3, 2, 14),
    J(5, 4, 10),
    S(5),
    J(5, 4, 9),
    S(5),
    S(0),
    J(0, 0, 5),
    Z(5),
    S(3),
    C(0, 4),
    Z(0),
    J(0, 0, 2),
    C(4, 0),
)


# Define the 'sub' function to perform subtraction using the URM simulator.
def sub(x, y, safety_count=100000):
    # Determine the number of registers needed based on the highest address used in the instructions.
    num_of_registers = urm.haddr(sub_instruct) + 1
    # Allocate the registers, initializing them with zeros.
    registers = urm.allocate(num_of_registers)
    # Setup the initial values for the registers based on the inputs.
    input_nodes = {1: x, 2: y}
    # Execute the URM program with the given instructions and input, then obtain the result.
    result = urm.forward(input_nodes, registers, sub_instruct, safety_count=safety_count)
    # Return the value in the result register (R0).
    return result.last_registers[0]


# Main execution block to test the subtraction function.
if __name__ == '__main__':
    for _ in range(5):
        x, y = random.randint(0, 20), random.randint(0, 20)
        z = sub(x, y)
        print(f'subtraction({x}, {y}) = {z}')
