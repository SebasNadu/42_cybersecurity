# **Assembly Language Basics**

Assembly language is a low-level programming language that provides a close representation of machine instructions. This document explains the fundamental concepts of x86 assembly to help beginners understand how assembly works.

---

## **Registers**

Registers are small, fast storage areas within the CPU used for operations.

### **General Purpose Registers**

1. **EAX (Accumulator):**

   - Used for arithmetic and logic operations.
   - Stores function return values.

2. **EBX (Base):**

   - General-purpose but traditionally holds base addresses in memory operations.

3. **ECX (Counter):**

   - Used as a loop counter or for repetitive instructions.

4. **EDX (Data):**
   - Assists EAX in division/multiplication.
   - Also used in input/output operations.

---

### **Special Purpose Registers**

1. **EBP (Base Pointer):**

   - Points to the base of the current stack frame.
   - Used to access local variables and function arguments.

2. **ESP (Stack Pointer):**

   - Points to the top of the stack.
   - Changes dynamically during function calls, variable pushes, and pops.

3. **EIP (Instruction Pointer):**

   - Holds the memory address of the next instruction to execute.

4. **EFLAGS:**
   - Contains status flags like Zero Flag (ZF), Carry Flag (CF), etc., used for conditional operations.

---

## **Assembly Instructions**

### **Data Movement**

- **`movl`**: Moves data from one location to another.

  ```assembly
  movl $0x5, %eax   # Moves the value 5 into the EAX register
  movl %ebx, %ecx   # Copies the value from EBX to ECX
  ```

### **Arithmetic and Logic**

- **`addl` / `subl`**: Addition and subtraction.

  ```assembly
  addl $1, %eax     # Increments EAX by 1
  subl $2, %ebx     # Decrements EBX by 2
  ```

- **`xorl`**: Logical XOR, often used to clear registers (`xorl %eax, %eax` sets EAX to 0).

### **Comparison and Jump**

- **`cmpl`**: Compares two values by subtracting them (without storing the result).

  ```assembly
  cmpl $0x0, %eax   # Compares EAX with 0
  ```

- **Jump instructions**:

  - **`je` (Jump if Equal)**: If the comparison result is 0 (values are equal).
  - **`jne` (Jump if Not Equal)**: If the result is not 0.
  - **`jmp` (Unconditional Jump)**: Always jumps to a specific address.

  ```assembly
  jne 0x1234        # Jumps to address 0x1234 if comparison result ≠ 0
  ```

---

## **Stack Operations**

The stack is a Last-In-First-Out (LIFO) structure for storing temporary data.

### Common Instructions

- **`pushl`**: Pushes a value onto the stack.

  ```assembly
  pushl %eax        # Pushes EAX onto the stack
  ```

- **`popl`**: Pops a value from the stack.

  ```assembly
  popl %ebx         # Pops the top value from the stack into EBX
  ```

- **Function Call Mechanism:**
  - **`call`**: Pushes the return address onto the stack and jumps to the called function.
  - **`ret`**: Pops the return address from the stack and jumps back.

---

## **Memory Addressing**

Assembly allows direct manipulation of memory using addresses.

- **Indirect Addressing**: Access memory at the address stored in a register.

  ```assembly
  movl (%ebx), %eax  # Loads the value at the memory address in EBX into EAX
  ```

- **Offset Addressing**: Adds an offset to the register value for memory access.

  ```assembly
  movl 4(%ebx), %eax # Loads the value at (EBX + 4) into EAX
  ```

---

## objdump

`objdump` is a versatile tool for analyzing object files, executables, and libraries. Below are some of the most commonly used options and their descriptions:

### Popular `objdump` Options and Their Usage

#### Basic Syntax

```bash
objdump [options] <file>
```

#### Popular Options

##### 1. **`-d` / `--disassemble`**

- **Description**: Disassembles the executable sections of the file into assembly code.
- **Use Case**: Analyze the assembly instructions of a binary.
- **Example**:

  ```bash
  objdump -d my_program
  ```

##### 2. **`-S` / `--source`**

- **Description**: Displays the source code (if available) alongside the disassembly.
- **Use Case**: Useful for debugging when debugging symbols are present.
- **Example**:

  ```bash
  objdump -S my_program
  ```

##### 3. **`-t` / `--syms`**

