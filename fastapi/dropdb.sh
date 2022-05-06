#!/bin/bash

killall -9 python3

psql -U stefan template1 -c 'drop database if exists adr;' -c 'create database adr;'


