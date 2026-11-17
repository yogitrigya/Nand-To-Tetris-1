import os
import re
import sys

DEST = {"": "000", "M": "001", "D": "010", "MD": "011", "DM": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111", "ADM": "111"}

JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

# The a-bit (A or M) followed by the six ALU control bits.
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}

PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
PREDEFINED.update({f"R{i}": i for i in range(16)})


def is_name(name):
    """A symbol may not start with a digit."""
    return re.fullmatch(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*", name) is not None


def assemble(asm_path):
    symbols = dict(PREDEFINED)
    program = []                                    
    errors = []                                     

    # First reading: remove comments and blank lines, note where each label is.
    for number, line in enumerate(open(asm_path), 1):
        text = "".join(line.split("//")[0].split())  # no comment, no spaces
        if not text:
            continue
        if text.startswith("("):
            if text.endswith(")") and is_name(text[1:-1]):
                symbols[text[1:-1]] = len(program)  # address of the next instruction
            else:
                errors.append((number, text))
        else:
            program.append((number, text))

    # Second reading: turn every instruction into 16 bits.
    binary = []
    next_variable = 16
    for number, text in program:
        if text.startswith("@"):                    # A-instruction
            name = text[1:]
            if name.isdigit() and int(name) < 32768:
                binary.append(format(int(name), "016b"))
            elif is_name(name):
                if name not in symbols:
                    symbols[name] = next_variable   
                    next_variable += 1
                binary.append(format(symbols[name], "016b"))
            else:
                errors.append((number, text))
        else:                                    
            try:
                dest, comp, jump = "", text, ""
                if "=" in comp:
                    dest, comp = comp.split("=")
                if ";" in comp:
                    comp, jump = comp.split(";")
                binary.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
            except (KeyError, ValueError):
                errors.append((number, text))
    return binary, errors


def main():
    asm_path = sys.argv[1]
    binary, errors = assemble(asm_path)

    if errors:
        for number, text in sorted(errors):
            print(f"Line {number}: invalid instruction '{text}'")
        sys.exit(1)                                 

    with open(os.path.splitext(asm_path)[0] + ".hack", "w") as f:
        f.write("\n".join(binary) + "\n")


if __name__ == "__main__":
    main()
