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


def pred(x, safety_count=10000):
    num_of_registers = urm.haddr(pred_instruct) + 1
    registers = urm.allocate(num_of_registers)
    input_nodes = {1: x}
    result = urm.forward(input_nodes, registers, pred_instruct, safety_count=safety_count)

    # Extract detailed execution information from the result.
    num_steps = result.num_of_steps  # The total number of steps (operations) performed.
    registers_from_steps = result.registers_from_steps  # The state of the registers after each step.
    ops_from_steps = result.ops_from_steps  # The description of each operation performed.

    # Iterate through each step of the computation.
    for idx in range(num_steps):
        # Print the operation performed in the current step.
        print(f'>{ops_from_steps[idx]}')
        # Print a summary of the register states after the current operation.
        print(registers_from_steps[idx].summary())

    return result.last_registers[0]


if __name__ == '__main__':
    x = 5
    y = pred(x)
    print(f'predecessor({x}) = {y}')
