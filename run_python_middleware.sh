#!/bin/bash


LOG=./logs/log.txt
touch $LOG

echo "--------$(date)--------" >> $LOG

echo "[INFO] $LOG file touched    $(date)" >> $LOG

echo "[INFO] pip list: $(pip list)"

echo "[INFO] running ./main.py..."
python main.py