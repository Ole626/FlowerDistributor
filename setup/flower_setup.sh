#!/bin/bash

sudo rm /usr/bin/python
sudo ln -s /usr/local/bin/python3.11 /usr/bin/python
sudo rm /user/lib/python3.11/EXTERNALLY-MANAGED

git clone -b updates https://github.com/Ole626/FlowerDistributor.git
pip install -r FlowerDistributor/requirements.txt
chmod +x FlowerDistributor/src/main.py
sudo nano /etc/systemd/system/flower_dist.service
sudo systemctl enable flower_dist.service
nano FlowerDistributor/conf.json
