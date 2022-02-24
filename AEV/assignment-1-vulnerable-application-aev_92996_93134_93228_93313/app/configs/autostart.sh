#!/bin/bash
chmod 773 /ws/source_code/backup
chown -R www-data:www-data /ws/source_code/uploads
service apache2 start
service mysql start
service cron start
service ssh start
/bin/bash
