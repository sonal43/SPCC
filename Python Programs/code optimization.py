def constant_folding(line):
    try:
        lhs, expr = line.split("=")
        expr = eval(expr.strip())
        return f"{lhs}= {expr}"
    except:
        return line
    
def copy_propagation(code):
    variables = {'T1', 'T2', 'T3', 'T5', 'T6'}
    replace = {}
    for line in code:
        lhs, rhs = line.split("=")
        lhs = lhs.strip()
        rhs = rhs.strip()

        if rhs in variables:
            replace[lhs] = rhs

    optimized_code = []
    for line in code:
        for key, value in replace.items():
            line = line.replace(key,value)
        optimized_code.append(line)

    optimized_code_final = []
    assigned_vars = set()
    for line in optimized_code:
        lhs, rhs = line.split("=")
        lhs = lhs.strip()
        rhs = rhs.strip()
        if lhs not in assigned_vars:
            optimized_code_final.append(line)
            assigned_vars.add(lhs)
    
    return optimized_code_final

def common_subexpression_elimination(code):
    temp = {}
    for line in code:
        lhs, rhs = line.split("=")
        lhs = lhs.strip()
        rhs = rhs.strip()
        temp[lhs]=rhs
    
    optimized_code = []
    for line in code:
        lhs, rhs = line.split("=")
        lhs = lhs.strip()
        rhs = rhs.strip()
        for key, value in temp.items():
            if key!=lhs and value in rhs:
                rhs = rhs.replace(value, key)
        optimized_code.append(f"{lhs} = {rhs}")

    return optimized_code

def optimize(code):
    optimized_code = [constant_folding(line) for line in code]
    optimized_code = copy_propagation(optimized_code)
    optimized_code = common_subexpression_elimination(optimized_code)
    return optimized_code

code = """T1 = 5 * 3 + 10
T3 = T1
T2 = T1 + T3
T5 = 4 * T2
T6 = 4 * T2 + 100"""

code = code.split("\n")

optimized_code = optimize(code)
print("optimized code: ")
for line in optimized_code:
    print(line)