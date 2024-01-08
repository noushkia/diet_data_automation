from cx_Freeze import setup, Executable

# Specify the list of files that need to be included
include_files = []

# Specify the list of packages to include
packages = []

# Create the executable
executable = Executable(
    script='main.py',  # Replace with the name of your script
    base='Win32GUI',  # Use 'Win32GUI' for a GUI application or 'Win32Console' for a console application
    target_name='main.exe',  # Name of the output executable
    icon="icon.ico"  # Path to the icon file (optional)
)

# Setup script configuration
setup(
    name='Expert Diet',
    version='1.0',
    description='Automation of form filling for dietitian patients',
    options={
        'build_exe': {
            'include_files': include_files,
            'packages': packages,
            'optimize': 2
        }
    },
    executables=[executable]
)
