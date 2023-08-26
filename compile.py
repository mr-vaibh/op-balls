import os
import shutil
import py_compile

# Create the build directory
build_dir = os.path.join(os.getcwd(), 'build')
os.makedirs(build_dir, exist_ok=True)

# Compile .py files to .pyc in the build directory
for root, _, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.py'):
            source_file = os.path.join(root, file)
            compiled_file = source_file + 'c'
            relative_path = os.path.relpath(compiled_file, os.getcwd())
            target_file = os.path.join(build_dir, relative_path)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            py_compile.compile(source_file, cfile=target_file, optimize=-1)

# Copy asset files/folders if provided
assets = ['config.txt', 'requirements.txt', 'asset_folder']
for asset in assets:
    source_path = os.path.join(os.getcwd(), asset)
    target_path = os.path.join(build_dir, asset)
    if os.path.exists(source_path):
        if os.path.isfile(source_path):
            shutil.copy(source_path, target_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, target_path)

# Create the batch script
install_script_path = os.path.join(build_dir, 'INSTALL.bat')
launch_script_path = os.path.join(build_dir, 'START.bat')

with open(install_script_path, 'w') as install_script:
    install_script.write('''@echo off
@REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed.
) else (
    echo Python is not installed. Downloading...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
    echo Python is downloaded. Installing...
    python_installer.exe /quiet PrependPath=1
    del python_installer.exe
    echo Python installation complete.
)

pause
''')
with open(launch_script_path, 'w') as launch_script:
    launch_script.write('''@echo off
@REM Installing dependecies
pip install -r requirements.txt
echo All dependent packages installed
cls

@REM Run the Python script
python main2.pyc
''')

print("Build process completed. You can find the build files in the 'build' directory.")
