#!/usr/bin/env python3
"""
Minimal fix - just change the two critical lines
"""

with open('collab_tunnel/validator.py', 'r') as f:
    content = f.read()

# Fix 1: Update docstrings
content = content.replace(
    "        4. Remove control characters (Unicode category Cc)\n",
    "        4. Remove control characters (Unicode category Cc), except TAB, LF, CR\n"
)

content = content.replace(
    "        5. Collapse ASCII whitespace to single space\n",
    "        5. Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space\n"
)

# Fix 2: Update implementation - the critical line 84
# OLD: text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')
# NEW: add preserved_cc logic

old_line_84 = "        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')\n"
new_lines_84 = "        preserved_cc = {chr(9), chr(10), chr(13)}  # TAB, LF, CR\n        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)\n"

content = content.replace(old_line_84, new_lines_84)

# Fix 3: Update line 85 - remove \f from regex
old_line_85 = "        text = re.sub(r'[ \\t\\n\\r\\f]+', ' ', text)\n"
new_line_85 = "        text = re.sub(r'[ \\t\\n\\r]+', ' ', text)\n"

content = content.replace(old_line_85, new_line_85)

# Write back
with open('collab_tunnel/validator.py', 'w') as f:
    f.write(content)

print("Applied minimal fix")

# Test syntax
try:
    compile(content, 'validator.py', 'exec')
    print("Syntax: OK")
except SyntaxError as e:
    print(f"Syntax error: {e}")
    exit(1)
