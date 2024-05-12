# First some AST Node classes we'll use to build the AST with
class ASTNode:
    def __init__(self):
        self.name = "ASTNode"


class ASTStatementNode(ASTNode):
    def __init__(self, statement):
        self.name = "ASTStatementNode"
        self.statement = statement

    def accept(self, visitor):
        visitor.visit_statement_node(self)


class ASTProgramNode(ASTNode):
    def __init__(self):
        self.name = "ASTProgramNode"
        self.stmts = []

    def add_statement(self, node):
        self.stmts.append(node)

    def accept(self, visitor):
        visitor.visit_program_node(self)


class ASTExpressionNode(ASTNode):
    def __init__(self, simple_expressions, Type=None):
        self.name = "ASTExpressionNode"
        self.simple_expressions = simple_expressions
        self.Type = Type

    def accept(self, visitor):
        visitor.visit_expression_node(self)


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


class ASTFunctionDeclarationNode(ASTStatementNode):
    def __init__(self, identifier, Type, block, formalParams=None):
        self.name = "ASTFunctionDeclarationNode"
        self.identifier = identifier
        self.formalParams = formalParams
        self.Type = Type
        self.block = block

    def accept(self, visitor):
        visitor.visit_function_declaration_node(self)


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


class ASTTermNode(ASTExpressionNode):
    def __init__(self, factor):
        self.name = "ASTTermNode"
        self.factor = factor

    def accept(self, visitor):
        visitor.visit_term_node(self)


class ASTSimpleExpressionNode(ASTExpressionNode):
    def __init__(self, term):
        self.name = "ASTSimpleExpressionNode"
        self.term = term

    def accept(self, visitor):
        visitor.visit_simple_expression_node(self)


class ASTPrintStatementNode(ASTExpressionNode):
    def __init__(self, expression):
        self.name = "ASTPrintStatementNode"
        self.expr = expression

    def accept(self, visitor):
        visitor.visit_print_statement_node(self)


class ASTDelayStatementNode(ASTExpressionNode):
    def __init__(self, expression):
        self.name = "ASTDelayStatementNode"
        self.expr = expression

    def accept(self, visitor):
        visitor.visit_delay_statement_node(self)


class ASTReturnStatementNode(ASTExpressionNode):
    def __init__(self, expression):
        self.name = "ASTReturnStatementNode"
        self.expr = expression

    def accept(self, visitor):
        visitor.visit_return_statement_node(self)


class ASTWriteStatementBoxNode(ASTExpressionNode):
    def __init__(self, expressions=None):
        if expressions is None:
            expressions = []
        self.name = "ASTWriteStatementBoxNode"
        self.expressions = expressions

    def accept(self, visitor):
        visitor.visit_write_statement_node(self)


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


class ASTForStatementNode(ASTStatementNode):
    def __init__(self, expr, block, variable_dec=None, assign=None):
        self.name = "ASTForStatementNode"
        self.variable_dec = variable_dec
        self.expr = expr
        self.assign = assign
        self.block = block

    def accept(self, visitor):
        visitor.visit_for_statement_node(self)


class ASTWhileStatementNode(ASTStatementNode):
    def __init__(self, expr, block):
        self.name = "ASTWhileStatementNode"
        self.expr = expr
        self.block = block

    def accept(self, visitor):
        visitor.visit_while_statement_node(self)


class ASTAssignmentNode(ASTStatementNode):
    def __init__(self, ast_identifier_node, ast_expression_node):
        self.name = "ASTStatementNode"
        self.id = ast_identifier_node
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_assignment_node(self)


class ASTVariableDeclarationSuffixNode(ASTStatementNode):
    def __init__(self, ast_type_node, ast_expression_node):
        self.name = "ASTVariableDeclarationSuffixNode"
        self.type = ast_type_node
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_variable_declaration_suffix_node(self)


