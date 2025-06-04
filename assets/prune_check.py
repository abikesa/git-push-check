import os
import argparse
import humanize
import shutil

MAX_SIZE_BYTES = 1.5 * (1024**3)  # 1.5 GB
ARTIFACT_DIRS = ['_build', '__pycache__', '.ipynb_checkpoints']
GITIGNORE_SUGGEST = ['*.mp4', '*.zip', '*.pptx', '*.pdf', '_build/', '__pycache__/', '.ipynb_checkpoints/']

def get_dir_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except:
                pass
    return total

def find_large_files(root, limit):
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

def top_folders_by_size(root, top_n=15, limit=100*1024*1024):
    folder_sizes = []
    for dirpath, _, _ in os.walk(root):
        size = get_dir_size(dirpath)
        if size > limit:
            folder_sizes.append((size, dirpath))
    return sorted(folder_sizes, reverse=True)[:top_n]

def delete_artifact_dirs(root):
    print("\n🧹 Deleting known artifact directories...")
    for dirpath, _, _ in os.walk(root):
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

def write_bigfiles_file(large_files, output_path="bigfiles.txt"):
    with open(output_path, "w") as f:
        for size, path in large_files:
            f.write(f"{humanize.naturalsize(size)}\t{path}\n")
    print(f"\n📝 Wrote {len(large_files)} large files to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Audit large files and repo size.")
    parser.add_argument("--threshold", type=int, default=100, help="File size threshold in MB (default: 100MB)")
    parser.add_argument("--write-bigfiles", action="store_true", help="Write large file list to bigfiles.txt")
    args = parser.parse_args()

    byte_threshold = args.threshold * 1024 * 1024

    print("📦 Auditing repo size...\n")
    total_size = get_dir_size(".")
    print(f"📏 Total repo size: {humanize.naturalsize(total_size)}")

    print("\n📁 Top folders by size:")
    for size, path in top_folders_by_size(".", limit=byte_threshold):
        print(f"  {humanize.naturalsize(size):>10} — {path}")

    print("\n🧱 Large individual files:")
    large_files = find_large_files(".", byte_threshold)
    for size, path in large_files:
        print(f"  {humanize.naturalsize(size):>10} — {path}")

    if args.write_bigfiles:
        write_bigfiles_file(large_files)

    if total_size > MAX_SIZE_BYTES:
        print(f"\n🚨 Repo is over {humanize.naturalsize(MAX_SIZE_BYTES)} — consider pruning or using Git LFS.")
        delete_artifact_dirs(".")
        suggest_gitignore()

if __name__ == "__main__":
    main()
