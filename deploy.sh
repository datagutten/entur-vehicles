#!/usr/bin/sh
git pull
python3 manage.py collectstatic
/etc/init.d/apache2 restart