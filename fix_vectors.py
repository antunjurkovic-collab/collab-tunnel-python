#!/usr/bin/env python3
"""
Fix vectors.py to match updated normalize_minimal() and add Form Feed test
"""

vectors_path = "collab_tunnel/vectors.py"

# Read the file
with open(vectors_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing vectors.py...")
print("=" * 60)

# Fix the normalize_minimal() function
old_normalize = """def normalize_minimal(text: str) -> str:
    text = html.unescape(text)
    text = unicodedata.normalize('NFKC', text)
    text = text.casefold()
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')
    text = re.sub(r'[ \\t\\n\\r\\f]+', ' ', text)
    return text.strip()"""

new_normalize = """def normalize_minimal(text: str) -> str:
    \"\"\"Normalize per TCT spec: preserve TAB, LF, CR in step 4.\"\"\"
    text = html.unescape(text)
    text = unicodedata.normalize('NFKC', text)
    text = text.casefold()
    # Preserve TAB, LF, CR for subsequent whitespace collapsing
    preserved_cc = {'\t', '\n', '\r'}
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)
    text = re.sub(r'[ \\t\\n\\r]+', ' ', text)
    return text.strip()"""

# Try both with and without escaped backslashes
if old_normalize in content:
    content = content.replace(old_normalize, new_normalize)
    print("OK: Updated normalize_minimal() function")
else:
    # Try without escaped backslashes
    old_normalize_alt = """def normalize_minimal(text: str) -> str:
    text = html.unescape(text)
    text = unicodedata.normalize('NFKC', text)
    text = text.casefold()
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')
    text = re.sub(r'[ \t\n\r\f]+', ' ', text)
    return text.strip()"""

    new_normalize_alt = """def normalize_minimal(text: str) -> str:
    \"\"\"Normalize per TCT spec: preserve TAB, LF, CR in step 4.\"\"\"
    text = html.unescape(text)
    text = unicodedata.normalize('NFKC', text)
    text = text.casefold()
    # Preserve TAB, LF, CR for subsequent whitespace collapsing
    preserved_cc = {'\t', '\n', '\r'}
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc' or ch in preserved_cc)
    text = re.sub(r'[ \t\n\r]+', ' ', text)
    return text.strip()"""

    if old_normalize_alt in content:
        content = content.replace(old_normalize_alt, new_normalize_alt)
        print("OK: Updated normalize_minimal() function (alt)")
    else:
        print("ERROR: Could not find normalize_minimal()")

# Add Form Feed test case to demo()
old_cases = """    cases = [
        "Hello\\tWorld\\n",
        "Title\\n\\nBody text with    spaces",
        "A non-breaking B space &amp; HTML -- entity",
        "  Trim  both  ends  ",
        "Line 1\\nLine 2\\r\\nLine 3\\tEnd",
    ]"""

new_cases = """    cases = [
        "Hello\\tWorld\\n",
        "Title\\n\\nBody text with    spaces",
        "A non-breaking B space &amp; HTML -- entity",
        "  Trim  both  ends  ",
        "Line 1\\nLine 2\\r\\nLine 3\\tEnd",
        "Hello\\fWorld\\fTest",  # Form Feed test
    ]"""

if old_cases in content:
    content = content.replace(old_cases, new_cases)
    print("OK: Added Form Feed test case")
else:
    # Try with unescaped version
    old_cases_alt = """    cases = [
        "Hello\tWorld\n",
        "Title\n\nBody text with    spaces",
        "A non-breaking B space &amp; HTML -- entity",
        "  Trim  both  ends  ",
        "Line 1\nLine 2\r\nLine 3\tEnd",
    ]"""

    new_cases_alt = """    cases = [
        "Hello\tWorld\n",
        "Title\n\nBody text with    spaces",
        "A non-breaking B space &amp; HTML -- entity",
        "  Trim  both  ends  ",
        "Line 1\nLine 2\r\nLine 3\tEnd",
        "Hello\fWorld\fTest",  # Form Feed test
    ]"""

    if old_cases_alt in content:
        content = content.replace(old_cases_alt, new_cases_alt)
        print("OK: Added Form Feed test case (alt)")
    else:
        print("ERROR: Could not add Form Feed test case")

# Write the updated file
with open(vectors_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 60)
print("SUCCESS: vectors.py updated!")
print("\nChanges made:")
print("  1. Updated normalize_minimal() to preserve TAB, LF, CR")
print("  2. Added Form Feed test case: 'Hello\\fWorld\\fTest'")
