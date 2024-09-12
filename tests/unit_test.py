
from lemonsky.data.dashboard.controllers import (
    _Project,
    Project,
    Content,
    _Shot,
    Shot,
    Task,
    Version,
)

# TODO: handle return multiple results
# Handle empty queries
# assert filter conditions
# option to get everything by ID

# a = Content.get(project_code="TS", type="shot", name="101_01_001")
project = _Project.get(code="TS")
project = Project.get(code="TS")

shot_a = _Shot.get(
    project_code=project.code, 
    name="101_01_001"
)
shot_b = Shot.get(
    project_code=project.code, 
    name="101_01_001"
)

task = Task.get(
    project_code=project.code, 
    content_type="shot", 
    content_name=shot_a.shot_code, 
    step_code="COMP",
)
print(task)

#TODO:
version = Version.create(task=task)

version.add_files()

print(version)
# version.add_files()
# version.publish()