#!/bin/bash

wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz

sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev git unzip
mkdir repos

tar -xzvf Python-3.11.4.tgz 
cd Python-3.11.4/
./configure --enable-optimizations
sudo make altinstall
