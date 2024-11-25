#!bin/sh

pip install --no-cache-dir -r /root/app/requirements.txt
exec "$@"
