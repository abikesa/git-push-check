import os
import humanize
import shutil

MAX_SIZE_BYTES = 1.5 * (1024**3)  # 1.5 GB

# Directories to delete (common junk)
ARTIFACT_DIRS = ['_build', '__pycache__', '.ipynb_checkpoints']
GITIGNORE_SUGGEST = ['*.mp4', '*.zip', '*.pptx', '*.pdf', '_build/', '__pycache__/', '.ipynb_checkpoints/']


def get_dir_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)
            except:
                pass
    return total

def find_large_files(root, limit=100*1024*1024):  # 100MB+
    large_files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            try:
                full_path = os.path.join(dirpath, f)
                size = os.path.getsize(full_path)
                if size > limit:
                    large_files.append((size, full_path))
            except:
                pass
    return sorted(large_files, reverse=True)

def top_folders_by_size(root, top_n=15):
    folder_sizes = []
    for dirpath, dirnames, filenames in os.walk(root):
        size = get_dir_size(dirpath)
        if size > 100*1024*1024:  # Only show big folders
            folder_sizes.append((size, dirpath))
    return sorted(folder_sizes, reverse=True)[:top_n]

def delete_artifact_dirs(root):
    print("\n🧹 Deleting known artifact directories...")
    for dirpath, dirnames, filenames in os.walk(root):
        for d in ARTIFACT_DIRS:
            full = os.path.join(dirpath, d)
            if os.path.exists(full):
                print(f"   🔥 Removing: {full}")
                try:
                    shutil.rmtree(full)
                except Exception as e:
                    print(f"   ❌ Could not delete {full}: {e}")

def suggest_gitignore():
    print("\n✍️ Suggested additions to your .gitignore:")
    for entry in GITIGNORE_SUGGEST:
        print(f"   {entry}")

def main():
    print("📦 Auditing repo size...\n")
    total_size = get_dir_size(".")
    print(f"📏 Total repo size: {humanize.naturalsize(total_size)}")

    print("\n📁 Top folders by size:")
    for size, path in top_folders_by_size("."):
        print(f"  {humanize.naturalsize(size):>10} — {path}")

    print("\n🧱 Large individual files:")
    for size, path in find_large_files("."):
        print(f"  {humanize.naturalsize(size):>10} — {path}")

    if total_size > MAX_SIZE_BYTES:
        print("\n🚨 Repo is over 1.5GB — consider pruning or using Git LFS for large binaries.")
        delete_artifact_dirs(".")
        suggest_gitignore()

if __name__ == "__main__":
    main()
