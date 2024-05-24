from ast_visitor import ASTVisitor
from symbol_table import SymbolTable
from ast_node import *


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

        if isinstance(node.suffix, ASTVariableDeclArrayNode):
            array_type = self.visit(node.suffix)
            self.symbol_table.add(identifier, array_type)
        elif isinstance(node.suffix, ASTVariableDeclarationSuffixNode):
            self.visit(node.suffix)
            self.symbol_table.add(identifier, node.suffix.Type.value)
        else:
            raise Exception(f"Unexpected suffix type in variable declaration: {type(node.suffix)}")

    def visit_variable_declaration_suffix_node(self, node):
        expr_type = self.visit(node.expr)

        if node.Type.value != expr_type and not (node.Type.value == "float" and expr_type == "int"):
            raise Exception(
                f"Type mismatch: declared type '{node.Type.value}' does not match expression type '{expr_type}'")

    def visit_assignment_node(self, node):
        if isinstance(node.id, ASTArrayAccessNode):
            array_type = self.visit(node.id.identifier)
            if not array_type.startswith('array_of_'):
                raise Exception(f"Identifier '{node.id.identifier.lexeme}' is not an array.")

            index_type = self.visit(node.id.index_expr)
            if index_type != 'int':
                raise Exception("Array index must be an integer.")

            value_type = self.visit(node.expr)
            element_type = array_type[len('array_of_'):]
            if value_type != element_type:
                raise Exception(
                    f"Type mismatch: array element type is '{element_type}' but assigned value is '{value_type}'")
        else:
            identifier = node.id.lexeme
            if not self.symbol_table.lookup(identifier):
                raise Exception(f"Variable '{identifier}' not declared before assignment")

            assigned_type = self.visit(node.expr)
            declared_type = self.symbol_table.lookup(identifier)

            if assigned_type != declared_type and not (declared_type == "float" and assigned_type == "int"):
                raise Exception(
                    f"Type mismatch: cannot assign type '{assigned_type}' to variable '{identifier}' of type '{declared_type}'")

    def visit_variable_decl_array_node(self, node):
        if node.size:
            array_size = int(node.size)
            if len(node.literals) != array_size:
                raise Exception(
                    f"Array size {array_size} does not match the number of provided literals {len(node.literals)}"
                )
        for literal in node.literals:
            literal_type = self.visit(literal)
            if literal_type != node.Type.value:
                raise Exception(
                    f"Array contains mixed types. Expected all literals to be of type '{node.Type.value}', but found '{literal_type}'"
                )
        return f'array_of_{node.Type.value}'

    def visit_array_access_node(self, node):
        identifier_type = self.visit(node.identifier)
        if not identifier_type.startswith('array_of_'):
            raise Exception(f"Identifier '{node.identifier.lexeme}' is not an array.")
        index_type = self.visit(node.index_expr)
        if index_type != 'int':
            raise Exception("Array index must be an integer.")
        element_type = identifier_type[len('array_of_'):]
        return element_type

    def visit_factor_node(self, node):
        return self.visit(node.factor)

    def visit_term_node(self, node):
        term_type = self.visit(node.factor1)
        if node.factor2:
            factor2_type = self.visit(node.factor2)
            if term_type != factor2_type:
                if (term_type == "int" and factor2_type == "float") or (term_type == "float" and factor2_type == "int"):
                    term_type = "float"
                else:
                    raise Exception(f"Type mismatch in term: '{term_type}' and '{factor2_type}'")
        return term_type

    def visit_sub_expression_node(self, node):
        return self.visit(node.expr)

    def visit_simple_expression_node(self, node):
        simple_expr_type = self.visit(node.term1)
        if node.term2:
            term2_type = self.visit(node.term2)
            if simple_expr_type != term2_type:
                if (simple_expr_type == "int" and term2_type == "float") or (
                        simple_expr_type == "float" and term2_type == "int"):
                    simple_expr_type = "float"
                else:
                    raise Exception(f"Type mismatch in simple expression: '{simple_expr_type}' and '{term2_type}'")
        return simple_expr_type

    def visit_expression_node(self, node):
        expr_type = self.visit(node.simple_expr1)
        if node.next_simple_expr:
            next_expr_type = self.visit(node.next_simple_expr)
            if expr_type != next_expr_type:
                if (expr_type == "int" and next_expr_type == "float") or (
                        expr_type == "float" and next_expr_type == "int"):
                    expr_type = "float"
                else:
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

    def check_all_paths_return(self, statements):
        all_paths_return = False
        for statement in statements:
            if isinstance(statement, ASTReturnStatementNode):
                all_paths_return = True
            elif isinstance(statement, ASTIfStatementNode):
                if_return = self.check_all_paths_return(statement.block1.stmts)
                else_return = self.check_all_paths_return(statement.block2.stmts) if statement.block2 else False
                all_paths_return = if_return and else_return
            elif isinstance(statement, ASTWhileStatementNode):
                all_paths_return = self.check_all_paths_return(statement.block.stmts)
            elif isinstance(statement, ASTBlockNode):
                all_paths_return = self.check_all_paths_return(statement.stmts)
            elif isinstance(statement, ASTStatementNode):
                all_paths_return = self.check_all_paths_return([statement.statement])
            if all_paths_return:
                break
        return all_paths_return

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

        all_paths_return = self.check_all_paths_return(node.block.stmts)

        if not all_paths_return:
            raise Exception(f"Function '{identifier}' is missing a return statement on some execution paths")

        self.visit(node.block)
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
