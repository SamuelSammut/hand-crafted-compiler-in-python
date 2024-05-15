from parser import Parser
from ast_node import *
from print_ast_visitor import PrintNodesVisitor
from semantic_visitor import SemanticVisitor

# Read code from a file
with open('code.par', 'r') as file:
    code = file.read()

# Remove new lines which generate a bad character in lexer
code = code.replace('\n', '').replace('\r', '')

# Initialize the parser with the code read from the file
parser = Parser(code)
parser.Parse()
#
# TEST RETURN TYPE IF WE CAN HAVE VOID AS TYPE MUST BE DECLARED IN FUNC DECLAR BUT RETURN CAN BE MISSING

# Initialize visitors
print_ast = PrintNodesVisitor()
semantic_visitor = SemanticVisitor()

# Accept visitors
parser.ASTroot.accept(print_ast)
parser.ASTroot.accept(semantic_visitor)

# Print success message if semantic analysis is successful
print("Semantic analysis completed successfully!")



