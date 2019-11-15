class TreeNode:

    def __init__(self, token):
        self.token = token
        self.lChild = None
        self.rChild = None
        self.parent = None


class Tree:

    def __init__(self):
        self.root = None
        self.nodeList = []
        self.holder = []

    def addNextOp(self, opTok):
        """if the current root is an operand, set the root as the new op and the operand as the left child"""
        opNode = TreeNode(opTok)
        if self.root is None:
            self.holder.append(opNode)
            return
        else:
            if len(self.holder) > 0:
                for b in self.holder:
                    x = b
                    self.holder.remove(b)
                    self.addNextOp(x.token)

        self.nodeList.append(opNode)
        if self.root.token.type in ["INTEGER", "ID", "FLOAT"]:  # if root is operand
            # temp = self.root
            opNode.lChild = self.root
            self.root = opNode
            opNode.lChild.parent = opNode
        else:  # otherwise, root is an OP
            if opNode.token.dataC in ["*", "/"]:  # if new op is mulop
                # go to the right-most non-leaf
                currNode = self.root
                if currNode.rChild is not None:
                    while currNode.rChild.token.type not in ["INTEGER", "ID", "FLOAT"]:
                        currNode = currNode.rChild
                if currNode.token.dataC in ["*", "/"]:  # if right-most non-leaf is mulop
                    # shift right-most op left and replace
                    opNode.parent = currNode.parent
                    opNode.lChild = currNode
                    currNode.parent = opNode
                    if opNode.parent is not None:
                        opNode.parent.rChild = opNode
                    else:
                        self.root = opNode
                else:  # otherwise, addop or relop
                    # insert new op as right-most op
                    opNode.parent = currNode
                    opNode.lChild = currNode.rChild
                    currNode.rChild = opNode
                    if opNode.lChild is not None:
                        opNode.lChild.parent = opNode
            elif opNode.token.dataC in ["*", "/"]:  # if new op is addop
                currNode = self.root
                while currNode.rChild.token.type not in ["INTEGER", "ID", "FLOAT"] and \
                        currNode.token.dataC not in ["+", "-"]:  # get right-most op or addop
                    currNode = currNode.rChild
                if currNode.token.dataC in ["+", "-"]:  # if addop found
                    # shift right-most addop left and replace
                    opNode.parent = currNode.parent
                    opNode.lChild = currNode
                    currNode.parent = opNode
                    if opNode.parent is not None:
                        opNode.parent.rChild = opNode
                    else:
                        self.root = opNode
                else:  # otherwise, relop found
                    # insert new op as right-most op
                    opNode.parent = currNode
                    opNode.lChild = currNode.rChild
                    currNode.rChild = opNode
                    opNode.lChild.parent = opNode
            else:  # new op is relop
                # shift root left and replace
                currNode = self.root
                opNode.parent = currNode.parent  # should be None anyways
                opNode.lChild = currNode
                currNode.parent = opNode
                if opNode.parent is not None:  # should always be None
                    opNode.parent.rChild = opNode
                else:
                    self.root = opNode

    def addNextOperand(self, operandTok):
        operandNode = TreeNode(operandTok)
        self.nodeList.append(operandNode)
        currNode = self.root
        if currNode is None:
            self.root = operandNode
            return
        while currNode.rChild is not None:
            currNode = currNode.rChild
        currNode.rChild = operandNode
