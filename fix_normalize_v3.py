#!/usr/bin/env python3
"""
Fix normalize_minimal() - version 3 (simple line-by-line replacement)
"""

validator_path = "collab_tunnel/validator.py"

# Read the entire file
with open(validator_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing normalize_minimal() in validator.py...")
print("=" * 60)

# Replacement 1: Update step 4 docstring
old_line_1 = "        4. Remove control characters (Unicode category Cc)"
new_line_1 = "        4. Remove control characters (Unicode category Cc), except TAB, LF, CR"

if old_line_1 in content:
    content = content.replace(old_line_1, new_line_1)
    print("OK: Updated step 4 docstring")
else:
    print("SKIP: Step 4 docstring already updated")

# Replacement 2: Update step 5 docstring
old_line_2 = "        5. Collapse ASCII whitespace to single space"
new_line_2 = "        5. Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space"

if old_line_2 in content:
    content = content.replace(old_line_2, new_line_2)
    print("OK: Updated step 5 docstring")
else:
    print("SKIP: Step 5 docstring already updated")

# Replacement 3: Fix the implementation - this is the critical one
# We need to replace the block starting from html.unescape to text.strip()

old_impl = """        text = html.unescape(text)
        text = unicodedata.normalize('NFKC', text)
        text = text.casefold()
        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')
        text = re.sub(r'[ \\t\\n\\r\\f]+', ' ', text)
        return text.strip()"""

new_impl = """        # Step 1: Decode HTML entities
        text = html.unescape(text)
        # Step 2: Unicode NFKC normalization
        text = unicodedata.normalize('NFKC', text)
        # Step 3: Case folding
        text = text.casefold()
        # Step 4: Remove Cc except TAB (U+0009), LF (U+000A), CR (U+000D)
        preserved_cc = {'\t', '\n', '\r'}
        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)
        # Step 5: Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space
        text = re.sub(r'[ \\t\\n\\r]+', ' ', text)
        # Step 6: Trim
        return text.strip()"""

if old_impl in content:
    content = content.replace(old_impl, new_impl)
    print("OK: Updated implementation")
else:
    print("ERROR: Could not find exact implementation block")
    print("Trying with different escaping...")

    # Try without escaped backslashes
    old_impl_alt = """        text = html.unescape(text)
        text = unicodedata.normalize('NFKC', text)
        text = text.casefold()
        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')
        text = re.sub(r'[ \t\n\r\f]+', ' ', text)
        return text.strip()"""

    new_impl_alt = """        # Step 1: Decode HTML entities
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

    if old_impl_alt in content:
        content = content.replace(old_impl_alt, new_impl_alt)
        print("OK: Updated implementation (alt escaping)")
    else:
        print("FATAL: Could not update implementation")
        # Write what we found to debug
        import re
        match = re.search(r"text = html\.unescape\(text\).*?return text\.strip\(\)", content, re.DOTALL)
        if match:
            print("\nFound this block:")
            print(repr(match.group(0)))
        exit(1)

# Write the updated content
with open(validator_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 60)
print("SUCCESS: validator.py updated!")
print("\nChanges made:")
print("  1. Step 4 docstring: added 'except TAB, LF, CR'")
print("  2. Step 5 docstring: specified 'SPACE, TAB, LF, CR'")
print("  3. Step 4 code: preserve TAB, LF, CR before removing Cc")
print("  4. Step 5 code: removed Form Feed from regex")
print("  5. Added inline comments for all 6 steps")
