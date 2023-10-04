#!/bin/bash

cd ./front_service || exit
python -m venv venv
pip install -r requirements.txt

cd ..
cd ./inner_service || exit
python -m venv venv
pip install -r requirements.txt

echo "///////////////////////////////////////////////"
echo "// Virtual Environments are been installed   //"
echo "///////////////////////////////////////////////"