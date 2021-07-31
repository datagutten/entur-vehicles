#!/usr/bin/sh
git pull
python3 vehicle_info/manage.py collectstatic
/etc/init.d/apache2 restart