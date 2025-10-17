# PyPI Publishing Guide - GitHub Trusted Publisher Method

## ✅ Files Created (Ready)

Your Python package is now ready with:
- `pyproject.toml` - Modern Python package configuration
- `setup.py` - Legacy setup (for compatibility)
- `LICENSE` - MIT License with patent notice
- `MANIFEST.in` - Package file inclusion rules
- `.gitignore` - Git ignore patterns
- `.github/workflows/publish.yml` - Automated publishing workflow

## Step-by-Step Publishing Process

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `collab-tunnel-python`
3. Description: "Python client library for the Collaboration Tunnel Protocol (TCT)"
4. Make it **Public** (required for PyPI)
5. Do NOT initialize with README (you already have one)
6. Click "Create repository"

### Step 2: Push Your Code to GitHub

Open terminal in `C:\Users\Antun\desktop\claude\partners\tools\python\` and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial release v1.0.0 - Collaboration Tunnel Protocol Python client"

# Add your GitHub repository as remote (replace 'yourusername' with your actual GitHub username)
git remote add origin https://github.com/yourusername/collab-tunnel-python.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Configure PyPI Trusted Publisher

**Now go back to PyPI where you saw the options:**

1. Click on **GitHub** tab (NOT Google, GitLab, or ActiveState)
2. Fill in these fields:

   **PyPI Project Name (required):**
   ```
   collab-tunnel
   ```

   **Owner (required):**
   ```
   yourusername
   ```
   *(Replace with your actual GitHub username)*

   **Repository name (required):**
   ```
   collab-tunnel-python
   ```

   **Workflow name (required):**
   ```
   publish.yml
   ```

   **Environment name (optional but recommended):**
   ```
   pypi
   ```

3. Click **Add** or **Save**

### Step 4: Create a GitHub Release (This Triggers Publishing)

1. Go to your GitHub repository: `https://github.com/yourusername/collab-tunnel-python`
2. Click on **Releases** (right sidebar)
3. Click **Create a new release**
4. Click **Choose a tag**
5. Type: `v1.0.0` (creates new tag)
6. Release title: `v1.0.0 - Initial Release`
7. Description:
   ```markdown
   ## Collaboration Tunnel Protocol - Python Client v1.0.0

   First public release of the Python client library for TCT protocol.

   ### Features
   - Sitemap-first discovery and crawling
   - Zero-fetch optimization (skip 90%+ unchanged content)
   - Conditional request support (304 Not Modified)
   - ETag validation and content integrity verification
   - Bandwidth tracking and statistics
   - Protocol compliance validator

   ### Measured Results
   - 83% bandwidth savings vs HTML-only crawling
   - 86% token reduction for AI processing

   ### Installation
   ```
   pip install collab-tunnel
   ```

   ### Quick Start
   ```python
   from collab_tunnel import CollabTunnelCrawler

   crawler = CollabTunnelCrawler(user_agent="MyBot/1.0")
   sitemap = crawler.fetch_sitemap("https://example.com/llm-sitemap.json")

   for item in sitemap.items:
       if crawler.should_fetch(item):
           content = crawler.fetch_content(item['mUrl'])
           print(content['title'])
   ```

   ### Links
   - Documentation: https://llmpages.org/docs/python/
   - Protocol Spec: https://llmpages.org/spec/
   - Patent: US 63/895,763 (Patent Pending)
   ```

8. Click **Publish release**

### Step 5: Watch Automatic Publishing

1. Go to **Actions** tab in your GitHub repository
2. You'll see "Publish to PyPI" workflow running
3. Wait 2-3 minutes for it to complete
4. If successful, your package is now on PyPI!

### Step 6: Verify Publication

Check that your package is live:
```bash
# Search on PyPI
https://pypi.org/project/collab-tunnel/

# Test installation
pip install collab-tunnel

# Test import
python -c "from collab_tunnel import CollabTunnelCrawler; print('Success!')"
```

## Why GitHub Method (Not Google)?

**GitHub Trusted Publisher:**
- ✅ No API tokens to manage
- ✅ Automatic publishing on release
- ✅ Secure (uses OpenID Connect)
- ✅ Industry standard for Python packages
- ✅ Integrates with your version control
- ✅ Full audit trail

**Google OpenID Connect:**
- ❌ Requires Google service account setup
- ❌ More complex configuration
- ❌ Less commonly used in Python ecosystem
- ❌ Harder to automate
- ❌ Only needed if you're using Google Cloud Build

## If Publishing Fails

### Error: "Package does not exist"
- Make sure you completed Step 3 (Configure PyPI Trusted Publisher) BEFORE creating the release
- The trusted publisher must be configured first

### Error: "Workflow not found"
- Check that `.github/workflows/publish.yml` exists in your repository
- Make sure you pushed all files including the `.github` folder

### Error: "Permission denied"
- Go to your repository Settings > Actions > General
- Under "Workflow permissions", select "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### Error: "Build failed"
- Check the Actions tab for detailed error logs
- Most common: missing `build` package - already handled in workflow

## Manual Publishing (Backup Method)

If GitHub Actions fails, you can publish manually:

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload to PyPI (you'll need to create an API token first)
python -m twine upload dist/*
```

But **GitHub method is strongly recommended** - it's more secure and automated.

## After First Publish

For future updates:
1. Update version in `pyproject.toml` and `setup.py`
2. Commit and push changes
3. Create new GitHub release (e.g., `v1.1.0`)
4. Automatic publishing happens again!

## Summary

**What you need to do NOW:**
1. ✅ Files ready (already done)
2. ⏳ Create GitHub repository
3. ⏳ Push code to GitHub
4. ⏳ Configure PyPI Trusted Publisher (GitHub tab)
5. ⏳ Create GitHub release v1.0.0
6. ✅ Automatic publishing!

**Time needed:** 10-15 minutes

**PyPI URL after publish:** https://pypi.org/project/collab-tunnel/

Good luck! 🚀
