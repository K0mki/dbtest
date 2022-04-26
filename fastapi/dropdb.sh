#!/bin/bash
psql -U stefan template1 -c 'drop database if exists adr;' -c 'create database adr;'
