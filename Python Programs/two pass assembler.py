from tabulate import tabulate

def pass_1(assembly_code):
    output_table = []
    output_lines = ''
    statements = assembly_code.split('\n')
    global address
    if 'START' in statements[0]:
        statement = statements[0]
        parts = statement.split()
        mnemonic, addr = parts
        address = addr
        start_value = get_pot(mnemonic)
        output_lines = f"(AD,{start_value}) - (C, {address})"
        output_table.append([statement, output_lines])
    else:
        print('INVALID CODE')
        return
    statements.pop(0)
    for statement in statements:
        output_lines = ''
        if any(key in statement.replace(',','').split() for key in pot.keys()):
            parts = statement.replace(',','').split()
            if parts[0] == 'END':
                end_value = get_pot(parts[0])
                output_lines, address = allocate_lc_littab(end_value, str(address))
                if len(output_lines) == 0:
                    output_line = ''
                else:
                    output_line = output_lines
                    
                output_table.append([statement, output_line])
                continue
            elif parts[0] == 'LTORG':
                output_lines = ''
                end_value = get_pot(parts[0])
                output_lines, address = allocate_lc_littab(end_value, str(address))
                output_table.append([statement, output_lines])
                continue
            elif parts[0] == 'ORIGIN':
                address = str(execute_value(parts[1]))
                output_table.append([statement,''])
                continue
            elif parts[1] == 'EQU':
                dest, mnemonic, value = parts
                lc = execute_value(value)
                symbol_table[dest] = lc
                print(symbol_table)
                output_table.append([statement,''])
                continue 
        if any(key in statement.split() for key in dl.keys()):
            symbol, mnemonic, value = statement.split()
            symbol_table[symbol] = f"{address}"
            mnemonic_value = get_dl(mnemonic)
            temp = value
            value = str(value).zfill(3)
            output_lines = f"{address} (DL,{mnemonic_value}) - {value}"
            if mnemonic_value == '01':
                address = str(int(address) + 1)
            elif mnemonic_value == '02':
                address = str(int(address) + int(temp))
            output_table.append([statement, output_lines])
            continue
        
        if statement == 'STOP':
            stop_value = get_mot(statement)
            output_lines = f"{address} (IS,{stop_value}) - -"
            output_table.append([statement, output_lines])
            address = str(int(address) + 1)
            continue

        parts = statement.split()
        if len(parts) == 2:
            mnemonic, dest = parts
            mnemonic_value = get_mot(mnemonic)
            if dest not in symbol_table:
                symbol_table[dest] = ''
            index = list(symbol_table.keys()).index(dest) + 1
            output_lines = f"{address} (IS,{mnemonic_value}) - (S,{index})"
            output_table.append([statement, output_lines])
            address = str(int(address) + 1)
            continue
        elif len(parts) > 3:
            label, mnemonic, src, dest = parts
            insert_label(label, address)
        elif len(parts) == 3:
            if parts[1] in mot:
                label, mnemonic, dest = parts
                insert_label(label, address)
                mnemonic, dest = parts
                mnemonic_value = get_mot(mnemonic)
                if dest not in symbol_table:
                    symbol_table[dest] = ''
                index = list(symbol_table.keys).index(dest) + 1
                output_lines = f"{address} (IS,{mnemonic_value}) - (S,i{index})"
                address = str(int(address) + 1)
                continue
            else:
                mnemonic, src, dest = parts
    
        mnemonic_value = get_mot(mnemonic)
        reg_value = get_reg(src)
        if '=' in dest:
            if dest in literal_table.keys():
                duplicate[dest] = dest.strip("'")
                literal_table[dest.strip("'")] = ''
            else:
                literal_table[dest] = ''
            index = list(literal_table.keys()).index(dest) + 1
            output_lines = f"{address} (IS,{mnemonic_value}) {reg_value} (L,{index})"
        elif dest not in symbol_table:
            symbol_table[dest] = ''
            index = list(symbol_table.keys()).index(dest) + 1
            output_lines = f"{address} (IS,{mnemonic_value}) {reg_value} (S,{index})"
        address = str(int(address) + 1)
        output_table.append([statement, output_lines])
    return output_table

def insert_label(label, address):
    if label not in symbol_table:
        symbol_table[label] = address
    else:
        raise ValueError('Cannot use the same label more than once')
    return

