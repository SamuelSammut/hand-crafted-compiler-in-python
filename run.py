from parser import Parser
from print_ast_visitor import PrintNodesVisitor
from semantic_visitor import SemanticVisitor
from code_generation import CodeGenerationVisitor

with open('code.par', 'r') as file:
    code = file.read()

code = code.replace('\n', '').replace('\r', '')

parser = Parser(code)
parser.Parse()


print_ast = PrintNodesVisitor()
semantic_visitor = SemanticVisitor()
code_generation = CodeGenerationVisitor()

parser.ASTroot.accept(print_ast)
parser.ASTroot.accept(semantic_visitor)

generated = code_generation.generate(parser.ASTroot)

print("GENERATED CODE:")
print(generated)

print("Semantic analysis completed successfully!")



