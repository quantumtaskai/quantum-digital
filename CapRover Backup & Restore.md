# **🟢 CapRover Backup & Restore — Step by Step (Clear)**

### **Step 1: Create backup folder**

`sudo mkdir -p /opt/caprover-backup`  
`sudo chown $USER:$USER /opt/caprover-backup`  
`cd /opt/caprover-backup`

✅ This folder stores your backups locally.

---

### **Step 2: Install rclone & connect Google Drive**

`curl https://rclone.org/install.sh | sudo bash`  
`rclone config`

* `n` → new remote

* Name it: `gdrive`

* Storage type → `drive` (Google Drive)

* Auth in browser → paste code back

* Test:

`rclone ls gdrive:`

✅ Should list your Drive files.

---

### **Step 3: Create backup script**

`nano /opt/caprover-backup/backup.sh`

Paste this:

`#!/bin/bash`  
`DATE=$(date +%F_%H-%M-%S)`  
`BACKUP_DIR="/opt/caprover-backup/$DATE"`  
`mkdir -p $BACKUP_DIR`

`# Backup CapRover config`  
`docker run --rm -v /captain:/captain alpine \`  
  `tar -czf - -C /captain . > $BACKUP_DIR/caprover-config.tar.gz`

`# Backup all Docker volumes`  
`for volume in $(docker volume ls -q); do`  
  `docker run --rm -v ${volume}:/volume -v $BACKUP_DIR:/backup alpine \`  
    `tar -czf /backup/${volume}.tar.gz -C /volume .`  
`done`

`# Keep only last 7 backups`  
`ls -dt /opt/caprover-backup/*/ | tail -n +8 | xargs rm -rf`

`# Upload to Google Drive`  
`rclone copy $BACKUP_DIR gdrive:caprover-backups/$DATE`

Make executable:

`chmod +x /opt/caprover-backup/backup.sh`

---

### **Step 4: Test backup manually**

`/opt/caprover-backup/backup.sh`

* Check Google Drive → folder `caprover-backups/<DATE>` appears

* Local folder `/opt/caprover-backup/<DATE>` contains tar.gz files

✅ Manual backup works.

---

### **Step 5: Automate daily backups**

`crontab -e`

Add line:

`0 2 * * * /opt/caprover-backup/backup.sh >> /opt/caprover-backup/backup.log 2>&1`

* Runs every day at 2 AM automatically

---

### **Step 6: Restore (step by step, no magic)**

1. Spin up new VPS → install Docker \+ CapRover \+ rclone

2. Pull backup from Google Drive (if not local):

`rclone copy gdrive:caprover-backups/2025-09-03_09-58-08 /opt/caprover-backup/restore`

3. Restore CapRover config:

`docker run --rm -v /captain:/captain -v /opt/caprover-backup/restore:/backup alpine \`  
  `sh -c "cd /captain && tar -xzf /backup/caprover-config.tar.gz --strip 1"`

4. Restore all volumes:

`for file in /opt/caprover-backup/restore/*.tar.gz; do`  
    `volume=$(basename $file .tar.gz)`  
    `[ "$volume" != "caprover-config" ] || continue`  
    `docker volume create $volume`  
    `docker run --rm -v ${volume}:/volume -v /opt/caprover-backup/restore:/backup alpine \`  
      `sh -c "cd /volume && tar -xzf /backup/${volume}.tar.gz"`  
`done`

✅ Apps and data restored.
