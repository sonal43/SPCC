def left_recursion(rules):
    temp = {}
    for lhs, productions in rules.items():
        alpharules = []
        betarules = []
        for production in productions:
            if production[0]==lhs:
                alpharules.append(production[1:])
            else:
                betarules.append(production)
        
        lhs_ = lhs + "'"
        if len(alpharules)!=0:
            for b in range(len(betarules)):
                betarules[b].append(lhs_)
        
            rules[lhs] = betarules

            for a in range(len(alpharules)):
                alpharules[a].append(lhs_)
            alpharules.append(['#'])

            temp[lhs_] = alpharules
    
    for lhs_ in temp.keys():
        rules[lhs_] = temp[lhs_]
    
    return rules

rules = {
    'S' : [['(','L',')'],['x']],
    'L' : [['L',',','S'],['S']]
}

new_rules = left_recursion(rules)

for lhs, rule in new_rules.items():
    print(f"{lhs} -> {[''.join(x) for x in rule]}")