"""
Created by Jingyu Yan on 2023/12/19.
"""

import copy
from typing import List, Tuple, Generator, Dict
from dataclasses import dataclass
import time
from functools import wraps


def cost(tag=''):
    """
    A decorator for timing a function execution.

    Usage:
    @cost('optional_tag')
    def your_function():
        # function implementation
    """
    def wrapper(fn):
        @wraps(fn)
        def wrapper_use_time(*args, **kw):
            t1 = time.time()
            try:
                res = fn(*args, **kw)
            except Exception as e:
                print(f"Error in {fn.__name__}({tag}): {str(e)}")
                return None
            else:
                t2 = time.time()
                print(f"{tag}@Cost of {fn.__name__}(): {round(t2 - t1, 3)} seconds")
                return res
        return wrapper_use_time
    return wrapper


class Instructions(object):
    """
    'Instructions' represents a list of URM (Unlimited Register Machine) instructions.

    This class is used to store and manipulate a sequence of instructions for a URM simulator.
    Each instruction in the list is a tuple representing a specific operation in the URM.
    """

    def __init__(self, *inst, ):
        """
        Initializes the Instructions object.

        :param inst: A list of tuples where each tuple represents a URM instruction.
                     Each instruction is a tuple consisting of an operation code followed
                     by its arguments. If None is provided, initializes with an empty list.
        """
        self.instructions = list()
        for item in inst:
            if isinstance(item, list):
                self.instructions += item
            elif isinstance(item, Instructions):
                self.instructions += item.instructions
            elif isinstance(item, tuple):
                self.instructions.append(item)
            else:
                raise TypeError("Input data error.")

    def __str__(self):
        formatted_instructions = []
        for instruction in self.instructions:
            formatted_instruction = f"{instruction[0]}({', '.join(map(str, instruction[1:]))})"
            formatted_instructions.append(formatted_instruction)
        return f"[{', '.join(formatted_instructions)}]"

    def copy(self):
        return copy.deepcopy(self)

    def summary(self):
        # Define the format for each row of the table
        row_format = "{:<5}\t{:<3}\t{:<4}\t{:<4}\t{:<7}\n"
        # Create a table header with lines
        header_line = '-' * 40
        table = row_format.format("Line", "Op", "Arg1", "Arg2", "Jump To") + header_line + '\n'

        # Iterate over the instructions and their indices
        for index, instruction in enumerate(self.instructions, 1):
            # Prepare args with empty strings for missing values
            args = [''] * 3
            # Fill the args list with actual values from the instruction
            for i, arg in enumerate(instruction[1:]):
                args[i] = str(arg)
            # Format each line as a row in the table
            line = row_format.format(index, instruction[0], *args)
            table += line

        return table

    def __getitem__(self, index):
        return self.instructions[index]

    def __setitem__(self, index, value):
        if not isinstance(value, tuple):
            raise ValueError("Type error.")
        self.instructions[index] = value

    def __iter__(self):
        return iter(self.instructions)

    def __len__(self):
        return len(self.instructions)

    def __add__(self, other):
        if not isinstance(other, Instructions):
            raise ValueError("Operand must be an instance of Instructions.")

        # Use concatenation function
        return Instructions.concatenation(self, other)

    def append(self, item):
        if isinstance(item, list):
            self.instructions += item
        elif isinstance(item, Instructions):
            self.instructions += item.instructions
        else:
            self.instructions.append(item)

    def haddr(self):
        highest_register = -1
        for instruction in self.instructions:
            op = instruction[0]
            if op in ['Z', 'S']:  # These instructions involve only one register
                highest_register = max(highest_register, instruction[1])
            elif op in ['C', 'J']:  # These instructions involving two registers
                highest_register = max(highest_register, instruction[1], instruction[2])
        return highest_register if highest_register >= 0 else None

    @staticmethod
    def normalize(instructions):
        normalized_instructions = Instructions()
        for instruction in instructions:
            if instruction[0] == 'J':  # Check if it's a jump instruction
                m, n, k = instruction[1], instruction[2], instruction[3]
                if not 1 <= k <= len(instructions):  # Check if k is out of range
                    k = len(instructions) + 1  # Set k to n + 1
                normalized_instructions.append(('J', m, n, k))
            else:
                normalized_instructions.append(instruction)

        return normalized_instructions

    @staticmethod
    def concatenation(p1, p2):
        if not p1.instructions:  # P is empty
            return Instructions(p2)
        else:
            # Normalize P and obtain P' = I'1 ... I'n
            normalized_p1 = Instructions.normalize(p1)
            n = len(normalized_p1)

            # Prepare the concatenated instructions list with normalized P
            concatenated = normalized_p1[:]

            # Process Q and adjust the jump instructions
            for instruction in p2:
                if instruction[0] == 'J':  # It's a jump instruction
                    # If I_k = J(k, l, q) then change I_k with I'_k = J(k, l, q+n)
                    k, l, q = instruction[1], instruction[2], instruction[3]
                    if q != 0:  # We don't adjust if q is 0 (means jump to start)
                        q += n
                    concatenated.append(('J', k, l, q))
                else:
                    # Non-jump instructions remain the same
                    concatenated.append(instruction)

            return Instructions(concatenated)

    @staticmethod
    def relocation(instructions, alloc: Tuple[int]):
        if not isinstance(alloc, tuple) or len(alloc) != instructions.haddr() + 1:
            raise ValueError("invalid allocation")
        relocated_instructions = []
        for i in instructions:
            if i[0] == 'Z' or i[0] == 'S':
                relocated_instructions.append((i[0], alloc[i[1]]))
            elif i[0] == 'C':
                relocated_instructions.append((i[0], alloc[i[1]], alloc[i[2]]))
            elif i[0] == 'J':
                relocated_instructions.append((i[0], alloc[i[1]], alloc[i[2]], i[3]))
        return Instructions(relocated_instructions)


