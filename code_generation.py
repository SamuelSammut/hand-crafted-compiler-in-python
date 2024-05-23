from ast_visitor import ASTVisitor
from symbol_table import SymbolTable
from ast_node import *
from symbol_table import FormalParamException


class CodeGenerationVisitor(ASTVisitor):
    def __init__(self):
        self.instructions = []
        self.current_scope_level = 0
        self.symbol_table = SymbolTable()
        self.function_addresses = {}
        self.current_function = None
        self.next_instruction_address = 0
        self.frame_opened = False
        self.function_instructions = []
        self.coming_from_function_call = False

    def visit_all(self, nodes):
        for node in nodes:
            self.visit(node)

    def generate(self, node):
        self.visit(node)
        self.instructions.append("")
        self.instructions.extend(self.function_instructions)
        return '\n'.join(self.instructions)

    def visit(self, node):
        node_name = node.name.lower().replace('ast', '', 1)
        method_name = f"visit_{node_name}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {node.name}")

    def add_instruction(self, instruction, comment='', show_address=False, show_comments=False):
        if show_comments and show_address:
            if comment:
                self.instructions.append(f"{self.get_next_address() + 1}: {instruction} - {comment}")
            else:
                self.instructions.append(instruction)
        elif show_address:
            self.instructions.append(f"{self.get_next_address() + 1}: {instruction}")
        elif show_comments:
            if comment:
                self.instructions.append(f"{instruction} - {comment}")
            else:
                self.instructions.append(instruction)

        else:
            if comment:
                self.instructions.append(f"{instruction}")
            else:
                self.instructions.append(instruction)
        self.next_instruction_address += 1

    def get_next_address(self):
        return self.next_instruction_address

    def visit_program_node(self, node):
        self.symbol_table.enter_scope()
        self.current_scope_level = 0
        self.add_instruction(".main", "Start of main program")
        self.add_instruction(f"oframe")
        self.frame_opened = True
        self.visit_all(node.stmts)
        self.add_instruction(f"cframe")
        self.frame_opened = False
        self.add_instruction("halt", "End of program")
        self.symbol_table.exit_scope()

    def visit_block_node(self, node, coming_from_function_call=False):
        if not coming_from_function_call:
            allvars = self.symbol_table.get_variables_in_current_scope()
            self.symbol_table.enter_scope()
            self.current_scope_level += 1
            self.add_instruction(f"oframe", f"Start of block with {len(node.stmts)} statements")
            self.frame_opened = True
            for var in allvars:
                self.symbol_table.add(var['identifier'], {
                    'type': var['type'],
                    'level': self.current_scope_level,
                    'index': len(self.symbol_table.scopes[-1])
                })

            self.visit_all(node.stmts)
            self.add_instruction("cframe", "End of block")
            self.frame_opened = False
            allvars = self.symbol_table.get_variables_in_current_scope()
            self.current_scope_level -= 1
            for var in allvars:
                self.symbol_table.add(var['identifier'], {
                    'type': var['type'],
                    'level': self.current_scope_level,
                    'index': len(self.symbol_table.scopes[-1]) - 1
                })
        else:
            self.visit_all(node.stmts)

    def visit_statement_node(self, node):
        self.visit(node.statement)

    def visit_variable_declaration_node(self, node):
        initial_identifier = node.identifier.lexeme
        identifier = node.identifier.lexeme
        if isinstance(node.suffix, ASTVariableDeclArrayNode):
            array_size = node.suffix.size if node.suffix.size is not None else len(node.suffix.literals)
            self.symbol_table.add(identifier, {
                'type': f'array_of_{node.suffix.Type.value}',
                'level': self.current_scope_level,
                'index': len(self.symbol_table.scopes[-1]),
                'size': array_size
            })

            for literal in reversed(node.suffix.literals):
                self.visit(literal)
            self.add_instruction(f"push {array_size}", f"Push size of array {identifier}")
            self.add_instruction("alloc")
            self.add_instruction(f"push {array_size}", f"Push size of array {identifier}")
            self.add_instruction(f"push {self.symbol_table.scopes[-1][identifier]['index']}",
                                 f"Push index for array {identifier}")
            self.add_instruction(f"push {self.current_scope_level}", f"Push scope level for array {identifier}")
            self.add_instruction("sta", f"Store array {identifier} in memory")
        else:
            expr_value = None
            calling_saved_parameters = []
            parameter_created_identifiers = []
            P1 = []
            P2 = []
            final_p = []
            if hasattr(node, 'suffix') and hasattr(node.suffix, 'expr') and hasattr(node.suffix.expr, 'factor'):
                factor = node.suffix.expr.factor
                if hasattr(factor, 'actual_params'):
                    count = 0

                    for params in factor.actual_params.actual_params:
                        function_identifier = factor.identifier.lexeme
                        if hasattr(params, "factor") and hasattr(params.factor, "lexeme"):
                            count = count + 1
                            var_info = self.symbol_table.lookup(params.factor.lexeme)

                            calling_saved_parameters.append(f"push [{var_info['index']}:{var_info['level']}]")
                            P1.append((f"push [{var_info['index']}:{var_info['level']}]", count))

                        elif hasattr(params, "factor") and hasattr(params.factor, "literal"):
                            count = count + 1
                            identifier = function_identifier + str(count)
                            parameter_created_identifiers.append(identifier)
                            P2.append((identifier, count))
                            expr_value = params.factor.literal.value
                            self.symbol_table.add(identifier, {
                                'type': params.factor.name,
                                'level': self.current_scope_level,
                                'index': len(self.symbol_table.scopes[-1])
                            })
                            self.symbol_table.lookup(identifier)
                            index = self.symbol_table.scopes[-1][identifier]['index']
                            self.add_instruction("push 1", f"Allocate space for {identifier}")

                            self.add_instruction("alloc", "Allocate additional space in the current frame")
                            self.add_instruction(f"push {expr_value}", f"Push initial value of {identifier}")
                            self.add_instruction(f"push {index}", f"Push index for {identifier}")
                            self.add_instruction(f"push {self.current_scope_level}",
                                                 f"Push scope level for {identifier}")
                            self.add_instruction("st", f"Store {identifier} in current frame")

                    final_p = P1 + P2
                    sor = sorted(final_p, key=lambda x: x[1])

                    for s in sor:
                        if s[0].__contains__(function_identifier):
                            var_info = self.symbol_table.lookup(s[0])
                            self.add_instruction(f"push [{var_info['index']}:{var_info['level']}]")
                        else:
                            self.add_instruction(s[0])
                    self.symbol_table.add(initial_identifier, {
                        'type': node.suffix.Type,
                        'level': self.current_scope_level,
                        'index': len(self.symbol_table.scopes[-1])
                    })
                    self.add_instruction("push 0")
                    self.add_instruction(f"push .{function_identifier}")
                    self.add_instruction("call")
                    self.coming_from_function_call = True

                elif hasattr(factor, 'literal') and factor.literal is not None:
                    expr_value = factor.literal.value

                    self.symbol_table.add(initial_identifier, {
                        'type': node.suffix.Type,
                        'level': self.current_scope_level,
                        'index': len(self.symbol_table.scopes[-1])
                    })
                    self.symbol_table.lookup(initial_identifier)
                    index = self.symbol_table.scopes[-1][initial_identifier]['index']
                    self.add_instruction("push 1", f"Allocate space for {initial_identifier}")
                    if not self.frame_opened:
                        self.add_instruction("oframe", "Create a new frame")
                    else:
                        self.add_instruction("alloc", "Allocate additional space in the current frame")
                    self.add_instruction(f"push {expr_value}", f"Push initial value of {initial_identifier}")
                    self.add_instruction(f"push {index}", f"Push index for {initial_identifier}")
                    self.add_instruction(f"push {self.current_scope_level}",
                                         f"Push scope level for {initial_identifier}")
                    self.add_instruction("st", f"Store {initial_identifier} in current frame")


                elif isinstance(factor, ASTArrayAccessNode):
                    array_identifier = factor.identifier.lexeme
                    index_expr = factor.index_expr
                    self.symbol_table.add(initial_identifier, {
                        'type': node.suffix.Type.value,
                        'level': self.current_scope_level,
                        'index': len(self.symbol_table.scopes[-1])
                    })
                    self.symbol_table.lookup(initial_identifier)
                    index = self.symbol_table.scopes[-1][initial_identifier]['index']
                    self.add_instruction("push 1")
                    self.add_instruction("alloc")
                    self.visit(index_expr)

                    self.add_instruction(
                        f"push +[{self.symbol_table.lookup(array_identifier)['index']}:{self.symbol_table.lookup(array_identifier)['level']}]",

                        f"Push base address of array {array_identifier}")

                    self.add_instruction(f"push {index}", f"Push index for {initial_identifier}")
                    self.add_instruction(f"push {self.current_scope_level}",
                                         f"Push scope level for {initial_identifier}")

                    self.add_instruction("st", f"Store {initial_identifier} in current frame")

    def visit_array_access_node(self, node):
        var_info = self.symbol_table.lookup(node.identifier.lexeme)
        self.visit(node.index_expr)
        self.add_instruction(f"push {var_info['index']}", f"Push base index for array {node.identifier.lexeme}")
        self.add_instruction(f"push {var_info['level']}", f"Push scope level for array {node.identifier.lexeme}")
        self.add_instruction("push+ [0:0]", f"Access element of array {node.identifier.lexeme}")

    def visit_variable_decl_array_node(self, node):
        for literal in reversed(node.literals):
            self.visit(literal)
        array_size = node.size if node.size is not None else len(node.literals)
        self.add_instruction(f"push {array_size}", "Push size of the array")

    def visit_assignment_node(self, node):
        identifier = node.id.lexeme
        try:
            paramCheck = self.symbol_table.lookupParameters(node.id.lexeme)
        except FormalParamException as e:
            paramCheck = None
        if paramCheck is not None:
            param_info = self.symbol_table.lookupParameters(node.id.lexeme)
            self.visit(node.expr)
            self.add_instruction(f"push {param_info['index']}", f"Push index for {identifier}")
            self.add_instruction(f"push {param_info['level']}", f"Push scope level for {identifier}")
            self.add_instruction("st", f"Store value in {identifier}")

        else:
            var_info = self.symbol_table.lookup(node.id.lexeme)
            self.visit(node.expr)
            self.add_instruction(f"push {var_info['index']}", f"Push index for {identifier}")
            self.add_instruction(f"push {var_info['level']}", f"Push scope level for {identifier}")
            self.add_instruction("st", f"Store value in {identifier}")

    def visit_print_statement_node(self, node):
        if not self.coming_from_function_call:
            self.visit(node.expr)
            self.add_instruction("print", "Print the value")
        elif self.coming_from_function_call:
            self.add_instruction("print", "Print the value")

    def visit_delay_statement_node(self, node):
        self.visit(node.expr)
        self.add_instruction("delay", "Delay execution")

    def visit_write_statement_node(self, node):
        for expr in reversed(node.expressions):
            self.visit(expr)

        if node.write_type == "write_box":
            self.add_instruction("writebox", "Write a box of pixels")
        elif node.write_type == "write":
            self.add_instruction("write", "Write a single pixel")

    def visit_if_statement_node(self, node):
        self.visit(node.expression)
        cjmp_index = self.get_next_address()
        self.add_instruction("push #PC+<true_block_address>", "Reserve address for true block")
        self.add_instruction("cjmp", "Conditional jump to true block if condition is true")
        jmp_index = self.get_next_address()
        self.add_instruction("push #PC+<end_block_address>", "Reserve address for end block")
        self.add_instruction("jmp", "Jump to end of if-else statement")
        true_block_start = self.get_next_address()
        self.visit(node.block1)
        if node.block2:
            self.add_instruction("push #PC+<false_block_size>", "Reserve address ")
        self.add_instruction("jmp", "Jump to end of if-else statement")
        true_block_end = self.get_next_address()
        true_block_size = true_block_end - true_block_start
        true_block_address = true_block_start - cjmp_index

        self.instructions[cjmp_index] = f"push #PC+{true_block_address}"
        end_block_address = true_block_end - jmp_index
        self.instructions[jmp_index] = f"push #PC+{end_block_address}"

        if node.block2:
            false_block_start = self.get_next_address()
            self.visit(node.block2)
            false_block_end = self.get_next_address()
            false_block_size = false_block_end - false_block_start
            self.instructions[jmp_index] = f"push #PC+{true_block_size + 2}"
            self.instructions[true_block_end - 2] = f"push #PC+{false_block_size + 2}"

    def visit_for_statement_node(self, node):
        self.visit(node.variable_dec)
        loop_start_address = self.get_next_address()
        self.visit(node.expr)
        self.add_instruction("push #PC+4", "Address to start of for loop block")
        cjmp_index = self.get_next_address() + 1
        self.add_instruction("cjmp", "Conditional jump to start of loop is condition is true")
        self.add_instruction("push #PC+<loop_end_address>", "Reserve address for loop end")
        self.add_instruction("jmp", "Unconditional jump to end of loop if condition is false")
        self.visit(node.block)
        self.visit(node.assign)
        self.add_instruction(f"push #PC{loop_start_address - self.get_next_address()}", "Jump back to loop start")
        print("current address: ", self.get_next_address())
        self.add_instruction("jmp", "Jump to loop start")
        loop_end_address = self.get_next_address()
        self.instructions[cjmp_index] = f"push #PC+{loop_end_address - cjmp_index}"

    def visit_while_statement_node(self, node):
        loop_start_address = self.get_next_address()

        self.visit(node.expr)
        self.add_instruction("push #PC+4", "If condition is true, go to block.")
        self.add_instruction("cjmp", "Conditional jump to start of block")

        cjmp_index = self.get_next_address()
        self.add_instruction("push #PC+<loop_end_address>", "Reserve address for loop end")
        self.add_instruction("jmp", "Conditional jump to end of loop if condition is false")

        self.visit(node.block)

        self.add_instruction(f"push #PC-{(self.get_next_address() - loop_start_address)}", "Jump back to loop start")
        self.add_instruction("jmp", "Jump to loop start")

        loop_end_address = self.get_next_address()
        self.instructions[cjmp_index] = f"push #PC+{loop_end_address - cjmp_index}"

    def visit_function_declaration_node(self, node):
        self.current_scope_level += 1

        function_instructions = []

        function_instructions.append(f".{node.identifier.lexeme}")

        old_instructions, self.instructions = self.instructions, function_instructions
        self.visit(node.formalParams)
        param_count = len(node.formalParams.formal_params)

        formal_parameters_scope = self.symbol_table.formal_parameters_scope
        for p in reversed(range(param_count)):
            param_name = list(formal_parameters_scope[0].keys())[p]
            index = formal_parameters_scope[0][param_name]['index']
            scope = self.current_scope_level
            function_instructions.append(f"push {index}")
            function_instructions.append(f"push {scope}")
            function_instructions.append("st")
        self.visit_block_node(node=node.block, coming_from_function_call=True)
        self.instructions = old_instructions
        self.function_instructions.extend(function_instructions)
        self.current_scope_level -= 1
        self.coming_from_function_call = True

    def visit_return_statement_node(self, node):
        self.visit(node.expr)
        self.add_instruction("ret", "Return from function")

    def visit_expression_node(self, node):
        if node.next_simple_expr:
            self.visit(node.next_simple_expr)
        self.visit(node.simple_expr1)
        if node.next_simple_expr:
            if node.relational_op == '<':
                self.add_instruction("lt", "Perform less than operation")
            elif node.relational_op == '>':
                self.add_instruction("gt", "Perform greater than operation")
            elif node.relational_op == '==':
                self.add_instruction("eq", "Perform equal to operation")
            elif node.relational_op == '!=':
                self.add_instruction("eq")
                self.add_instruction("not", "Perform not equal to operation")
            elif node.relational_op == '<=':
                self.add_instruction("le", "Perform less than or equal to operation")
            elif node.relational_op == '>=':
                self.add_instruction("ge", "Perform greater than or equal to operation")

    def visit_simple_expression_node(self, node):
        if node.term2:
            self.visit(node.term2)
        self.visit(node.term1)
        if node.term2:
            if node.additive_op == '+':
                self.add_instruction("add", "Perform addition")
            elif node.additive_op == '-':
                self.add_instruction("sub", "Perform subtraction")
            elif node.additive_op == 'or':
                self.add_instruction("or", "Perform logical OR operation")

    def visit_term_node(self, node):
        if node.factor2:
            self.visit(node.factor2)
        self.visit(node.factor1)
        if node.factor2:
            if node.multiplicative_op == '*':
                self.add_instruction("mul", "Perform multiplication")
            elif node.multiplicative_op == '/':
                self.add_instruction("div", "Perform division")
            elif node.multiplicative_op == 'and':
                self.add_instruction("and", "Perform logical AND operation")

    def visit_factor_node(self, node):
        return self.visit(node.factor)

    def visit_literal_node(self, node):
        return self.visit(node.literal)

    def visit_boolean_literal_node(self, node):
        self.add_instruction("push 1") if node.value == 'true' else self.add_instruction("push 0")

    def visit_integer_literal_node(self, node):
        self.add_instruction(f"push {node.value} ", "Pushed value of literal")

    def visit_float_literal_node(self, node):
        self.add_instruction(f"push {node.value} ", "Pushed value of literal")

    def visit_colour_literal_node(self, node):
        self.add_instruction(f"push {int(node.value[1:], 16)} ", "Pushed value of literal")

    def visit_pad_width_literal_node(self, node):
        self.add_instruction("width", "Push width of the PAD2000c display")

    def visit_pad_height_literal_node(self, node):
        self.add_instruction("height", "Push height of the PAD2000c display")

    def visit_padread_node(self, node):
        self.visit(node.expr1)
        self.visit(node.expr2)
        self.add_instruction("read")

    def visit_padrandi_node(self, node):
        self.visit(node.expr)
        self.add_instruction("irnd", "Generate random integer")

    def visit_sub_expression_node(self, node):
        return self.visit(node.expr)

    def visit_unary_node(self, node):
        expr_value = self.visit(node.expr)
        if node.unary_op == '-':
            self.add_instruction(f"push {expr_value}", "Push operand for unary negation")
            self.add_instruction("neg", "Perform unary negation")
        elif node.unary_op == 'not':
            self.add_instruction(f"push {expr_value}", "Push operand for logical NOT")
            self.add_instruction("not", "Perform logical NOT")
        return expr_value

    def visit_identifier_node(self, node):
        try:
            paramCheck = self.symbol_table.lookupParameters(node.lexeme)
        except FormalParamException as e:
            paramCheck = None
        if paramCheck is not None:
            param_info = self.symbol_table.lookupParameters(node.lexeme)
            self.add_instruction(f"push [{param_info['index']}:{param_info['level']}]",
                                 f"Push value of variable {node.lexeme}")
        else:
            var_info = self.symbol_table.lookup(node.lexeme)
            self.add_instruction(f"push [{var_info['index']}:{var_info['level']}]",
                                 f"Push value of variable {node.lexeme}")
        return node.lexeme

    def visit_actual_params_node(self, node):
        for param in node.actual_params:
            return param.factor.literal.value

    def visit_formal_parameter_node(self, node):
        identifier = node.identifier.lexeme
        self.symbol_table.add_formal_parameter(identifier, {
            'type': node.Type.value,
            'level': self.current_scope_level,
            'index': len(self.symbol_table.formal_parameters_scope[-1])
        })

    def visit_formal_params(self, node):
        for param in node.formal_params:
            self.visit(param)

    def visit_type_node(self, node):
        return node.value

    def visit_variable_declaration_suffix_node(self, node):
        expr_value = self.visit(node.expr)
        return expr_value
