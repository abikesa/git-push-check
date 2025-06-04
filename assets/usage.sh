# Default 100MB threshold, no output file
python prune_check.py

# Custom threshold (e.g. 30MB)
python prune_check.py --threshold 30

# Create bigfiles.txt for anything over 20MB
python prune_check.py --threshold 20 --write-bigfiles
