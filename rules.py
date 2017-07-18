rules1 = ['001***N00','000*1*W01', '000*0*E02', '0201**E02', '0200**S01', '01***1S01', '01***0X00']

def rule_converter(rule):
    """ converts old-style rules 
        into nine character string 
        used by matplotlib program
    """
    out = ''
    rule = rule.split(' ')
    state = '0'*(2-len(rule[0])) + rule[0]
    out += state
    surr = ''
    for i in range(4):
        if rule[1][i] == '*':
            surr += rule[1][i]
        elif rule[1][i] in 'xX':
            surr += '1'
        elif rule[1][i] in 'NEWS':
            surr += '0'
        else:
            raise Exception("surrounding not recognized")
    out += surr
    out += rule[3]
    newstate = '0'*(2-len(rule[4])) + rule[4]
    out += newstate
    return out

def rule_deconverter(rule):
    """ converts nine character strings
        back to old-style rules
    """
    d = {0:'N', 1:'E', 2:'W', 3:'S'}
    out = ''
    out += rule[:2]
    out += ' '
    for i in range(4):
        if rule[i+2] == '*':
            out += rule[i+2]
        elif rule[i+2] == '0':
            out += d[i]
        elif rule[i+2] == '1':
            out += 'X'
    out += ' -> '
    out += rule[6]
    out += ' '
    out += rule[7:]
    return out

#oldmazerules = ['0 x*W* -> N 0', '0 **x* -> W 2', '0 NxW* -> E 1', '0 NEW* -> S 3', 
                 #   '1 Nx** -> E 1', '1 NE*x -> S 3', '1 x*** -> N 0', '1 NE*S -> W 2', 
                 #   '2 **xS -> W 2', '2 ***x -> S 3', '2 x*WS -> N 0', '2 N*WS -> E 1', 
                 #   '3 *E*x -> S 3', '3 *ExS -> W 2', '3 *x** -> E 1', '3 xEWS -> N 0']

#maze_rules = [ rule_converter(rule) for rule in oldmazerules ]

def get_rules(filename):
    f = open(filename)
    lines = f.readlines()
    rules_list = []
    for line in lines:
        if line[0] in '0123456789':
            line = line.rstrip()
            rules_list += [line]
    f.close()
    return rules_list

hw0pr4Rules = get_rules('diamondrules.txt')
rules2 = [rule_converter(rule) for rule in hw0pr4Rules]