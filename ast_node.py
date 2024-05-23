class ASTNode:
    def __init__(self):
        self.name = "ASTNode"


class ASTStatementNode():
    def __init__(self, statement):
        self.name = "ASTStatement_Node"
        self.statement = statement

    def accept(self, visitor):
        visitor.visit_statement_node(self)


class ASTVariableDeclArrayNode(ASTNode):
    def __init__(self, Type, size, literals):
        self.name = "ASTVariable_Decl_Array_Node"
        self.Type = Type
        self.size = size
        self.literals = literals

    def accept(self, visitor):
        visitor.visit_variable_decl_array_node(self)


class ASTArrayAccessNode(ASTNode):
    def __init__(self, identifier, index_expr):
        self.name = "ASTArray_Access_Node"
        self.identifier = identifier
        self.index_expr = index_expr

    def accept(self, visitor):
        visitor.visit_array_access_node(self)


class ASTProgramNode():
    def __init__(self):
        self.name = "ASTProgram_Node"
        self.stmts = []

    def add_statement(self, node):
        self.stmts.append(node)

    def accept(self, visitor):
        visitor.visit_program_node(self)


class ASTExpressionNode():
    def __init__(self, simple_expr1, relational_op=None, next_simple_expr=None, Type=None):
        self.name = "ASTExpression_Node"
        self.simple_expr1 = simple_expr1
        self.relational_op = relational_op
        self.next_simple_expr = next_simple_expr
        self.Type = Type

    def accept(self, visitor):
        visitor.visit_expression_node(self)


class ASTSubExpressionNode():
    def __init__(self, expr):
        self.name = "ASTSub_Expression_Node"
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_sub_expression_node(self)


class ASTFactorNode():
    def __init__(self, factor):
        self.name = "ASTFactor_Node"
        self.factor = factor

    def accept(self, visitor):
        visitor.visit_factor_node(self)


class ASTFunctionDeclarationNode():
    def __init__(self, identifier, Type, block, formalParams=None):
        self.name = "ASTFunction_Declaration_Node"
        self.identifier = identifier
        self.formalParams = formalParams
        self.Type = Type
        self.block = block

    def accept(self, visitor):
        visitor.visit_function_declaration_node(self)


class ASTUnaryNode():
    def __init__(self, unary_op, expr):
        self.name = "ASTUnary_Node"
        self.unary_op = unary_op
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_unary_node(self)


class ASTActualParams():
    def __init__(self, actual_params):
        self.name = "ASTActual_Params_Node"
        self.actual_params = actual_params

    def accept(self, visitor):
        visitor.visit_actual_params_node(self)


class ASTSimpleExpressionNode():
    def __init__(self, term1, additive_op, term2):
        self.name = "ASTSimple_Expression_Node"
        self.term1 = term1
        self.additive_op = additive_op
        self.term2 = term2

    def accept(self, visitor):
        visitor.visit_simple_expression_node(self)


class ASTPrintStatementNode():
    def __init__(self, expression):
        self.name = "ASTPrint_Statement_Node"
        self.expr = expression

    def accept(self, visitor):
        visitor.visit_print_statement_node(self)


class ASTDelayStatementNode():
    def __init__(self, expression):
        self.name = "ASTDelay_Statement_Node"
        self.expr = expression

    def accept(self, visitor):
        visitor.visit_delay_statement_node(self)


class ASTReturnStatementNode():
    def __init__(self, expression):
        self.name = "ASTReturn_Statement_Node"
        self.expr = expression

    def accept(self, visitor):
        visitor.visit_return_statement_node(self)


class ASTWriteStatementBoxNode():
    def __init__(self, write_type, expressions=None):
        if expressions is None:
            expressions = []
        self.name = "ASTWrite_Statement_Node"
        self.write_type = write_type
        self.expressions = expressions

    def accept(self, visitor):
        visitor.visit_write_statement_node(self)


class ASTFunctionCallNode():
    def __init__(self, identifier, actual_params=None):
        if actual_params is None:
            actual_params = ASTActualParams([])
        self.name = "ASTFunction_Call_Node"
        self.identifier = identifier
        self.actual_params = actual_params

    def accept(self, visitor):
        visitor.visit_function_call_node(self)


class ASTIdentifierNode():
    def __init__(self, lexeme):
        self.name = "ASTIdentifier_Node"
        self.lexeme = lexeme

    def accept(self, visitor):
        visitor.visit_identifier_node(self)


class ASTPadRandINode():
    def __init__(self, expr):
        self.name = "ASTPadRandI_Node"
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_padrandi_node(self)


