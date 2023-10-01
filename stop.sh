#!/bin/bash

TO_KILL=()
PID_LIST=()

PROCESSES=$(ps)

PID_REGEX="^[0-9]{2,9}$"
UVICORN_REGEX="^uvicorn$"

for value in $PROCESSES; do
  if [[ $value =~ $PID_REGEX ]]; then
    # echo "PID Detected"
    PID_LIST=("$value" "${PID_LIST[@]}")
    # echo "$PID_LIST"
  elif [[ $value =~ $UVICORN_REGEX ]]; then
    # echo "Uvicorn Detected"
    TO_KILL+=("${PID_LIST[0]}")
  else
    continue
  fi
done

for proccess in "${TO_KILL[@]}"; do
  kill "$proccess"
done

echo ""
echo "    ****Stopping all process****"
echo ""
echo "////////////////////////////////////////////"
echo "//      After this, press CTRL + C        //"
echo "////////////////////////////////////////////"