class Registers(object):
    """
    'Registers' represents a list of register values for a URM (Unlimited Register Machine).

    This class is used to store the state of the registers in a URM simulator.
    Each register can hold an integer value. The registers are indexed starting from 0.
    """

    def __init__(self, lis: List[int]):
        """
        Initializes the Registers object with a given list of integers.

        Each integer in the list represents the initial value of a register in the URM.
        The registers are indexed in the order they appear in the list.

        :param lis: A list of integers representing the initial values of the registers.
                    Each integer must be non-negative, as URM registers can only hold
                    natural numbers (including zero).

        :raises ValueError: If any item in the list is not an integer or is a negative integer.
        """
        for item in lis:
            if not isinstance(item, int):
                raise ValueError("All items in the list must be integers")
            if item < 0:
                raise ValueError("An integer greater than 0 must be entered")

        self.registers = lis

    def copy(self):
        return copy.deepcopy(self)

    def summary(self):
        headers = [f"R{i}" for i in range(len(self.registers))]
        divider = '-' * (len(headers) * 8 - 1)
        header_row = '\t'.join(headers)
        values_row = '\t'.join(map(str, self.registers))
        table = f"{header_row}\n{divider}\n{values_row}"
        return table

    def __str__(self):
        return str(self.registers)

    def __getitem__(self, index):
        return self.registers[index]

    def __setitem__(self, index, value):
        if not isinstance(value, int):
            raise ValueError("Only integers can be assigned")
        if value < 0:
            raise ValueError("An integer greater than 0 must be entered")
        self.registers[index] = value

    def __len__(self):
        return len(self.registers)

    @staticmethod
    def allocate(num: int):
        r = [0 for _ in range(num)]
        reg = Registers(r)
        return reg


@dataclass
class URMResult(object):
    """
    Store URM simulator calculation results.
    """
    num_of_steps: int
    ops_from_steps: List[str]
    registers_from_steps: List[Registers]
    last_registers: Registers