class ASTForStatementNode():
    def __init__(self, expr, block, variable_dec=None, assign=None):
        self.name = "ASTFor_Statement_Node"
        self.variable_dec = variable_dec
        self.expr = expr
        self.assign = assign
        self.block = block

    def accept(self, visitor):
        visitor.visit_for_statement_node(self)


class ASTWhileStatementNode():
    def __init__(self, expr, block):
        self.name = "ASTWhile_Statement_Node"
        self.expr = expr
        self.block = block

    def accept(self, visitor):
        visitor.visit_while_statement_node(self)


class ASTAssignmentNode():
    def __init__(self, ast_identifier_node, ast_expression_node):
        self.name = "ASTAssignment_node"
        self.id = ast_identifier_node
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_assignment_node(self)


class ASTVariableDeclarationSuffixNode():
    def __init__(self, ast_type_node, ast_expression_node):
        self.name = "ASTVariable_Declaration_Suffix_Node"
        self.Type = ast_type_node
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_variable_declaration_suffix_node(self)


class ASTLiteralNode():
    def __init__(self, literal):
        self.name = "ASTLiteral_Node"
        self.literal = literal

    def accept(self, visitor):
        visitor.visit_literal_node(self)


class ASTTermNode():
    def __init__(self, factor1, multiplicative_op, factor2):
        self.name = "ASTTerm_Node"
        self.factor1 = factor1
        self.multiplicative_op = multiplicative_op
        self.factor2 = factor2

    def accept(self, visitor):
        visitor.visit_term_node(self)


class ASTBooleanLiteralNode():
    def __init__(self, value):
        self.name = "ASTBoolean_Literal_Node"
        self.value = value

    def accept(self, visitor):
        visitor.visit_boolean_literal_node(self)


class ASTIntegerLiteralNode():
    def __init__(self, value):
        self.name = "ASTInteger_Literal_Node"
        self.value = value

    def accept(self, visitor):
        visitor.visit_integer_literal_node(self)


class ASTVariableDeclarationNode():
    def __init__(self, ast_identifier_node, suffix):
        self.name = "ASTVariable_Declaration_Node"
        self.identifier = ast_identifier_node
        self.suffix = suffix

    def accept(self, visitor):
        visitor.visit_variable_declaration_node(self)


class ASTIfStatementNode():
    def __init__(self, ast_expression_node, ast_block1_node, ast_block2_node=None):
        self.block2 = ast_block2_node
        self.name = "ASTIf_Statement_Node"
        self.expression = ast_expression_node
        self.block1 = ast_block1_node

    def accept(self, visitor):
        visitor.visit_if_statement_node(self)


class ASTFloatLiteralNode():
    def __init__(self, value):
        self.name = "ASTFloat_Literal_Node"
        self.value = value

    def accept(self, visitor):
        visitor.visit_float_literal_node(self)


class ASTColourLiteralNode():
    def __init__(self, value):
        self.name = "ASTColour_Literal_Node"
        self.value = value

    def accept(self, visitor):
        visitor.visit_colour_literal_node(self)


class ASTPadWidthLiteralNode():
    def __init__(self, value):
        self.name = "ASTPad_Width_Literal_Node"
        self.value = value

    def accept(self, visitor):
        visitor.visit_pad_width_literal_node(self)


class ASTTypeNode():
    def __init__(self, value):
        self.name = "ASTType_Node"
        self.value = value

    def accept(self, visitor):
        visitor.visit_type_node(self)


class ASTPadHeightLiteralNode():
    def __init__(self, value):
        self.name = "ASTPad_Height_Literal_Node"
        self.value = value

    def accept(self, visitor):
        visitor.visit_pad_height_literal_node(self)


class ASTFormalParameterNode():
    def __init__(self, identifier, Type):
        self.name = "ASTFormal_Parameter_Node"
        self.identifier = identifier
        self.Type = Type

    def accept(self, visitor):
        visitor.visit_formal_parameter_node(self)


class ASTFormalParametersNode():
    def __init__(self, formal_params):
        self.name = "ASTFormal_Params"
        self.formal_params = formal_params

    def accept(self, visitor):
        visitor.visit_formal_params(self)


class ASTPadReadNode():
    def __init__(self, expr1, expr2):
        self.name = "ASTPadRead_Node"
        self.expr1 = expr1
        self.expr2 = expr2

    def accept(self, visitor):
        visitor.visit_padread_node(self)


class ASTBlockNode():
    def __init__(self):
        self.name = "ASTBlock_Node"
        self.stmts = []

    def add_statement(self, node):
        self.stmts.append(node)

    def accept(self, visitor):
        visitor.visit_block_node(self)
