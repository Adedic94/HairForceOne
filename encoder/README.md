# Install the virtual environment and start the application

Execute the following instructions in the folder where this README.md resides.

# Instructions for Mac and Linux

## Create the virtual environment

`python3 -m venv venv`

## Activate the virtual environment

`. venv/bin/activate`
voor mac:
`source venv/bin/activate`
voor linux:
`. venv/bin/activate`

## Install the requirements and the HFO module

If there is no PIP on your system, install it using the instructions here:
https://packaging.python.org/tutorials/installing-packages/

`pip install -e .`

Now run the HFO Flask application:

```
export FLASK_APP=hf1
export FLASK_ENV=development
flask run
```

## Available commands while starting Flask

Create the database:
`flask init-db`

Recreate the database and fill with some demo data:
`flask fill-db`

# Instructions for Windows PowerShell

## Create the virtual environment

`python3 -m venv venv`

## Activate the virtual environment

`.\venv\Scripts\activate.bat`

## Install the requirements and the HFO module

If there is no PIP on your system, install it using the instructions here:
https://packaging.python.org/tutorials/installing-packages/

`pip install -e .`

Now run the HFO Flask application:

```
$env:FLASK_APP="hf1"
$env:FLASK_ENV="development"
python -m flask run
```

## Available commands while starting Flask

Create the database:
`python -m flask init-db`

Recreate the database and fill with some demo data:
`python -m flask fill-db`

## Rounding up

The app can be configure using an config.cfg file in the instance directory.

```python
APP_VERSION='0.1poc'
SECRET_KEY='my_secret'
```

## Instruction on how to use VS Code

- Install Visual Studio Code https://code.visualstudio.com/Download
- Install the pyhton extension: Python
- Select the Python venv (bottom left task bar)
- Select the debug icon (left task bar)
- Select the debug settings (right to the green play button)
- Select Python->Flask->hf1 and a the flask config is added

VS Code can now debug your flask web application.
