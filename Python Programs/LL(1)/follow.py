rules = {
    'E':[['T',"E'"]],
    "E'":[['+','T',"E'"],['#']],
    'T':[['F',"T'"]],
    "T'":[['*','F',"T'"],['#']],
    'F':[['(','#',')'],['id']]
}

non_terminals = ["E", "E'","T","T'","F"]
terminals = ['+','#','*','(',')','id']

first = {
    'E':['(','id'],
    "E'":['+','#'],
    'T':['(','id'],
    "T'":['*','#'],
    'F':['(','id']
}

follow = {nt: set() for nt in non_terminals}
follow['E'].add('$')

while True:
    updated = False
    for nt, productions in rules.items():
        for production in productions:
            for i, symbol in enumerate(production):
                if symbol in non_terminals:
                    if i == len(production)-1:
                        if follow[nt]:
                            if follow[symbol].update(follow[nt]):
                                updated = True
                    else:
                        next_symbol = production[i+1]
                        first_next_symbol = first[next_symbol]
                        if '#' in first_next_symbol:
                            if follow[nt]:
                                if follow[symbol].update(follow[nt]):
                                    updated = True
                                if follow[symbol].update(set(first_next_symbol) - {'#'}):
                                    updated = True
                        else:
                            if follow[nt]:
                                if follow[symbol].update(set(first_next_symbol)):
                                    updated = True
    if not updated:
        break

for n in non_terminals:
    f = follow[n]
    print(n,f)
