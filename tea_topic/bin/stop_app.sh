#!/usr/bin/bash
ps aux|grep uwsgi.ini|grep -v grep|awk -F ' ' '{print $2}'|xargs -i kill -9 {}
