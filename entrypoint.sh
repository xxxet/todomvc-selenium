#!/usr/bin/env bash
pip install -r requirements.txt -U
pytest --browser=chrome -n 2 --alluredir=./allure-results --remote_driver='http://127.0.0.1:4444/wd/hub'