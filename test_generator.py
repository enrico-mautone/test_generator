import os
import ast
import argparse

def parse_functions_from_file(filepath):
    """Parsa un file Python e restituisce una lista di nomi di funzioni"""
    with open(filepath, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=filepath)
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def create_test_file(module_name, functions, output_dir):
    """Crea un file di test per il modulo specificato"""
    test_filename = os.path.join(output_dir, f"test_{module_name}.py")
    with open(test_filename, "w", encoding="utf-8") as test_file:
        test_file.write("import unittest\n")
        test_file.write(f"from {module_name} import *\n\n")
        
        for func in functions:
            test_file.write(f"class Test{func.capitalize()}(unittest.TestCase):\n")
            test_file.write(f"    def test_{func}(self):\n")
            test_file.write(f"        # TODO: Implement test for {func}\n")
            test_file.write(f"        pass\n\n")
    
    print(f"Creato {test_filename}")

def main():
    parser = argparse.ArgumentParser(description="Genera test unitari per un progetto Python")
    parser.add_argument("source_dir", help="Path alla cartella dei sorgenti")
    parser.add_argument("output_dir", nargs='?', help="Path alla cartella di output", default=None)
    
    args = parser.parse_args()
    source_dir = args.source_dir
    output_dir = args.output_dir
    
    if output_dir is None:
        output_dir = source_dir.rstrip('/\\') + 'Test'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                module_name = os.path.splitext(file)[0]
                filepath = os.path.join(root, file)
                functions = parse_functions_from_file(filepath)
                if functions:
                    create_test_file(module_name, functions, output_dir)

if __name__ == "__main__":
    main()