class ASTLiteralNode(ASTAssignmentNode):
    def __init__(self, literal):
        self.name = "ASTLiteralNode"
        self.literal = literal

    def accept(self, visitor):
        visitor.visit_literal_node(self)


class ASTMultiplicativeOperatorNode(ASTNode):
    def __init__(self, multiplicative_op):
        self.name = "ASTMultiplicativeOperatorNode"
        self.multiplicative_op = multiplicative_op

    def accept(self, visitor):
        visitor.visit_multiplicative_op(self)


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


class ASTVariableDeclarationNode(ASTVariableDeclarationSuffixNode):
    def __init__(self, ast_identifier_node, ast_expression_node):
        self.name = "ASTVariableDeclarationNode"
        self.identifier = ast_identifier_node
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_variable_declaration_node(self)


class ASTIfStatementNode(ASTStatementNode):
    def __init__(self, ast_expression_node, ast_block1_node, ast_block2_node=None):
        self.block2 = ast_block2_node
        self.name = "ASTIfStatementNode"
        self.expression = ast_expression_node
        self.block1 = ast_block1_node

    def accept(self, visitor):
        visitor.visit_if_statement_node(self)


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


class ASTTypeNode(ASTLiteralNode):
    def __init__(self, value):
        self.name = "ASTTypeNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_type_node(self)


class ASTPadHeightLiteralNode(ASTLiteralNode):
    def __init__(self, value):
        self.name = "ASTPadHeightLiteralNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_pad_height_literal_node(self)


class ASTFormalParameterNode(ASTStatementNode):
    def __init__(self, identifier, type):
        self.name = "ASTFormalParameterNode"
        self.identifier = identifier
        self.type = type

    def accept(self, visitor):
        visitor.visit_formal_parameter_node(self)