- **Description**: Lists the symbols from the symbol table.
- **Use Case**: Identify functions, global variables, and other symbols in the binary.
- **Example**:

  ```bash
  objdump -t my_program
  ```

##### 4. **`-x` / `--all-headers`**

- **Description**: Displays all header information from the file.
- **Use Case**: Inspect detailed information such as section headers, entry points, and more.
- **Example**:

  ```bash
  objdump -x my_program
  ```

##### 5. **`-h` / `--section-headers`**

- **Description**: Lists section headers in the file, including size and memory addresses.
- **Use Case**: Identify the structure of the file, such as `.text`, `.data`, `.bss`, `.rodata` sections.
- **Example**:

  ```bash
  objdump -h my_program
  ```

##### 6. **`-r` / `--reloc`**

- **Description**: Displays relocation entries in the binary.
- **Use Case**: Debug unresolved references or dynamic linking issues.
- **Example**:

  ```bash
  objdump -r my_program
  ```

##### 7. **`-g` / `--debugging`**

- **Description**: Displays debugging information if available.
- **Use Case**: Analyze debugging details, including DWARF or STABS information.
- **Example**:

  ```bash
  objdump -g my_program
  ```

##### 8. **`-C` / `--demangle`**

- **Description**: Demangles C++ symbols to make them human-readable.
- **Use Case**: Useful when working with C++ binaries to understand symbol names.
- **Example**:

  ```bash
  objdump -C -t my_program
  ```

##### 9. **`-s` / `--full-contents`**

- **Description**: Displays the complete contents of all sections in hexadecimal.
- **Use Case**: Inspect raw data in the binary.
- **Example**:

  ```bash
  objdump -s my_program
  ```

  `-s -j <section>`

- Description: Dumps the full content of a specific section in hexadecimal format.
- Use Case: Analyze data in particular sections, such as .rodata, which often contains read-only strings or constants.
- Example:

```bash
Copy code
objdump -s -j .rodata my_program
```

This command specifically examines the .rodata section.

##### 10. **`-R` / `--dynamic-reloc`**

- **Description**: Displays the dynamic relocation entries.
- **Use Case**: Analyze dynamically linked executables or shared libraries.
- **Example**:

  ```bash
  objdump -R my_program
  ```

##### 11. **`-p` / `--private-headers`**

- **Description**: Displays information specific to the file type, such as ELF details.
- **Use Case**: Inspect internal headers of the binary.
- **Example**:

  ```bash
  objdump -p my_program
  ```

#### Combining Options

Options can be combined for more detailed analysis. For example:

```bash
objdump -d -S -C my_program
```

This command disassembles the program, includes source code, and demangles symbols.

---

## **Parche Example: Accepting Any Password**

### **Code Snippet**

```assembly
1241: 83 f8 00                      cmpl    $0x0, %eax
1244: 0f 85 16 00 00 00             jne     0x1260
```

### **Explanation**

This code:

1. Compares the value in `EAX` with `0` using `cmpl`.
2. If `EAX ≠ 0`, it jumps to address `0x1260` (`jne`).

---

### **Method 1: Replace `jne` with `nop`**

Replace `jne` (`0f 85`) with **6 `nop` instructions** (`90` opcode). This removes the conditional jump, allowing the program to accept any password.

### **Method 2: Force `EAX` to 0**

Insert this instruction before the comparison:

```assembly
b8 00 00 00 00   movl $0x0, %eax
```

This forces `EAX` to always be `0`, making the comparison always succeed.

---

## **Assembly Debugging Tools**

- **GDB (GNU Debugger):**

  - Disassemble functions: `disas main`
  - View registers: `info registers`

- **Hex Editors** (e.g., `ht` or `x64dbg`): Modify binary executables directly.

---

## **Further Concepts**

1. **Flags in EFLAGS:**

   - **Zero Flag (ZF):** Set if the result of a comparison or operation is `0`.
   - **Carry Flag (CF):** Set if an arithmetic operation generates a carry/borrow.

2. **Instruction Encoding:**

   - Each assembly instruction has a binary encoding (opcode + operands).

3. **Interrupts and System Calls:**

   - **`int 0x80`**: A system call interrupt on Linux for kernel services.

4. **Optimization Techniques:**
   - Use registers effectively to minimize memory accesses.
   - Replace conditional jumps with simpler logic where possible.
