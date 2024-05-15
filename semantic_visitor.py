from ast_visitor import ASTVisitor
from symbol_table import SymbolTable


class SemanticVisitor(ASTVisitor):
    def __init__(self):
        self.return_encountered = None
        self.symbol_table = SymbolTable()
        self.current_function_type = None

    def visit(self, node):
        node_name = node.name.lower().replace('ast', '', 1)
        method_name = f"visit_{node_name}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {node.name}")

    def visit_identifier_node(self, node):
        return self.symbol_table.lookup(node.lexeme)

    def visit_integer_literal_node(self, node):
        return "int"

    def visit_float_literal_node(self, node):
        return "float"

    def visit_boolean_literal_node(self, node):
        return "bool"

    def visit_colour_literal_node(self, node):
        return "colour"

    def visit_program_node(self, node):
        self.symbol_table.enter_scope()
        for statement in node.stmts:
            self.visit(statement)
        self.symbol_table.exit_scope()

    def visit_block_node(self, node):
        self.symbol_table.enter_scope()
        for statement in node.stmts:
            self.visit(statement)
        self.symbol_table.exit_scope()

    def visit_statement_node(self, node):
        self.visit(node.statement)

    def visit_variable_declaration_node(self, node):
        identifier = node.identifier.lexeme

        if self.symbol_table.lookup_in_current_scope(identifier):
            raise Exception(f"Variable '{identifier}' already declared in this scope")

        self.visit(node.expr)

        self.symbol_table.add(identifier, node.expr.Type.value)

    def visit_variable_declaration_suffix_node(self, node):
        expr_type = self.visit(node.expr)

        if node.Type.value != expr_type:
            raise Exception(
                f"Type mismatch: declared type '{node.Type.value}' does not match expression type '{expr_type}'")

    def visit_assignment_node(self, node):
        identifier = node.id.lexeme
        if not self.symbol_table.lookup(identifier):
            raise Exception(f"Variable '{identifier}' not declared before assignment")

        assigned_type = self.visit(node.expr)
        declared_type = self.symbol_table.lookup(identifier)

        if assigned_type != declared_type:
            raise Exception(
                f"Type mismatch: cannot assign type '{assigned_type}' to variable '{identifier}' of type '{declared_type}'")

    def visit_factor_node(self, node):
        return self.visit(node.factor)

    def visit_term_node(self, node):
        term_type = self.visit(node.factor1)
        if node.factor2:
            factor2_type = self.visit(node.factor2)
            if term_type != factor2_type:
                raise Exception(f"Type mismatch in term: '{term_type}' and '{factor2_type}'")
        return term_type

    def visit_sub_expression_node(self, node):
        # Visit the inner expression and return its type
        return self.visit(node.expr)

    def visit_simple_expression_node(self, node):
        simple_expr_type = self.visit(node.term1)
        if node.term2:
            term2_type = self.visit(node.term2)
            if simple_expr_type != term2_type:
                raise Exception(f"Type mismatch in simple expression: '{simple_expr_type}' and '{term2_type}'")
        return simple_expr_type

    def visit_expression_node(self, node):
        expr_type = self.visit(node.simple_expr1)
        if node.next_simple_expr:
            next_expr_type = self.visit(node.next_simple_expr)
            if expr_type != next_expr_type:
                raise Exception(f"Type mismatch in expression: '{expr_type}' and '{next_expr_type}'")

            if node.relational_op:
                expr_type = "bool"

        if node.Type:
            expr_type = node.Type.value
        return expr_type

    def visit_unary_node(self, node):
        expr_type = self.visit(node.expr)
        if node.unary_op == 'not' and expr_type != 'bool':
            raise Exception(f"Unary operator 'not' requires a boolean expression, got '{expr_type}'")
        if node.unary_op == '-' and expr_type not in ['int', 'float']:
            raise Exception(f"Unary operator '-' requires an integer or float expression, got '{expr_type}'")
        return expr_type

    def visit_function_declaration_node(self, node):
        identifier = node.identifier.lexeme
        if self.symbol_table.lookup_in_current_scope(identifier):
            raise Exception(f"Function '{identifier}' already declared in this scope")

        formal_params = node.formalParams.formal_params if node.formalParams is not None else []
        function_record = FunctionRecord(node.Type.value, formal_params)
        self.symbol_table.add(identifier, function_record)

        self.symbol_table.enter_scope()
        self.current_function_type = node.Type.value
        self.return_encountered = False

        if node.formalParams:
            for param in node.formalParams.formal_params:
                self.visit_formal_parameter_node(param)

        for statement in node.block.stmts:
            self.visit(statement)

        if self.current_function_type != "void" and not self.return_encountered:
            raise Exception(f"Function '{identifier}' is missing a return statement")

        self.symbol_table.exit_scope()
        self.current_function_type = None

    def visit_function_call_node(self, node):
        identifier = node.identifier.lexeme
        function_record = self.symbol_table.lookup(identifier)

        if not isinstance(function_record, FunctionRecord):
            raise Exception(f"'{identifier}' is not a function")

        expected_params = function_record.formal_params
        actual_params = node.actual_params.actual_params

        if len(actual_params) != len(expected_params):
            raise Exception(
                f"Function '{identifier}' expects {len(expected_params)} arguments, got {len(actual_params)}")

        for actual_param, expected_param in zip(actual_params, expected_params):
            actual_param_type = self.visit(actual_param)
            if actual_param_type != expected_param.Type.value:
                raise Exception(
                    f"Type mismatch in function call '{identifier}': expected '{expected_param.Type.value}', got '{actual_param_type}'")

        return function_record.return_type

    def visit_formal_parameter_node(self, node):
        identifier = node.identifier.lexeme
        if self.symbol_table.lookup_in_current_scope(identifier):
            raise Exception(f"Parameter '{identifier}' already declared in this scope")
        self.symbol_table.add(identifier, node.Type.value)

    def visit_formal_params(self, node):
        for param in node.formal_params:
            self.visit(param)

    def visit_print_statement_node(self, node):
        expr_type = self.visit(node.expr)
        if expr_type not in ['int', 'float', 'bool', 'colour']:
            raise Exception(f"__print statement only supports int, float, bool, or colour types, got '{expr_type}'")

    def visit_delay_statement_node(self, node):
        expr_type = self.visit(node.expr)
        if expr_type != 'int':
            raise Exception(f"__delay statement requires an integer expression, got '{expr_type}'")

    def visit_write_statement_node(self, node):
        expr_types = [self.visit(expr) for expr in node.expressions]

        if node.write_type == "write_box":
            if not (len(expr_types) == 5 and all(t == 'int' for t in expr_types[:4]) and expr_types[4] == 'colour'):
                raise Exception(
                    f"__write_box statement requires four int expressions followed by one colour expression, got {expr_types}")

        elif node.write_type == "write":
            if not (len(expr_types) == 3 and all(t == 'int' for t in expr_types[:2]) and expr_types[2] == 'colour'):
                raise Exception(
                    f"__write statement requires two int expressions followed by one colour expression, got {expr_types}")

        else:
            raise Exception("Unknown write statement type")

    def visit_if_statement_node(self, node):
        expr_type = self.visit(node.expression)
        if expr_type != 'bool':
            raise Exception(f"If statement condition must be a boolean expression, got '{expr_type}'")
        self.visit(node.block1)
        if node.block2:
            self.visit(node.block2)

    def visit_for_statement_node(self, node):
        self.symbol_table.enter_scope()
        if node.variable_dec:
            self.visit(node.variable_dec)
        expr_type = self.visit(node.expr)
        if expr_type != 'bool':
            raise Exception(f"For statement condition must be a boolean expression, got '{expr_type}'")
        if node.assign:
            self.visit(node.assign)
        self.visit(node.block)
        self.symbol_table.exit_scope()

    def visit_while_statement_node(self, node):
        expr_type = self.visit(node.expr)
        if expr_type != 'bool':
            raise Exception(f"While statement condition must be a boolean expression, got '{expr_type}'")
        self.visit(node.block)

    def visit_return_statement_node(self, node):
        expr_type = self.visit(node.expr)
        if expr_type != self.current_function_type:
            raise Exception(
                f"Return statement type '{expr_type}' does not match function return type '{self.current_function_type}'")
        self.return_encountered = True

    def visit_literal_node(self, node):
        return self.visit(node.literal)

    def visit_actual_params_node(self, node):
        return [self.visit(param) for param in node.actual_params]

    def visit_pad_width_literal_node(self, node):
        return "int"

    def visit_pad_height_literal_node(self, node):
        return "int"

    def visit_padread_node(self, node):
        expr1_type = self.visit(node.expr1)
        expr2_type = self.visit(node.expr2)
        if expr1_type != 'int' or expr2_type != 'int':
            raise Exception(f"__read statement requires two int expressions, got '{expr1_type}' and '{expr2_type}'")
        return "int"

    def visit_padrandi_node(self, node):
        expr_type = self.visit(node.expr)
        if expr_type != 'int':
            raise Exception(f"__random_int statement requires an int expression, got '{expr_type}'")
        return "int"


class FunctionRecord:
    def __init__(self, return_type, formal_params):
        self.return_type = return_type
        self.formal_params = formal_params
