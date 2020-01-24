#!/bin/bash
cd /home/pi/encoder
python3 -m venv venv
. venv/bin/activate
cd /home/pi/encoder

echo "(Re)starting application by command at $(date)" >> ~/hfo_logfile.log
pkill -f flask
. venv/bin/activate
export FLASK_APP=hf1
export FLASK_ENV=development
export APP_VERSION=$(git rev-parse --short HEAD)
flask init-db
flask fill-db
echo "Starting the website at $(hostname -I) on port 8080 at $(date)" >> ~/hfo_$
nohup flask run -h 0.0.0.0 -p 8080 &



