class ASTVisitor:

    def visit_integer_literal_node(self, node):
        raise NotImplementedError

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