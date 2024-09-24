# ls-core
shared-library for pipeline TDs - Test

# Setup
python -m pip venv env
source env/Scripts/activate
env/Scripts/python -m pip install -e .
env/Scripts/python -m pip install -e .[dev]
env/Scripts/python -m pip install -e .[dev-lint]

create settings.json under `lemonsky/resources` folder, copy contents from other devs


# Prerequisites:
1. clone a copy of LemonCORE-WEB in N drive, edit local settings to point to prod DB
2. Add requirements of LemonCORE-Web into ls-core, keep them updated
3. Match dependencies between this library and Skyline
