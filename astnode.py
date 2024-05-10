# First some AST Node classes we'll use to build the AST with
class ASTNode:
    def __init__(self):
        self.name = "ASTNode"


class ASTStatementNode(ASTNode):
    def __init__(self):
        self.name = "ASTStatementNode"


class ASTExpressionNode(ASTNode):
    def __init__(self):
        self.name = "ASTExpressionNode"


class ASTSubExpressionNode(ASTExpressionNode):
    def __init__(self, expr):
        self.name = "ASTSubExpressionNode"
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_sub_expression_node(self)

class ASTFactorNode(ASTExpressionNode):
    def __init__(self, factor):
        self.name = "ASTFactorNode"
        self.factor = factor

    def accept(self, visitor):
        visitor.visit_factor_node(self)

class ASTUnaryNode(ASTExpressionNode):
    def __init__(self, expr):
        self.name = "ASTUnaryNode"
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_unary_node(self)


class ASTActualParams(ASTExpressionNode):
    def __init__(self, actual_params):
        self.name = "ASTActualParamsNode"
        self.actual_params = actual_params

    def accept(self, visitor):
        visitor.visit_actual_params_node(self)


class ASTFunctionCallNode(ASTExpressionNode):
    def __init__(self, identifier, actual_params=None):
        if actual_params is None:
            actual_params = []
        self.name = "ASTFunctionalCallNode"
        self.identifier = identifier
        self.actual_params = actual_params

    def accept(self, visitor):
        visitor.visit_function_call_node(self)


class ASTIdentifierNode(ASTExpressionNode):
    def __init__(self, lexeme):
        self.name = "ASTIdentifierNode"
        self.lexeme = lexeme

    def accept(self, visitor):
        visitor.visit_identifier_node(self)


class ASTPadRandINode(ASTStatementNode):
    def __init__(self, expr):
        self.name = "ASTPadRandINode"
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_padrandi_node(self)


class ASTAssignmentNode(ASTStatementNode):
    def __init__(self, ast_identifier_node, ast_expression_node):
        self.name = "ASTStatementNode"
        self.id = ast_identifier_node
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_assignment_node(self)


class ASTLiteralNode(ASTAssignmentNode):
    def __init__(self, literal):
        self.name = "ASTLiteralNode"
        self.literal = literal

    def accept(self, visitor):
        visitor.visit_literal_node(self)


class ASTBooleanLiteralNode(ASTLiteralNode):
    def __init__(self, value):
        self.name = "ASTBooleanLiteralNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_boolean_literal_node(self)


class ASTIntegerLiteralNode(ASTLiteralNode):
    def __init__(self, value):
        self.name = "ASTIntegerLiteralNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_integer_literal_node(self)


class ASTFloatLiteralNode(ASTLiteralNode):
    def __init__(self, value):
        self.name = "ASTFloatLiteralNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_float_literal_node(self)


class ASTColourLiteralNode(ASTLiteralNode):
    def __init__(self, value):
        self.name = "ASTColourLiteralNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_colour_literal_node(self)


class ASTPadWidthLiteralNode(ASTLiteralNode):
    def __init__(self, value):
        self.name = "ASTPadWidthLiteralNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_pad_width_literal_node(self)


class ASTPadHeightLiteralNode(ASTLiteralNode):
    def __init__(self, value):
        self.name = "ASTPadHeightLiteralNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_pad_height_literal_node(self)


class ASTPadReadNode(ASTLiteralNode):
    def __init__(self, expr1, expr2):
        self.name = "ASTPadReadNode"
        self.expr1 = expr1
        self.expr2 = expr2

    def accept(self, visitor):
        visitor.visit_padread_node(self)


class ASTBlockNode(ASTNode):
    def __init__(self):
        self.name = "ASTBlockNode"
        self.stmts = []

    def add_statement(self, node):
        self.stmts.append(node)

    def accept(self, visitor):
        visitor.visit_block_node(self)


