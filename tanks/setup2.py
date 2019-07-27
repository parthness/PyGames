__author__ = 'Parth'
import cx_Freeze

executables=[cx_Freeze.Executable("tanks.py")]

cx_Freeze.setup(
    name="Just for Nishu",
    options={"build_exe":{"packages":["pygame"],"include_files":["boom.wav"] }},
    description="Tanks Game",
    executables=executables
)