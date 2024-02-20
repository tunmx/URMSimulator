import urm
from urm import C, J, Z, S

"""
Defines a URM program to calculate the sum of two numbers using the URM model.
The program uses the concept of Unlimited Register Machines for computation.

Parameters:
- input_R1: Contains the first number (x)
- input_R2: Contains the second number (y)
- output_R0: Will contain the result of adding x and y

The URM program consists of a series of instructions designed to add x and y.
"""

# Define the sequence of instructions for the addition operation.
add_instruct = urm.Instructions(
    C(2, 0),
    Z(2),
    J(1, 2, 0),
    S(0),
    S(2),
    J(3, 3, 3),
)

# Define the function to perform addition using the URM simulator.
def add(x, y, safety_count=1000):
    # Determine the number of registers needed based on the highest address used in instructions.
    num_of_registers = urm.haddr(add_instruct) + 1
    # Allocate the registers, initializing them to zero.
    registers = urm.allocate(num_of_registers)
    # Set up the initial values for the registers based on the inputs.
    input_nodes = {1: x, 2: y}
    # Execute the program and obtain the result.
    result = urm.forward(input_nodes, registers, add_instruct, safety_count=safety_count)
    # Return the value in the result register (R0).
    return result.last_registers[0]


if __name__ == '__main__':
    x = 5
    y = 7
    z = add(x, y)
    print(f'add({x}, {y}) = {z}')
