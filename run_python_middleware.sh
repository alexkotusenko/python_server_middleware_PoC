#!/bin/bash


LOG=./logs/log.txt
touch $LOG

echo "--------$(date)--------" >> $LOG

echo "[INFO] $LOG file touched    $(date)" >> $LOG