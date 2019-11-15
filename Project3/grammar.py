import sys

expression_prime_list = [";", "[", "]", ")", "=", "<=", "<", ">", ">=", "==", "!=", "+", "-", "*", "/", ","]
expression_double_prime_list = [";", "]", ")", "<=", "<", ">", ">=", "==", "!=", "+", "-", "*", "/", ","]
var_follow = [";", ")", "]", "=", "<=", "<", ">", ">=", "==", "!=", "+", "-", "*", "/", ","]
ok_expression_prime_d1 = ["<=", "<", ">", ">=", "==", "!="]
ok_expression_prime_d2 = [";", ")", "]", ","]
allmatchs = ["ID", "INTEGER", "FLOAT"]
nummatch = ["INTEGER", "FLOAT"]
additive_expression_prime_follow = [";", ")", "<=", "<", ">", ">=", "==", "!=", "]", ","]
term_follow = [";", ")", "<=", "<", ">", ">=", "==", "!=", "+", "-", "]", ","]
factor_prime_list = ["[", ";", ")", "<=", "<", ">", ">=", "==", "!=", "+", "-", "*", "/", "]"]


def log(content):
    on = False
    if on:
        print(content)


class Symbol:

    def __init__(self, sType, sID):
        self.type = sType
        self.id = sID
        self.paramTypes = None
        self.length = None


class Scope:

    def __init__(self, pScope):
        self.symbolTable = {}  # symbol table is a dictionary

        self.next = None
        self.previous = pScope

    def isGlobalScope(self):
        if self.previous is None:
            return True
        else:
            return False


class SymbolTable:

    def __init__(self):
        self.globalScope = Scope(None)  # Global scope has no parent scope
        self.localScope = self.globalScope  # global scope is local scope initially

    def newScope(self):
        self.localScope.next = Scope(self.localScope)  # create new next scope
        self.localScope = self.localScope.next  # set local scope to next scope

    def endLocalScope(self):
        self.localScope = self.localScope.previous

    def addSymbolToLocalScope(self, sType, sID):
        if sID in self.localScope.symbolTable:
            print("REJECT")
            sys.exit(0)
        else:
            self.localScope.symbolTable[sID] = Symbol(sType, sID)

    def testVariable(self, sID):
        if self.localScope.symbolTable[sID].type == "void":
            log("variable cannot be type void")
            print("REJECT")
            sys.exit(0)

    def getSymbol(self, sID):
        currScope = self.localScope
        while currScope is not None:
            if sID in currScope.symbolTable:
                return currScope.symbolTable[sID]
            else:
                currScope = currScope.previous
        log("Symbol DNE: getSymbol()")
        print("REJECT")  # symbol not found in any scope
        sys.exit(0)

    def getFuncSymbol(self, fID):
        currScope = self.localScope
        while currScope is not None:
            if fID in currScope.symbolTable:
                x = currScope.symbolTable[fID].paramTypes
            if fID in currScope.symbolTable and currScope.symbolTable[fID].paramTypes is not None:
                return currScope.symbolTable[fID]
            else:
                currScope = currScope.previous
        log("REJECT: symbol not declared as function from this scope")
        print("REJECT")
        sys.exit(0)

    def getSymbolType(self, sid):
        currScope = self.localScope
        while currScope is not None:
            if sid in currScope.symbolTable:
                return currScope.symbolTable[sid].type
            else:
                currScope = currScope.previous
        log("Symbol DNE: getSymbolType()")
        print("REJECT")  # symbol not found in any scope
        sys.exit(0)

    def getFunctionParams(self, sid):
        currScope = self.localScope
        while currScope is not None:
            if sid in currScope.symbolTable:
                if currScope.symbolTable[sid].paramTypes is None:
                    log("symbol not a function")
                    print("REJECT")  # symbol not a function
                    sys.exit(0)
                else:
                    return currScope.symbolTable[sid].paramTypes
            else:
                currScope = currScope.previous
        log("Symbol DNE: getFunctionParams()")
        print("REJECT")  # symbol not found in any scope
        sys.exit(0)

    def getArrayLength(self, sid):
        currScope = self.localScope
        while currScope is not None:
            if sid in currScope.symbolTable:
                if currScope.symbolTable[sid].length is None:
                    log("symbol not an array")
                    print("REJECT")  # symbol not an array
                    sys.exit(0)
                else:
                    return currScope.symbolTable[sid].length
                # return currScope.symbolTable[sid].length  # None -> not an array
            else:
                currScope = currScope.previous
        log("Symbol DNE: getArrayLength()")
        print("REJECT")  # symbol not found in any scope
        sys.exit(0)

    def setParamTypes(self, fID, typeArray):
        self.globalScope.symbolTable[fID].paramTypes = typeArray

    def setSymbolArrayLength(self, sID, aLength):
        self.localScope.symbolTable[sID].length = aLength

    def isArray(self, sID):
        if self.getSymbol(sID).length is not None:
            return True
        else:
            return False

    def isFunction(self, sID):
        d = self.getFuncSymbol(sID)
        if d is not None:
            return True
        else:
            return False
        # else:
        #     return False


