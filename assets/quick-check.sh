git lfs track
du -sh *
git rev-list --objects --all | sort -k 2 > allfiles.txt
