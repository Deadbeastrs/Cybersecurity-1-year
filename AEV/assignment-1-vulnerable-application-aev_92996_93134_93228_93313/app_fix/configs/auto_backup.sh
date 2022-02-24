#!/bin/bash
/bin/tar -zcvf /ws/source_code/backup/backup.tar.gz /ws/source_code
/bin/rsync -avz --no-perms --chown=jovemguilhas:jovemguilhas /ws/source_code/backup/ /home/jovemguilhas/backup # fix by going to backup folder

/bin/rm /ws/source_code/backup/backup.tar.gz
/bin/rm /home/jovemguilhas/backup/index.php
