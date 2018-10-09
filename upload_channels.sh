#!/usr/bin/env bash
export PYTHONPATH=/var/www/html/DataBunkerApp
export MONGODB_URI=mongodb://heroku_bd48jtkh:d51bt9lfikmakpvvvnpqd35omk@ds243501.mlab.com:43501/heroku_bd48jtkh
/var/www/html/DataBunkerApp/venv/bin/python /var/www/html/DataBunkerApp/app/upload_channels.py
