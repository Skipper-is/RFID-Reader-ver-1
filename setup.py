from cx_Freeze import setup, Executable

base = None


executables = [Executable("RFID.py", base=base)]

packages = ["serial"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "RFID App",
    options = options,
    version = "1.0",
    description = 'Version 1.0 RFID app',
    executables = executables
)