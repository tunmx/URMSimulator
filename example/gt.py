import random

import urm
from urm import C, J, Z, S

# Defines a URM program to determine if x is greater than y.
gt_instruct = urm.Instructions(
    Z(0),

    # Check if either x (R1) or y (R2) is 0 first. If so, proceed to the "end game" conditions.
    J(1, 0, 25),
    J(2, 0, 24),

    # Compute the predecessor of R1 (x), simulating x - 1.
    Z(3),
    J(3, 1, 25),
    S(4),
    J(1, 4, 11),
    S(3),
    S(4),
    J(0, 0, 7),
    C(3, 1),
    Z(4),

    # Compute the predecessor of R2 (y), simulating y - 1.
    Z(3),
    J(3, 2, 25),
    S(4),
    J(2, 4, 20),
    S(3),
    S(4),
    J(0, 0, 16),
    C(3, 2),
    Z(4),

    Z(3),  # Reset R3 for safety.
    J(0, 0, 2),  # Jump back to the start to check conditions again.

    S(0),  # Set R0 to 1 indicating x > y.
)


# The gt function uses the URM model to determine if x > y.
def gt(x, y, safety_count=10000):
    # Determine the number of registers needed.
    num_of_registers = urm.haddr(gt_instruct) + 1
    # Allocate registers with initial values set to 0.
    registers = urm.allocate(num_of_registers)
    # Set initial values for x and y.
    input_nodes = {1: x, 2: y}
    # Execute the URM instructions and return the result stored in R0.
    result = urm.forward(input_nodes, registers, gt_instruct, safety_count=safety_count)
    return result.last_registers[0]


if __name__ == '__main__':
    for _ in range(5):
        x, y = random.randint(0, 20), random.randint(0, 20)
        z = gt(x, y)
        print(f'{x} > {y} is {z}')
