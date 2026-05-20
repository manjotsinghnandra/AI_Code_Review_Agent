import os
from core.parser import parse_python_file

print("🔍 Beginning AST Parsing checks...")

# Force it to look directly at our new mock file
found_py_file = "mock_code.py"

if not os.path.exists(found_py_file):
    print(f"❌ Error: {found_py_file} not found! Please create it first.")
else:
    # Run the parsing logic on our mock code file
    extracted_items = parse_python_file(found_py_file)
    
    print(f"🎯 Successfully parsed target: {found_py_file}")
    print(f"📦 Extracted {len(extracted_items)} structural code components.")
    
    for item in extracted_items:
        print(f"\n🔹 Type: {item['type'].upper()} | Name: {item['name']} (Line {item['line']})")
        print("--- Code Excerpt ---")
        print(item['code'])
        print("--------------------")