#!/usr/bin/env bash
pip install -r requirements.txt -U
pytest --browser=chrome -n 2 --alluredir=$1 --remote_driver='http://selenium-hub:4444/wd/hub'