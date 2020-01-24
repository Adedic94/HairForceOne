#!/bin/bash
cd /home/pi/encoder

if git pull | grep "Already up-to-date."; then
	echo "Checked for new versions, nothing to change at $(date)" >> ~/hfo_logfile.log
else
	echo "New files have been checked in; upgrading the environment at $(date)" >> ~/hfo_logfile.log
        pkill -f flask
        . venv/bin/activate
        export FLASK_APP=hf1
        export FLASK_ENV=development
        export APP_VERSION=$(git rev-parse --short HEAD)
        flask init-db
        flask fill-db
	echo "Starting the website at $(hostname -I) on port 5000 at $(date)" >> ~/hfo_logfile.log
        nohup flask run -h 0.0.0.0 -p 5000 &
	sleep 10
fi
