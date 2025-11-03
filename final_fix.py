#!/usr/bin/env python3
# Read validator.py
with open('collab_tunnel/validator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Update specific lines by line number (1-indexed in editor, 0-indexed in list)
# Line 71: step 4 docstring
lines[70] = "        4. Remove control characters (Unicode category Cc), except TAB, LF, CR\n"

# Line 72: step 5 docstring
lines[71] = "        5. Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space\n"

# Lines 81-86: implementation
# Insert comments and update step 4 and 5
new_impl = [
    "        # Step 1: Decode HTML entities\n",
    "        text = html.unescape(text)\n",
    "        # Step 2: Unicode NFKC normalization\n",
    "        text = unicodedata.normalize('NFKC', text)\n",
    "        # Step 3: Case folding\n",
    "        text = text.casefold()\n",
    "        # Step 4: Remove Cc except TAB (U+0009), LF (U+000A), CR (U+000D)\n",
    "        preserved_cc = {chr(9), chr(10), chr(13)}  # TAB, LF, CR\n",
    "        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)\n",
    "        # Step 5: Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space\n",
    "        text = re.sub(r'[ \\t\\n\\r]+', ' ', text)\n",
    "        # Step 6: Trim\n",
    "        return text.strip()\n",
]

# Replace lines 80-85 (0-indexed: 80-86)
lines[80:86] = new_impl

# Write back
with open('collab_tunnel/validator.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("File updated successfully!")

# Verify syntax
try:
    compile(open('collab_tunnel/validator.py').read(), 'collab_tunnel/validator.py', 'exec')
    print("Syntax check: PASSED")
except SyntaxError as e:
    print(f"Syntax error: {e}")
    import sys
    sys.exit(1)
