#This is where code that does not work but can offer functionality goes

**LEXER CODE**
```
elif tok == "call:":
        tokens.append("CALL")
        tok = ""
elif tok == "end":
      tokens.append("END")
      tok = ""
  elif tok == "function":
      #if var != "":
      #    tokens.append("NAME:" + var)
      #    var = ""
      tokens.append("FUNCTION")
      tok = ""
  elif tok == "do":
      tokens.append("DO")
      tok = ""
```











**PARSER CODE**
elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:4] + " " + toks[i+3][0:6] == "PRINT STRING STRING":
        print(toks[i+3][8:])
        i+=2

if toks[i][0:4] + " " + toks[i+1][0:3] == "CALL VAR":
        print(getVARIABLE(toks[i+1][4:]))
        i+=1

if toks[i] == "END":
        #print("end")
        i+=1
    elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] == "FUNCTION VAR DO":
        if toks[i+1][0:4] == "VAR:":
            t = 0
            while t < len(toks):
                if(toks[t] == "DO"):
                    #print(toks[i+1][4:])
                    #print(toks[t+1:])
                    doASSIGN(toks[i+1][4:], toks[t+1:])
                t+=1
        i+=3
        #return
