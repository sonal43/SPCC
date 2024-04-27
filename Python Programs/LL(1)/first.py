rules = {
    'E':[['T',"E'"]],
    "E'":[['+','T',"E'"],['#']],
    'T':[['F',"T'"]],
    "T'":[['*','F',"T'"],['#']],
    'F':[['(','#',')'],['id']]
}

non_terminals = ["E", "E'","T","T'","F"]
terminals = ['+','#','*','(',')','id']

first = {}

for lhs in reversed(list(rules.keys())):
    productions = rules[lhs]
    firsts = set()
    for production in productions:
        if production[0] in terminals:
            firsts.add(production[0])
        elif production[0] in non_terminals:
            firsts.update(first[production[0]])
    first[lhs]=firsts

print(first)
                