def execute_value(value):
    addr = ''
    try:
        addr = int(value)
    except ValueError:
        import re
        def replace_variables(match):
            variable = match.group(1)
            if variable in symbol_table.keys():
                return str(symbol_table[variable])
            else:
                return match.group(0)
        eval_expression = re.sub(r"([A-Za-z]\w*)(\d*)", replace_variables, value)
        addr = eval(eval_expression)
    return addr

def allocate_lc_littab(end_value, address):
    output_lines = []
    if not literal_table:
        index = 1
    else:
        index = float('inf')
    for key, value in literal_table.items():
        if value == '':
            index = min(index, list(literal_table.keys()).index(key) + 1)
            literal_table[key] = address
            key_value = str(key.strip("'=")).zfill(3)
            line = f"{address} (AD,{end_value}) - {key_value}"
            output_lines.append(line)
            address = str(int(address) + 1)
    pool_table.append(index)
    return [output_lines], address

def get_mot(mnemonic):
    return mot.get(mnemonic, 'INVALID_MOT')
    
def get_reg(reg):
    reg = reg.strip(",")
    return registers.get(reg, 'INVALID_REGISTER')

def get_dl(mnemonic):
    return dl.get(mnemonic, 'INVALID_DL')

def get_pot(mnemonic):
    return pot.get(mnemonic, 'INVALID_POT')

mot = {
    'STOP': '00',
    'ADD': '01',
    'SUB': '02',
    'MULT': '03',
    'MOVER': '04',
    'MOVEM': '05',
    'COMP': '06',
    'BC': '07',
    'DIV': '08',
    'READ': '09',
    'PRINT': '10'
}

pot = {
    'START': '01',
    'END': '02',
    'ORIGIN': '03',
    'EQU': '04',
    'LTORG': '05'
}

dl = {
    'DC': '01',
    'DS': '02'
}

registers = {
    'AREG': '01',
    'BREG': '02',
    'CREG': '03',
    'DREG': '04'
}

address = ''
symbol_table = {}
literal_table = {}
duplicate = {}
pool_table = []
assembly_code = '''START 501
A DS 1
B DS 1
C DS 1
READ A
READ B
MOVER AREG, A
ADD AREG, B
MOVEM AREG, C
PRINT C
STOP
END'''

assembly_code_2 = """START 100
A DS 3
L1 MOVER AREG, B
ADD AREG, C  
MOVEM AREG, D
D EQU A+1
L2 PRINT D
ORIGIN A-1
C DC '=5'
ORIGIN L2+1
STOP
B DC '=19'
END"""
# output_table = pass_1(assembly_code)
output_table = pass_1(assembly_code_2)
formatted_outputs = []
for row in output_table:
    source = row[0]
    if isinstance(row[1], str):
        intermediate = row[1]
    else:
        intermediate = '\n'.join([_ for _ in row[1][0]])
    formatted_outputs.append([source, intermediate])
print(tabulate(formatted_outputs, headers=["Source code", "Intermediate Code"], tablefmt="grid"))

symbol_tab = [(index+1, key, value) for index, (key, value) in enumerate(list(symbol_table.items()))]
formatted_symbols = []
for row in symbol_tab:
    index = row[0]
    symbol_name = row[1]
    lc = row[2]
    formatted_symbols.append([index, symbol_name, lc])
print('\nSymbol Table:')
print(tabulate(formatted_symbols, headers=["Index", "Symbol Name", "LC"], tablefmt="grid"))

literal_tab = [(index+1, key, value) for index, (key, value) in enumerate(list(literal_table.items()))]
formatted_literals = []
for row in literal_tab:
    index = row[0]
    literal_name = row[1]
    if literal_name in duplicate.values():
        literal_name = "'"+row[1]+"'"
    lc = row[2]
    formatted_literals.append([index, literal_name, lc])
print('\nLiteral Table:')
print(tabulate(formatted_literals, headers=["Index", "Literal Name", "LC"], tablefmt="grid"))


formatted_pools = []
for row in pool_table:
    index = pool_table.index(row) + 1
    pool_entry = row
    formatted_pools.append([index, pool_entry])
print('\nPool Table:')
print(tabulate(formatted_pools, headers=["Index", "Pool Entry"], tablefmt="grid"))