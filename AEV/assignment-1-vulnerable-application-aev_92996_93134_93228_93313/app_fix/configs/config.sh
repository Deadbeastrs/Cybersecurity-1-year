service mysql stop && usermod -d /var/lib/mysql/ mysql && service mysql start
service apache2 restart
mysql < /ws/create_db.sql
mysql rkown < /ws/source_code/sql/onlinestore.sql
cd /ws && mysql < secure_mysql.sql
useradd jovemguilhas
echo "jovemguilhas:Natureza1"| chpasswd
#echo "Defaults env_keep += \"ftp_proxy http_proxy https_proxy no_proxy\"
#jovemguilhas ALL=(root) NOPASSWD: /bin/apt update, /bin/apt upgrade" >> /etc/sudoers
#echo "deb [trusted=yes] http://packages.aev/aev ascii main" >> /etc/apt/sources.list
chown -R jovemguilhas:jovemguilhas /home/jovemguilhas
#chown root:www-data /home/jovemguilhas/personalProgram
chmod 755 /home/jovemguilhas/personalProgram
#chmod u+s /home/jovemguilhas/personalProgram
chown -R www-data:www-data /ws/source_code/uploads

#chown root:root /home/jovemguilhas/auto_backup.sh //Wrong
chown jovemguilhas:jovemguilhas /home/jovemguilhas/auto_backup.sh # Correct

chmod 744 /home/jovemguilhas/auto_backup.sh

touch /var/spool/cron/crontabs/root
echo "*/1 * * * * /home/jovemguilhas/auto_backup.sh" >> /var/spool/cron/crontabs/root
chmod 600 /var/spool/cron/crontabs/root
chown root:crontab /var/spool/cron/crontabs/root

mkdir /home/jovemguilhas/.ssh
chown jovemguilhas:jovemguilhas /home/jovemguilhas/.ssh
chmod 700 /home/jovemguilhas/.ssh

#Secure files
chmod 700 /ws/create_db.sql
chmod 700 /ws/secure_mysql.sql
chmod 700 /ws/config.sh
chmod 700 /autostart.sh
