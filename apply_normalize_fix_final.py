#!/usr/bin/env python3
"""
Apply normalize_minimal fix to validator.py - FINAL VERSION
Uses careful string handling to avoid escape sequence issues
"""

validator_path = "collab_tunnel/validator.py"

# Read the file
with open(validator_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Applying normalize_minimal fix to validator.py...")
print("=" * 60)

# Define the old and new code blocks carefully
# OLD: The original implementation without TAB/LF/CR preservation
old_block = """        text = html.unescape(text)
        text = unicodedata.normalize('NFKC', text)
        text = text.casefold()
        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')
        text = re.sub(r'[ \t\n\r\f]+', ' ', text)
        return text.strip()"""

# NEW: With TAB/LF/CR preservation and comments
# Using raw string to preserve escape sequences properly
new_block = r"""        # Step 1: Decode HTML entities
        text = html.unescape(text)
        # Step 2: Unicode NFKC normalization
        text = unicodedata.normalize('NFKC', text)
        # Step 3: Case folding
        text = text.casefold()
        # Step 4: Remove Cc except TAB (U+0009), LF (U+000A), CR (U+000D)
        preserved_cc = {'\t', '\n', '\r'}
        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)
        # Step 5: Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space
        text = re.sub(r'[ \t\n\r]+', ' ', text)
        # Step 6: Trim
        return text.strip()"""

# Also update the docstrings
old_doc_step4 = "        4. Remove control characters (Unicode category Cc)"
new_doc_step4 = "        4. Remove control characters (Unicode category Cc), except TAB, LF, CR"

old_doc_step5 = "        5. Collapse ASCII whitespace to single space"
new_doc_step5 = "        5. Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space"

# Apply replacements
if old_block in content:
    content = content.replace(old_block, new_block)
    print("OK: Replaced implementation code")
else:
    print("ERROR: Could not find old implementation block")
    exit(1)

if old_doc_step4 in content:
    content = content.replace(old_doc_step4, new_doc_step4)
    print("OK: Updated step 4 docstring")
else:
    print("SKIP: Step 4 docstring already updated or not found")

if old_doc_step5 in content:
    content = content.replace(old_doc_step5, new_doc_step5)
    print("OK: Updated step 5 docstring")
else:
    print("SKIP: Step 5 docstring already updated or not found")

# Write back
with open(validator_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 60)
print("SUCCESS!")
print("\nVerifying fix...")

# Try to import to verify syntax
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("validator", validator_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("OK: Module imports successfully - no syntax errors!")
except SyntaxError as e:
    print(f"ERROR: Syntax error: {e}")
    exit(1)
except Exception as e:
    print(f"WARNING: Import failed but may be due to dependencies: {e}")
