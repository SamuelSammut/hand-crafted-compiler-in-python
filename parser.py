
import ast_node as ast
import lexer as lex
# from print_ast_visitor import PrintNodesVisitor

class Parser:
    def __init__(self, src_program_str):
        self.name = "PARSEAR"
        self.lexer = lex.Lexer()
        self.index = -1  # start at -1 so that the first token is at index 0
        self.nextTokenIndex = 0  # Initialize next token index
        self.src_program = src_program_str
        self.tokens = self.lexer.GenerateTokens(self.src_program)
        print("[Parser] Lexer generated token list ::")
        for t in self.tokens:
            print(t.type, t.lexeme)
        self.crtToken = lex.Token("", lex.TokenType.VOID)
        self.nextToken = lex.Token("", lex.TokenType.VOID)
        self.ASTroot = None  # this will need to change once you introduce the AST program node ....
        # that should become the new root node

    def PeekNextToken(self, k=1):
        peek_index = self.index + k
        while peek_index < len(self.tokens) and self.tokens[peek_index].type == lex.TokenType.WS:
            peek_index += 1  # Skip over whitespace tokens
        if peek_index < len(self.tokens):
            return self.tokens[peek_index]
        else:
            return lex.Token(lex.TokenType.END, "END")

    def NextTokenSkipWS(self):
        self.index += 1  # Grab the next token
        if self.index < len(self.tokens):
            self.crtToken = self.tokens[self.index]
            self.nextToken = self.PeekNextToken()  # Update next token
        else:
            self.crtToken = lex.Token(lex.TokenType.END, "END")
            self.nextToken = lex.Token(lex.TokenType.END, "END")

    def NextToken(self):
        self.NextTokenSkipWS()
        while self.crtToken.type == lex.TokenType.WS:
            print("--> Skipping WS")
            self.NextTokenSkipWS()

        print("Next Token Set to ::: ", self.crtToken.type, self.crtToken.lexeme)

    def ParseLiteral(self):
        literal = None

        if self.crtToken.type == lex.TokenType.BOOLEAN_LITERAL:
            literal = ast.ASTBooleanLiteralNode(self.crtToken.lexeme)
            self.NextToken()
            print("Boolean Literal Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        elif self.crtToken.type == lex.TokenType.INTEGER_LITERAL:
            literal = ast.ASTIntegerLiteralNode(self.crtToken.lexeme)
            self.NextToken()
            print("Integer Literal Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        elif self.crtToken.type == lex.TokenType.FLOAT_LITERAL:
            literal = ast.ASTFloatLiteralNode(self.crtToken.lexeme)
            self.NextToken()
            print("Float Literal Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        elif self.crtToken.type == lex.TokenType.COLOUR_LITERAL:
            literal = ast.ASTColourLiteralNode(self.crtToken.lexeme)
            self.NextToken()
            print("Colour Literal Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        elif self.crtToken.type == lex.TokenType.PAD_WIDTH:
            literal = ast.ASTPadWidthLiteralNode(self.crtToken.lexeme)
            self.NextToken()
            print("Pad Width Literal Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        elif self.crtToken.type == lex.TokenType.PAD_HEIGHT:
            literal = ast.ASTPadHeightLiteralNode(self.crtToken.lexeme)
            self.NextToken()
            print("Pad Height Literal Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        elif self.crtToken.type == lex.TokenType.PAD_READ:
            literal = self.ParsePadRead()
            # self.NextToken()

        return ast.ASTLiteralNode(literal)

    def ParseFunctionCall(self):
        if self.crtToken.type == lex.TokenType.IDENTIFIER:
            identifier = ast.ASTIdentifierNode(self.crtToken.lexeme)
            self.NextToken()
            print("Variable Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)

        if self.crtToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
            self.NextToken()
            print("LEFT ROUND BRACKET Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)

            actual_params = None
            # Check if there are actual parameters
            if self.crtToken.type != lex.TokenType.RIGHT_ROUND_BRACKET:
                actual_params = self.ParseActualParams()

            # After parsing actual parameters, expect a closing parenthesis
            if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                self.NextToken()  # Move past the closing parenthesis
                # Create and return the function call AST node
                return ast.ASTFunctionCallNode(identifier, actual_params)
        return ast.ASTFunctionCallNode(identifier)

    def ParseActualParams(self):
        actualParams = []
        exp1 = self.ParseExpression()
        actualParams.append(exp1)
        while self.crtToken.type == lex.TokenType.COMMA:
            self.NextToken()
            exprN = self.ParseExpression()
            actualParams.append(exprN)
        return ast.ASTActualParams(actualParams)

    def ParseExpression(self):
        simpleExpr1 = self.ParseSimpleExpression()

        if simpleExpr1 is None:
            raise Exception("First factor in term is null.")

        relational_op = None
        next_simple_expr = None

        while self.crtToken.type == lex.TokenType.RELATIONAL_OPERAND:
            relational_op = self.crtToken.lexeme
            if relational_op is None:
                raise Exception("Relational operator expected")
            self.NextToken()

            next_simple_expr = self.ParseSimpleExpression()

            simpleExpr1 = ast.ASTExpressionNode(simple_expr1=simpleExpr1, relational_op=relational_op,
                                                next_simple_expr=next_simple_expr, Type=None)

        if self.crtToken.type == lex.TokenType.AS:
            self.NextToken()

            # Parse the Type
            Type = ast.ASTTypeNode(self.crtToken.lexeme)
            self.NextToken()

            return ast.ASTExpressionNode(simple_expr1=simpleExpr1, relational_op=relational_op,
                                         next_simple_expr=next_simple_expr, Type=Type.value)

        return simpleExpr1

    def ParsePadRead(self):
        if self.crtToken.type == lex.TokenType.PAD_READ:
            self.NextToken()
            expr1 = self.ParseExpression()
            if self.crtToken.type == lex.TokenType.COMMA:
                self.NextToken()
                expr2 = self.ParseExpression()
                return ast.ASTPadReadNode(expr1, expr2)
            else:
                print("!!!ERROR: Expected comma after the first expression in PadRead")
        else:
            print("!!!ERROR: Expected '__read' token")
        return None

    def ParsePadRandI(self):
        if self.crtToken.type == lex.TokenType.RANDOM_INT:
            self.NextToken()
            expr = self.ParseExpression()
            return ast.ASTPadRandINode(expr)
        else:
            print("Error: Expected '__random_int' token")
        return None

    def ParseUnary(self):
        if self.crtToken.type == lex.TokenType.NOT or self.crtToken.lexeme == "-":
            unary_op = self.crtToken.lexeme
            self.NextToken()
            expr = self.ParseExpression()
            if expr is None:
                raise Exception("Expected expression after - or not.")
            return ast.ASTUnaryNode(unary_op, expr)
        else:
            raise Exception("Expected expression to follow - or 'not'. ")

    def ParseSubExpression(self):
        if self.crtToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
            self.NextToken()
            expr = self.ParseExpression()
            if expr is None:
                raise Exception("Expected expression after opening brackets. ")
            if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                self.NextToken()
                return ast.ASTSubExpressionNode(expr)
            else:
                raise Exception("Expected sub expression to end with ')'. ")
        else:
            raise Exception("Expected sub expression to start with '('.")

    def ParseFactor(self):
        factor = None
        if self.crtToken.type == lex.TokenType.BOOLEAN_LITERAL or \
                self.crtToken.type == lex.TokenType.INTEGER_LITERAL or \
                self.crtToken.type == lex.TokenType.FLOAT_LITERAL or \
                self.crtToken.type == lex.TokenType.COLOUR_LITERAL or \
                self.crtToken.type == lex.TokenType.PAD_WIDTH or \
                self.crtToken.type == lex.TokenType.PAD_HEIGHT or \
                self.crtToken.type == lex.TokenType.PAD_READ:
            factor = self.ParseLiteral()
        elif self.crtToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
            factor = self.ParseSubExpression()
        elif self.crtToken.type == lex.TokenType.NOT or self.crtToken.lexeme == "-":
            factor = self.ParseUnary()
        elif self.crtToken.type == lex.TokenType.RANDOM_INT:
            factor = self.ParsePadRandI()
        elif self.crtToken.type == lex.TokenType.PAD_WIDTH:
            factor = self.ParsePadWidth()
        elif self.crtToken.type == lex.TokenType.PAD_HEIGHT:
            factor = self.ParsePadHeight()
        elif self.crtToken.type == lex.TokenType.PAD_READ:
            factor = self.ParsePadRead()
        elif self.crtToken.type == lex.TokenType.IDENTIFIER:
            if self.nextToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
                factor = self.ParseFunctionCall()
            else:
                factor = ast.ASTIdentifierNode(self.crtToken.lexeme)
                self.NextToken()
                print("Variable Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        return ast.ASTFactorNode(factor)

    def ParsePadWidth(self):
        if self.crtToken.type == lex.TokenType.PAD_WIDTH:
            return ast.ASTPadWidthLiteralNode(self.crtToken.lexeme)

    def ParsePadHeight(self):
        if self.crtToken.type == lex.TokenType.PAD_HEIGHT:
            return ast.ASTPadHeightLiteralNode(self.crtToken.lexeme)
    def ParseAssignment(self):
        if self.crtToken.type == lex.TokenType.IDENTIFIER:
            assignment_lhs = ast.ASTIdentifierNode(self.crtToken.lexeme)
            self.NextToken()
            if self.crtToken.type == lex.TokenType.EQUALS:
                self.NextToken()
                assignment_rhs = self.ParseExpression()
                if assignment_rhs is None:
                    raise Exception("Expression on right hand side of assignment is null")
                else:
                    return ast.ASTAssignmentNode(assignment_lhs, assignment_rhs)
            else:
                raise Exception("Expected equal sign to follow identifier when parsing assignment.")
        else:
            raise Exception("Expected assignment to start with identifier")

    def ParseTerm(self):
        factor1 = self.ParseFactor()
        if factor1 is None:
            raise Exception("First factor in term is null.")
        multiplicative_op = None
        factor2 = None

        # Check if there are additional factors with multiplicative operators
        while self.crtToken.type == lex.TokenType.MULTIPLICATIVE_OPERAND:
            multiplicative_op = self.crtToken.lexeme
            if multiplicative_op is None:
                raise Exception("Multiplicative operator expected")
            self.NextToken()

            next_factor = self.ParseFactor()

            factor1 = ast.ASTTermNode(factor1, multiplicative_op, next_factor)

        return factor1

    # def ParseSimpleExpression(self):
    #     terms = []
    #     term1 = self.ParseTerm()
    #     terms.append(term1)
    #     if term1 is None:
    #         raise Exception("Initial term empty when parsing simple expression.")
    #     while self.crtToken.type == lex.TokenType.ADDITIVE_OPERAND:
    #         self.NextToken()
    #         termsN = self.ParseTerm()
    #         if termsN is None:
    #             raise Exception("No term following additive operand in simple expression parsing.")
    #         terms.append(termsN)
    #     return ast.ASTSimpleExpressionNode(terms)
    def ParseSimpleExpression(self):
        term1 = self.ParseTerm()
        if term1 is None:
            raise Exception("First factor in term is null.")
        additive_op = None
        term2 = None

        while self.crtToken.type == lex.TokenType.ADDITIVE_OPERAND:
            additive_op = self.crtToken.lexeme
            if additive_op is None:
                raise Exception("Additive operator expected.")
            self.NextToken()

            nextTerm = self.ParseTerm()

            term1 = ast.ASTSimpleExpressionNode(term1, additive_op, nextTerm)

        return term1

    def ParseVariableDeclarationSuffix(self):
        if self.crtToken.type == lex.TokenType.COLON:
            self.NextToken()
            if self.crtToken.type == lex.TokenType.TYPE:
                Type = ast.ASTTypeNode(self.crtToken.lexeme)
                self.NextToken()
                if Type is None:
                    raise Exception("Expected type to not be null after colon in variable declaration suffix.")
                if self.crtToken.type == lex.TokenType.EQUALS:
                    self.NextToken()
                    expression = self.ParseExpression()
                    if expression is None:
                        raise Exception("Expected expression to not be null in Variable Declaration suffix.")
                    else:
                        return ast.ASTVariableDeclarationSuffixNode(Type, expression)
                else:
                    raise Exception("Expected equal sign after type in variable declaration suffix.")

            else:
                raise Exception("Expected type to follow colon in variable declaration suffix.")
        else:
            raise Exception("Expected Variable Declaration Suffix to start with colon symbol.")

    def ParsePrintStatement(self):
        if self.crtToken.type == lex.TokenType.PRINT:
            self.NextToken()
            expression = self.ParseExpression()
            if expression is None:
                raise Exception("Expected expression after print statement")
            else:
                return ast.ASTPrintStatementNode(expression)

        else:
            raise Exception("Expected print statement to start with __print keyword")

    def ParseDelayStatement(self):
        if self.crtToken.type == lex.TokenType.DELAY:
            self.NextToken()
            expression = self.ParseExpression()
            if expression is None:
                raise Exception("Expected expression after delay statement")
            else:
                return ast.ASTDelayStatementNode(expression)

        else:
            raise Exception("Expected delay statement to start with __delay keyword")

    def ParseWriteStatement(self):
        expressionList = []
        if self.crtToken.type == lex.TokenType.WRITE_BOX:
            write_type = "write_box"
            self.NextToken()
            for i in range(5):
                expression = self.ParseExpression()
                expressionList.append(expression)
                if i < 4:
                    if self.crtToken.type == lex.TokenType.COMMA:
                        self.NextToken()
                    else:
                        raise Exception("Expected a comma between expressions when parsing write_box statements.")
            return ast.ASTWriteStatementBoxNode(write_type, expressionList)

        elif self.crtToken.type == lex.TokenType.WRITE:
            write_type = "write"
            self.NextToken()
            for i in range(3):
                expression = self.ParseExpression()
                expressionList.append(expression)
                if i < 2:
                    if self.crtToken.type == lex.TokenType.COMMA:
                        self.NextToken()
                    else:
                        raise Exception("Expected a comma between expressions when parsing write statements.")
            return ast.ASTWriteStatementBoxNode(write_type, expressionList)

        else:
            raise Exception("Expected Write statement to start with __write or __write_box")

    def ParseReturnStatement(self):
        if self.crtToken.type == lex.TokenType.RETURN:
            self.NextToken()
            expression = self.ParseExpression()
            if expression is None:
                raise Exception("Expected expression after return statement")
            else:
                self.NextToken()
                return ast.ASTReturnStatementNode(expression)

        else:
            raise Exception("Expected return statement to start with return keyword")

    def ParseVariableDeclaration(self):
        if self.crtToken.type == lex.TokenType.LET:
            self.NextToken()
            if self.crtToken.type == lex.TokenType.IDENTIFIER:
                identifier = ast.ASTIdentifierNode(self.crtToken.lexeme)
                self.NextToken()
                if identifier is None:
                    raise Exception("Expected identifier to follow 'let' keyword when parsing variable declaration.")
                else:
                    variableDeclarationSuffix = self.ParseVariableDeclarationSuffix()
                    if variableDeclarationSuffix is None:
                        raise Exception(
                            "Expected identifier to be followed by variable declaration suffix, but it is None")
                    else:
                        return ast.ASTVariableDeclarationNode(identifier, variableDeclarationSuffix)

            else:
                raise Exception("Expected identifier to follow 'let' keyword when parsing variable declaration.")

        else:
            raise Exception("Expected variable declaration to start with keyword: 'let'")

    def ParseIfStatement(self):
        if self.crtToken.type == lex.TokenType.IF:
            self.NextToken()
            if self.crtToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
                self.NextToken()
                expression = self.ParseExpression()
                if expression is None:
                    raise Exception("Expression is null. ")
                else:
                    if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                        self.NextToken()
                        block1 = self.ParseBlock()
                        if block1 is None:
                            raise Exception("First block after if statement expression is null.")
                        else:
                            if self.crtToken.type == lex.TokenType.ELSE:
                                self.NextToken()
                                block2 = self.ParseBlock()
                                if block2 is None:
                                    raise Exception("Second block after else statement is null. ")
                                else:
                                    return ast.ASTIfStatementNode(expression, block1, block2)
                            else:
                                return ast.ASTIfStatementNode(expression, block1)
                    else:
                        raise Exception("Expected right round bracket after expression in if statement. ")
            else:
                raise Exception("Expected 'if' keyword to be followed by a left round bracket. ")
        else:
            raise Exception("Expected first token in if statement to be 'if'. ")

    def ParseStatement(self):
        statement = None
        if self.crtToken.type == lex.TokenType.LET:
            statement = self.ParseVariableDeclaration()
            if self.crtToken.type != lex.TokenType.SEMI_COLON:
                raise Exception("Expected semicolon after variable declaration statement.")
            else:
                self.NextToken()
                return ast.ASTStatementNode(statement)
        elif self.crtToken.type == lex.TokenType.IDENTIFIER:
            statement = self.ParseAssignment()
            if self.crtToken.type != lex.TokenType.SEMI_COLON:
                raise Exception("Expected semicolon after assignment statement.")
            else:
                self.NextToken()
                return ast.ASTStatementNode(statement)
        elif self.crtToken.type == lex.TokenType.PRINT:
            statement = self.ParsePrintStatement()
            if self.crtToken.type != lex.TokenType.SEMI_COLON:
                raise Exception("Expected semicolon after print statement.")
            else:
                self.NextToken()
                return ast.ASTStatementNode(statement)
        elif self.crtToken.type == lex.TokenType.DELAY:
            statement = self.ParseDelayStatement()
            if self.crtToken.type != lex.TokenType.SEMI_COLON:
                raise Exception("Expected semicolon after delay statement.")
            else:
                self.NextToken()
                return ast.ASTStatementNode(statement)
        elif self.crtToken.type == lex.TokenType.WRITE or self.crtToken.type == lex.TokenType.WRITE_BOX:
            statement = self.ParseWriteStatement()
            if self.crtToken.type != lex.TokenType.SEMI_COLON:
                raise Exception("Expected semicolon after write statement.")
            else:
                self.NextToken()
                return ast.ASTStatementNode(statement)
        elif self.crtToken.type == lex.TokenType.IF:
            return ast.ASTStatementNode(self.ParseIfStatement())
        elif self.crtToken.type == lex.TokenType.FOR:
            return ast.ASTStatementNode(self.ParseForStatement())
        elif self.crtToken.type == lex.TokenType.WHILE:
            return ast.ASTStatementNode(self.ParseWhileStatement())
        elif self.crtToken.type == lex.TokenType.RETURN:
            return ast.ASTStatementNode(self.ParseReturnStatement())
        elif self.crtToken.type == lex.TokenType.FUN:
            return ast.ASTStatementNode(self.ParseFunctionDeclaration())
        elif self.crtToken.type == lex.TokenType.LEFT_CURLY_BRACKET:
            return ast.ASTStatementNode(self.ParseBlock())
        else:
            raise Exception("No valid statement")

    def ParseWhileStatement(self):
        if self.crtToken.type == lex.TokenType.WHILE:
            self.NextToken()
            if self.crtToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
                self.NextToken()
                expression = self.ParseExpression()
                if expression is None:
                    raise Exception("Expression in while statement is null.")
                else:
                    if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                        self.NextToken()
                        block = self.ParseBlock()
                        if block is None:
                            raise Exception("Block in while statement is null.")
                        else:
                            return ast.ASTWhileStatementNode(expression, block)
                    else:
                        raise Exception(
                            "Expected expression in while statement to be followed by closing round brackets.")
            else:
                raise Exception("Expected while keyword to be followed by open round brackets.")
        else:
            raise Exception("Expected while statement to start with while keyword.")

    def ParseFormalParameter(self):
        if self.crtToken.type == lex.TokenType.IDENTIFIER:
            identifier = ast.ASTIdentifierNode(self.crtToken.lexeme)
            self.NextToken()
            if identifier is None:
                raise Exception("Identifier at start of formal parameter is null.")
            else:
                if self.crtToken.type == lex.TokenType.COLON:
                    self.NextToken()
                    if self.crtToken.type == lex.TokenType.TYPE:
                        type = ast.ASTTypeNode(self.crtToken.lexeme)
                        self.NextToken()
                        if type is None:
                            raise Exception("Type in formal parameter is null.")
                        else:
                            return ast.ASTFormalParameterNode(identifier, type)
                    else:
                        raise Exception("Expected token after colon to be a type in Formal parameter parse.")
                else:
                    raise Exception("Expected colon too follow identifier in Formal Parameter parse.")
        else:
            raise Exception("Expected identifier at start of formal parameter")

    def ParseFormalParameters(self):
        formalParameters = []
        if self.crtToken.type == lex.TokenType.IDENTIFIER:
            # self.NextToken()
            formalParameter1 = self.ParseFormalParameter()
            if formalParameter1 is None:
                raise Exception("First formal parameter is null.")
            else:
                formalParameters.append(formalParameter1)
                while self.crtToken.type == lex.TokenType.COMMA:
                    self.NextToken()
                    formalParameterN = self.ParseFormalParameter()
                    if formalParameterN is None:
                        raise Exception("A formal parameter is null.")
                    else:
                        formalParameters.append(formalParameterN)
                if formalParameters is None:
                    raise Exception("Error occurred while parsing formal parameters list.")
                else:
                    return ast.ASTFormalParametersNode(formalParameters)

        else:
            raise Exception("Expected formal parameters to start with identifier.")

    def ParseFunctionDeclaration(self):
        if self.crtToken.type == lex.TokenType.FUN:
            self.NextToken()
            if self.crtToken.type == lex.TokenType.IDENTIFIER:
                identifier = ast.ASTIdentifierNode(self.crtToken.lexeme)
                self.NextToken()
                if identifier is None:
                    raise Exception("Identifier in function declaration is null.")
                else:
                    if self.crtToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
                        self.NextToken()
                        if self.crtToken.type == lex.TokenType.IDENTIFIER:
                            # self.NextToken()
                            formalParams = self.ParseFormalParameters()
                            if formalParams is None:
                                raise Exception("Formal parameters in function declaration is null.")
                            else:
                                if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                                    self.NextToken()
                                    if self.crtToken.type == lex.TokenType.ARROW:
                                        self.NextToken()
                                        if self.crtToken.type == lex.TokenType.TYPE:
                                            Type = ast.ASTTypeNode(self.crtToken.lexeme)
                                            self.NextToken()
                                            if Type is None:
                                                raise Exception("Type in function declaration is null.")
                                            else:
                                                block = self.ParseBlock()
                                                if block is None:
                                                    raise Exception("Block in function declaration is null.")
                                                else:
                                                    return ast.ASTFunctionDeclarationNode(identifier=identifier,
                                                                                          formalParams=formalParams,
                                                                                          Type=Type, block=block)
                                        else:
                                            raise Exception("Expected type after arrow in function declaration. ")
                                    else:
                                        raise Exception(
                                            "Expected arrow '->' after round brackets in function declaration. ")
                                else:
                                    raise Exception(
                                        "Expected closing round bracket after formal parameters in function declaration.")
                        elif self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                            self.NextToken()
                            if self.crtToken.type == lex.TokenType.ARROW:
                                self.NextToken()
                                if self.crtToken.type == lex.TokenType.TYPE:
                                    Type = ast.ASTTypeNode(self.crtToken.lexeme)
                                    self.NextToken()
                                    if Type is None:
                                        raise Exception("Type in function declaration is null.")
                                    else:
                                        block = self.ParseBlock()
                                        if block is None:
                                            raise Exception("Block in function declaration is null.")
                                        else:
                                            return ast.ASTFunctionDeclarationNode(identifier=identifier, Type=Type,
                                                                                  block=block, formalParams=None)
                                else:
                                    raise Exception("Expected type after arrow in function declaration. ")
                            else:
                                raise Exception("Expected arrow '->' after round brackets in function declaration. ")
                        else:
                            raise Exception(
                                "Expected either formal parameters or empty brackets after identifier in function declaration. ")
                    else:
                        raise Exception(
                            "Expected identifier to be followed by an opening round bracket in function declaration.")
            else:
                raise Exception("Expected fun keyword to be followed by an identfier.")
        else:
            raise Exception("Expected function declaration to start with 'fun' keyword.")

    def ParseForStatement(self):
        if self.crtToken.type == lex.TokenType.FOR:
            self.NextToken()
            if self.crtToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
                self.NextToken()
                if self.crtToken.type == lex.TokenType.LET:
                    variableDeclaration = self.ParseVariableDeclaration()
                    if variableDeclaration is None:
                        raise Exception("Variable declaration in for statement is null.")
                    if self.crtToken.type == lex.TokenType.SEMI_COLON:
                        self.NextToken()
                        expression = self.ParseExpression()
                        if expression is None:
                            raise Exception("Expression in for statement is null.")
                        if self.crtToken.type == lex.TokenType.SEMI_COLON:
                            self.NextToken()
                            if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                                self.NextToken()
                                block = self.ParseBlock()
                                if block is None:
                                    raise Exception("Block statement in for statement is null.")
                                return ast.ASTForStatementNode(variable_dec=variableDeclaration, expr=expression,
                                                               block=block, assign=None)
                            elif self.crtToken.type == lex.TokenType.IDENTIFIER:
                                assignment = self.ParseAssignment()
                                if assignment is None:
                                    raise Exception("Assignment in for statement is none.")
                                else:
                                    if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                                        self.NextToken()
                                        block = self.ParseBlock()
                                        if block is None:
                                            raise Exception("Block at end of for statement is null.")
                                        else:
                                            return ast.ASTForStatementNode(variable_dec=variableDeclaration,
                                                                           expr=expression, assign=assignment,
                                                                           block=block)
                                    else:
                                        raise Exception("Expected closing round brackets at end of for statement.")

                            else:
                                raise Exception("Expected, either a closing round bracket or assignment declaration "
                                                "at end of for statement.")
                        else:
                            raise Exception("Expected a semicolon after variable declaration in for statement.")

                    else:
                        raise Exception("Expected ")
                elif self.crtToken.type == lex.TokenType.SEMI_COLON:
                    self.NextToken()
                    expression = self.ParseExpression()
                    if self.crtToken.type == lex.TokenType.SEMI_COLON:
                        self.NextToken()
                        if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                            self.NextToken()
                            block = self.ParseBlock()
                            if block is None:
                                raise Exception("Block at end of for statement is null.")
                            else:
                                return ast.ASTForStatementNode(expr=expression, block=block, variable_dec=None,
                                                               assign=None)
                        elif self.crtToken.type == lex.TokenType.IDENTIFIER:
                            assignment = self.ParseAssignment()
                            if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
                                self.NextToken()
                                block = self.ParseBlock()
                                if block is None:
                                    raise Exception("Block at end of for statement is null.")
                                else:
                                    return ast.ASTForStatementNode(expr=expression, block=block, variable_dec=None,
                                                                   assign=assignment)
                            else:
                                raise Exception("Expected closing round brackets after assignment in for statement.")
                        else:
                            raise Exception("Expected either a closing round bracket or assignment in for statement.")
                    else:
                        raise Exception("Expected semicolon following expression in for statement.")
                else:
                    raise Exception(
                        "Expected a variable declaration or a semicolon after opening of brackets in for statement.")
            else:
                raise Exception("Expected left round bracket to follow 'for' keyword'.")
        else:
            raise Exception("Expected for statement to start with 'for' keyword.")

    def ParseBlock(self):
        # At the moment we only have assignment statements .... you'll need to add more for the assignment -
        # branching depends on the token type
        if self.crtToken.type == lex.TokenType.LEFT_CURLY_BRACKET:
            self.NextToken()
            block = ast.ASTBlockNode()

            while self.crtToken.type != lex.TokenType.END:
                print("New Statement - Processing Initial Token:: ", self.crtToken.type, self.crtToken.lexeme)
                s = self.ParseStatement()
                block.add_statement(s)
                if self.crtToken.type == lex.TokenType.RIGHT_CURLY_BRACKET:
                    self.NextToken()
                    return block


            else:
                raise Exception("Expected block to be followed by a right curly bracket.")

        else:
            raise Exception("Expected block to start with left curly brackets.")

    def ParseProgram(self):
        self.NextToken()  # set crtToken to the first token (skip all WS)
        # At the moment we only have assignment statements .... you'll need to add more for the assignment -
        # branching depends on the token type

        program = ast.ASTProgramNode()

        while self.crtToken.type != lex.TokenType.END:
            print("New Statement - Processing Initial Token:: ", self.crtToken.type, self.crtToken.lexeme)
            s = self.ParseStatement()
            program.add_statement(s)

        return program

    def Parse(self):
        self.ASTroot = self.ParseProgram()

