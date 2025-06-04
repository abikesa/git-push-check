 
cd repo
python prune_check.py
brew install git-filter-repo
git filter-repo --invert-paths --path-glob "*.mp4"
