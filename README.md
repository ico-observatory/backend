# Internet Centralization Observatory - Backend

![ICO](ico/static/images/logo.png "Internet Centralization Observatory")

This project contains the backend code for the Internet Centralization Observatory web application.
Internet Centralization Observatory Backend is develeped using Django and Django Rest Framework.

The Frontend project can be found [here](https://github.com/ComputerNetworks-UFRGS/ICO-frontend).

## Development environment setup
To setup your development environment, please follow the steps below.

1. Install [Git](https://git-scm.com/).
2. Install [VS Code](https://code.visualstudio.com/).
3. Install Python3, Pip3 and Pipenv.
    * `sudo apt-get install python3.6 python3-pip python3.6-dev libmysqlclient-dev`
    * `sudo pip install pipenv autopep8`
4. Clone this repo.
    * `git clone https://github.com/ComputerNetworks-UFRGS/ICO-backend.git`
5. Inside the repository directory, run the following commands.
    * `pipenv install --dev`
    * `pipenv shell`
6. Install the required Atom packages.
    * `apm install --packages-file atom-packages.txt`
7. Configure Atom-Beautify package.
    * Edit > Preferences > Packages > atom-beautify > Python.
    * Check 'Beautify On Save'.
8. Configure linter-pylint package.
    * Change 'pylint' the path to the virtual environment.
    * /home/`<user>`/.local/share/virtualenvs/ico-backend-`<venvid>`/bin/pylint
8. To verify the installation, open Atom and check for linter errors.

## Running the application locally
Run the application, inside the Pipenv environment, with the following commands.
 * `cd ./ICO-backend/ico/`
 * `python manage.py runserver --settings=ico.settings.development`

 <!-- ALL-CONTRIBUTORS-LIST: START - Do not remove or modify this section -->
 <!-- ALL-CONTRIBUTORS-LIST:END -->

## Contributing
Before starting a new implementation, check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this repository.

Note: package.json is used for Pull Request changelog.

## Commands
Build local db
```
python manage.py loaddata db.json --settings=ico.settings.local
```