class Parser:

    def __init__(self, money):
        self.boi = 0
        self.Works = money
        self.Tok = self.Works[self.boi]
        self.Table = SymbolTable()
        self.fDict = {"main-declared": False, "func-stmt": False, "func-call": False, "func-returned": False}
        self.sDict = {"type-specifier": "", "ID": "", "func-ID": "", "func-type": "",
                      "param-types": [], "arg-count": 0,"call_funcID" : "","one":False}

    def testExpression(self, gank):
        """Takes a List of symbols to compare"""
        tank = []
        for symbol in gank:
            if symbol is not None:
                tank.append(symbol)
        if len(tank) == 0:  # if no symbols
            return None  # no symbols to return
        elif len(tank) == 1:  # if 1 symbol
            return tank[0]  # only 1 symbol to return
        else:  # otherwise, more than 1 symbol
            for i in range(len(tank) - 1):  # then compare symbol types
                if tank[i].type != tank[i + 1].type or 'void' in tank[i].type or 'void' in tank[i+1].type:  # if types don't match
                    log("illegal expression: testExpression()")
                    print("REJECT")  # illegal expression
                    sys.exit(0)
            return tank[0]

    def start(self):
        self.program()
        print("ACCEPT")
        sys.exit(0)

    def program(self):
        if self.Tok.dataC in ['int', 'float', 'void']:
            self.declaration_list()
            return
        else:
            print("REJECT")
            sys.exit(0)

    def accept(self, value, temp):
        if value == temp:
            self.boi = self.boi + 1
            self.Tok = self.Works[self.boi]

    def declaration_list(self):
        if self.Tok.dataC in ['int', 'float', 'void']:
            self.declaration()
            self.declaration_list_prime()
            return
        else:
            print("REJECT")
            sys.exit(0)

    def declaration(self):
        if self.Tok.dataC in ['int', 'float', 'void']:
            self.type_specifier()
            if self.Tok.type == 'ID':
                self.sDict["ID"] = self.Tok.dataC
                self.Table.addSymbolToLocalScope(self.sDict["type-specifier"], self.sDict["ID"])
                self.accept(self.Tok.type, 'ID')
                self.declaration_prime()
                return
        print("REJECT")
        sys.exit(0)

    def declaration_prime(self):
        if self.Tok.dataC in [";", "["]:
            if not self.fDict["main-declared"]:
                self.Table.testVariable(self.sDict["ID"])  # test to see if it exsit
                self.var_declaration_prime()  # goes into new recursive method
                return
        elif self.Tok.dataC == '(':
            self.sDict["func-ID"] = self.sDict["ID"]  # capture function ID
            self.sDict["func-type"] = self.Table.getSymbol(self.sDict["func-ID"]).type
            if self.fDict["main-declared"]:  # if declaring a function and main already declared
                log("REJECT in C_: main function must be last")
                print("REJECT")
                sys.exit(0)
            elif self.sDict["func-ID"] == "main":  # handle main
                if self.sDict["func-type"] != 'void':
                    print("REJECT")
                    sys.exit(0)
                self.fDict["main-declared"] = True  # raise flag
            self.Table.newScope()  # new scope for function  parameters
            self.fDict["func-stmt"] = True  # entering function statement
            self.accept(self.Tok.dataC, "(")  # way to accept values
            self.params()  # call to param function
            if self.Tok.dataC == ")":
                # semantic: give param types to current function
                self.Table.setParamTypes(self.sDict["func-ID"],
                                         self.sDict["param-types"][:])
                # accept a )
                self.accept(self.Tok.dataC, ")")
                self.compound_stmt()
                # semantic: end of fun-declaration
                if not self.fDict["func-returned"] and self.sDict["func-type"] in ["int", "float"]:
                    log("REJECT in C_: " + self.sDict["func-type"] + " function did not return")
                    print("REJECT")
                    sys.exit(0)
                self.fDict["func-returned"] = False  # reset return flag
                self.fDict["func-stmt"] = False  # exiting function statement
                return
            print("REJECT", self.Works[self.boi].dataC, self.boi)
            sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)

    def var_declaration(self):
        if self.Tok.dataC in ['int', 'float']:
            self.type_specifier()
            if self.Tok.type == 'ID':
                self.sDict["ID"] = self.Tok.dataC
                self.Table.addSymbolToLocalScope(self.sDict["type-specifier"], self.sDict["ID"])
                self.accept(self.Tok.type, 'ID')
                self.var_declaration_prime()
                return
            print("REJECT")
            sys.exit(0)
        else:
            print("REJECT")
            sys.exit(0)

    def type_specifier(self):
        if self.Tok.dataC in ['int', 'float', 'void']:
            self.sDict["type-specifier"] = self.Tok.dataC
            self.accept(self.Tok.dataC, self.Tok.dataC)
            return
        print("REJECT")
        sys.exit(0)

    def function_declaration(self):
        if self.Tok.dataC in ['int', 'float', 'void']:
            self.type_specifier()  # see the lit bit the accept that hoe
            if self.Tok.type == "ID":
                self.sDict["ID"] = self.Tok.dataC  # accept that hoe
                self.accept(self.Tok.dataC, "ID")
                if self.Tok.dataC == "(":
                    self.sDict["func-ID"] = self.sDict["ID"]  # gets function id
                    self.sDict["func-type"] = self.Table.getSymbol(self.sDict["func-ID"]).type
                    if self.fDict["main-declared"]:  # looks for already declared main
                        print("REJECT")
                        sys.exit(0)
                    elif self.sDict["func-ID"] == "main":
                        self.fDict["main-declared"] = True
                    self.Table.newScope()
                    self.fDict["func-smt"] = True
                    self.accept(self.Tok.dataC, "(")
                    self.params()
                    if self.Tok.dataC == ")":
                        self.Table.setParamTypes(self.sDict["func-IF"], self.sDict["param-types"][:])
                        self.accept(self.Tok.dataC, ")")
                        self.compound_stmt()
                        if not self.fDict["func-returned"] and self.sDict["func-type"] in ["int", "float"]:
                            print("REJECT")
                            sys.exit(0)
                        self.fDict["func-returned"] = False  # reset return flag
                        self.fDict["func-stmt"] = False  # exiting function statement
                        return
        print("REJECT")
        sys.exit(0)

    def params(self):
        self.sDict["param-types"] = []
        if self.Tok.dataC in ["int", "float"]:
            self.sDict["type-specifier"] = self.Tok.dataC
            self.sDict["param-types"].append(self.Tok.dataC)
            self.accept(self.Tok.dataC, self.Tok.dataC)
            if self.Tok.type == "ID":
                self.sDict["ID"] = self.Tok.dataC
                self.Table.addSymbolToLocalScope(self.sDict["type-specifier"], self.sDict["ID"])
                self.accept(self.Tok.type, "ID")
                self.param_prime()
                self.param_list_prime()
                return
        elif self.Tok.dataC == "void":
            self.sDict["type-specifoer"] = self.Tok.dataC
            self.sDict["param-types"].append(self.Tok.dataC)
            self.accept(self.Tok.dataC, "void")
            self.params_prime()
            return
        print("REJECT")
        sys.exit(0)

    def param_list(self):
        if self.Tok.dataC in ['int', 'float', 'void']:
            self.param()
            self.param_list_prime()
            return
        else:
            print("REJECT")
            sys.exit(0)

    def param(self):
        if self.Tok.dataC in ['int', 'float']:
            self.type_specifier()
            self.sDict["param-types"].append(self.sDict["type-specifier"])
            if self.Tok.type == "ID":
                self.sDict["ID"] = self.Tok.dataC
                self.Table.addSymbolToLocalScope(self.sDict["type-specifier"], self.sDict["ID"])
                self.accept(self.Tok.type, "ID")
                self.param_prime()
                return
        print("REJECT")
        sys.exit(0)

    def compound_stmt(self):
        log("Entering Compound")
        if self.Works[self.boi].dataC == '{':
            if self.fDict["func-stmt"]:
                self.fDict["func-stmt"] = False
            else:
                self.Table.newScope()
            self.accept(self.Tok.dataC, '{')
            self.local_declarations()
            self.statement_list()
            if self.Works[self.boi].dataC == '}':
                self.Table.endLocalScope()
                self.accept(self.Tok.dataC, '}')
                return
        print("REJECT")
        sys.exit(0)

    def local_declarations(self):
        log("Enter local Decl")
        if self.Tok.dataC in [";", "int", "float", "void", "(", "{", "}", "if", "while", "return"] \
                or self.Tok.type in ["ID", "INTEGER", "FLOAT"]:
            self.local_declarations_prime()
            return
        print("REJECT")
        sys.exit(0)

    def statement_list(self):
        if self.Tok.dataC in [";", "(", "{", "}", "if", "while", "return"] \
                or self.Tok.type in ["ID", "FLOAT", "INTEGER"]:
            self.statement_list_prime()
            return
        print("REJECT")
        sys.exit(0)

    def statement(self):
        log("Entering statement :" + self.Tok.dataC + " " + self.Tok.type)
        tem = self.Tok.dataC
        if tem in [";", "("] or self.Tok.type in ["ID", "FLOAT", "INTEGER"]:
            self.expression_stmt()
            return
        elif tem == "{":
            self.compound_stmt()
            return
        elif tem == "if":
            self.selection_stmt()
            return
        elif tem == "while":
            self.iteration_stmt()
            return
        elif tem == "return":
            self.return_stmt()
            return
        else:
            print("REJECT")
            sys.exit(0)

    def expression_stmt(self):
        if self.Tok.type in ["ID", "FLOAT", "INTEGER"] or self.Tok.dataC == "(":
            self.expression()
            if self.Tok.dataC == ";":
                self.accept(self.Tok.dataC, ";")  # accept: ;
                return
        elif self.Tok.dataC == ";":
            self.accept(self.Tok.dataC, ";")  # accept: ;
            return
        print("REJECT")
        sys.exit(0)

    def selection_stmt(self):
        if self.Tok.dataC == 'if':
            self.accept(self.Tok.dataC, 'if')
            if self.Tok.dataC == '(':
                self.accept(self.Tok.dataC, '(')
                self.expression()
                if self.Tok.dataC == ')':
                    self.accept(self.Tok.dataC, ')')
                    self.statement()
                    self.selection_stmt_prime()
                    return
        print("REJECT")
        sys.exit(0)

    def iteration_stmt(self):
        if self.Tok.dataC == 'while':
            self.accept(self.Tok.dataC, 'while')
            if self.Tok.dataC == '(':
                self.accept(self.Tok.dataC, '(')
                self.expression()
                if self.Tok.dataC == ')':
                    self.accept(self.Tok.dataC, ')')
                    self.statement()
                    return
        print("REJECT")
        sys.exit(0)

    def return_stmt(self):
        if self.Tok.dataC == 'return':
            self.fDict["func-returned"] = True
            self.accept(self.Tok.dataC, 'return')
            self.return_stmt_prime()
            return
        print("REJECT")
        sys.exit(0)

    def expression(self):
        if self.Tok.type == "ID":
            # aR'
            # semantic: check table for id
            if self.Works[self.boi + 1].dataC != "(":
                symb = self.Table.getSymbol(self.Tok.dataC)
            else:
                symb = self.Table.getFuncSymbol(self.Tok.dataC)
            self.sDict["ID"] = self.Tok.dataC  # capture ID

            # accept: ID
            self.accept(self.Tok.type, "ID")
            expr = self.expression_prime()
            return self.testExpression([symb, expr])
        elif self.Tok.type == "INTEGER" or self.Tok.type == "FLOAT":
            # bX'V'T'
            if self.Tok.type == "FLOAT":
                type = "float"
            else:
                type = "int"
            num = Symbol(type, "NUM")
            # accept: NUM
            self.accept(self.Tok.type, self.Tok.type)
            term = self.term_prime()
            adde = self.additive_expression_prime()
            sime = self.ok_expression_prime()
            return self.testExpression([num, term, adde, sime])
        elif self.Tok.dataC == "(":
            # accept: (
            self.accept(self.Tok.dataC, "(")
            expr = self.expression()
            if self.Tok.dataC == ")":
                # accept: )
                self.accept(self.Tok.dataC, ")")
                term = self.term_prime()
                adde = self.additive_expression_prime()
                sime = self.ok_expression_prime()
                return self.testExpression([expr, term, adde, sime])
        print("REJECT")
        sys.exit(0)

    def var(self):
        if self.Tok.type == 'ID':
            self.accept(self.Tok.type, 'ID')
            self.var_prime()
            return
        else:
            print("REJECT")
            sys.exit(0)

    def relop(self):
        if self.Tok.dataC == '<=':
            self.accept(self.Tok.dataC, '<=')
            return
        elif self.Tok.dataC == '<':
            self.accept(self.Tok.dataC, '<')
            return
        elif self.Tok.dataC == '>':
            self.accept(self.Tok.dataC, '>')
            return
        elif self.Tok.dataC == '>=':
            self.accept(self.Tok.dataC, '>=')
            return
        elif self.Tok.dataC == '==':
            self.accept(self.Tok.dataC, '==')
            return
        elif self.Tok.dataC == '!=':
            self.accept(self.Tok.dataC, '!=')
            return
        print("REJECT")
        sys.exit(0)

    def ok_expression(self):
        if self.Tok.type in ['ID', "INTEGER", "FLOAT"] or self.Tok.dataC == "(":
            left = self.additive_expression()
            right = self.ok_expression_prime()
            if right is not None:
                if left.type == right.type:
                    return left
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                return left
        print("REJECT")
        sys.exit(0)

    def ok_expression_prime(self):
        if self.Tok.dataC in ok_expression_prime_d1:
            self.relop()
            return self.additive_expression()
        elif self.Tok.dataC in ok_expression_prime_d2:
            return None
        print("REJECT")
        sys.exit(0)

    def additive_expression(self):
        if self.Tok.type in allmatchs:
            left = self.term()
            right = self.additive_expression_prime()
            if right is not None:
                if left.type == right.type:
                    return left
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                return left
        print("REJECT")
        sys.exit(0)

    def addop(self):
        if self.Tok.dataC == '+':
            self.accept(self.Tok.dataC, '+')
        elif self.Tok.dataC == '-':
            self.accept(self.Tok.dataC, '-')
        else:
            print("REJECT")
            sys.exit(0)

    def term(self):
        log("Enter term" + self.Tok.dataC + self.Tok.type)
        if self.Tok.type in allmatchs or self.Tok.dataC == "(":
            left = self.factor()
            right = self.term_prime()
            if right is not None:
                if left.type == right.type:
                    return left
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                return left
        print("REJECT")
        sys.exit(0)

    def mulop(self):
        if self.Tok.dataC == '*':
            self.accept(self.Tok.dataC, '*')
            return
        elif self.Tok.dataC == '/':
            self.accept(self.Tok.dataC, '/')
            return
        else:
            print("REJECT")
            sys.exit(0)

    def factor(self):
        log("Enter factor" + self.Tok.dataC + self.Tok.type)
        if self.Tok.dataC == '(':
            self.accept(self.Tok.dataC, '(')
            fact = self.expression()
            if self.Tok.dataC == ')':
                self.accept(self.Tok.dataC, ')')
                return fact
        elif self.Tok.type == 'ID':  # add check of current type
            self.sDict["ID"] = self.Tok.dataC
            fact = self.Table.getSymbol(self.sDict["ID"])
            self.accept(self.Tok.type, 'ID')
            self.factor_prime()
            return fact
        elif self.Tok.type in nummatch:
            if self.Tok.type == "FLOAT":
                type = "float"
            else:
                type = "int"
            factor = Symbol(type, "NUM")
            self.accept(self.Tok.type, self.Tok.type)
            return factor
        print("REJECT")
        sys.exit(0)

    def factor_prime(self):
        log("Enter fp" + self.Tok.dataC + self.Tok.type)
        if self.Tok.dataC in factor_prime_list:
            self.var_prime()
            return
        elif self.Tok.dataC == "(":
            if not self.Table.isFunction(self.sDict["ID"]):
                print("REJECT")
                sys.exit(0)
            fs = self.Table.getFuncSymbol(self.sDict["ID"])
            self.accept(self.Tok.dataC, "(")
            self.sDict["call_funcID"] = self.sDict["ID"]
            ag = self.args()
            if ag is None:
                ag = [Symbol("void", None)]
            if self.Tok.dataC == ")":
                if ag[0].type == "void" and fs.paramTypes[0] != "void":
                    print("REJECT")
                    sys.exit(0)
                elif len(fs.paramTypes) != len(ag):
                    print("REJECT")
                    sys.exit(0)
                elif len(fs.paramTypes) == len(ag):
                    for dank in range(len(ag)):
                        if ag[dank].length is not None:
                            if fs.paramTypes[dank] != ag[dank].type + "[]" and not self.sDict["one"]:
                                print("REJECT")
                                sys.exit(0)
                        else:
                            if fs.paramTypes[dank] != ag[dank].type:
                                print("REJECT")
                                sys.exit(0)
                self.accept(self.Tok.dataC, ")")
                return

        print("REJECT")
        sys.exit(0)

    def call(self):
        if self.Tok.type == "ID":
            self.sDict["ID"] = self.Tok.dataC
            self.accept(self.Tok.type, "ID")
            if self.Tok.dataC == "(":
                f = self.Table.getSymbol(self.sDict["ID"])
                self.accept(self.Tok.dataC, "(")
                self.args()
                if self.Tok.dataC == ")":
                    self.accept(self.Tok.dataC, ")")
                    return f
        print("REJECT")
        sys.exit(0)

    def args(self):
        log("Enter args" + self.Tok.dataC + self.Tok.type)
        if self.Tok.type in allmatchs or self.Tok.dataC == "(":
            return self.arg_list()
        elif self.Tok.dataC == ')':
            return None
        else:
            print("REJECT")
            sys.exit(0)

    def arg_list(self):
        log("Enter arg_list" + self.Tok.dataC + self.Tok.type)
        # check here for the aguments function type
        if self.Tok.type in allmatchs or self.Tok.dataC == "(":
            ar = self.expression()
            ars = self.arg_list_prime()
            if ars is None:
                return [ar]
            else:
                bigTank = [ar]
                bigTank.extend(ars)
                return bigTank
        print("REJECT")
        sys.exit(0)

    def var_declaration_prime(self):
        log("Enter var_decl_prime" + self.Tok.dataC + self.Tok.type + " " + str(self.boi))
        if self.Tok.dataC == ';':
            self.accept(self.Tok.dataC, ';')
            return
        elif self.Tok.dataC == '[':
            self.accept(self.Tok.dataC, '[')
            if self.Works[self.boi].type == 'INTEGER':  # Next couple lines are lookoing for proper array
                self.Table.setSymbolArrayLength(self.sDict["ID"],
                                                self.Tok.dataC)
                self.accept(self.Tok.type, 'INTEGER')
                if self.Tok.dataC == ']':
                    self.accept(self.Tok.dataC, ']')
                    if self.Tok.dataC == ';':
                        self.accept(self.Tok.dataC, ';')
                        return
        print("REJECT")
        sys.exit(0)

    def param_prime(self):
        log("Enter param_prime" + self.Tok.dataC + self.Tok.type)
        if self.Tok.dataC == '[':
            self.Table.setSymbolArrayLength(self.sDict["ID"], -1)
            self.sDict["param-types"][len(self.sDict["param-types"]) - 1] += "[]"

            self.accept(self.Tok.dataC, '[')
            if self.Tok.dataC == ']':
                self.accept(self.Tok.dataC, ']')
                return
        elif self.Tok.dataC == ',' or self.Tok.dataC == ')':
            return
        print("REJECT")
        sys.exit(0)

    def selection_stmt_prime(self):
        if self.Tok.dataC == "else":
            self.accept(self.Tok.dataC, 'else')
            self.statement()
            return
        elif self.Tok.dataC in [";", "(", "{", "}", "if", "while", "return"] \
                or self.Tok.type in ["ID", "INTEGER", "FLOAT"]:
            return
        else:
            print("REJECT")
            sys.exit(0)

    def return_stmt_prime(self):
        log("Enterign return_stmt_prime")
        if self.Tok.type in ["ID", "FLOAT", "INTEGER"] or self.Tok.dataC == "(":
            expr = self.expression()
            if self.sDict["func-type"] != expr.type:
                print("REJECT")
                sys.exit(0)
            elif self.sDict["func-type"] == "void":
                print("REJECT")
                sys.exit(0)
            if self.Tok.dataC == ";":
                # accept: ;
                self.accept(self.Tok.dataC, ";")
            else:
                log("REJECT in Q_")
                print("REJECT")
                sys.exit(0)
        elif self.Tok.dataC == ";":
            # semantic: func-type must be void for empty return
            if self.sDict["func-type"] != "void":
                print("REJECT")
                sys.exit(0)
            # accept: ;
            self.accept(self.Tok.dataC, ";")
            log("Leaving return_stm_prime")
        else:
            print("REJECT")
            sys.exit(0)

    def declaration_list_prime(self):
        log("Enter declaration_list_prime" + self.Tok.dataC + self.Tok.type)
        if self.Tok.dataC in ['int', 'float', 'void']:
            self.declaration()
            self.declaration_list_prime()
            return
        elif self.Tok.dataC == '$':
            if not self.fDict["main-declared"]:
                return
        else:
            print("REJECT")
            sys.exit(0)

    def var_prime(self):
        log("Enter Var_ Prime " + " " + self.Tok.dataC + " " + str(self.boi))
        if self.Tok.dataC in var_follow:
            if self.Table.isArray(self.sDict["ID"]) and self.Table.getFuncSymbol(self.sDict["call_funcID"]).paramTypes[self.sDict["arg-count"]] != str(
                    self.sDict["type-specifier"] + "[]"):
                print("REJECT")
                sys.exit(0)
            elif self.Table.getSymbol(self.sDict["ID"]).paramTypes is not None:
                print("REJECT")
                sys.exit(0)
            return None  # empty
        elif self.Tok.dataC == '[':
            self.Table.getArrayLength(self.sDict["ID"])
            self.accept(self.Tok.dataC, '[')
            ex = self.expression()
            if self.sDict["call_funcID"] != "":
                if self.Table.getFuncSymbol(self.sDict["call_funcID"]).paramTypes[self.sDict["arg-count"]] in ["int[]","float[]"]:
                    print("REJECT")
                    sys.exit(0)
            if self.Tok.dataC == ']' and ex.type == 'int':
                self.sDict["one"] = True
                self.accept(self.Tok.dataC, ']')
                return
        print("REJECT")
        sys.exit(0)

    def params_prime(self):  # params'
        if self.Tok.type == "ID":
            self.sDict["ID"] = self.Tok.dataC
            self.Table.addSymbolToLocalScope(self.sDict["type-specifier"],
                                             self.sDict["ID"])
            self.accept("self.Tok.type", "ID")
            self.param_list_prime()
            self.param_prime()
        elif self.Tok.dataC == ")":
            return  # follow
        print("REJECT")
        sys.exit(0)

    def param_list_prime(self):
        if self.Tok.dataC == ',':
            self.accept(self.Tok.dataC, ',')
            self.param()
            self.param_list_prime()
            return
        elif self.Tok.dataC == ')':
            return
        print("REJECT")
        sys.exit(0)

    def local_declarations_prime(self):
        log("Entering local decla prime")
        if self.Tok.dataC in ['int', 'float']:
            self.var_declaration()
            self.local_declarations_prime()
            return
        elif self.Tok.dataC in [";", "{", "}", "if", "while", "return"] or self.Tok.type in ["ID", "FLOAT", "INTEGER"]:
            return
        print("REJECT")
        sys.exit(0)

    def statement_list_prime(self):
        if self.Tok.dataC in [";", "(", ")", "{", 'if', "while", "return"] \
                or self.Tok.type in ["ID", "FLOAT", "INTEGER"]:
            self.statement()
            self.statement_list_prime()
            return
        elif self.Tok.dataC == '}':
            return
        print("REJECT")
        sys.exit(0)

    def expression_prime(self):
        log("Enter exp_prime " + self.Tok.dataC + " " + self.Tok.type + " " + str(self.boi))
        if self.Tok.dataC in expression_prime_list:
            # S'R''
            self.var_prime()
            return self.expression_double_prime()
        elif self.Tok.dataC == "(":
            # semantic: verify symbol is function
            if not self.Table.isFunction(self.sDict["ID"]):
                print("REJECT")
                sys.exit(0)
            Boi = self.Table.getFuncSymbol(self.sDict["ID"])
            # accept: (
            self.sDict["call_funcID"] = self.sDict["ID"]
            self.accept(self.Tok.dataC, "(")
            args = self.args()
            self.sDict["arg-count"] = 0
            if args is None:
                args = [Symbol("void", None)]
            if self.Tok.dataC == ")":
                # semantic: check function arguments
                if args[0].type == "void" and Boi.paramTypes[0] != "void":
                    print("REJECT")
                    sys.exit(0)
                elif len(Boi.paramTypes) != len(args):
                    print("REJECT")
                    sys.exit(0)
                elif len(Boi.paramTypes) == len(args):
                    for i in range(len(args)):
                        if args[i].length is not None:
                            if Boi.paramTypes[i] != args[i].type + "[]" and not self.sDict["one"]:
                                print("REJECT")
                                sys.exit(0)
                        else:
                            if Boi.paramTypes[i] != args[i].type:
                                print("REJECT")
                                sys.exit(0)
                # accept: )
                self.accept(self.Tok.dataC, ")")
                term = self.term_prime()
                adde = self.additive_expression_prime()
                sime = self.ok_expression_prime()
                return self.testExpression([term, adde, sime])
        log("REJECT in R_")
        print("REJECT")
        sys.exit(0)

    def expression_double_prime(self):
        log("Enter expression_double_prime" + self.Tok.dataC + self.Tok.type)
        if self.Tok.dataC in expression_double_prime_list:
            term = self.term_prime()
            adde = self.additive_expression_prime()
            sime = self.ok_expression_prime()
            return self.testExpression([term, adde, sime])
        elif self.Tok.dataC == "=":
            self.accept(self.Tok.dataC, "=")  # accept: =
            return self.expression()
        else:
            print("REJECT")
            sys.exit(0)

    def additive_expression_prime(self):
        log("Enter add expres prime" + self.Tok.dataC + self.Tok.type)
        if self.Tok.dataC in ["+", "-"]:
            self.addop()
            left = self.term()
            right = self.additive_expression_prime()
            if right is not None:
                if left.type == right.type:
                    return left
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                return left
        elif self.Tok.dataC in additive_expression_prime_follow:
            return None
        print("REJECT")
        sys.exit(0)

    def term_prime(self):
        if self.Tok.dataC in ["*", "/"]:
            self.mulop()
            left = self.factor()
            right = self.term_prime()
            if right is not None:
                if left.type == right.type:
                    return left
                else:
                    print("REJECT")
                    sys.exit(0)
            else:
                return left
        elif self.Tok.dataC in term_follow:
            return
        else:
            print("REJECT")
            sys.exit(0)

    def arg_list_prime(self):  # final check here for args
        log("Enter arg_list_prime" + self.Tok.dataC + self.Tok.type)
        if self.Tok.dataC == ',':
            self.accept(self.Tok.dataC, ',')
            self.sDict["arg-count"] = self.sDict["arg-count"] + 1
            a = self.expression()
            ast = self.arg_list_prime()
            if ast is None:
                return [a]
            else:
                bigboi = [a]
                bigboi.extend(ast)
                return bigboi
        elif self.Tok.dataC == ")":  # reset arg-count

            return None
        else:
            print("REJECT")
            sys.exit(0)
