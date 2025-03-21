import PyInstaller.__main__
import os
import shutil

ICON_PATH = "Assets" + os.pathsep + "Images" + os.pathsep + "IconsAndLogos" + os.pathsep + "MMLogo.ico"
OUTPUT_DIR = "output"

def BuildClient():
    PyInstaller.__main__.run([
        '--onefile',
        '--windowed',
        '--icon', ICON_PATH,
        '--distpath', OUTPUT_DIR,
        'Client.py'
    ])

def BuildServer():
    PyInstaller.__main__.run([
        '--onefile',
        '--icon', ICON_PATH,
        '--distpath', OUTPUT_DIR,
        'Server.py'
    ])

def BuildMain():
    PyInstaller.__main__.run([
        '--onefile',
        '--windowed',
        '--icon', ICON_PATH,
        '--distpath', OUTPUT_DIR,
        'Main.py'
    ])

def CopyFiles():
    """ Copies necessary files to the output directory. """

    shutil.copy("SETTINGS.toml", OUTPUT_DIR)
    shutil.copytree("Assets", os.path.join(OUTPUT_DIR, "Assets"), dirs_exist_ok=True)


# Build executables
BuildMain()
BuildClient()
BuildServer()

# Copy necessary files
CopyFiles()
