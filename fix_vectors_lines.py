#!/usr/bin/env python3
"""
Fix vectors.py using line-by-line editing
"""

with open('collab_tunnel/vectors.py', 'r') as f:
    lines = f.readlines()

# Line 17-18: Update normalize_minimal implementation
# Line 17 (index 16): text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')
# Replace with two lines
lines[16] = "    preserved_cc = {chr(9), chr(10), chr(13)}  # TAB, LF, CR\n"
lines.insert(17, "    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)\n")

# Line 18 (now 19 after insert): remove \f from regex
lines[18] = "    text = re.sub(r'[ \\t\\n\\r]+', ' ', text)\n"

# Line 41 (now 42 after insert): Add Form Feed test case before closing bracket
# Find the line with "Line 1\nLine 2..." and add a new case after it
for i, line in enumerate(lines):
    if 'Line 1\\nLine 2\\r\\nLine 3\\tEnd' in line:
        # Add new test case after this line
        lines.insert(i+1, '        "Hello\\fWorld\\fTest",  # Form Feed test (U+000C)\n')
        print(f"Added Form Feed test case after line {i+1}")
        break

# Write back
with open('collab_tunnel/vectors.py', 'w') as f:
    f.writelines(lines)

print("Fixed vectors.py")

# Test syntax
content = ''.join(lines)
try:
    compile(content, 'vectors.py', 'exec')
    print("Syntax: OK")
except SyntaxError as e:
    print(f"Syntax error: {e}")
    import sys
    sys.exit(1)
