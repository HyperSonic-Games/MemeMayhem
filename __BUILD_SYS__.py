import PyInstaller.__main__
import os
import platform
import shutil

OUTPUT_DIR = "output"

def BuildClient():
    PyInstaller.__main__.run([
        '--onefile',
        '--windowed',
        '--distpath', OUTPUT_DIR,
        'Client.py'
    ])

def BuildServer():
    PyInstaller.__main__.run([
        '--onefile',
        '--distpath', OUTPUT_DIR,
        'Server.py'
    ])

def BuildMain():
    PyInstaller.__main__.run([
        '--onefile',
        '--windowed',
        '--distpath', OUTPUT_DIR,
        'Main.py'
    ])

def CopyFiles():
    """ Copies necessary files to the output directory. """

    if platform.system() == 'Windows':
        shutil.copy("SETTINGS.toml", OUTPUT_DIR)
        shutil.copytree("Assets", os.path.join(OUTPUT_DIR, "Assets"), dirs_exist_ok=True)

# Build executables
BuildMain()
BuildClient()
BuildServer()

# Copy necessary files
CopyFiles()
