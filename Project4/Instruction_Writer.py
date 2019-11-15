import grammar


def writeEQU(self, last, ender):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "ASSIGN"
    self.gen[len(self.gen) - 1].partA = last
    self.gen[len(self.gen) - 1].Target = ender


def iteration_instruction_write(self, rel):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "BR" + str(self.switchIT(rel)).upper()
    self.gen[len(self.gen) - 1].partA = grammar.Parser.get_last(self)
    self.gen[len(self.gen) - 1].Target = len(self.gen) + 1
    self.gen[len(self.gen) - 1].Backpatch = "bpin:" + str(len(self.gen) + 1)
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "BR"

def iteration_instruction_write2(self, backup, tempbackpatch):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "BR"
    self.gen[len(self.gen) - 1].Target = tempbackpatch
    self.gen[backup].Target = len(self.gen)
    self.gen[len(self.gen) - 1].Backpatch = "val for bpw"


def writeArgument(self, z):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "ARGS"
    if z.id == "NUM":
        self.gen[len(self.gen) - 1].Target = z.content
    else:
        self.gen[len(self.gen) - 1].Target = z.id


def writefunction(self, z):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "CALL"
    if z.id == "NUM":
        self.gen[len(self.gen) - 1].Target = z.content
    else:
        self.gen[len(self.gen) - 1].partA = z.id
    self.gen[len(self.gen) - 1].partB = len(z.paramTypes)
    self.gen[len(self.gen) - 1].Target = grammar.Parser.get_newt(self)


def writeSelection(self, rel):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "BR" + str(self.switchIT(rel)).upper()
    self.gen[len(self.gen) - 1].partA = grammar.Parser.get_last(self)
    self.gen[len(self.gen) - 1].Target = len(self.gen) + 1
    self.gen[len(self.gen) - 1].Backpatch = str(len(self.gen) -2)
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "BR"


def openBlock(self):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "BLOCK"


def closeBlock(self):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "END"
    self.gen[len(self.gen) - 1].partA = "BLOCK"


def writeElse(self):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "BR"


def writeReturnpre(self):
    self.gen.append(grammar.Instruction())
    self.gen[len(self.gen) - 1].Action = "RETURN"

def ArrayInstruct(self,value):
    self.gen.append(grammar.Instruction())
    if value == 0:
        self.gen[len(self.gen) - 1].Action = "DISP"
        self.gen[len(self.gen) - 1].partA = ""
        self.gen[len(self.gen) - 1].partB = str(int("10") * 4)
    else:
        self.gen[len(self.gen) - 1].Action = "MUL"
        self.gen[len(self.gen) - 1].partA = "4"
        if value != 0:
            self.gen[len(self.gen) - 1].partB = "ops"
        else:
            self.gen[len(self.gen) - 1].partB = "gank"
        self.gen[len(self.gen) - 1].Target = self.get_newt()
        self.gen.append(grammar.Instruction())
        self.gen[len(self.gen) - 1].Action = "DISP"
        self.gen[len(self.gen) - 1].partA = ""
        self.gen[len(self.gen) - 1].partB = self.get_last()