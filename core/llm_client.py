import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load the secret API Key from your .env file
load_dotenv()

# Initialize our free Groq Engine Client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

SYSTEM_PROMPT = """
You are an elite Senior Staff Engineer and automated Code Review Agent. 
Your task is to analyze Python code blocks and generate structured review feedback.

You must respond ONLY with a single JSON object containing a key named "comments", which holds an array of findings.

Each finding inside the "comments" array must contain exactly these keys:
- "target_name": (string) Name of function/class analyzed.
- "line_number": (integer) Starting line number.
- "severity": (string choosing ONLY from: "Critical", "Warning", "Suggestion", "Optimization")
- "category": (string choosing ONLY from: "Security", "Code Style", "Performance", "Bug Risk", "Documentation")
- "comment": (string) Detailed technical review explaining the issue and how to resolve it.
- "confidence_score": (integer from 0 to 100 representing certainty. For definitive bugs or security flaws, give 85-100. For subjective recommendations or stylistic preferences, give below 70).
- "suggested_fix": (string) Refactored code block showing the fix.

Example Output Structure:
{
  "comments": [
    {
      "target_name": "example_func",
      "line_number": 10,
      "severity": "Warning",
      "category": "Bug Risk",
      "comment": "Description of issue...",
      "confidence_score": 90,
      "suggested_fix": "def example_func():\\n    ..."
    }
  ]
}
"""

def analyze_code_structures(structures: list) -> list:
    """
    Feeds extracted AST structures into the AI model,
    enforces structured outputs, and parses JSON blocks cleanly.
    """
    if not client:
        raise RuntimeError("Groq API client is not initialized. Please verify your .env file.")

    all_comments = []

    for item in structures:
        user_content = f"""
        Analyze this block:
        File Position: {item['file_path']}
        Block Type: {item['type']}
        Block Name: {item['name']}
        Starting Line: {item['line']}
        
        Source Code:
        {item['code']}
        """

        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.2, 
                response_format={"type": "json_object"} 
            )

            raw_response = chat_completion.choices[0].message.content
            parsed_json = json.loads(raw_response)
            
            # Extract comments array adaptively
            if "comments" in parsed_json and isinstance(parsed_json["comments"], list):
                all_comments.extend(parsed_json["comments"])
            elif isinstance(parsed_json, dict) and "target_name" in parsed_json:
                all_comments.append(parsed_json)
                
        except Exception as e:
            print(f"⚠️ Failed to analyze code structure '{item['name']}': {e}")
            continue

    return all_comments