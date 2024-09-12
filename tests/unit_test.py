from lemonsky.data.dashboard.controllers import (
    Project,
    Content,
    Shot,
    Task,
    Version,
)

# a = Content.get(project_code="TS", type="shot", name="101_01_001")
project = Project.get(code="TS")
shot_a = Shot.get(
    project_code=project.code, 
    name="101_01_001"
)
task = Task.get(
    project_code=project.code, 
    content_type="shot", 
    content_name=shot_a.shot_code, 
    step_code="COMP"
)

print(shot_a)
print(task)

#TODO:
# version = task.create_version()
# version.add_files()
# version.publish()