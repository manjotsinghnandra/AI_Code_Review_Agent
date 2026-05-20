from core.parser import parse_python_file
from core.llm_client import analyze_code_structures

print("🚀 Testing AI Code Review Agent Pipeline...")

# Step 1: Parse the local code
structures = parse_python_file("mock_code.py")
print(f"📦 Local AST parsed. Submitting {len(structures)} blocks to the Free AI Model...")

# Step 2: Feed structures into the AI review helper
ai_feedback = analyze_code_structures(structures)

print(f"\n✨ AI Analysis Completed! Received {len(ai_feedback)} review findings:")
print("=" * 60)

for index, comment in enumerate(ai_feedback, 1):
    print(f"\n📢 Finding #{index}:")
    print(f"🔹 Location: {comment.get('target_name')} (Line {comment.get('line_number')})")
    print(f"🔹 Category: {comment.get('category')} | Severity: {comment.get('severity')}")
    print(f"🧠 Confidence Level: {comment.get('confidence_score')}%")
    print(f"📝 Review Comment:\n{comment.get('comment')}")
    print(f"🛠️ Suggested Solution:\n{comment.get('suggested_fix')}")
    print("-" * 60)