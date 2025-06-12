#!/bin/bash
echo "Running Django collectstatic..."
python manage.py collectstatic --noinput --clear
echo "collectstatic finished."
chmod +x build_files.sh