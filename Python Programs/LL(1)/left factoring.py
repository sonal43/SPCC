def left_factoring(rules):
    new_grammar = {}

    for lhs, productions in rules.items():
        prefix = common_prefix(productions)

        if prefix:
            with_prefix = []
            without_prefix = []
            for production in productions:
                if production[:len(prefix)]==prefix:
                    with_prefix.append(production[len(prefix):])
                else:
                    without_prefix.append(production)
            
            lhs_ = lhs + "'"
            new_grammar[lhs] = [prefix + [lhs_]]
            new_grammar[lhs_] = without_prefix

            if with_prefix:
                new_grammar[lhs_].extend(with_prefix)
        
        else:
            new_grammar[lhs] = productions
    return new_grammar

def common_prefix(productions):
    if not productions:
        return []
    prefix = productions[0]
    for production in productions:
        length = min(len(prefix), len(production))
        i = 0
        while i < length and production[i]==prefix[i]:
            i+=1
        prefix = prefix[:i]
    
    return prefix

rules = {
    'A' : [['b','E','+','a','c','F'],['b','E','+','F']]
}

new_rules = left_factoring(rules)

for lhs, production in new_rules.items():
    print(lhs, production)