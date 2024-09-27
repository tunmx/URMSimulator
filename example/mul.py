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
mul_instruct = urm.Instructions(
    J(1, 3, 12),    # I1
    J(2, 3, 11),    # I2
    C(1, 3),        # I3
    S(5),           # I4
    J(2, 5, 11),    # I5
    Z(4),           # I6
    S(3),           # I7
    S(4),           # I8
    J(1, 4, 4),     # I9
    J(1, 1, 7),     # I10
    C(3, 1),        # I11
    Z(2),           # I12
    Z(3),           # I13
    Z(4),           # I14
    Z(5),           # I15
    C(1, 0),        # I16
    # 结束程序
)

# Define the function to perform multiplication using the URM simulator.
def mul(x, y, safety_count=1000):
    # Determine the number of registers needed based on the highest address used in instructions.
    num_of_registers = urm.haddr(mul_instruct) + 1
    # Allocate the registers, initializing them to zero.
    registers = urm.allocate(num_of_registers)
    # Set up the initial values for the registers based on the inputs.
    input_nodes = {1: x, 2: y}
    # Execute the program and obtain the result.
    result = urm.forward(input_nodes, registers, mul_instruct, safety_count=safety_count)
    # Return the value in the result register (R0).
    return result.last_registers[0]


if __name__ == '__main__':
    x = 5
    y = 7
    z = mul(x, y)
    print(f'mul({x}, {y}) = {z}')
