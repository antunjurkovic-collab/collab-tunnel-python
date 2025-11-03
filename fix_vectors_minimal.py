#!/usr/bin/env python3
"""
Fix vectors.py - minimal version
"""

with open('collab_tunnel/vectors.py', 'r') as f:
    content = f.read()

# Fix normalize_minimal function
old_line = "    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')\n"
new_lines = "    preserved_cc = {chr(9), chr(10), chr(13)}  # TAB, LF, CR\n    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)\n"

content = content.replace(old_line, new_lines)

# Remove \f from regex
old_regex = "    text = re.sub(r'[ \\t\\n\\r\\f]+', ' ', text)\n"
new_regex = "    text = re.sub(r'[ \\t\\n\\r]+', ' ', text)\n"

content = content.replace(old_regex, new_regex)

# Add Form Feed test case
old_cases = '''    cases = [
        "Hello\\tWorld\\n",
        "Title\\n\\nBody text with    spaces",
        "A non-breaking B space &amp; HTML -- entity",
        "  Trim  both  ends  ",
        "Line 1\\nLine 2\\r\\nLine 3\\tEnd",
    ]'''

new_cases = '''    cases = [
        "Hello\\tWorld\\n",
        "Title\\n\\nBody text with    spaces",
        "A non-breaking B space &amp; HTML -- entity",
        "  Trim  both  ends  ",
        "Line 1\\nLine 2\\r\\nLine 3\\tEnd",
        "Hello\\fWorld\\fTest",  # Form Feed test (U+000C)
    ]'''

content = content.replace(old_cases, new_cases)

# Write back
with open('collab_tunnel/vectors.py', 'w') as f:
    f.write(content)

print("Fixed vectors.py")

# Test syntax
try:
    compile(content, 'vectors.py', 'exec')
    print("Syntax: OK")
except SyntaxError as e:
    print(f"Syntax error: {e}")
    exit(1)
