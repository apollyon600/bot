#!/bin/bash
cp -n -R /app/. /data/ 2>/dev/null
cd /data
python run.py
