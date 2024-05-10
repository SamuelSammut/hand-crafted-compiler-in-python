# Now we need the parser (using tokens produced by the Lexer) to build the AST - this code snipper is able to build ASTAssignmentNode trees. LHS can only be an integer here ....
# A small predictive recursive descent parser
import astnode as ast
import lexer as lex


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
        self.ASTroot = ast.ASTAssignmentNode  # this will need to change once you introduce the AST program node ....
        # that should become the new root node

    def PeekNextToken(self, k=1):
        peek_index = self.index + k
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
            literal = ast.ASTBooleanLiteralNode(self.crtToken.lexeme)
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
            self.NextToken()

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
        simpleExpressions = []
        simpleExpression1 = self.ParseSimpleExpression()
        if simpleExpression1 is None:
            raise Exception("Expected a simple expression to start parsing an expression")
        simpleExpressions.append(simpleExpression1)
        while self.crtToken == lex.TokenType.RELATIONAL_OPERAND:
            self.NextToken()
            simpleExpressionN = self.ParseSimpleExpression()
            if simpleExpressionN is None:
                raise Exception("No simple expression following relational operand in expression parsing.")
            simpleExpressions.append(simpleExpressionN)
        self.NextToken()
        if self.crtToken.type == lex.TokenType.AS and self.nextToken.type == lex.TokenType.TYPE:
            self.NextToken()
            Type = ast.ASTTypeNode(self.crtToken.lexeme)
            if Type is None:
                raise Exception("Expected 'AS' keyword and Type after simple expression.")
            else:
                return ast.ASTExpressionNode(simpleExpressions, Type)
        else:
            return ast.ASTExpressionNode(simpleExpressions)





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
            self.NextToken()
            expr = self.ParseExpression()
            if expr is None:
                raise Exception("Expected expression after - or not.")
            return ast.ASTUnaryNode(expr)
        else:
            raise Exception("Expected expression to follow - or 'not'. ")

    def ParseSubExpression(self):
        if self.crtToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
            self.NextToken()
            expr = self.ParseExpression()
            if expr is None:
                raise Exception("Expected expression after opening brackets. ")
            if self.crtToken.type == lex.TokenType.RIGHT_ROUND_BRACKET:
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
        elif self.crtToken.type == lex.TokenType.IDENTIFIER:
            if self.nextToken.type == lex.TokenType.LEFT_ROUND_BRACKET:
                factor = self.ParseFunctionCall()
            else:
                factor = ast.ASTIdentifierNode(self.crtToken.lexeme)
                self.NextToken()  # Consume the current token
                print("Variable Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)
        return ast.ASTFactorNode(factor)
    def ParseAssignment(self):
        # Assignment is made up of two main parts; the LHS (the variable) and RHS (the expression)
        if self.crtToken.type == lex.TokenType.IDENTIFIER:
            # create AST node to store the identifier
            assignment_lhs = ast.ASTIdentifierNode(self.crtToken.lexeme)
            self.NextToken()
            print("Variable Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)

        if self.crtToken.type == lex.TokenType.EQUALS:
            # no need to do anything ... token can be discarded
            self.NextToken()
            print("EQ Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)

        # Next sequence of tokens should make up an expression ... therefor call ParseExpression that will return the
        # subtree representing that expression
        assignment_rhs = self.ParseExpression()

        return ast.ASTAssignmentNode(assignment_lhs, assignment_rhs)

    def ParseTerm(self):
        factors = []
        factor1 = self.ParseFactor()
        factors.append(factor1)
        if factor1 is None:
            raise Exception("Initial factor empty when parsing terms.")
        while self.crtToken.type == lex.TokenType.MULTIPLICATIVE_OPERAND:
            self.NextToken()
            factorN = self.ParseFactor()
            if factorN is None:
                raise Exception("No factor following multiplicative operand in term parsing.")
            factors.append(factorN)
        return ast.ASTTermNode(factors)

    def ParseSimpleExpression(self):
        terms = []
        term1 = self.ParseTerm()
        terms.append(term1)
        if term1 is None:
            raise Exception("Initial term empty when parsing simple expression.")
        while self.crtToken.type == lex.TokenType.ADDITIVE_OPERAND:
            self.NextToken()
            termsN = self.ParseTerm()
            if termsN is None:
                raise Exception("No term following additive operand in simple expression parsing.")
            terms.append(termsN)
        return ast.ASTSimpleExpressionNode(terms)

    def ParseStatement(self):
        return self.ParseExpression()
        # if self.crtToken.type in [lex.TokenType.BOOLEAN_LITERAL, lex.TokenType.INTEGER_LITERAL,
        #                           lex.TokenType.FLOAT_LITERAL, lex.TokenType.COLOUR_LITERAL,
        #                           lex.TokenType.PAD_WIDTH, lex.TokenType.PAD_HEIGHT, lex.TokenType.PAD_READ]:
        #     return self.ParseLiteral()
        # elif self.crtToken.type == lex.TokenType.RANDOM_INT:
        #     return self.ParsePadRandI()
        # else:
        #     return self.ParseAssignment()

    def ParseBlock(self):
        # At the moment we only have assignment statements .... you'll need to add more for the assignment -
        # branching depends on the token type

        block = ast.ASTBlockNode()

        while self.crtToken.type != lex.TokenType.END:
            print("New Statement - Processing Initial Token:: ", self.crtToken.type, self.crtToken.lexeme)
            s = self.ParseStatement()
            block.add_statement(s)
            if self.crtToken.type == lex.TokenType.SEMI_COLON:
                self.NextToken()
            else:
                print("Syntax Error - No Semicolon separating statements in block")
                break

        return block

    def ParseProgram(self):
        self.NextToken()  # set crtToken to the first token (skip all WS)
        b = self.ParseBlock()
        return b

    def Parse(self):
        self.ASTroot = self.ParseProgram()


parser = Parser(" xyz * 32.3 - __width / 2 == 2 as bool ;")
parser.Parse()

print_visitor = ast.PrintNodesVisitor()
parser.ASTroot.accept(print_visitor)
