#!/usr/bin/env python3
"""
Fix normalize_minimal() to preserve TAB, LF, CR in step 4 per updated spec
"""

import re

validator_path = "collab_tunnel/validator.py"

# Read the file
with open(validator_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing normalize_minimal() in validator.py...")
print("=" * 60)

# Replace the entire normalize_minimal method
old_method = '''    @staticmethod
    def normalize_minimal(text: str) -> str:
        """
        Normalize plain-text content following TCT spec (diagnostics only).

        6-step normalization pipeline:
        1. Decode HTML entities (&amp; → &, &#x2014; → —)
        2. Apply Unicode NFKC normalization
        3. Apply Unicode case folding (locale-independent lowercase)
        4. Remove control characters (Unicode category Cc)
        5. Collapse ASCII whitespace to single space
        6. Trim leading/trailing whitespace

        Args:
            text: Plain-text content string (no HTML markup)

        Returns:
            Normalized text ready for SHA-256 hashing
        """
        text = html.unescape(text)
        text = unicodedata.normalize('NFKC', text)
        text = text.casefold()
        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')
        text = re.sub(r'[ \\t\\n\\r\\f]+', ' ', text)
        return text.strip()'''

new_method = '''    @staticmethod
    def normalize_minimal(text: str) -> str:
        """
        Normalize plain-text content following TCT spec (diagnostics only).

        6-step normalization pipeline:
        1. Decode HTML entities (&amp; → &, &#x2014; → —)
        2. Apply Unicode NFKC normalization
        3. Apply Unicode case folding (locale-independent lowercase)
        4. Remove control characters (Unicode category Cc), except TAB, LF, CR
        5. Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space
        6. Trim leading/trailing whitespace

        Args:
            text: Plain-text content string (no HTML markup)

        Returns:
            Normalized text ready for SHA-256 hashing
        """
        # Step 1: Decode HTML entities
        text = html.unescape(text)
        # Step 2: Unicode NFKC normalization
        text = unicodedata.normalize('NFKC', text)
        # Step 3: Case folding
        text = text.casefold()
        # Step 4: Remove Cc except TAB (U+0009), LF (U+000A), CR (U+000D)
        preserved_cc = {'\\t', '\\n', '\\r'}
        text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)
        # Step 5: Collapse ASCII whitespace (SPACE, TAB, LF, CR) to single space
        text = re.sub(r'[ \\t\\n\\r]+', ' ', text)
        # Step 6: Trim
        return text.strip()'''

if old_method in content:
    content = content.replace(old_method, new_method)
    print("✓ Updated normalize_minimal() method")
else:
    print("✗ Could not find exact match for old method")
    print("  Trying alternative regex replacement...")

    # Try a more flexible regex-based replacement
    pattern = r'(@staticmethod\s+def normalize_minimal\(text: str\) -> str:.*?return text\.strip\(\))'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content.replace(match.group(0), new_method)
        print("✓ Updated normalize_minimal() using regex")
    else:
        print("✗ Failed to update - manual intervention required")
        exit(1)

# Write the updated file
with open(validator_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 60)
print("✓ validator.py updated successfully!")
print("\nChanges made:")
print("  1. Updated docstring: 'Remove control characters (Cc), except TAB, LF, CR'")
print("  2. Added preserved_cc set with TAB, LF, CR")
print("  3. Updated step 4 to preserve TAB, LF, CR")
print("  4. Removed Form Feed (\\f) from step 5 regex")
print("  5. Added inline comments for each step")
