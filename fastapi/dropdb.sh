#!/bin/bash

killall -9 Python

psql -U stefan template1 -c 'drop database if exists adr;' -c 'create database adr;'

./start.sh

sleep 1

curl -X POST http://localhost:8000/init 
 