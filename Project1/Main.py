import sys
import re


delimitters = ['(', '{', ';', ',', '}', ')', ' ', '  ', ']', '[']
keyword = ["if", "int", "float", "while", "void", "else", "return"]
relop = ["!=", ">=", "<=", "==", ">", "<", "="]
relop2 = ("!=", ">=", "<=", "==", ">", "<")
relopOp = ("!", ">", "<", "=")
addOp = ("+", "-")
mulOp = ("*", "/")
relopBad = ["=!", "=>", "=<"]
mather = ["*", "-", "+", "/"]
counterCount = 0
boi = 0
holder = []
comCad = ["/", "*"]
finalCom = ["/*", "*/"]


def main():
    T = read()
    Toys = Lexer(T).Seperation
    coi = 0
    for line in holder:
        line = line.strip("\n")
        line = line.strip()
        print("INPUT: ", line)
        #print("Output: ")
        while coi < len(Toys):
            if Toys[coi].state is not "ENDL" and Toys[coi].dataC is not " ":
                print(Toys[coi].state, Toys[coi].dataC, sep=" : ")
            elif Toys[coi].state is "ENDL":
                coi = coi + 1
                break
            coi = coi + 1
    #Parser(Toys).test()


def read():
    f = open(sys.argv[1])
    #print("Read")
    l = []
    global holder
    for line in f:
        holder.append(line)
        for s in line:
            l.append(cNode(s, ""))
        l.append(cNode("", "ENDL"))
    #print("Returning")
    return l


