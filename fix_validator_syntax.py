#!/usr/bin/env python3
"""
Fix syntax error in validator.py - replace literal chars with escape sequences
"""

validator_path = "collab_tunnel/validator.py"

# Read the file as binary to handle control characters
with open(validator_path, 'rb') as f:
    content = f.read()

print("Fixing syntax error in validator.py...")
print("=" * 60)

# Convert to string
content_str = content.decode('utf-8', errors='replace')

# Find the problematic line and replace it
# The line has literal TAB, LF, CR characters which need to be escaped

import re

# Replace the bad preserved_cc line with the correct one
# Look for the pattern with any characters in the set
pattern = r"preserved_cc = \{[^\}]+\}"
replacement = r"preserved_cc = {'\t', '\n', '\r'}"

match = re.search(pattern, content_str)
if match:
    print(f"Found problematic line: {repr(match.group(0))}")
    content_str = re.sub(pattern, replacement, content_str)
    print(f"Replaced with: {repr(replacement)}")
else:
    print("ERROR: Could not find preserved_cc pattern")
    exit(1)

# Write back
with open(validator_path, 'w', encoding='utf-8') as f:
    f.write(content_str)

print("=" * 60)
print("SUCCESS: Syntax error fixed!")
print("Now using proper escape sequences: \\t, \\n, \\r")
