:: ################# REQUIREMENTS ###################

:: Virtual environment with all packages defined in Pipfile.lock must be installed before executing this script

:: ##################################################

@echo OFF

call ".venv\Scripts\activate.bat"

server.py
