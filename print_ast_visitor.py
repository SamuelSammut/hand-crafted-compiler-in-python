from ast_visitor import ASTVisitor

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

    def visit_term_node(self, term_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Multiplicative operator::", term_node.multiplicative_op)
        self.inc_tab_count()
        term_node.factor1.accept(self)
        # may need to accept multop later
        term_node.factor2.accept(self)
        self.dec_tab_count()

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

        ## hwen vistin blokc node create new scope in visitor
        ## when getting out, pop scope form stack

        ##create a vistior for type checing
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
        # print('\t' * self.tab_count, "Literal node => ")
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
        print('\t' * self.tab_count, "Unary node => ", unary_node.unary_op)
        self.inc_tab_count()
        unary_node.expr.accept(self)
        self.dec_tab_count()

    def visit_factor_node(self, factor_node):
        self.node_count += 1
        # print('\t' * self.tab_count, "Factor node => ")
        self.inc_tab_count()
        factor_node.factor.accept(self)
        self.dec_tab_count()

    def visit_simple_expression_node(self, simple_expression_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Additive operator node => ", simple_expression_node.additive_op)
        self.inc_tab_count()
        simple_expression_node.term1.accept(self)
        # may need to accept addtive op later
        simple_expression_node.term2.accept(self)
        self.dec_tab_count()

    #
    def visit_expression_node(self, expression_node):
        self.node_count += 1
        if expression_node.relational_op is not None:
            print('\t' * self.tab_count, "Relational operator::", expression_node.relational_op)
            self.inc_tab_count()
        expression_node.simple_expr1.accept(self)
        # may need to accept reltainal later
        if expression_node.next_simple_expr is not None:
            expression_node.next_simple_expr.accept(self)
            self.dec_tab_count()
        if expression_node.Type is not None:
            print('\t' * self.tab_count, "Expression Type::", expression_node.Type)

    def visit_variable_declaration_suffix_node(self, variable_declaration_suffix_node):
        self.node_count += 1
        # print('\t' * self.tab_count, "Variable declaration suffix node => ")
        self.inc_tab_count()
        variable_declaration_suffix_node.Type.accept(self)
        variable_declaration_suffix_node.expr.accept(self)
        self.dec_tab_count()

    def visit_variable_declaration_node(self, variable_declaration_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Variable declaration node => ")
        self.inc_tab_count()
        variable_declaration_node.identifier.accept(self)

        ##idetnfier put in symbol table  take type
        # chec if already in scope, if already in throw expceiont else put in symbol table in the current scope
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
        formal_parameter_node.Type.accept(self)
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
