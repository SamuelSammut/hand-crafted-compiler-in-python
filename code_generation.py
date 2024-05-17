from ast_visitor import ASTVisitor
from symbol_table import SymbolTable
from ast_node import *


class CodeGenerationVisitor(ASTVisitor):
    def __init__(self):
        self.instructions = []
        self.current_scope_level = 0
        self.symbol_table = SymbolTable()
        self.function_addresses = {}
        self.current_function = None
        self.next_instruction_address = 0

    def visit_all(self, nodes):
        for node in nodes:
            self.visit(node)

    def generate(self, node):
        self.visit(node)
        return '\n'.join(self.instructions)

    def visit(self, node):
        node_name = node.name.lower().replace('ast', '', 1)
        method_name = f"visit_{node_name}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {node.name}")

    def add_instruction(self, instruction, comment=''):
        if comment:
            self.instructions.append(f"{self.next_instruction_address}::   {instruction}")
        else:
            self.instructions.append(instruction)
        self.next_instruction_address += 1

    def get_next_address(self):
        return self.next_instruction_address

    def visit_program_node(self, node):
        self.symbol_table.enter_scope()
        self.current_scope_level = 0
        self.add_instruction(".main", "Start of main program")
        self.visit_all(node.stmts)
        self.add_instruction("halt", "End of program")
        self.symbol_table.exit_scope()

    def visit_block_node(self, node):
        self.symbol_table.enter_scope()
        self.current_scope_level += 1
        self.add_instruction(f"oframe", f"Start of block with {len(node.stmts)} statements")
        self.visit_all(node.stmts)
        self.add_instruction("cframe", "End of block")
        self.symbol_table.exit_scope()
        self.current_scope_level -= 1

    def visit_statement_node(self, node):
        self.visit(node.statement)

    def visit_variable_declaration_node(self, node):
        identifier = node.identifier.lexeme
        expr_value = self.visit(node.expr)
        self.symbol_table.add(identifier, {
            'type': node.expr.Type,
            'level': self.current_scope_level,
            'index': len(self.symbol_table.scopes[-1])
        })
        index = self.symbol_table.scopes[-1][identifier]['index']
        self.add_instruction("push 1", f"Allocate space for {identifier}")
        if len(self.symbol_table.scopes[-1]) == 1:
            self.add_instruction("oframe", "Create a new frame")
        else:
            self.add_instruction("alloc", "Allocate additional space in the current frame")
        self.add_instruction(f"push {expr_value}", f"Push initial value of {identifier}")
        self.add_instruction(f"push {index}", f"Push index for {identifier}")
        self.add_instruction(f"push {self.current_scope_level}", f"Push scope level for {identifier}")
        self.add_instruction("st", f"Store {identifier} in current frame")

    def visit_assignment_node(self, node):
        identifier = node.id.lexeme
        expr_value = self.visit(node.expr)
        var_info = self.symbol_table.lookup(identifier)
        self.add_instruction(f"push {expr_value}", f"Push value to be assigned to {identifier}")
        self.add_instruction(f"push {var_info['index']}", f"Push index for {identifier}")
        self.add_instruction(f"push {var_info['level']}", f"Push scope level for {identifier}")
        self.add_instruction("st", f"Store value in {identifier}")

    def visit_print_statement_node(self, node):
        expr_value = self.visit(node.expr)
        self.add_instruction("print", "Print the value")

    def visit_delay_statement_node(self, node):
        expr_value = self.visit(node.expr)
        self.add_instruction(f"push {expr_value}", "Push delay time")
        self.add_instruction("delay", "Delay execution")

    def visit_write_statement_node(self, node):
        for expr in node.expressions:
            expr_value = self.visit(expr)
            self.add_instruction(f"push {expr_value}", "Push value for write operation")
        if node.write_type == "write_box":
            self.add_instruction("writebox", "Write a box of pixels")
        elif node.write_type == "write":
            self.add_instruction("write", "Write a single pixel")

    def visit_if_statement_node(self, node):
        self.visit(node.expression)
        # self.add_instruction(f"push {expr_value}", "Evaluate condition for if statement")
        # true_block_address = self.get_next_address() + 2
        self.add_instruction(f"push #PC+{5}", "Push address of true block")
        self.add_instruction(f"cjmp", "Conditional jump to true block if condition is true")
        if node.block2:
            self.add_instruction(f"push #PC+{7}", "Push address of true block")
        else:
            self.add_instruction(f"push #PC+{6}", "Push address of true block")
        self.add_instruction(f"jmp", "aa")
        self.visit(node.block1)
        if node.block2:
            self.visit(node.block2)
            # end_if_address = self.get_next_address() + 1
            # self.add_instruction(f"push #PC+1", "Push address of end if statement")
            # self.add_instruction("jmp", "Jump to end if statement")
            #

    def visit_for_statement_node(self, node):
        self.symbol_table.enter_scope()
        self.current_scope_level += 1
        self.visit(node.variable_dec)
        loop_start_address = self.get_next_address()
        expr_value = self.visit(node.expr)
        self.add_instruction(f"push {expr_value}", "Evaluate loop condition")
        loop_end_address = self.get_next_address() + 4
        self.add_instruction(f"push #{loop_end_address}", "Push address of loop end")
        self.add_instruction("cjmp", "Conditional jump to loop end if condition is false")
        self.visit(node.block)
        self.visit(node.assign)
        self.add_instruction(f"push #{loop_start_address}", "Jump to loop start")
        self.add_instruction("jmp", "Jump to loop start")
        self.add_instruction("cframe", "End of loop block")
        self.symbol_table.exit_scope()
        self.current_scope_level -= 1

    def visit_while_statement_node(self, node):
        loop_start_address = self.get_next_address()
        expr_value = self.visit(node.expr)
        self.add_instruction(f"push {expr_value}", "Evaluate while loop condition")
        loop_end_address = self.get_next_address() + 3
        self.add_instruction(f"push #{loop_end_address}", "Push address of loop end")
        self.add_instruction("cjmp", "Conditional jump to loop end if condition is false")
        self.visit(node.block)
        self.add_instruction(f"push #{loop_start_address}", "Jump to loop start")
        self.add_instruction("jmp", "Jump to loop start")

    def visit_function_declaration_node(self, node):
        identifier = node.identifier.lexeme
        self.function_addresses[identifier] = self.get_next_address()
        self.symbol_table.add(identifier, {
            'type': node.Type.value,
            'level': self.current_scope_level,
            'index': len(self.symbol_table.scopes[-1])
        })
        self.add_instruction(f".{identifier}")
        self.symbol_table.enter_scope()
        self.current_scope_level += 1
        self.visit(node.block)
        self.add_instruction("ret")
        self.symbol_table.exit_scope()
        self.current_scope_level -= 1

    def visit_function_call_node(self, node):
        identifier = node.identifier.lexeme
        for param in node.actual_params.actual_params:
            param_value = self.visit(param)
            self.add_instruction(f"push {param_value}", f"Push parameter {param.lexeme} for function {identifier}")
        self.add_instruction(f"call #{self.function_addresses[identifier]}", f"Call function {identifier}")

    def visit_return_statement_node(self, node):
        expr_value = self.visit(node.expr)
        self.add_instruction(f"push {expr_value}", "Push return value")
        self.add_instruction("ret", "Return from function")

    def visit_expression_node(self, node):
        simple_expr1_value = self.visit(node.simple_expr1)
        if node.next_simple_expr:
            next_simple_expr_value = self.visit(node.next_simple_expr)
            self.add_instruction(f"push {next_simple_expr_value}", "Push second operand for relational operation")
            if node.relational_op == '<':
                self.add_instruction("lt", "Perform less than operation")
            elif node.relational_op == '>':
                self.add_instruction("gt", "Perform greater than operation")
            elif node.relational_op == '==':
                self.add_instruction("eq", "Perform equal to operation")
            elif node.relational_op == '!=':
                self.add_instruction("ne", "Perform not equal to operation")
            elif node.relational_op == '<=':
                self.add_instruction("le", "Perform less than or equal to operation")
            elif node.relational_op == '>=':
                self.add_instruction("ge", "Perform greater than or equal to operation")
        return simple_expr1_value

    def visit_simple_expression_node(self, node):
        term1_value = self.visit(node.term1)
        if node.term2:
            term2_value = self.visit(node.term2)
            self.add_instruction(f"push {term1_value}", "Push first operand for additive operation")
            self.add_instruction(f"push {term2_value}", "Push second operand for additive operation")
            if node.additive_op == '+':
                self.add_instruction("add", "Perform addition")
            elif node.additive_op == '-':
                self.add_instruction("sub", "Perform subtraction")
            elif node.additive_op == 'or':
                self.add_instruction("or", "Perform logical OR operation")
        return term1_value

    def visit_term_node(self, node):
        factor1_value = self.visit(node.factor1)
        if node.factor2:
            factor2_value = self.visit(node.factor2)
            self.add_instruction(f"push {factor1_value}", "Push first operand for multiplicative operation")
            self.add_instruction(f"push {factor2_value}", "Push second operand for multiplicative operation")
            if node.multiplicative_op == '*':
                self.add_instruction("mul", "Perform multiplication")
            elif node.multiplicative_op == '/':
                self.add_instruction("div", "Perform division")
            elif node.multiplicative_op == 'and':
                self.add_instruction("and", "Perform logical AND operation")
        return factor1_value

    def visit_factor_node(self, node):
        return self.visit(node.factor)

    def visit_literal_node(self, node):
        return self.visit(node.literal)

    def visit_boolean_literal_node(self, node):
        return 1 if node.value == 'true' else 0

    def visit_integer_literal_node(self, node):
        return node.value

    def visit_float_literal_node(self, node):
        return node.value

    def visit_colour_literal_node(self, node):
        return int(node.value[1:], 16) # Convert hex color to integer

    def visit_pad_width_literal_node(self, node):
        self.add_instruction("width", "Push width of the PAD2000c display")
        return "width"

    def visit_pad_height_literal_node(self, node):
        self.add_instruction("height", "Push height of the PAD2000c display")
        return "height"

    def visit_padread_node(self, node):
        expr1_value = self.visit(node.expr1)
        expr2_value = self.visit(node.expr2)
        self.add_instruction(f"push {expr1_value}", "Push x-coordinate for pad read")
        self.add_instruction(f"push {expr2_value}", "Push y-coordinate for pad read")
        self.add_instruction("push [0:0]", "Perform pad read")
        return "padread"

    def visit_padrandi_node(self, node):
        expr_value = self.visit(node.expr)
        self.add_instruction(f"push {expr_value}", "Push maximum value for random integer generation")
        self.add_instruction("irnd", "Generate random integer")
        return "padrandi"

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
        var_info = self.symbol_table.lookup(node.lexeme)
        self.add_instruction(f"push [{var_info['index']}:{var_info['level']}]", f"Push value of variable {node.lexeme}")
        return node.lexeme

    def visit_actual_params_node(self, node):
        return [self.visit(param) for param in node.actual_params]

    def visit_formal_parameter_node(self, node):
        identifier = node.identifier.lexeme
        self.symbol_table.add(identifier, {
            'type': node.Type.value,
            'level': self.current_scope_level,
            'index': len(self.symbol_table.scopes[-1])
        })

    def visit_formal_params(self, node):
        for param in node.formal_params:
            self.visit(param)

    def visit_type_node(self, node):
        # Type nodes do not generate any specific instructions, they just carry type information
        return node.value

    def visit_variable_declaration_suffix_node(self, node):
        expr_value = self.visit(node.expr)
        declared_type = self.visit(node.Type)

        # Assuming we need to return the value for further usage in the variable declaration
        return expr_value

