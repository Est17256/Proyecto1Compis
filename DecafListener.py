# Generated from Decaf.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DecafParser import DecafParser
else:
    from DecafParser import DecafParser

# This class defines a complete listener for a parse tree produced by DecafParser.
class DecafListener(ParseTreeListener):

    # Enter a parse tree produced by DecafParser#program.
    def enterProgram(self, ctx:DecafParser.ProgramContext):
        pass

    # Exit a parse tree produced by DecafParser#program.
    def exitProgram(self, ctx:DecafParser.ProgramContext):
        pass


    # Enter a parse tree produced by DecafParser#declaration.
    def enterDeclaration(self, ctx:DecafParser.DeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#declaration.
    def exitDeclaration(self, ctx:DecafParser.DeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#varDeclaration.
    def enterVarDeclaration(self, ctx:DecafParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#varDeclaration.
    def exitVarDeclaration(self, ctx:DecafParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#structDeclaration.
    def enterStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#structDeclaration.
    def exitStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#varType.
    def enterVarType(self, ctx:DecafParser.VarTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#varType.
    def exitVarType(self, ctx:DecafParser.VarTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#methodType.
    def enterMethodType(self, ctx:DecafParser.MethodTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#methodType.
    def exitMethodType(self, ctx:DecafParser.MethodTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#parameter.
    def enterParameter(self, ctx:DecafParser.ParameterContext):
        pass

    # Exit a parse tree produced by DecafParser#parameter.
    def exitParameter(self, ctx:DecafParser.ParameterContext):
        pass


    # Enter a parse tree produced by DecafParser#parameterType.
    def enterParameterType(self, ctx:DecafParser.ParameterTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#parameterType.
    def exitParameterType(self, ctx:DecafParser.ParameterTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#block.
    def enterBlock(self, ctx:DecafParser.BlockContext):
        pass

    # Exit a parse tree produced by DecafParser#block.
    def exitBlock(self, ctx:DecafParser.BlockContext):
        pass


    # Enter a parse tree produced by DecafParser#regIfS.
    def enterRegIfS(self, ctx:DecafParser.RegIfSContext):
        pass

    # Exit a parse tree produced by DecafParser#regIfS.
    def exitRegIfS(self, ctx:DecafParser.RegIfSContext):
        pass


    # Enter a parse tree produced by DecafParser#regElseS.
    def enterRegElseS(self, ctx:DecafParser.RegElseSContext):
        pass

    # Exit a parse tree produced by DecafParser#regElseS.
    def exitRegElseS(self, ctx:DecafParser.RegElseSContext):
        pass


    # Enter a parse tree produced by DecafParser#temp1.
    def enterTemp1(self, ctx:DecafParser.Temp1Context):
        pass

    # Exit a parse tree produced by DecafParser#temp1.
    def exitTemp1(self, ctx:DecafParser.Temp1Context):
        pass


    # Enter a parse tree produced by DecafParser#regMethS.
    def enterRegMethS(self, ctx:DecafParser.RegMethSContext):
        pass

    # Exit a parse tree produced by DecafParser#regMethS.
    def exitRegMethS(self, ctx:DecafParser.RegMethSContext):
        pass


    # Enter a parse tree produced by DecafParser#temp2.
    def enterTemp2(self, ctx:DecafParser.Temp2Context):
        pass

    # Exit a parse tree produced by DecafParser#temp2.
    def exitTemp2(self, ctx:DecafParser.Temp2Context):
        pass


    # Enter a parse tree produced by DecafParser#regAssigS.
    def enterRegAssigS(self, ctx:DecafParser.RegAssigSContext):
        pass

    # Exit a parse tree produced by DecafParser#regAssigS.
    def exitRegAssigS(self, ctx:DecafParser.RegAssigSContext):
        pass


    # Enter a parse tree produced by DecafParser#temp3.
    def enterTemp3(self, ctx:DecafParser.Temp3Context):
        pass

    # Exit a parse tree produced by DecafParser#temp3.
    def exitTemp3(self, ctx:DecafParser.Temp3Context):
        pass


    # Enter a parse tree produced by DecafParser#location.
    def enterLocation(self, ctx:DecafParser.LocationContext):
        pass

    # Exit a parse tree produced by DecafParser#location.
    def exitLocation(self, ctx:DecafParser.LocationContext):
        pass


    # Enter a parse tree produced by DecafParser#regDistE.
    def enterRegDistE(self, ctx:DecafParser.RegDistEContext):
        pass

    # Exit a parse tree produced by DecafParser#regDistE.
    def exitRegDistE(self, ctx:DecafParser.RegDistEContext):
        pass


    # Enter a parse tree produced by DecafParser#regClosE.
    def enterRegClosE(self, ctx:DecafParser.RegClosEContext):
        pass

    # Exit a parse tree produced by DecafParser#regClosE.
    def exitRegClosE(self, ctx:DecafParser.RegClosEContext):
        pass


    # Enter a parse tree produced by DecafParser#regLocE.
    def enterRegLocE(self, ctx:DecafParser.RegLocEContext):
        pass

    # Exit a parse tree produced by DecafParser#regLocE.
    def exitRegLocE(self, ctx:DecafParser.RegLocEContext):
        pass


    # Enter a parse tree produced by DecafParser#regOps.
    def enterRegOps(self, ctx:DecafParser.RegOpsContext):
        pass

    # Exit a parse tree produced by DecafParser#regOps.
    def exitRegOps(self, ctx:DecafParser.RegOpsContext):
        pass


    # Enter a parse tree produced by DecafParser#regLitE.
    def enterRegLitE(self, ctx:DecafParser.RegLitEContext):
        pass

    # Exit a parse tree produced by DecafParser#regLitE.
    def exitRegLitE(self, ctx:DecafParser.RegLitEContext):
        pass


    # Enter a parse tree produced by DecafParser#regMethE.
    def enterRegMethE(self, ctx:DecafParser.RegMethEContext):
        pass

    # Exit a parse tree produced by DecafParser#regMethE.
    def exitRegMethE(self, ctx:DecafParser.RegMethEContext):
        pass


    # Enter a parse tree produced by DecafParser#reg_E.
    def enterReg_E(self, ctx:DecafParser.Reg_EContext):
        pass

    # Exit a parse tree produced by DecafParser#reg_E.
    def exitReg_E(self, ctx:DecafParser.Reg_EContext):
        pass


    # Enter a parse tree produced by DecafParser#methodCall.
    def enterMethodCall(self, ctx:DecafParser.MethodCallContext):
        pass

    # Exit a parse tree produced by DecafParser#methodCall.
    def exitMethodCall(self, ctx:DecafParser.MethodCallContext):
        pass


    # Enter a parse tree produced by DecafParser#op.
    def enterOp(self, ctx:DecafParser.OpContext):
        pass

    # Exit a parse tree produced by DecafParser#op.
    def exitOp(self, ctx:DecafParser.OpContext):
        pass


    # Enter a parse tree produced by DecafParser#arith_op.
    def enterArith_op(self, ctx:DecafParser.Arith_opContext):
        pass

    # Exit a parse tree produced by DecafParser#arith_op.
    def exitArith_op(self, ctx:DecafParser.Arith_opContext):
        pass


    # Enter a parse tree produced by DecafParser#rel_op.
    def enterRel_op(self, ctx:DecafParser.Rel_opContext):
        pass

    # Exit a parse tree produced by DecafParser#rel_op.
    def exitRel_op(self, ctx:DecafParser.Rel_opContext):
        pass


    # Enter a parse tree produced by DecafParser#eq_op.
    def enterEq_op(self, ctx:DecafParser.Eq_opContext):
        pass

    # Exit a parse tree produced by DecafParser#eq_op.
    def exitEq_op(self, ctx:DecafParser.Eq_opContext):
        pass


    # Enter a parse tree produced by DecafParser#cond_op.
    def enterCond_op(self, ctx:DecafParser.Cond_opContext):
        pass

    # Exit a parse tree produced by DecafParser#cond_op.
    def exitCond_op(self, ctx:DecafParser.Cond_opContext):
        pass


    # Enter a parse tree produced by DecafParser#literal.
    def enterLiteral(self, ctx:DecafParser.LiteralContext):
        pass

    # Exit a parse tree produced by DecafParser#literal.
    def exitLiteral(self, ctx:DecafParser.LiteralContext):
        pass


    # Enter a parse tree produced by DecafParser#int_literal.
    def enterInt_literal(self, ctx:DecafParser.Int_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#int_literal.
    def exitInt_literal(self, ctx:DecafParser.Int_literalContext):
        pass


    # Enter a parse tree produced by DecafParser#char_literal.
    def enterChar_literal(self, ctx:DecafParser.Char_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#char_literal.
    def exitChar_literal(self, ctx:DecafParser.Char_literalContext):
        pass


    # Enter a parse tree produced by DecafParser#bool_literal.
    def enterBool_literal(self, ctx:DecafParser.Bool_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#bool_literal.
    def exitBool_literal(self, ctx:DecafParser.Bool_literalContext):
        pass



del DecafParser