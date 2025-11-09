# Changelog

All notable changes to the collab-tunnel Python client library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-09

### BREAKING CHANGES

This release updates the library to comply with **draft-jurkovikj-collab-tunnel-01**. Several breaking API changes have been made:

#### 1. Sitemap Field Renamed
- **Old:** `contentHash`
- **New:** `etag`
- **Impact:** Code accessing `item['contentHash']` will fail
- **Migration:** Replace all `contentHash` references with `etag`

```python
# Before (1.x):
for item in sitemap.items:
    hash = item['contentHash']

# After (2.0):
for item in sitemap.items:
    etag = item['etag']
```

#### 2. Weak ETags Now Rejected
- **Old:** Weak ETags (`W/"..."`) generated warnings but were accepted
- **New:** Weak ETags are rejected as non-compliant per draft-01 Section 6.2
- **Impact:** Implementations using weak ETags will fail validation
- **Migration:** Ensure M-URLs return strong ETags only (no `W/` prefix)

#### 3. Validator Function Signature Changed
- **Old:** `validate_parity(sitemap_hash, etag, payload_hash)`
- **New:** `validate_parity(sitemap_etag, response_etag, payload_hash)`
- **Impact:** Code using positional arguments with old parameter names
- **Migration:** Update parameter names (functionality unchanged)

### Changed
- Updated all documentation and docstrings to reference draft-01
- Updated `SitemapParser` to require `etag` field instead of `contentHash`
- Updated `ContentValidator.validate_sitemap_item()` to check for `etag` field
- Updated `CollabTunnelCrawler.should_fetch()` to use `etag` for zero-fetch optimization
- Updated error messages to specify draft-01 section references

### Removed
- Removed all references to Method B (draft-01 only allows Method A)
- Removed support for weak ETags in validator

## [1.0.1] - 2025-10-31

### Fixed
- **normalize_minimal()**: Fixed TAB, LF, CR preservation in step 4 (remove control characters)
  - Now correctly preserves TAB (U+0009), LF (U+000A), CR (U+000D) for subsequent whitespace collapsing in step 5
  - Aligns with TCT specification requirements for content-string normalization
  - Commit: 2d99b8d

### Changed
- Updated README for specification alignment and consistency
- Improved documentation with profile field validation examples

### Removed
- Removed internal setup guides from public repository

## [1.0.0] - 2025-10-17

### Added
- Initial release of Collaboration Tunnel Protocol (TCT) Python client
- Core crawler implementation with sitemap-first verification
- Content fingerprint validation (parity-only)
- Conditional GET support with If-None-Match
- ETag validation and cache control
- Diagnostic normalization function (normalize_minimal)
- Command-line interface (collab-tunnel CLI)
- Complete test suite with test vectors
- Comprehensive documentation and examples

### Features
- Zero-fetch optimization via sitemap contentHash comparison
- 304 Not Modified support for bandwidth savings
- Weak ETag validation per TCT specification
- RFC 9110, 9111, 8288 compliance
- Python 3.7+ support
