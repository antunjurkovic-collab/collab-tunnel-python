# Changelog

All notable changes to the collab-tunnel Python client library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
