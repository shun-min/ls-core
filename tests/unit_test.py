
# from lemonsky.data.dashboard.controllers import (
#     # _Project,
#     Project,
#     Content,
#     # _Shot,
#     Shot,
#     Task,
#     Version,
#     File,
# )

# # TODO: handle return multiple results
# # Handle empty queries
# # assert filter conditions
# # option to get everything by ID

# # a = Content.get(project_code="TS", type="shot", name="101_01_001")
# # project = _Project.get(code="TS")
# project = Project.get(code="TS")

# # shot_a = _Shot.get(
# #     project_code=project.code,
# #     name="101_01_001",
# # )
# shot_b = Shot.get(
#     project_code=project.code,
#     name="101_01_001",
# )

# task = Task.get(
#     project_code=project.code,
#     content_type="shot",
#     content_name=shot_b.name,
#     step_code="COMP",
# )
# print(task)

# # version = Version.create(client_version=2, task=task)
# version = Version.get(task=task, internal_version=2)[0]
# print(version)

# # file1 = File.create(
# #     version_id=68,
# #     version_type="publish",
# #     keys = ["texture", "bg"],
# #     name=r"L:\Temp\TechTeam\TS_PROJ\LEMONCORE\TS_PROJ\animation\season01\101\01\001\COMP\renderOutput\Background\TS_101_01_001_Background_0298.exr",
# #     start_frame=298,
# #     end_frame=298,
# # )
# # file2 = File.create(
# #     version_id=68,
# #     version_type="publish",
# #     keys = ["camera"],
# #     name=r"L:\Temp\TechTeam\TS_PROJ\LEMONCORE\TS_PROJ\animation\season01\101\01\001\COMP\associatedFiles\mayaCamera.abc",
# # )

# # file1 = File.create(
# #     keys = ["texture", "bg"],
# #      =r"L:\Temp\TechTeam\TS_PROJ\LEMONCORE\TS_PROJ\animation\season01\101\01\001\COMP\renderOutput\Background\TS_101_01_001_Background_0298.exr",
# #     start_frame=298,
# #     end_frame=298,
# # )

# success = version.add_file(
#     keys = ["texture", "background"],
#     setting_keyword="camera",
#     name=r"TS_101_01_001_Background_0298.exr",
#     start_frame=298,
#     end_frame=298,
# )
# print(version, success)

# f = version.get_files(keys=["texture", "background"])
# print(f)
# # version.publish()


from studio.data.pipeline.controllers import Content
contents = Content.get_all(
    type="asset",
    project_code="TS",
    category="Asset",
)


from studio.data.pipeline.controllers import Project, Shot, Task, Version, File
projects = Project.get_assigned(lsid="ls0915")

p = Project.get(code="TS")
s = Shot.get(project_code=p.code, name="101_01_001")
t = Task.get(
    project_code=p.code,
    content_type="shot",
    content_name=s.name,
    step_code="COMP",
)[0]

#version = Version.create(client_version=2, task=t)
version = Version.get(task=t, internal_version=1)

v: Version = version[0]
files = v.get_files(tags=["texture", "background"])