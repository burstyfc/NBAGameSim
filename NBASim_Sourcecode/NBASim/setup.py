import cx_Freeze

executables = [cx_Freeze.Executable('NBASim.py')]

cx_Freeze.setup(
    name='NBA Simulator',
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["ball.png", "court.png", "Swish.wav", "rim.wav"]}},
    executables=executables

)