# Repository Cleanup Instructions - Option 2

⚠️ **WARNING: THIS IS A DESTRUCTIVE OPERATION** ⚠️
This will permanently remove files from git history and cannot be undone.

## What This Will Do

✅ **Keep (Public)**:
- `nuc_rag/` folder and all Python source code
- `README.md`, `LICENSE`, etc.
- Essential documentation

❌ **Remove (Private/Sensitive)**:
- `PUB2058_web_gsg_18.pdf` (nuclear safety document)
- All `.hdf5` files (databases)
- All `.csv` and `.xlsx` files (data outputs)
- `cline_docs/` folder (private documentation)
- Development files (`custom_embed.py`, etc.)

## Step-by-Step Process

### Phase 1: Remove Files from Working Directory

```bash
cd /Volumes/coder/rag/rag_nuclear_safety

# Remove sensitive files (they'll be ignored in future)
rm PUB2058_web_gsg_18.pdf
rm *.hdf5
rm *.csv
rm *.xlsx
rm custom_embed.py
rm docker-compose.txt
rm dockerfile.txt
rm github-workflow-*.txt
rm gitignore.txt
rm requirements-txt.txt
rm -rf __pycache__
rm -rf cline_docs
```

### Phase 2: Add .gitignore and Commit

```bash
# Add the new .gitignore
git add .gitignore requirements.txt

# Commit the cleanup
git commit -m "Add comprehensive .gitignore and cleanup repository

- Remove sensitive nuclear safety documents
- Remove development data files
- Remove private documentation
- Keep only essential package files for public use"
```

### Phase 3: Remove Files from Git History (DESTRUCTIVE)

⚠️ **BACKUP FIRST**: Make a complete backup of your repository before proceeding!

```bash
# Create backup
cp -r /Volumes/coder/rag/rag_nuclear_safety /Volumes/coder/rag/rag_nuclear_safety_BACKUP

# Remove sensitive files from ALL git history
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch \
PUB2058_web_gsg_18.pdf \
*.hdf5 \
*.csv \
*.xlsx \
custom_embed.py \
docker-compose.txt \
dockerfile.txt \
github-workflow-ci.txt \
github-workflow-deploy.txt \
gitignore.txt \
requirements-txt.txt \
cline_docs/* \
__pycache__/*' \
--prune-empty --tag-name-filter cat -- --all
```

### Phase 4: Clean Up and Force Push

```bash
# Clean up repository
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push to GitHub (DESTRUCTIVE - updates remote history)
git push --force-with-lease origin main
```

## Alternative: Use git-filter-repo (Recommended if available)

If you have `git-filter-repo` installed (safer than filter-branch):

```bash
# Install git-filter-repo if needed
# pip install git-filter-repo

# Remove sensitive files from history
git filter-repo --path PUB2058_web_gsg_18.pdf --invert-paths
git filter-repo --path-glob '*.hdf5' --invert-paths
git filter-repo --path-glob '*.csv' --invert-paths
git filter-repo --path-glob '*.xlsx' --invert-paths
git filter-repo --path custom_embed.py --invert-paths
git filter-repo --path-glob 'cline_docs/*' --invert-paths
git filter-repo --path-glob '__pycache__/*' --invert-paths

# Force push
git push --force-with-lease origin main
```

## Verification

After cleanup, verify the repository only contains:
- `nuc_rag/` folder with Python package
- `README.md`, `LICENSE`
- `.gitignore`, `requirements.txt`
- No sensitive files in `git log --name-only --all`

## Result

Your repository will be clean and public-ready while maintaining the same URL!
