import linecache

def get_rules(filename):
    f = open(filename)
    rule_list = []
    d = {}
    for num, line in enumerate(f, 1):
        message = "on line number " + str(num) + ", which is this\n"
        message += "    " + line
        line = line.rstrip()
        rule = line.split(' ')
        if len(rule[0]) == 0: #works
            continue
        elif rule[0][0] == '#': continue #works
        elif len(rule) > 5: #works
            message += "there are too many tokens with "
            message += str(len(rule))
            message += " seen. \n   5 are needed"
            print(message)
            raise SystemExit
        elif len(rule) < 5: #works
            message += "there are too few tokens with only "
            message += str(len(rule))
            message += " seen\n  5 are needed"
            print(message)
            raise SystemExit
        if len(rule[0]) > 2: #works
            message += "the first token, representing input state, "
            message += "was\n   not an integer between 0 and 99 inclusive"
            print(message)
            raise SystemExit
        state = '0'*(2-len(rule[0])) + rule[0]
        if surr_convert(rule[1]) == -1: #works
            message += "the second token representing 'NEWS' surroundings\n"
            message += "    was not in a recognized format. it should be\n"
            message += "    from xxxx to NEWS with * allowed."
            print(message)
            raise SystemExit
        surr = surr_convert(rule[1])
        if rule[2] == '-': #works
            message += "it seems you have a dash instead of an arrow ->\n"
            message += "    perhaps there's a space between the - and the >\n"
            message += "    be sure your rule is in the form\n"
            message += "    state surr -> move newState"
            print(message)
            raise SystemExit
        elif rule[2] != '->': #works
            message += "the middle token should be an arrow: ->\n"
            message += "    instead it was " + rule[2]
            message += "\n    be sure your rule is in the form\n"
            message += "    state surr -> move newState"
            print(message)
            raise SystemExit 
        if rule[3] not in 'nNeEwWsSxX': #works
            message += "the token representing the movement direction\n"
            message += "    should be one of these: N, E, W, S, or X.\n"
            message += "    rather, it was " + rule[3]
            print(message)
            raise SystemExit
        direction = rule[3].upper()
        if len(rule[4]) > 2: #works
            message += "the last token, representing output state, "
            message += "was\n    not an integer between 0 and 99 inclusive"
            print(message)
            raise SystemExit
        newstate = '0'*(2-len(rule[4])) + rule[4]
        rule = state + surr + direction + newstate
        if state not in d:
            rule_list += [rule]
            d[state] = [surr, num]
        else:
            for i in range(int(len(d[state])/2)):
                if checksurr(surr,d[state][2*i]):
                    conflict = linecache.getline(filename,2*(i+1))
                    conflict = conflict.rstrip()
                    message += "repeat rule! the state: " + state + " surr: "
                    message += surr_deconvert(surr, d[state][2*i]) 
                    message += "\n   was already handled on line #" 
                    message += str(d[state][2*i+1]) + "\n   which reads as follows:\n   " 
                    message += conflict
                    print(message)
                    raise SystemExit
            d[state] += [surr, num]
            rule_list += [rule]

    f.close()
    return rule_list

#helper functions!
def surr_convert(surr):
    """ changes NEWS/xxxx surroundings
        to 0000/1111 surroundings.
        returns -1 if something's not 
        the way it needs to be
    """
    out = ''
    if len(surr) != 4:
        return -1
    try:
        for i in range(4):
            if surr[i] == '*':
                out += surr[i]
            elif surr[i] in 'xX':
                out += '1'
            elif surr[i] in 'NEWS':
                out += '0'
            else:
                return -1
        return out
    except: return -1

def checksurr(surr1, surr2):
    """ returns True if surr1 !!= surr2
    """
    for i in range(4):
        if surr1[i] + surr2[i] == '01' or\
                surr1[i] + surr2[i] == '10':
            return False
    return True

def surr_deconvert(surr1,surr2):
    """ converts 4 character binary
        string back to NEWS surroundings
    """
    d = {0:'N', 1:'E', 2:'W', 3:'S'}
    out = ''
    for i in range(4):
        if surr1[i] == '0':
            out += d[i]
        elif surr1[i] == '1':
            out += 'x'
        elif surr1[i] == '*':
            if surr2[i] == '*':
                out += 'x'
            elif surr2[i] == '0':
                out += d[i]
            else: out += 'x'
    return out