class ASTVisitor:
    def visit_integer_literal_node(self, node):
        raise NotImplementedError()

    def visit_boolean_literal_node(self, node):
        raise NotImplementedError()

    def visit_float_literal_node(self, node):
        raise NotImplementedError()

    def visit_colour_literal_node(self, node):
        raise NotImplementedError()

    def visit_pad_width_literal_node(self, node):
        raise NotImplementedError()

    def visit_pad_height_literal_node(self, node):
        raise NotImplementedError()

    def visit_assignment_node(self, node):
        raise NotImplementedError()

    def visit_identifier_node(self, node):
        raise NotImplementedError()

    def visit_padread_node(self, node):
        raise NotImplementedError()

    def visit_padrandi_node(self, node):
        raise NotImplementedError()

    def visit_block_node(self, node):
        raise NotImplementedError()

    def inc_tab_count(self):
        raise NotImplementedError()

    def dec_tab_count(self):
        raise NotImplementedError()

    def visit_literal_node(self, node):
        raise NotImplementedError()

    def visit_actual_params_node(self, node):
        raise NotImplementedError()

    def visit_function_call_node(self, node):
        raise NotImplementedError()

    def visit_sub_expression_node(self, node):
        raise NotImplementedError()

    def visit_unary_node(self, node):
        raise  NotImplementedError()

    def visit_factor_node(self, node):
        raise  NotImplementedError

class PrintNodesVisitor(ASTVisitor):
    def __init__(self):
        self.name = "Print Tree Visitor"
        self.node_count = 0
        self.tab_count = 0

    def inc_tab_count(self):
        self.tab_count += 1

    def dec_tab_count(self):
        self.tab_count -= 1

    def visit_boolean_literal_node(self, boolean_literal_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Boolean literal:", boolean_literal_node.value)

    def visit_integer_literal_node(self, int_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Integer value::", int_node.value)

    def visit_float_literal_node(self, float_literal_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Float literal:", float_literal_node.value)

    def visit_colour_literal_node(self, colour_literal_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Colour literal:", colour_literal_node.value)

    def visit_pad_width_literal_node(self, pad_width_literal_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Pad width literal:", pad_width_literal_node.value)

    def visit_pad_height_literal_node(self, pad_height_literal_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Pad height literal:", pad_height_literal_node.value)

    def visit_assignment_node(self, ass_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Assignment node => ")
        self.inc_tab_count()
        ass_node.id.accept(self)
        ass_node.expr.accept(self)
        self.dec_tab_count()

    def visit_identifier_node(self, identifier_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Identifier => ", identifier_node.lexeme)

    def visit_block_node(self, block_node):
        self.node_count += 1
        print('\t' * self.tab_count, "New Block => ")
        self.inc_tab_count()

        for st in block_node.stmts:
            st.accept(self)

        self.dec_tab_count()

    def visit_padread_node(self, padread_node):
        self.node_count += 1
        print('\t' * self.tab_count, "PadRead node => ")
        self.inc_tab_count()
        padread_node.expr1.accept(self)
        padread_node.expr2.accept(self)
        self.dec_tab_count()

    def visit_padrandi_node(self, padrandi_node):
        self.node_count += 1
        print('\t' * self.tab_count, "PadRandI node => ")
        self.inc_tab_count()
        padrandi_node.expr.accept(self)
        self.dec_tab_count()

    def visit_literal_node(self, literal_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Literal node => ")
        self.inc_tab_count()
        literal_node.literal.accept(self)
        self.dec_tab_count()

    def visit_actual_params_node(self, actual_params_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Actual Params node => ")
        self.inc_tab_count()
        for param in actual_params_node.actual_params:
            param.accept(self)
        self.dec_tab_count()

    def visit_function_call_node(self, function_call_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Function call node => ")
        self.inc_tab_count()
        function_call_node.identifier.accept(self)
        if function_call_node.actual_params:
            for param in function_call_node.actual_params.actual_params:
                param.accept(self)
        self.dec_tab_count()

    def visit_sub_expression_node(self, sub_expression_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Sub expression node => ")
        self.inc_tab_count()
        sub_expression_node.expr.accept(self)
        self.dec_tab_count()

    def visit_unary_node(self, unary_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Unary node => ")
        self.inc_tab_count()
        unary_node.expr.accept(self)
        self.dec_tab_count()

    def visit_factor_node(self, factor_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Factor node => ")
        self.inc_tab_count()
        factor_node.factor.accept(self)
        self.dec_tab_count()

#
# # Create a print visitor instance
# print_visitor = PrintNodesVisitor()
#
# # assume root node the AST assignment node ....
# # x=23
# print("Building AST for assigment statement x=23;")
# assignment_lhs = ASTVariableNode("x")
# assignment_rhs = ASTIntegerNode(23)
# root = ASTAssignmentNode(assignment_lhs, assignment_rhs)
# root.accept(print_visitor)
# print("Node Count => ", print_visitor.node_count)
# print("----")
# # assume root node the AST variable node ....
# # x123
# print("Building AST for variable x123;")
# root = ASTVariableNode("x123")
# root.accept(print_visitor)
# print("Node Count => ", print_visitor.node_count)