class URMSimulator(object):
    """
    Implementation scheme for simulating an Unlimited Register Machine,
    realizing the computational logic of four types of instructions: zero, successor, copy, and jump.
    """

    @staticmethod
    def _execute_zero(registers: Registers, n: int) -> Registers:
        """
        Set the value of register number n to 0.
        """
        registers[n] = 0
        return registers

    @staticmethod
    def _execute_successor(registers: Registers, n: int) -> Registers:
        """
        Increment the value of register number n.
        """
        registers[n] += 1
        return registers

    @staticmethod
    def _execute_copy(registers: Registers, j: int, k: int) -> Registers:
        """
        Copy the value of register number j to register number k.
        """
        registers[k] = registers[j]
        return registers

    @staticmethod
    def _execute_jump(registers: Registers, m: int, n: int, q: int, current_line: int) -> int:
        """
        Jump to line 'q' if values in registers 'm' and 'n' are equal, else go to the next line.
        """
        if registers[m] == registers[n]:
            return q - 1  # Adjust for zero-based indexing
        else:
            return current_line + 1

    @staticmethod
    def execute_instructions(instructions: Instructions, initial_registers: Registers,
                             safety_count: int = 1000) -> Generator:
        """
        Execute a set of URM (Unlimited Register Machine) instructions.

        :param instructions: The set of URM instructions to execute.
        :param initial_registers: The initial state of the registers.
        :param safety_count: Maximum number of iterations to prevent infinite loops.
        :return: Generator yielding the state of the registers after each instruction.
        """
        registers = initial_registers
        exec_instructions = copy.deepcopy(instructions)
        exec_instructions.append(('END',))
        current_line = 0
        count = 0

        while current_line < len(exec_instructions):
            if count > safety_count:
                raise ValueError("The number of cycles exceeded the safe number.")

            instruction = exec_instructions[current_line]
            op = instruction[0]

            try:
                if op == 'Z':
                    registers = URMSimulator._execute_zero(registers, instruction[1])
                    current_line += 1
                elif op == 'S':
                    registers = URMSimulator._execute_successor(registers, instruction[1])
                    current_line += 1
                elif op == 'C':
                    registers = URMSimulator._execute_copy(registers, instruction[1], instruction[2])
                    current_line += 1
                elif op == 'J':
                    jump_result = URMSimulator._execute_jump(registers, instruction[1], instruction[2], instruction[3],
                                                             current_line)
                    current_line = jump_result if jump_result != -1 else len(exec_instructions)
                elif op == 'END':
                    break
                count += 1
            except Exception as e:
                raise RuntimeError(f"Error executing instruction at line {current_line}: {e}")

            yield copy.deepcopy(registers), f"[{current_line}]{op}" + "(" + ", ".join(map(str, instruction[1:])) + ")"

    @staticmethod
    def forward(param: Dict[int, int], initial_registers: Registers, instructions: Instructions,
                safety_count: int = 1000) -> URMResult:
        registers = copy.deepcopy(initial_registers)
        if isinstance(param, dict):
            for key, value in param.items():
                if not isinstance(key, int):
                    raise TypeError("All keys must be integers")
                if not isinstance(value, int):
                    raise TypeError("All values must be integers")
                if value < 0:
                    raise ValueError("Input Value must be a natural number")
                if key < 0:
                    raise ValueError("Input Index must be a natural number")
                registers[key] = value

        registers_list = [copy.deepcopy(registers), ]
        ops_info = ['Initial']
        if len(registers) < instructions.haddr():
            raise ValueError("The number of registers requested cannot satisfy this set of instructions.")
        gen = URMSimulator.execute_instructions(instructions=instructions, initial_registers=registers,
                                                safety_count=safety_count)
        num_of_steps = 0
        last_registers = None
        for registers_moment, command in gen:
            num_of_steps += 1
            ops_info.append(command)
            registers_list.append(registers_moment)
            last_registers = registers_moment
        result = URMResult(ops_from_steps=ops_info, registers_from_steps=registers_list, last_registers=last_registers,
                           num_of_steps=num_of_steps)

        return result


