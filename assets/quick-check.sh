python3 <(curl -s https://raw.githubusercontent.com/abikesa/git-push-check/refs/heads/main/assets/prune_check.py)  
git lfs track
du -sh *
git rev-list --objects --all | sort -k 2 > allfiles.txt
