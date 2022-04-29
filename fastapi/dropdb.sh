#!/bin/bash

killall -9 python

psql -U stefan template1 -c 'drop database if exists adr;' -c 'create database adr;'

uvicorn main:app --reload

sleep 1

curl -X POST http://localhost:8000/init 
 