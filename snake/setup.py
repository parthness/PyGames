import cx_Freeze

executables=[cx_Freeze.Executable("mygame.py")]

cx_Freeze.setup(
    name="Snake",
    options={"build_exe":{"packages":["pygame"],"include_files":["apple.png","snakehead.png"] }},
    description="Snake Game",
    executables=executables
)