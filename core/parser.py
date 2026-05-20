import ast

def parse_python_file(file_path: str) -> list:
    """
    Reads a Python file, builds its Abstract Syntax Tree (AST), 
    and isolates functions and classes with their raw code segments.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    try:
        # Build the structural language tree map
        tree = ast.parse(source_code)
    except SyntaxError:
        print(f"⚠️ Skipping unparseable file due to syntax compilation errors: {file_path}")
        return []

    structures = []
    lines = source_code.splitlines()

    # Traverse all components in the syntax layout
    for node in ast.walk(tree):
        # 1. Target standard or async functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start_line = node.lineno
            # Fetch ending lines securely (handles variations across different Python versions)
            end_line = getattr(node, 'end_lineno', len(lines))
            func_code = "\n".join(lines[start_line-1:end_line])
            
            structures.append({
                "type": "function",
                "name": node.name,
                "line": start_line,
                "code": func_code,
                "file_path": file_path
            })
            
        # 2. Target object classes
        elif isinstance(node, ast.ClassDef):
            start_line = node.lineno
            end_line = getattr(node, 'end_lineno', len(lines))
            class_code = "\n".join(lines[start_line-1:end_line])
            
            structures.append({
                "type": "class",
                "name": node.name,
                "line": start_line,
                "code": class_code,
                "file_path": file_path
            })
            
    return structures