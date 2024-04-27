def quadruple(op, arg1=None, arg2=None, result=None):
    return (op, arg1, arg2, result)

def triple(op, arg1=None, arg2=None):
    return (op, arg1, arg2)

def infix_to_postfix(expression):
    precedence = {'+':1, '-':1, '*':2, '/':2}
    stack = []
    postfix = []
    tokens = expression.split()

    for token in tokens:
        if token.isalpha() or token.isalpha():
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1]!='(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1]!='(' and precedence.get(token, 0) <= precedence.get(stack[-1],0):
                postfix.append(token)
            stack.append(token)
    
    while stack:
        postfix.append(stack.pop())

    return postfix


def generate_3ac(expression):
    postfix = infix_to_postfix(expression)
    stack = []
    quadruples = []
    triples = []
    results = []
    temp_count = 0

    for token in postfix:
        if token.isdigit() or token.isalpha():
            stack.append(token)
        else:
            if token == "=":
                arg1 = stack.pop()
                result = stack.pop()
                arg2 = ""
            else:
                arg2 = stack.pop()
                arg1 = stack.pop()
                result = f"t{temp_count}"
                
            results.append(result)

            quadruples.append(quadruple(token, arg1, arg2, result))

            for item in results:
                if item == arg1:
                    arg1 = results.index(item)
                    arg1 = f"[{arg1}]"
                if item == arg2:
                    arg2 = results.index(item)
                    arg2 = f"[{arg2}]"
                if token == "=":
                    arg2 = result
                    
            triples.append(triple(token, arg1, arg2))
            stack.append(result)
            temp_count += 1
    
    return quadruples,triples

def print_table(data, header):
    print(" " * 10, end="")
    for item in header:
        print(f"{item:<10}", end="")
    print()
    for i, row in enumerate(data):
        print(f"{i:<10}", end="")
        for item in row:
            print(f"{item:<10}", end="")
        print()

expression = input("Enter the expression: ")
quadruples , triples = generate_3ac(expression)

print("\n3 Address Code:")
for quad in quadruples:
    if quad[0] == "=":
        print(f"{quad[3]} {quad[0]} {quad[1]}")
    else:
        print(f"{quad[3]} = {quad[1]} {quad[0]} {quad[2]}")

quadruples_data = [[quad[0], quad[1], quad[2], quad[3]] for quad in quadruples]
quadruples_header = ["Operator", "Argument1", "Argument2", "Result"]
print("\nQuadruples:")
print_table(quadruples_data, quadruples_header)

triples_data = [[triple[0], triple[1], triple[2]] for triple in triples]
triples_header = ["Operator", "Argument1", "Argument2"]
print("\nTriples:")
print_table(triples_data, triples_header)