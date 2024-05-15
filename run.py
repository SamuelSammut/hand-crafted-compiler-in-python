from parser import Parser
from ast_node import *
from print_ast_visitor import PrintNodesVisitor
from semantic_visitor import SemanticVisitor
from code_generation import CodeGenerationVisitor

# Read code from a file
with open('code.par', 'r') as file:
    code = file.read()

# Remove new lines which generate a bad character in lexer
code = code.replace('\n', '').replace('\r', '')

# Initialize the parser with the code read from the file
parser = Parser(code)
parser.Parse()


# Initialize visitors
print_ast = PrintNodesVisitor()
semantic_visitor = SemanticVisitor()
code_generation = CodeGenerationVisitor()

# Accept visitors
parser.ASTroot.accept(print_ast)
parser.ASTroot.accept(semantic_visitor)

generated = code_generation.generate(parser.ASTroot)

print("GENERATED CODE:")
print(generated)

# Print success message if semantic analysis is successful
print("Semantic analysis completed successfully!")



