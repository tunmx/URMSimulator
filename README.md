URM Simulator is a Python library for simulating the operations of an Unlimited Register Machine (URM), a simplified model in theoretical computer science that simulates computation processes through a series of basic operations. This library provides a way to define URM programs, execute these programs, and observe changes in register values.

## Main Features

- **Support for the Four Basic URM Operations**: Zero, Successor, Copy, and Jump.
- **Program Execution and Tracking**: Offers a simulator for executing URM programs and tracking their execution process.
- **Custom URM Programs**: Allows users to define and execute custom URM programs and check the results of the execution.
- **Support Visual**: Add the GUI functionality to support visual representation of each step in URM instruction execution. This feature will facilitate users' learning and analysis of the instruction execution process.

## Advanced Features

- **size Function**: Calculates the number of instructions in a URM program. This is helpful for analyzing program complexity and debugging.
- **haddr Function**: Finds the highest register address used in a URM program. This is crucial for determining how many registers a program needs.
- **normalize Method**: Normalizes a URM program to ensure all jump operations point to valid instruction lines. This helps optimize program structure and prevent errors.
- **concat Method**: Concatenates two URM programs into a single program. This is useful for building complex logic or reusing existing code.
- **reloc Method**: Relocates register addresses in a URM program according to a specified mapping. This is useful when adjusting a program to fit a specific register configuration.

## Installation

Install URM Simulator using pip:

```bash
pip install urm
```

Make sure your Python environment is version 3.7 or higher.

## Usage Examples for GUI

You can directly use the GUI functionality for a more convenient and intuitive way to build URM programs and visualize their execution process. You only need to execute the following command in the command line:

```python
# Run the GUI program
urm gui
```

The program will use port 8975. If there's a conflict, you can modify the port number yourself.

```python
# Modify the port
urm gui --port 8975
```

After successfully launching the GUI program, you can open the URM program panel by accessing http://localhost:8975/index through your web browser.

![creator page](images/page-1.png)

![steps page](images/page-2.png)


## Usage Examples for Python Code

Below is an example of how to define and execute a simple URM program using the URM Simulator library:

### add(x, y) Function

Defines a URM program to calculate the sum of two numbers using the URM model.

```python
import urm
from urm import C, J, Z, S

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
    num_of_registers = urm.haddr(add_instruct) + 1
    registers = urm.allocate(num_of_registers)
    input_nodes = {1: x, 2: y}
    result = urm.forward(input_nodes, registers, add_instruct, safety_count=safety_count)
    return result.last_registers[0]

if __name__ == '__main__':
    x = 5
    y = 7
    z = add(x, y)
    print(f'add({x}, {y}) = {z}')
```

**Output:**

```bash
add(5, 7) = 12
```


### predecessor(x) function
Define a URM program to calculate the predecessor of a given number.
```bash
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
```
**Output:**
```bash
predecessor(9) = 8
predecessor(8) = 7
predecessor(4) = 3
predecessor(0) = 0
predecessor(3) = 2
```


### subtraction(x,y) function
Define the sequence of instructions for the subtraction operation.
```bash
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

```
**Output:**
```bash
subtraction(5, 14) = 0
subtraction(6, 9) = 0
subtraction(19, 13) = 6
subtraction(14, 1) = 13
subtraction(10, 3) = 7
```


### greater_than(x,y) function
Defines a URM program to determine if x is greater than y.
```bash
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

```
**Output:**
```bash
10 > 4 is 1
20 > 19 is 1
20 > 1 is 1
14 > 20 is 0
18 > 19 is 0
```


### fibb(x) function
Define the instructions for computing the nth Fibonacci number using the URM model.
```bash
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

```
### Tracking Execution Process - predecessor(x)
To track the execution process of your designed URM program, showing each step's instructions and register states, refer to the `predecessor(x)` example for debugging your instructions.
```bash
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

```
**Output:**
```bash
>Initial
R0      R1      R2
-----------------------
0       5       0
>1: J(0, 1, 0)
R0      R1      R2
-----------------------
0       5       0
>2: S(2)
R0      R1      R2
-----------------------
0       5       1
>3: J(1, 2, 0)
R0      R1      R2
-----------------------
0       5       1
>4: S(0)
R0      R1      R2
-----------------------
1       5       1
>5: S(2)
R0      R1      R2
-----------------------
1       5       2
>2: J(0, 0, 3)
R0      R1      R2
-----------------------
1       5       2
>3: J(1, 2, 0)
R0      R1      R2
-----------------------
1       5       2
>4: S(0)
R0      R1      R2
-----------------------
2       5       2
>5: S(2)
R0      R1      R2
-----------------------
2       5       3
>2: J(0, 0, 3)
R0      R1      R2
-----------------------
2       5       3
>3: J(1, 2, 0)
R0      R1      R2
-----------------------
2       5       3
>4: S(0)
R0      R1      R2
-----------------------
3       5       3
>5: S(2)
R0      R1      R2
-----------------------
3       5       4
>2: J(0, 0, 3)
R0      R1      R2
-----------------------
3       5       4
>3: J(1, 2, 0)
R0      R1      R2
-----------------------
3       5       4
>4: S(0)
R0      R1      R2
-----------------------
4       5       4
>5: S(2)
R0      R1      R2
-----------------------
4       5       5
>2: J(0, 0, 3)
R0      R1      R2
-----------------------
4       5       5


predecessor(5) = 4
```
## Author

- Jingyu Yan ([tunmxy@163.com](mailto:tunmxy@163.com))

