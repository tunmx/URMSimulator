import urm
from urm import C, J, Z, S

# Define the instructions for computing the nth Fibonacci number using the URM model.
fibb_instructions = urm.Instructions(
    J(1, 0, 0),  # If R1 (input n) is 0, end the program (fib(0) = 0, already in R0).
    S(0),  # Set R0 to 1 (to handle the case of fib(1)).
    J(1, 0, 0),  # If R1 is 1, end the program (fib(1) = 1).
    S(2),  # Initialize R2 (counter k) to 1.

    J(1, 2, 0),  # Loop condition: if R1 equals R2, end the program.

    S(2),  # Increment R2 (k).
    C(0, 4),  # Copy R0 (current Fibonacci number) to R4.
    Z(0),  # Zero R0 for the next calculation.
    Z(5),  # Zero R5, used as a counter in the loop.

    C(4, 0),  # Copy R4 (fib(k-1)) back to R0.
    J(5, 3, 15),  # Loop: if R5 equals R3, jump to instruction 15.
    S(0),  # Increment R0.
    S(5),  # Increment R5.
    J(1, 1, 11),  # Jump back to instruction 11, continue the loop.
    C(4, 3),  # Copy fib(k-1) to fib(k-2) for the next iteration.

    J(2, 2, 5),  # Jump back to instruction 5, continue until R1 equals R2.
)


# Define the function to compute the nth Fibonacci number using the URM instructions.
def fibb(x, safety_count=10000):
    # Determine the number of registers based on the highest address used.
    num_of_registers = urm.haddr(fibb_instructions) + 1
    # Allocate registers with initial values set to 0.
    registers = urm.allocate(num_of_registers)
    # Set the input value (n) in R1.
    input_nodes = {1: x}
    # Execute the URM program and return the result stored in R0 (the nth Fibonacci number).
    result = urm.forward(input_nodes, registers, fibb_instructions, safety_count=safety_count)
    return result.last_registers[0]


if __name__ == '__main__':
    for n in range(11):
        y = fibb(n)
        print(f'fibb({n}) = {y}')
