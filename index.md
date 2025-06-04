
## 🔍 `prune_check.py`: Smart Pre-Git Push Repo Size Audit

This script:

* Walks the directory tree.
* Ignores `.git`, `venv`, `__pycache__`, and `_build`.
* Tracks total size.
* Identifies top offenders (>50MB or top N by weight).
* Offers interactive pruning guidance (optional).

```python
import os
from pathlib import Path
import humanize
from collections import defaultdict

# Thresholds
SIZE_THRESHOLD_MB = 50  # flag files larger than 50MB
TOP_N_LARGEST = 15       # number of largest files to show

# Directories to ignore
IGNORE_DIRS = {'.git', '__pycache__', 'venv', '_build'}

def get_file_sizes(start_path='.'):
    large_files = []
    folder_sizes = defaultdict(int)
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(start_path):
        # Skip ignored dirs
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(fp)
            except OSError:
                continue  # skip broken symlinks or permission errors

            total_size += size
            folder_sizes[dirpath] += size
            if size > SIZE_THRESHOLD_MB * 1024 * 1024:
                large_files.append((fp, size))

    return total_size, folder_sizes, sorted(large_files, key=lambda x: x[1], reverse=True)

def main():
    print("📦 Auditing repo size...")

    total_size, folder_sizes, large_files = get_file_sizes()

    print(f"\n📏 Total repo size: {humanize.naturalsize(total_size)}")

    # Top heavy folders
    sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)[:TOP_N_LARGEST]
    print("\n📁 Top folders by size:")
    for path, size in sorted_folders:
        print(f"  {humanize.naturalsize(size):>10} — {path}")

    # Top large files
    print("\n🧱 Large individual files:")
    for path, size in large_files[:TOP_N_LARGEST]:
        print(f"  {humanize.naturalsize(size):>10} — {path}")

    if total_size > 1.5 * 1024**3:
        print("\n🚨 Repo is over 1.5GB — consider pruning or using Git LFS for large binaries.")

    # Suggested deletions
    print("\n🗑️ Suggested deletions (build artifacts, notebook outputs):")
    for path, size in large_files:
        if any(sub in path for sub in ['_build', 'jupyter_execute']) or path.endswith(('.png', '.ipynb')):
            print(f"  {humanize.naturalsize(size):>10} — {path}")

if __name__ == '__main__':
    main()
```

---

## 🧠 Opinionated Guidance

Your biggest offenders:

* `ukb/dolce/_build/` → **Always delete before commit.** Auto-regenerated.
* `*.ipynb`, especially from `jupyter_execute/` → Should **not** be committed unless manually edited.
* `*.png` (output cells) → **Use Git LFS or `.gitignore`**.

---

## 🧼 Next Steps (Highly Recommended)

1. Add this to your `.gitignore`:

```gitignore
_build/
jupyter_execute/
*.ipynb_checkpoints
*.png
```

2. Add a `prepush.sh` with:

```bash
#!/bin/bash
python prune_check.py
read -p "Continue with git push? (y/N): " yn
if [[ "$yn" =~ ^[Yy]$ ]]; then
    git push "$@"
fi
```

Then alias `git-push-safe` to that.

