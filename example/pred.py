import random

import urm
from urm import C, J, Z, S

# Define a URM program to calculate the predecessor of a given number.
# The 'pred_instruct' represents a series of URM instructions for this purpose.
pred_instruct = urm.Instructions(
    J(0, 1, 0),
    S(2, ),
    J(1, 2, 0),
    S(0),
    S(2),
    J(0, 0, 3)
)


# Define the 'pred' function to calculate the predecessor of a number using the URM model.
def pred(x, safety_count=10000):
    # Determine the number of registers needed based on the highest address used in the instructions.
    num_of_registers = urm.haddr(pred_instruct) + 1
    # Allocate the registers, initializing them with zeros.
    registers = urm.allocate(num_of_registers)
    # Setup the initial values for the registers based on the input.
    input_nodes = {1: x}
    # Execute the URM program with the given instructions and input, then obtain the result.
    result = urm.forward(input_nodes, registers, pred_instruct, safety_count=safety_count)
    # Return the value in the result register (R0).
    return result.last_registers[0]


if __name__ == '__main__':
    for _ in range(5):
        x = random.randint(0, 10)
        y = pred(x)
        print(f'predecessor({x}) = {y}')
