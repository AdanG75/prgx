#!/bin/bash

cd ./front_service || exit
source ./venv/bin/activate
uvicorn main:app --reload &

cd ..
cd ./inner_service || exit
source ./venv/bin/activate
uvicorn main:app --reload --port=9856 &

cd ..

echo "////////////////////////////////////////////"
echo "//      After this, press CTRL + C        //"
echo "////////////////////////////////////////////"