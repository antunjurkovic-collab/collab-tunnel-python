"""
Content validator for TCT protocol
"""

import hashlib
import html
import re
import unicodedata
from typing import Dict, Any, List, Optional


class ContentValidator:
    """
    Validates TCT protocol compliance and content integrity.
    """

    @staticmethod
    def validate_etag(etag: str, content: str) -> bool:
        """
        Validate that ETag matches content hash.

        Args:
            etag: ETag header value (e.g., W/"sha256-abc123..." or "sha256-abc123...")
            content: Content text to hash

        Returns:
            True if ETag matches content hash
        """
        # Extract hash from ETag (remove W/ prefix, quotes, and sha256- prefix)
        etag_clean = etag
        if etag_clean.startswith('W/'):
            etag_clean = etag_clean[2:]  # Strip weak prefix
        etag_hash = etag_clean.replace('"', '').replace('sha256-', '')

        # Normalize content (lowercase, collapse whitespace)
        normalized = ContentValidator.normalize_text(content)

        # Compute SHA256
        computed_hash = hashlib.sha256(normalized.encode('utf-8')).hexdigest()

        return etag_hash == computed_hash

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text following TCT 7-step normalization pipeline:
        1. Strip HTML tags and script/style elements
        2. Decode HTML entities (&amp; → &, &#x2014; → —)
        3. Convert to lowercase (Unicode-aware)
        4. Collapse whitespace to single space (\\s+ → " ")
        5. Remove punctuation/symbols (Unicode P,S categories)
        6. Trim leading/trailing whitespace
        7. Ready for SHA-256 hashing

        Args:
            text: Input text (may contain HTML)

        Returns:
            Normalized text ready for hashing
        """
        # Step 1: Strip HTML tags (including script/style content)
        # Remove script and style tags entirely
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remove all other HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Step 2: Decode HTML entities
        text = html.unescape(text)

        # Step 3: Convert to lowercase (Unicode-aware)
        text = text.lower()

        # Step 4: Collapse whitespace to single space
        text = re.sub(r'\s+', ' ', text)

        # Step 5: Remove punctuation and symbols (Unicode categories P and S)
        # Unicode categories: P = Punctuation, S = Symbols
        text = ''.join(
            char if unicodedata.category(char) not in ('Pc', 'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps',
                                                         'Sc', 'Sk', 'Sm', 'So')
            else ' '
            for char in text
        )

        # Re-collapse whitespace after punctuation removal
        text = re.sub(r'\s+', ' ', text)

        # Step 6: Trim leading/trailing whitespace
        text = text.strip()

        # Step 7: Ready for SHA-256 (caller handles hashing)
        return text

    @staticmethod
    def check_headers(headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Check TCT protocol compliance of HTTP headers.

        Args:
            headers: Dictionary of HTTP headers

        Returns:
            Dictionary with compliance check results
        """
        results = {
            'compliant': True,
            'checks': {},
            'errors': []
        }

        # Check Content-Type
        content_type = headers.get('content-type', '').lower()
        results['checks']['json_content_type'] = 'application/json' in content_type

        if not results['checks']['json_content_type']:
            results['errors'].append("Content-Type should be application/json")
            results['compliant'] = False

        # Check ETag
        etag = headers.get('etag', '')
        results['checks']['etag_present'] = bool(etag)
        results['checks']['etag_format'] = False
        results['checks']['etag_weak'] = False

        if etag:
            # Accept both weak (W/"sha256-...") and strong ("sha256-...") ETags
            etag_clean = etag
            if etag_clean.startswith('W/'):
                results['checks']['etag_weak'] = True
                etag_clean = etag_clean[2:]

            results['checks']['etag_format'] = (
                etag_clean.startswith('"sha256-') or
                etag_clean.startswith('sha256-')
            )
            if not results['checks']['etag_format']:
                results['errors'].append("ETag should contain 'sha256-' hash")
                results['compliant'] = False
        else:
            results['errors'].append("ETag header missing")
            results['compliant'] = False

        # Check Link canonical
        link = headers.get('link', '')
        results['checks']['canonical_link'] = 'rel="canonical"' in link.lower()

        if not results['checks']['canonical_link']:
            results['errors'].append("Link header missing rel='canonical'")
            results['compliant'] = False

        # Check Cache-Control
        cache_control = headers.get('cache-control', '').lower()
        results['checks']['must_revalidate'] = 'must-revalidate' in cache_control
        results['checks']['stale_while_revalidate'] = 'stale-while-revalidate' in cache_control

        if not results['checks']['must_revalidate']:
            results['errors'].append("Cache-Control should include must-revalidate")

        # Check Vary (should be Accept-Encoding, not Accept)
        vary = headers.get('vary', '').lower()
        results['checks']['vary_accept_encoding'] = 'accept-encoding' in vary

        if not results['checks']['vary_accept_encoding']:
            results['errors'].append("Vary header should include Accept-Encoding")

        return results

    @staticmethod
    def validate_sitemap_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single sitemap item structure.

        Args:
            item: Sitemap item dictionary

        Returns:
            Validation results
        """
        results = {
            'valid': True,
            'errors': []
        }

        # Check required fields
        required_fields = ['cUrl', 'mUrl', 'contentHash']
        for field in required_fields:
            if field not in item:
                results['errors'].append(f"Missing required field: {field}")
                results['valid'] = False

        # Check URL format
        if 'cUrl' in item and not item['cUrl'].startswith('http'):
            results['errors'].append("cUrl must be absolute URL")
            results['valid'] = False

        if 'mUrl' in item and not item['mUrl'].startswith('http'):
            results['errors'].append("mUrl must be absolute URL")
            results['valid'] = False

        # Check hash format
        if 'contentHash' in item:
            hash_val = item['contentHash']
            if not (hash_val.startswith('sha256-') or re.match(r'^[a-f0-9]{64}$', hash_val)):
                results['errors'].append("contentHash must be sha256 hash")
                results['valid'] = False

        # Check modified date format (if present)
        if 'modified' in item:
            modified = item['modified']
            if not re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', modified):
                results['errors'].append("modified must be ISO 8601 format")
                results['valid'] = False

        return results
