#!/bin/bash

scriptDir=$(dirname $0)
rootDir="${scriptDir}/../"

start() {
    consul-template -consul-addr ${CONSUL_SERVER_ADDR}:8500 \
                    -template "${rootDir}/consul/config.tpl:${rootDir}/housingprice/myconfig.ini" \
                    -exec "python3 ${rootDir}/manage.py runserver 0.0.0.0:8000"
}

start
