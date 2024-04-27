from tabulate import tabulate

def check_register_map(var, register_map):
    if var in register_map:
        return register_map[var]
    else:
        return var

def register_desc(register_map):
    reg_desc = [f"{register_map[result]} contains {result}" for result in register_map.keys()]
    return reg_desc

def address_desc(register_map):
    add_desc = [f"{result} in {register_map[result]}" for result in register_map.keys()]
    return add_desc

statements = """t = a - b
u = a - c
v = t + u
d = v + u"""
statements = statements.split("\n")
output_table = []
register_map = {}
available_registers = ['R0','R1','R2','R3']
assembly_code = {}

for i, statement in enumerate(statements):
    result, assign, arg1, op, arg2 = statement.split()
    if arg1 not in list(register_map):
        register_map[arg1] = available_registers.pop(0)
        reg = register_map[arg1]
        assembly = f"MOV {arg1},{reg}"
        assembly_code[statement] = [assembly]
    
    assembly = {
        '+': f"ADD {check_register_map(arg2, register_map)}, {register_map[arg1]}",
        '-': f"SUB {check_register_map(arg2, register_map)}, {register_map[arg1]}",
        '*': f"MUL {check_register_map(arg2, register_map)}, {register_map[arg1]}",
        '/': f"DIV {check_register_map(arg2, register_map)}, {register_map[arg1]}"
    }.get(op,0)

    register_map[result] = register_map.pop(arg1)

    if statement not in list(assembly_code.keys()):
        assembly_code[statement] = [assembly]
    else:
        assembly_code[statement].append(assembly)
    reg_desc = register_desc(register_map)
    add_desc = address_desc(register_map)
    if i == len(statements)-1:
        add_desc.append("and memory")
    output_table.append([statement, assembly_code[statement],reg_desc,add_desc])

last_line = f"MOV {register_map[result]}, {result}"
assembly_code[statement].append(last_line)

formatted_rows = []
for row in output_table:
    code_gen = '\n'.join(row[1])
    reg_desc = '\n'.join(row[2])
    add_desc = '\n'.join(row[3])
    formatted_rows.append([row[0],code_gen, reg_desc,add_desc])

print(tabulate(formatted_rows, headers=["Statements", "Assembly Code", "Registers Description","Address Description"], tablefmt="grid"))