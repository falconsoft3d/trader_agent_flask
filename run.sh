#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=development
# Ensure dependencies are installed just in case
pip install -r requirements.txt
python3.10 app.py
