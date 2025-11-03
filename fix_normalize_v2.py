#!/usr/bin/env python3
"""
Fix normalize_minimal() - version 2
"""

validator_path = "collab_tunnel/validator.py"

# Read the file
with open(validator_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Fixing normalize_minimal() in validator.py...")

# Find and replace the critical lines
modified = False
for i, line in enumerate(lines):
    # Fix step 4 docstring
    if i > 60 and i < 75 and "4. Remove control characters (Unicode category Cc)" in line:
        lines[i] = "        4. Remove control characters (Unicode category Cc), except TAB, LF, CR\n"
        print(f"Line {i+1}: Updated step 4 docstring")
        modified = True

    # Fix step 5 docstring
    if i > 60 and i < 75 and "5. Collapse ASCII whitespace to single space" in line:
        lines[i] = "        5. Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space\n"
        print(f"Line {i+1}: Updated step 5 docstring")
        modified = True

    # Add comments and fix step 4 implementation
    if i > 75 and i < 90:
        # Replace the old implementation lines with new ones
        if "text = html.unescape(text)" in line:
            lines[i] = "        # Step 1: Decode HTML entities\n"
            lines.insert(i+1, "        text = html.unescape(text)\n")
            print(f"Line {i+1}: Added step 1 comment")
            modified = True

        if "text = unicodedata.normalize('NFKC', text)" in line and "# Step 2" not in lines[i-1]:
            lines[i] = "        # Step 2: Unicode NFKC normalization\n"
            lines.insert(i+1, "        text = unicodedata.normalize('NFKC', text)\n")
            print(f"Line {i+1}: Added step 2 comment")
            modified = True

        if "text = text.casefold()" in line and "# Step 3" not in lines[i-1]:
            lines[i] = "        # Step 3: Case folding\n"
            lines.insert(i+1, "        text = text.casefold()\n")
            print(f"Line {i+1}: Added step 3 comment")
            modified = True

        # This is the critical fix - replace the step 4 implementation
        if "''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')" in line:
            lines[i] = "        # Step 4: Remove Cc except TAB (U+0009), LF (U+000A), CR (U+000D)\n"
            lines.insert(i+1, "        preserved_cc = {'\t', '\n', '\r'}\n")
            lines.insert(i+2, "        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)\n")
            print(f"Line {i+1}: Fixed step 4 - now preserves TAB, LF, CR")
            modified = True

        # Fix step 5 - remove \f (form feed) from regex
        if "re.sub(r'[ \\t\\n\\r\\f]+', ' ', text)" in line:
            lines[i] = "        # Step 5: Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space\n"
            lines.insert(i+1, "        text = re.sub(r'[ \\t\\n\\r]+', ' ', text)\n")
            print(f"Line {i+1}: Fixed step 5 - removed Form Feed from regex")
            modified = True

        if "return text.strip()" in line and "# Step 6" not in lines[i-1]:
            lines[i] = "        # Step 6: Trim\n"
            lines.insert(i+1, "        return text.strip()\n")
            print(f"Line {i+1}: Added step 6 comment")
            modified = True

if modified:
    # Write back
    with open(validator_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("\nFile updated successfully!")
else:
    print("\nNo changes made - pattern not found")
