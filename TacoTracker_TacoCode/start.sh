#!/bin/bash

procs=$(cat /proc/cpuinfo |grep processor | wc -l)
sed -i -e "s/worker_processes 5/worker_processes $procs/" /etc/nginx/nginx.conf

/usr/bin/supervisord -n -c /etc/supervisord.conf
