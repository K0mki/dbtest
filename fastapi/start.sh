#!/bin/bash

uvicorn main:app --reload

sleep 5

curl -X POST http://localhost:8000/

sleep 5