class ASTFormalParametersNode(ASTStatementNode):
    def __init__(self, formal_params):
        self.name = "ASTFormalParametersNode"
        self.formal_params = formal_params

    def accept(self, visitor):
        visitor.visit_formal_params(self)


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

    def visit_for_statement_node(self, node):
        raise NotImplementedError

    def visit_while_statement_node(self, node):
        raise NotImplementedError

    def visit_type_node(self, node):
        raise NotImplementedError

    def visit_block_node(self, node):
        raise NotImplementedError()

    def visit_program_node(self, node):
        raise NotImplementedError

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
        raise NotImplementedError()

    def visit_factor_node(self, node):
        raise NotImplementedError

    def visit_term_node(self, node):
        raise NotImplementedError

    def visit_simple_expression_node(self, node):
        raise NotImplementedError

    def visit_expression_node(self, node):
        raise NotImplementedError

    def visit_variable_declaration_suffix_node(self, node):
        raise NotImplementedError

    def visit_variable_declaration_node(self, node):
        raise NotImplementedError

    def visit_if_statement_node(self, node):
        raise NotImplementedError

    def visit_print_statement_node(self, node):
        raise NotImplementedError

    def visit_delay_statement_node(self, node):
        raise NotImplementedError

    def visit_return_statement_node(self, node):
        return NotImplementedError

    def visit_write_statement_node(self, node):
        raise NotImplementedError

    def visit_statement_node(self, node):
        raise NotImplementedError

    def visit_formal_parameter_node(self, node):
        raise NotImplementedError

    def visit_formal_params(self, node):
        raise NotImplementedError

    def visit_function_declaration_node(self, node):
        raise NotImplementedError

    def visit_multiplicative_op(self, node):
        raise NotImplementedError


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

    def visit_multiplicative_op(self, multiplicative_op_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Multiplicative operator::", multiplicative_op_node.multiplicative_op)

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

    def visit_program_node(self, program_node):
        self.node_count += 1
        print('\t' * self.tab_count, "New Program => ")
        self.inc_tab_count()

        for st in program_node.stmts:
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

    def visit_type_node(self, type_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Type => ", type_node.value)

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

    def visit_write_statement_node(self, write_statement_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Write statement call node => ")
        self.inc_tab_count()
        if write_statement_node.expressions:
            for write_statement in write_statement_node.expressions:
                write_statement.accept(self)
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

    def visit_term_node(self, term_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Term node => ")
        self.inc_tab_count()
        for term in term_node.factor:
            term.accept(self)
        self.dec_tab_count()

    def visit_simple_expression_node(self, simple_expression_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Simple expression node => ")
        self.inc_tab_count()
        for simple_expr in simple_expression_node.term:
            simple_expr.accept(self)
        self.dec_tab_count()

    def visit_expression_node(self, expression_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Expression node => ")
        self.inc_tab_count()
        for simple_expr in expression_node.simple_expressions:
            simple_expr.accept(self)
        if expression_node.Type is not None:
            expression_node.Type.accept(self)
        self.dec_tab_count()

    def visit_variable_declaration_suffix_node(self, variable_declaration_suffix_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Variable declaration suffix node => ")
        self.inc_tab_count()
        variable_declaration_suffix_node.type.accept(self)
        variable_declaration_suffix_node.expr.accept(self)
        self.dec_tab_count()

    def visit_variable_declaration_node(self, variable_declaration_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Variable declaration node => ")
        self.inc_tab_count()
        variable_declaration_node.identifier.accept(self)
        variable_declaration_node.expr.accept(self)
        self.dec_tab_count()

    def visit_if_statement_node(self, if_statement_node):
        self.node_count += 1
        print('\t' * self.tab_count, "If statement node => ")
        self.inc_tab_count()
        if_statement_node.expression.accept(self)
        if_statement_node.block1.accept(self)
        if if_statement_node.block2 is not None:
            if_statement_node.block2.accept(self)
        self.dec_tab_count()

    def visit_print_statement_node(self, print_statement_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Print statement node => ")
        self.inc_tab_count()
        print_statement_node.expr.accept(self)
        self.dec_tab_count()

    def visit_delay_statement_node(self, delay_statement_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Delay statement node => ")
        self.inc_tab_count()
        delay_statement_node.expr.accept(self)
        self.dec_tab_count()

    def visit_return_statement_node(self, return_statement_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Return statement node => ")
        self.inc_tab_count()
        return_statement_node.expr.accept(self)
        self.dec_tab_count()

    def visit_statement_node(self, statement_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Statement node => ")
        self.inc_tab_count()
        statement_node.statement.accept(self)
        self.dec_tab_count()

    def visit_for_statement_node(self, for_statement_node):
        self.node_count += 1
        print('\t' * self.tab_count, "For statement node => ")
        self.inc_tab_count()
        if for_statement_node.variable_dec is not None:
            for_statement_node.variable_dec.accept(self)
        for_statement_node.expr.accept(self)
        if for_statement_node.assign is not None:
            for_statement_node.assign.accept(self)
        for_statement_node.block.accept(self)
        self.dec_tab_count()

    def visit_while_statement_node(self, while_statement_node):
        self.node_count += 1
        print('\t' * self.tab_count, "While statement node => ")
        self.inc_tab_count()
        while_statement_node.expr.accept(self)
        while_statement_node.block.accept(self)
        self.dec_tab_count()

    def visit_formal_parameter_node(self, formal_parameter_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Formal parameter node => ")
        self.inc_tab_count()
        formal_parameter_node.identifier.accept(self)
        formal_parameter_node.type.accept(self)
        self.dec_tab_count()

    def visit_formal_params(self, formal_params_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Formal Params node => ")
        self.inc_tab_count()
        for param in formal_params_node.formal_params:
            param.accept(self)
        self.dec_tab_count()

    def visit_function_declaration_node(self, function_declaration_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Function declaration node => ")
        self.inc_tab_count()
        function_declaration_node.identifier.accept(self)
        if function_declaration_node.formalParams is not None:
            function_declaration_node.formalParams.accept(self)
        function_declaration_node.Type.accept(self)
        function_declaration_node.block.accept(self)
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
