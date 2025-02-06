#!/bin/bash


LOG=/app/logs/log.txt
touch $LOG

echo "--------$(date)--------" >> $LOG

echo "[INFO] $LOG file touched    $(date)" >> $LOG

echo "[INFO] running pip install flask"
pip install flask requests

echo "[INFO] pip list: $(pip list)"

echo "[INFO] running ./main.py..."
python /app/main.py