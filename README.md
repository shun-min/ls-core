# ls-core
shared-library for pipeline TDs - Test

# Setup
python -m pip venv env
source env/Scripts/activate
env/Scripts/python -m pip install -e .
env/Scripts/python -m pip install -e .[dev]
env/Scripts/python -m pip install -e .[dev-lint]

create settings.json under `lemonsky/resources` folder, copy contents from other devs