def urm_op(func):
    """
    Decorator to convert the function to op.
    """

    def wrapper(*args):
        function_name = func.__name__
        return (function_name, *args)

    return wrapper


@urm_op
def C():
    """
    URM Copy operation. Copies the value from one register to another.
    """
    pass


@urm_op
def J():
    """
    URM Jump operation. Jumps to a specified line if two registers hold the same value.
    """
    pass


@urm_op
def Z():
    """
    URM Zero operation. Sets the value of a register to zero.
    """
    pass


@urm_op
def S():
    """
    URM Successor operation. Increments the value of a register by one.
    """
    pass


_END = "END"  # Marker for the end of a URM program (used internally)


def size(instructions: Instructions) -> int:
    """
    Calculates the number of instructions in a URM program.

    :param instructions: An Instructions object representing a URM program.
    :return: The number of instructions in the program.
    """
    return len(instructions)


def haddr(instructions: Instructions) -> int:
    """
    Finds the highest register address used in a URM program.

    :param instructions: An Instructions object representing a URM program.
    :return: The highest register index used in the program.
    """
    return instructions.haddr()


def normalize(instructions: Instructions) -> Instructions:
    """
    Normalizes a URM program so that all jump operations target valid instruction lines.

    :param instructions: An Instructions object representing a URM program.
    :return: A new Instructions object with normalized jump targets.
    """
    return Instructions.normalize(instructions)


def concat(p: Instructions, q: Instructions) -> Instructions:
    """
    Concatenates two URM programs into a single program.

    :param p: An Instructions object representing the first URM program.
    :param q: An Instructions object representing the second URM program.
    :return: A new Instructions object with the concatenated program.
    """
    return Instructions.concatenation(p, q)


def reloc(instructions: Instructions, alloc: Tuple[int, ...]) -> Instructions:
    """
    Relocates the register addresses in a URM program according to a specified mapping.

    :param instructions: An Instructions object representing a URM program.
    :param alloc: A tuple defining the new register addresses for each original address.
    :return: A new Instructions object with relocated register addresses.
    """
    return Instructions.relocation(instructions, alloc)


def allocate(num: int) -> Registers:
    """
    Allocates a specified number of registers, initializing them with zero values.

    This function creates a new Registers object with a given number of registers.
    Each register is initialized with the value 0.

    :param num: The number of registers to allocate.
    :return: A Registers object with 'num' registers, each initialized to 0.
    """
    return Registers.allocate(num)


def forward(param: Dict[int, int], initial_registers: Registers, instructions: Instructions,
            safety_count: int = 1000) -> URMResult:
    """
    Executes a URM (Unlimited Register Machine) simulation with given parameters, initial registers, and instructions.

    This function sets up the registers according to the input parameters, then runs the URM simulation
    with the provided instructions. It executes the instructions step by step and keeps track of the
    state of the registers after each step, returning the final result of the simulation.

    :param param: A dictionary representing the input parameters for the URM simulation.
                  The keys are register indices (int), and the values are the initial values (int) for those registers.
    :param initial_registers: A Registers object representing the initial state of all registers.
                              This object is modified during the simulation according to the URM instructions.
    :param instructions: An Instructions object representing the set of URM instructions to be executed.
    :param safety_count: An integer specifying the maximum number of steps to simulate.
                         This prevents infinite loops in the simulation.

    :return: An URMResult object that contains information about the simulation,
             including the number of steps executed, the operations performed in each step,
             the state of the registers after each step, and the final state of the registers.

    Raises:
        AssertionError: If the input parameters are not a dictionary with integer keys and values,
                        or if the initial values are not non-negative integers,
                        or if the number of registers is insufficient for the given instructions.
    """
    return URMSimulator.forward(param=param, initial_registers=initial_registers, instructions=instructions,
                                safety_count=safety_count)
