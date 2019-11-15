var_follow = ['*', '/', '+', '-', '<=', '<', '>', '>=', '==', '!=', ';', ')', ']','=',',']
term_follow = ['+', '-', '<=', '<', '>', '>=', '==', '!=', ',', ';', ')', ']']
additive_expression_prime_follow = [',', ';', ')', ']', '<=', '<', '>', '>=', '==', '!=']
selection_statment_prime2_follow = [';', '(', '{', 'if', 'while', 'return','}']
local_declaration_prime_follow = [';', '(', '{', 'if', 'while', 'return','}']
selection_statment_prime2_follow2 = ['NUM', 'ID']
args_list_prime_follow = [')',']',';']


class Parser:
    Works = []
    boi = 0
    allmighty_checker = True

    def __init__(self, money):
        self.boi = 0
        self.Works = money

    def program(self):
        if self.declaration_list() and self.Works[self.boi].dataC == '$':
            return True
        else:
            self.allmighty_checker = False
            return False

    def accept(self, value, temp):
        if value == temp:
            self.boi = self.boi + 1
            return True

    def declaration_list(self):
        if self.declaration():
            if self.declaration_list_prime():
                return True
            else:
                return False
        else:
            return False

    def declaration(self):
        if self.type_specifier():
            if self.Works[self.boi].type == 'ID':
                 if self.accept(self.Works[self.boi].type,'ID'):
                    if self.DDD():
                        return True
            return False
        else:
            return False

    def DDD(self):
        if self.var_declaration_prime():
            return True
        elif self.Works[self.boi].dataC == '(':
            if self.accept(self.Works[self.boi].dataC, '('):
                if self.params():
                   if self.Works[self.boi].dataC == ')':
                        if self.accept(self.Works[self.boi].dataC, ')'):
                            if self.compound_stmt():
                                return True
            return False
        else:
            return False

    def var_declaration(self):
        if self.type_specifier():
            if self.Works[self.boi].type == 'ID':
                if self.accept(self.Works[self.boi].type, 'ID'):
                    if self.var_declaration_prime():
                        return True
            return False
        else:
            return False

    def type_specifier(self):
        if self.Works[self.boi].dataC == 'int':
            if self.accept(self.Works[self.boi].dataC, 'int'):
                return True
        elif self.Works[self.boi].dataC == 'float':
            if self.accept(self.Works[self.boi].dataC, 'float'):
                return True
        elif self.Works[self.boi].dataC == 'void':
            if self.accept(self.Works[self.boi].dataC, 'void'):
                return True
        else:
            return False

    def params(self):
        if self.param_list():
            return True
        elif self.Works[self.boi].dataC == 'void':
            if self.accept(self.Works[self.boi].dataC, 'void'):
                return True
            return False
        else:
            return False

    def param_list(self):
        if self.param():
            if self.param_list_prime():
                return True
            return False
        else:
            return False

    def param(self):
        if self.Works[self.boi].dataC == 'int' and self.Works[self.boi+1].type == 'ID':
            if self.accept(self.Works[self.boi].dataC, 'int'):
                if self.Works[self.boi].type == 'ID':
                    if self.accept(self.Works[self.boi].type, 'ID'):
                        if self.param_prime():
                            return True
            return False
        elif self.Works[self.boi].dataC == 'float' and self.Works[self.boi+1].type == 'ID':
            if self.accept(self.Works[self.boi].dataC, 'float'):
                if self.Works[self.boi].type == 'ID':
                    if self.accept(self.Works[self.boi].type, 'ID'):
                        if self.param_prime():
                            return True
            return False
        elif self.Works[self.boi].dataC == 'void' and self.Works[self.boi+1].type == 'ID':
            if self.accept(self.Works[self.boi].dataC, 'void'):
                if self.Works[self.boi].type == 'ID':
                    if self.accept(self.Works[self.boi].type, 'ID'):
                        if self.param_prime():
                            return True
            return False
        else:
            return False

    def compound_stmt(self):
        if self.Works[self.boi].dataC == '{':
            if self.accept(self.Works[self.boi].dataC, '{'):
                if self.local_declarations():
                    if self.statement_list():
                        if self.Works[self.boi].dataC ==  '}':
                            if self.accept(self.Works[self.boi].dataC, '}'):
                                return True
            return False
        else:
            return False

    def local_declarations(self):
        if self.local_declarations_prime():
            return True
        return False

    def statement_list(self):
        if self.statement_list_prime():
            return True

    def statement(self):
        if self.expression_stmt():
            return True
        elif self.compound_stmt():
            return True
        elif self.selection_stmt():
            return True
        elif self.iteration_stmt():
            return True
        elif self.return_stmt():
            return True
        else:
            return False

    def expression_stmt(self):
        if self.expression():
            if self.Works[self.boi].dataC == ';':
                if self.accept(self.Works[self.boi].dataC, ';'):
                    return True
            return False
        elif self.Works[self.boi].dataC == ';':
                if self.accept(self.Works[self.boi].dataC, ';'):
                    return True
                else:
                    return False
        else:
            return False

    def selection_stmt(self):
        if self.Works[self.boi].dataC == 'if':
            if self.accept(self.Works[self.boi].dataC, 'if'):
                if self.Works[self.boi].dataC == '(':
                    if self.accept(self.Works[self.boi].dataC, '('):
                        if self.expression():
                            if self.Works[self.boi].dataC == ')':
                                if self.accept(self.Works[self.boi].dataC, ')'):
                                    if self.statement():
                                        if self.selection_stmt_prime():
                                            return True
        return False

    def iteration_stmt(self):
        if self.Works[self.boi].dataC == 'while':
            if self.accept(self.Works[self.boi].dataC, 'while'):
                if self.Works[self.boi].dataC == '(':
                    if self.accept(self.Works[self.boi].dataC, '('):
                        if self.expression():
                            if self.Works[self.boi].dataC == ')':
                                if self.accept(self.Works[self.boi].dataC, ')'):
                                    if self.statement():
                                        return True
        return False

    def return_stmt(self):
        if self.Works[self.boi].dataC == 'return':
            if self.accept(self.Works[self.boi].dataC, 'return'):
                if self.return_stmt_prime():
                    return True
        return False

    def expression(self):
        if self.Works[self.boi].type == 'ID':
            if self.accept(self.Works[self.boi].type, 'ID'):
                if self.FFF():
                    return True
            return False
        elif self.Works[self.boi].dataC == '(':
            if self.accept(self.Works[self.boi].dataC, '('):
                if self.expression():
                    if self.Works[self.boi].dataC == ')':
                        if self.accept(self.Works[self.boi].dataC, ')') and self.term() and self.SSS():
                            return True
            return False
        elif self.Works[self.boi].type == 'NUM':
            if self.accept(self.Works[self.boi].type, 'NUM'):
                if self.term_prime():
                    if self.SSS():
                        return True
            return False
        else:
            return False

    def FFF(self):
        if self.Works[self.boi].dataC == '(':
            if self.accept(self.Works[self.boi].dataC, '('):
                if self.args():
                    if self.Works[self.boi].dataC == ')':
                        if self.accept(self.Works[self.boi].dataC, ')'):
                            if self.term_prime():
                                if self.SSS():
                                    return True
            return False
        elif self.var_prime():
            if self.XXX():
                return True
        else:
            return False

    def XXX(self):
        if self.Works[self.boi].dataC == '=':
            if self.accept(self.Works[self.boi].dataC, '='):
                if self.expression():
                    if self.arg_list_prime():
                        return True
            return False
        elif self.term_prime():
            if self.additive_expression_prime():
                if self.SSS():
                    return True
            return False
        else:
            return False

    def var(self):
        if self.Works[self.boi].type == 'ID':
            if self.accept(self.Works[self.boi].type, 'ID') and self.var_prime():
                return True
        return False

    def SSS(self):
        if self.additive_expression_prime() and self.arg_list_prime():
            return True
        elif self.relop() and self.additive_expression() and self.arg_list_prime():
            return True
        else:
            return False

    def relop(self):
        if self.Works[self.boi].dataC == '<=':
            if self.accept(self.Works[self.boi].dataC, '<='):
                return True
        elif self.Works[self.boi].dataC == '<':
            if self.accept(self.Works[self.boi].dataC, '<'):
                return True
        elif self.Works[self.boi].dataC == '>':
            if self.accept(self.Works[self.boi].dataC, '>'):
                return True
        elif self.Works[self.boi].dataC == '>=':
            if self.accept(self.Works[self.boi].dataC, '>='):
                return True
        elif self.Works[self.boi].dataC == '==':
            if self.accept(self.Works[self.boi].dataC, '=='):
                return True
        elif self.Works[self.boi].dataC == '!=':
            if self.accept(self.Works[self.boi].dataC, '!='):
                return True
        else:
            return False

    def additive_expression(self):
        if self.term():
            if self.additive_expression_prime():
                return True
            return False
        else:
            return False

    def addop(self):
        if self.Works[self.boi].dataC == '+':
            if self.accept(self.Works[self.boi].dataC, '+'):
                return True
        elif self.Works[self.boi].dataC == '-':
            if self.accept(self.Works[self.boi].dataC, '-'):
                return True
        else:
            return False

    def term(self):
        if self.factor():
            if self.term_prime():
                return True
        return False

    def mulop(self):
        if self.Works[self.boi].dataC == '*':
            if self.accept(self.Works[self.boi].dataC, '*'):
                return True
            return False
        elif self.Works[self.boi].dataC == '/':
            if self.accept(self.Works[self.boi].dataC, '/'):
                return True
            return False
        else:
            return False

    def factor(self):
        if self.Works[self.boi].dataC == '(':
            if self.accept(self.Works[self.boi].dataC, '(') and self.expression():
                if self.Works[self.boi].dataC == ')':
                    if self.accept(self.Works[self.boi].dataC, ')'):
                        return True
            return False
        elif self.Works[self.boi].type == 'ID':
            if self.accept(self.Works[self.boi].type, 'ID') and self.factorXYZ():
                return True
            else:
                return False
        elif self.Works[self.boi].type == 'NUM':
                if self.accept(self.Works[self.boi].type, 'NUM'):
                    return True
        else:
            return False

    def factorXYZ(self):
        if self.var_prime():
            return True
        elif self.Works[self.boi].dataC == '(':
            if self.accept(self.Works[self.boi].dataC, '('):
                if self.args():
                    if self.Works[self.boi].dataC == ')':
                        if self.accept(self.Works[self.boi].dataC, ')'):
                            return True
            return False
        else:
            return False

    def args(self):
        if self.arg_list():
            return True
        elif self.Works[self.boi].dataC == ')':
            return True
        else:
            return False

    def arg_list(self):
        if self.Works[self.boi].type == 'ID':
            if self.accept(self.Works[self.boi].type, 'ID') and self.CS():
                return True
            return False
        elif self.Works[self.boi].dataC == '(':
            if self.accept(self.Works[self.boi].dataC, '('):
                if self.expression():
                    if self.Works[self.boi].dataC == ')':
                        if self.accept(self.Works[self.boi].dataC, ')') and self.term_prime() and self.FID():
                            return True
            return False
        elif self.Works[self.boi].type == 'NUM':
                if self.accept(self.Works[self.boi].type, 'NUM') and self.term_prime() and self.FID():
                    return True
        else:
            return False

    def CS(self):
        if self.var_prime() and self.EEE():
            return True
        elif self.Works[self.boi].dataC == '(':
            if self.accept(self.Works[self.boi].dataC, '('):
                if self.args() and self.Works[self.boi].dataC ==')':
                        if self.accept(self.Works[self.boi].dataC, ')') and self.term_prime() and self.FID():
                            return True
            return False
        else:
            return False

    def EEE(self):
        if self.Works[self.boi].dataC == '=':
            if self.accept(self.Works[self.boi].dataC, '=') and self.expression() and self.arg_list_prime():
                return True
            return False
        elif self.term_prime() and self.FID():
            return True
        else:
            return False

    def FID(self):
        if self.relop() and self.additive_expression() and self.arg_list_prime():
            return True
        elif self.additive_expression_prime() and self.arg_list_prime():
            return True
        else:
            return False

    def var_declaration_prime(self):
        if self.Works[self.boi].dataC == ';':
            if self.accept(self.Works[self.boi].dataC, ';'):
                return True
            return False
        elif self.Works[self.boi].dataC == '[':
            if self.accept(self.Works[self.boi].dataC, '['):
                if self.Works[self.boi].type == 'NUM':
                    if self.accept(self.Works[self.boi].type, 'NUM'):
                        if self.Works[self.boi].dataC == ']':
                            if self.accept(self.Works[self.boi].dataC, ']'):
                                if self.Works[self.boi].dataC == ';':
                                    if self.accept(self.Works[self.boi].dataC, ';'):
                                        return True
            return False
        else:
            return False

    def param_prime(self):
        if self.Works[self.boi].dataC == '[':
            if self.accept(self.Works[self.boi].dataC, '[') and self.Works[self.boi].dataC == ']':
                if self.accept(self.Works[self.boi].dataC, ']'):
                    return True
        elif self.Works[self.boi].dataC == ',' or self.Works[self.boi].dataC == ')':
            return True
        else:
            return False

    def selection_stmt_prime(self):
        if self.Works[self.boi].dataC == "else":
            if self.accept(self.Works[self.boi].dataC, 'else'):
                if self.statement():
                    return True
            return False
        elif self.Works[self.boi].dataC in selection_statment_prime2_follow or self.Works[self.boi].type in selection_statment_prime2_follow2:
            return True
        return False

    def return_stmt_prime(self):
        if self.Works[self.boi].dataC == ";":
            if self.accept(self.Works[self.boi].dataC, ';'):
                return True
            return False
        elif self.Works[self.boi].type == "ID":
            if self.accept(self.Works[self.boi].type, 'ID') and self.CCC():
                return True
            return False
        elif self.Works[self.boi].type == "NUM":
                if self.accept(self.Works[self.boi].type, 'NUM') and self.term_prime() and self.BBB():
                    return True
                return False
        elif self.Works[self.boi].dataC == "(":
            if self.accept(self.Works[self.boi].dataC, '('):
                if self.expression() and self.Works[self.boi].dataC == ")":
                        if self.accept(self.Works[self.boi].dataC, ')') and self.term_prime() and self.BBB():
                            return True
            return False
        else:
            return False

    def AAA(self):
        if self.Works[self.boi].dataC == '=':
            if self.accept(self.Works[self.boi].dataC, '=') and self.expression():
                if self.Works[self.boi].dataC == ';':
                    if self.accept(self.Works[self.boi].dataC, ';'):
                        return True
            return False
        elif self.term_prime() and self.BBB():
            return True
        else:
            return False

    def BBB(self):
        if self.relop() and self.additive_expression() and self.Works[self.boi].dataC == ';':
            if self.accept(self.Works[self.boi].dataC, ';'):
                return True
        elif self.additive_expression_prime() and self.Works[self.boi].dataC == ';':
            if self.accept(self.Works[self.boi].dataC, ';'):
                return True
        else:
            return False

    def CCC(self):
        if self.var_prime() and self.AAA():
            return True
        elif self.Works[self.boi].dataC == '(':
            if self.accept(self.Works[self.boi].dataC, '('):
                if self.args():
                    if self.Works[self.boi].dataC == ')':
                        if self.accept(self.Works[self.boi].dataC, ')') and self.term_prime() and self.BBB():
                            return True
            return False
        else:
            return False

    def declaration_list_prime(self):
        if self.declaration():
            if self.declaration_list_prime():
                return True
            return False
        elif self.Works[self.boi].dataC == '$':
            if self.boi > 1:
                if self.Works[self.boi-1].dataC == '{':
                    return False
                else:
                    return True
        else:
            return False

    def var_prime(self):
        if self.Works[self.boi].dataC in var_follow:
            return True
        elif self.Works[self.boi].dataC == '[':
            if self.accept(self.Works[self.boi].dataC, '['):
                if self.expression():
                    if self.Works[self.boi].dataC == ']':
                        if self.accept(self.Works[self.boi].dataC, ']'):
                            return True
            return False
        else:
            return False

    def param_list_prime(self):
        if self.Works[self.boi].dataC == ',':
            if self.accept(self.Works[self.boi].dataC, ',') and self.param() and self.param_list_prime():
                return True
        elif self.Works[self.boi].dataC == ')':
            return True
        else:
            return False

    def local_declarations_prime(self):
        if self.var_declaration() and self.local_declarations():
            return True
        elif self.Works[self.boi].dataC in local_declaration_prime_follow or self.Works[self.boi].type in selection_statment_prime2_follow2:
            return True
        else:
            return False

    def statement_list_prime(self):
        if self.statement() and self.statement_list_prime():
            return True
        elif self.Works[self.boi].dataC == '}':
            return True
        else:
            return False

    def additive_expression_prime(self):
        if self.addop():
            if self.term():
                if self.additive_expression_prime():
                    return True
            return False
        elif self.Works[self.boi].dataC in additive_expression_prime_follow:
            return True
        else:
            return False

    def term_prime(self):
        if self.mulop():
            if self.factor():
                if self.term_prime():
                    return True
            return False
        elif self.Works[self.boi].dataC in term_follow:
                return True
        else:
            return False

    def arg_list_prime(self):
        if self.Works[self.boi].dataC == ',':
            if self.accept(self.Works[self.boi].dataC, ','):
                if self.expression():
                    if self.arg_list_prime():
                        return True
        elif self.Works[self.boi].dataC in args_list_prime_follow:
            return True
        return False
