from sys import *


tokens = []
symbols = {}

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data
def lex(filecontents):
    tok = ""
    state = 0
    isexpr = 0
    varstarted = 0
    func = ""
    isfunc = 0
    var = ""
    string = ""
    expr = ""
    n = ""
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        #print(tok)
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0

            tok = ""

        elif tok == "=" and state == 0:
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tokens.append("EQUALS")
            tok = ""
        elif tok  == "?" and state == 0:
            varstarted = 1
            var += tok
            tok = ""
        elif varstarted == 1:
            if tok == "<" or tok == ">":
                 if var != "":
                     tokens.append("VAR:" + var)
                     var = ""
                     varstarted = 0
            var += tok
            tok = ""

        elif tok == "print:":
            #print("print")
            tokens.append("PRINT")
            tok = ""
        #Basis for functions
        #unfinished (Currently not working)
        elif tok == "{" and state == 0:
            isfunc = 1
            func += tok
            tok = ""
        elif isfunc == 1:
            if tok == "<" or tok == ">":
                if func != "":
                    tokens.append("CODE:" + func)
                    func = ""
                    isfunc = 0
            func += tok
            tok = ""


        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "/" or tok == "*":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string)
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    print(tokens)
    #print(symbols)
    #return ""
    return tokens
def doPRINT(num):
    if num[0:6] == "STRING":
        print(num[8:])
    elif num[0:3] == "NUM":
        print(num[4:])
    elif num[0:4] == "EXPR":
        print(num[5:])
def evalEXPRESSION(expr):
    return eval(expr[5:])
def doASSIGN(varname, varvalue):
    symbols[varname] = varvalue
    #print(symbols)
def getVARIABLE(varname):
    #print(varname)
    if varname in symbols:
        print(symbols[varname])
        return ""
        #return symbols[varname]
    else:
        return "TypeError: Undefined Variable"
evaledarray = []
def evalCODE(code):

    code = code[6:]
    txt = code.find("}")
    eol = code.find(";")
    line = code[:eol]
    count = code.count(";")
    line = code.split(";")
    i = 0
    while i <= len(line) - 1:
        if line[i] != "}":
            if line[i].count("\"") > 0:
                end = line[i][7:].find("\"")
                txt = line[i][7:]
                evaledarray.append(txt[:end])
            elif line[i].count("+") > 0 or line[i].count("-") > 0 or line[i].count("*") > 0 or line[i].count("/") > 0:
                txt = eval(line[i][6:])
                evaledarray.append(txt)
            else:
                evaledarray.append(line[i][6:])
        i+=1
        return ""
    #if eol != 0:
    #    line2 = code[eol:]
    #    txt = line2.find("}")
    #    line2 = line2[1:txt]
    #    line2 = line2[7:]
    #    line1 = code[:eol]
    #    line1 = line1[7:]
    #    block = line1 + "\n" + line2
    #    print(block)
    #else:
    #    print(line1)
    return evaledarray
def parse(toks):
    i = 0
    while(i < len(toks)):
        #print(toks[i] + " " + toks[i+1] + " " + toks[i+2])
        if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
            if toks[i+1][0:6] == "STRING":
                doPRINT(toks[i+1])
            elif toks[i+1][0:3] == "NUM":
                doPRINT(toks[i+1])
            elif toks[i+1][0:4] == "EXPR":
                print(evalEXPRESSION(toks[i+1]))
            elif toks[i+1][0:3] == "VAR":
                print(getVARIABLE(toks[i+1][4:]))
            i+=2
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS CODE":
            if toks[i+2][0:6] == "STRING":
                doASSIGN(toks[i][4:],  toks[i+2][8:])
            if toks[i+2][0:3] == "NUM":
                doASSIGN(toks[i][4:], toks[i+2][4:])
            if toks[i+2][0:4] == "EXPR":
                #print(toks[i+2])
                doASSIGN(toks[i][4:], evalEXPRESSION(toks[i+2]))
            if toks[i+2][0:4] == "CODE":
                doASSIGN(toks[i][4:], evalCODE(toks[i+2]))
            i+=3
            #print(symbols)
        #i+=1
def run():
    data = open_file(argv[1])
    tok = lex(data)
    parse(tok)
run()