class Lexer:
    def __init__(self, T):
        self.bigBoi = T

    @property
    def Seperation(self):
        newList = []
        temp = " "
        wholelist = False
        global counterCount
        commentChaser = ""
        most = len(self.bigBoi)
        global boi
        while boi < most - 1:
            s = self.bigBoi[boi]
            t = self.bigBoi[boi + 1]
            if s.state is "ENDL":
                newList.append(cNode("", "ENDL"))
                boi = boi + 1
                temp = " "
                wholelist = False
            elif s.dataC in delimitters and counterCount == 0 and wholelist is False:
                newList = self.makeUp(temp, newList, boi)
                newList.append(cNode(s.dataC, "delimit"))
                temp = " "
                commentChaser = ""
            elif re.fullmatch(r"\d+", s.dataC) and t.dataC is "." and counterCount == 0 and wholelist is False:
                temp = temp + s.dataC + t.dataC
                boi = boi + 2
                temp = self.floatFind(temp)
                newList = self.makeUp(temp, newList, boi)
                temp = self.bigBoi[boi - 1].dataC
            elif re.fullmatch(r"\d+", s.dataC) and re.fullmatch(r"[Ee]",t.dataC) and counterCount == 0 and wholelist is False:
                temp = temp + s.dataC + t.dataC
                boi = boi + 2
                temp = self.floatFind(temp)
                newList = self.makeUp(temp, newList, boi)
                temp = self.bigBoi[boi-1].dataC
            elif s.dataC in mather and s.dataC not in comCad and counterCount == 0 and wholelist is False:
                newList = self.makeUp(s.dataC, newList, boi)
                temp = " "
            elif not self.Type(s.dataC,
                               t.dataC) and t.dataC not in delimitters and s.dataC not in comCad and counterCount == 0:
                newList = self.makeUp(temp + s.dataC, newList, boi)
                temp = " "
                commentChaser = ""
            elif s.dataC in comCad and wholelist is False:
                commentChaser = commentChaser + s.dataC
                if re.fullmatch(r"/\*", commentChaser):
                    counterCount = counterCount + 1
                    commentChaser = ""
                    boi = boi + 1
                elif re.fullmatch(r"\*/", commentChaser):
                    if counterCount > 0:
                        counterCount = counterCount - 1
                        commentChaser = ""
                        boi = boi + 1
                    else:
                        newList = self.makeUp(self.bigBoi[boi - 1].dataC, newList, boi)
                        newList = self.makeUp(s.dataC, newList, boi)
                        commentChaser = ""
                elif re.fullmatch(r"//", commentChaser):
                    wholelist = True
                    commentChaser = ""
                    temp = ""
                    boi = boi + 1
                elif (self.bigBoi[boi + 1].dataC in delimitters or re.fullmatch(r"[a-zA-z0-9]+", self.bigBoi[
                    boi + 1].dataC)) and counterCount == 0:
                    newList = self.makeUp(self.bigBoi[boi].dataC, newList, boi)
                elif len(commentChaser) > 1:
                    commentChaser = s.dataC
                    boi = boi + 1
                else:
                    boi = boi + 1
            else:
                if counterCount == 0 and wholelist is False:
                    temp = temp + s.dataC
                commentChaser = ""
                boi = boi + 1
                while wholelist is True:
                    s = self.bigBoi[boi]
                    if s.state is "ENDL":
                        wholelist = False
                        break
                    boi = boi + 1
        #print("At the end")
        return newList

    def Type(self, temp1, temp2):
        temp1 = temp1.strip()
        temp2 = temp2.strip()
        if re.fullmatch(r"[A-Za-z]+", temp1) and re.fullmatch(r"[a-zA-Z]+", temp2):
            return True
        elif re.fullmatch(r"[0-9]|[0-9]+\\.?[0-9]+", temp1) and re.fullmatch(r"[0-9]|[0-9]+\\.?[0-9]+", temp2):
            return True
        else:
            return False

    def floatFind(self, temp):
        global boi
        newtemp = temp
        cake = newtemp.find("E")
        dang = newtemp.find("+")
        dang2 = newtemp.find("-")
        period = newtemp.find(".")
        good = 0
        symbol = 0
        Etype = 0
        if period != -1:
            good = 1
        if dang != -1:
            symbol = 1
        if dang2 != -1:
            symbol = 1
        if cake != -1:
            Etype = 1
        while re.fullmatch(r"\d|[Ee]|\+|-|\.", self.bigBoi[boi].dataC):
            tre = self.bigBoi[boi].dataC
            temp2 = self.bigBoi[boi+1].dataC
            if re.fullmatch(r"\.", self.bigBoi[boi].dataC):
                good = good + 1
                if good > 1:
                    boi = boi + 1
                    return newtemp
                boi = boi + 1
            elif re.fullmatch(r"\+|-", self.bigBoi[boi].dataC):
                symbol = symbol + 1
                if Etype == 1 and symbol ==1 and  re.fullmatch(r"\d",self.bigBoi[boi + 1].dataC):
                    newtemp = newtemp + self.bigBoi[boi].dataC
                    boi = boi + 1
                else:
                    return newtemp
            elif re.fullmatch(r"[Ee]", self.bigBoi[boi].dataC):
                Etype = Etype + 1
                if Etype == 1 and re.fullmatch(r"\d|\+|-",self.bigBoi[boi + 1].dataC) and re.fullmatch(r"\d",self.bigBoi[boi + 2].dataC):
                    newtemp = newtemp + self.bigBoi[boi].dataC
                    boi = boi + 1
                else:
                    return newtemp
            elif Etype + symbol is 3:
                return newtemp
            else:
                newtemp = newtemp + self.bigBoi[boi].dataC
                boi = boi + 1
        return newtemp

    def makeUp(self, temp, newList, index):
        temp = temp.strip()
        tempNew = self.bigBoi
        o = len(self.bigBoi)
        global boi
        tempNew2 = ""
        if boi < len(self.bigBoi) - 1:
            tempNew2 = tempNew[boi].dataC + tempNew[boi + 1].dataC
        if not temp.isspace():
            if temp.isalpha():
                if temp in keyword:
                    newList.append(cNode(temp, "keyword"))
                else:
                    newList.append(cNode(temp, "ID"))
                boi = boi + 1
            elif re.fullmatch("\d+(\.\d+)?(E(\+|-)?\d*)?", temp):
                boom = temp.find(".")
                first = temp.find("E")
                if first == -1 and boom == -1:
                    newList.append(cNode(temp, "int"))
                else:
                    newList.append(cNode(temp, "float"))
                boi = boi + 1
            elif tempNew2 in relop:
                newList.append(cNode(tempNew2, "relop"))
                boi = boi + 2
            elif tempNew2 in relopBad:
                newList.append(cNode(tempNew2, "Error"))
                boi = boi + 2
            elif temp in mather:
                newList.append(cNode(temp, "mathop"))
                boi = boi + 1
            elif temp in relop:
                newList.append(cNode(temp, "relop"))
                boi = boi + 1
            elif temp in delimitters:
                newList.append(cNode(temp, "delimit"))
                boi = boi + 1
            else:
                if re.fullmatch(r"[^a-zA-Z\\s]", temp):
                    newList.append(cNode(temp, "Error"))
                boi = boi + 1
        return newList


class cNode:
    def __init__(self, dataC: str, position: str, ):
        """
        :type position: str
        :type dataC: str
        :type level: int
        """
        self.dataC = dataC
        self.state = position
        self.level = 0


class Parser:
    def __init__(self, me):
        """
        :type me: list
        """
        self.letgo = me


   # def test(self):
    #    terp = (lambda b,x:b[x],grammar.toReturn)


        #x = list(map(lambda x, y: x in y, "IF", terp))
    #    print(list(terp),sep="((")


main()


