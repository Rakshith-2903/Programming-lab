class javasimulator:
    '''
    A simple Java Virtual Machine (JVM) simulator.
    Executes a custom subset of bytecode instructions using a stack and registers.
    '''
    def __init__(self, max_stack_size=10, max_registers=10):
        self.stack = []
        self.max_stack_size = max_stack_size
        self.registers = [0] * max_registers
        self.pc = 0
        self.instructions = []

    def load_program(self, filepath):
        self.instructions = []
        with open(filepath, "r") as file:
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line and not cleaned_line.startswith("#"): # Ignore empty lines and comments (lines starting with '#')
                    self.instructions.append(cleaned_line)

    def run_pro(self):
        self.pc = 0
        while self.pc < len(self.instructions):
            intr_line = self.instructions[self.pc].split()  # Fetch the next instruction and split it into opcode and argument
            oper_code = intr_line[0].lower()
            arg = int(intr_line[1]) if len(intr_line) > 1 else None
            self.pc += 1   # Increment PC before execution so branching instructions can override it
            self.execute_instrns(oper_code, arg) # Execute the decoded instruction

    def execute_instrns(self, op_code, arg):   # Processes an individual bytecode operation
        condition = False

        #-------------Memory and input operations-------------------
        if op_code == "ldc":
            # Load a constant value onto the stack
            if len(self.stack) >= self.max_stack_size:
                raise OverflowError("stack_overflow")
            self.stack.append(arg)
            
        elif op_code == "read":
            # Added Overflow check
            if len(self.stack) >= self.max_stack_size:
                raise OverflowError("stack_overflow")
            self.stack.append(int(input("ENTER AN INTEGER:  ")))
            
        elif op_code == "print":
            # Added Underflow check
            if not self.stack:
                raise IndexError("stack_underflow")
            print(f"Output: {self.stack.pop()}")
            
        elif op_code == "iload":
            # Added Overflow check
            if len(self.stack) >= self.max_stack_size:
                raise OverflowError("stack_overflow")
            self.stack.append(self.registers[arg])
            
        elif op_code == "istore":
            # Added Underflow check
            if not self.stack:
                raise IndexError("stack_underflow")
            self.registers[arg] = self.stack.pop()

        #-------------Math operations----------------------------
        elif op_code in ["iadd", "isub", "imul", "idiv"]:
            # Added Underflow check for math operations (needs at least 2 items)
            if len(self.stack) < 2:
                raise IndexError("stack_underflow: need two values for math operation")
            
            v2 = self.stack.pop() # Top of stack (Right operand)
            v1 = self.stack.pop() # Bottom of stack (Left operand)
            
            if op_code == "iadd":
                self.stack.append(v1 + v2)
            elif op_code == "isub":
                self.stack.append(v1 - v2) # Left minus Right!
            elif op_code == "imul":
                self.stack.append(v1 * v2)
            elif op_code == "idiv":
                # Added Division by Zero check
                if v2 == 0:
                    raise ZeroDivisionError("division by zero")
                self.stack.append(int(v1 / v2))

        #---------------Branching operations---------------------
        elif op_code in ["ifeq", "iflt", "ifgt"]:
            # Added Underflow check
            if not self.stack:
                raise IndexError("stack_underflow")
                
            value = self.stack.pop()   # Pop the top value to evaluate the condition
            
            if op_code == "ifeq" and value == 0:
                condition = True
            elif op_code == "iflt" and value < 0:
                condition = True
            elif op_code == "ifgt" and value > 0:
                condition = True

            if condition:   # If the condition is met, jump to the line specified by the argument
                self.pc = arg

        else:
            raise ValueError(f"Unknown instruction : {op_code}")

if __name__ == "__main__":
    sim = javasimulator()
    sim.load_program("test_C.txt")    # Change the filename below to test different programs
    sim.run_pro()