import sys
import re
import grammar


class Lexer():
    def __init__(self):
        self.lexer = [
            ('FLOAT', r'([-+]?\d+(?:(?:\.\d+)?[eE][-+]?\d+|\.\d+))'),
            ('OPEN_PAREN', r'\('), ('CLOSE_PAREN', r'\)'), ('CLOSE_CURLY', r'\}'),
            ('OPEN_CURLY', r'\{'), ('OPEN_BRACK', r'\['), ('CLOSE_BRACK', r'\]'), ('SEMI_COLON', r'\;'),
            ('NOTEQUAL', r'!='), ('DEQUAL', r'=='), ('GREATE', r'>='), ('LESSE', r'<='), ('EQUAL', r'='),
            ('LESS', r'<'), ('GREAT', r'>'), ('SUM', r'\+'), ('SUB', r'-'), ("MUL", r'\*'), ('DIV', r'/'),
            ('INTEGER', r'\d+'), ('ENDL', r'\n'), ('KEYWORD_INT', r'int'), ('KEYWORD_WHILE', r'while'),
            ('SPACE', r'\s'),
            ('KEYWORD_IF', r'if'), ('KEYWORD_RETURN', r'return'), ('KEYWORD_ELSE', r'else'), ('KEYWORD_void', r'void'),
            ('KEYWORD_float', r'float'),
            ('ID', r'[A-Za-z]+'), ('COMMA', r','), ('ERROR', r'[^A-Za-z0-9]|[^A-Za-z0-9]\W+')
        ]

    def get_lexer(self):
        return self.lexer


class cNode:
    dataC = ""
    type = ""

    def __init__(self, data, sake):
        self.dataC = data
        self.type = sake


lexer = Lexer().get_lexer()
l = []
holder = []
picks = open(sys.argv[1]).read()
bean = int(0)
cCounter = 0
poon = str()
pie = []
test = str()
final = []
if len(picks) == 0:
    print("REJECT")
    exit(0)
while bean < len(picks) - 2:
    test = str(picks[bean]) + str(picks[bean + 1])
    if re.match(r"/\*", test):
        cCounter = cCounter + 1
        bean = bean + 2
    elif re.match(r"\*/", test) and cCounter > 0:
        cCounter = cCounter - 1
        bean = bean + 2
    elif re.search(r"//", test) and cCounter == 0:
        me = bean
        while me < len(picks):
            if re.match(r"\n", picks[me] + picks[me + 1]):
                break
            else:
                me = me + 1
        bean = me
    elif cCounter == 0:
        poon = poon + str(picks[bean])
        bean = bean + 1
    else:
        bean = bean + 1
if cCounter == 0:
    poon = poon + str(picks[bean] + picks[bean + 1])
test = ""
for items in poon:
    test = test + str(items)
    if items == "\n":
        pie.append(test.strip(" "))
        test = ""
pie.append(test)
lep = len(lexer)
for cool in pie:
    while len(cool) != 0:
        x = 0
        while x != lep:
            name, pat = lexer[x]
            boom = re.match(pat, cool)
            if boom:
                final.append((name, boom.group(0)))
                toy = len(boom.group(0))
                cool = cool[toy:]
                x = 0
                spot = lexer[x]
            else:
                x = x + 1
z = 0
tank = []
for mel in final:
    name, gank = mel
    if gank is not ' ' and gank is not '\n' and gank is not '\t':
        # print(mel)
        tank.append(cNode(gank, name))
tank.append(cNode('$', 'END'))
scoon = grammar.Parser(tank)
scoon.start()
